# Suite-4 PMC 场景 — Dataview 拉数答案（test_run_20260327104600）

依据：`kweaver dataview query` 对数据源 `90b93fb3-4d8e-42db-8c1a-84f8658364f6`（catalog `mysql_1j6tsjwo."supply_chain_data"`）。以下为归纳结论，**非金标对照**。

---

## F1 基础信息查询

### Q-F1-01 产品库存查询

- **成品库存（`inventory_event`，`item_code=UAV-BF-IND-H20`，中央成品仓）**：**2216 台**（`quantity=2216`，`status=Active`）。
- **在库 / 在途 / 冻结**：当前快照行未拆分「在途」「冻结」字段；**无法从本表直接给出**在途、冻结台数。
- **参考（非标准在途库存）**：`shipment_event` 中同产品、`delivery_status=运输中` 的数量合计 **1174 台**（发运口径，不宜等同 WMS 在途）。

### Q-F1-02 需求预测单查询

- `forecast_event`：`billno=MDS-202605-002`，物料 **霸风30L植保无人机**，`qty=600` 台，`enddate=2026-05-30`。
- **状态**：`status=Active`；库中无「草稿/已确认」枚举，**无法**严格回答草稿或已确认。

### Q-F1-03 物料 PO 查询

- 极风整机 `UAV-JF-ENT-AG` → 子件 `ASSY-PWR-TQ` → 电机料号 `**PART-MOTOR-4114-400KV`**（4114 400KV 高扭矩电机）。
- **未关闭（`document_status=执行中`）PO 示例**：`PO-202605-0317`，供应商 **索尼半导体解决方案**，订货量 **3420**，`planned_arrival_date=2026-05-17`，`required_date=2026-05-22`。其余同料号样本多为 **已收货**。

### Q-F1-04 物料库存查询

- BOM 上飞控为 `**ASSY-FC-RTK`（RTK 高精度飞控总成）**。
- **各仓数量汇总（`inventory_event`）**：`ASSY-FC-RTK` 合计 **5278**；子件示例 `COMP-FC-PCB-R1` **3743**。
- **与安全库存**：未见可靠 `safety_stock` 字段；`shortage_flag` 为 **否**，**无法**断言是否低于安全库存水位。

### Q-F1-05 BOM 结构查询

- `**UAV-BF-IND-H30` 直属 BOM 行**：**10** 行。
- **子 BOM**：仅 `**ASSY-FC-RTK`** 下挂子层，**5** 行。
- **展开行数**：10 + 5 = **15** 行（一层子展开）。
- **层数**：约 **3 层**（成品 → 直属件/总成 → 飞控子件，无统一 level 字段时为归纳）。
- **自制/采购（按 `assembly_set` 行级近似）**：直属 9「是」/1「否」；`ASSY-FC-RTK` 下 4「是」/1「否」；合计 **自制 13 行、采购 2 行**（行计数，非物料去重种类数）。

### Q-F1-06 供应商信息查询

- 喷洒组件取 `**PART-SPRAYER-16L`（16 升智能喷洒系统）**。
- `purchase_order_event` 按供应商汇总（样本）：**深圳农业喷洒系统公司** 8 笔 PO、平均下单至计划到货约 **32.5 天**；索尼、TI 代理、ST、芯源等亦有记录。
- **准时率（小样本）**：`material_procurement_event` 中 TI 代理、该料号 **2** 笔、准时率 **100%**（样本量小，仅作参考）。

---

## F2 MRP 状态分析

### Q-F2-01 MRP 投放状态

- `mrp_plan_order_event`：`rootdemandbillno=MDS-202605-001` 存在多行计划。
- **最近一次 MRP 时间**：`MAX(createtime)=2026-03-25 10:00:00`。

### Q-F2-02 缺料汇总分析

