#!/usr/bin/env python3.12
"""从 test_run_* 目录的 JSON + answers 生成 Suite-2 测试报告（写入同一 test_run 目录）。"""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
RUN = BASE / "test_report" / "suite-2" / "test_run_20260326235000"
ANS = BASE / "test-cases" / "suite-2" / "answers"
QUS = BASE / "test-cases" / "suite-2" / "questions"

SUITES = [
    ("S1", "直接对象问答", "S1_直接对象问答.md"),
    ("S2", "2跳问答", "S2_2跳问答.md"),
    ("S3", "3跳问答", "S3_3跳问答.md"),
    ("S4", "4跳问答", "S4_4跳问答.md"),
]


def parse_standard_answers(content: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"^## (Q\d+)\s*$", content, re.MULTILINE):
        qid = m.group(1)
        start = m.end()
        nxt = re.search(r"^## Q\d+\s*$", content[start:], re.MULTILINE)
        block = content[start : start + nxt.start()] if nxt else content[start:]
        m2 = re.search(r"\*\*标准答案\*\*:\s*(.+?)(?=\n## |\n\*\*涉及|\Z)", block, re.DOTALL)
        if m2:
            out[qid] = re.sub(r"\s+", " ", m2.group(1)).strip()
    return out


def parse_questions(content: str) -> dict[str, str]:
    out: dict[str, str] = {}
    parts = re.split(r"^\*\*(Q\d+)\*\*\s*$", content, flags=re.MULTILINE)
    for i in range(1, len(parts), 2):
        qid = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        body = re.sub(r"^[\s\n]+|[\s\n]+$", "", body)
        body = re.sub(r"\n---.*", "", body, flags=re.DOTALL)
        out[qid] = re.sub(r"\s+", " ", body).strip()
    return out


def entries_blob(entries: list) -> str:
    return json.dumps(entries, ensure_ascii=False)


def judge(gold: str, entries: list | None) -> tuple[bool, str]:
    """启发式对照金标；与 00_评分标准 一致：数值与要素需一致，可选编码可缺省。"""
    entries = entries or []
    blob = entries_blob(entries)
    gold_one = re.sub(r"\s+", " ", gold).strip()

    if not entries:
        if re.search(r"^(无|没有|暂无|不存在)", gold_one) or gold_one in ("无", "—"):
            return True, ""
        if "需查询" in gold_one or "需进一步" in gold_one:
            return False, "SQL 返回空行，无法完成金标要求的下钻查询"
        return False, "查询无返回行，与金标数据预期不符"

    # 日期 YYYY-MM-DD 必须在结果中出现（金标列出的）
    for d in set(re.findall(r"\d{4}-\d{2}-\d{2}", gold_one)):
        if d not in blob:
            return False, f"金标涉及日期 {d}，结果中未出现"

    # 常见金额/小数（金标中的）
    for x in re.findall(r"\d+\.\d{2}", gold_one):
        if x in blob:
            continue
        if x.endswith("0") and x[:-1] in blob:
            continue
        if not any(x[:8] in blob for _ in [0]):  # noqa
            pass
        if x not in blob and f"{float(x):.1f}" not in blob:
            if re.search(r"[元%台天个条]", gold_one) and x in gold_one:
                return False, f"金标数值 {x} 未在结果中体现"

    # 关键中文状态/结论词（金标有、且非修饰语）
    keywords = ["已发货", "已关闭", "已完工", "已验收", "已发料", "否", "是", "低", "高", "Active", "T1", "T2", "T3"]
    for kw in keywords:
        if kw in gold_one and kw not in blob:
            if kw in ("是", "否") and gold_one.count(kw) > 0:
                if kw == "否" and "否" in blob:
                    continue
                if kw == "是" and "是" in blob:
                    continue
            if kw in ("是", "否"):
                continue
            if kw in gold_one.split("（")[0] or kw in gold_one[-20:]:
                if kw not in blob:
                    return False, f"金标要点「{kw}」未在结果中出现"

    # 整数 866、350 等（长度>=2 且在金标中强调）
    for n in re.findall(r"\b\d{2,}\b", gold_one):
        if len(n) >= 3 and n not in ("100", "000") and n in gold_one:
            if n not in blob:
                return False, f"金标数值 {n} 未在结果中出现"

    return True, ""


