#!/usr/bin/env python3.12
"""Step 1: Explore hd_supply database schema, output table structures and sample data."""
from __future__ import annotations
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from db_config import get_connection


def main():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SHOW TABLES")
    tables = [r[0] for r in cur.fetchall()]
    print(f"=== Tables ({len(tables)}) ===")
    for t in tables:
        print(f"  {t}")

    schema_info = {}

    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM `{t}`")
        cnt = cur.fetchone()[0]
        print(f"\n{'='*60}")
        print(f"TABLE: {t}  ({cnt} rows)")
        print(f"{'='*60}")

        cur.execute(f"DESCRIBE `{t}`")
        cols = cur.fetchall()
        col_info = []
        for c in cols:
            col_info.append({
                "name": c[0], "type": c[1],
                "nullable": c[2], "key": c[3], "default": str(c[4]) if c[4] else None
            })
            print(f"  {c[0]:45s} {c[1]:25s} {'NULL' if c[2]=='YES' else 'NOT NULL':10s} {c[3] or '':5s}")

        schema_info[t] = {"count": cnt, "columns": col_info}

        if cnt > 0:
            cur.execute(f"SELECT * FROM `{t}` LIMIT 3")
            col_names = [d[0] for d in cur.description]
            rows = cur.fetchall()
            print(f"\n  --- Sample rows ({len(rows)}) ---")
            for row in rows:
                d = {k: (str(v)[:120] if v is not None else None) for k, v in zip(col_names, row)}
                print(f"  {json.dumps(d, ensure_ascii=False, default=str)[:600]}")

    out_path = os.path.join(os.path.dirname(__file__), "schema_info.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(schema_info, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nSchema info saved to {out_path}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
