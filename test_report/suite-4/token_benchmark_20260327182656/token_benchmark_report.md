# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 18:33:23  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 10 | 3 | — |
| 工具调用次数 | 10 | 2 | — |
| 工具返回数据量 | 6,473 chars | 103,882 chars | 16.0x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 243 chars → output 351 chars
  4. `sql_query` — input 125 chars → output 978 chars
  5. `sql_query` — input 229 chars → output 357 chars
  6. `sql_query` — input 159 chars → output 170 chars
  7. `sql_query` — input 122 chars → output 1,162 chars
  8. `sql_query` — input 245 chars → output 213 chars
  9. `sql_query` — input 124 chars → output 978 chars
  10. `sql_schema` — input 32 chars → output 1,022 chars

**BKN**:

  1. `bkn_get` — input 34 chars → output 23,882 chars
  2. `bkn_query` — input 151 chars → output 80,000 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 6 | 9 | — |
| 工具调用次数 | 6 | 8 | — |
| 工具返回数据量 | 32,818 chars | 480,792 chars | 14.7x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_schema` — input 32 chars → output 648 chars
  3. `sql_query` — input 108 chars → output 648 chars
  4. `sql_query` — input 133 chars → output 20,989 chars
  5. `sql_query` — input 247 chars → output 5,566 chars
  6. `sql_query` — input 293 chars → output 3,855 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 27,329 chars
  2. `bkn_query` — input 165 chars → output 80,000 chars
  3. `bkn_query` — input 165 chars → output 80,000 chars
  4. `bkn_query` — input 167 chars → output 80,000 chars
  5. `bkn_query` — input 164 chars → output 60,580 chars
  6. `bkn_query` — input 166 chars → output 80,000 chars
  7. `bkn_query` — input 158 chars → output 60,596 chars
  8. `bkn_query` — input 162 chars → output 12,287 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| 工具返回数据量 | 39,291 chars | 584,674 chars | 14.9x |
| 单题平均 tokens | 0 | 0 | 0.0x |
| **24 题外推** | **0** | **0** | **0.0x** |
