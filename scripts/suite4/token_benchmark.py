#!/usr/bin/env python3.12
"""
Suite-4 Token Benchmark: SQL vs BKN
用 LangChain Agent + MiniMax（OpenAI 兼容）跑样本题，精确记录 token 消耗。
"""
import os
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DATAVIEW_ID = "4bebeb86-838b-478c-b51a-b5f81041042d"
CATALOG = 'mysql_1j6tsjwo."supply_chain_data"'
BKN_KN = "supplychain_bkn_v4"

TABLES = [
    "inventory_event", "bom_event", "mrp_plan_order_event",
    "purchase_order_event", "purchase_requisition_event",
    "sales_order_event", "forecast_event", "production_order_event",
    "shipment_event", "material_requisition_event",
    "product_entity", "material_entity", "supplier_entity",
    "customer_entity", "factory_entity", "warehouse_entity",
]

QUESTIONS = [
    ("Q-F1-01", "霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？"),
    ("Q-F2-02", "预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？"
                "缺料最严重的前5颗物料是哪些？各自缺口数量是多少？"),
]

MAX_OUTPUT = int(os.environ.get("MAX_TOOL_OUTPUT", "80000"))
BKN_MAX_OUTPUT = int(os.environ.get("BKN_MAX_TOOL_OUTPUT", "20000"))

KEEP_FIELDS = None  # populated per-query by bkn_get


def _run(args, truncate=MAX_OUTPUT):
    r = subprocess.run(args, capture_output=True, text=True, timeout=60)
    out = r.stdout or r.stderr or ""
    if r.returncode != 0:
        return f"ERROR (exit {r.returncode}): {out[:truncate]}"
    return out[:truncate]


def _trim_schema(raw: str) -> str:
    """Extract only name/display_name/type/comment from bkn_get output."""
    try:
        data = json.loads(raw)
        entries = data.get("entries", [data] if "data_properties" in data else [])
        result = []
        for entry in entries:
            ot = {"id": entry.get("id"), "name": entry.get("name"), "fields": []}
            for prop in entry.get("data_properties", []):
                ot["fields"].append({
                    "name": prop.get("name"),
                    "display_name": prop.get("display_name"),
                    "type": prop.get("type"),
                    "comment": prop.get("comment", ""),
                })
            result.append(ot)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except (json.JSONDecodeError, KeyError):
        return raw[:BKN_MAX_OUTPUT]


def _trim_query_rows(raw: str, max_chars: int = BKN_MAX_OUTPUT) -> str:
    """Convert query results to compact TSV format, removing internal fields."""
    try:
        data = json.loads(raw)
        datas = data.get("datas", [])
        if not datas:
            return f"(0 rows returned)"
        skip_keys = {"_score", "_display", "_instance_id", "_instance_identity"}
        cols = [k for k in datas[0].keys() if k not in skip_keys]
        lines = ["\t".join(cols)]
        for row in datas:
            lines.append("\t".join(str(row.get(c, "")) for c in cols))
        result = f"({len(datas)} rows)\n" + "\n".join(lines)
        if len(result) <= max_chars:
            return result
        # Truncate rows if still too large
        while len(lines) > 2:  # keep header + at least 1 row
            lines.pop()
            result = f"({len(lines)-1}/{len(datas)} rows, truncated)\n" + "\n".join(lines)
            if len(result) <= max_chars:
                return result
        return result[:max_chars]
    except (json.JSONDecodeError, KeyError):
        return raw[:max_chars]


# ── SQL tools ────────────────────────────────────────────────

@tool
def sql_query(sql: str) -> str:
    """Execute a SQL query on the supply chain dataview.
    Table names must use the catalog prefix, e.g.:
      SELECT * FROM mysql_1j6tsjwo."supply_chain_data".inventory_event LIMIT 5
    Returns JSON with entries array."""
    return _run(["kweaver", "dataview", "query", DATAVIEW_ID, "--sql", sql, "--pretty"])


@tool
def sql_schema(table_name: str) -> str:
    """Get column names of a table by fetching 1 row.
    Pass ONLY the table name (e.g. 'inventory_event'), not the full path."""
    sql = f'SELECT * FROM {CATALOG}.{table_name} LIMIT 1'
    return _run(["kweaver", "dataview", "query", DATAVIEW_ID, "--sql", sql, "--pretty"])


# ── BKN tools ────────────────────────────────────────────────

_bkn_query_cache: dict[str, str] = {}

@tool
def bkn_get(object_type: str) -> str:
    """Get schema of a BKN object type: field name, display_name, type, comment.
    Example: bkn_get('inventory_event')"""
    raw = _run(["kweaver", "bkn", "object-type", "get", BKN_KN, object_type, "--pretty"])
    return _trim_schema(raw)


