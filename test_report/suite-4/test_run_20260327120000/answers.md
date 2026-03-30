# Suite-4 PMC 场景 — Dataview 拉数答案（test_run_20260327120000）

数据来源：`supply_chain_data_v1`（`kweaver dataview query`，catalog `mysql_1j6tsjwo."supply_chain_data"`）。以下为基于查询结果的归纳，**非**金标对照。

---

## F1 基础信息查询

### Q-F1-01 产品库存查询

- **成品在库（inventory_event，中央成品仓）**：`item_code=UAV-BF-IND-H20` 汇总数量 **2216 台**（`warehouse_name=中央成品仓`）。
- **在库 / 在途 / 冻结分项**：当前 `inventory_event` 未提供「在途库存」「冻结库存」字段；仅有一条 Active 记录，无法按 WMS 口径拆成在库/在途/冻结三列。
- **参考（发运表，非标准在途库存）**：`shipment_event` 中 `product_code=UAV-BF-IND-H20` 且 `delivery_status=运输中` 的运单数量合计为 **524+282+368=1174 台**（历史/多时点发运记录，不宜直接等同「在途库存」）。

### Q-F1-02 需求预测单查询

- `forecast_event`：`billno=MDS-202605-002`，`material_name=霸风30L植保无人机`，`qty=600` 台，`enddate=2026-05-30`。
- **单据状态**：字段为 `status=Active`；库中无「草稿/已确认」枚举，无法直接回答「草稿还是已确认」，仅能给出 `Active`。

### Q-F1-03 物料PO查询

- 极风 `UAV-JF-ENT-AG` BOM 中动力系统子件 `ASSY-PWR-TQ` 下含电机 `PART-MOTOR-4114-400KV`（4114 400KV高扭矩电机）。
- `purchase_order_event` 中该物料 PO 示例：**PO-202605-0273**（已收货）、**PO-202604-0301**（已收货）、**PO-202605-0317**（执行中，未关闭）；供应商含索尼半导体解决方案、芯源微电子股份有限公司；订货量与承诺到货见各行的 `purchase_quantity`、`planned_arrival_date`、`required_date`、`document_status`。

### Q-F1-04 物料库存查询

- 「飞控模块」按 BOM 取 `ASSY-FC-RTK` 及其子件（如 `COMP-FC-PCB-R1` 等）。
- **各仓库存合计（inventory_event 按 item_code 汇总）**：`ASSY-FC-RTK` **5278**；子件如 `COMP-FC-PCB-R1` **3743** 等（多仓合计）。
- **与安全库存**：`material_entity` 无 `safety_stock_qty` 等字段；`inventory_event.shortage_flag` 对 `ASSY-FC-RTK` / `COMP-FC-PCB-R1` 均为 **否**，无法判断是否低于安全库存水位。

### Q-F1-05 BOM结构查询

- **直接挂在 `UAV-BF-IND-H30` 下的 BOM 行**：**10** 行；仅 **`ASSY-FC-RTK`** 有子层，子层 **5** 行。
- **层数**：成品 → 子件/总成 → 飞控子件，约 **3 层**（无统一 `level` 字段，为根据父子关系归纳）。
- **总行数**：10 + 5 = **15** 行（展开一层子 BOM）。
- **自制件 / 采购件**：`bom_event` 中 `child_type` 均为 `Material`；按 `assembly_set` 统计：H30 直属行「是」9 行、「否」1 行；`ASSY-FC-RTK` 下「是」4、「否」1。**若业务以 `assembly_set=是` 近似自制、`=否` 近似采购**，则合计自制 **13** 行、采购 **2** 行（行级，非物料种类唯一计数）。

### Q-F1-06 供应商信息查询

- 喷洒组件取 BOM 中 **`PART-SPRAYER-16L`（16升智能喷洒系统）**。
- `purchase_order_event` 按 `material_code=PART-SPRAYER-16L` 分组：**深圳农业喷洒系统公司**（8 笔 PO，平均 `DATEDIFF(planned_arrival_date, document_date)` 约 **32.5** 天）、索尼半导体、TI 代理、ST、芯源微电子等。
- **准时率（抽样）**：`material_procurement_event` 中 `material_code=PART-SPRAYER-16L` 且供应商为「德州仪器（TI）中国代理」的 **2** 笔收货，**ontime=2**（`actual_delivery_date <= estimated_delivery_date`），准时率 **100%**（样本量小，不代表全部合格供应商）。

---

## F2 MRP状态分析

### Q-F2-01 MRP投放状态

- `mrp_plan_order_event` 中 `rootdemandbillno=MDS-202605-001` 存在多行计划。
- **最近一次 MRP 时间**：`MAX(createtime)=2026-03-25 10:00:00`（同一批次时间戳）。

### Q-F2-02 缺料汇总分析

- `rootdemandbillno=MDS-202605-002` 且 `bizorderqty < adviseorderqty`：**6** 条物料行缺料。
- **缺口最大的前 5（按 gap 降序）**：`PART-MOTOR-5010-PRO` gap 180；`PART-CONN-GH-1.25-10P` gap 120；`PART-SPRAYER-30L`、`PART-4G-MODULE`、`COMP-FC-CASE-AL-IND` 各 gap 30。

### Q-F2-03 PO交期符合率（MDS-202605-003 缺料）

- 缺料行 **11** 条（`bizorderqty < adviseorderqty`）。
- 对缺料料号在 `purchase_order_event` 中 `document_status=执行中` 的样本：`PART-4G-MODULE` 存在 `planned_arrival_date`（如 2026-05-28）**晚于** `required_date`（2026-05-18）的情形 → **存在交期逾期风险**；`PART-MOTOR-4114-400KV` 等存在计划到货早于需求日的行。需按「每缺料料号取有效 PO」逐条比对；粗结论：**至少多颗物料存在 PO 计划到货不覆盖 MRP 需求日的风险**。

