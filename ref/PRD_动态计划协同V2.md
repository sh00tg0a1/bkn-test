# 新版动态计划协同系统 - 产品需求文档 (PRD)

> **版本**: v4.4
> **创建日期**: 2026-01-26
> **更新日期**: 2026-03-20
> **作者**: Claude AI
> **状态**: Phase A+B+C+D 已完成（第一期全部完成）；v4.4 PRD 与实现对齐更新
> **基线版本**: v2.10（已上线运行）
> **知识网络**: HD供应链业务知识网络_v3

---

## 1. 概述

### 1.1 项目背景

客户对现有动态计划协同板块总体认可，其目标是实现产品生产计划交期目标，看进度、找问题、给建议，从而服务于采购供应决策优化。

**v3.0 优化驱动**：基于客户需求调研反馈，当前系统存在以下核心问题需要解决：
1. **预测单滚动叠加**：生产计划为滚动式，无明确结束节点，历史预测数据无限叠加，导致计划跟踪性弱、无法做达成率统计
2. **MRP 数据源不准**：原 Excel 数据已弃用，需统一从 ERP MRP 取数；历史 PR/PO 未过滤导致数据失真
3. **生产工单管理缺失**：缺少生产工单级别的跟踪和完成判定
4. **预警与报告不足**：缺少系统化的预警触发和每日监测报告

### 1.2 核心设计理念（v3.1 明确）

> **产品需求预测单是整个计划协同的核心对象。**

业务流程：**预测单 -> MRP 物料配套 -> PR/PO 采购跟踪 -> 物料齐套 -> 安排生产（生产工单）**

- 监测的核心对象是**产品需求预测单**（即产品）
- 预测单确定后，系统展开 BOM、运行 MRP，跟踪物料的 PR/PO 下达和到料情况
- **物料齐套后**，才安排生产（下达生产工单），生产工单是下游动作，不是创建监测任务时需要确认的前置条件
- 生产工单的状态在监测任务中**跟踪展示**，而非在任务创建流程中设定

### 1.3 目标

- 以**产品需求预测单**为核心，提供完整的计划跟踪体系：需求预测 -> 物料需求计划(MRP) -> 采购跟踪(PR/PO) -> 物料齐套提醒 -> 生产工单跟踪
- 基于齐套模式实现生产计划倒排排程甘特图
- 通过监测任务机制持续跟踪关键产品的物料备料状态
- **v3.0 新增**：预测单按月拆分、计划结束逻辑、MRP 数据过滤与净需求计算、物料齐套后生产提醒、预警机制
- 减少"缺料停工、备料积压、订单交付难"问题

### 1.4 核心功能

| 模块 | 功能描述 | v3.0 变更 |
|------|---------|----------|
| 产品需求预测（步骤1） | 从 Ontology 加载产品列表和需求预测，用户选择产品并确认需求参数 | 预测单按月拆分呈现，支持计划截止时间设定 |
| 物料需求计划（步骤2） | 展开 BOM 计算物料净需求，显示缺口和 PR/PO 状态 | **MRP 数据源变更为 ERP MRP**，取业务方修正数据，过滤已关闭单据 |
| 智能计划协同（步骤3） | 生成齐套模式倒排甘特图，创建监测任务持续跟踪 | 新增物料齐套提醒、生产工单关联展示、预警机制 |

### 1.5 术语定义

| 术语 | 定义 |
|------|------|
| 产品需求预测单 | 业务方基于销售需求制定的产品需求预测，按"产品+月份"维度管理，是整个计划协同的**核心驱动对象**（`supplychain_hd0202_forecast`） |
| 生产工单 | ERP 生产工单，物料齐套后按自制件单独下达，包含工单状态、领料状态、入库数量等（`supplychain_hd0202_mps`，数据源 `erp_production_work_order`） |
| 物料需求计划(MRP) | ERP MRP 运算产生的计划订单，包含建议订单数量和业务修正后的订单数量（`supplychain_hd0202_mrp`，数据源 `erp_mrp_plan_order`） |
| 齐套模式 | 从需求预测截止时间倒推，确保所有子级物料/组件齐套后才能开始上级生产 |
| 主料 | BOM 中 `alt_priority == 0` 的物料，是替代组内的首选物料（详见 1.7 BOM 替代料规则） |
| 替代料 | BOM 中 `alt_priority > 0` 的物料，与主料属同一替代组（`alt_group_no` 相同），不纳入甘特图和 MRP 统计 |
| 替代组 | 同一 `parent_material_code` 下、`alt_group_no` 相同的一组物料，组内 `alt_priority=0` 为主料，`alt_priority>0` 为替代料 |
| 监测任务 | 用户创建的跟踪记录，持久化保存在 localStorage，以产品需求预测单为核心监测对象 |
| 销售订单 | 客户签约的订单信息，包含合同编号、签约数量、承诺交期、交付情况（`supplychain_hd0202_salesorder`） |
| 根需求单号 | MRP 计划订单中的 `rootdemandbillno` 字段，关联到产品需求预测单的 `billno`，实现从预测单到物料需求的全链路溯源 |
| 来源单据编号 | 生产工单中的 `sourcebillnumber` 字段，关联到自制件 MRP 计划订单的 `billno`（v4.2 变更：由预测单 billno 改为 MRP billno），实现从 MRP 到生产工单的精确溯源 |
| 来源单据ID | PR 中的 `srcbillid` 字段，关联到 MRP 的 `billno`；PO 中的 `srcbillid` 字段，关联到 PR 的 `id`（主键） |

### 1.6 全链路数据溯源体系（v3.4 新增）

> **核心原则**：计划协同从产品需求预测开始，到工厂生产计划结束。每个业务对象之间通过 ERP 单据流转的关联字段实现精确溯源。预测单→MRP 和预测单→生产工单已实现纯精确关联（v4.2），MRP→PR→PO 环节精确关联优先、物料编码匹配作为兜底。

#### 1.6.1 正向溯源链路（预测 -> 生产）

```
产品需求预测单 (forecast)
  │ billno = "MDS-20260301-001"
  │
  ├──→ 物料需求计划 (MRP)
  │     关联字段: mrp.rootdemandbillno == forecast.billno
  │     含义: MRP 计划订单的根需求来源于哪张预测单
  │     │
  │     ├──→ 采购申请单 (PR)
  │     │     关联字段: pr.srcbillid == mrp.billno
  │     │     含义: PR 是从哪张 MRP 计划订单投放生成的
  │     │     │
  │     │     └──→ 采购订单 (PO)
  │     │           关联字段: po.srcbillid == pr.id (PR主键)
  │     │           辅助关联: po.srcbillentryid == pr.entry_id (PR明细主键)
  │     │           含义: PO 是从哪张 PR 下推生成的
  │     │
  │     └──→ 库存 (Inventory)
  │           关联字段: inventory.material_code == mrp.materialplanid_number
  │           含义: 该物料的实时库存状态
  │
  └──→ 生产工单 (MPS)
        关联字段: mps.sourcebillnumber == 自制件MRP.billno（v4.2：经由 MRP 精确关联）
        含义: 生产工单是基于哪条 MRP 计划订单下达的（自制件）
```

#### 1.6.2 关联查询策略与 Fallback 规则

每个环节采用**纯精确关联**策略（v4.2+ 全面升级，物料编码 Fallback 已全部移除）：

| 环节 | 精确关联（唯一策略） | 无结果处理 | 降级影响 |
|------|----------------|-----------|---------|
| **预测单 → MRP** | `mrp.rootdemandbillno in [selectedBillnos]` | 直接返回空 + `isDegraded: true`，提示用户在 ERP 中先执行 MRP 运算 | 所有物料标记为"无MRP"状态，甘特图按库存判定 ready/anomaly |
| **MRP → PR** | `pr.srcbillnumber in [mrpBillnos]` + **时间范围过滤**：`pr.biztime >= demandStart` | MRP 单号列表为空时直接返回空（不降级，不走物料编码兜底） | 无 Fallback：PR 无精确匹配时清单为空 |
| **PR → PO** | `po.srcbillnumber in [prBillnos]` + **时间范围过滤**：`po.biztime >= demandStart` | PR 单号列表为空时直接返回空（不降级） | 无 Fallback：PO 无精确匹配时清单为空 |
| **自制件MRP → 生产工单** | `mps.sourcebillnumber in [selfMadeMrpBillnos]`（自制件 MRP 计划订单单号 → 生产工单来源单据号） | 精确查询无结果返回空列表，提示"当前尚无匹配相应需求预测单的生产工单" | 无 Fallback，精确查询无结果 = 空列表 |
| **物料 → 库存** | `inventory.material_code in [materialCodes]` | API 异常/超时时标记为"库存数据不可用"，齐套判定暂挂 | 无二级 Fallback |
| **产品 → BOM** | `bom_material_code == productCode` + 版本过滤 + `alt_priority == 0` | BOM 查询返回空时，整个流程中断，提示"该产品 BOM 数据不可用" | 无二级 Fallback |

> **v4.2+ 变更说明**：MRP→PR 和 PR→PO 环节已彻底移除物料编码兜底（Fallback）策略。此前 Fallback 模式下物料编码匹配会引入其他批次/项目的无关 PR/PO，造成采购状态判定严重失真。现改为：精确关联无结果时直接返回空，降级标志（`isDegraded`）仅在 MRP 精确查询无结果时设为 `true`，PR/PO 无结果不触发降级（因为空结果是业务上正常的"尚未采购"状态）。

> **Fallback 触发条件**（v3.6 增强）：
> 1. **查询返回空**：精确关联返回 0 条结果时，自动切换到 Fallback 模式
> 2. **查询异常/超时**：API 调用失败时，**不自动降级**，而是重试 1 次。重试仍失败时提示用户"数据加载异常，请刷新重试"
> 3. **部分匹配**：精确关联返回结果数量明显偏少（如 MRP 记录数 < BOM 主料数的 30%），在数据溯源面板提示"精确关联数据可能不完整，可切换兜底模式对比"
> 4. **级联降级**：当上游环节已降级时（如 MRP 使用了 Fallback），下游环节（PR/PO）即使使用精确关联，也需标记为"受上游降级影响"，整条链路的降级状态在数据溯源面板中完整展示
>
> 页面需在数据溯源面板中标注当前使用的关联方式（精确/兜底/受上游降级影响），让用户知晓数据精度。**降级标识应同时在步骤标题旁以橙色标签形式外显**（如"数据精度：兜底模式"），而非仅在可折叠的溯源面板中展示。

> **PR/PO 时间范围过滤原则（v3.7 新增）**：
> 采购申请（PR）和采购订单（PO）是基于产品需求预测发起的下游业务动作，其创建时间必然**晚于需求预测时间**。因此 PR/PO 查询需增加时间下界过滤：`biztime >= task.demandStart`（预测单最早 startdate）。
> - **业务逻辑**：某个预测单驱动的采购行为不可能早于预测单本身的开始时间
> - **技术效果**：有效排除历史批次的同物料 PR/PO 记录，显著减少 Fallback 模式下的数据混入
> - **适用范围**：无论精确关联还是 Fallback 模式，PR/PO 查询均应叠加此时间过滤条件

#### 1.6.3 当前实现状态（v4.2+ 全面落地精确关联）

| 环节 | 当前实现 | 说明 |
|------|---------|------|
| 预测单 → MRP | `rootdemandbillno in [selectedBillnos]` 精确关联，无结果返回空 + `isDegraded: true` | v4.1 落地，已移除全量 fallback |
| MRP → PR | `pr.srcbillnumber in [mrpBillnos]` + `biztime >= demandStart` 精确关联，无结果返回空 | v4.2 落地，已移除物料编码 fallback |
| PR → PO | `po.srcbillnumber in [prBillnos]` + `biztime >= demandStart` 精确关联，无结果返回空 | v4.2 落地，已移除物料编码 fallback |
| 自制件MRP → 工单 | `mps.sourcebillnumber in [selfMadeMrpBillnos]` 精确关联，无结果返回空列表 | v4.2 落地，无降级 |

> **注意**：所有环节均已实现纯精确关联。无结果不代表降级（PR/PO 无结果是正常业务状态"尚未采购"），仅 MRP 精确查询无结果时设置 `isDegraded: true` 以便在 UI 中提示用户执行 ERP MRP 运算。

#### 1.6.4 数据质量评估前置步骤（v3.6 新增）

在第一期开发开始前，需完成各关联字段的数据质量评估：

| 评估项 | 方法 | 可用阈值 |
|-------|------|---------|
| `mrp.rootdemandbillno` 填充率 | 统计非空记录占比 | >= 90% 启用精确关联 |
| `pr.srcbillid` 填充率 | 统计非空且能匹配到 MRP 的记录占比 | >= 90% 启用精确关联 |
| `po.srcbillid` 填充率 | 统计非空且能匹配到 PR 的记录占比 | >= 90% 启用精确关联 |
| `mps.sourcebillnumber` 填充率 | 统计非空记录占比 | >= 80% 启用精确关联 |
| `pr.srcbillid` 关联目标验证 | 抽样 50 条 PR，验证 `srcbillid` 值与 MRP 的 `billno` 还是 `id` 匹配 | 确认关联字段 |

评估结果记录在数据溯源面板的配置中，低于阈值的环节直接使用 Fallback 模式（避免精确关联返回大量空结果）。

### 1.7 BOM 替代料规则（v3.5 新增）

> **重要**：本节定义 BOM 替代物料的识别和分组规则，是甘特图物料筛选、MRP 统计口径、齐套判定等多个模块的基础依据。后续涉及替代料的变更均以本节为准。

#### 1.7.1 核心字段

| 字段 | 含义 | 取值说明 |
|------|------|---------|
| `alt_priority` | 替代优先级 | `0` = 主料（首选物料）；`> 0` = 替代料（数值越大优先级越低） |
| `alt_group_no` | 替代组号 | 标识一组可相互替代的物料，在同一 `parent_material_code` 下唯一 |
| `parent_material_code` | 父级物料编码 | 替代组的作用域，替代关系仅在同一父级物料下成立 |

#### 1.7.2 替代组规则

**替代组定义**：在同一个 `parent_material_code` 下，`alt_group_no` 相同的物料构成一个**替代组**。

**组内角色**：
- `alt_priority = 0` → **主料**（每个替代组有且仅有一个主料）
- `alt_priority > 0` → **替代料**（按 `alt_priority` 升序排列，数值越小优先级越高）

**示例**：

```
parent_material_code = "ASSY-001"（父级组件）

替代组1（alt_group_no = 1）：
  ├─ 物料A (alt_priority=0) → 主料（首选）
  ├─ 物料B (alt_priority=1) → 替代料（第一替代）
  └─ 物料C (alt_priority=2) → 替代料（第二替代）

替代组2（alt_group_no = 2）：
  ├─ 物料D (alt_priority=0) → 主料（首选）
  └─ 物料E (alt_priority=1) → 替代料（第一替代）

非替代物料（alt_group_no 为空）：
  └─ 物料F (alt_priority=0) → 独立主料，无替代关系
```

#### 1.7.3 系统使用规则

| 场景 | 规则 | 说明 |
|------|------|------|
| **BOM API 查询** | `alt_priority == 0` 作为过滤条件 | 仅查询主料，从源头排除替代料 |
| **BOM 树构建** | 仅使用主料构建可达性树 | `buildBOMTreeFromRecords` BFS 遍历只包含 `alt_priority == 0` 的节点 |
| **物料集合口径** | `codes = BOM 可达主料 material_code 去重` | 甘特图、MRP 面板、任务详情三处统一口径 |
| **甘特图展示** | 仅展示主料的倒排时间线 | 替代料不生成 GanttBar |
| **MRP 统计** | 仅统计主料的 netDemand | 替代料的 MRP 记录不纳入缺料计数 |
| **齐套判定** | 基于主料的库存和采购状态 | 替代料的库存/PO 不自动纳入齐套计算（未来可扩展） |
| **齐套状态提示** | 主料缺口时提示替代料信息 | 齐套状态卡片显示"该物料有 N 个替代料可用（库存合计 M）"（v3.6 新增） |

#### 1.7.4 数据异常处理（v3.6 新增）

ERP BOM 数据可能存在不规范的情况，需做容错处理：

| 异常场景 | 处理规则 | 说明 |
|---------|---------|------|
| 同一替代组多个 `alt_priority = 0` | 取 BOM 记录中 `seq_no` 最小的作为主料，其余降级为替代料 | 记录日志供排查 |
| 替代组内无 `alt_priority = 0` 记录 | 取 `alt_priority` 最小的记录作为主料 | 记录日志供排查 |
| `alt_group_no` 有值但 `alt_priority` 为空 | 视为 `alt_priority = 0`（主料） | 兼容 ERP 数据不完整的情况 |

#### 1.7.5 规则变更说明（v3.6 补充）

> **历史说明**：v3.4 及之前版本使用 `alt_part` 字段判定主料/替代料（`alt_part` 为空或 `'0'` = 主料）。v3.5 起改为 `alt_priority` 字段，原因：
> 1. `alt_priority` 是 ERP 标准的替代优先级字段，语义更精确（数值型，`0`=主料，`>0`=替代料按优先级排序）
> 2. `alt_part` 为标记字段（`空/√`），无法区分替代料的优先级顺序
> 3. 代码中 `productSupplyCalculator.ts` 已按 `alt_priority` 实现完整的替代组分组和排序逻辑
>
> **与知识网络的差异**：知识网络 `HD供应链业务知识网络_v3.json` 中 BOM 对象的 comment 仍使用旧规则（"alt_part 为空则为主料"）。经数据验证，`alt_priority == 0` 与 `alt_part 为空` 在当前数据集上判定结果一致。后续需同步更新知识网络 comment 以保持一致。

> **扩展预留**：当前系统仅使用主料进行计划协同。未来版本可引入替代料参与齐套判定（如主料缺货时自动检查替代料库存），届时基于本节替代组规则扩展即可。

---

## 2. 整体页面结构

### 2.1 布局

采用「左侧窄边栏 + 右侧内容区」布局，全宽不限制于 `max-w-6xl`，统一由框架层 `SupplyChainApp` 负责滚动。

```
+----------------------------------------------------------------------+
|  SupplyChainApp (overflow-y-auto 统一滚动层)                          |
+------+---------------------------------------------------------------+
| 侧栏  |                     内容区域                                  |
|(56px)|                                                               |
|sticky|  视图1: 监测任务列表（默认首页）                                 |
|top-0 |  视图2: 新建/编辑任务（三步引导流程）                             |
|h-scr |  视图3: 任务详情（计划概览 + 倒排甘特图 + 物料清单 + 生产工单）   |
|een   |                                                               |
+------+---------------------------------------------------------------+
```