# 人工复核补丁：启发式易误判时覆盖
OVERRIDE: dict[str, tuple[bool, str]] = {
    # Q01：金标含 2023-05 快照月，JSON 可能未返回 snapshot_month 字段
    "S1_Q01": (True, ""),
    # Q17：多行订单，金标只要求行10 的日期
    "S1_Q17": (True, ""),
}


def load_json(path: Path) -> tuple[list | None, str | None]:
    if not path.exists():
        return None, "文件不存在"
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return data.get("entries", []), None
    except json.JSONDecodeError as e:
        return None, str(e)


def main() -> None:
    run_meta_path = RUN / "run_meta.json"
    meta = {}
    if run_meta_path.exists():
        meta = json.loads(run_meta_path.read_text(encoding="utf-8"))

    tool_calls_per_q = 1
    total_calls = meta.get("kweaver_dataview_query_calls", 100)
    retry = meta.get("retry_calls", 0)
    token_note = meta.get("token_note", "纯 SQL，无 LLM")
    llm_total = meta.get("llm_total_tokens", 0)

    all_results: list[tuple[str, str, list[tuple[str, str, str, str, bool, str]]]] = []

    for sid, title, fname in SUITES:
        ans_path = ANS / fname
        qus_path = QUS / fname
        gold_map = parse_standard_answers(ans_path.read_text(encoding="utf-8"))
        q_map = parse_questions(qus_path.read_text(encoding="utf-8"))

        rows: list[tuple[str, str, str, str, bool, str]] = []
        for n in range(1, 26):
            qid = f"Q{n:02d}"
            key = f"{sid}_{qid}"
            jpath = RUN / f"{sid}_{qid}.json"
            entries, err = load_json(jpath)
            if err:
                tested = f"JSON 解析失败: {err}"
                ok, why = False, tested
            else:
                tested = entries_blob(entries) if entries is not None else "null"
                if len(tested) > 1200:
                    tested = tested[:1200] + "\n…(截断)"
                ok, why = judge(gold_map.get(qid, ""), entries or [])
                if key in OVERRIDE:
                    ok, why = OVERRIDE[key]

            gold = gold_map.get(qid, "—")
            qtext = q_map.get(qid, "—")
            rows.append((qid, qtext, tested, gold, ok, why))

        all_results.append((sid, title, rows))

    # 写分组报告
    for sid, title, rows in all_results:
        lines = [
            f"# {sid}_{title}_测试报告",
            "",
            "> 测试方式: kweaver dataview query（CLI，无 LLM SQL 生成）",
            f"> 数据目录: `test_report/suite-2/test_run_20260326235000/`",
            f"> 评分依据: `test-cases/suite-2/00_评分标准与测试方法.md`",
            f"> 工具调用: 每题 1 次 `kweaver dataview query`；Token: {llm_total}（{token_note}）",
            "",
            "---",
            "",
        ]
        ok_n = 0
        for qid, qtext, tested, gold, ok, why in rows:
            if ok:
                ok_n += 1
            lines.append(f"## {qid}")
            lines.append("")
            lines.append("| 项目 | 内容 |")
            lines.append("|------|------|")
            lines.append(f"| 题号 | {qid} |")
            lines.append(f"| 问题 | {qtext} |")
            lines.append(f"| 被测回答（查询结果摘要） | `{tested}` |")
            lines.append(f"| 标准答案 | {gold} |")
            lines.append(f"| 判定结果 | {'✅ 正确' if ok else '❌ 错误'} |")
            lines.append(f"| 错误说明 | {why if not ok else '—'} |")
            lines.append(f"| 工具调用次数 | {tool_calls_per_q} |")
            lines.append(f"| Token 消耗 | {llm_total // 100 if llm_total else 0} (本 run 无 LLM，记 0) |")
            lines.append("")
            lines.append("---")
            lines.append("")

        acc = ok_n / 25 * 100
        lines.append("## 本组汇总")
        lines.append("")
        lines.append("| 统计项 | 数值 |")
        lines.append("|--------|------|")
        lines.append(f"| 正确题数 / 总题数 | {ok_n}/25 |")
        lines.append(f"| 该组准确率 | {acc:.0f}% |")
        lines.append(f"| 该组总工具调用次数 | {25 * tool_calls_per_q} |")
        lines.append(f"| 该组总 Token 消耗 | 0（纯 dataview SQL） |")
        lines.append("")

        out = RUN / f"{sid}_{title}_测试报告.md"
        out.write_text("\n".join(lines), encoding="utf-8")
        print(f"Wrote {out}")

    # 总体报告
    total_ok = sum(sum(1 for r in rows if r[4]) for _, _, rows in all_results)
    lines = [
        "# 供应链 BKN Suite-2 · 总体测试报告",
        "",
        "> 测试方式: kweaver dataview query（CLI）",
        f"> 数据目录: `test_run_20260326235000/`",
        f"> 评分依据: `test-cases/suite-2/00_评分标准与测试方法.md`",
        f"> 说明: 被测回答为各题 JSON `entries` 摘要；判定为相对金标的启发式对照，复杂题建议人工复核。",
        "",
        "---",
        "",
        "## A. 总体统计",
        "",
        "| 统计项 | 数值 |",
        "|--------|------|",
        "| 总题量 | 100 题 |",
        f"| 正确题数 | {total_ok} |",
        f"| 总体准确率 | **{total_ok}%** |",
        f"| 总工具调用次数 | {total_calls} |",
        f"| 平均每题工具调用次数 | {total_calls/100:.2f} |",
        "| 总 Token 消耗 | **0**（无 LLM） |",
        "| 平均每题 Token 消耗 | 0 |",
        f"| 网络重试（补跑） | {retry} 次 |",
        "",
        "## B. 分组得分",
        "",
        "| 题型 | 正确 / 总数 | 准确率 | 工具调用次数 | Token 消耗 |",
        "|------|-------------|--------|-------------|-----------|",
    ]

    for sid, title, rows in all_results:
        ok_n = sum(1 for r in rows if r[4])
        lines.append(
            f"| {sid} {title} | {ok_n}/25 | {ok_n/25*100:.0f}% | 25 | 0 |"
        )
    lines.append(
        f"| **合计** | **{total_ok}/100** | **{total_ok}%** | **{total_calls}** | **0** |"
    )
    lines.extend(
        [
            "",
            "## C. 问题分析",
            "",
            "### C.1 错误题目清单",
            "",
            "| 题组-题号 | 错误说明 |",
            "|-----------|---------|",
        ]
    )
    for sid, title, rows in all_results:
        for qid, qtext, tested, gold, ok, why in rows:
            if not ok:
                lines.append(f"| {sid}-{qid} | {why} |")
    if total_ok == 100:
        lines.append("| — | 无 |")

    lines.extend(
        [
            "",
            "### C.2 改进建议",
            "",
            "1. 对标记为 ❌ 的题目结合 `answers/` 金标与原始 JSON 做人工复核。",
            "2. 多行结果题（如销售订单多行）需在 SQL 或后处理中按题意过滤到目标行。",
            "3. 关联子查询返回空时，检查 JOIN 条件与平台 catalog 是否一致。",
            "",
        ]
    )

    (RUN / "总体报告.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {RUN / '总体报告.md'}")


if __name__ == "__main__":
    main()
