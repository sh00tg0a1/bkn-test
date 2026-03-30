# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 20:45:56  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 19,615 | 13,241 | 0.7x |
| completion tokens | 1,808 | 1,255 | 0.7x |
| **total tokens** | **21,423** | **14,496** | **0.7x** |
| LLM 调用次数 | 10 | 5 | — |
| 工具调用次数 | 10 | 4 | — |
| 工具返回数据量 | 6,389 chars | 6,754 chars | 1.1x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_query` — input 146 chars → output 1,885 chars
  3. `sql_query` — input 173 chars → output 203 chars
  4. `sql_query` — input 261 chars → output 237 chars
  5. `sql_query` — input 138 chars → output 978 chars
  6. `sql_query` — input 300 chars → output 251 chars
  7. `sql_schema` — input 32 chars → output 302 chars
  8. `sql_query` — input 141 chars → output 1,132 chars
  9. `sql_query` — input 466 chars → output 270 chars
  10. `sql_query` — input 458 chars → output 191 chars

**BKN**:

  1. `bkn_query` — input 164 chars → output 592 chars
  2. `bkn_get` — input 34 chars → output 3,810 chars
  3. `bkn_query` — input 166 chars → output 2,335 chars
  4. `bkn_query` — input 173 chars → output 17 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 28,385 | 8,110 | 0.3x |
| completion tokens | 2,756 | 1,700 | 0.6x |
| **total tokens** | **31,141** | **9,810** | **0.3x** |
| LLM 调用次数 | 7 | 3 | — |
| 工具调用次数 | 7 | 2 | — |
| 工具返回数据量 | 29,494 chars | 7,191 chars | 0.2x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_schema` — input 32 chars → output 648 chars
  3. `sql_schema` — input 32 chars → output 302 chars
  4. `sql_query` — input 108 chars → output 648 chars
  5. `sql_schema` — input 27 chars → output 950 chars
  6. `sql_query` — input 124 chars → output 23,062 chars
  7. `sql_query` — input 451 chars → output 2,772 chars

**BKN**:

  1. `bkn_query` — input 156 chars → output 376 chars
  2. `bkn_query` — input 172 chars → output 6,815 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 48,000 | 21,351 | 0.4x |
| completion tokens | 4,564 | 2,955 | 0.6x |
| **total tokens** | **52,564** | **24,306** | **0.5x** |
| 工具返回数据量 | 35,883 chars | 13,945 chars | 0.4x |
| 单题平均 tokens | 26,282 | 12,153 | 0.5x |
| **24 题外推** | **630,768** | **291,672** | **0.5x** |