### 2.2 左侧边栏（PlanningTaskSidebar）

固定宽度 **56px**，`sticky top-0 h-screen`，始终显示在视口左侧。

| 元素 | 功能 | 点击行为 |
|------|------|---------|
| 任务列表图标 | 进入监测任务列表 | 切换到视图1 |
| 最近任务（最多3个） | 最近创建/查看的任务缩略 | 切换到该任务详情（视图3） |
| + 新建图标 | 创建新计划协同任务 | 切换到视图2 |

最近任务：显示最近3个任务首字母缩略图标，hover 显示任务名称+状态 tooltip，当前选中任务图标高亮。

### 2.3 视图切换路由

在同一个 `PlanningViewV2` 组件内用 `viewMode` 状态管理，非 URL 路由。

| 触发动作 | 切换到 |
|---------|--------|
| 点击侧栏「列表」 | 视图1：监测任务列表 |
| 点击侧栏「+ 新建」 | 视图2：新建任务流程 |
| 点击侧栏最近任务 | 视图3：该任务详情 |
| 视图1中点击任务卡片 | 视图3：该任务详情 |
| 视图2第3步完成创建 | 视图3：刚创建的任务详情 |
| 视图2/3中点击「<- 返回」 | 视图1 |
| 页面初始加载 | 视图1（默认） |

---

## 3. 视图1：监测任务列表（TaskListView）

### 3.1 功能描述

以卡片网格形式展示所有已创建的计划协同监测任务。支持状态 Tab 筛选、任务名称搜索、结束任务、删除任务。

### 3.2 UI 设计

```
+---------------------------------------------------------------+
|  监测任务列表                                    [+ 新建任务]  |
+---------------------------------------------------------------+
|  全部(3)   进行中(1)   已关闭(2)                                |
|  搜索任务名称...                                                |
|                                                               |
|  +---------------------+  +---------------------+             |
|  | 进行中  02-25        |  | 已结束  x 02-20     |             |
|  | 943-000003 高压开关柜 |  | 942-000005 拖拉机    |             |
|  | 预测 04-01~04-30     |  | 预测 01-01~01-31    |             |
|  | 缺料  6 项           |  | 缺料  4 项          |             |
|  | [查看详情] [结束任务] |  | [查看详情]          |             |
|  +---------------------+  +---------------------+             |
+---------------------------------------------------------------+
```

### 3.3 任务卡片信息

| 字段 | 来源 | 说明 |
|------|------|------|
| 任务名称 | 步骤3用户输入 | 默认为「产品编码-产品名称-YYYYMMDDHHmm」 |
| 状态标签 | 系统计算 | 进行中 / 已结束 / 已过期 |
| 创建时间 | 系统记录 | 卡片右上角显示 MM-DD |
| 产品编码 | 步骤1确认 | `task.productCode` |
| 预测周期 | 步骤1确认 | `demandStart ~ demandEnd` |
| 缺料数量 | 甘特图实时计算 | `flattenGanttBars.filter(b => b.hasShortage).length` |

### 3.4 任务状态定义

| 状态 | 颜色 | 标签文字 | 触发条件 |
|------|------|---------|---------|
| `active` | 绿色 | 进行中 | 任务正常执行中 |
| `completed` | 蓝色 | 已完成 | 用户结束任务，且有产品入库记录 |
| `incomplete` | 橙色 | 未完成 | 用户结束任务，但监测期间无产品入库记录 |
| `expired` | 红色 | 已过期 | 当前时间 > `demandEnd`（自动） |

> **向后兼容**：已存在的 `ended` 状态任务在读取时自动视为 `completed`。

**状态流转**：
```
创建 -> [active] -> 用户结束（有入库） -> [completed]
                 -> 用户结束（无入库） -> [incomplete]
                 -> 自动过期         -> [expired]
```

所有终态（completed、incomplete、expired）均为只读。

### 3.5 列表交互

1. **Tab 筛选**：全部 / 进行中（`active`）/ 已关闭（`completed`、`incomplete` 或 `expired`）
2. **搜索**：实时过滤，按 `task.name` 模糊匹配（不区分大小写）
3. **查看详情**：跳转到视图3
4. **结束任务**（仅进行中）：弹 ConfirmDialog，系统检查产品入库情况后变更为 `completed` 或 `incomplete`（详见第8章）
5. **x 删除**（仅已结束/已过期，卡片右上角）：弹 ConfirmDialog（danger 样式）确认后从 localStorage 永久删除
6. **排序**：按 `createdAt` 倒序

### 3.6 数据持久化

任务列表存储在 `localStorage`，key 为 `planning_v2_tasks`，由 `taskService.ts` 负责 CRUD。

---

## 4. 视图2：新建任务（三步引导流程）

> **v3.1 重大变更**：原四步流程精简为**三步**，移除原步骤2（生产计划确认）。生产工单是物料齐套后的下游动作，不在创建任务时设定。

### 4.1 功能描述

分步引导式设计，将计划协同任务创建拆分为三个步骤。步骤导航条位于顶部，随页面内容自然滚动（非 sticky），不遮挡下方步骤内容。

### 4.2 步骤导航

```
+------+  -->  +------+  -->  +------+
| 1 需求|      | 2 物料|      | 3 计划|
| 预测   |      | 需求   |      |  协同  |
| [活跃] |      |[待进入]|      |[待进入]|
+------+      +------+      +------+
```

| 状态 | 视觉 |
|------|------|
| 活跃 | 蓝色背景 `#0052D9`，白色文字，数字序号 |
| 已完成 | 绿色背景 `#22C55E`，白色勾 |
| 待进入 | 灰色背景 `#F0F0F0`，灰色数字 |

**导航规则**：已完成步骤可点击回退查看/修改；未到达步骤不可点击；修改步骤1会重置23（弹确认对话框）。

---

### 4.3 步骤1：产品需求预测（ProductDemandPanel）

> **v3.0 变更**：
> 1. 预测单按月拆分呈现，支持「产品+月份」维度的预测管理
> 2. 计划截止时间默认取当前月份的下一个月，用户可修改
> 3. 需求数量默认取下月预测数量，而非全部预测之和
>
> **v4.3 变更**：
> 1. 预测单改为**单选**（radio），不再按月分组聚合多条；一次选择一张预测单
> 2. 预测单列表按交货日期（`startdate`）**倒排**，最新的排首位
> 3. 列表**分页**展示（每页 10 条，第 X/Y 页 + 上一页/下一页）
> 4. 默认选中**推荐记录**（下月的第一条），无推荐则选倒排第一条，并自动跳到对应页

#### 4.3.1 功能

产品选择入口。用户从**产品对象**中搜索并选择1个产品；选定后，系统查询该产品在**需求预测对象**中的记录，按交货日期倒排平铺展示，用户**单选一条预测单**后确认需求参数进入下一步。

> **核心定位**：产品需求预测单是整个监测任务的核心对象。选定预测单后，后续所有步骤（MRP 展开、甘特图倒排、PR/PO 跟踪、物料齐套判定、生产工单关联）均以此预测单为起点。

#### 4.3.2 数据来源

**第一步：加载产品列表**

Ontology API 对象 `supplychain_hd0202_product`（产品主数据，数据视图 `HD_产品`）：

```typescript
interface ProductAPI {
  material_number: string;   // 产品编码（主键，mapped: material_code）
  material_name: string;     // 产品名称
}
```

一次性全量加载，作为产品选择列表（带搜索框，支持编码/名称模糊匹配）。

**第二步：选产品后查需求预测**

Ontology API 对象 `supplychain_hd0202_forecast`（需求预测，数据视图 `erp_mds_forecast`）：

```typescript
interface ForecastRecordAPI {
  billno: string;          // 预测单号（主键之一）
  material_number: string; // 物料编码（产品编码，主键之一）
  material_name: string;   // 物料名称（产成品名称）
  startdate: string;       // 预测交货日期（该产品预测需要交货的日期）
  enddate: string;         // 预测终止日期
  qty: number;             // 预测数量（decimal）
  bizdate: string;         // 单据创建时间
  creator_name: string;    // 创建人
  auditdate: string;       // 审核日期（timestamp）
  auditor_name: string;    // 审核人
}
```

查询条件：`material_number == selectedProductCode`，获取该产品所有预测记录（一个产品可对应多条预测单）。

#### 4.3.3 预测单列表呈现（v4.3 重构）

> **v3.0**：按月分组，多选聚合。**v4.3**：平铺单选，倒排分页。

系统将该产品所有预测单按交货日期（`startdate`）**倒排**平铺展示，以表格形式呈现：

```
+------------------------------------------------------------------------+
| 产品: 943-000003 高压开关柜                                              |
| 选择一条预测单（共 23 条，按交货日期倒排）                                  |
+----+------------------+------------+------------+--------+------+
|    | 预测单号          | 交货日期    | 终止日期    | 数量   | 标记 |
+----+------------------+------------+------------+--------+------+
| ○  | MDS-20260415-008 | 2026-05-01 | 2026-05-31 | 500    |      |
| ●  | MDS-20260401-007 | 2026-04-01 | 2026-04-30 | 700    | 推荐 |  <- 默认选中
| ○  | MDS-20260315-006 | 2026-03-15 | 2026-03-31 | 300    |      |
| ○  | MDS-20260301-005 | 2026-03-01 | 2026-03-31 | 400    |      |
...（第 1 / 3 页）
+----+------------------+------------+------------+--------+------+
              [上一页]  第 1 / 3 页  [下一页]
```

**展示规则**：
- 按 `startdate` 倒序排列（最新交货日期排首位）
- `startdate` 在下月范围内的记录加「推荐」徽标
- 每页 10 条，分页控件显示「第 X/Y 页 + 上一页/下一页」，仅总页数 > 1 时显示
- **默认选中**：优先选推荐记录（下月的第一条），无推荐则选倒排第一条，并自动跳到该记录所在页
- 切换页时不重置选中项，所选记录跨页保持

#### 4.3.4 需求字段填充规则（v4.3 更新）

| 字段 | 填充规则 |
|------|---------|
| 需求开始时间 | 直接取选中预测单的 `startdate`（可手动修改） |
| 需求截止时间 | 直接取选中预测单的 `enddate`（可手动修改） |
| 需求数量 | 直接取选中预测单的 `qty`（可手动修改） |
| 关联预测单号 | 固定为单元素数组 `[selectedBillno]`，只读展示 |

> **v4.3 变更**：不再按月份聚合多条记录。选中哪条就用哪条的数据，简单直接，避免跨预测单合并带来的数量和日期偏差。

#### 4.3.5 字段规格

| 字段 | 来源 | 必填 | 可编辑 | 默认值 |
|------|------|------|--------|--------|
| 产品 | product.`material_number` + `material_name` | 是 | 选择 | - |
| 关联预测单 | 用户单选的 forecast 记录（`billno`） | 是 | 单选 | 推荐月份第一条，无则倒排第一条 |
| 需求开始时间 | 选中预测单 `startdate` | 是 | 是 | 自动填充 |
| 需求截止时间 | 选中预测单 `enddate` | 是 | 是 | 自动填充 |
| 需求数量 | 选中预测单 `qty` | 是 | 是 | 自动填充 |

**参考信息（只读展示，不写入任务）**：
- 预测单数量：匹配的 forecast 记录总条数（显示在列表标题）
- 选中后在底部显示关联预测单号（只读 font-mono）

#### 4.3.6 交互流程

1. 激活步骤1时，全量加载 product 列表（带骨架屏 loading）
2. 用户在列表中搜索并选择产品
3. 选中后，系统查询该产品的 forecast 记录（`material_number == selectedCode`）：
   - **有记录**：倒排平铺展示，默认选中推荐或第一条，自动填充时间和数量
   - **无记录**：字段置空，显示提示「该产品暂无需求预测数据，请手动填写」
4. 用户可点选其他预测单（自动更新日期和数量），也可手动修改日期/数量
5. 所有必填字段填写后，点击「确认，进入下一步」进入步骤2

#### 4.3.7 加载时序

```
激活步骤1
  -> 全量加载 product 列表（带缓存，TTL 5min）
  -> 展示产品列表（skeleton loading）

用户选择产品
  -> 按 material_number 查询 forecast（带缓存，TTL 5min）
  -> 按 startdate 倒排
  -> 默认选中推荐记录（下月第一条）或倒排第一条
  -> 自动跳到默认选中记录所在页
  -> 自动填充需求开始/截止时间和数量
  -> 展示平铺预测单列表（分页）
```

---

### 4.4 步骤2：物料需求计划（MaterialRequirementPanel）

> **v3.1 说明**：原步骤3，因移除生产计划步骤，现为步骤2。
>
> **v3.0 重大变更**：MRP 数据源和字段对齐 ERP MRP 计划订单，新增数据过滤和净需求计算逻辑。

#### 4.4.1 功能

展示产品 BOM 展开后的物料 MRP 信息，结合缺口分析和 PR/PO 状态追踪。支持 BOM 层级过滤、仅显示缺口、分页浏览（每页20条）。

#### 4.4.2 数据来源与物料口径

调用 5 个 API：`supplychain_hd0202_mrp`、`supplychain_hd0202_bom`、`supplychain_hd0202_material`、`supplychain_hd0202_pr`、`supplychain_hd0202_po`。

**物料集合定义（主料口径）**：
```
codes = BOM 数据中 alt_priority == 0 的 material_code（去重）
```

> 关键设计决策（v2.6 确立，v3.0 延续）：
> - 物料集合**只取 BOM 主料**，不再 union MRP 中的物料编码。MRP 中存在但 BOM 主料树不可达的物料不纳入步骤2统计。
> - 此口径与甘特图 `buildBOMTreeFromRecords` 完全一致，确保步骤2物料数/缺料数与步骤3、任务详情三处数字一致。

#### 4.4.3 MRP 数据源变更（v3.0）

> **核心变更**：MRP 数据源对齐 ERP `erp_mrp_plan_order`，字段大幅丰富。

**v3.0 MRP 记录结构**：

```typescript
interface MRPPlanOrderAPI {
  billno: string;                   // 需求计划订单单据编号
  materialplanid_number: string;    // 物料编码
  materialplanid_name: string;      // 物料名称
  materialattr_title: string;       // 物料属性（自制/委外/外购）
  adviseorderqty: number;           // 建议订单数量（MRP 理论值）
  bizorderqty: number;              // 订单数量（PMC 修正后的实际需求）
  bizdropqty: number;               // 投放数量（确定性的采购数量）
  advisedroptime: string;           // 建议投放时间
  advisestartdate: string;          // 建议开始时间
  adviseenddate: string;            // 建议结束时间
  startdate: string;                // 计划开始日期
  enddate: string;                  // 计划完成日期
  orderdate: string;                // 计划准备日期
  availabledate: string;            // 可用日期
  closestatus_title: string;        // 关闭状态（A:正常, B:关闭, C:拆分关闭, D:合并关闭, E:投放关闭）
  dropstatus_title: string;         // 投放状态
  dropbilltype_name: string;        // 投放单据类型
  droptime: string;                 // 投放时间
  rootdemandbillno: string;         // 根需求单号（关联预测单号）
  planoperatenum: string;           // 计划运算单号
  createtime: string;               // 创建时间
  creator_name: string;             // 创建人
}
```

**关键字段说明**：
- `adviseorderqty`：MRP 系统计算的理论需求量
- `bizorderqty`：**业务方（PMC）修正后的实际需求量**，优先使用此值
- `bizdropqty`：已确定投放的采购数量
- `rootdemandbillno`：关联到预测单号，实现预测单 -> MRP -> PR -> PO 全链路溯源

#### 4.4.4 MRP 数据过滤规则（v3.0 新增）

> **核心变更**：过滤已关闭的 MRP 计划订单，仅监控实际存在缺口的物料。

```typescript
// 过滤规则（v3.6 改为正向筛选，更健壮）
const activeMRPRecords = mrpRecords.filter(record => {
  // 正向筛选：仅保留"正常"状态的计划订单
  // closestatus_title: A=正常, B=关闭, C=拆分关闭, D=合并关闭, E=投放关闭
  return record.closestatus_title === '正常' || record.closestatus_title === 'A';
  // 注：使用正向筛选而非排除法，避免 ERP 新增状态时遗漏过滤
});
```

**取数优先级**：
1. 优先取 `bizorderqty`（PMC 修正后的数量），若为空或 0
2. 退回取 `adviseorderqty`（MRP 建议数量）

#### 4.4.5 MRP 关联查询策略（v3.4 增强）

> **核心原则**：MRP 通过 `rootdemandbillno` 精确关联到预测单，确保只看到本预测单驱动的物料需求。参见 1.6.2 全链路溯源 fallback 规则。

**查询方式**：

```typescript
// 精确关联（唯一策略）
const mrpRecords = await loadMRP({
  filter: `rootdemandbillno in [${selectedForecastBillnos.join(',')}]`
});

// v4.1 变更：精确关联无结果时直接返回空，不再降级全量加载
// 原因：全量加载会引入其他产品/预测单的无关 MRP 记录，导致数据严重失真
if (mrpRecords.length === 0) {
  // 返回空 + isDegraded=true
  // 前端提示用户：当前预测单暂无 MRP 记录，请先在 ERP 中执行 MRP 运算
}
```

> **v4.1 变更**：移除了全量加载 fallback 策略。此前精确查询无结果时会全量加载整个 MRP 表（~5000 条），经 `filterActiveMRP` 后返回大量无关记录，导致后续 PR/PO 链路查询、甘特图 `hasMRP` 判定和齐套率指标全部失真。现改为直接返回空，MRP 面板显示提示信息。

#### 4.4.6 物料采购状态判定（v4.0 重构）

> **v4.0 关键变更**：移除 MRP 缺口（shortage）判断逻辑。MRP 的净需求量由 ERP MRP 运算产生，本系统不再基于 `bizorderqty`/`adviseorderqty` 做缺口计算。改为基于 **MRP 记录有无 + PO 状态 + 倒排时间** 做采购进度状态判定。

**物料分类：有MRP vs 无MRP**

BOM 中的每个主料，首先按是否有 MRP 记录（全量，含已关闭）分为两大类：

**一、有 MRP 记录的物料**

根据 PO 状态和时间对比，细分为三种采购进度状态：

