# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 18:54:10  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 15,752 | 102,639 | 6.5x |
| completion tokens | 1,456 | 1,730 | 1.2x |
| **total tokens** | **17,208** | **104,369** | **6.1x** |
| LLM 调用次数 | 10 | 5 | — |
| 工具调用次数 | 10 | 4 | — |
| 工具返回数据量 | 5,618 chars | 103,142 chars | 18.4x |
| 返回记录数（估算） | ~14 rows | ~70 rows | 5.0x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — 940 chars (schema)
  2. `sql_query` — 286 chars → ~1 row
  3. `sql_query` — 292 chars → ~1 row
  4. `sql_query` — 326 chars → ~1 row
  5. `sql_query` — 978 chars → ~2 rows
  6. `sql_query` — 228 chars → ~1 row
  7. `sql_query` — 204 chars → ~1 row
  8. `sql_schema` — 302 chars (schema)
  9. `sql_query` — 1,798 chars → ~5 rows
  10. `sql_query` — 264 chars → ~1 row

**BKN**:

  1. `bkn_query` — 53,647 chars → **~48 rows**（全量返回）
  2. `bkn_get` — 23,882 chars (schema)
  3. `bkn_query` — 21,576 chars → **~19 rows**
  4. `bkn_query` — 4,037 chars → ~3 rows

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 34,815 | 781,455 | 22.4x |
| completion tokens | 2,653 | 3,794 | 1.4x |
| **total tokens** | **37,468** | **785,249** | **21.0x** |
| LLM 调用次数 | 6 | 10 | — |
| 工具调用次数 | 7 | 10 | — |
| 工具返回数据量 | 25,606 chars | 599,971 chars | 23.4x |
| 返回记录数（估算） | ~63 rows | ~515 rows | 8.2x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — 1,112 chars (schema)
  2. `sql_schema` — 950 chars (schema)
  3. `sql_schema` — 940 chars (schema)
  4. `sql_query` — 10,517 chars → ~30 rows
  5. `sql_query` — 7,084 chars → ~20 rows
  6. `sql_query` — 4,887 chars → ~13 rows
  7. `sql_query` — 116 chars → 0 rows

**BKN**:

  1. `bkn_get` — 27,329 chars (schema)
  2. `bkn_query` — 80,000 chars → **~72 rows**（全量，截断）
  3. `bkn_query` — 7,574 chars → ~6 rows
  4. `bkn_query` — 80,000 chars → **~72 rows**（全量，截断）
  5. `bkn_query` — 24,500 chars → ~22 rows
  6. `bkn_query` — 80,000 chars → **~72 rows**（全量，截断）
  7. `bkn_query` — 60,568 chars → **~55 rows**
  8. `bkn_query` — 80,000 chars → **~72 rows**（全量，截断）
  9. `bkn_query` — 80,000 chars → **~72 rows**（全量，截断）
  10. `bkn_query` — 80,000 chars → **~72 rows**（全量，截断）

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 50,567 | 884,094 | 17.5x |
| completion tokens | 4,109 | 5,524 | 1.3x |
| **total tokens** | **54,676** | **889,618** | **16.3x** |
| 工具返回数据量 | 31,224 chars | 703,113 chars | 22.5x |
| 返回记录数（估算） | ~77 rows | ~585 rows | 7.6x |
| 单题平均 tokens | 27,338 | 444,809 | 16.3x |
| **24 题外推** | **656,112** | **10,675,416** | **16.3x** |
