"""Shared database configuration for suite-2 scripts."""

DB_CONFIG = dict(
    host='116.63.205.204',
    port=3306,
    user='root',
    password='x8NF!diQS*4cZh9n',
    database='hd_supply',
    charset='utf8mb4',
    connect_timeout=30,
)

DB_CONFIG_INTERNAL = dict(
    host='10.240.1.178',
    port=3306,
    user='root',
    password='x8NF!diQS*4cZh9n',
    database='hd_supply',
    charset='utf8mb4',
    connect_timeout=30,
)


def get_connection():
    import pymysql
    for cfg in [DB_CONFIG, DB_CONFIG_INTERNAL]:
        try:
            return pymysql.connect(**cfg)
        except Exception:
            continue
    raise ConnectionError(
        "Cannot connect to MySQL at either 116.63.205.204 or 10.240.1.178"
    )
