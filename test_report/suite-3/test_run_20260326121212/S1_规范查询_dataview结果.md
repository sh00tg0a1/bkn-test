# S1 规范查询 — Dataview 直连结果（test_run_20260326121212）

## 度量

| 项 | 值 |
|----|-----|
| `kweaver dataview query` 调用次数（本 run） | 26（含失败/超时） |
| LLM token | 0（未使用 Agent 对话） |
| 入口视图 ID | `81d60443-ca6e-49c2-b377-4b89b7752cd4` |
| 数据源 | `kweaver_demo`（`10ee24cb-bdb8-4324-95cb-1bed928ef3c4`） |

**说明**：当前租户库中 **无** `forecast_event`、`mrp_plan_order_event`、`purchase_requisition_event` 等表；`inventory_event` 亦无金标 CSV 中的 `shortage_flag` 字段。与 `test-cases/suite-3/answers/` 金标不一致时，以下以 **本次 dataview 返回** 为准，并标注「库无数据 / 表不存在 / 字段不存在」。

---

## Q01 — 旋风基础版整机在中央成品仓 2023年5月库存（台）

**SQL**

```sql
SELECT COALESCE(SUM(CAST(quantity AS DECIMAL(18,4))),0) AS qty
FROM mysql_mhggp0vj."tem"."inventory_event"
WHERE item_type='Product' AND item_code='UAV-XF-BASIC'
  AND warehouse_id='WH001' AND snapshot_month='2023-05';
```

**结果**：`866.0000` 台（与金标一致）。

---

## Q02 — 入门塑料机身总成 2023年5月各仓合计（套）

**SQL（汇总）**

```sql
SELECT COALESCE(SUM(CAST(quantity AS DECIMAL(18,4))),0) AS qty
FROM mysql_mhggp0vj."tem"."inventory_event"
WHERE item_type='Material' AND item_code='ASSY-BODY-PLA-01' AND snapshot_month='2023-05';
```

**结果**：`3521.0000`（金标 CSV 口径为 1215，**线上库与 CSV 快照不一致**）。

**分仓（便于排查）**

```sql
SELECT warehouse_id, warehouse_name, SUM(CAST(quantity AS DECIMAL(18,4))) AS q
FROM mysql_mhggp0vj."tem"."inventory_event"
WHERE item_type='Material' AND item_code='ASSY-BODY-PLA-01' AND snapshot_month='2023-05'
GROUP BY warehouse_id, warehouse_name;
```

**结果**：WH001 中央成品仓 `151`；WH002 电子材料仓 `3370`。

---

## Q03 — 预测单 MDS-202604-001 产品编码与计划数量

**SQL**

```sql
SELECT material_number, qty FROM mysql_mhggp0vj."tem"."forecast_event"
WHERE billno='MDS-202604-001';
```

**结果**：`Table ... forecast_event does not exist` — **当前数据源无此表**。

---

## Q04 — 采购单 PO-202604-0250 计划到货日与状态

**SQL**

```sql
SELECT planned_arrival_date, document_status
FROM mysql_mhggp0vj."tem"."purchase_order_event"
WHERE purchase_order_number='PO-202604-0250';
```

**结果**：`entries: []` — **库中无该单号**（金标为 2026-04-14 / 执行中）。

---

## Q05 — 博世传感器平均交货周期与供货风险

**SQL**

```sql
SELECT supplier_name, lead_time_avg, risk_level
FROM mysql_mhggp0vj."tem"."supplier_entity"
WHERE supplier_code='SUP-004';
```

**结果**：平均交货周期 `45`；风险等级 `低`；供应商名称「博世传感器技术有限公司」（与金标一致）。

---

## Q06 — 中央成品仓在系统中的正式名称

**SQL**

```sql
SELECT warehouse_name FROM mysql_mhggp0vj."tem"."warehouse_entity"
WHERE warehouse_id='WH001';
```

