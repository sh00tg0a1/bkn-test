# HD 供应链业务知识网络（BKN）

基于 KWeaver 平台的 HD 供应链业务知识网络定义，覆盖产品需求预测→MRP→采购申请→采购订单→物料齐套→生产计划的完整供应链路。

## 前置安装

需要安装两个 Agent Skill：

```bash
# 安装 KWeaver CLI（需 Node.js 22+）
npm install -g @kweaver-ai/kweaver-sdk

# 安装 Agent Skills
npx skills add https://github.com/kweaver-ai/kweaver-sdk \
  --skill kweaver-core --skill create-bkn
```

## 目录结构

```
ref/                            # 参考资料（只读）
├── 对象类.json                  # 平台导出的对象类定义（含数据视图 ID、字段映射、索引配置）
├── 关系类.json                  # 平台导出的关系类定义（含 mapping_rules）
├── 知识网络文件.json             # 平台导出的知识网络元信息
└── PRD_动态计划协同V2.md         # 用户业务需求文档（动态计划协同 PRD）

bkn/                            # 生成的 BKN 知识网络定义（可直接导入平台）
├── network.bkn                 # 网络根定义
├── object_types/               # 12 个对象类型
├── relation_types/             # 13 个关系类型
├── concept_groups/             # 概念分组
└── SKILL.md                    # Agent 说明 & 跨对象业务规则

scripts/                        # 辅助脚本
```

## 数据来源

`ref/` 中的 JSON 文件是从 KWeaver 平台导出的**现有知识网络描述**，包含真实的数据视图 ID、向量模型 ID 和字段映射关系。`PRD_动态计划协同V2.md` 描述动态计划协同场景下的业务规则、查询与统计口径、数据流转与实现约定。

## 目标

使用 `create-bkn` 工具，以 `ref/` 中的平台导出数据为基础，结合 PRD 业务需求，优化并生成结构化的 BKN 知识网络定义。优化内容包括：补充业务规则、完善字段描述、明确关联关系的语义；**与 PRD 不一致时**，在属性/对象/关系描述或 `SKILL.md` 中写清产品口径，并保持 `data_source.id`、关系 mapping 与平台导出一致以便导入。

## 规则绑定原则

业务规则按作用范围分层放置，确保每条规则都绑定在最合适的位置：

1. **属性级规则** → 对应 `object_types/*.bkn` 属性表的 Description 列
2. **单对象/单关系规则** → 对应 `.bkn` 文件的「### 业务规则」节
3. **跨对象规则** → `bkn/SKILL.md`「跨对象业务规则（全文）」（10 条规则）
4. **无法绑定到具体数据对象的规则** → `bkn/network.bkn`（数据口径一致性、API 查询策略等）

详见 `bkn/network.bkn`「规则绑定原则」。

## 导入即用

`bkn/` 中所有对象类型的数据视图 ID（`data_source.id`）和向量模型 ID（`model_id`）均与平台现有资源保持一致，导入后无需重新绑定数据源，可直接使用。

```bash
# 认证
kweaver auth login <platform-url>

# 推送知识网络
kweaver bkn push bkn/
```

## 提示词参考

### BKN 构建 Agent

以下提示词总结了本项目的完整工作流，可用于复现或在新项目中使用：

> 你是一个供应链业务知识网络的构建助手。请使用 `@create-bkn` 和 `@kweaver-core` 两个 skill。
>
> **输入材料在 `ref/` 目录：**
> - `对象类.json`、`关系类.json`、`知识网络文件.json` — 从 KWeaver 平台导出的现有知识网络定义，包含真实的数据视图 ID、字段映射和索引配置
> - `PRD_动态计划协同V2.md` — 用户的业务需求文档（动态计划协同：查询策略、过滤、齐套、预警、甘特口径等）
>
> **请完成以下工作：**
> 1. 读取 `ref/` 中的 JSON 导出文件，理解现有知识网络的对象类、关系类结构及其数据源绑定
> 2. 精读 **PRD**，将需求落到合适位置：**仅与某属性相关的逻辑** 写入该属性在 `object_types/*.bkn` 表格中的 **Description**；**对象或关系整体语义** 写入对应对象类/关系类正文与 **「### 业务规则」**；**跨对象的全局口径与链路** 写入 **`network.bkn`**（网络级说明）与 **`bkn/SKILL.md`「跨对象业务规则」**（长文规则）
> 3. 使用 `create-bkn` 规范，在 `bkn/` 目录下生成完整的 BKN 定义（`network.bkn`、`object_types/`、`relation_types/`、`concept_groups/`）
> 4. 确保所有对象类的 `data_source.id`（数据视图 ID）与 `ref/` 中平台导出值一致，不使用占位符
> 5. 完成后使用 `kweaver bkn push bkn/` 推送到平台
>
> **关键约束：** 生成的 BKN 须导入即用 — 数据视图 ID、向量模型 ID 与平台现有资源保持一致；业务解释以 **PRD** 与各 `.bkn` / `SKILL.md` 描述补全。