@tool
def bkn_query(object_type: str, condition_json: str = "", limit: int = 20) -> str:
    """Query instances of a BKN object type with server-side filtering.
    Returns TSV table. DO NOT call with same object_type+condition twice — results are stable.

    condition_json: a FULL JSON body string, e.g.:
      {"limit":20,"condition":{"field":"item_name","operation":"==","value":"霸风20L植保无人机"}}

    Supported operations: ==, !=, >, >=, <, <=, in, not_in, like, not_like
    Combine with: {"operation":"and","sub_conditions":[...]}

    IMPORTANT: ALWAYS provide condition_json to filter results!
    If empty, only limit is applied (max 5 rows without condition)."""
    cache_key = f"{object_type}|{condition_json}"
    if cache_key in _bkn_query_cache:
        return "(与上次查询结果完全相同，请直接使用之前返回的数据)"
    args = ["kweaver", "bkn", "object-type", "query", BKN_KN, object_type]
    if condition_json:
        args.append(condition_json)
    else:
        args.extend(["--limit", "5"])
    args.append("--pretty")
    raw = _run(args, truncate=MAX_OUTPUT)
    result = _trim_query_rows(raw, max_chars=BKN_MAX_OUTPUT)
    _bkn_query_cache[cache_key] = result
    return result


# ── Token tracking via OpenAI client patch ───────────────────

class _TokenAccumulator:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.calls = 0

    def reset(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.calls = 0


token_counter = _TokenAccumulator()


def _patch_chat_openai():
    """Patch ChatOpenAI._stream to capture token usage from stream chunks."""
    _orig_stream = ChatOpenAI._stream

    def _tracked_stream(self, messages, stop=None, run_manager=None, **kwargs):
        for chunk in _orig_stream(self, messages, stop=stop, run_manager=run_manager, **kwargs):
            yield chunk
            msg = getattr(chunk, "message", None)
            meta = getattr(msg, "usage_metadata", None) if msg else None
            if meta and (meta.get("input_tokens") or meta.get("output_tokens")):
                token_counter.calls += 1
                token_counter.prompt_tokens += meta.get("input_tokens", 0)
                token_counter.completion_tokens += meta.get("output_tokens", 0)
                token_counter.total_tokens += meta.get("input_tokens", 0) + meta.get("output_tokens", 0)

    ChatOpenAI._stream = _tracked_stream


_patch_chat_openai()


# ── Agent runner ─────────────────────────────────────────────

def make_agent(tools, system_msg):
    model = os.environ.get("OPENAI_MODEL", "MiniMax-M2.5")
    llm = ChatOpenAI(model=model, temperature=0, streaming=False,
                      model_kwargs={"stream_options": {"include_usage": True}})
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_msg),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10,
                         return_intermediate_steps=True)


def run_with_tracking(executor, question):
    token_counter.reset()
    result = executor.invoke({"input": question})

    tool_calls_info = []
    total_tool_input_chars = 0
    total_tool_output_chars = 0
    for action, observation in result.get("intermediate_steps", []):
        inp = json.dumps(action.tool_input, ensure_ascii=False) if isinstance(action.tool_input, dict) else str(action.tool_input)
        out_len = len(str(observation))
        tool_calls_info.append({
            "tool": action.tool,
            "input_chars": len(inp),
            "output_chars": out_len,
        })
        total_tool_input_chars += len(inp)
        total_tool_output_chars += out_len

    return {
        "answer": result["output"],
        "prompt_tokens": token_counter.prompt_tokens,
        "completion_tokens": token_counter.completion_tokens,
        "total_tokens": token_counter.total_tokens,
        "llm_calls": token_counter.calls,
        "tool_calls": tool_calls_info,
        "tool_input_chars": total_tool_input_chars,
        "tool_output_chars": total_tool_output_chars,
    }


SQL_SYSTEM = f"""你是供应链数据分析专家。用 SQL 查询回答问题。
catalog 前缀: {CATALOG}
可用表: {', '.join(TABLES)}
步骤: 1) 用 sql_schema 查字段  2) 写 SELECT 拉数  3) 归纳答案。简洁作答。"""