- `rootdemandbillno=MDS-202605-002` 且 `bizorderqty < adviseorderqty`：**6** 条缺料行。
- **缺口最大的前 5（按 gap）**：`PART-MOTOR-5010-PRO` gap **180**；`PART-CONN-GH-1.25-10P` gap **120**；`PART-SPRAYER-30L`、`PART-4G-MODULE`、`COMP-FC-CASE-AL-IND`、`PART-FPGA-ICE40` 等 gap **30**。

### Q-F2-03 PO 交期符合率（MDS-202605-003 缺料）

- 缺料行 **11** 条。
- 示例：`PART-4G-MODULE` 存在执行中 PO，`planned_arrival_date`（如 **2026-05-28**）**晚于** MRP 需求侧 `required_date`（**2026-05-18**）的情形 → **存在 PO 计划到货不覆盖需求日的风险**；需按每颗缺料料号与其有效 PO 逐条核对。

### Q-F2-04 PR 待转换清单

- `purchase_requisition_event` ⋈ `mrp_plan_order_event`（`pr.srcbillid = mrp.billno`），`rootdemandbillno=MDS-202605-001`：**20** 张不同 `billno` 的 PR。
- **未完结审批（`status <> 已审批`）**涉及物料示例：`PART-CAM-FPV`、`PART-SPRAYER-20L`、`PART-RADAR-ALT`、`PART-PROP-1755-CF`、`PART-CABLE-ESC-HD`、`RAW-LIPO-CELL`、`PART-MCU-STM32H753`、`PART-PCB-FC-8L`、`PART-FPGA-ICE40`、`RAW-COPPER-WIRE`、`RAW-SI-WAFER-12IN`、`RAW-FR4-CCL` 等。
- **PR→PO**：`purchase_order_event.srcbillid` 多为空，**无法用库内字段可靠判定**是否已转 PO。

### Q-F2-05 自制件 MRP 状态

- 霸风 30L 直属 BOM 含 `**PART-FRAME-HEX-CF-HD`（机架）**、`PART-SPRAYER-30L` 等；子 BOM 仅 `**ASSY-FC-RTK`** 展开。
- `mrp_plan_order_event` 可见 `materialattr_title=自制/外购`、`dropstatus_title` 等；与 **600 台预测**是否充分匹配需结合工单与缺口逐条核对，**本次未做完整工单闭环证明**。

### Q-F2-06 齐套率分析

- 库内无统一「齐套率」字段；完整计算需 BOM 全展开与库存/在途聚合。
- **代理指标**：`MDS-202605-003` 上 `**bizorderqty < adviseorderqty` 行数 = 11**。

---

## F3 交期复杂分析

### Q-F3-01 批次最早交货日

- `MDS-202605-001` 缺料行含 `ASSY-FC-RTK`、`PART-4G-MODULE`、`PART-MOTOR-4114-400KV` 等；MRP `enddate` 多在 **2026-05-20～2026-05-26**。
- 对缺料料号在 `purchase_order_event` 上 `**MAX(planned_arrival_date)`** 的抽样结果中，`**PART-4G-MODULE` 最晚至 2026-05-28** 等；再叠加 `**product_entity` 无生产提前期字段**，**无法给出唯一「最早具备交付日」**，仅能判断 **瓶颈到货不早于约 2026-05-28 量级（需加装配提前期，数据不足）**。

### Q-F3-02 交付卡点识别

- 霸风 30L / `MDS-202605-002` 缺料包括 `**PART-MOTOR-5010-PRO`、`PART-CONN-GH-1.25-10P`、`PART-SPRAYER-30L`、`PART-4G-MODULE`** 等；**关键卡点**可优先取 **gap 最大**的前两颗电机与连接器。
- **最早到货**：需按每料号取有效 PO 的 `planned_arrival_date`；示例 `**PART-4G-MODULE`** 执行中 PO 计划到货 **2026-05-28**（与需求日存在偏差）。

### Q-F3-03 风险物料分级