**结果**：`深圳天翼中央成品仓库`（金标写「中央成品仓」— **命名口径不同**）。

---

## Q07 — 预测单 MDS-202604-001 展成的 MRP 行数

**结果**：依赖 `mrp_plan_order_event` — **表不存在**，无法查询。

---

## Q08 — 同上预测单 MRP 缺料行数

**结果**：同上 — **表不存在**。

---

## Q09 — 采购申请 PR-202604-0001 来源 MRP 单号

**结果**：依赖 `purchase_requisition_event` — **表不存在**。

---

## Q10 — 预测单下 PART-MOTOR-4114-400KV 缺口数量

**结果**：依赖 `mrp_plan_order_event` — **表不存在**。

---

## Q11 — 从 MRP-202604-0001 生成的采购申请条数

**结果**：依赖 `purchase_requisition_event` — **表不存在**。

---

## Q12 — 发货单 SH-202305-0001 预计送达日

**SQL**

```sql
SELECT estimated_delivery_date, actual_delivery_date
FROM mysql_mhggp0vj."tem"."shipment_event"
WHERE shipment_number='SH-202305-0001';
```

**结果**：预计 `2023-05-30`（与金标一致）；`actual_delivery_date` 为空字符串。

---

## Q13 — 发货单 SH-202305-0002 实际签收日

（与 Q12 同次查询两行）

**结果**：`actual_delivery_date`: `2023-05-28`（与金标一致）。

---

## Q14 — MDS-202604-001 对应 MRP 可用日最晚一天

**结果**：依赖 `mrp_plan_order_event` — **表不存在**。

---

## Q15 — 销售订单 SO-202604-00001 第 10 行承诺交货日与状态

**SQL**

```sql
SELECT planned_delivery_date, order_status, line_number
FROM mysql_mhggp0vj."tem"."sales_order_event"
WHERE sales_order_number='SO-202604-00001' AND CAST(line_number AS VARCHAR)='10';
```

**结果**：`entries: []` — **库中无该订单/行**。

---

## Q16 — 生产工单 MO-202305001 计划完工日与状态

**SQL**

```sql
SELECT planned_finish_date, work_order_status
FROM mysql_mhggp0vj."tem"."production_order_event"
WHERE production_order_number='MO-202305001';
```

**结果**：计划完工 `2023-05-19`；状态 `已完工`（与金标一致）。

---

## Q17 — 2023年5月中央成品仓「短缺」库存记录条数

**SQL（金标口径）**

```sql
SELECT COUNT(*) AS n FROM mysql_mhggp0vj."tem"."inventory_event"
WHERE warehouse_id='WH001' AND snapshot_month='2023-05' AND shortage_flag='是';
```

**结果**：`Column 'shortage_flag' cannot be resolved` — **当前库无该列**。

---

## Q18 — 旋风基础版 BOM 顶层子件行数

**SQL**

```sql
SELECT COUNT(*) AS n FROM mysql_mhggp0vj."tem"."bom_event"
WHERE parent_code='UAV-XF-BASIC';
```

**结果**：`6`（与金标一致）。

---

## Q19 — 系统需求预测条数

**结果**：依赖 `forecast_event` — **表不存在**。

---

## Q20 — 供应商主数据条数

**SQL**

```sql
SELECT COUNT(*) AS n FROM mysql_mhggp0vj."tem"."supplier_entity";
```

**结果**：`44`（与金标一致）。

---

## 附录：Shell 调用注意

对 `kweaver dataview query` 传入 SQL 时，推荐使用 **双引号包裹整条 `--sql`**，并对内部双引号转义为 `\"`，避免部分环境下请求体未带 `Type/QueryType` 的 400 错误。

示例：

```bash
kweaver dataview query 81d60443-ca6e-49c2-b377-4b89b7752cd4 \
  --sql "SELECT 1 FROM mysql_mhggp0vj.\"tem\".\"product_entity\" LIMIT 1"
```
