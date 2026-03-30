# -*- coding: utf-8 -*-
"""Parse test-cases/suite-3/cases/*.md and write suite-3_cases.csv"""
from __future__ import absolute_import, print_function

import csv
import os
import re
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CASES_DIR = os.path.join(_ROOT, "test-cases", "suite-3", "cases")
OUT_CSV = os.path.join(CASES_DIR, "suite-3_cases.csv")

FILES = [
    ("S1", "S1_规范查询.md"),
    ("S2", "S2_口语模糊查询.md"),
    ("S3", "S3_追问下钻.md"),
    ("S4", "S4_异常边界.md"),
    ("S5", "S5_多意图混合.md"),
]

FIELD_PATTERNS = [
    ("behavior_type", re.compile(r"^\*\*行为类型\*\*:\s*(.*)$")),
    ("function_category", re.compile(r"^\*\*功能类别\*\*:\s*(.*)$")),
    ("user_role", re.compile(r"^\*\*用户角色\*\*:\s*(.*)$")),
    ("question", re.compile(r"^\*\*问题\*\*:\s*(.*)$")),
    ("context", re.compile(r"^\*\*上文假设\*\*:\s*(.*)$")),
    ("expected_behavior", re.compile(r"^\*\*预期行为\*\*:\s*(.*)$")),
    ("involved_objects", re.compile(r"^\*\*涉及对象\*\*:\s*(.*)$")),
    ("key_fields", re.compile(r"^\*\*关键字段\*\*:\s*(.*)$")),
]


def parse_case_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Split by **Qxx** blocks
    blocks = re.split(r"\n(?=\*\*Q\d{2}\*\*)", text)
    cases = []
    for block in blocks:
        block = block.strip()
        if not block.startswith("**Q"):
            continue
        m = re.match(r"^\*\*(Q\d{2})\*\*", block)
        if not m:
            continue
        qid = m.group(1)
        lines = block.split("\n")
        rec = {
            "question_id": qid,
            "behavior_type": "",
            "function_category": "",
            "user_role": "",
            "question": "",
            "context": "",
            "expected_behavior": "",
            "involved_objects": "",
            "key_fields": "",
            "standard_answer": "",
        }
        i = 1
        in_answer = False
        answer_lines = []
        while i < len(lines):
            line = lines[i]
            if line.strip() == "**标准答案**:":
                in_answer = True
                i += 1
                continue
            if in_answer:
                if line.strip().startswith("---"):
                    break
                answer_lines.append(line)
                i += 1
                continue
            matched = False
            for key, pat in FIELD_PATTERNS:
                mm = pat.match(line.strip())
                if mm:
                    rec[key] = mm.group(1).strip()
                    matched = True
                    break
            if not matched and line.strip() and not line.strip().startswith("#"):
                pass
            i += 1
        rec["standard_answer"] = "\n".join(answer_lines).strip()
        cases.append(rec)
    return cases


def main():
    rows = []
    for suite_id, fname in FILES:
        path = os.path.join(CASES_DIR, fname)
        if not os.path.isfile(path):
            print("Missing:", path, file=sys.stderr)
            sys.exit(1)
        for rec in parse_case_file(path):
            rows.append(
                {
                    "suite_group": suite_id,
                    "suite_file": fname,
                    "question_id": rec["question_id"],
                    "behavior_type": rec["behavior_type"],
                    "function_category": rec["function_category"],
                    "user_role": rec["user_role"],
                    "question": rec["question"],
                    "context": rec["context"],
                    "expected_behavior": rec["expected_behavior"],
                    "involved_objects": rec["involved_objects"],
                    "key_fields": rec["key_fields"],
                    "standard_answer": rec["standard_answer"],
                }
            )

    fieldnames = [
        "suite_group",
        "suite_file",
        "question_id",
        "behavior_type",
        "function_category",
        "user_role",
        "question",
        "context",
        "expected_behavior",
        "involved_objects",
        "key_fields",
        "standard_answer",
    ]
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)
    print("Wrote %d rows -> %s" % (len(rows), OUT_CSV))
    return 0


if __name__ == "__main__":
    main()
