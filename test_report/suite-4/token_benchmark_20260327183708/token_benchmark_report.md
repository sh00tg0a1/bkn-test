# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 18:44:15  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 0 | 0 | — |
| 工具调用次数 | 10 | 4 | — |
| 工具返回数据量 | 8,181 chars | 122,752 chars | 15.0x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 151 chars → output 978 chars
  4. `sql_query` — input 338 chars → output 278 chars
  5. `sql_query` — input 172 chars → output 466 chars
  6. `sql_query` — input 178 chars → output 978 chars
  7. `sql_query` — input 151 chars → output 978 chars
  8. `sql_query` — input 113 chars → output 718 chars
  9. `sql_schema` — input 32 chars → output 1,022 chars
  10. `sql_schema` — input 34 chars → output 1,521 chars

**BKN**:

  1. `bkn_get` — input 33 chars → output 8,124 chars
  2. `bkn_get` — input 34 chars → output 23,882 chars
  3. `bkn_query` — input 151 chars → output 80,000 chars
  4. `bkn_query` — input 150 chars → output 10,746 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 0 | 0 | — |
| 工具调用次数 | 8 | 10 | — |
| 工具返回数据量 | 28,507 chars | 591,683 chars | 20.8x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_schema` — input 32 chars → output 648 chars
  3. `sql_query` — input 108 chars → output 648 chars
  4. `sql_query` — input 133 chars → output 10,517 chars
  5. `sql_query` — input 287 chars → output 7,068 chars
  6. `sql_query` — input 392 chars → output 7,653 chars
  7. `sql_query` — input 339 chars → output 745 chars
  8. `sql_query` — input 196 chars → output 116 chars

**BKN**:

  1. `bkn_get` — input 33 chars → output 16,156 chars
  2. `bkn_get` — input 39 chars → output 27,329 chars
  3. `bkn_query` — input 142 chars → output 7,574 chars
  4. `bkn_query` — input 159 chars → output 80,000 chars
  5. `bkn_query` — input 159 chars → output 80,000 chars
  6. `bkn_query` — input 161 chars → output 80,000 chars
  7. `bkn_query` — input 161 chars → output 80,000 chars
  8. `bkn_query` — input 141 chars → output 80,000 chars
  9. `bkn_query` — input 147 chars → output 80,000 chars
  10. `bkn_query` — input 148 chars → output 60,624 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| 工具返回数据量 | 36,688 chars | 714,435 chars | 19.5x |
| 单题平均 tokens | 0 | 0 | 0.0x |
| **24 题外推** | **0** | **0** | **0.0x** |
