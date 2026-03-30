# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 19:59:49  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 22,685 | 89,140 | 3.9x |
| completion tokens | 2,272 | 2,588 | 1.1x |
| **total tokens** | **24,957** | **91,728** | **3.7x** |
| LLM 调用次数 | 10 | 10 | — |
| 工具调用次数 | 11 | 9 | — |
| 工具返回数据量 | 12,565 chars | 117,600 chars | 9.4x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 32 chars → output 302 chars
  2. `sql_schema` — input 33 chars → output 940 chars
  3. `sql_query` — input 233 chars → output 323 chars
  4. `sql_query` — input 114 chars → output 978 chars
  5. `sql_query` — input 244 chars → output 331 chars
  6. `sql_query` — input 307 chars → output 395 chars
  7. `sql_query` — input 187 chars → output 211 chars
  8. `sql_schema` — input 32 chars → output 1,022 chars
  9. `sql_query` — input 147 chars → output 7,737 chars
  10. `sql_query` — input 91 chars → output 148 chars
  11. `sql_query` — input 171 chars → output 178 chars

**BKN**:

  1. `bkn_get` — input 34 chars → output 191 chars
  2. `bkn_get` — input 33 chars → output 8,124 chars
  3. `bkn_query` — input 164 chars → output 527 chars
  4. `bkn_get` — input 34 chars → output 23,882 chars
  5. `bkn_query` — input 162 chars → output 1,219 chars
  6. `bkn_query` — input 155 chars → output 1,219 chars
  7. `bkn_query` — input 158 chars → output 1,219 chars
  8. `bkn_query` — input 158 chars → output 1,219 chars
  9. `bkn_query` — input 48 chars → output 80,000 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 19,902 | 24,269 | 1.2x |
| completion tokens | 1,732 | 1,769 | 1.0x |
| **total tokens** | **21,634** | **26,038** | **1.2x** |
| LLM 调用次数 | 4 | 3 | — |
| 工具调用次数 | 3 | 2 | — |
| 工具返回数据量 | 26,061 chars | 54,405 chars | 2.1x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_query` — input 133 chars → output 20,989 chars
  3. `sql_query` — input 281 chars → output 3,960 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 27,329 chars
  2. `bkn_query` — input 181 chars → output 27,076 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 42,587 | 113,409 | 2.7x |
| completion tokens | 4,004 | 4,357 | 1.1x |
| **total tokens** | **46,591** | **117,766** | **2.5x** |
| 工具返回数据量 | 38,626 chars | 172,005 chars | 4.5x |
| 单题平均 tokens | 23,296 | 58,883 | 2.5x |
| **24 题外推** | **559,092** | **1,413,192** | **2.5x** |
