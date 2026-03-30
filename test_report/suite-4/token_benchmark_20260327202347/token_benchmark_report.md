# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 20:28:08  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 19,144 | 10,729 | 0.6x |
| completion tokens | 1,355 | 1,403 | 1.0x |
| **total tokens** | **20,499** | **12,132** | **0.6x** |
| LLM 调用次数 | 10 | 5 | — |
| 工具调用次数 | 11 | 4 | — |
| 工具返回数据量 | 7,160 chars | 6,780 chars | 0.9x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 32 chars → output 302 chars
  2. `sql_schema` — input 33 chars → output 940 chars
  3. `sql_query` — input 110 chars → output 978 chars
  4. `sql_query` — input 288 chars → output 391 chars
  5. `sql_query` — input 279 chars → output 425 chars
  6. `sql_query` — input 138 chars → output 144 chars
  7. `sql_query` — input 123 chars → output 576 chars
  8. `sql_query` — input 168 chars → output 978 chars
  9. `sql_schema` — input 34 chars → output 1,521 chars
  10. `sql_query` — input 121 chars → output 633 chars
  11. `sql_query` — input 225 chars → output 272 chars

**BKN**:

  1. `bkn_get` — input 34 chars → output 3,810 chars
  2. `bkn_query` — input 166 chars → output 990 chars
  3. `bkn_query` — input 167 chars → output 990 chars
  4. `bkn_query` — input 167 chars → output 990 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 36,042 | 36,073 | 1.0x |
| completion tokens | 2,359 | 3,299 | 1.4x |
| **total tokens** | **38,401** | **39,372** | **1.0x** |
| LLM 调用次数 | 7 | 5 | — |
| 工具调用次数 | 6 | 4 | — |
| 工具返回数据量 | 32,821 chars | 52,175 chars | 1.6x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_query` — input 133 chars → output 191 chars
  3. `sql_query` — input 103 chars → output 719 chars
  4. `sql_query` — input 133 chars → output 20,989 chars
  5. `sql_query` — input 273 chars → output 6,509 chars
  6. `sql_query` — input 303 chars → output 3,301 chars

**BKN**:

  1. `bkn_get` — input 39 chars → output 4,276 chars
  2. `bkn_get` — input 34 chars → output 3,810 chars
  3. `bkn_query` — input 180 chars → output 21,008 chars
  4. `bkn_query` — input 181 chars → output 23,081 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 55,186 | 46,802 | 0.8x |
| completion tokens | 3,714 | 4,702 | 1.3x |
| **total tokens** | **58,900** | **51,504** | **0.9x** |
| 工具返回数据量 | 39,981 chars | 58,955 chars | 1.5x |
| 单题平均 tokens | 29,450 | 25,752 | 0.9x |
| **24 题外推** | **706,800** | **618,048** | **0.9x** |
