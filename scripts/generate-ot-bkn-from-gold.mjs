/**
 * Generate object_types/*.bkn from the bundled full KN export under ref/.
 * Run: node scripts/generate-ot-bkn-from-gold.mjs
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const knExportPath = join(root, 'ref', 'HD供应链业务知识网络_v3.json');
const gold = JSON.parse(readFileSync(knExportPath, 'utf8'));

const idToFile = {
  supplychain_hd0202_bom: 'bom.bkn',
  supplychain_hd0202_forecast: 'forecast.bkn',
  supplychain_hd0202_inventory: 'inventory.bkn',
  supplychain_hd0202_material: 'material.bkn',
  supplychain_hd0202_monitoring_task: 'monitoring_task.bkn',
  supplychain_hd0202_mps: 'mps.bkn',
  supplychain_hd0202_mrp: 'mrp.bkn',
  supplychain_hd0202_po: 'po.bkn',
  supplychain_hd0202_pr: 'pr.bkn',
  supplychain_hd0202_product: 'product.bkn',
  supplychain_hd0202_salesorder: 'salesorder.bkn',
  supplychain_hd0202_supplier: 'supplier.bkn',
};

function esc(s) {
  if (s == null) return '';
  return String(s).replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
}

function yamlTags(tags) {
  if (!tags?.length) return 'tags: []';
  return 'tags:\n' + tags.map((t) => `  - ${t}`).join('\n');
}

function typeMap(t) {
  const m = { text: 'text', timestamp: 'timestamp', date: 'date', datetime: 'datetime', json: 'json', integer: 'integer', float: 'float', decimal: 'decimal' };
  return m[t] || t || 'string';
}

/** Short intro per OT — PRD-aligned one-liners; expanded rules stay in ### 业务规则 */
const intros = {
  supplychain_hd0202_bom:
    '产品物料清单（BOM），描述成品/半成品由哪些物料组成、用量与替代组。是 MRP 展开与齐套分析的基础数据。',
  supplychain_hd0202_forecast:
    '产品需求预测单：计划协同的**核心驱动对象**（PRD §1.2）。业务方基于销售与市场预判形成“产品+时间窗”的需求输入，向上游驱动 MRP→PR/PO→齐套→生产工单。',
  supplychain_hd0202_inventory:
    '实时库存视图。齐套与倒排中用于判断可用量；`available_inventory_qty` 口径见属性说明（PRD §6.6）。',
  supplychain_hd0202_material:
    '物料主数据：属性（自制/外购/委外）、提前期等，决定 MRP 投放路径与倒排 lead time（PRD §5.4）。',
  supplychain_hd0202_monitoring_task:
    '监测任务：围绕所选预测单/产品持续跟踪物料与执行状态；任务级状态与 UI 逻辑见 PRD §3、§8（非 ERP 单据）。',
  supplychain_hd0202_mps:
    '工厂生产工单（ERP）。物料齐套后的下游执行单据；与自制件 MRP 的溯源关系见 PRD §1.6、v4.2（`sourcebillnumber`）。',
  supplychain_hd0202_mrp:
    'MRP 计划订单：连接预测与采购执行。有效记录过滤、数量优先级与根需求溯源字段见属性说明（PRD §4.4）。',
  supplychain_hd0202_po:
    '采购订单：PR 下推形成，记录供应商、数量、交期与入库执行；与 PR 的精确关联字段见属性说明（PRD §1.6）。',
  supplychain_hd0202_pr:
    '采购申请：由 MRP 投放生成，是计划域到执行域的桥梁；`srcbillid` 等溯源字段见属性说明（PRD §1.6）。',
  supplychain_hd0202_product:
    '成品/产品主数据。产品编码即成品物料编码，用于关联预测单、BOM 与库存。',
  supplychain_hd0202_salesorder:
    '销售订单视图（历史/老数据标签见 tags）。与产品的关联用于需求侧参考（PRD 术语表）。',
  supplychain_hd0202_supplier:
    '供应商主数据：与 PO 关联，用于采购跟踪与交期类分析。',
};

