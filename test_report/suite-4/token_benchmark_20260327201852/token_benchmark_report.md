# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 20:22:40  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 9,682 | 7,581 | 0.8x |
| completion tokens | 1,409 | 930 | 0.7x |
| **total tokens** | **11,091** | **8,511** | **0.8x** |
| LLM 调用次数 | 8 | 4 | — |
| 工具调用次数 | 7 | 3 | — |
| 工具返回数据量 | 3,006 chars | 5,790 chars | 1.9x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 259 chars → output 244 chars
  4. `sql_query` — input 169 chars → output 178 chars
  5. `sql_query` — input 159 chars → output 170 chars
  6. `sql_query` — input 125 chars → output 978 chars
  7. `sql_query` — input 225 chars → output 194 chars

**BKN**:

  1. `bkn_get` — input 34 chars → output 3,810 chars
  2. `bkn_query` — input 168 chars → output 990 chars
  3. `bkn_query` — input 169 chars → output 990 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 19,925 | 95,792 | 4.8x |
| completion tokens | 2,237 | 5,521 | 2.5x |
| **total tokens** | **22,162** | **101,313** | **4.6x** |
| LLM 调用次数 | 4 | 10 | — |
| 工具调用次数 | 3 | 10 | — |
| 工具返回数据量 | 26,130 chars | 79,627 chars | 3.0x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_query` — input 137 chars → output 20,989 chars
  3. `sql_query` — input 270 chars → output 4,029 chars

**BKN**:

  1. `bkn_query` — input 167 chars → output 274 chars
  2. `bkn_get` — input 33 chars → output 2,567 chars
  3. `bkn_query` — input 162 chars → output 664 chars
  4. `bkn_get` — input 39 chars → output 4,276 chars
  5. `bkn_get` — input 34 chars → output 3,810 chars
  6. `bkn_query` — input 178 chars → output 18,993 chars
  7. `bkn_query` — input 180 chars → output 18,993 chars
  8. `bkn_query` — input 178 chars → output 18,993 chars
  9. `bkn_query` — input 258 chars → output 7,088 chars
  10. `bkn_get` — input 28 chars → output 3,969 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 29,607 | 103,373 | 3.5x |
| completion tokens | 3,646 | 6,451 | 1.8x |
| **total tokens** | **33,253** | **109,824** | **3.3x** |
| 工具返回数据量 | 29,136 chars | 85,417 chars | 2.9x |
| 单题平均 tokens | 16,626 | 54,912 | 3.3x |
| **24 题外推** | **399,036** | **1,317,888** | **3.3x** |