### 需求复核 Agent

以下提示词用于在 BKN 构建完成后进行需求覆盖度审查，确保 PRD 中的每条业务规则都已绑定到合适的位置：

> 你是一个供应链业务知识网络的**需求复核 Agent**。你的任务是逐条审查 `ref/PRD_动态计划协同V2.md` 中的所有业务规则，验证它们是否被 `bkn/` 中的 BKN 文件覆盖。
>
> **审查步骤：**
> 1. **提取规则清单**：精读 PRD 全文，逐节提取所有离散的业务规则、数据约束和处理逻辑，按以下分类整理为编号清单：
>    - 数据过滤条件（如 MRP 有效行过滤、工单完工过滤）
>    - 字段语义与取值优先级（如 bizorderqty vs adviseorderqty）
>    - 关联/溯源策略（如 rootdemandbillno → billno）
>    - 计算公式（如齐套率、采购完成率、倒排日期）
>    - 状态定义与映射（如 task_status 四态、supplyStatus 四分类）
>    - 预警触发与关闭条件
>    - 全局约束（如口径一致性、数据质量阈值）
>    跳过纯 UI 布局规则（按钮位置、颜色主题），但保留编码业务状态的 UI 规则（如状态→颜色映射）。
>
> 2. **逐条比对**：将清单中每条规则与 BKN 文件交叉比对，检查四个层级：
>    - `object_types/*.bkn` 属性表 Description 列（属性级规则）
>    - `object_types/*.bkn` 和 `relation_types/*.bkn` 的「### 业务规则」节（对象/关系级规则）
>    - `bkn/SKILL.md`「跨对象业务规则」（跨对象规则）
>    - `bkn/network.bkn`「全局规则」（无法绑定到单一对象的规则）
>
> 3. **输出报告**：生成覆盖度报告，包含：
>    - ✅ 已覆盖规则：规则 ID + 所在文件与位置
>    - ❌ 未覆盖规则：规则 ID + 建议写入位置（属性描述 / 业务规则节 / SKILL.md / network.bkn）
>    - ⚠️ 部分覆盖：规则 ID + 缺失部分说明
>
> 4. **修复缺口**：对所有未覆盖和部分覆盖的规则，按「规则绑定原则」写入对应的 BKN 文件：
>    - 仅与某属性相关 → 属性 Description
>    - 对象/关系整体语义 → 该 `.bkn` 的「### 业务规则」
>    - 跨对象规则 → `SKILL.md`
>    - 无法绑定 → `network.bkn`「全局规则」
>
> **关键原则：** 规则必须和数据绑定。每条规则应绑定到它涉及的最具体的数据字段或对象上，只有确实无法绑定时才放到 `network.bkn`。

### BKN 效果评估 Agent

> 请使用 /kweaver-core 进行准确率测试，业务知识网络id是supplychain_hd0202_bkn_optimized。请仔细阅读
> @test-cases/00_基准数据基准.md @test-cases/00_评分标准与测试方法.md 
> 业务知识网络的情况是@bkn 
> 下面你要做的是：
> 1. 完成对 @test-cases/questions 中一个个问题的回答，记得要串行，不要并行
> 2. 完成测试报告，所有结果输出在 @test_report/supplychain_hd0202_bkn_optimized_new_method
> 3. 不需要参考其他的 test_report 中的文件