- 结合 `**purchase_order_event.risk_level`、`document_status`** 与是否缺料：**高风险**：缺料且无执行中 PO 或风险等级「高」的料号（需逐料查询）；**中风险**：PO 已下达但 `**planned_arrival_date` 偏晚**于 MRP `enddate`（如 `PART-4G-MODULE`）。

### Q-F3-04 备货周期拆解

- `**product_entity`** 当前字段未包含 **采购周期 / 生产周期 / 装配周期** 分项；**无法从本数据源直接拆分**总备货周期。

### Q-F3-05 本月问题产品扫描

- 结合 `**forecast_event`（2026-05 需求）** 与 `**mrp_plan_order_event` 缺料行**：三款产品均可能存在 **缺料/交期** 类风险；具体「主要风险原因」需按各产品关联 `rootdemandbillno` 汇总缺料与 PO 覆盖情况（本次未逐产品展开全量）。

### Q-F3-06 是否满足承诺交期

- 客户承诺 **2026-05-30**（与预测 `enddate` 同量级）；`**PART-4G-MODULE`** 等存在 **计划到货 2026-05-28** 仍偏紧、且多料仍缺口的记录 → **存在不能按时齐套的风险**；**精确延期天数**需完工与排产数据，**本次未算**。

---

## F4 研究与报告生成

### Q-F4-01 生产计划日报

- **要点**：`MDS-202605-001` 缺料 **12** 行量级；PR **20** 张关联 MRP，其中多笔 **审批中**；最近一次 MRP **2026-03-25 10:00:00**。
- **数据来源**：`mrp_plan_order_event`、`purchase_requisition_event`、`purchase_order_event`、`bom_event`、`inventory_event`。
- **飞书排版**：本次仅列要点，未生成飞书卡片/HTML。

### Q-F4-02 可生产数量综合分析（霸风 30L）

- 需按 **H30 全 BOM 多层**与 **库存 + 在途 PO + 替代料** 做 min 运算；**本次未跑完整 ATP**，仅提示：**缺料行 6 条**（`MDS-202605-002`），**无法**直接给「最多可生产台数」与「再产 50 台补货清单」的精确数。

### Q-F4-03 可生产数量综合分析（极风农业版）

- 同 F4-02，需全 BOM + 替代组；**本次未算**最大可生产台数与最少补货情景。

### Q-F4-04 风险物料专项报告（MDS-202605-001）

- **风险清单**：缺料行见 F3-01 列表；**风险级别**可参考 `purchase_order_event.risk_level` 与 PR `status`（审批中）。
- **依据**：`mrp_plan_order_event`、`purchase_order_event`、`purchase_requisition_event`。

### Q-F4-05 供应商到货预测报告（2026-05-01～05-14）

- 对三款产品 BOM 子件在窗内的 `**purchase_order_event`** 抽样：**2026-05-04** `PART-SPRAYER-16L`；**2026-05-06** `PART-MOTOR-5010-PRO`；**2026-05-08** `ASSY-PWR-TQ`；**2026-05-14** `PART-CAM-FPV`、`PART-SPRAYER-16L` 等。
- **影响生产节点**：窗内到货的 **动力/喷洒/相机** 类物料通常直接约束总装投料。

### Q-F4-06 月度整体交付汇报


| 预测单            | 产品    | 计划数量（forecast_event） | 交付窗口（enddate） |
| -------------- | ----- | -------------------- | ------------- |
| MDS-202605-001 | 霸风20L | 460                  | 2026-05-30    |
| MDS-202605-002 | 霸风30L | 600                  | 2026-05-30    |
| MDS-202605-003 | 极风农业版 | 600                  | 2026-05-30    |


- **可确认交付量 / 延期量**：需结合 ATP 与工单执行，**本次未汇总为单一数字**；缺料与 PO 风险见上各题。

---

## 说明

- 部分 SQL 因列名与 Vega 解析差异 **失败重试**（见 `run_meta.json` 的 `failed_attempt_notes`）。
- **LLM token**：未调用 `kweaver agent chat`，平台侧 **记 0**；本文件为会话归纳，非 CLI 计量。

