# Suite-3 · PMC 智能问答系统 — PRD 解析与测试设计

> 依据：[ref/suite-3/PMC智能问答系统_PRD_v1.0.docx](../../ref/suite-3/PMC智能问答系统_PRD_v1.0.docx)  
> 数据基线：[ref/suite-3/supplychaindata_1/](../../ref/suite-3/supplychaindata_1/)（UAV 供应链示例数据）

---

## 1.1 功能模块清单（Agent 能力域）

PRD 将能力分为四类，本测试集用 **F1–F4** 标注每题所属能力：

| 类别 | 说明 | 典型能力 |
|------|------|----------|
| **F1 基础信息查询** | 库存、物料、预测、PO、供应商、BOM 等单表/简单关联查询 | 产品/物料库存、预测单明细、PO 状态与交期、供应商付款条件与交期、BOM 结构 |
| **F2 MRP 状态分析** | 基于需求来源的 MRP 结果、缺料、PR/PO 联动 | MRP 行数、缺料行（bizdropqty）、PR 与 MRP 对应、齐套/缺料排序 |
| **F3 交期复杂分析** | 发货、工单、承诺交期、到货窗口、风险扫描 | 发货预计/实际签收、工单计划完工、MRP availabledate 窗口、销售订单交期承诺 |
| **F4 研究与报告型** | 汇总、统计、跨表摘要（本数据集中以可计算的汇总指标代替完整 HTML 报告） | 缺货行统计、BOM 规模、主数据条数、数据覆盖摘要 |

---

## 1.2 用户角色画像

| 角色 | 核心诉求 | 常用术语 | 提问风格 |
|------|----------|----------|----------|
| 业务领导 | 交期、风险、能否按时交付 | 交期、卡点、风险、本月 | 口语化、要结论 |
| PMC 计划员 | MRP、缺料、齐套、预测与工单 | MRP、FCST、缺料、PR/PO、齐套 | 数字敏感、单据号明确 |
| 物料管理员 | PO 交期、在途、供应商 | PO、到货、交期、芯源/TI | 简短、跟单式 |
| 供应链管理者 | 全局统计、备货与供应安全 | 库存水位、供应商数、数据覆盖 | 分析型、汇总型 |

---

## 1.3 核心数据实体与 CSV 映射

| 业务实体 | CSV 文件 | 说明 |
|----------|----------|------|
| 产品主数据 | `product_entity_*.csv` | product_id / product_code / product_name |
| 物料主数据 | `material_entity_*.csv` | material_id / material_code |
| BOM | `bom_event_*.csv` | parent_code / child_code / quantity |
| 库存快照 | `inventory_event_*.csv` | item_type(Product/Material), item_id, item_code, warehouse_id, snapshot_month, quantity, shortage_flag |
| 需求预测 | `forecast_event_*.csv` | billno, material_number, qty, customer_id |
| MRP 计划 | `mrp_plan_order_event_*.csv` | billno, rootdemandbillno, materialplanid_number, bizdropqty, availabledate, dropstatus_title |
| 采购申请 | `purchase_requisition_event_*.csv` | billno, srcbillid→MRP billno, material_number, status |
| 采购订单 | `purchase_order_event_*.csv` | purchase_order_number, planned_arrival_date, document_status |
| 物料采购执行 | `material_procurement_event_*.csv` | 与供应商、仓库、物流相关的采购执行明细 |
| 供应商 | `supplier_entity_*.csv` | payment_terms, lead_time_avg, risk_level |
| 仓库 | `warehouse_entity_*.csv` | warehouse_id, warehouse_name |
| 客户 | `customer_entity_*.csv` | is_named_customer, has_contract |
| 销售订单 | `sales_order_event_*.csv` | order_status, planned_delivery_date |
| 发货 | `shipment_event_*.csv` | estimated_delivery_date, actual_delivery_date |
| 生产工单 | `production_order_event_*.csv` | planned_finish_date, work_order_status |
| 领料 | `material_requisition_event_*.csv` | production_order_number, material_id |

**库存字段说明**：成品/物料在 `inventory_event` 中 `quantity` 为快照数量；物料行同时存在 `item_id`（如 M0001）与 `item_code`（物料编码如 ASSY-xxx）。

---

## 2. 测试集结构（100 题）

| 分组 | 行为类型 | 题量 | 占比 |
|------|----------|------|------|
| S1 | 规范查询 | 20 | 20% |
| S2 | 口语/模糊查询 | 30 | 30% |
| S3 | 追问/下钻 | 20 | 20% |
| S4 | 异常/边界 | 20 | 20% |
| S5 | 多意图混合 | 10 | 10% |

### 2.1 各组功能覆盖（计划内分配）

- **S1**：F1×6 + F2×5 + F3×5 + F4×4  
- **S2**：F1×10 + F2×8 + F3×8 + F4×4  
- **S3**：F1×4 + F2×6 + F3×6 + F4×4（含「上文假设」）  
- **S4**：F1×6 + F2×5 + F3×5 + F4×4（含不存在编码、超范围、只读边界）  
- **S5**：跨 F1–F4 混合 10 题  

### 2.2 金标来源

- 标准答案由 **[scripts/suite3/compute_answers.py](../../scripts/suite3/compute_answers.py)** 对 CSV **验算**；用例 Markdown 由 **[scripts/suite3/generate_suite3_markdown.py](../../scripts/suite3/generate_suite3_markdown.py)** 生成（`python3 scripts/suite3/generate_suite3_markdown.py`）。
- 关键汇总指标可通过 **[scripts/suite3/verify_suite3.py](../../scripts/suite3/verify_suite3.py)** 回归校验（`python3 scripts/suite3/verify_suite3.py`）。

---

## 3. 文件索引

| 路径 | 说明 |
|------|------|
| [00_评分标准与测试方法.md](./00_评分标准与测试方法.md) | 评分与报告规范 |
| `cases/S*.md` | 完整用例（含行为类型、功能类别、角色、标准答案等） |
| `questions/S*.md` | 仅题目（S3 含上文假设） |
| `answers/S*.md` | 涉及对象、关键字段、标准答案 |

---

*文档版本：v1.0（Suite-3）*