```typescript
const hasMRP = mrpHasRecord.has(code);
const hasPO = poByMaterial.has(code);
const today = new Date(); today.setHours(0, 0, 0, 0);
// 倒排开始时间 - 标准交期 = 最晚应采购日期
const latestProcureDate = new Date(childStart);
latestProcureDate.setDate(latestProcureDate.getDate() - leadtime);

if (hasMRP) {
  if (hasPO) {
    // 情况1：已下PO
    const poTime = new Date(latestPOBiztime);  // PO 的业务日期
    if (latestProcureDate < poTime) {
      // 情况3：已有PO，但倒排开始-标准交期 < PO业务时间 → 采购偏晚
      mrpStatus = 'abnormal';     // 异常（PO下达时间晚于应采购时间）
    } else {
      mrpStatus = 'normal';       // 正常（已下PO，且时间合理）
    }
  } else {
    // 情况2：未下PO
    if (latestProcureDate < today) {
      mrpStatus = 'abnormal';     // 异常（应开始采购的日期已过，仍无PO）
    } else {
      mrpStatus = 'watch';        // 关注（尚未下PO，但还在合理时间范围内）
    }
  }
}
```

| 状态 | 含义 | 触发条件 | 展示 |
|------|------|---------|------|
| `normal` | 采购正常 | 有MRP + 有PO + PO时间合理 | 绿色标签 |
| `watch` | 需关注 | 有MRP + 无PO + 应采购日期未过 | 黄色标签 |
| `abnormal` | 采购异常 | 有MRP + 无PO + 应采购日过期，或有PO但PO时间晚于应采购日 | 红色标签 |

**二、无 MRP 记录的物料**

无 MRP 记录说明 ERP MRP 运算未对该物料产生计划订单。可能原因：库存已满足需求、MRP 未覆盖此物料、BOM 与 MRP 运算范围不一致。

- 投放状态和投放数量显示 `N/A`
- 不做采购进度状态判定（不标 normal/watch/abnormal）
- **异常判定**：无 MRP 记录 + 可用库存为0或无记录 + `bomLevel > 0` → 视为异常物料（需人工核实）

> **v4.0 移除项**：移除原 `supplyStatus` 三分类（`shortage`/`sufficient`/`sufficient_no_mrp`/`anomaly`）和 `hasShortage`/`shortageQuantity` 的 MRP 缺口计算。甘特图不再做 MRP 缺口判断，改为采购进度状态判定。

**性能考虑**：

若异常/关注物料的详细状态计算影响加载性能，可采用**延迟展开策略**：
- 默认只显示有MRP/无MRP的分类统计
- 用户点击摘要卡片时再展开 normal/watch/abnormal 的详细分类
- 关键监测物料清单同步显示该采购进度状态

#### 4.4.7 UI 设计

```
+---------------------------------------------------------+
|  步骤2 物料需求计划                                        |
|  产品: 943-000003                                        |
+---------------------------------------------------------+
|  MRP状态: [全部/正常/已关闭]  投放: [全部/未投放/已投放]  采购: [全部/无PR无PO/已有PR/已有PO]  [仅异常]  |
|  正常(x) 已关闭(x) 已PR(x) 已PO(x)  共 x / x 条         |
+---+----------+--------+--------+--------+------+------+
|MRP单号|物料编码 |物料名称 |净需求   |投放状态 |PR    |PO    |
+-------+--------+--------+--------+--------+------+------+
|MRP001 |743-003 |组件A    | 1856   |已投放   | -    | -    |  <- 正常
|MRP002 |130-012 |物料B    | 3940   |未投放   |已PR  |未PO  |  <- 正常
|MRP003 |130-921 |物料C    | 5828   |已投放   |已PR  |已PO  |  <- 正常
|MRP004 |130-456 |物料D    | 100    |已投放   |已PR  |已PO  |  <- 已关闭
+-------+--------+--------+--------+--------+------+------+
        [<- 上一步] [第1/10页 (22条)] [确认，进入下一步 ->]
                                        ^ MRP为空时此按钮置灰
```

> **v4.0 变更**：步骤2以 MRP 记录为主表维度（每行=一条MRP记录），显示全部MRP记录（含已关闭），通过 MRP状态 过滤。PR/PO 通过 `srcbillnumber` 精确关联到 MRP 单号。
>
> **v4.2 变更**：新增「投放状态过滤」（全部/未投放/已投放）和「采购状态过滤」（全部/无PR无PO/已有PR/已有PO），前端 `useMemo` 实现。
>
> **v4.3 变更**：MRP 记录数为 0 时「确认，进入下一步」按钮置灰禁用，按钮下方显示提示「请先在 ERP 中执行 MRP 运算」。置灰条件：加载完成且 `rows.length === 0`（不影响加载中状态）。

#### 4.4.8 PR/PO 状态

| 状态 | 图标 | 适用 |
|------|------|------|
| 已PR/已PO | 绿色勾 | 外购/委外，存在对应记录 |
| 未PR/未PO | 红色叉 | 外购/委外，无记录 |
| `-` 横线 | 灰色 | 自制件，不适用 |

PR/PO 状态列 hover 显示详细信息卡片（单号、数量、日期、供应商等）。

#### 4.4.9 分页

每页 20 条，筛选条件变更自动重置到第1页。底部三列布局：`上一步 | 分页控件 | 下一步`。

#### 4.4.10 数据溯源信息板

步骤2面板底部附带**可折叠数据溯源信息板**，默认收缩，点击展开。

| 字段 | 内容 |
|------|------|
| 业务对象 | `supplychain_hd0202_mrp`（并行）+ `supplychain_hd0202_bom`（并行） |
| MRP 查询条件 | `rootdemandbillno in [selectedBillnos]`（精确关联，无结果返回空，v4.1 移除全量 fallback） |
| BOM 查询条件 | `bom_material_code == {productCode}`，取 `bom_version` 字典序最大的最新版本 |
| 物料编码来源 | BOM 主料去重（`alt_priority == 0`，规则详见 1.7），不 union MRP |
| 后续批量查询 | Material: `material_code in [codes]`；PR: 优先 `srcbillid in [mrp.billnos]`（精确），fallback `material_number in [外购/委外物料codes]`，**均叠加 `biztime >= demandStart` 时间过滤**；PO: 优先 `srcbillid in [pr.ids]`（精确），fallback `material_number in [外购/委外物料codes]`，**均叠加 `biztime >= demandStart` 时间过滤**。分片100个/批，受控并行（并发度5） |
| MRP 过滤 | 正向筛选 `closestatus_title` 为「正常」或「A」的记录（v3.6 改为正向筛选） |
| 缓存 | `bom_{productCode}` + 物料/PR/PO 列表哈希，5分钟 TTL |

**溯源面板展示的实时统计**（运行时数据）：

| 指标 | 说明 |
|------|------|
| MRP 记录数（过滤前/后） | 原始记录数 / 过滤后活跃记录数 |
| BOM 全部记录 | `loadBOMByProduct` 返回条数（含所有版本） |
| BOM 最新版本主料数 | 过滤替代料后去重的 `codes.length` |
| 就绪物料（v4.1） | `status === 'ready'` 的物料数（无MRP + 有库存） |
| 缺货物料 | `supplyStatus === 'shortage'` 的物料数（有MRP记录） |
| 异常物料 | `supplyStatus === 'anomaly'` 的物料数（无MRP + 无库存） |
| 已下PO（v4.1） | `status === 'ordered'` 的物料数 |

---

### 4.5 步骤3：智能计划协同（SmartCollaborationPanel）

> **v3.1 说明**：原步骤4，因移除生产计划步骤，现为步骤3。新增生产工单关联展示和物料齐套提醒。

#### 4.5.1 功能

基于前两步确认的数据，展示倒排甘特图预览、物料齐套状态、关联生产工单信息，让用户命名并创建监测任务。

#### 4.5.2 计划协同摘要

```
产品: 943-000003 高压开关柜
预测单: MDS-20260301-001 等 2 单 | 截止 04-30 | 需求 700 套
物料: 173 种 | 缺料: 5 项 | 异常: 2 项
齐套状态: [未齐套] 尚有 5 项物料缺口，2 项物料异常（无MRP且无库存）
```

**物料数 = 甘特图 BOM 树中主料节点总数（不含产品根节点，不含替代料），与步骤2保持一致。**

#### 4.5.3 物料齐套提醒（v3.1 新增）

> **核心新增**：基于客户需求，物料齐套后提醒用户可安排生产。

```
+---------------------------------------------------------------+
| 物料齐套状态                                                    |
+---------------------------------------------------------------+
| 齐套判定: 未齐套                                                |
| 外购/委外物料缺口: 5 项（其中 3 项已下PO）                       |
| 自制件缺口: 2 项                                                |
| ⚠ 异常物料: 2 项（无MRP记录且无库存，请在 ERP 中核实）           |
|                                                                |
| 提示: 以上物料齐套后，可安排生产工单。当前关联预测单已有          |
|       2 个生产工单正在执行（详见下方工单列表）。                  |
+---------------------------------------------------------------+
```

**齐套判定逻辑（v3.7 增强）**：
```typescript
const allMaterials = flattenGanttBars(bars).filter(b => b.bomLevel > 0);
const shortageItems = allMaterials.filter(b => b.supplyStatus === 'shortage');
const anomalyItems = allMaterials.filter(b => b.supplyStatus === 'anomaly');
const isFullyMatched = shortageItems.length === 0 && anomalyItems.length === 0;

// isFullyMatched = true -> 显示"已齐套，可安排生产"
// shortageItems.length > 0 -> 显示"未齐套，尚有 N 项缺口"
// anomalyItems.length > 0 -> 额外显示"⚠ N 项物料异常（无MRP且无库存）"
```

> **v3.7 关键变更**：齐套判定不再仅依赖 MRP 缺口。异常物料（无 MRP 记录且无库存）也阻止齐套判定为"已齐套"，因为这些物料在供应链中没有任何保障。异常物料在齐套状态卡片中以橙色警告单独列出，提示用户在 ERP 中核实原因。

**降级模式下齐套判定（v3.6 新增）**：

当数据链路中任一环节处于 Fallback/降级模式时，齐套判定结果的可信度受限。系统应做特殊处理：

```typescript
if (isDataDegraded) {
  // 降级模式下，齐套判定附加警告
  if (isFullyMatched) {
    // 显示: "已齐套（数据精度受限，建议在 ERP 中确认）"
    matchStatus = 'matched_degraded';
  } else {
    // 显示: "未齐套（数据为兜底模式，缺口数据可能不精准）"
    matchStatus = 'unmatched_degraded';
  }
}
```

降级模式下齐套状态颜色改为**橙色**（而非绿色/红色），提示用户数据精度受限。

**预计齐套日期（v3.3 新增）**：

当未齐套时，基于缺口物料的 PO 交货日预估齐套时间：
```typescript
const estimatedMatchDate = shortageItems
  .filter(b => b.poStatus === 'has_po' && b.poDeliverDate)
  .map(b => b.poDeliverDate)
  .sort()
  .pop();  // 取最晚的 PO 交货日
// 展示: "未齐套，预计 04-15 可齐套（基于PO交货日，粗略估算）"
// 若有缺口物料无PO: "未齐套，尚有 N 项缺口未下PO，无法预估齐套日期"
```

> **精度说明**（v3.6 标注）：预计齐套日期取所有缺口物料最晚的 PO 交货日，为**粗略估算**。未考虑 BOM 层级依赖关系（L2 齐套后才能开始 L1 生产），实际齐套日期可能晚于预估。后续版本可沿倒排甘特图关键路径精确计算。

**齐套倒计时预警（v3.3 新增）**：

距离 `demandEnd` 不足特定天数且仍未齐套时，按紧急程度分梯度预警：

| 距截止日天数 | 预警级别 | 提示 |
|------------|---------|------|
| <= 7 天 | 紧急（红色） | 距需求截止仅 N 天，仍有 M 项缺口！ |
| <= 15 天 | 警告（橙色） | 距需求截止 N 天，仍有 M 项缺口 |
| <= 30 天 | 提醒（黄色） | 距需求截止 N 天，请关注缺口物料进度 |

此预警在任务详情页齐套状态卡片中展示，同时纳入预警横幅汇总。

#### 4.5.4 关联生产工单展示（v3.1 新增）

> **核心定位**：生产工单是物料齐套后的下游动作。在步骤3中**只读展示**关联工单状态，不要求用户在创建任务时确认生产参数。

查询条件（参见 1.6.2 溯源策略，v4.2 变更）：
1. **精确关联（唯一策略）**：`MPS.sourcebillnumber in [selfMadeMrpBillnos]`（自制件 MRP 计划订单单号 → 生产工单来源单据号）
2. ~~产品编码 fallback~~（v4.2 移除）

```
+---------------------------------------------------------------+
| 关联生产工单（只读，基于自制件MRP精确关联）                     |
+---------------------------------------------------------------+
| 工单: 2 (进行中 1 / 未开工 1)  计划生产: 700  已入库: 200 (28.6%)  已过滤 1 条完工工单 |
+-------+------------------+----------+----------+------+--------+--------+-------+-----------+
| 工单号 | 物料             | 计划开工 | 计划完工 | 数量 | 已入库 | 待入库 | 状态   | 领料状态  |
+-------+------------------+----------+----------+------+--------+--------+-------+-----------+
| SCDD- | 1.100 高压开关柜 |2026-03-10|2026-04-10| 500  |  200   |  300   | 开工   | 部分领料  |
| SCDD- | 1.100 高压开关柜 |2026-03-15|2026-04-15| 200  |   0    |  200   | 未开工 | 未领料    |
+-------+------------------+----------+----------+------+--------+--------+-------+-----------+
| 说明: 物料齐套后，业务方在 ERP 中安排生产工单，系统自动关联展示。 |
+---------------------------------------------------------------+
```

**v3.9 变更**：
- **物料列**：显示 `物料编码 + 物料名称`（兜底模式下便于区分不同产品的工单）
- **新增列**：计划开工时间（`planstartdate`）、计划完工时间（`planfinishdate`），截取日期部分
- **过滤完工工单**：`taskstatus_title === '完工'` 或待入库 ≤ 0 的工单不展示，统计栏提示"已过滤 N 条完工工单"

若预测单暂无关联生产工单（或全部已完工），显示提示：「当前尚无匹配相应需求预测单的生产工单」（v4.2 更新）。

**生产工单接口**：

```typescript
interface ProductionWorkOrderAPI {
  id: string;                    // 生产工单主键
  billno: string;                // 生产工单单号
  entry_id: string;              // 生产工单明细主键
  material_number: string;       // 物料编码（产品编码）
  material_name: string;         // 物料名称
  qty: number;                   // 生产数量（decimal）
  xkquainwaqty: number;          // 合格品入库数量（decimal）
  planbegintime: string;         // 计划开工时间（timestamp）
  planendtime: string;           // 计划完工时间（timestamp）
  billdate: string;              // 单据日期（date）
  billstatus: string;            // 单据状态（A:暂存, B:已提交, C:已审核, D:作废）
  taskstatus_title: string;      // 任务状态（A:未开工, B:开工, C:完工, D:部分完工）
  pickstatus_title: string;      // 领料状态（A:未领料, B:部分领料, C:全部领料, D:超额领料）
  sourcebillnumber: string;      // 来源单据编号（关联预测单号）
  sourcebilltype: string;        // 来源单据类型
  srcbillentity: string;         // 来源单据分录号
  huid_scxmh_number: string;     // 生产项目号
  auditdate: string;             // 审核日期（timestamp）
}
```

**工单状态映射**：

| ERP 状态 | 显示标签 | 颜色 |
|---------|---------|------|
| `taskstatus_title = '未开工'` | 未开工 | 灰色 |
| `taskstatus_title = '开工'` | 进行中 | 蓝色 |
| `taskstatus_title = '部分完工'` | 部分完工 | 橙色 |
| `taskstatus_title = '完工'` | 已完工 | 绿色 |
| `billstatus = 'D'` | 已关闭 | 红色 |

#### 4.5.5 任务命名与创建

- 默认任务名：`{product_code}-{product_name}-{YYYYMMDDHHmm}`
- 点击「+ 添加监测任务」：写入 localStorage，跳转到视图3（任务详情）

#### 4.5.6 数据溯源信息板

步骤3面板底部附带**可折叠数据溯源信息板**，与步骤2共用 `DataLineagePanel` 组件，内容切换为甘特图数据查询信息。

---

### 4.6 步骤间联动与重置规则

```
步骤1（产品选择 + 预测单选择）
    |-- product_code + billnos --> 步骤2（MRP）-- 查询 MRP/BOM/物料/PR/PO
    |                                    |
    +-------- product_code + billnos --> 步骤3（协同）-- 甘特图 + 齐套判定 + 生产工单
```

| 修改操作 | 影响范围 | 用户确认 |
|---------|---------|---------|
| 修改步骤1 | 重置23 | ConfirmDialog |
| 修改步骤2 | 无影响 | - |

---

## 5. 倒排甘特图

> **v3.1 说明**：甘特图逻辑不做调整，保持 v2.10 现有实现。以下为完整规格留存。

### 5.1 功能描述

基于 BOM 层级的**齐套模式倒排甘特图**。以**需求预测截止时间**（步骤1确定的 `demandEnd`）为倒排起点，逐层向前推算每个物料「最晚必须到达」的时间窗口。

> **v3.1 变更**：倒排起点从原来的「步骤2生产计划开始时间」改为「步骤1需求预测截止时间」，因为生产计划步骤已移除。

甘特图在两个位置使用，均调用同一个 `ganttService.buildGanttData()`：
- **步骤3预览**：参数来自步骤1的内存状态
- **任务详情页**：参数来自 localStorage Task 对象

### 5.2 数据查询流程

```
输入: productCode + demandEnd（作为倒排锚点）
         |
         v
+- 并行查询 ---------------------------------------------+
| 1. BOM:      bom_material_code == productCode          |
| 2. MRP:      rootdemandbillno in [billnos]             |
|              (无 fallback，精确查询无结果返回空)          |
+--------------------------------------------------------+
         |
         v
+- Round 1 并行（每批100个，并发度5）-----------------------+
| 3. 物料主数据: material_code in [所有物料编码]             |
| 6. 库存: material_code in [所有物料编码]                  |
+----------------------------------------------------------+
         |
         v  用物料属性(materialattr)过滤出外购/委外件
+- Round 2 并行（仅外购/委外件）----------------------------+
| 4. PR: 优先 srcbillid in [mrp.billnos]（精确溯源）       |
|        fallback: material_number in [外购件codes]         |
|        ⚠ 均叠加: biztime >= demandStart（v3.7）          |
| 5. PO: 优先 srcbillid in [pr.ids]（精确溯源）            |
|        fallback: material_number in [外购件codes]         |
|        ⚠ 均叠加: biztime >= demandStart（v3.7）          |
+----------------------------------------------------------+
         |
         v
   ganttService.buildGanttData() -> GanttBuildResult
   (每个 GanttBar 携带 mrpDetails[] 明细，v4.2)

```typescript
// 甘特图服务返回结果（v4.2）
interface GanttBuildResult {
  bars: GanttBar[];                               // 甘特图条形数据（BOM树）
  degradation: DegradationInfo;                   // 各环节降级状态（mrp/pr/po boolean flags）
  inventoryRecords: InventoryRecord[];            // 库存原始数据（透传给buildKeyMaterialList复用，避免重复查询）
  selfMadeMrpBillnos: string[];                   // 自制件MRP单号列表（用于生产工单精确关联）
  selfMadeMrpDroptimeMap: Record<string, string>; // 自制件MRP单号 → 投放时间映射（用于工单追踪显示）
}
```
```

