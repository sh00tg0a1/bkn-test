#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple


ORDERED_FILES = [
    "S1_交期判断.md",
    "S2_晨会全局扫描.md",
    "S3_物料跟催.md",
    "S4_风险预警播报.md",
    "S5_计划执行日报.md",
    "S6_深度追问与综合场景.md",
    "S7_边界与异常处理.md",
]

AGENT_ID = "01KFT0E68A1RES94ZV6DA131X4"


@dataclass
class Row:
    qid: str
    scene: str
    role: str
    question: str
    gold: str
    agent_answer: str
    call_success: bool
    exit_code: int
    latency_sec: float
    consistency: str
    score_accuracy: int
    score_conclusion: int
    score_action: int
    score_coherence: int
    score_total: int
    veto: bool
    veto_reason: str
    passed: bool
    diff_note: str


def parse_questions(md_text: str, scene: str) -> List[dict]:
    lines = md_text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        m = re.match(r"^\*\*(Q\d{2})\*\*（([^）]+)）\s*(.*)$", lines[i].strip())
        if not m:
            i += 1
            continue
        qid, role, inline_q = m.group(1), m.group(2), m.group(3).strip()
        if inline_q:
            question = inline_q
            i += 1
        else:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            question = lines[j].strip() if j < len(lines) else ""
            i = j + 1
        out.append({"qid": qid, "scene": scene, "role": role, "question": question})
    return out


def parse_answers(md_text: str) -> Dict[str, str]:
    lines = md_text.splitlines()
    out: Dict[str, str] = {}
    current_qid = None
    buf: List[str] = []
    for line in lines:
        m = re.match(r"^##\s+(Q\d{2})\s*", line.strip())
        if m:
            if current_qid:
                out[current_qid] = "\n".join(x for x in buf if x.strip()).strip()
            current_qid = m.group(1)
            buf = []
            continue
        if current_qid is not None:
            buf.append(line)
    if current_qid:
        out[current_qid] = "\n".join(x for x in buf if x.strip()).strip()
    return out


def clean_answer(stdout: str) -> str:
    t = (stdout or "").strip()
    marker = "\n\nTo continue this conversation"
    if marker in t:
        t = t.split(marker, 1)[0].strip()
    return t


