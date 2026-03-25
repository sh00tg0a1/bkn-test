---
type: fragment
id: supplychain_hd0202_skill_md
name: HD 供应链业务知识网络 · Agent 说明
---

> **Network ID**: `supplychain_hd0202_bkn_import` | **Branch**: main | **Tags**: 供应链, 动态计划协同, 采购, 齐套分析

# HD 供应链业务知识网络

HD 供应链业务知识网络（v3）覆盖从产品需求预测到物料采购、齐套分析的完整业务链路。核心场景是"动态计划协同"：以产品需求预测单为起点，通过 MRP 展开物料需求，驱动采购申请（PR）和采购订单（PO）的生成，实时追踪物料齐套状态，触发六类智能预警，支撑 PMC 动态调整计划。

跨对象业务规则与计算逻辑见 **下文「跨对象业务规则（全文）」**；对象/关系级规则见各 `.bkn` 内「### 业务规则」。

## 核心对象

| 对象 | 文件路径 | 描述 |
|------|---------|------|
| 产品需求预测单 | `object_types/forecast.bkn` | 全链路根节点，按月滚动预测未来 3 个月需求 |
| 物料需求计划 | `object_types/mrp.bkn` | BOM 展开后的物料需求，含过滤规则和数量取值逻辑 |
| 采购申请单 | `object_types/pr.bkn` | MRP 投放触发生成，中间转换单据 |
| 采购订单 | `object_types/po.bkn` | 发给供应商的正式订单，含交货日期追踪逻辑 |
| 物料 | `object_types/material.bkn` | 物料主数据，含采购提前期（倒排关键参数）和物料属性 |
| 产品BOM | `object_types/bom.bkn` | 产品物料清单，含替代料规则（alt_priority / alt_group_no） |
| 产品 | `object_types/product.bkn` | 产成品，需求链路起点 |
| 库存 | `object_types/inventory.bkn` | 可用库存，齐套判断输入 |
| 工厂生产计划 | `object_types/mps.bkn` | 齐套后安排生产，关联预测单 |
| 供应商 | `object_types/supplier.bkn` | PO 关联供应商，交货日期监控 |
| 销售订单 | `object_types/salesorder.bkn` | 需求输入之一，关联产品 |
| 监控任务 | `object_types/monitoring_task.bkn` | 预警载体，关联预测单 |

## 核心关系

| 关系 | 文件路径 | Source → Target | 描述 |
|------|---------|----------------|------|
| 物料需求计划关联产品预测需求 | `relation_types/mrp2forecast.bkn` | mrp → forecast | **溯源核心**：rootdemandbillno → billno |
| 采购申请单关联物料需求计划 | `relation_types/pr2mrp.bkn` | pr → mrp | srcbillid → billno，PR 未下推检测 |
| 采购订单关联物料请购单 | `relation_types/po2pr.bkn` | po → pr | srcbillid → id，PO 无交货日期检测 |
| 物料需求计划关联物料 | `relation_types/mrp2material.bkn` | mrp → material | 获取采购提前期和物料属性 |
| 产品关联产品BOM | `relation_types/product2bom.bkn` | product → bom | BOM 展开入口 |
| 产品BOM关联物料 | `relation_types/bom2material.bkn` | bom → material | 获取替代料信息和提前期 |
| 物料关联库存 | `relation_types/material2inventory.bkn` | material → inventory | 齐套判断：库存可用量 |
| 采购订单关联供应商 | `relation_types/po2supplier.bkn` | po → supplier | 供应商交货监控 |
| 生产计划关联需求预测单 | `relation_types/mps2forecast.bkn` | mps → forecast | v4.2: `sourcebillnumber` 实为自制件MRP单号（见该文件「业务规则」） |
| 产品关联需求预测单 | `relation_types/product2forecast.bkn` | product → forecast | 查询产品全部预测单 |
| 产品关联库存 | `relation_types/product2inventory.bkn` | product → inventory | 成品库存判断 |
| 销售订单关联产品 | `relation_types/salesorder2product.bkn` | salesorder → product | 销售驱动需求 |
| 监控任务关联需求预测单 | `relation_types/monitor2forecast.bkn` | monitoring_task → forecast | 预警绑定预测单 |