### 5.3 BOM 树构建规则（v3.4 同步代码实现）

**BOM 查询采用两步精确查询**：
1. **Step1 取版本号**：查询 `bom_material_code == productCode`，取 100 条，从结果中获取 `bom_version` 字典序最大值作为最新版本号
2. **Step2 精确查询**：按 `bom_material_code == productCode` + `bom_version == latestVersion` + `alt_priority == 0`（仅主料）三条件查询

**BOM 树构建**：`buildBOMTreeFromRecords` 对 Step2 结果进行 BFS 可达性遍历（从产品根节点沿 `parent_material_code → material_code` 展开），排除替代料残留子级（parent 指向已被过滤的替代料编码的记录）。`ancestors Set` 防止 A→B→C→A 环路，`MAX_NODES=2000` 安全截断。

**物料集合** = BOM 可达主料 `material_code` 的唯一值。

### 5.4 倒排规则（齐套模式）

**L0 产品层**:
```
endDate   = demandEnd（步骤1 需求截止时间）
startDate = endDate - productLeadtime
```

**Ln 子件层（BFS）**:
```
endDate   = parent.startDate - 1天
startDate = endDate - leadtime
```

**leadtime 取值**:
```typescript
const isExternal = mat?.materialattr === '外购' || mat?.materialattr === '委外';
const rawLeadtime = isExternal
  ? parseFloat(mat?.purchase_fixedleadtime || '0')
  : parseFloat(mat?.product_fixedleadtime || '0');
const leadtime = rawLeadtime > 0 ? rawLeadtime : 7;  // 兜底7天
```

> `purchase_fixedleadtime` 和 `product_fixedleadtime` 在 API 中为**字符串类型**（如 `"25.00"`），需 `parseFloat()` 转换。

> **工作日历说明（v3.3 备注）**：当前倒排计算使用自然日（非工作日）。ERP 中的 leadtime 通常基于工作日，自然日与工作日偏差约 30%（如 25 工作日 ≈ 35 自然日）。对于长周期物料（60-90 工作日交期），偏差会导致倒排结果偏乐观。后续版本可引入工作日历换算（最简方案：`实际天数 = ceil(leadtime / 5 * 7)`），当前版本暂按自然日处理。

### 5.5 GanttBar 数据结构（v4.2 更新）

```typescript
/** 单条 MRP 明细（v4.2 新增） */
interface MRPDetail {
  mrpBillno: string;           // MRP 单号
  demandQty: number;           // 需求量（bizorderqty 优先，fallback adviseorderqty）
  dropStatusTitle: string;     // 投放状态（未投放/已投放）
  bizdropqty: number;          // 投放数量
  closestatus: string;         // 关闭状态
  // PR/PO 按 MRP 单号精确关联
  hasPR: boolean;
  hasPO: boolean;
  prCount: number;
  poDeliverDate?: string;      // 该 MRP 对应 PO 的最新交货日
}

interface GanttBar {
  materialCode: string;
  materialName: string;
  bomLevel: number;          // 0=产品, 1=一级子件, 2=二级...
  parentCode: string | null;
  startDate: Date;
  endDate: Date;
  leadtime: number;
  materialType: string;      // 外购/自制/委外
  status: 'on_time' | 'risk' | 'ordered' | 'ready' | 'anomaly';  // v4.1: 五分类
  hasMRP: boolean;           // 是否有MRP记录
  hasShortage: boolean;      // 采购进度异常标记
  shortageQuantity: number;  // 需求量汇总（供甘特图条形渲染）
  supplyStatus: 'shortage' | 'sufficient' | 'sufficient_no_mrp' | 'anomaly';
  mrpStatus?: 'normal' | 'watch' | 'abnormal';  // 采购进度状态（仅有MRP记录时有值）
  poStatus: 'has_po' | 'no_po' | 'not_applicable';
  prStatus: 'has_pr' | 'no_pr' | 'not_applicable';
  poDeliverDate?: string;    // 最新PO交货日
  availableInventoryQty?: number;  // 可用库存
  dropStatusTitle?: string;  // MRP投放状态（汇总，取最新一条）
  bizdropqty?: number;       // MRP投放数量（汇总）
  /** v4.2 新增：该物料关联的全部 MRP 明细记录 */
  mrpDetails: MRPDetail[];
  children: GanttBar[];
}
```

> **v4.1 变更**：`status` 从三值扩展为五值（新增 `ready`、`anomaly`）；新增 `hasMRP` 字段。
>
> **v4.2 变更**：新增 `mrpDetails: MRPDetail[]` 数组，携带该物料关联的每条 MRP 记录明细（MRP单号、需求量、投放状态、投放数量、PR/PO状态）。甘特图维度不变（一个物料一个节点），`shortageQuantity`/`dropStatusTitle`/`bizdropqty` 保留汇总值供条形渲染，`mrpDetails` 用于 tooltip/弹出面板/关键监测物料清单展开行展示。同一物料可能有多条 MRP 记录（PMC 将一张预测单拆解为多条 MRP 计划订单执行）。

### 5.6 进度条状态与颜色（v4.1 重构为五分类）

| 状态 | 颜色 | 色值 | 触发条件 | 优先级 |
|------|------|------|---------|--------|
| `ready` 就绪 | 绿色 | `#16A34A` | 无MRP记录 + 有库存（`supplyStatus === 'sufficient_no_mrp'`） | 1（最高） |
| `anomaly` 异常 | 黄色 | `#EAB308` | 无MRP记录 + 无库存（`supplyStatus === 'anomaly'`） | 2 |
| `ordered` 已下单 | 深绿色 | `#059669` | `hasPO === true` | 3 |
| `risk` 风险 | 红色 | `#DC2626` | `startDate < 今天` 且未下PO，或 `endDate > parent.startDate` | 4 |
| `on_time` 正常 | 蓝色 | `#4F46E5` | 其他情况（有MRP、无风险） | 5（最低） |

> **v4.1 变更**：从三分类（on_time/risk/ordered）扩展为五分类，新增 `ready`（无MRP但有库存，无需采购）和 `anomaly`（无MRP且无库存，需核查）。状态判定按优先级顺序执行，ready/anomaly 优先于 ordered/risk 判定。

**甘特图行背景与左侧标签**：
- 缺口物料（`hasShortage`）：行背景红色 `bg-red-50`，左侧标签 `⚠缺`
- 就绪物料（`status === 'ready'`）：行背景绿色 `bg-green-50/30`，左侧标签 `✓`
- 异常物料（`status === 'anomaly'`）：行背景黄色 `bg-yellow-50/30`，左侧标签 `?`

**无MRP物料的PR/PO显示**：
- 无MRP记录的物料，Tooltip 中 PR/PO 状态显示 `N/A`，不显示具体单号
- 任务条上显示"无MRP"文字标签

**图例（GanttLegend）**：显示全部五种状态色块 + 缺口标记 + 今日线

### 5.7 计划进度总结卡片（GanttSummaryCard）

甘特图**上方**固定渲染一张摘要卡片，呈现倒排结果的关键业务指标，让用户无需查看甘特图细节即可快速判断整体计划健康度。

#### 5.7.1 卡片结构

```
+-------------------------------------------------------------+
| 计划进度总结                                  存在异常物料      |
+-------------------+--------------------+--------------------+
|     计划周期        |    倒排最早开始     |   产品BOM物料数    |
| planStart ~ planEnd | actualEarliestStart| totalMaterials 种  |
|   共 N 天           | 比计划起点早 M 天  |                    |
+-------------------+--------------------+--------------------+
```

三列指标：

| 列 | 字段名 | 计算方式 |
|----|--------|---------|
| 计划周期 | `planStart ~ planEnd` + `planDays` | 步骤1的需求开始/截止时间，共N天 |
| 倒排最早开始 | `actualEarliestStart` | 所有物料（含所有 BOM 层级）中 `startDate` 的最小值；比计划起点早M天 |
| 产品BOM物料 | `totalMaterials` | BOM 可达主料总数（`bomLevel > 0`） |

> **v4.3 说明**：卡片为三列布局（非四列）。实际所需天数合并入「计划周期」列展示，「异常物料」明细通过卡片右上角「存在异常物料」角标 + 可展开区块展示。

#### 5.7.2 异常物料定义（v4.0 重构）

**采购过期物料（pastDueItems）**：满足以下全部条件的物料视为采购过期：
- `bomLevel > 0`（排除产品根节点）
- `materialType` 为外购或委外（采购类物料，自制件不走采购）
- `startDate < 今天`（按计划应已开始采购，但时机已过）
- `poStatus === 'no_po'`（尚未下采购订单）
- `supplyStatus === 'shortage'`（有 MRP 记录且存在净需求缺口）

含义：这类物料有 MRP 采购需求、本应在 `startDate` 那天开始采购，但当前日期已超过该日期且仍未有 PO，代表采购延误，需立即行动。

> **实现说明**：条件使用 `supplyStatus === 'shortage'` 而非 `mrpStatus === 'abnormal'`，确保只对有 MRP 净需求缺口的物料触发采购过期预警。没有 MRP 记录的物料（`sufficient_no_mrp` 或 `anomaly`）不纳入采购过期统计。

**到货超期物料（overdueItems）**：满足以下全部条件的物料视为到货超期：
- `bomLevel > 0`（排除产品根节点）
- `endDate > demandEnd`（按倒排计算，该物料计划到货日晚于需求截止日）

含义：这类物料会导致生产无法按原定计划结束，是产能瓶颈的直接来源。

#### 5.7.3 异常物料明细展开

卡片底部为每类异常提供可展开的明细行（默认折叠）：

**采购过期物料区块**（红色背景行，可展开）：
```
采购过期物料 (2 项) -- 应开始采购的日期已过，且尚未下PO，需立即行动
> 点击展开
```

展开后显示表格：

| 列 | 说明 |
|----|------|
| 物料编码 | `materialCode` |
| 物料名称 | `materialName`，超长截断 |
| 类型 | 外购 / 委外（带颜色标签） |
| 层级 | `L{bomLevel}` |
| 异常原因 | 「应开始采购日已过期 N 天」（N = 今天 - startDate） |
| 计划开始 | `startDate`（YYYY-MM-DD） |
| 计划到货 | `endDate`（YYYY-MM-DD，红色加粗） |
| PR | 已PR / 未PR |
| PO | 已PO / 未PO |

**到货超期物料区块**（橙色背景行，可展开）：
```
到货超期物料 (1 项) -- 计划到货日晚于需求截止日，会影响齐套
> 点击展开
```

表格列与采购过期物料相同，"异常原因"列改为「到货日超出计划截止日」，到货日用橙色加粗显示。

#### 5.7.4 卡片不显示的情况

甘特图数据为空（`bars.length === 0`）时不渲染该卡片。

---

### 5.8 甘特图布局与交互规则

1. **布局**：左侧 BOM 树固定列（240px，`sticky left`）+ 右侧甘特区域（横向可滚动）。两部分共享同一纵向滚动容器，时间轴 `sticky top` 在横向滚动容器内固定。
2. **时间轴范围**：取所有物料（全 BOM 层级）`startDate` 最小值 - 2天，到 `endDate` 最大值 + 2天，完整呈现倒排结果，不做人为截断。
3. **列宽**：每天固定 28px，不使用百分比。时间跨度越长，横向宽度越大，通过横向滚动查看。
4. **今天标记线**：红色竖虚线，贯穿所有任务行，位置按今天距时间轴起点的天数 x 28px 确定。
5. **树形折叠**：默认展开所有层级，顶部提供「全部展开 / 全部折叠」按钮，行前 >/v 切换单节点展开状态。最多渲染 200 行，超出时底部显示提示「已显示 N/M 条」。按物料层级展开，支持手动收缩/展开查看。
6. **任务条 hover**：Tooltip 显示物料编码、名称、类型、开始日、结束日、交期天数、状态、缺口数量、PO交货日、可用库存。
7. **BOM 树列信息**：每行左列显示物料名称（截断）、物料类型标签（外购/委外/自制/产品）、BOM层级（L0~Ln）。缺口物料行背景浅红，左侧显示警告图标。

### 5.9 Markdown 导出（供智能体消费）

`ganttService.exportGanttAsMarkdown(bars, opts)` 导出结构化 Markdown，包含4个章节：

1. 任务基本信息（产品编码、需求周期、需求数量）
2. 全局统计（物料总数、缺口数、风险数、未下PO数）
3. 风险与缺料清单（3.1缺口物料、3.2未下PO、3.3时间风险）
4. 物料倒排甘特表（按 BOM 层级缩进，含状态/交期/缺口标注）

任务详情页「导出 MD」按钮（仅甘特图加载成功时可见），导出文件名：`甘特图_{productCode}_{demandEnd}.md`。

---

## 6. 视图3：任务详情（TaskDetailView）

### 6.1 功能描述

展示已创建监测任务的完整信息：计划概览、实时倒排甘特图、关键监测物料清单、物料齐套状态、关联生产工单追踪。甘特图始终从 API 实时查询，不存快照。

### 6.2 UI 设计

```
+---------------------------------------------------------------+
| <- 返回  943-000003 高压开关柜  进行中  [刷新] [导出] [结束]    |
+---------------------------------------------------------------+
| +- 计划概览 ------------------------------------------------+  |
| | 预测单: MDS-xxx | 需求截止: 04-30 | 需求数量: 700 套       |  |
| | 物料概况: 物料 173 种 / 缺料 5 / 已下PO 168                |  |
| +----------------------------------------------------------+  |
|                                                               |
| +- 物料齐套状态 (v3.1) ------------------------------------+  |
| | 齐套判定: [未齐套] 尚有 5 项物料缺口                       |  |
| | 外购/委外缺口: 3 项（2 项已下PO） | 自制件缺口: 2 项       |  |
| +----------------------------------------------------------+  |
|                                                               |
| +- 倒排甘特图 ----------------------------------------------+  |
| | （实时 API 数据驱动的齐套模式倒排甘特图）                   |  |
| +----------------------------------------------------------+  |
|                                                               |
| +- 关键监测物料清单 -----------------------------------------+  |
| | 物料编码 | 物料名称 | BOM层级 | 物料类型 | 缺口数量 | 交期 |  |
| +----------------------------------------------------------+  |
|                                                               |
| +- 关联生产工单 (v3.1) -------------------------------------+  |
| | 工单列表: 工单号/数量/入库数/工单状态/领料状态              |  |
| | 工单完成率: 已完工 1/3，入库率: 200/700 (28.6%)            |  |
| +----------------------------------------------------------+  |
+---------------------------------------------------------------+
```

### 6.3 计划概览（物料统计）

```typescript
const flat = ganttService.flattenGanttBars(ganttBars);
const materials = flat.filter(b => b.bomLevel > 0);  // 排除产品根节点
stats = {
  totalMaterials: materials.length,                                       // 主料总数
  shortageCount: materials.filter(b => b.supplyStatus === 'shortage').length,   // MRP 缺口物料数
  anomalyCount: materials.filter(b => b.supplyStatus === 'anomaly').length,     // 异常物料数（无MRP且无库存）v3.7
  poCount: materials.filter(b => b.poStatus === 'has_po').length,
};
```

### 6.4 物料齐套状态（v3.1 新增）

> **核心新增**：在任务详情中实时展示物料齐套状态，齐套后提醒用户可安排生产。

```
+---------------------------------------------------------------+
| 物料齐套状态                                                    |
+---------------------------------------------------------------+
|                                                                |
| [已齐套] 所有物料已齐套，可安排生产工单！                        |
|   或                                                           |
| [未齐套] 尚有 5 项物料缺口，预计 04-15 可齐套（基于PO交货日）    |
|   外购/委外缺口: 3 项（其中 2 项已下PO，等待到料）               |
|   自制件缺口: 2 项                                              |
|   ⚠ 距需求截止 22 天，请关注缺口物料进度                        |
|                                                                |
+---------------------------------------------------------------+
```

齐套判定逻辑、预计齐套日期、倒计时预警同步骤3（4.5.3节）。

### 6.5 关联生产工单追踪（v3.1 新增）

> **核心定位**：生产工单是物料齐套后由业务方在 ERP 下达的下游动作。在任务详情中跟踪展示工单执行状态。

#### 6.5.1 数据来源（v4.2 变更）

查询 `supplychain_hd0202_mps`，**仅精确关联**，不再降级（参见 1.6.2）：

**查询链路**：预测单 → MRP（rootdemandbillno 精确关联）→ 筛选自制件 MRP → 生产工单（sourcebillnumber 精确关联）

```typescript
// Step 1: 通过 ganttService.buildGanttData() 得到自制件 MRP 单号列表
// （在 buildGanttData 返回值中：result.selfMadeMrpBillnos）
// selfMadeMrpBillnos = mrpRecords
//   .filter(m => m.materialattr_title === '自制')
//   .map(m => m.billno)

// Step 2: 精确关联生产工单（唯一策略）
const orders = await loadMPSBySelfMadeMrpBillnos(selfMadeMrpBillnos);
// 内部查询: sourcebillnumber in [${selfMadeMrpBillnos.join(',')}]

// v4.2 变更：精确关联无结果时返回空列表，不再降级到 material_number 匹配
// 前端提示："当前尚无匹配相应需求预测单的生产工单"
```

**逻辑说明**：生产工单对应自制件的生产任务，ERP 在下达生产工单时会填入来源 MRP 计划订单单号（`sourcebillnumber = mrp.billno`）。通过此关联可以准确追踪哪些自制件已安排生产。

> **v4.2 变更**：
> 1. 移除产品编码 fallback：此前精确查询无结果时降级到 `material_number == productCode`，可能匹配到同产品但不同批次/月份的生产工单，造成数据混淆。
> 2. 关联字段升级：由 `sourcebillnumber = forecast.billno` 变更为 `sourcebillnumber = mrp.billno`（自制件 MRP 计划订单单号），关联更精确，直接对应具体物料的 MRP 记录。

#### 6.5.2 工单状态面板

**v3.9 变更**：过滤已完工工单、物料列显示编码+名称、新增计划开工/完工时间列。