def ask_agent(question: str, timeout_sec: int) -> Tuple[bool, int, float, str, str]:
    cmd = ["kweaver", "agent", "chat", AGENT_ID, "-m", question, "--no-stream"]
    try:
        st = time.time()
        timeout = None if timeout_sec <= 0 else timeout_sec
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        latency = round(time.time() - st, 3)
        ans = clean_answer(proc.stdout)
        return proc.returncode == 0 and bool(ans), proc.returncode, latency, ans, (proc.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return False, 124, float(timeout_sec), "", "TIMEOUT"


def tokens(text: str) -> List[str]:
    pats = [
        r"\bQ\d{2}\b",
        r"\b\d{3}-\d{6}\b",
        r"\bYCD\d{16}\b",
        r"\bMRP-\d{8}(?:-\d+)?\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d+\b",
    ]
    arr: List[str] = []
    for p in pats:
        arr.extend(re.findall(p, text))
    seen = set()
    out = []
    for a in arr:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


def score_one(question: str, gold: str, ans: str, call_success: bool, exit_code: int) -> Tuple[Dict[str, int], bool, str, str, str]:
    if not call_success or not ans.strip():
        return ({"acc": 0, "con": 0, "act": 0, "coh": 0}, True, "无有效回答（超时或空答案）", "❌", "Agent 未返回可评估文本")

    first_sentence = ans.split("\n", 1)[0]
    con = 20 if any(k in first_sentence for k in ["结论", "高风险", "低风险", "可以", "不能", "是", "否"]) else 10
    act = 25 if any(k in ans for k in ["今天", "本周", "建议", "需要", "应", "先", "跟进"]) else 12
    coh = 15 if ("是否" in ans or ans.rstrip().endswith("？") or ans.rstrip().endswith("?")) else 8

    gold_toks = tokens(gold)
    ans_toks = set(tokens(ans))
    overlap = sum(1 for t in gold_toks if t in ans_toks)
    if not gold_toks:
        key_num = 12
    elif overlap == len(gold_toks):
        key_num = 20
    elif overlap >= max(1, len(gold_toks) // 2):
        key_num = 12
    elif overlap >= 1:
        key_num = 6
    else:
        key_num = 0

    no_fab = 10
    gap = 5 if any(k in ans for k in ["待确认", "无法", "缺口", "需核对", "暂无"]) else 2
    is_calc_q = any(k in question for k in ["多少", "率", "完成率", "齐套率", "区间"])
    calc = 5 if (not is_calc_q or any(k in ans for k in ["按", "口径", "计算", "%"])) else 2
    acc = key_num + no_fab + gap + calc

    veto = False
    veto_reason = ""
    if key_num == 0 and gold_toks:
        veto = True
        veto_reason = "关键数据与金标不存在可验证一致项（触发事实差异否决）"
    if any(k in ans for k in ["供应商：", "到货日："]) and "待系统确认" not in ans and "待确认" not in ans:
        # 仅做保守拦截，避免明显编造
        veto = True
        veto_reason = "存在潜在虚构关键字段（供应商/到货日）"

    total = acc + con + act + coh
    if veto:
        total = 0
        acc = 0
        con = 0
        act = 0
        coh = 0

    if total >= 85:
        consistency = "✅"
    elif total >= 70:
        consistency = "⚠️"
    else:
        consistency = "❌"

    diff_note = "与金标一致性较低，建议人工复核" if consistency == "❌" else ("部分一致" if consistency == "⚠️" else "高度一致")
    return ({"acc": acc, "con": con, "act": act, "coh": coh}, veto, veto_reason, consistency, diff_note)


def md_escape(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", "<br>")


def build_compare_table(row: Row) -> str:
    c_con = row.consistency
    c_data = row.consistency
    c_act = "✅" if row.score_action >= 18 else ("⚠️" if row.score_action >= 12 else "❌")
    c_gap = "✅" if any(k in row.agent_answer for k in ["待确认", "无法", "缺口", "需核对", "暂无"]) else "⚠️"
    c_fab = "❌" if row.veto and "虚构" in row.veto_reason else "✅"
    return "\n".join(
        [
            "| 对比项 | 金标答案 | Agent 回答 | 是否一致 | 准确性得分 |",
            "|---|---|---|---|---|",
            f"| 结论 | {md_escape(row.gold)} | {md_escape(row.agent_answer)} | {c_con} | - |",
            f"| 关键数据 | {md_escape(row.gold)} | {md_escape(row.agent_answer)} | {c_data} | {row.score_accuracy}/40 |",
            f"| 行动建议 | {md_escape(row.gold)} | {md_escape(row.agent_answer)} | {c_act} | - |",
            f"| 数据缺口处理 | - | {md_escape(row.agent_answer)} | {c_gap} | - |",
            f"| 虚构数据 | - | {md_escape(row.agent_answer)} | {c_fab} | - |",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--timeout-sec", type=int, default=20, help="0 means no timeout")
    args = parser.parse_args()

    root = Path(args.workspace_root)
    out_dir = Path(args.output_dir)
    result_dir = out_dir / "result"
    result_dir.mkdir(parents=True, exist_ok=True)

    questions_dir = root / "test-cases" / "questions"
    answers_dir = root / "test-cases" / "answers"

    questions: List[dict] = []
    gold_map: Dict[str, str] = {}
    for fn in ORDERED_FILES:
        scene = fn.replace(".md", "")
        q_text = (questions_dir / fn).read_text(encoding="utf-8")
        a_text = (answers_dir / fn).read_text(encoding="utf-8")
        questions.extend(parse_questions(q_text, scene))
        gold_map.update(parse_answers(a_text))

    rows: List[Row] = []
    for q in questions:
        q_path = result_dir / f"{q['qid']}.json"
        if q_path.exists():
            data = json.loads(q_path.read_text(encoding="utf-8"))
            rows.append(Row(**data))
            continue

        success, code, latency, ans, stderr = ask_agent(q["question"], args.timeout_sec)
        gold = gold_map.get(q["qid"], "")
        subs, veto, veto_reason, consistency, diff_note = score_one(q["question"], gold, ans, success, code)
        total = subs["acc"] + subs["con"] + subs["act"] + subs["coh"]
        passed = total >= 70 and subs["acc"] >= 25 and not veto
        row = Row(
            qid=q["qid"],
            scene=q["scene"],
            role=q["role"],
            question=q["question"],
            gold=gold,
            agent_answer=ans,
            call_success=success,
            exit_code=code,
            latency_sec=latency,
            consistency=consistency,
            score_accuracy=subs["acc"],
            score_conclusion=subs["con"],
            score_action=subs["act"],
            score_coherence=subs["coh"],
            score_total=total if not veto else 0,
            veto=veto,
            veto_reason=veto_reason,
            passed=passed,
            diff_note=diff_note if not stderr else f"{diff_note}；{stderr}",
        )
        rows.append(row)
        result_dir.mkdir(parents=True, exist_ok=True)
        q_path.write_text(json.dumps(asdict(row), ensure_ascii=False, indent=2), encoding="utf-8")

    (result_dir / "all_rows.json").write_text(json.dumps([asdict(r) for r in rows], ensure_ascii=False, indent=2), encoding="utf-8")

    # 答案对比汇总报告
    compare_lines = ["# 答案对比汇总报告", ""]
    for r in rows:
        compare_lines += [
            f"## {r.qid}（{r.scene}）",
            f"- 问题：{r.question}",
            f"- Agent 回答：{r.agent_answer if r.agent_answer else '【无有效回答】'}",
            f"- 金标答案：{r.gold}",
            f"- 差异说明：{r.diff_note}",
            "",
            build_compare_table(r),
            "",
            f"- 四维得分：准确性 {r.score_accuracy}/40，结论优先 {r.score_conclusion}/20，行动导向 {r.score_action}/25，连贯性 {r.score_coherence}/15",
            f"- 总分：{r.score_total}/100，是否通过：{'是' if r.passed else '否'}",
        ]
        if r.veto:
            compare_lines.append(f"- 一票否决：是（{r.veto_reason}）")
        else:
            compare_lines.append("- 一票否决：否")
        compare_lines.append("")
    (out_dir / "答案对比汇总报告.md").write_text("\n".join(compare_lines) + "\n", encoding="utf-8")

    # 分场景报告
    by_scene: Dict[str, List[Row]] = defaultdict(list)
    for r in rows:
        by_scene[r.scene].append(r)
    for scene, rs in by_scene.items():
        lines = [f"# {scene}_测试报告", ""]
        lines.append(f"- 题量：{len(rs)}")
        lines.append(f"- 调用成功率：{sum(1 for x in rs if x.call_success)}/{len(rs)} = {sum(1 for x in rs if x.call_success)/len(rs)*100:.2f}%")
        lines.append(f"- 通过率：{sum(1 for x in rs if x.passed)}/{len(rs)} = {sum(1 for x in rs if x.passed)/len(rs)*100:.2f}%")
        lines.append("")
        for r in rs:
            lines += [
                f"## {r.qid}",
                f"- 问题：{r.question}",
                f"- Agent 回答：{r.agent_answer if r.agent_answer else '【无有效回答】'}",
                f"- 金标答案：{r.gold}",
                f"- 是否一致：{r.consistency}",
                f"- 总分：{r.score_total}/100（通过：{'是' if r.passed else '否'}）",
                f"- 差异说明：{r.diff_note}",
                "",
            ]
        (out_dir / f"{scene}_测试报告.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 汇总报告
    total = len(rows)
    call_ok = sum(1 for r in rows if r.call_success)
    passed = sum(1 for r in rows if r.passed)
    veto_n = sum(1 for r in rows if r.veto)
    avg_total = sum(r.score_total for r in rows) / total if total else 0
    avg_acc = sum(r.score_accuracy for r in rows) / total if total else 0
    dist = defaultdict(int)
    for r in rows:
        if r.score_accuracy >= 35:
            dist["35-40"] += 1
        elif r.score_accuracy >= 25:
            dist["25-34"] += 1
        elif r.score_accuracy >= 15:
            dist["15-24"] += 1
        else:
            dist["0-14"] += 1
    cons = defaultdict(int)
    for r in rows:
        cons[r.consistency] += 1

    summary = [
        "# 全量测试汇总报告",
        "",
        "## 核心统计",
        f"- 总题量：{total}",
        f"- 调用次数：{total}",
        f"- 调用成功率：{call_ok}/{total} = {call_ok/total*100:.2f}%",
        f"- 通过题数：{passed}",
        f"- 被否决题数：{veto_n}",
        f"- 通过率：{passed}/{total} = {passed/total*100:.2f}%",
        f"- 平均总分：{avg_total:.2f}",
        f"- 平均准确性：{avg_acc:.2f}/40 = {avg_acc/40*100:.2f}%",
        "",
        "## 准确性分布",
        f"- 35-40：{dist['35-40']}",
        f"- 25-34：{dist['25-34']}",
        f"- 15-24：{dist['15-24']}",
        f"- 0-14：{dist['0-14']}",
        "",
        "## 与金标一致性分布",
        f"- ✅ 高度一致：{cons['✅']}",
        f"- ⚠️ 部分一致：{cons['⚠️']}",
        f"- ❌ 不一致：{cons['❌']}",
        "",
        "## 输出文件",
        "- `答案对比汇总报告.md`",
        "- `S1_交期判断_测试报告.md` ~ `S7_边界与异常处理_测试报告.md`",
        "- `result/`（逐题结果 JSON + all_rows.json）",
    ]
    (out_dir / "全量测试汇总报告.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    print(f"done total={total} call_ok={call_ok} passed={passed} output={out_dir}")


if __name__ == "__main__":
    main()
