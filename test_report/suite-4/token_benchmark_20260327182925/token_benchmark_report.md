# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 18:36:16  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 10 | 8 | — |
| 工具调用次数 | 10 | 8 | — |
| 工具返回数据量 | 6,517 chars | 167,582 chars | 25.7x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 185 chars → output 267 chars
  4. `sql_query` — input 218 chars → output 267 chars
  5. `sql_query` — input 156 chars → output 164 chars
  6. `sql_query` — input 114 chars → output 978 chars
  7. `sql_query` — input 228 chars → output 197 chars
  8. `sql_query` — input 122 chars → output 1,162 chars
  9. `sql_query` — input 111 chars → output 719 chars
  10. `sql_schema` — input 34 chars → output 1,521 chars

**BKN**:

  1. `bkn_get` — input 34 chars → output 23,882 chars
  2. `bkn_get` — input 33 chars → output 8,124 chars
  3. `bkn_query` — input 147 chars → output 4,037 chars
  4. `bkn_query` — input 152 chars → output 53,647 chars
  5. `bkn_query` — input 225 chars → output 10,746 chars
  6. `bkn_query` — input 152 chars → output 21,576 chars
  7. `bkn_get` — input 35 chars → output 34,824 chars
  8. `bkn_query` — input 145 chars → output 10,746 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 6 | 10 | — |
| 工具调用次数 | 5 | 10 | — |
| 工具返回数据量 | 30,071 chars | 365,892 chars | 12.2x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 32 chars → output 648 chars
  2. `sql_query` — input 116 chars → output 648 chars
  3. `sql_schema` — input 38 chars → output 1,112 chars
  4. `sql_query` — input 124 chars → output 23,062 chars
  5. `sql_query` — input 290 chars → output 4,601 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 27,329 chars
  2. `bkn_query` — input 165 chars → output 80,000 chars
  3. `bkn_query` — input 165 chars → output 80,000 chars
  4. `bkn_get` — input 33 chars → output 16,156 chars
  5. `bkn_query` — input 148 chars → output 7,574 chars
  6. `bkn_get` — input 33 chars → output 8,124 chars
  7. `bkn_query` — input 149 chars → output 2,068 chars
  8. `bkn_query` — input 144 chars → output 4,037 chars
  9. `bkn_query` — input 160 chars → output 60,604 chars
  10. `bkn_query` — input 165 chars → output 80,000 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| 工具返回数据量 | 36,588 chars | 533,474 chars | 14.6x |
| 单题平均 tokens | 0 | 0 | 0.0x |
| **24 题外推** | **0** | **0** | **0.0x** |