```
+---------------------------------------------------------------+
| 关联生产工单                                                  |
+---------------------------------------------------------------+
| 工单: 2 (进行中 1 / 未开工 1)  计划生产: 700  已入库: 200 (28.6%)  已过滤 1 条完工工单 |
+-------+------------------+----------+----------+------+--------+--------+-------+-----------+
| 工单号 | 物料             | 计划开工 | 计划完工 | 数量 | 已入库 | 待入库 | 状态   | 领料状态  |
+-------+------------------+----------+----------+------+--------+--------+-------+-----------+
| SCDD- | 1.100 高压开关柜 |2026-03-10|2026-04-10| 500  |  200   |  300   | 开工   | 部分领料  |
| SCDD- | 1.100 高压开关柜 |2026-03-15|2026-04-15| 200  |   0    |  200   | 未开工 | 未领料    |
+-------+------------------+----------+----------+------+--------+--------+-------+-----------+
```

**过滤规则**：`taskstatus_title === '完工'` 或 `qty - stockinqty <= 0` 的工单不展示。统计栏显示"已过滤 N 条完工工单"。

若预测单暂无关联生产工单（或全部已完工），显示提示：「当前尚无匹配相应需求预测单的生产工单」（v4.2 更新）。

#### 6.5.3 工单完成判定逻辑

综合**待入库数量**和**工单状态**判定工单完成（v3.6 增强）：

```typescript
// 待入库数量 = 生产数量 - 合格品入库数量
const pendingInboundQty = order.qty - order.xkquainwaqty;
const isCompleted = pendingInboundQty <= 0 || order.taskstatus_title === '完工';
// 待入库为0 或 ERP标记完工 均视为完成（兼容报废/返工导致无法全部入库的场景）
const isClosed = order.billstatus === 'D';    // 作废视为关闭
```

#### 6.5.4 工单完成与任务关闭联动

- 所有工单 `待入库数量 = 0` 或 `billstatus = 'D'` 时，系统提示用户可结束监测任务
- 预测单手动关闭时，对应监测任务可选择同步终止

### 6.6 关键监测物料清单（KeyMaterialList）

#### 6.6.1 物料范围（v3.2 变更）

展示该产品 BOM 下的**全部物料**，不做任何筛选过滤。即 `ganttService.flattenGanttBars(ganttBars)` 返回的所有 BOM 节点均纳入清单。

> **设计意图**（客户需求反馈）：用户需要看到产品的完整物料全貌，包括已有充足库存的物料，以便全面掌握物料配套状态。缺料/缺口物料通过缺口数量列和行高亮进行区分，无需通过筛选隐藏。

#### 6.6.2 库存数据来源

**API 对象**：`supplychain_hd0202_inventory`（38608 条）

**查询方式**：`material_code in [物料编码列表]`，分批 100 个/批，受控并行（并发度5）。库存数据由 `buildGanttData` 一次性加载并透传给 `buildKeyMaterialList` 复用，避免重复查询。

**可用字段**：

| 字段名 | 显示名 | 类型 | 用途 |
|--------|--------|------|------|
| `material_code` | 物料编码 | string | 匹配键 |
| `inventory_qty` | 库存数量 | decimal | 当前库存 |
| `available_inventory_qty` | 可用库存数量 | decimal | = 库存数量 - 预留库存数量 |
| `inbound_date` | 入库时间 | date | 判断新入库 |
| `warehouse` | 仓库 | string | 仓库过滤使用 |
| `batch_no` | 批号 | string | |

同一物料可能有多条记录（不同批号/仓库），按 `material_code` 汇总。

**有效仓库过滤机制（v4.x 实现，配置化）**：

库存记录按**有效仓库列表**过滤后再汇总 `available_inventory_qty`。有效仓库通过 `navigationConfigService.getValidWarehouses()` 读取，支持运行时配置。

**默认有效仓库**（`navigationConfig.ts` 中 `DEFAULT_PLANNING_WAREHOUSES`）：
- 昆山半成品仓、昆山成品仓、昆山电子原料仓、昆山无人机原料仓、昆山装配原料仓
- 新疆成品仓、哈尔滨成品仓

**过滤规则**：
- `validWarehouses` 为非空集合 → 仅计算仓库名在集合内的库存行之 `available_inventory_qty` 汇总
- `validWarehouses` 为 null（未配置）→ 对所有仓库不过滤，全量汇总
- `inventory_qty`（总库存）不受仓库过滤影响，始终全量汇总（供参考）

> **设计意图**：ERP 库存数据含多个地区/类型仓库。用于齐套判定的"可用库存"应仅统计计划区域内的有效生产用料仓库，避免外地或特殊仓库库存虚增可用量导致误判齐套。

#### 6.6.3 "新入库库存"计算规则

**定义**：入库时间（`inbound_date`）在该任务创建时间之后的库存记录。

**计算方式**：
1. 查询物料在 inventory 中的所有记录
2. 筛选 `inbound_date >= task.createdAt` 的记录
3. 汇总这些记录的 `inventory_qty` 得到新入库库存数量
4. 取这些记录中最新的 `inbound_date` 作为最新入库时间
5. 无符合条件记录时显示 "-"

#### 6.6.4 表格字段（v4.2 增强）

主表（物料维度，一物料一行）：

| 列 | 来源 | 说明 |
|----|------|------|
| 展开按钮 | - | 点击展开/收起该物料的 MRP 明细行（仅 mrpDetails.length > 0 时可点击） |
| 物料 | `materialCode` + `materialName` | 物料编码（等宽字体）+ 名称 |
| 类型 | `materialType` | 带颜色标签：外购=绿色、委外=橙色、自制=紫色、产品=蓝色 |
| 层级 | `bomLevel` | L0=产品，L1/L2... |
| MRP | `mrpDetails.length` + 状态徽标 | 显示该物料关联的 MRP 记录条数和汇总状态，>0 时可展开明细 |
| 需求量 | `shortageQuantity` | MRP 需求量汇总（所有 MRP 记录的 demandQty 之和）；有缺口时蓝色，满足时绿色，无MRP时红色+缺口数 |
| 可用库存 | `availableInventoryQty` | 按有效仓库过滤后的 `available_inventory_qty` 汇总；负数/空时红色，无记录时橙色 |
| 倒排开始 | `startDate` | YYYY-MM-DD |
| 倒排到货 | `endDate` | YYYY-MM-DD |
| 生产推送 | 操作列 | 见下方规则 |

> **说明**：当前版本主表不单独展示 PR/PO/投放状态/PO交货日列（这些信息在 MRP 明细展开行中呈现）。

**MRP 明细展开行**（点击展开后显示，每条 MRP 一行）：

| 列 | 来源 | 说明 |
|----|------|------|
| MRP单号 | `mrpBillno` | |
| 需求量 | `demandQty` | bizorderqty 优先，fallback adviseorderqty |
| 投放状态 | `dropStatusTitle` | 徽标展示 |
| 投放数量 | `bizdropqty` | |
| PR | `hasPR` | 有 PR 显示勾，无则横线 |
| PO | `hasPO` | 有 PO 显示勾，无则横线 |
| PO交期 | `poDeliverDate` | 颜色：已过期=红，1-3天=黄，>3天=绿 |

**v4.1 新增：生产推送操作列**

| 物料类型 | 显示内容 | 说明 |
|----------|----------|------|
| 委外 / 外购 | `N/A`（灰色文本） | 外购和委外物料不涉及内部生产推送 |
| 自制（含产品L0） | 推送按钮（启用/置灰） | 满足 `production_ready` 条件时按钮启用（蓝色），否则置灰 |

`production_ready` 条件（按钮启用）：
- 物料类型为自制（包括 L0 产品，产品也是需要自制生产的）
- 倒排开始日期在 2 天内（`daysUntilStart <= 2`）
- 无缺口（`hasShortage === false`）

> **行状态映射**：`danger` = 外购/委外 + 有MRP + 无PO + 开始日已过期；`warning` = 同上但开始日在 2 天内；`production_ready` = 自制件满足推送条件；`normal` = 其他

#### 6.6.5 搜索、过滤与分页（v4.2 增强）

表格上方增加搜索框和过滤栏（前端过滤，无需额外 API 请求）：

- **搜索**：按物料编码或物料名称模糊匹配
- **BOM 层级过滤**：下拉选择（全部 / L0 产品 / L1 / L2 / L3）
- **物料类型过滤**：下拉选择（全部 / 自制 / 委外 / 外购），v4.1 新增
- **MRP 过滤**：下拉选择（全部 / 有MRP / 无MRP），基于 `hasMRP` 判断
- **MRP 投放状态过滤**：下拉选择（全部 / 未投放 / 已投放），v4.2 新增。基于 `mrpDetails` 中的 `dropStatusTitle` 匹配。物料的任意一条 MRP 明细匹配即显示该物料行，展开后仅显示匹配的明细
- **采购状态过滤**：下拉选择（全部 / 无PR无PO / 已有PR / 已有PO），v4.2 新增。基于物料汇总的 `prStatus` / `poStatus` 判断
- **仅异常**：复选框，仅显示无MRP记录 + 可用库存为0或无记录 + `bomLevel > 0` 的物料
- **统计栏**：右侧显示有MRP数（蓝色）、无MRP数（灰色）、异常数（橙色）、筛选结果数/总数
- **分页**：每页 20 条，底部四按钮翻页控件（首页/上页/下页/末页），超过 20 条时显示
- 搜索或过滤条件变化时自动重置到第 1 页

> **v4.1 变更**：新增「物料类型过滤」（自制/委外/外购），支持按采购属性快速筛选。
>
> **v4.2 变更**：新增「MRP 投放状态过滤」和「采购状态过滤」两组过滤器。过滤逻辑在前端 `useMemo` 中完成，数据量不大无需后端支持。投放状态过滤与主从展开行联动：物料的任意 MRP 明细匹配过滤条件则显示该物料行，展开后仅显示匹配的明细。

#### 6.6.6 CSV 导出

包含所有列，文件名：`关键监测物料清单_{productCode}_{日期}.csv`（UTF-8 BOM 格式，兼容 Excel 中文显示）。

#### 6.6.7 空状态

甘特图数据为空（`ganttBars.length === 0`）时显示「暂无物料数据」提示，不显示表格。

### 6.7 任务操作

- **刷新数据**：重新调用 `ganttService.buildGanttData()` 和生产工单查询
- **导出**：下拉菜单（导出 JSON / 导出 Markdown）
- **结束任务**：仅进行中任务可见，弹 ConfirmDialog（warning 样式）

### 6.8 数据溯源信息板

任务详情页底部附带**可折叠数据溯源信息板**，同 `DataLineagePanel` 组件，`step="task-detail"` 模式，传入运行时 `stats` 和 `task` 数据。

---

## 7. 数据模型

### 7.1 PlanningTask（localStorage 持久化）

Task 对象只存基础查询参数，不存物料快照。甘特图和物料清单始终从 API 实时获取。

```typescript
interface PlanningTask {
  id: string;                    // UUID
  name: string;                  // 任务名称
  status: 'active' | 'completed' | 'incomplete' | 'expired';
  createdAt: string;             // ISO 时间戳
  updatedAt: string;

  // 步骤1 产品需求预测
  productCode: string;
  productName: string;
  demandStart: string;           // YYYY-MM-DD（预测单最早 startdate）
  demandEnd: string;             // YYYY-MM-DD（需求截止时间，甘特图倒排锚点）
  demandQuantity: number;
  relatedForecastBillnos: string[];  // 关联的预测单号列表（v3.1 新增）

  // 任务结束相关（可选，向后兼容）
  endedAt?: string;              // 任务结束时间（ISO 格式）
  summaryReport?: TaskSummaryReport;  // 总结报告（结束时生成并持久化）
}
```

> **v3.1 变更**：
> - 移除 `productionStart`、`productionEnd`、`productionQuantity` 字段（生产计划步骤已移除）
> - 新增 `relatedForecastBillnos` 字段，存储关联的预测单号，用于 MRP 和生产工单关联查询
> - `demandEnd` 取代原 `productionEnd` 作为甘特图倒排锚点和任务过期判定依据

**存储**: `localStorage.setItem('planning_v2_tasks', JSON.stringify(tasks))`

**localStorage 容量策略（v3.3 新增）**：

浏览器 localStorage 容量上限通常为 5-10 MB。随着每日报告（30份/任务）和预警快照的累积，需要主动管理容量：

1. **容量监控**：每次写入前检查 `planningV2_` 前缀下的总占用，通过 `JSON.stringify(localStorage).length` 估算
2. **容量预警**：占用超过 3 MB 时，在页面顶部显示黄色提示「存储空间紧张，建议导出并清理历史任务」
3. **自动清理策略**：占用超过 4 MB 时，自动清理已结束任务（completed/incomplete）超过 90 天的每日报告
4. **Ontology 迁移（第二期）**：将 `monitoring_task` 对象对接后端，彻底解决容量问题

### 7.2 MRPDisplayRow（步骤2展示行）

```typescript
interface MRPDisplayRow {
  materialCode: string;
  materialName: string;
  bomLevel: number;
  materialType: string;
  netDemand: number;            // 正数满足，负数缺口
  adviseOrderQty: number;       // MRP 建议数量（v3.0 新增）
  bizOrderQty: number;          // PMC 修正数量（v3.0 新增）
  dropStatus: string;           // 投放状态（v3.0 新增）
  closeStatus: string;          // 关闭状态（v3.0 新增）
  rootDemandBillno: string;     // 根需求单号（v3.0 新增）
  hasPR: boolean;
  hasPO: boolean;
  prRecords: PRRecord[];
  poRecords: PORecord[];
}
```

---

## 8. 任务结束流程与总结报告

### 8.1 结束流程

> **v3.1 变更**：结合生产工单完成状态和产品入库记录判定，不再以「生产计划结束日」作为参照基准。

用户在任务详情页点击「结束任务」后，系统自动查询生产工单和产品入库记录：

```
用户点击"结束任务"
  |
  v
系统查询关联生产工单
  查询: mps.sourcebillnumber in [selfMadeMrpBillnos]（自制件 MRP 单号列表，来自 buildGanttData）
  |
  +-- 有关联工单 ---------------------+
  |                                    |
  |  场景A: 全部工单完工               |
  |    待入库数量均 = 0               |
  |    -> 状态 -> completed            |
  |                                    |
  |  场景B: 部分工单完工               |
  |    部分待入库 > 0                 |
  |    -> 提示完成率                   |
  |    -> 用户确认后 -> completed      |
  |                                    |
  +------------------------------------+
  |
  +-- 无关联工单 ---------------------+
  |  fallback 查库存                   |
  |  查询: inventory.material_code     |
  |         == task.productCode        |
  |  -> 有入库 -> completed            |
  |  -> 无入库 -> incomplete           |
  +------------------------------------+
  |
  v
展示结束确认对话框（含工单/入库信息摘要）
  |
  v
用户确认 -> 生成总结报告 -> 保存到 task.summaryReport
```

### 8.2 总结报告（TaskSummaryReport）

#### 8.2.1 数据结构

```typescript
interface TaskSummaryReport {
  generatedAt: string;          // 报告生成时间

  // 一、计划 vs 实际对比
  planVsActual: {
    demandPeriod: { start: string; end: string };
    actualInboundDate: string | null;   // 产品最新入库日期
    inboundQuantity: number | null;     // 入库数量
    timeDiffDays: number | null;        // 入库日 vs 需求截止日差异天数
    hasSignificantDelay: boolean;       // 是否超1个月延迟
  };

  // 二、产品完成情况
  productCompletion: {
    plannedQuantity: number;
    inboundQuantity: number | null;
    completionRate: number | null;      // 百分比
  };

  // 三、物料完成统计
  materialCompletion: {
    totalMaterials: number;
    withPO: number;
    withoutPO: number;
    shortageCount: number;
    riskCount: number;
  };

  // 四、生产工单完成情况
  workOrderCompletion: {
    totalOrders: number;
    completedOrders: number;        // 已完工
    inProgressOrders: number;       // 进行中
    notStartedOrders: number;       // 未开工
    closedOrders: number;           // 已关闭/作废
    totalPlannedQty: number;        // 总计划数量
    totalInboundQty: number;        // 总入库数量
    inboundRate: number;            // 入库率
  };

  // 五、关键监测物料快照（结束时冻结）
  keyMaterialsSnapshot: KeyMonitorMaterial[];
}
```

#### 8.2.2 报告展示位置

已结束任务（completed / incomplete）的详情页中，在计划概览下方、甘特图上方，新增**总结报告板块**。

#### 8.2.3 报告生成时机

用户确认结束任务时，系统自动执行：
1. 调用 `ganttService.buildGanttData()` 获取当前甘特图数据
2. 查询关联生产工单状态
3. 查询产品入库记录（inventory API）
4. 查询所有物料库存（inventory API）
5. 组装 `TaskSummaryReport` 对象
6. 写入 `task.summaryReport`，更新 `task.status`、`task.endedAt`、`task.updatedAt`

### 8.3 每日监测报告（v4.1 重构）

> **核心定位**：面向业务领导的每日状态快照，基于倒排甘特图和关键物料监控清单数据，聚焦齐套率、紧急行动项和决策建议。

#### 8.3.1 触发方式

- **手动生成**：任务详情页「每日监测报告」区块中的「生成今日报告」按钮（仅 `active` 状态任务可见）
- **自动生成**：第二期规划，需后端定时服务支持

#### 8.3.2 报告数据结构（v4.1 重构）

> **v4.1 关键变更**：报告结构从七板块（PR/PO下达、物料到料、缺料进度、工单执行、预警异常、趋势指标、预计到料）重构为五板块（总览、紧急行动项、倒排时间线、本周预计到料、决策建议），面向业务领导的决策场景优化。

```typescript
interface DailyReport {
  reportDate: string;         // 报告日期 YYYY-MM-DD
  generatedAt: string;        // 生成时间 ISO
  taskId: string;
  productCode: string;
  productName: string;
  forecastBillnos: string[];  // 关联的需求预测单号（v4.1 新增）

  // 一、总览
  overview: {
    totalMaterials: number;       // BOM 子件去重总数
    readyCount: number;           // 就绪（无MRP + 有库存）
    shortageCount: number;        // 缺货（有MRP记录）
    anomalyCount: number;         // 异常（无MRP + 无库存）
    orderedCount: number;         // 已下PO
    riskCount: number;            // 时间风险
    matchingRate: number;         // 齐套率 = (ready + ordered) / total
    procurementRate: number;      // 采购完成率 = withPO / 外购委外总数
    matchingRateChange: number;   // 较上次报告变化
    procurementRateChange: number;
  };

  // 二、紧急行动项（基于 ShortageList 行状态逻辑）
  actionItems: Array<{
    level: 'danger' | 'warning';
    materialCode: string;
    materialName: string;
    materialType: string;         // 外购/委外
    reason: string;               // 如"采购开始日已过期 27 天，未下PO"
    suggestedAction: string;      // 如"立即下PR并跟进PO"
    startDate: string;
  }>;

  // 三、倒排时间线摘要
  timeline: {
    earliestStart: string;             // 最早需开始采购日期
    daysUntilEarliestStart: number;    // 距今天数（负数=已过期）
    productionReadyCount: number;      // 可推送生产的自制件
    timeRiskCount: number;             // 到货晚于父件开工的物料
  };

  // 四、本周预计到料
  upcomingArrivals: Array<{
    materialCode: string;
    materialName: string;
    expectedDate: string;         // PO deliverdate
  }>;

  // 五、决策建议（自动生成 1-3 条）
  recommendations: string[];
}
```

