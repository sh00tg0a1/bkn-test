# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 15:54:14  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| cost (USD) | $0.0000 | $0.0000 | N/A |
| LLM 调用次数 | 0 | 0 | — |
| 工具调用次数 | 8 | 2 | — |
| 工具返回数据量 | 3,565 chars | 649 chars | 0.2x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 125 chars → output 978 chars
  4. `sql_query` — input 114 chars → output 269 chars
  5. `sql_query` — input 125 chars → output 269 chars
  6. `sql_query` — input 192 chars → output 269 chars
  7. `sql_query` — input 181 chars → output 269 chars
  8. `sql_query` — input 85 chars → output 269 chars

**BKN**:

  1. `bkn_get` — input 34 chars → output 201 chars
  2. `bkn_query` — input 47 chars → output 448 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| cost (USD) | $0.0000 | $0.0000 | N/A |
| LLM 调用次数 | 0 | 0 | — |
| 工具调用次数 | 5 | 4 | — |
| 工具返回数据量 | 1,345 chars | 1,270 chars | 0.9x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 269 chars
  2. `sql_schema` — input 27 chars → output 269 chars
  3. `sql_query` — input 90 chars → output 269 chars
  4. `sql_schema` — input 32 chars → output 269 chars
  5. `sql_query` — input 99 chars → output 269 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 201 chars
  2. `bkn_query` — input 146 chars → output 448 chars
  3. `bkn_query` — input 155 chars → output 448 chars
  4. `bkn_query` — input 47 chars → output 173 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| cost (USD) | $0.0000 | $0.0000 | N/A |
| 工具返回数据量 | 4,910 chars | 1,919 chars | 0.4x |
| 单题平均 tokens | 0 | 0 | 0.0x |
| **24 题外推** | **0** | **0** | **0.0x** |
