#!/usr/bin/env python3.12
"""Explore hd_supply database schema and sample data."""
import pymysql
import json

DB_CONFIG = dict(
    host='116.63.205.204',
    port=3306,
    user='root',
    password='x8NF!diQS*4cZh9n',
    database='hd_supply',
    charset='utf8mb4',
    connect_timeout=30,
)


def main():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SHOW TABLES")
    tables = [r[0] for r in cur.fetchall()]
    print(f"=== Tables ({len(tables)}) ===")
    for t in tables:
        print(f"  {t}")

    print("\n=== Table Details ===")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM `{t}`")
        cnt = cur.fetchone()[0]
        print(f"\n--- {t} ({cnt} rows) ---")

        cur.execute(f"DESCRIBE `{t}`")
        cols = cur.fetchall()
        for c in cols:
            print(f"  {c[0]:40s} {c[1]:20s} {'NULL' if c[2]=='YES' else 'NOT NULL':8s} {c[3] or '':5s} {str(c[4]) if c[4] is not None else '':20s}")

        if cnt > 0:
            cur.execute(f"SELECT * FROM `{t}` LIMIT 2")
            col_names = [d[0] for d in cur.description]
            rows = cur.fetchall()
            print(f"  Sample ({len(rows)} rows):")
            for row in rows:
                d = dict(zip(col_names, row))
                for k, v in d.items():
                    if v is not None:
                        d[k] = str(v)[:100]
                print(f"    {json.dumps(d, ensure_ascii=False, default=str)[:500]}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