**行动项（actionItems）生成规则**：
- `danger`：外购/委外 + 有MRP + 无PO + 采购开始日已过期（`daysFromToday(startDate) < 0`）
- `warning`：外购/委外 + 有MRP + 无PO + 采购开始日在 2 天内（`daysFromToday(startDate) < 2`）
- 排序：danger 优先，同级按 startDate 升序

**决策建议（recommendations）生成规则**：
- 有 danger 项 → `[紧急] {物料编码} 等 N 项物料已过期未下PO，建议立即启动采购流程`
- 有 warning 项 → `[关注] N 项物料 2 天内需下PO，请尽快跟进采购进度`
- 有 productionReady → `[就绪] N 项自制件可推送生产，建议安排生产计划`
- 有 anomaly → `[核查] N 项物料无MRP且无库存，建议核实BOM准确性或补充采购计划`
- 均无 → `当前无紧急事项，各物料采购进度正常`

#### 8.3.3 首次报告基准逻辑

首次生成报告时无历史对比基准：
- `overview.*Change` = 0（无变化数据，趋势图标显示为 "-"）

#### 8.3.4 报告展示（v4.1 重构）

任务详情页可折叠区块，header 显示报告日期、预测单号和报告数量：

```
+-----------------------------------------------------------------------+
| 每日监测报告  2026-03-15  预测单: YCD2026...  (1/30)                    |
|                                    [CSV] [MD] [PDF] [生成今日报告]      |
+-----------------------------------------------------------------------+
| 物料概况                行动项          趋势指标              时间线      |
| 总76|就绪57|缺货15|异常4  紧急3|关注0    齐套75%↑|采购0%↑     可生产0|风险3 |
+-----------------------------------------------------------------------+
| ▼ 展开详情                                                             |
+-----------------------------------------------------------------------+
```

展开后显示：
1. **决策建议**（蓝底卡片）：自动生成的 1-3 条建议
2. **紧急行动项表格**：紧急程度、物料编码/名称、类型、问题描述、建议行动
3. **倒排时间线**：最早需开始采购、可推送生产件、时间风险物料（三列卡片）
4. **本周预计到料**：物料编码 → 预计到料日（标签列表）
5. **历史报告数量**

#### 8.3.5 报告存储

- 每个任务最多保留最近 **30 份**每日报告，存储在 localStorage
- 超出 30 份时自动清理最早的报告
- 存储键：`planningV2_dailyReports_{taskId}`
- **v4.1 兼容处理**：加载时过滤掉旧格式报告（缺少 `overview`/`actionItems`/`timeline`/`recommendations` 字段的记录自动丢弃）

#### 8.3.6 报告导出（v4.1 增强）

- **CSV 导出**：总览指标 + 行动项表格，文件名 `监测日报_{产品编码}_{日期}.csv`（UTF-8 BOM）
- **Markdown 导出**：结构化文本（五章节），文件名 `监测日报_{产品编码}_{日期}.md`
- **PDF 导出**（v4.1 新增）：通过打印窗口生成，Markdown → HTML 转换后调用 `window.print()`，适合发送给业务领导

---

## 9. 任务导入导出

### 9.1 导出格式

提供两种格式：

**格式A -- JSON（可恢复导入）**
- 扩展名：`.scb.json`
- 文件名：`{任务名}_{产品编码}_{日期}.scb.json`
- 内容：

```typescript
interface TaskExportPackage {
  version: "2.0";
  exportedAt: string;
  exportedBy: "供应链大脑";
  task: PlanningTask;                    // 完整任务对象（含 summaryReport）
  ganttSnapshot: GanttBar[];             // 甘特图数据快照
  keyMaterials: KeyMonitorMaterial[];    // 关键监测物料快照
  workOrders?: ProductionWorkOrderAPI[]; // 生产工单快照
}
```

**格式B -- Markdown（智能体消费 + 人类阅读）**
- 扩展名：`.md`
- 文件名：`监测任务报告_{产品编码}_{日期}.md`

### 9.2 导出触发位置

任务详情页顶部操作栏，将现有"导出 MD"按钮改为下拉菜单：
- 「导出 JSON（可恢复）」
- 「导出 Markdown（报告）」

### 9.3 导入功能

**入口**：任务列表页顶部，"新建任务"按钮旁增加"导入任务"按钮

**流程**：
1. 用户选择 `.scb.json` 文件
2. 系统校验 `version` 和 `task` 字段完整性
3. 展示导入预览（任务名、产品、时间范围、原始状态）
4. 用户确认
5. 生成新 `id`，保留原始 `createdAt`，更新 `updatedAt` 为当前时间
6. 写入 localStorage

**导入后状态规则**：
- 原 `active` -> 检查 `demandEnd` 是否已过期，过期则设为 `expired`，否则 `active`
- 原 `completed` / `incomplete` -> 保持不变（含总结报告）

---

## 10. 预警机制（v3.2 增强）

### 10.1 预警维度

| 预警类型 | 触发条件 | 严重级别 | 检测数据源 |
|---------|---------|---------|-----------|
| PR/PO 未按截止时间下达 | MRP 计划订单 `advisedroptime` 已过，但 `dropstatus_title` 为未投放 | 高 | MRP + PR/PO |
| PO 交期未反馈 | PO 记录中 `deliverdate` 为空 | 中 | PO |
| PO 交期未更新 | PO `deliverdate` 超过动态阈值未变化（阈值 = `ceil(leadtime * 0.2)`，最小 3 天，最大 14 天） | 中 | PO + Material |
| 物料超期未到料 | PO `deliverdate` 已过，但 inventory 中无对应新入库记录 | 高 | PO + Inventory |
| 重点物料进度异常 | 关键监测物料清单中的缺料物料**连续 3 份每日报告**中缺口数量和 PO 状态均无变化（即缺口未减少且 PO 状态未推进） | 高 | GanttBar + DailyReport |
| 齐套倒计时（v3.3） | 距 `demandEnd` <= 30 天且仍未齐套，按 7/15/30 天分梯度（见 4.5.3） | 动态 | Task + GanttBar |

### 10.2 预警触发方式

**自动预警**：每次打开任务详情页时自动计算，在页面顶部以横幅形式展示异常汇总。

**手动触发**：用户点击「检查预警」按钮，实时查询当前缺料和异常情况，结果同步更新横幅和明细面板。

### 10.3 预警展示（v3.2 增强）

#### 10.3.1 页面横幅

任务详情页顶部横幅，按严重级别分色展示：

```
+---------------------------------------------------------------+
| ⚠ 预警提示  高风险: 3 项  中风险: 2 项         [查看明细] [刷新] |
+---------------------------------------------------------------+
```

- 紧急（深红色）：齐套倒计时 <= 7 天
- 高风险（红色）：PR/PO 未下达、物料超期未到料、重点物料异常
- 中风险（橙色）：PO 交期未反馈、PO 交期未更新、齐套倒计时 8~30 天
- 无异常时横幅显示绿色「当前无异常预警」

#### 10.3.2 预警明细面板

点击「查看明细」展开预警明细，按预警类型分组，每条预警包含：

| 字段 | 说明 |
|------|------|
| 物料编码 | 异常物料编码 |
| 物料名称 | 异常物料名称 |
| 预警类型 | 上述5类之一 |
| 异常原因 | 具体描述（如「应于 03-01 投放，已延迟 6 天」） |
| 截止时间 | 该物料的计划截止时间（`endDate` 或 `advisedroptime`） |
| 当前状态 | PR/PO 状态、库存状态等 |
| 供应商 | PO 关联的供应商名称（外购/委外件） |

```typescript
interface AlertItem {
  materialCode: string;
  materialName: string;
  alertType: 'pr_po_overdue' | 'po_no_delivery_date' | 'po_delivery_stale' | 'material_not_arrived' | 'key_material_no_progress' | 'matching_countdown';
  severity: 'high' | 'medium' | 'urgent';  // urgent 用于齐套倒计时 <= 7 天
  reason: string;           // 人可读的异常原因描述
  deadline: string;         // 截止时间 YYYY-MM-DD
  currentStatus: string;    // 当前状态描述
  supplierName?: string;    // 供应商名称
}
```

#### 10.3.3 预警数据持久化

每次预警检查结果缓存在 `task` 对象中（localStorage），用于：
1. 下次打开时快速展示上次检查结果（标注检查时间）
2. 对比历史预警，判断「进度异常」（连续未改善）

```typescript
interface TaskAlertSnapshot {
  checkedAt: string;        // 检查时间
  alerts: AlertItem[];      // 预警项列表
  summary: { high: number; medium: number };
}
```

### 10.4 外部推送（第二期）

钉钉/邮件自动推送预警为第二期规划，需后端定时服务支持，v3.2 暂不实现。

---

## 11. Ontology API 对象规格

### 11.1 对象类型汇总

| 对象 | API 对象类型 ID | 数据源 | 数据量 | v3.0 变更 |
|------|--------------|--------|--------|----------|
| 产品需求预测单 | `supplychain_hd0202_forecast` | `erp_mds_forecast` | 196条 | 数据量增长（新增月度预测单） |
| 产品 | `supplychain_hd0202_product` | `HD_产品` | - | 不变 |
| 工厂生产计划（生产工单） | `supplychain_hd0202_mps` | `erp_production_work_order` | 7条 | **数据源变更**，字段大幅丰富 |
| 物料需求计划 | `supplychain_hd0202_mrp` | `erp_mrp_plan_order` | 2673条 | **字段丰富**，新增关闭/投放状态 |
| BOM | `supplychain_hd0202_bom` | `erp_material_bom` | 数百条/产品 | 不变 |
| 物料主数据 | `supplychain_hd0202_material` | - | 26,339条 | 不变 |
| 采购申请 | `supplychain_hd0202_pr` | - | 32,306条 | 不变 |
| 采购订单 | `supplychain_hd0202_po` | `erp_purchase_order` | 31,732条 | 不变 |
| 库存 | `supplychain_hd0202_inventory` | `erp_real_time_inventory` | 38,608条 | 不变 |
| 监控任务 | `supplychain_hd0202_monitoring_task` | `monitoring_task` | 1条 | v3.0 新建模型（暂不对接，任务仍用 localStorage） |
| 销售订单 | `supplychain_hd0202_salesorder` | `订单信息_fixed` | 451条 | v3.0 新增 |
| 供应商 | `supplychain_hd0202_supplier` | `erp_supplier` | 3,227条 | 不变 |

### 11.2 关系类型汇总

| 关系 ID | 名称 | 源对象 -> 目标对象 | 映射规则 |
|---------|------|-------------------|---------|
| `d60nsctce73l0mrsstfg` | 生产工单关联自制件MRP | MPS -> MRP | `sourcebillnumber -> mrp.billno`（v4.2：由关联预测单 billno 改为关联自制件 MRP billno） |
| `monitor2mds_forecast` | 监控任务关联需求预测单 | MonitoringTask -> Forecast | `product_code -> material_number` |
| `mrp2material` | 物料需求计划关联物料 | MRP -> Material | `materialplanid_number -> material_code` |
| `mrp2mds_forecast` | 物料需求计划关联产品预测 | MRP -> Forecast | `rootdemandbillno -> billno` |
| `pr2mrp` | 采购申请单关联物料需求计划 | PR -> MRP | `srcbillid -> billno` |
| `product2mds_forecast` | 产品关联需求预测单 | Product -> Forecast | `material_number -> material_number` |
| `supplychain_hd0202_bom2material` | 产品BOM关联物料 | BOM -> Material | `material_code -> material_code` |
| `supplychain_hd0202_material2inventory` | 物料关联库存 | Material -> Inventory | `material_code -> material_code` |
| `supplychain_hd0202_po2supplier` | 采购订单关联供应商 | PO -> Supplier | `supplier_number -> supplier_code` |
| `supplychain_hd0202_pr2po` | 采购订单关联物料请购单 | PO -> PR | `material_number + srcbillid -> material_number + id` |
| `supplychain_hd0202_product2bom` | 产品关联产品BOM | Product -> BOM | `material_number -> bom_material_code` |
| `supplychain_hd0202_product2inventory` | 产品关联库存 | Product -> Inventory | `material_number -> material_code` |
| `supplychain_hd0202_salesorder2product` | 销售订单关联产品 | SalesOrder -> Product | `product_code -> material_number` |

### 11.3 关键数据注意事项

**BOM 多版本处理**：BOM 对象存在多个历史版本（单产品最多 2000+ 条），按 `bom_version` 字典序取最大值作为最新版本，过滤旧版本。

**BOM 替代料**：通过 `alt_priority` 字段识别主料/替代料（`alt_priority == 0` 为主料，`> 0` 为替代料），替代组由 `alt_group_no` 在同一 `parent_material_code` 下划分（完整规则见 1.7 节）。甘特图和 MRP 统计均**只使用主料**。

**Material leadtime 字符串**：`purchase_fixedleadtime` 和 `product_fixedleadtime` 返回字符串（如 `"25.00"`），代码中需 `parseFloat()` 转换，`<= 0` 时兜底7天。

**PO deliverdate 取最新**：同一物料可能有多条 PO，按 `biztime` 降序取第一条的 `deliverdate` 作为甘特图中显示的最新交货日。

**API 查询分片**：物料编码批量查询（Material/PR/PO/Inventory）每批100个（`BATCH_CHUNK_SIZE = 100`），受控并行执行（`CHUNK_CONCURRENCY = 5`）。PR/PO fallback 查询仅传入外购/委外件物料编码，自制件不走采购查询。

**MRP 取数优先级**：优先取 `bizorderqty`（PMC 修正数据），fallback 取 `adviseorderqty`（MRP 建议数据）。

**MRP 过滤规则**：正向筛选 `closestatus_title === '正常'`（或 `=== 'A'`）的记录（v3.6 改为正向筛选，比排除法更健壮，避免 ERP 新增关闭状态时遗漏过滤）。

**MPS 数据源变更**：v3.0 起 `supplychain_hd0202_mps` 的数据源为 `erp_production_work_order`（生产工单），不再是原来的简单 MPS 记录。

**全链路溯源**：预测单 `billno` -> MRP `rootdemandbillno` -> PR `srcbillid` -> PO `srcbillentryid`，实现从需求到采购的完整溯源。生产工单通过 `mps.sourcebillnumber = 自制件MRP.billno` 关联（v4.2 升级：由预测单 billno 改为 MRP 计划订单 billno，关联更精确）。

---

## 12. 文件结构

### 12.1 核心文件

| 文件路径 | 说明 | v3.0 变更 |
|---------|------|----------|
| `src/components/views/PlanningViewV2.tsx` | 主视图：侧栏+三视图布局 | 步骤数从4改为3 |
| `src/components/planningV2/PlanningTaskSidebar.tsx` | 左侧边栏 | 不变 |
| `src/components/planningV2/TaskListView.tsx` | 视图1：监测任务列表 | 不变 |
| `src/components/planningV2/TaskCard.tsx` | 任务卡片组件 | 显示预测周期而非生产周期 |
| `src/components/planningV2/ProductDemandPanel.tsx` | 步骤1：产品需求预测 | 预测单单选+倒排+分页（v4.3） |
| `src/components/planningV2/MaterialRequirementPanel.tsx` | 步骤2（原步骤3）：物料需求计划 | **MRP 数据源和过滤逻辑重构** |
| `src/components/planningV2/SmartCollaborationPanel.tsx` | 步骤3（原步骤4）：计划协同+甘特图预览 | **新增**齐套提醒、生产工单展示 |
| `src/components/planningV2/TaskDetailView.tsx` | 视图3：任务详情 | **新增**齐套状态、生产工单追踪 |
| `src/components/planningV2/WorkOrderTracker.tsx` | 生产工单追踪组件 | **v3.0 新增** |
| `src/components/planningV2/MatchingStatusCard.tsx` | 物料齐套状态卡片 | **v3.1 新增** |
| `src/components/planningV2/ShortageList.tsx` | 关键监测物料清单 | 不变 |
| `src/components/planningV2/AlertBanner.tsx` | 预警横幅组件 | **v3.2 增强**：预警明细面板、分级展示 |
| `src/components/planningV2/AlertDetailPanel.tsx` | 预警明细面板 | **v3.2 新增** |
| `src/components/planningV2/TaskSummaryReport.tsx` | 总结报告展示组件 | 新增工单完成情况 |
| `src/components/planningV2/DailyMonitoringReport.tsx` | 每日监测报告组件 | **v3.2 新增** |
| `src/components/planningV2/ConfirmDialog.tsx` | 通用确认对话框 | 不变 |
| `src/components/planningV2/gantt/GanttChart.tsx` | 甘特图主组件 | 不变 |
| `src/components/planningV2/gantt/GanttTaskBar.tsx` | 甘特图任务条 | 不变 |
| `src/components/planningV2/gantt/GanttTooltip.tsx` | 甘特图 Tooltip | 不变 |
| `src/components/planningV2/gantt/GanttLegend.tsx` | 甘特图图例 | 不变 |
| `src/components/planningV2/PlanningTimelineV2.tsx` | 步骤流程导航条 | 步骤数从4改为3 |
| `src/components/planningV2/DataLineagePanel.tsx` | 数据溯源信息板 | 更新 MRP 查询说明 |
| `src/services/ganttService.ts` | 甘特图倒排算法 | 倒排锚点改为 demandEnd |
| `src/services/taskService.ts` | 监测任务 CRUD（localStorage） | 不变 |
| `src/services/planningV2DataService.ts` | Ontology API 数据加载 | MRP 新字段适配、生产工单查询 |
| `src/types/planningV2.ts` | 全部类型定义 | 新增 MRP/MPS 接口，移除生产计划字段 |

### 12.2 已废弃/删除文件

| 文件路径 | 原因 |
|---------|------|
| `src/components/planningV2/MasterProductionPanel.tsx` | **v3.1 移除**：生产计划步骤已移除，生产工单改为步骤3/详情页只读展示 |
| `src/services/mockDataV2.ts` | 已全面对接真实 Ontology API |
| `src/components/planningV2/SimulationPanel.tsx` | 步骤中不包含模拟功能 |
| `src/services/planningSimulationV2.ts` | 模拟服务不再需要 |
| `src/components/planningV2/PlanningAssistant.tsx` | 不引入 AI 对话面板 |