## 网络拓扑

```
salesorder ──→ product ──→ forecast ←── monitoring_task
                │              ↑
                ↓              │ rootdemandbillno
               bom           mrp ──→ material ──→ inventory
                │              │
                ↓              ↓
             material        pr ──→ po ──→ supplier
                │
                ↓
             inventory
                                ↓
                              mps
```

核心主链路（动态计划协同）：
```
forecast → mrp → pr → po → (入库) → mps → 完成
```

## 业务规则索引

跨对象规则全文见 **「跨对象业务规则（全文）」**（本节下方）；速查表：

| 规则 | 章节 | 关键字段 |
|------|------|---------|
| 全链路数据溯源 | 规则一 | rootdemandbillno, srcbillnumber |
| BOM 替代料规则 | 规则二 | alt_group_no, alt_priority |
| MRP 过滤与数量取值 | 规则三 | closestatus_title, bizorderqty vs adviseorderqty |
| 采购进度状态三分类 | 规则四 | normal / watch / abnormal |
| 倒排计划规则 | 规则五 | purchase_fixedleadtime, 剩余天数 |
| 物料四分类（supplyStatus） | 规则六 | shortage / sufficient / sufficient_no_mrp / anomaly |
| 物料齐套判断 | 规则七 | isFullyMatched, estimatedMatchDate |
| 齐套率指标 | 规则八 | matchingRate = (readyCount + orderedCount) / totalMaterials |
| 六类预警机制 | 规则九 | PR未下推/PO无交货日期/日期未更新/超期/关键物料连续3报/倒排 |
| 进度条颜色规则 | 规则十 | ready绿#16A34A / anomaly黄#EAB308 / ordered深绿#059669 / risk红#DC2626 / on_time蓝#4F46E5 |

对象/关系级「### 业务规则」：见对应 `object_types/*.bkn`、`relation_types/*.bkn`。

## 跨对象业务规则（全文）

跨对象业务规则（动态计划协同 V2）的完整叙述如下。字段级与单对象规则见各 `object_types/*.bkn`、各 `relation_types/*.bkn` 内「### 业务规则」。

PRD 来源：`../ref/PRD_动态计划协同V2.md`

### 涉及对象类型

- 产品需求预测单 (`supplychain_hd0202_forecast`)
- 物料需求计划 (`supplychain_hd0202_mrp`)
- 采购申请单 (`supplychain_hd0202_pr`)
- 采购订单 (`supplychain_hd0202_po`)
- 物料 (`supplychain_hd0202_material`)
- 产品BOM (`supplychain_hd0202_bom`)
- 产品 (`supplychain_hd0202_product`)
- 库存 (`supplychain_hd0202_inventory`)
- 工厂生产计划 (`supplychain_hd0202_mps`)
- 监控任务 (`supplychain_hd0202_monitoring_task`)

平台中的关系映射与 PRD 应用层查询差异见本文「重要版本差异说明」。

---

### 规则一：全链路数据溯源体系

**来源**：PRD §1.6

供应链全链路的溯源路径如下（从上游到下游）：

```
产品需求预测单 → 物料需求计划 → 采购申请单 → 采购订单
(forecast)       (mrp)          (pr)          (po)
```

**关联字段精确映射**：

| 溯源跳转 | 关系文件 | Source 字段 | Target 字段 |
|---------|---------|------------|------------|
| MRP → Forecast | `mrp2forecast.bkn` | `mrp.rootdemandbillno` | `forecast.billno` |
| PR → MRP | `pr2mrp.bkn` | `pr.srcbillid` | `mrp.billno` |
| PR → MRP（API 精确查询，v4.2+）| 运行时 | `pr.srcbillnumber` | `mrp.billno` |
| PO → PR | `po2pr.bkn`（BKN 映射） | `po.srcbillid` | `pr.id` |
| PO → PR（单号，API 查询）| 运行时 | `po.srcbillnumber` | `pr.billno` |
| PO → PR（明细） | `po2pr.bkn` | `po.srcbillentryid` | `pr.entry_id` |