_BKN_SCHEMA = """inventory_event(库存清单): quantity(数量,int), warehouse_name(仓库名称), item_code(物料编码), item_name(物料名称), item_id(物料ID), item_type(物料类型), warehouse_id(仓库ID), status(状态), storage_reason(入库原因), unit_price(单价,float), total_price(总金额,float), inventory_id(库存记录ID,PK), snapshot_month(快照月份), month_end_qty(月末数量), movement_type, shortage_flag, batch_number(批次号)
mrp_plan_order_event(物料需求计划): mrp_id(MRP记录ID,PK), materialplanid_name(物料名称), materialplanid_number(物料编码), bizorderqty(确认需求数量,int), bizdropqty(确认投放数量,int), adviseorderqty(建议下达数量,int), rootdemandbillno(根需求单号), dropstatus_title(投放状态), closestatus_title(关闭状态), materialattr_title(物料属性), customer_name(客户名称), sales_order_number(销售订单号), billno(单号), status(状态), orderdate(订单日期), startdate, enddate, availabledate(可用日期), project_name(项目名称)
product_entity(产品): product_id(PK), product_code(产品编码), product_name(产品名称), product_type, main_unit, status
forecast_event(预测单): forecast_id(PK), billno(单号), material_name, material_number, qty(数量,int), customer_name, sales_order_number, forecast_month, status
purchase_order_event(采购订单): purchase_order_id(PK), purchase_order_number, material_name, material_code, purchase_quantity(int), supplier_name, planned_arrival_date, document_status, srcbillid(来源MRP)
shipment_event(发货单): shipment_id(PK), product_name, product_code, quantity(int), delivery_status, shipment_date, estimated_delivery_date, customer_name, warehouse_name
bom_event(BOM): bom_id(PK), parent_code(父件编码), child_code(子件编码), child_name(子件名称), quantity(float), scrap_rate(损耗率), bom_version
material_entity(物料): material_id(PK), material_code, material_name, material_type, unit, status
supplier_entity(供应商): supplier_id(PK), supplier_name, supplier_code, lead_time_avg(平均交期,int), risk_level, status
production_order_event(生产工单): production_order_id(PK), production_order_number, output_name, output_code, production_quantity(int), planned_start_date, planned_finish_date, work_order_status, factory_name
purchase_requisition_event(采购申请): pr_id(PK), billno, material_name, material_number, qty(int), status, srcbillid(来源MRP)
sales_order_event(销售订单): sales_order_id(PK), sales_order_number, product_name, product_code, quantity(int), customer_name, planned_delivery_date, order_status"""

_BKN_SYSTEM = (
    "你是供应链数据分析专家。用 BKN 知识网络 API 回答问题。\n"
    f"知识网络: {BKN_KN}\n\n"
    "=== 对象类 Schema ===\n"
    f"{_BKN_SCHEMA}\n\n"
    "=== 查询规则 ===\n"
    "Schema 已内置，无需调用 bkn_get。直接用 bkn_query 查数据，务必带 condition 过滤。\n"
    "返回格式为 TSV（制表符分隔），直接分析即可。\n\n"
    'condition 语法（传给 condition_json）:\n'
    '  {"limit":20,"condition":{"field":"item_name","operation":"==","value":"霸风20L植保无人机"}}\n'
    '  {"limit":20,"condition":{"operation":"and","sub_conditions":[{"field":"F1","operation":"==","value":"V1"},{"field":"F2","operation":"==","value":"V2"}]}}\n\n'
    "操作符: ==, !=, >, >=, <, <=, in, not_in, like, not_like（禁用 eq/gt/lt）\n"
    "简洁作答。"
)
BKN_SYSTEM = _BKN_SYSTEM