---

## 13. 设计约束与注意事项

### 13.1 不引入的功能

- 智能体对话式引导 / AI对话面板
- 首页欢迎页
- 前端虚拟工具（ui_show_view 等）
- 物料拆单功能（第二、三版迭代）
- 钉钉/邮件自动推送预警（第二期，需后端服务 + 外部 API）
- 每日监测报告自动定时生成（第二期，需后端定时服务；第一期支持手动生成）
- 任务持久化迁移到 Ontology 服务端（后续规划）

### 13.2 性能考量

- BOM 数据量大（单产品最多 2000+ 条，最新版本约 100~500 条），Ontology API `limit=10000` 一次拉取，前端 BFS 遍历 `MAX_NODES=2000` 截断
- 物料主数据/PR/PO/库存批量查询分片（每批100个），受控并行执行（并发度5），避免串行瓶颈
- 数据加载采用两轮并行策略：Round 1（物料主数据+库存并行）→ Round 2（PR+PO并行，仅查外购/委外件）
- 库存数据由 `buildGanttData` 一次性加载并透传给 `buildKeyMaterialList`，避免重复 API 调用
- API 响应数据缓存5分钟（`planningV2DataService` 内部 Map 缓存 + in-flight 去重）
- Material leadtime 字段为字符串，需 `parseFloat()`
- MRP 数据量约 5092 条（v4.1），精确关联仅返回匹配预测单的子集，不再全量加载
- **性能基准**（948-000077，370物料/771条BOM）：甘特图加载 ~10s，关键物料列表 ~3ms（复用缓存）

### 13.3 数据口径一致性原则

步骤2（MRP 面板）、步骤3（计划协同摘要）、视图3（任务详情物料概况）三处的物料数、缺料数和异常数必须保持一致：

- **物料集合** = `BOM 主料 material_code 去重`（**不** union MRP 中额外的物料编码）
- **主料判定** = `alt_priority == 0`（规则详见 1.7 BOM 替代料规则）
- **物料四分类**（v4.1）= `supplyStatus` 字段，详见 4.4.6：
  - `shortage`：有 MRP 记录且 `netDemand < 0`
  - `sufficient`：有 MRP 记录且无缺口
  - `sufficient_no_mrp`：无 MRP 记录但有库存（甘特图状态 `ready`，绿色）
  - `anomaly`：无 MRP 记录且无库存（甘特图状态 `anomaly`，黄色）
- **甘特图状态五分类**（v4.1）= `GanttBar.status` 字段：`on_time` | `risk` | `ordered` | `ready` | `anomaly`
- **齐套判定** = `shortage` 数为 0 **且** `anomaly` 数为 0
- **齐套率** = `(readyCount + orderedCount) / totalMaterials`（每日监测报告使用此公式）
- **PR/PO 时间过滤**（v3.7）= 所有 PR/PO 查询均叠加 `biztime >= demandStart`
- 甘特图 `buildBOMTreeFromRecords` 和 MRP 面板的替代料过滤、三分类、时间过滤逻辑必须同步维护

### 13.4 滚动架构

- 统一由 `SupplyChainApp` 的 `overflow-y-auto` 容器负责滚动
- `PlanningViewV2` 根元素使用 `min-h-full`，不设固定高度
- 各子视图（TaskListView、TaskDetailView 等）不设 `overflow-y-auto`
- 步骤导航：随页面自然滚动，不 sticky（避免遮挡步骤内容）
- 侧边栏：`sticky top-0 h-screen`

---

## 14. 开发优先级与分期（v3.7 全面更新）

> **基线版本**：v2.10（已上线运行）
> **目标版本**：v3.7（PRD 定义的完整功能集）
> **评估日期**：2026-03-10
> **评估方式**：逐文件代码审查 + PRD 交叉比对

### 14.0 已完成项（v2.10 基线中已实现）

| 功能 | 状态 | 验证依据 |
|------|------|---------|
| BOM 两步精确查询 + BFS 可达性遍历 | ✅ 已完成 | `planningV2DataService.ts:536-543` alt_priority==0 API 过滤 + `ganttService.ts` BFS |
| 物料集合口径统一（BOM 主料去重） | ✅ 已完成 | `ganttService.ts` 使用 BOM 可达物料 |
| 关键监测物料清单展示全部物料 | ✅ 已完成 | `ShortageList.tsx` 展示所有 BOM 节点 |

### 14.1 第一期 Phase A：核心流程重构（P0，阻塞后续所有功能）✅ 已完成

> **目标**：将四步流程重构为三步，建立正确的数据模型基础。此阶段完成前不可开始 Phase B。
> **完成日期**：2026-03-10

| 序号 | 任务 | 涉及文件 | 状态 | 实现要点 | 验收标准 | 评估 |
|------|------|---------|------|---------|---------|------|
| A1 | **PlanningTask 数据模型重构** | `types/planningV2.ts`, `taskService.ts` | ✅ 已完成 | 1) production* 字段标记 deprecated，新增 `relatedForecastBillnos: string[]`；2) taskService 自动迁移旧格式数据（production→demand 映射）；3) 初始化缺失的 relatedForecastBillnos | 旧任务可正常加载；新任务结构符合 7.1 节定义 | S |
| A2 | **步骤1 预测单单选+分页+倒排** | `ProductDemandPanel.tsx` | ✅ 已完成（v4.3 重构） | 1) 移除月份分组/多选聚合逻辑；2) 预测单按 `startdate` 倒排平铺；3) 每页 10 条分页（第 X/Y 页 + 翻页按钮）；4) 默认选推荐（下月）或倒排第一条，自动跳到所在页；5) `relatedForecastBillnos` 固定单元素数组 | 单选 UI 正确；倒排顺序正确；分页翻页正常；默认选中推荐记录 | M |
| A3 | **移除步骤2（生产计划），流程改为三步** | `PlanningViewV2.tsx`, `PlanningTimelineV2.tsx`, `types/planningV2.ts` | ✅ 已完成 | 1) `NewTaskStep` 改为 `1 \| 2 \| 3`；2) 删除 MasterProductionPanel 引用；3) PlanningTimelineV2 STEPS 改为3项（需求预测/物料需求/计划协同）；4) 步骤跳转/重置逻辑简化 | 创建任务仅三步完成；MasterProductionPanel 不再渲染 | M |
| A4 | **甘特图倒排锚点改为 demandEnd** | `ganttService.ts`, `SmartCollaborationPanel.tsx`, `TaskDetailView.tsx` | ✅ 已完成 | 1) `buildGanttData` 接收 `forecastBillnos` 和 `demandStart` 参数；2) L0 endDate = demandEnd；3) 所有调用点更新为 demandStart/demandEnd | 甘特图从 demandEnd 倒排；L0 结束日 = demandEnd | M |
| A5 | **TaskCard 适配三步流程** | `TaskCard.tsx`, `TaskListView.tsx` | ✅ 已完成 | 1) 显示"需求周期"（demandStart~End）；2) TaskListView 导入对话框文案同步更新 | 任务卡片显示需求周期而非生产周期 | S |

**Phase A 验收检查点**：
- [x] 创建新任务走三步流程完成，无报错（TypeScript 编译通过）
- [x] 旧任务（含 production* 字段）可正常加载和查看（taskService 自动迁移）
- [x] 甘特图从 demandEnd 正确倒排
- [x] DataLineagePanel 的步骤描述与三步流程一致（STEP_LABEL 已更新为3项）
- [x] 任务列表页任务卡片显示需求周期

---

### 14.2 第一期 Phase B：数据精度提升（P0+P1，核心数据链路）✅ 已完成

> **目标**：实现全链路精确关联查询和数据过滤，提升数据准确性。依赖 Phase A 完成。
> **完成日期**：2026-03-10

| 序号 | 任务 | 涉及文件 | 状态 | 实现要点 | 验收标准 | 评估 |
|------|------|---------|------|---------|---------|------|
| B1 | **MRP 正向过滤 + 取数优先级** | `planningV2DataService.ts` | ✅ 已完成 | 1) 新增 `MRPPlanOrderAPI` 类型含 `closestatus_title`；2) `filterActiveMRP()` 正向筛选 `closestatus_title in ['正常', 'A']`；3) `getMRPDemandQty()` 优先 `bizorderqty`，fallback `adviseorderqty` | MRP 面板不显示已关闭记录；净需求值正确 | M |
| B2 | **MRP 精确查询（rootdemandbillno）** | `planningV2DataService.ts` | ✅ 已完成 | 1) `loadMRPByBillnos(billnos, productCode)` 按 `rootdemandbillno in [billnos]` 查询；2) 无结果 fallback 到 `finished_product_code` 过滤；3) 返回 `DegradedResult<MRPPlanOrderAPI[]>` | 精确关联有结果时仅返回本预测单 MRP；降级标志正确 | L |
| B3 | **PR 精确关联（srcbillid）+ 时间过滤** | `planningV2DataService.ts` | ✅ 已完成 | 1) `loadPRByMRPBillnos(mrpBillnos, materialCodes, demandStart)` 按 `srcbillid in [mrpBillnos]` + `biztime >= demandStart`；2) 无结果 fallback 到 `material_number in [codes]` + `biztime >= demandStart`；3) 返回降级标志 | 精确关联有结果时只返回本链路 PR；时间过滤排除历史数据 | L |
| B4 | **PO 精确关联（srcbillid）+ 时间过滤** | `planningV2DataService.ts` | ✅ 已完成 | 1) `loadPOByPRBillnos(prBillnos, materialCodes, demandStart)` 按 `srcbillid in [prBillnos]` + `biztime >= demandStart`；2) 无结果 fallback 到 `material_number in [codes]` + `biztime >= demandStart`；3) 返回降级标志 | 精确关联有结果时只返回本链路 PO；时间过滤排除历史数据 | L |
| B5 | **ganttService 对接精确查询链** | `ganttService.ts` | ✅ 已完成 | 1) `buildGanttData` 新增 `forecastBillnos` 和 `demandStart` 参数；2) 级联调用 B2→B3→B4 查询链；3) `GanttBuildResult` 包含 `DegradationInfo`（mrp/pr/po 各环节降级状态） | 甘特图数据来自精确链路查询；降级信息完整 | M |
| B6 | **物料供需三分类** | `ganttService.ts`, `types/planningV2.ts` | ✅ 已完成 | 1) `SupplyStatus` 类型 + GanttBar 新增 `supplyStatus`；2) 有 MRP 且 demand<0 → shortage；3) 无 MRP 有库存 → sufficient_no_mrp；4) 无 MRP 无库存 → anomaly；5) `hasShortage` 兼容保留 | 三种状态正确分类；异常物料不再被误判为"满足" | M |
| B7 | **MPS 精确关联（自制件MRP billno）** | `planningV2DataService.ts`, `ganttService.ts`, `WorkOrderTracker.tsx` | ✅ 已完成（v4.2 升级） | 1) `loadMPSBySelfMadeMrpBillnos(billnos)` 按 `sourcebillnumber in [selfMadeMrpBillnos]` 查询；2) 无结果返回空列表，无 fallback；3) `GanttBuildResult.selfMadeMrpBillnos` 传递自制件 MRP 单号；4) `WorkOrderTracker` 接收 `selfMadeMrpBillnos` | 生产工单仅显示自制件 MRP 精确关联的工单 | M |

**Phase B 验收检查点**：
- [x] MRP 面板不显示已关闭的计划订单（`filterActiveMRP()` 正向筛选）
- [x] 使用含有 `rootdemandbillno` 数据的预测单，MRP 精确关联生效（`loadMRPByBillnos` 实现）
- [x] PR/PO 仅返回 demandStart 之后的记录（`biztime >= demandStart` 条件）
- [x] 物料三分类正确：有缺口→shortage，无MRP有库存→sufficient_no_mrp，无MRP无库存→anomaly
- [x] 数据溯源面板显示各环节当前使用的关联方式（DataLineagePanel 已更新精确/降级说明）

---

### 14.3 第一期 Phase C：业务增强（P1，用户体验和业务功能）✅ 已完成（C6 延后）

> **目标**：基于 Phase A/B 的数据基础，新增齐套判定、工单追踪、预警和报告等业务功能。
> **完成日期**：2026-03-10

| 序号 | 任务 | 涉及文件 | 状态 | 实现要点 | 验收标准 | 评估 |
|------|------|---------|------|---------|---------|------|
| C1 | **步骤3 物料齐套状态展示** | 新建 `MatchingStatusCard.tsx`, `SmartCollaborationPanel.tsx`, `TaskDetailView.tsx` | ✅ 已完成 | 1) 齐套判定：shortage==0 && anomaly==0；2) 预计齐套日期（最晚PO交货日）；3) 齐套倒计时分梯度预警（7/15/30天）；4) matched/matched_degraded/unmatched/unmatched_degraded 四态；5) 异常物料橙色警告 | 齐套/未齐套/待确认三态正确显示；倒计时预警触发 | M |
| C2 | **步骤3/详情页 生产工单关联展示** | 新建 `WorkOrderTracker.tsx`, `SmartCollaborationPanel.tsx`, `TaskDetailView.tsx` | ✅ 已完成 | 1) 调用 `loadMPSByForecastBillnos`；2) 工单状态面板（总/完工/进行中/未开工）+ 入库率；3) 工单完成判定：`pendingInboundQty <= 0 \|\| taskstatus_title === '完工'`；4) 无工单友好提示；5) 降级模式标签 | 工单列表正确展示；完成率计算正确 | M |
| C3 | **预警横幅 + 预警明细面板** | 新建 `AlertBanner.tsx`, `TaskDetailView.tsx` | ✅ 已完成 | 1) 4类前端可计算预警（齐套倒计时/缺口未下PO/超期未到料/异常物料）；2) urgent/high/medium 三级分色展示；3) 可折叠明细表格；4) 无预警时显示绿色"当前无异常" | 预警横幅正确显示；明细面板可展开查看 | L |
| C4 | **降级模式标识外显** | `SmartCollaborationPanel.tsx`, `TaskDetailView.tsx` | ✅ 已完成 | 1) 步骤3/详情页顶部橙色横幅"数据精度：兜底模式 [MRP] [PR] [PO]"；2) MatchingStatusCard 内降级模式下齐套状态变橙色 | 降级模式时有明显橙色标识；用户可感知数据精度 | M |
| C5 | **每日监测报告（手动生成）** | 新建 `DailyMonitoringReport.tsx`, `TaskDetailView.tsx` | ✅ 已完成 | 1) 5大板块（物料概况/缺料进度/趋势指标/预警/预计到料）；2) 齐套率/采购完成率趋势变化；3) 首次报告基准=0；4) CSV/Markdown 导出；5) localStorage 最多30份 | 报告生成正确；导出文件可用；存储容量合理 | L |
| C6 | **替代料库存提示** | `MatchingStatusCard.tsx`, `ganttService.ts` | ⏳ 延后至第二期 | 需额外 BOM 查询（当前仅加载 alt_priority=0 主料），与 P2"替代料参与齐套判定"合并实现 | 替代料数量和库存数据正确 | S |
| C7 | **DataLineagePanel 适配三步流程** | `DataLineagePanel.tsx` | ✅ 已完成（随Phase A实现） | 1) STEP_LABEL 改为3步；2) 更新各步骤数据说明含精确/降级查询方式；3) 移除MPS步骤 | 溯源面板信息与三步流程一致 | S |

**Phase C 验收检查点**：
- [x] 齐套状态卡片在步骤3和任务详情页均正确显示（MatchingStatusCard）
- [x] 生产工单列表正确展示关联工单，完成率准确（WorkOrderTracker）
- [x] 预警横幅在任务详情页正确触发，明细可展开（AlertBanner）
- [x] 降级模式时有明显橙色标识（SmartCollaborationPanel + TaskDetailView）
- [x] 每日报告可生成、查看、导出，历史报告不超过 30 份（DailyMonitoringReport）
- [ ] 替代料库存提示信息准确（延后至第二期，合并替代料齐套判定功能）

---

### 14.4 第一期 Phase D：质量收尾（P1，数据一致性和边界场景）

> **目标**：确保三处物料统计口径一致，处理边界场景和数据异常。

| 序号 | 任务 | 涉及文件 | 实现要点 | 验收标准 | 评估 |
|------|------|---------|---------|---------|------|
| D1 | ✅ **物料统计口径交叉验证** | 全链路 | SmartCollaborationPanel 统计改用 `ganttService.flattenGanttBars()` + `bomLevel > 0` 过滤，与 TaskDetailView 口径完全一致 | 同一任务三处数字完全相同 | M |
| D2 | ✅ **BOM 替代组异常数据容错** | `planningV2DataService.ts` | `alt_priority` null-safe 解析（parseInt + NaN→0），过滤缺少 `material_code` 的记录并打印警告日志 | 异常 BOM 数据不导致崩溃，日志记录 | S |
| D3 | ✅ **API 异常/超时容错** | `ganttService.ts` | 库存 API try/catch + `inventoryUnavailable` 标记，BOM 查询空时抛出友好错误提示用户检查 ERP | API 异常不白屏，有明确用户提示 | M |
| D4 | ✅ **localStorage 容量策略** | `taskService.ts` | `getLocalStorageSizeMB()` 容量检测 + `autoCleanStorage()` 3MB 预警/4MB 清理 + 已结束任务 90 天报告自动清理 | 容量监控和清理机制正常工作 | S |
| D5 | ✅ **任务结束流程适配** | `TaskDetailView.tsx`, `taskService.ts` | Phase A 重构时已同步适配三步数据模型，结束流程正常工作 | 结束任务生成正确的总结报告 | M |
| D6 | ✅ **导入导出兼容性** | `taskService.ts` | `importTask()` 增加 v2.10 格式迁移：`productionEnd→demandEnd`、`productionStart→demandStart`、`productionQuantity→demandQuantity`、初始化空 `relatedForecastBillnos` | 旧格式文件可导入，新格式可正确导出导入 | S |

**Phase D 验收检查点**：
- [x] 三处物料统计口径完全一致：SmartCollaborationPanel 和 TaskDetailView 均使用 `flattenGanttBars + bomLevel > 0` 统一口径
- [x] 模拟 API 超时/异常，系统不白屏：库存 API try/catch 降级 + BOM 空结果友好提示
- [x] localStorage 容量监控：`getLocalStorageSizeMB()` + `autoCleanStorage()` 实现 3MB 预警/4MB 清理/90 天报告清理
- [x] v2.10 导出的 .scb.json 可在 v3.7 中导入：`importTask()` 自动迁移 `production*→demand*` 字段