> **v4.2+ 精确关联**：应用层 MRP→PR、PR→PO 使用 `srcbillnumber` 批量匹配 + `biztime >= demandStart`；**已移除物料编码 Fallback**。**仅当按预测单精确查 MRP 无结果**时置 `isDegraded: true`；PR/PO 无匹配多为正常「尚未采购」，**不**因此置降级（PRD §1.6.2、§1.6.3）。`pr2mrp.bkn` 中平台侧映射仍为 `srcbillid`→`billno`，与导入 Ontology 一致。

**时间过滤口径**：所有 PR/PO 查询均叠加 `biztime >= demandStart`（需求预测开始时间），排除历史采购数据，确保数据口径一致（PRD §13.3，v3.7）。

**向下展开查询**：给定 Forecast，查 `rootdemandbillno in [billnos]` 得 MRP；再按 PRD 用 `pr.srcbillnumber`、`po.srcbillnumber` 精确下钻，并统一叠加 `biztime >= demandStart`。

---

### 规则二：BOM 替代料规则

**来源**：PRD §1.7

当 BOM 中存在替代料时，系统按以下规则处理物料需求：

**识别字段**：
- `bom.alt_group_no`：替代组编号，同一 `parent_material_code` 下组号相同则互为替代
- `bom.alt_priority`：`0` = 主料（每组唯一），`> 0` = 替代料，数值越大优先级越低（PRD §1.7）
- `bom.parent_material_code`：父级物料编码，界定替代组作用域

**评估顺序**：
1. 按 `alt_priority` 升序排列同一替代组的所有物料
2. 从优先级最高的物料开始，检查其库存 + 在途 PO
3. 若满足需求量，选用该物料，不再检查后续物料
4. 若不满足，继续检查下一优先级物料
5. 所有替代料均不满足，则标记为短缺（shortage）

**齐套判断**：替代料组内任意一种物料满足需求量，则该 BOM 行视为齐套。

---

### 规则三：MRP 有效记录过滤与数量取值规则

**来源**：PRD §4.4

**有效记录过滤（正向筛选，PRD §4.4.4）**：
- 保留 `closestatus_title === '正常'` **或** `=== 'A'` 的记录
- 其他关闭类状态不纳入「活跃 MRP」口径（优于纯排除法，避免 ERP 新增状态疏漏）

**采购数量取值优先级**（用于展示与对比）：
```
需求数量 = (bizorderqty 有效) ? bizorderqty : adviseorderqty
```
- `bizorderqty`：PMC 修订量，优先
- `adviseorderqty`：MRP 理论值，退回
- `isDegraded` **不**因两字段不一致而置位；仅用于 MRP 精确查询无结果等链路场景（PRD §4.4.5）

**投放单据类型映射**（`dropbilltype_name`）：
- 物料属性=外购 → 生产项目采购申请单（走 PR→PO 流程）
- 物料属性=自制 → 汇报生产（走生产工单流程，不生成 PR/PO）
- 物料属性=委外 → 普通委外（走委外加工流程）

---

### 规则四：采购进度状态三分类

**来源**：PRD §4.5，§5.6

系统对每条 MRP 对应的采购链路计算衍生状态（非数据库字段，运行时计算）：

| 状态 | 英文 | 判断条件 |
|------|------|---------|
| 正常 | normal | PO 已审核，`deliverdate` 有效且在需求日期前，`rowclosestatus_title` 正常 |
| 关注 | watch | PO 在途但 `deliverdate` 临近需求日期（剩余天数 ≤ 预警阈值），或 PR 已生成但未转 PO |
| 异常 | abnormal | PO `rowterminatestatus_title` 非空（已终止）；或超期未收料；或 PR 未下推且已超过下单窗口 |

进度条颜色与状态对应：
- normal → 绿色进度条
- watch → 黄色进度条  
- abnormal → 红色进度条（PRD §5.6）

---

### 规则五：倒排计划规则（齐套模式）

**来源**：PRD §5.4

**定义**：基于 BOM 层级结构，从需求截止时间向前逐层推算每个物料「最晚必须到达」的时间窗口（齐套模式倒排甘特图）。