def main():
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "test_report", "suite-4", f"token_benchmark_{ts}")
    os.makedirs(out_dir, exist_ok=True)

    sql_agent = make_agent([sql_query, sql_schema], SQL_SYSTEM)
    bkn_agent = make_agent([bkn_get, bkn_query], BKN_SYSTEM)

    results = []
    for qid, qtxt in QUESTIONS:
        print(f"\n{'='*60}\n{qid}: {qtxt}\n{'='*60}", flush=True)

        print("\n▶ SQL path", flush=True)
        sql_res = run_with_tracking(sql_agent, qtxt)
        print(f"  tokens: {sql_res['total_tokens']} (prompt={sql_res['prompt_tokens']}, "
              f"completion={sql_res['completion_tokens']})", flush=True)

        print("\n▶ BKN path", flush=True)
        _bkn_query_cache.clear()
        bkn_res = run_with_tracking(bkn_agent, qtxt)
        print(f"  tokens: {bkn_res['total_tokens']} (prompt={bkn_res['prompt_tokens']}, "
              f"completion={bkn_res['completion_tokens']})", flush=True)

        results.append({"id": qid, "question": qtxt, "sql": sql_res, "bkn": bkn_res})

    with open(os.path.join(out_dir, "token_benchmark.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    md = gen_report(results)
    report_path = os.path.join(out_dir, "token_benchmark_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\n{'='*60}", flush=True)
    print(f"✅ 结果已保存: {out_dir}", flush=True)
    print(f"   报告: {report_path}", flush=True)


def _r(a, b):
    if not b:
        return "N/A"
    return f"{a / b:.1f}x"


def gen_report(results):
    lines = [
        "# Suite-4 Token Benchmark: SQL vs BKN\n",
        f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**模型**: {os.environ.get('OPENAI_MODEL', 'MiniMax-M2.5')}  ",
        f"**样本**: {len(results)} 题\n",
    ]

    totals = {"sql_prompt": 0, "sql_comp": 0, "sql_total": 0,
              "bkn_prompt": 0, "bkn_comp": 0, "bkn_total": 0,
              "sql_tool_out": 0, "bkn_tool_out": 0}

    for r in results:
        s, b = r["sql"], r["bkn"]
        totals["sql_prompt"] += s["prompt_tokens"]
        totals["sql_comp"] += s["completion_tokens"]
        totals["sql_total"] += s["total_tokens"]
        totals["sql_tool_out"] += s["tool_output_chars"]
        totals["bkn_prompt"] += b["prompt_tokens"]
        totals["bkn_comp"] += b["completion_tokens"]
        totals["bkn_total"] += b["total_tokens"]
        totals["bkn_tool_out"] += b["tool_output_chars"]

        ratio_t = b["total_tokens"] / s["total_tokens"] if s["total_tokens"] else 0
        lines.append(f"## {r['id']}\n")
        lines.append(f"**问题**: {r['question']}\n")
        lines.append("| 指标 | SQL | BKN | 倍率 |")
        lines.append("|------|-----|-----|------|")
        lines.append(f"| prompt tokens | {s['prompt_tokens']:,} | {b['prompt_tokens']:,} | {_r(b['prompt_tokens'], s['prompt_tokens'])} |")
        lines.append(f"| completion tokens | {s['completion_tokens']:,} | {b['completion_tokens']:,} | {_r(b['completion_tokens'], s['completion_tokens'])} |")
        lines.append(f"| **total tokens** | **{s['total_tokens']:,}** | **{b['total_tokens']:,}** | **{ratio_t:.1f}x** |")
        lines.append(f"| LLM 调用次数 | {s['llm_calls']} | {b['llm_calls']} | — |")
        lines.append(f"| 工具调用次数 | {len(s['tool_calls'])} | {len(b['tool_calls'])} | — |")
        lines.append(f"| 工具返回数据量 | {s['tool_output_chars']:,} chars | {b['tool_output_chars']:,} chars | {_r(b['tool_output_chars'], s['tool_output_chars'])} |")
        lines.append("")

        lines.append("<details><summary>工具调用明细</summary>\n")
        for label, data in [("SQL", s), ("BKN", b)]:
            lines.append(f"**{label}**:\n")
            for i, tc in enumerate(data["tool_calls"], 1):
                lines.append(f"  {i}. `{tc['tool']}` — input {tc['input_chars']:,} chars → output {tc['output_chars']:,} chars")
            lines.append("")
        lines.append("</details>\n")

    ratio_total = totals["bkn_total"] / totals["sql_total"] if totals["sql_total"] else 0
    lines.append("## 汇总\n")
    lines.append("| 指标 | SQL | BKN | 倍率 |")
    lines.append("|------|-----|-----|------|")
    lines.append(f"| prompt tokens | {totals['sql_prompt']:,} | {totals['bkn_prompt']:,} | {_r(totals['bkn_prompt'], totals['sql_prompt'])} |")
    lines.append(f"| completion tokens | {totals['sql_comp']:,} | {totals['bkn_comp']:,} | {_r(totals['bkn_comp'], totals['sql_comp'])} |")
    lines.append(f"| **total tokens** | **{totals['sql_total']:,}** | **{totals['bkn_total']:,}** | **{ratio_total:.1f}x** |")
    lines.append(f"| 工具返回数据量 | {totals['sql_tool_out']:,} chars | {totals['bkn_tool_out']:,} chars | {_r(totals['bkn_tool_out'], totals['sql_tool_out'])} |")
    n = len(results)
    avg_sql = totals["sql_total"] / n if n else 0
    avg_bkn = totals["bkn_total"] / n if n else 0
    lines.append(f"| 单题平均 tokens | {avg_sql:,.0f} | {avg_bkn:,.0f} | {ratio_total:.1f}x |")
    lines.append(f"| **24 题外推** | **{avg_sql * 24:,.0f}** | **{avg_bkn * 24:,.0f}** | **{ratio_total:.1f}x** |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