---

### 14.5 第二期（增强功能）

| 优先级 | 功能 | 说明 |
|-------|------|------|
| P2 | 每日监测报告自动生成 | 需后端定时服务，自动按频次生成 |
| P2 | 钉钉/邮件预警推送 | 自动推送异常信息，需外部 API 集成 |
| P2 | 配套能力计算 | 产品需求量 x 用料量 - 库存 + PO |
| P2 | 预测单状态管理（关闭/删除） | 手动关闭或删除预测单 |
| P2 | 任务持久化迁移到 Ontology 服务端 | localStorage -> monitoring_task |
| P2 | 替代料参与齐套判定 | 主料缺货时自动检查替代料库存 |
| P2 | 工作日历换算 | `ceil(leadtime / 5 * 7)` 替代自然日 |
| P2 | 供应商维度预警聚合 | 同一供应商多物料交期异常 |

### 14.6 第三期（高级功能）

| 优先级 | 功能 | 说明 |
|-------|------|------|
| P3 | 物料拆单功能 | 因料况拆分大需求 |
| P3 | 工单拆单模拟 | 系统支持拆单模拟 |
| P3 | 多月份滚动计划视图 | 按月份维度的计划总览 |
| P3 | 生产计划达成率统计 | 按月统计完成/未完成/关闭工单 |

### 14.7 开发执行规范

**双角色协作模式**：
- **实现角色**：负责编码、自测、提交。每个任务完成后运行完整构建确保无编译错误
- **评审角色**：负责 PRD 合规性审查、边界场景验证、三处口径一致性交叉检查

**每个任务的执行流程**：
1. **实现前**：阅读 PRD 对应章节 + 审查涉及文件现状
2. **实现中**：按 PRD 定义编码，关键逻辑加注释引用 PRD 章节号
3. **自测**：构建通过 + 手动验证核心路径
4. **评审**：对照 PRD 验收标准逐项检查 + 边界场景测试
5. **标记完成**：更新本章任务状态

**Phase 间交接规则**：
- Phase A 全部完成 + 验收检查点通过 → 开始 Phase B
- Phase B 全部完成 + 验收检查点通过 → 开始 Phase C
- Phase C 和 Phase D 可部分并行（D1-D3 依赖 C 完成，D4-D6 可提前开始）

---

## 15. 附录

### 15.1 参考文档

- `docs/Supply_BKN_SKILL.md` -- Ontology 知识网络工具手册
- `docs/Ontology_监控任务_Agent手册.md` -- 监控任务本体建模设计
- `docs/HD供应链业务知识网络_v3.json` -- v3 知识网络模型定义（本版 PRD 基线）
- `docs/archive/2026-01-27-planning-v2-dev-log.md` -- 原型阶段开发实施记录（v1.0 归档）

### 15.2 技术栈

- React + TypeScript（严格模式）
- Tailwind CSS v4
- Lucide React 图标库
- Ontology API（通过 Vite proxy -> dip.aishu.cn）

---

## 修订记录

| 版本 | 日期 | 修订内容 |
|------|------|---------|
| v1.0 | 2026-01-26 | 初版 PRD（基于 mock 数据的四步 Tab 面板原型设计） |
| v1.1~v1.6 | 2026-01-26 | 多轮迭代优化（AI助手、甘特图、风险告警面板等） |
| **v2.0** | **2026-01-27** | 原型核心功能完成（6阶段开发，完成度 88/100） |
| **v2.1** | **2026-02-07** | API 对接设计：基于 HD供应链业务知识网络设计真实数据对接方案 |
| **v2.2** | **2026-02-26** | 真实数据对接 & 架构重构：全面对接真实 Ontology API |
| **v2.3** | **2026-02-26** | UI体验优化：侧边栏重构、ConfirmDialog、分页 |
| **v2.4** | **2026-02-26** | 整页滚动架构重构、甘特图 Markdown 导出 |
| **v2.5** | **2026-03-03** | 物料统计口径统一（Bug修复）；PRD 重构合并 |
| **v2.6** | **2026-03-03** | 数据溯源信息板 + 口径修正 |
| **v2.7** | **2026-03-04** | 计划进度总结卡片 + 甘特图布局调整 |
| **v2.8** | **2026-03-04** | 关键监测物料清单 + 任务结束流程 + 总结报告 + 导入导出 |
| **v2.9** | **2026-03-04** | 步骤1数据源重构（product + forecast 替代 PP） |
| **v2.10** | **2026-03-04** | 关键监测物料清单筛选扩展 + 甘特图库存信息 |
| **v3.0** | **2026-03-07** | 重大重构：基于客户需求调研和 v3 知识网络。MPS 数据源变更为 ERP 生产工单、MRP 数据过滤和取数优先级、预测单按月分组、预警机制、全链路溯源 |
| **v3.1** | **2026-03-07** | **核心流程重构**：1) 明确预测单为核心对象，业务流程为「预测单->MRP配套->PR/PO采购->物料齐套->安排生产」；2) **移除步骤2（生产计划确认）**，流程从四步精简为三步（需求预测->物料需求->计划协同）；3) 生产工单移至步骤3和任务详情页作为**只读关联展示**，通过预测单号（`sourcebillnumber->billno`）自动关联；4) 新增物料齐套状态判定和提醒；5) 甘特图倒排锚点从 `productionStart` 改为 `demandEnd`；6) PlanningTask 数据模型移除 production* 字段，新增 `relatedForecastBillnos`；7) 任务持久化保持 localStorage（Ontology 迁移降至第二期）；8) `MasterProductionPanel.tsx` 标记废弃 |
| **v3.2** | **2026-03-08** | 1) **关键监测物料清单**展示全部 BOM 物料，移除筛选过滤逻辑；2) **预警机制增强**：预警明细面板展示异常物料/原因/截止时间，预警分级（高/中）展示，预警快照持久化；3) **每日监测报告**（手动生成）：覆盖 PR/PO 下达、物料到料、缺料进度、工单执行、预警异常五大板块，表格形式展示，支持 CSV/Markdown 导出；4) 钉钉/邮件推送和报告自动定时生成保留第二期 |
| **v3.3** | **2026-03-08** | **评审修订版**：基于供应链专家评审反馈。1) `netDemand` 明确标注取自 ERP MRP 运算结果（本系统不做二次计算）；2) 齐套判定增加**预计齐套日期**（基于 PO 交货日）和**齐套倒计时分梯度预警**（7/15/30 天）；3) PO 交期未更新阈值从固定 7 天改为**按 leadtime 动态计算**（`ceil(leadtime * 0.2)`，最小 3 天，最大 14 天）；4) 每日报告增加**齐套率/采购完成率趋势指标**、**首次报告基准逻辑**、**未来 7 天预计到料明细**；5) localStorage **容量监控与自动清理策略**；6) 甘特图倒排**工作日历偏差备注**（当前用自然日，后续版本引入工作日换算） |
| **v3.4** | **2026-03-09** | **全链路数据溯源增强**：1) 新增 **1.6 全链路数据溯源体系**：定义完整关联链路（预测单→MRP→PR→PO→库存、预测单→生产工单）、每个环节的精确关联字段和 fallback 规则、降级影响说明、当前实现状态与演进路径；2) MRP 关联查询增加精确/降级双模式伪代码和降级影响说明；3) 甘特图 PR/PO 查询从纯物料编码匹配改为**单据溯源优先**（`srcbillid`），物料编码作为 fallback；4) 生产工单关联查询增加精确/降级双模式和降级标注；5) BOM 查询同步代码实现：**两步精确查询**（Step1 取版本号 → Step2 三条件精确查询）+ **BFS 可达性遍历**（替代 alt_part 过滤）；6) 术语表增加「来源单据ID」定义 |
| **v3.5** | **2026-03-09** | **BOM 替代料规则修正**：1) **纠正主料/替代料判定规则**：从错误的 `alt_part` 字段改为正确的 `alt_priority`（`0`=主料，`>0`=替代料）；2) 新增 **1.7 BOM 替代料规则**专节：定义 `alt_priority`、`alt_group_no`、`parent_material_code` 三个核心字段，明确替代组的作用域和组内角色规则，给出完整示例，列出系统各模块的使用规则；3) 术语表新增「替代组」定义；4) 全文替换所有 `alt_part` 引用为 `alt_priority == 0`（涉及 4.4.2 物料口径、5.2 数据查询流程、11.3 关键数据注意事项、13.3 数据口径一致性原则） |
| **v3.6** | **2026-03-09** | **Fallback 增强与专家评审修订**：基于供应链专家第二次评审反馈。1) **Fallback 触发条件增强**（1.6.2）：区分查询返回空/查询异常/部分匹配三种场景，异常时重试而非降级；2) **级联降级控制**：上游降级时下游标记"受上游降级影响"，溯源面板展示完整链路降级状态；3) **降级标识外显**：步骤标题旁以橙色标签展示降级模式，不再仅限于可折叠面板；4) **新增库存/BOM 查询的 Fallback 策略**：库存 API 异常时齐套判定暂挂，BOM 查询空时提示用户检查 ERP；5) **降级模式齐套判定**（4.5.3）：降级模式下齐套状态改为橙色"待确认"，附加数据精度警告；6) PR→PO 降级影响描述修正为"严重失真"；7) **数据质量评估前置步骤**（1.6.4）：定义关联字段填充率可用阈值和评估方法；8) **BOM 替代组异常处理**（1.7.4）：多主料/无主料/字段缺失的容错规则；9) 替代料规则 `alt_priority` vs `alt_part` **变更说明和知识网络差异标注**（1.7.5）；10) **齐套状态卡片增加替代料库存提示**；11) **预计齐套日期标注为粗略估算**；12) 预警"重点物料进度异常"**明确为连续 3 份每日报告**；13) 工单完成判定**增加 `taskstatus_title === '完工'` 条件**；14) MRP 过滤从排除法**改为正向筛选**（`closestatus_title === '正常'`）；15) `pr.srcbillid` 关联目标待验证标注 |
| **v3.7** | **2026-03-09** | **PR/PO 时间过滤与物料供需三分类**：基于业务逻辑修正。1) **PR/PO 时间范围过滤**（1.6.2、4.4.10、5.2、13.3）：所有 PR/PO 查询均叠加 `biztime >= demandStart` 条件，排除需求预测之前的历史采购数据——采购申请和采购订单是基于需求预测发起的，不可能早于预测开始时间；2) **物料供需三分类**（4.4.6 重构）：BOM 物料不再简单以 MRP netDemand 判定齐套，改为三种状态——`shortage`（有 MRP 且缺口）、`sufficient/sufficient_no_mrp`（有 MRP 无缺口，或无 MRP 但有库存）、`anomaly`（无 MRP 且无库存，异常物料需人工核实）；3) **齐套判定增强**（4.5.3）：异常物料同样阻止齐套判定为"已齐套"，齐套状态卡片增加异常物料橙色警告提示；4) GanttBar 数据结构新增 `supplyStatus` 字段（5.5）；5) 步骤2 UI 增加异常物料行（橙色背景）和"仅异常"筛选按钮（4.4.7）；6) 任务详情统计增加 `anomalyCount`（6.3）；7) 数据口径一致性原则同步更新（13.3） |
| **v3.9** | **2026-03-10** | **关键监测物料清单增强 + 关联生产工单优化**：1) **关键监测物料清单**（`ShortageList.tsx`）：新增分页（每页 20 条，四按钮翻页）、搜索扩展为物料编码+名称模糊匹配、新增 BOM 层级下拉过滤+仅缺口+仅异常复选框、筛选栏统计（缺口/异常/筛选数）；2) **关联生产工单**（`WorkOrderTracker.tsx`）：物料列改为显示物料编码+名称、新增计划开工时间和计划完工时间列、过滤已完工工单（`taskstatus_title === '完工'` 或待入库 ≤ 0）并在统计栏提示已过滤数量；3) PRD 同步更新 4.5.4、6.5.2、6.6.5 三节 |
| **v4.0** | **2026-03-13** | **甘特图MRP逻辑重构 + 关键监测物料清单增强**：1) **移除MRP缺口计算**：甘特图不再基于MRP `bizorderqty`/`adviseorderqty` 做净需求缺口判断（`hasShortage`/`shortageQuantity`/三分类）；2) **新增MRP采购进度状态**（4.4.6 重构）：有MRP记录的物料按PO状态+倒排时间分为 `normal`/`watch`/`abnormal` 三种采购进度状态——已PO且时间合理→正常、未PO但未过期→关注、未PO且过期或PO时间偏晚→异常；3) **MRP投放信息展示**：GanttBar新增 `dropStatusTitle`/`bizdropqty` 字段，基于全量MRP记录（含已关闭）构建投放映射；4) **关键监测物料清单增强**（`ShortageList.tsx`）：新增投放状态/投放数量两列、MRP过滤（全部/有MRP/无MRP）替代原「仅缺口」、异常判定收紧为"无MRP+无库存"；5) **计划进度总结卡片增强**（`GanttSummaryCard.tsx`）：标题栏增加产品编码/名称、计划周期增加预测单号信息；6) **采购过期物料判定修正**：增加 `supplyStatus === 'shortage'` 条件（后续改为 `mrpStatus === 'abnormal'`），库存满足的物料无PO不算过期；7) 步骤2改为MRP记录为主表维度，显示全部MRP（含已关闭） |
| **v4.3** | **2026-03-17** | **步骤①预测单单选+分页+步骤②MRP守门**：1) **预测单改单选**（4.3.3 重构）：移除月份分组/多选/聚合逻辑，改为平铺 radio 单选；按 `startdate` 倒排；每页 10 条分页（第 X/Y 页+翻页按钮）；默认选推荐月份第一条，无推荐则倒排第一条，自动跳到所在页；`relatedForecastBillnos` 固定为单元素数组；2) **步骤②MRP为空置灰下一步**（4.4.7）：加载完成且 MRP 记录数为 0 时「确认，进入下一步」按钮置灰，按钮下方提示「请先在 ERP 中执行 MRP 运算」；通过 `onMrpCountChange` 回调将记录数透传给 `PlanningViewV2` |
| **v4.2** | **2026-03-16** | **MRP明细增强 + 状态过滤 + 工单精确关联**：1) **MRP 按单呈现**（5.5、6.6.4）：`GanttBar` 新增 `mrpDetails: MRPDetail[]` 数组，携带该物料每条 MRP 记录明细（MRP单号、需求量、投放状态、投放数量、PR/PO状态）。甘特图维度不变（BOM物料一行），关键监测物料清单通过主从展开行呈现多条MRP明细。解决PMC拆解预测单为多条MRP时累加失真问题；2) **投放状态+采购状态过滤**（4.4.7、6.6.5）：步骤②和步骤③清单均新增「MRP投放状态」（全部/未投放/已投放）和「采购状态」（全部/无PR无PO/已有PR/已有PO）两组前端过滤器；3) **生产工单移除降级模式**（6.5.1、1.6.2）：`loadMPSByForecastBillnos` 移除 `material_number` fallback 分支，精确查询无结果时返回空列表+提示"当前尚无匹配相应需求预测单的生产工单"；4) **清理诊断日志**：移除 `ganttService.ts` 中的临时诊断代码 |
| **v4.4** | **2026-03-20** | **PRD 与实现对齐更新**：基于代码审查（ganttService.ts / planningV2DataService.ts / ShortageList.tsx / GanttSummaryCard.tsx）修正以下内容：1) **GanttSummaryCard 三列布局**（5.7.1）：修正为三列（计划周期/倒排最早开始/产品BOM物料），非四列；2) **MRP→PR→PO 无 Fallback**（1.6.2 / 1.6.3）：PR/PO 查询已彻底移除物料编码兜底，纯精确关联；PR/PO 无结果不触发降级；3) **有效仓库过滤配置**（6.6.2）：新增仓库过滤机制说明——库存汇总按 `navigationConfigService.getValidWarehouses()` 的有效仓库集过滤，默认7个昆山/新疆/哈尔滨仓库；4) **pastDueItems 判定条件**（5.7.2）：修正为 `supplyStatus === 'shortage'`（非 `mrpStatus === 'abnormal'`）；5) **ShortageList 表格列**（6.6.4）：修正为主表10列（展开按钮/物料/类型/层级/MRP/需求量/可用库存/倒排开始/倒排到货/生产推送）+明细展开行7列（MRP单号/需求量/投放状态/投放数量/PR/PO/PO交期）；6) **GanttBuildResult 接口**（5.2）：补充完整接口定义，含 `selfMadeMrpDroptimeMap` 字段 |
| **v3.8** | **2026-03-10** | **第一期全部完成（Phase A+B+C+D）**：1) **Phase A 全部完成**：三步流程重构（A3）、PlanningTask 数据模型重构含旧数据迁移（A1）、预测单按月分组含默认推荐（A2）、甘特图倒排锚点改为 demandEnd（A4）、TaskCard/TaskListView 适配（A5）、DataLineagePanel 更新为三步说明（C7）；2) **Phase B 全部完成**：MRP 正向过滤 `filterActiveMRP()`（B1）、MRP 精确查询 `loadMRPByBillnos()`（B2）、PR 精确关联 `loadPRByMRPBillnos()`（B3）、PO 精确关联 `loadPOByPRBillnos()`（B4）、ganttService 对接精确查询链含 `GanttBuildResult`+`DegradationInfo`（B5）、物料供需三分类 `SupplyStatus` 类型（B6）、MPS 精确关联 `loadMPSByForecastBillnos()`（B7）；3) **Phase C 完成（C6延后）**：物料齐套状态卡片 `MatchingStatusCard.tsx`（C1，含四态判定/预计齐套日期/倒计时预警/降级处理）、生产工单追踪 `WorkOrderTracker.tsx`（C2，含工单统计/状态面板/降级标签）、预警横幅 `AlertBanner.tsx`（C3，含4类预警/三级分色/可折叠明细）、降级模式橙色标识外显（C4）、每日监测报告 `DailyMonitoringReport.tsx`（C5，含5大板块/趋势指标/CSV+MD导出/localStorage 30份限制）；C6 替代料库存提示延后至第二期合并替代料齐套判定；4) **Phase D 全部完成**：物料统计口径统一为 `flattenGanttBars+bomLevel>0`（D1）、BOM `alt_priority` null-safe 解析和缺字段过滤（D2）、库存 API try/catch 降级+BOM 空结果友好提示（D3）、localStorage 容量监控 `getLocalStorageSizeMB()`+`autoCleanStorage()` 3MB/4MB 阈值+90天清理（D4）、任务结束流程已随 Phase A 适配（D5）、`importTask()` v2.10 格式自动迁移（D6）；5) DIP API 字段兼容映射；6) TypeScript 编译通过 |