**倒排锚点**：步骤1 需求预测截止时间 `demandEnd`（v3.1：由原 `productionStart` 改为 `demandEnd`）。

**BOM 层级倒排公式**：

L0 产品层（根节点）：
```
endDate   = demandEnd
startDate = endDate − productLeadtime
```

Ln 子件层（BFS 广度优先遍历，逐层向前推）：
```
endDate   = parent.startDate − 1天
startDate = endDate − leadtime
```

**leadtime 取值**：
```
isExternal = materialattr 为「外购」或「委外」
leadtime   = isExternal
             ? parseFloat(purchase_fixedleadtime || '0')
             : parseFloat(product_fixedleadtime || '0')
if leadtime ≤ 0: leadtime = 7  // 兜底 7 天
```
> `purchase_fixedleadtime` / `product_fixedleadtime` 在 API 中为**字符串**（如 `"25.00"`），需 `parseFloat()` 转换。

**倒排状态判断**：
- 剩余天数 > 30：充裕，无需预警
- 15–30 天：提醒（黄色）
- 7–15 天：警告（橙色）
- ≤ 7 天：紧急（红色）——齐套倒排预警（PRD §10 类型六）
- ≤ 0：已超过最迟下单日期，触发高优先级预警

**多物料最晚瓶颈**：产品齐套倒排天数 = 所有物料（全 BOM 层级）中 `startDate` 最小值为整体最早需开始采购的日期，以瓶颈物料为准。

> **工作日历说明**：当前使用自然日，ERP leadtime 基于工作日。长周期物料偏差约 30%，后续版本可引入 `ceil(leadtime / 5 × 7)` 换算。

---

### 规则六：物料四分类（supplyStatus）

**来源**：PRD §4.4.6，§13.3（v4.1 重构）

系统通过 `GanttBar.supplyStatus` 字段对每种 BOM 物料（`bomLevel > 0`）进行四分类（衍生字段，运行时由 ganttService 计算）：

| `supplyStatus` 值 | 中文 | 判断条件 | 甘特图状态 | 颜色 |
|-----------------|------|---------|----------|------|
| `shortage` | 缺货 | 有 MRP 记录且 `netDemand < 0`（有净需求缺口） | `risk` / `on_time` | 红 `#DC2626` |
| `sufficient` | 满足 | 有 MRP 记录且无净需求缺口 | `ordered` / `on_time` | 深绿 / 蓝 |
| `sufficient_no_mrp` | 就绪 | 无 MRP 记录 + 有可用库存 | `ready` | 绿 `#16A34A` |
| `anomaly` | 异常 | 无 MRP 记录 + 无可用库存 | `anomaly` | 黄 `#EAB308` |

> **v4.0 说明**：本系统**不做净需求二次计算**，`netDemand` 直接取 ERP MRP 运算结果（`bizorderqty` 优先，fallback `adviseorderqty`）。

**衍生计数字段**（用于齐套状态计算和每日监测报告）：
- `shortageCount`：`supplyStatus === 'shortage'` 的物料数
- `anomalyCount`：`supplyStatus === 'anomaly'` 的物料数
- `readyCount`：`status === 'ready'`（即 `sufficient_no_mrp`）的物料数
- `orderedCount`：`poStatus === 'has_po'` 的物料数（已下 PO）
- `totalMaterials`：`bomLevel > 0` 的物料总数（BOM 主料，`alt_priority == 0` 去重）

---

### 规则七：物料齐套判断规则

**来源**：PRD §4.5，§3.7 增强

**齐套判断逻辑**（基于 `supplyStatus` 字段，针对一张产品需求预测单）：

```typescript
const allMaterials = flattenGanttBars(bars).filter(b => b.bomLevel > 0);
const shortageItems = allMaterials.filter(b => b.supplyStatus === 'shortage');
const anomalyItems = allMaterials.filter(b => b.supplyStatus === 'anomaly');
const isFullyMatched = shortageItems.length === 0 && anomalyItems.length === 0;
```

- `isFullyMatched = true` → 显示"已齐套，可安排生产"
- `shortageItems.length > 0` → 显示"未齐套，尚有 N 项缺口"
- `anomalyItems.length > 0` → 额外显示"⚠ N 项物料异常（无MRP且无库存）"

