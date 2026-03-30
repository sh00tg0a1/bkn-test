#!/usr/bin/env python3
"""Generate suite-2 markdown files from ref/suite-2/test_dataset.xlsx."""
from __future__ import annotations

import os
from collections import OrderedDict

import openpyxl

ROOT = os.path.dirname(os.path.abspath(__file__))
# ROOT = test-cases/suite-2; repo root is two levels up
REPO_ROOT = os.path.dirname(os.path.dirname(ROOT))
XLSX = os.path.join(REPO_ROOT, "ref", "suite-2", "test_dataset.xlsx")

TYPE_ORDER = [
    "直接对象问答",
    "2跳问答",
    "3跳问答",
    "4跳问答",
]

TYPE_TO_S = {
    "直接对象问答": ("S1", "直接对象问答"),
    "2跳问答": ("S2", "2跳问答"),
    "3跳问答": ("S3", "3跳问答"),
    "4跳问答": ("S4", "4跳问答"),
}


def load_rows() -> OrderedDict[str, list[tuple]]:
    wb = openpyxl.load_workbook(XLSX)
    ws = wb["供应链BKN测试集"]
    buckets: OrderedDict[str, list] = OrderedDict()
    for t in TYPE_ORDER:
        buckets[t] = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or row[0] is None:
            continue
        qtype = str(row[0]).strip()
        if qtype not in buckets:
            raise ValueError(f"Unknown question type: {qtype!r}")
        # row: 问题类型, 跳数, 问题, 涉及对象, 关键字段, 标准答案
        buckets[qtype].append(tuple(row[:6]))

    for t in TYPE_ORDER:
        if len(buckets[t]) != 25:
            raise ValueError(f"Expected 25 rows for {t!r}, got {len(buckets[t])}")
    return buckets


def esc(s: object) -> str:
    if s is None:
        return ""
    return str(s).strip()


def fmt_qnum(i: int) -> str:
    return f"Q{i:02d}"


def build_cases(sid: str, title: str, rows: list[tuple]) -> str:
    lines = [
        f"# {sid} {title} — 25题（{fmt_qnum(1)}–{fmt_qnum(len(rows))}）",
        "",
        "> **前置条件**: 阅读 [00_评分标准与测试方法.md](../00_评分标准与测试方法.md)",
        "",
        "---",
        "",
    ]
    for i, row in enumerate(rows, start=1):
        _, hops, q, objs, keys, ans = row
        lines.extend(
            [
                f"**{fmt_qnum(i)}**",
                f"**跳数**: {esc(hops)}",
                f"**问题**: {esc(q)}",
                f"**涉及对象**: {esc(objs)}",
                f"**关键字段**: {esc(keys)}",
                "",
                "**标准答案**:",
                esc(ans),
                "",
                "---",
                "",
            ]
        )
    lines.append(f"*{sid} 结束 · {len(rows)} 题（{fmt_qnum(1)}–{fmt_qnum(len(rows))}）*")
    lines.append("")
    return "\n".join(lines)


def build_questions(sid: str, title: str, rows: list[tuple]) -> str:
    lines = [
        f"# {sid} {title} — Questions（{fmt_qnum(1)}–{fmt_qnum(len(rows))}）",
        "",
        "> 前置：`../00_评分标准与测试方法.md`",
        "",
        "---",
        "",
    ]
    for i, row in enumerate(rows, start=1):
        q = esc(row[2])
        lines.extend([f"**{fmt_qnum(i)}**", q, "", "---", ""])
    return "\n".join(lines).rstrip() + "\n"


def build_answers(sid: str, title: str, rows: list[tuple]) -> str:
    lines = [
        f"# {sid} {title} — Answers（{fmt_qnum(1)}–{fmt_qnum(len(rows))}）",
        "",
    ]
    for i, row in enumerate(rows, start=1):
        objs, keys, ans = esc(row[3]), esc(row[4]), esc(row[5])
        lines.extend(
            [
                f"## {fmt_qnum(i)}",
                "",
                f"**涉及对象**: {objs}",
                "",
                f"**关键字段**: {keys}",
                "",
                f"**标准答案**: {ans}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    buckets = load_rows()
    subdirs = ("cases", "questions", "answers")
    for d in subdirs:
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)

    for qtype in TYPE_ORDER:
        sid, short = TYPE_TO_S[qtype]
        rows = buckets[qtype]
        base = f"{sid}_{short}.md"
        with open(os.path.join(ROOT, "cases", base), "w", encoding="utf-8") as f:
            f.write(build_cases(sid, short, rows))
        with open(os.path.join(ROOT, "questions", base), "w", encoding="utf-8") as f:
            f.write(build_questions(sid, short, rows))
        with open(os.path.join(ROOT, "answers", base), "w", encoding="utf-8") as f:
            f.write(build_answers(sid, short, rows))
        print("Wrote", base, len(rows), "questions")


if __name__ == "__main__":
    main()