/** Extra ### 业务规则 blocks — global pipeline + object-specific PRD (concise) */
const businessRules = {
  supplychain_hd0202_bom: `### 业务规则

- **主料/替代料（PRD §1.7，与平台字段一致）**：\`alt_priority == 0\` 为主料；同父件、同 \`alt_group_no\` 内 \`alt_priority > 0\` 为替代料。分析/甘特/MRP 统计仅使用主料行（过滤替代料）。
- **版本**：取最新 \`bom_version\`（字典序最大）全量参与查询；空 BOM 则链路中断（PRD §5.3）。
- **异常**：同组多主料、无主料、字段缺失等处理见 PRD §1.7.4。`,
  supplychain_hd0202_forecast: `### 业务规则

- **核心对象**：全链路以预测单为根；MRP 通过 \`rootdemandbillno\` / 关联逻辑对齐预测（PRD §1.6）。
- **时间口径**：PR/PO 类查询需满足 \`biztime >= demandStart\`（需求起点，PRD §1.6.2）。
- **关闭**：\`closestatus_title\` 表示是否仍驱动新需求。`,
  supplychain_hd0202_inventory: `### 业务规则

- **可用量**：\`available_inventory_qty = inventory_qty - reserved_inventory_qty\`（字段注释）；齐套按业务配置的有效仓库汇总（PRD §6.6）。
- **异常**：库存接口失败时齐套判定挂起，不静默兜底（PRD §1.6.2）。`,
  supplychain_hd0202_material: `### 业务规则

- **提前期**：外购/委外优先 \`purchase_fixedleadtime\`，自制优先 \`product_fixedleadtime\`；缺失或 ≤0 时业务侧默认 7 天（PRD §5.4，实现以产品为准）。
- **属性**：\`materialattr\` 决定外购/自制/委外路径。`,
  supplychain_hd0202_monitoring_task: `### 业务规则

- 监测任务为产品侧跟踪载体；与预测单的关联见 \`monitor2forecast\` 关系（\`product_code\` ↔ \`material_number\`）。
- 任务状态、结束、过期规则见 PRD §3.4（实现层，非本表字段枚举）。`,
  supplychain_hd0202_mps: `### 业务规则

- **v4.2 溯源**：生产工单 \`sourcebillnumber\` 对齐**自制件 MRP 计划订单** \`billno\`（非直接对齐预测单号）；与 forecast 的关系对象在数据模型中可能仍为 \`sourcebillnumber → billno\`，业务查询以 PRD §1.6 为准。
- **完工**：合格入库与任务状态共同判定（PRD §4.5、§6.5）。`,
  supplychain_hd0202_mrp: `### 业务规则

- **有效行**：动态计划协同侧通常仅保留 \`closestatus_title\` 为「正常」或 \`A\` 的记录（PRD §4.4.4）。
- **数量**：优先 \`bizorderqty\`，否则 \`adviseorderqty\`；\`bizdropqty\` 为投放数量。
- **溯源**：\`rootdemandbillno\` 对齐预测单 \`billno\`。`,
  supplychain_hd0202_po: `### 业务规则

- **溯源**：\`srcbillid\`→PR 主键，\`srcbillentryid\`→PR 明细主键，\`srcbillnumber\`→PR 单号（PRD §1.6.1）。
- **交期**：\`deliverdate\` 用于齐套与预警；多 PO 取数规则见 PRD §4.4 / §11.3。`,
  supplychain_hd0202_pr: `### 业务规则

- **溯源**：\`srcbillid\` 对齐 MRP \`billno\`；下推 PO 后 \`joinqty\` 反映已转订单数量（PRD §4.4）。
- **时间过滤**：\`biztime >= demandStart\`（PRD §1.6.2）。`,
  supplychain_hd0202_product: `### 业务规则

- 产品编码与物料主数据 \`material_code\` 同源；用于关联预测、BOM、库存与销售订单。`,
  supplychain_hd0202_salesorder: `### 业务规则

- 复合主键见 Keys；与产品通过 \`product_code\` ↔ \`material_number\` 关联（关系类定义）。`,
  supplychain_hd0202_supplier: `### 业务规则

- PO 通过 \`supplier_number\` 对齐 \`supplier_code\`（见 \`po2supplier\`）。`,
};

for (const ot of gold.object_types) {
  const file = idToFile[ot.id];
  if (!file) continue;

  const pk = (ot.primary_keys || []).join(', ');
  const dk = ot.display_key || '';
  const ik = ot.incremental_key ?? '';
  const ds = ot.data_source;

  const rows = (ot.data_properties || []).map((p) => {
    const mf = p.mapped_field?.name || p.name;
    const desc = esc(p.comment || '');
    return `| ${esc(p.name)} | ${esc(p.display_name)} | ${typeMap(p.type)} | ${desc} | ${mf} |`;
  });

  const iconYaml = JSON.stringify(ot.icon || '');
  const colorYaml = JSON.stringify(ot.color || '');

  const body = `---
type: object_type
id: ${ot.id}
name: ${ot.name}
${yamlTags(ot.tags)}
icon: ${iconYaml}
color: ${colorYaml}
---

## ObjectType: ${ot.id}

${intros[ot.id] || ot.name}

${businessRules[ot.id] || ''}

### Data Properties

| Name | Display Name | Type | Description | Mapped Field |
|------|-------------|------|-------------|-------------|
${rows.join('\n')}

### Keys

Primary Keys: ${pk}
Display Key: ${dk}
Incremental Key: ${ik}

### Data Source

| Type | ID | Name |
|------|-----|------|
| ${ds?.type || 'data_view'} | ${ds?.id || ''} | ${ds?.name || ''} |
`;

  writeFileSync(join(root, 'bkn/object_types', file), body, 'utf8');
  console.log('Wrote', file);
}

console.log('Done.');