**异常物料同样阻止齐套**（v3.7）：无 MRP 记录且无库存的物料在供应链中无任何保障，即使无短缺也不可标记为齐套。降级模式下齐套状态改为橙色"待确认"（`matched_degraded`/`unmatched_degraded`）。

**预计齐套日期**（`estimatedMatchDate`，v3.3 新增）：
- 取所有缺口物料（`supplyStatus === 'shortage'`）对应 PO 中 `deliverdate` 最晚的日期
- 若无在途 PO，则 `estimatedMatchDate = null`（不确定）
- 标注：此日期为粗略估算，不考虑工厂实际工作日历

**齐套倒计时分梯度预警**（v3.3）：
- 距需求日期 > 30 天：无预警
- 15–30 天：低级预警（提示关注）
- 7–15 天：中级预警（warning）
- ≤ 7 天：高级预警（urgent）

---

### 规则八：齐套率指标

**来源**：PRD §13.3，§8.3（每日监测报告，v4.1 修订）

**定义**：在指定时间范围内，基于 BOM 物料供需状态计算的产品物料准备完成度。

**计算公式**（v4.1，每日监测报告使用）：
```
齐套率（matchingRate）= (readyCount + orderedCount) / totalMaterials
```

- **readyCount**：`status === 'ready'`（即 `supplyStatus === 'sufficient_no_mrp'`）的物料数（无MRP但有库存，无需采购）
- **orderedCount**：`poStatus === 'has_po'` 的物料数（已下采购订单）
- **totalMaterials**：`bomLevel > 0` 的物料总数（BOM 主料，`alt_priority == 0` 去重）

**配套指标 - 采购完成率**：
```
采购完成率（procurementRate）= withPO数 / 外购委外物料总数
```

**统计口径**（PRD §13.3）：
- 物料集合 = BOM 主料 `material_code` 去重（不 union MRP 中额外的物料编码）
- 主料判定 = `alt_priority == 0`
- 每日监测报告记录趋势变化（`matchingRateChange`），首次报告基准为 0

---

### 规则九：预警机制（六大预警类型）

**来源**：PRD §10

系统自动检测以下六类预警条件，按严重程度分级（info / warning / critical）触发监控任务：

| 类型 | 预警名称 | 触发条件 | 严重程度 |
|------|---------|---------|---------|
| 一 | PR 未下推 | MRP 已投放（`dropstatus_title` = 已投放），但对应 PR 的 `joinqty = 0`（未生成 PO） | warning |
| 二 | PO 无交货日期 | PO 已审核（存在 `auditdate`），但 `deliverdate` 为空，且距审核超过阈值天数 | warning |
| 三 | 交货日期长时间未更新 | PO 的 `deliverdate` 已存在，但超过动态阈值天数未发生变更（供应商无反馈） | warning |
| 四 | 物料超期未收料 | `supplyStatus === 'shortage'` + `startDate < 今天` + `poStatus === 'no_po'`（采购过期）；或 PO `deliverdate` 已过 + `actqty < qty`（到货超期） | critical |
| 五 | 关键物料进度异常 | 物料 `purchase_fixedleadtime` 超过阈值，且连续 3 份每日监测报告均无有效进展 | critical |
| 六 | 齐套倒排预警 | 距需求日期（`forecast.startdate`）的倒排天数阶梯触发：> 30 天无、15–30 天提示、7–15 天 warning、≤ 7 天 urgent | info → warning → urgent（随天数递减升级） |

**预警三/五的精确阈值**（v3.3/v3.6 修订）：
- **类型三 - PO 交期未更新阈值**：`ceil(material.purchase_fixedleadtime × 0.2)`，最小 3 天，最大 14 天（按物料采购提前期动态计算，而非固定值）
- **类型五 - 关键物料进度异常**：须连续 3 份每日监测报告（Daily Monitoring Report）中均无进展方可触发，防止一次性噪音

**前端可计算的预警（Phase C 已实现，4类）**：
1. 齐套倒计时（类型六）
2. 缺口未下PO（`supplyStatus === 'shortage' && poStatus === 'no_po'`）
3. 超期未到料（`endDate > demandEnd`）
4. 异常物料（`supplyStatus === 'anomaly'`）

