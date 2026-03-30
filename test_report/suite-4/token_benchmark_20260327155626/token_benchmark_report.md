# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 16:04:00  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 4 | 6 | — |
| 工具调用次数 | 4 | 5 | — |
| 工具返回数据量 | 1,672 chars | 169,690 chars | 101.5x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 33 chars → output 940 chars
  2. `sql_schema` — input 32 chars → output 302 chars
  3. `sql_query` — input 177 chars → output 230 chars
  4. `sql_query` — input 230 chars → output 200 chars

**BKN**:

  1. `bkn_get` — input 33 chars → output 8,124 chars
  2. `bkn_get` — input 34 chars → output 23,882 chars
  3. `bkn_query` — input 150 chars → output 4,037 chars
  4. `bkn_query` — input 151 chars → output 80,000 chars
  5. `bkn_query` — input 141 chars → output 53,647 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| LLM 调用次数 | 4 | 10 | — |
| 工具调用次数 | 3 | 10 | — |
| 工具返回数据量 | 27,498 chars | 426,387 chars | 15.5x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_query` — input 133 chars → output 20,989 chars
  3. `sql_query` — input 329 chars → output 5,397 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 27,329 chars
  2. `bkn_query` — input 165 chars → output 80,000 chars
  3. `bkn_query` — input 164 chars → output 60,608 chars
  4. `bkn_get` — input 33 chars → output 16,156 chars
  5. `bkn_query` — input 148 chars → output 7,574 chars
  6. `bkn_query` — input 165 chars → output 80,000 chars
  7. `bkn_query` — input 160 chars → output 24,500 chars
  8. `bkn_query` — input 154 chars → output 60,568 chars
  9. `bkn_query` — input 157 chars → output 9,080 chars
  10. `bkn_query` — input 166 chars → output 60,572 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 0 | 0 | N/A |
| completion tokens | 0 | 0 | N/A |
| **total tokens** | **0** | **0** | **0.0x** |
| 工具返回数据量 | 29,170 chars | 596,077 chars | 20.4x |
| 单题平均 tokens | 0 | 0 | 0.0x |
| **24 题外推** | **0** | **0** | **0.0x** |
