# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 20:16:38  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 3,789 | 17,994 | 4.7x |
| completion tokens | 763 | 1,853 | 2.4x |
| **total tokens** | **4,552** | **19,847** | **4.4x** |
| LLM 调用次数 | 4 | 7 | — |
| 工具调用次数 | 4 | 6 | — |
| 工具返回数据量 | 1,599 chars | 8,880 chars | 5.6x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 402 chars → output 189 chars
  4. `sql_query` — input 231 chars → output 168 chars

**BKN**:

  1. `bkn_get` — input 34 chars → output 3,810 chars
  2. `bkn_query` — input 164 chars → output 997 chars
  3. `bkn_query` — input 164 chars → output 997 chars
  4. `bkn_query` — input 163 chars → output 990 chars
  5. `bkn_query` — input 221 chars → output 189 chars
  6. `bkn_query` — input 208 chars → output 1,897 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 33,569 | 276,617 | 8.2x |
| completion tokens | 2,267 | 5,912 | 2.6x |
| **total tokens** | **35,836** | **282,529** | **7.9x** |
| LLM 调用次数 | 7 | 10 | — |
| 工具调用次数 | 6 | 9 | — |
| 工具返回数据量 | 26,962 chars | 164,276 chars | 6.1x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 32 chars → output 648 chars
  2. `sql_schema` — input 38 chars → output 1,112 chars
  3. `sql_query` — input 172 chars → output 702 chars
  4. `sql_query` — input 137 chars → output 20,989 chars
  5. `sql_query` — input 317 chars → output 2,863 chars
  6. `sql_query` — input 118 chars → output 648 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 4,276 chars
  2. `bkn_query` — input 180 chars → output 20,000 chars
  3. `bkn_query` — input 197 chars → output 20,000 chars
  4. `bkn_query` — input 198 chars → output 20,000 chars
  5. `bkn_query` — input 181 chars → output 20,000 chars
  6. `bkn_query` — input 198 chars → output 20,000 chars
  7. `bkn_query` — input 197 chars → output 20,000 chars
  8. `bkn_query` — input 181 chars → output 20,000 chars
  9. `bkn_query` — input 196 chars → output 20,000 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 37,358 | 294,611 | 7.9x |
| completion tokens | 3,030 | 7,765 | 2.6x |
| **total tokens** | **40,388** | **302,376** | **7.5x** |
| 工具返回数据量 | 28,561 chars | 173,156 chars | 6.1x |
| 单题平均 tokens | 20,194 | 151,188 | 7.5x |
| **24 题外推** | **484,656** | **3,628,512** | **7.5x** |