**预警聚合**：相同产品/相同预测单下的多条同类预警合并为一条，避免重复通知。

**预警关闭条件**：
- 类型一：PR 的 `joinqty > 0`（已生成 PO）后自动关闭
- 类型二/三：PO 的 `deliverdate` 更新后自动关闭
- 类型四：PO 的 `actqty = qty`（完全入库）后自动关闭
- 类型五/六：物料达到齐套条件后自动关闭

---

### 规则十：进度条状态与颜色规则

**来源**：PRD §5.6（v4.1 重构为五分类）

系统在甘特图中对每种 BOM 物料展示进度条（`GanttBar.status`），颜色编码按优先级从高到低判定：

| `status` 值 | 颜色 | 色值 | 触发条件（按优先级顺序执行）| 优先级 |
|------------|------|------|--------------------------|-------|
| `ready` 就绪 | 绿色 | `#16A34A` | 无MRP记录 + 有库存（`supplyStatus === 'sufficient_no_mrp'`） | 1（最高）|
| `anomaly` 异常 | 黄色 | `#EAB308` | 无MRP记录 + 无库存（`supplyStatus === 'anomaly'`） | 2 |
| `ordered` 已下单 | 深绿色 | `#059669` | `poStatus === 'has_po'`（已下采购订单） | 3 |
| `risk` 风险 | 红色 | `#DC2626` | `startDate < 今天` 且 `poStatus === 'no_po'`，或 `endDate > parent.startDate` | 4 |
| `on_time` 正常 | 蓝色 | `#4F46E5` | 其他情况（有MRP、无风险、无PO但时间充裕） | 5（最低）|

> **v4.1 变更**：从三分类（on_time/risk/ordered）扩展为五分类，新增 `ready`（无MRP但有库存，无需采购）和 `anomaly`（无MRP且无库存，需核查）。`ready`/`anomaly` 优先于 `ordered`/`risk` 判定。

**甘特图行背景与左侧标签**：
- `hasShortage = true`：行背景红色 `bg-red-50`，左侧标签 `⚠缺`
- `status === 'ready'`：行背景绿色 `bg-green-50/30`，左侧标签 `✓`
- `status === 'anomaly'`：行背景黄色 `bg-yellow-50/30`，左侧标签 `?`

**倒排天数显示**：进度条旁显示最近截止节点的剩余倒排天数，格式为 "还有 X 天"，超期显示 "已超期 X 天"（PRD §5.6）。

**无MRP物料的PR/PO显示**：Tooltip 中 PR/PO 状态显示 `N/A`，任务条上显示"无MRP"文字标签，不做采购进度状态判定（不标 normal/watch/abnormal）。

## 查询策略（object-type query）

为避免返回数据过大导致截断或解析失败，建议遵循以下约束：

1. **通用上限**：`limit` 不要超过 `30`（默认可用 `20~30`）
2. **BOM 特殊约束**：查询 `bom` 时，单次 `limit` **建议不超过 `10`**
3. **需要更多数据时分页**：使用 `search_after` 取下一批，**不要**通过增大 `limit` 获取更多结果
4. **先过滤再分页**：优先加 `condition`（如物料号、版本、状态），避免全表扫描

示例（BOM 分批查询）：

```bash
# 第 1 批
kweaver bkn object-type query <kn> bom '{"limit":10,"condition":[...]}'

# 第 2 批（使用上一批返回的 search_after）
kweaver bkn object-type query <kn> bom '{"limit":10,"condition":[...],"search_after":["v1","v2","v3"]}'
```

## 使用场景

**查询某产品的齐套状态**：
1. 读 `object_types/forecast.bkn` 了解预测单结构
2. 读 `relation_types/mrp2forecast.bkn` 了解 MRP 关联方式
3. 读本 SKILL「跨对象业务规则」**规则七**

**分析采购进度异常**：
1. 读 `object_types/po.bkn` 了解 PO 字段
2. 读 `relation_types/po2pr.bkn` 了解 PO→PR 关联
3. 读本 SKILL「跨对象业务规则」**规则九**