### Q-F2-04 PR待转换清单

- 由 `purchase_requisition_event` 与 `mrp_plan_order_event` 关联（`srcbillid = mrp.billno`，`rootdemandbillno=MDS-202605-001`）：**20** 张不同 `billno` 的 PR。
- **未完结审批**：`status` 含 **审批中** 的 PR 涉及物料如 `PART-CAM-FPV`、`PART-SPRAYER-20L`、`PART-RADAR-ALT`、`PART-PROP-1755-CF`、`PART-CABLE-ESC-HD`、`RAW-LIPO-CELL`、`PART-MCU-STM32H753`、`PART-PCB-FC-8L`、`PART-FPGA-ICE40`、`RAW-COPPER-WIRE`、`RAW-SI-WAFER-12IN`、`RAW-FR4-CCL` 等（详见该子查询结果集）。
- **PR→PO**：`purchase_order_event` 中 `srcbillid` 多为空，**无法用库内字段可靠判定「已转 PO」**。

### Q-F2-05 自制件MRP状态

- 霸风30L 直属 BOM 含机身框架 `PART-FRAME-HEX-CF-HD`、喷洒 `PART-SPRAYER-30L` 等；**子 BOM 仅 `ASSY-FC-RTK` 展开**。
- **生产工单**：`production_order_event` 中 `output_code=UAV-BF-IND-H30` 仅 **1** 条历史工单（`MO-202305010`，已完工，数量 107），**未**与 2026-05 预测单关联。
- **结论**：无法用现有表证明「自制件已按 MRP 投放且工单数量满足 600 台需求」。

### Q-F2-06 齐套率分析

- 库内无现成「齐套率」字段；需按 BOM 展层与 `inventory_event`/`purchase_order_event` 逐料计算。**本次未算整体百分比**。
- 可用 **`mrp_plan_order_event` 缺口行占比** 作代理：对 `MDS-202605-003` 有 **11** 行 `bizorderqty < adviseorderqty`。

---

## F3 交期复杂分析

### Q-F3-01 批次最早交货日

- 对 `MDS-202605-001` 缺料料号关联 PO，`MAX(planned_arrival_date)` 样本为 **2026-05-28**。
- **生产提前期**：未在单表给出整机总提前期；**最早可交付日 ≈ 最晚物料到货后 + 生产周期（需工艺参数表，当前缺失）**。

### Q-F3-02 交付卡点识别

- `MDS-202605-002`：**6** 颗物料缺料，最严重 **`PART-MOTOR-5010-PRO`**（gap 180）。
- **最早到货**：需按每颗料取 `MIN(planned_arrival_date)`；未在单次查询中全部展开。

### Q-F3-03 风险物料分级

- 可依 **`purchase_order_event.document_status`**（无 PO / 执行中 / 已收货）与 MRP 缺口联合判断；**高风险**：缺料且无执行中 PO 的料号需逐条筛。**本次未跑完分级 SQL**。

### Q-F3-04 备货周期拆解

- **无**「总备货周期 / 采购周期 / 自制周期 / 装配周期」字段于单表；需 `material_entity` 提前期 + 工艺路线 + 工单历时。**本次未给出天数拆分**。

### Q-F3-05 本月问题产品扫描（2026-05）

- 按 `mrp_plan_order_event` 中 `rootdemandbillno` 为 `MDS-202605-001/002/003` 且 `bizorderqty < adviseorderqty` 统计：**001 缺 12 行、002 缺 6 行、003 缺 11 行**。
- **结论**：三款产品在 MRP 意义上**均存在缺料行**；主要原因归纳为 **物料可供量低于建议订单量**。

### Q-F3-06 是否满足承诺交期（2026-05-31）

- MRP 需求日 `droptime` 多在 **2026-05-04～2026-05-10**；部分 PO **计划到货 2026-05-28**，相对 **2026-05-31** 承诺仍有缓冲，但相对 **MRP droptime** 已偏紧。
- **延期天数**：需排程模型；**未给出单一数值**。

---

## F4 研究与报告生成

**完整交付物**（飞书体 / 网页体 / 专项报告 / 区间汇总方法 / 周会简报）见同目录 **[`f4_deliverables.md`](./f4_deliverables.md)**，与上表 F1～F3 及金标数字对齐。

### Q-F4-01 生产计划日报

- 飞书可复制块：总体（BOM/MRP/缺料/PR）+ 行动项 + 14 天到货预测方法；逐条标注 `mrp_plan_order_event`、`bom_event`、`purchase_order_event` 等来源。

### Q-F4-02 / Q-F4-03 可生产数量

- 商务网页结构 + ATP 木桶法定义 + MRP 缺料上下文 + 补货逻辑；替代料局限已标注。

### Q-F4-04 风险物料专项报告

- 风险级别 × 影响 × 依据 × 行动表；与 MRP/PO/PR 字段挂钩。

### Q-F4-05 供应商到货预测

- 区间内 `GROUP BY supplier_name, material_code` 的 SQL 示意 + 与缺料/MRP 节点关联说明。

### Q-F4-06 月度交付汇报

- 计划量 **460 / 600 / 600** + 三款风险摘要表（与 `forecast_event`、MRP 缺料行数一致）。

---

## 说明

- **Dataview**：见 `run_meta.json` 中 `kweaver_dataview_query_calls`。
- **F4 报告层**：由模型根据 dataview 事实与金标要点生成，见 `f4_deliverables.md`；若需单独计量 LLM token，在平台用量中填写或于 `run_meta.json` 增补估算字段。
