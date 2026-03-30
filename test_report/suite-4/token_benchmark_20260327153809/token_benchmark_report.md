# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 15:49:39  
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
| 工具调用次数 | 10 | 8 | — |
| 工具返回数据量 | 6,258 chars | 256,824 chars | 41.0x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 135 chars → output 978 chars
  4. `sql_query` — input 251 chars → output 200 chars
  5. `sql_query` — input 124 chars → output 1,162 chars
  6. `sql_query` — input 145 chars → output 978 chars
  7. `sql_schema` — input 32 chars → output 1,022 chars
  8. `sql_query` — input 91 chars → output 148 chars
  9. `sql_query` — input 309 chars → output 261 chars
  10. `sql_query` — input 250 chars → output 267 chars

**BKN**:

  1. `bkn_get` — input 33 chars → output 8,124 chars
  2. `bkn_get` — input 34 chars → output 23,882 chars
  3. `bkn_query` — input 151 chars → output 80,000 chars
  4. `bkn_get` — input 33 chars → output 25,257 chars
  5. `bkn_query` — input 150 chars → output 21,576 chars
  6. `bkn_query` — input 150 chars → output 22,762 chars
  7. `bkn_query` — input 212 chars → output 21,576 chars
  8. `bkn_query` — input 148 chars → output 53,647 chars

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
| 工具调用次数 | 7 | 10 | — |
| 工具返回数据量 | 29,058 chars | 612,565 chars | 21.1x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_schema` — input 27 chars → output 950 chars
  4. `sql_query` — input 116 chars → output 648 chars
  5. `sql_query` — input 118 chars → output 302 chars
  6. `sql_query` — input 133 chars → output 20,989 chars
  7. `sql_query` — input 295 chars → output 4,755 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 27,329 chars
  2. `bkn_query` — input 165 chars → output 80,000 chars
  3. `bkn_get` — input 33 chars → output 16,156 chars
  4. `bkn_query` — input 167 chars → output 80,000 chars
  5. `bkn_query` — input 165 chars → output 80,000 chars
  6. `bkn_query` — input 46 chars → output 9,080 chars
  7. `bkn_query` — input 165 chars → output 80,000 chars
  8. `bkn_query` — input 163 chars → output 80,000 chars
  9. `bkn_query` — input 154 chars → output 80,000 chars
  10. `bkn_query` — input 240 chars → output 80,000 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| cost (USD) | $0.0000 | $0.0000 | N/A |
| 工具返回数据量 | 35,316 chars | 869,389 chars | 24.6x |
| 单题平均 tokens | 0 | 0 | 0.0x |
| **24 题外推** | **0** | **0** | **0.0x** |