**全链路溯源（从 PO 溯源到预测单）**：
1. `PO.srcbillid` → `PR.id`（关系：`po2pr`）
2. `PR.srcbillid` → `MRP.billno`（关系：`pr2mrp`）
3. `MRP.rootdemandbillno` → `Forecast.billno`（关系：`mrp2forecast`）

精确查询与 v4.2 字段优先级见本 SKILL「跨对象业务规则」**规则一**及「重要版本差异说明」。

### 当前批次数据查询（历史数据隔离）

> **核心问题**：按 `material_number` 直接查询 PR/PO/工单会返回**所有历史批次**的数据，不仅限当前预测单。必须按以下链路逐层关联，才能获取当前批次的精确数据。

**标准查询链路**（给定预测单 `forecast.billno`）：

```
Step 1: 查当前批次 MRP
  → 条件: mrp.rootdemandbillno = forecast.billno
  → 结果: 当前批次的全部 MRP 记录

Step 2: 查当前批次 PR
  → 从 Step 1 结果中提取所有 MRP 的 billno 列表
  → 条件: pr.srcbillnumber in [mrp_billno_list]
  → 叠加时间过滤: pr.biztime >= forecast.startdate
  → 结果: 当前批次的 PR 记录

Step 3: 查当前批次 PO
  → 从 Step 2 结果中提取所有 PR 的 billno 列表
  → 条件: po.srcbillnumber in [pr_billno_list]
  → 叠加时间过滤: po.biztime >= forecast.startdate
  → 结果: 当前批次的 PO 记录

Step 4: 查当前批次工单（MPS）
  → 从 Step 1 结果中提取自制件 MRP 的 billno 列表
  → 条件: mps.sourcebillnumber in [selfmade_mrp_billno_list]
  → 结果: 当前批次的生产工单
```

**反模式（禁止）**：
- ❌ 用 `material_number` 直接查 PR/PO/工单 → 返回所有历史批次，导致误判
- ❌ 不加 `biztime >= demandStart` 时间过滤 → 混入更早的采购记录

**简化场景**：若已知当前批次 PR 的 `billno`（如 `CGSQ-260228-000014`），可直接用 `po.srcbillnumber = PR_billno` 查关联 PO，跳过 Step 1-2。

## 重要版本差异说明

以下是 **BKN / 平台关系映射** 与 **PRD 动态计划协同实现** 之间的已知差异，查数与建模时须对照使用：

| 项目 | BKN / 平台映射 | PRD v4.2+ 应用行为 | 说明 |
|------|---------------|-----------------|------|
| PR → MRP | `pr2mrp`：`srcbillid`→`billno` | API：`pr.srcbillnumber in [mrpBillnos]` + 时间过滤 | 导入以 BKN 为准；运行时查询以 PRD 为准 |
| PO → PR | `po2pr`：`srcbillid`→`id` 等 | API：`po.srcbillnumber in [prBillnos]` + 时间过滤 | 同上 |
| MPS `sourcebillnumber` | 数据视图注释为预测单号；关系 `mps→forecast` 映射 `sourcebillnumber`→`billno` | 工单查询：`sourcebillnumber in [selfMadeMrpBillnos]` | ERP 实际存值可能为 MRP 单号，见 `mps2forecast.bkn` |
| Fallback / 降级 | 历史曾用物料编码兜底 | v4.2+ 无物料编码 Fallback | **仅 MRP 精确无结果** → `isDegraded`；PR/PO 空结果不降级 |

## 按功能分组

- **计划域**：`forecast.bkn`, `mrp.bkn`, `mps.bkn`
- **采购域**：`pr.bkn`, `po.bkn`, `supplier.bkn`
- **物料主数据**：`material.bkn`, `bom.bkn`, `product.bkn`
- **库存域**：`inventory.bkn`
- **需求域**：`salesorder.bkn`, `monitoring_task.bkn`
- **跨对象业务规则**：本文件「跨对象业务规则（全文）」；概念分组索引：`concept_groups/dynamic_planning_collab.bkn`
- **网络根**：`network.bkn`
