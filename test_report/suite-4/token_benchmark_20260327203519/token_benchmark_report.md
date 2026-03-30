# Suite-4 Token Benchmark: SQL vs BKN

**时间**: 2026-03-27 20:39:19  
**模型**: MiniMax-M2.5  
**样本**: 2 题

## Q-F1-01

**问题**: 霸风20L植保无人机当前的成品库存是多少台？其中在库、在途、冻结库存分别是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 16,243 | 4,763 | 0.3x |
| completion tokens | 1,855 | 850 | 0.5x |
| **total tokens** | **18,098** | **5,613** | **0.3x** |
| LLM 调用次数 | 10 | 3 | — |
| 工具调用次数 | 11 | 2 | — |
| 工具返回数据量 | 6,163 chars | 1,184 chars | 0.2x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 32 chars → output 302 chars
  2. `sql_schema` — input 33 chars → output 940 chars
  3. `sql_query` — input 181 chars → output 292 chars
  4. `sql_query` — input 91 chars → output 148 chars
  5. `sql_query` — input 139 chars → output 719 chars
  6. `sql_query` — input 114 chars → output 978 chars
  7. `sql_query` — input 270 chars → output 247 chars
  8. `sql_query` — input 131 chars → output 193 chars
  9. `sql_query` — input 146 chars → output 196 chars
  10. `sql_schema` — input 32 chars → output 1,022 chars
  11. `sql_query` — input 140 chars → output 1,126 chars

**BKN**:

  1. `bkn_query` — input 164 chars → output 592 chars
  2. `bkn_query` — input 167 chars → output 592 chars

</details>

## Q-F2-02

**问题**: 预测单MDS-202605-002对应的霸风30L植保无人机MRP结果中，共有多少颗物料缺料？缺料最严重的前5颗物料是哪些？各自缺口数量是多少？

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 15,180 | 30,521 | 2.0x |
| completion tokens | 1,427 | 3,705 | 2.6x |
| **total tokens** | **16,607** | **34,226** | **2.1x** |
| LLM 调用次数 | 5 | 5 | — |
| 工具调用次数 | 5 | 4 | — |
| 工具返回数据量 | 16,885 chars | 20,821 chars | 1.2x |

<details><summary>工具调用明细</summary>

**SQL**:

  1. `sql_schema` — input 38 chars → output 1,112 chars
  2. `sql_schema` — input 32 chars → output 648 chars
  3. `sql_query` — input 116 chars → output 648 chars
  4. `sql_query` — input 133 chars → output 10,517 chars
  5. `sql_query` — input 257 chars → output 3,960 chars

**BKN**:

  1. `bkn_query` — input 149 chars → output 376 chars
  2. `bkn_query` — input 165 chars → output 6,815 chars
  3. `bkn_query` — input 178 chars → output 6,815 chars
  4. `bkn_query` — input 181 chars → output 6,815 chars

</details>

## 汇总

| 指标 | SQL | BKN | 倍率 |
|------|-----|-----|------|
| prompt tokens | 31,423 | 35,284 | 1.1x |
| completion tokens | 3,282 | 4,555 | 1.4x |
| **total tokens** | **34,705** | **39,839** | **1.1x** |
| 工具返回数据量 | 23,048 chars | 22,005 chars | 1.0x |
| 单题平均 tokens | 17,352 | 19,920 | 1.1x |
| **24 题外推** | **416,460** | **478,068** | **1.1x** |
