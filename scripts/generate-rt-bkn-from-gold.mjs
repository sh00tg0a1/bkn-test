/**
 * Generate relation_types/*.bkn from the bundled full KN export under ref/.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const knExportPath = join(root, 'ref', 'HD供应链业务知识网络_v3.json');
const gold = JSON.parse(readFileSync(knExportPath, 'utf8'));

const idToFile = {
  d60nsctce73l0mrsstfg: 'mps2forecast.bkn',
  monitor2mds_forecast: 'monitor2forecast.bkn',
  mrp2material: 'mrp2material.bkn',
  mrp2mds_forecast: 'mrp2forecast.bkn',
  pr2mrp: 'pr2mrp.bkn',
  product2mds_forecast: 'product2forecast.bkn',
  supplychain_hd0202_bom2material: 'bom2material.bkn',
  supplychain_hd0202_material2inventory: 'material2inventory.bkn',
  supplychain_hd0202_po2supplier: 'po2supplier.bkn',
  supplychain_hd0202_pr2po: 'po2pr.bkn',
  supplychain_hd0202_product2bom: 'product2bom.bkn',
  supplychain_hd0202_product2inventory: 'product2inventory.bkn',
  supplychain_hd0202_salesorder2product: 'salesorder2product.bkn',
};

function esc(s) {
  if (s == null) return '';
  return String(s).replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
}

function yamlTags(tags) {
  if (!tags?.length) return 'tags: []';
  return 'tags:\n' + tags.map((t) => `  - ${t}`).join('\n');
}

/** Extra relation-level PRD notes (concise) */
const extraRules = {
  d60nsctce73l0mrsstfg:
    '\n\n**PRD v4.2**：业务上生产工单 `sourcebillnumber` 对齐**自制件 MRP 的 billno**；本关系在数据模型中仍为 `sourcebillnumber → forecast.billno`，查询请以 PRD §1.6 精确关联为准。',
  mrp2mds_forecast:
    '\n\n**PRD**：`rootdemandbillno → billno` 为精确溯源；无结果时需回 ERP 核对 MRP 是否已运算（PRD §4.4.5）。',
  pr2mrp:
    '\n\n采购申请单（PR）在 MRP 投放后生成，通过 `srcbillid` 回溯对应 MRP 计划订单 `billno`。',
  supplychain_hd0202_pr2po:
    '\n\n**PRD §1.6**：双键匹配；PR/PO 查询需加 `biztime >= demandStart`。',
};

for (const rt of gold.relation_types) {
  const file = idToFile[rt.id];
  if (!file) continue;

  const mapRows = (rt.mapping_rules || []).map((rule) => {
    const sp = rule.source_property || {};
    const tp = rule.target_property || {};
    return `| ${esc(sp.name)} | ${esc(sp.display_name)} | ${esc(tp.name)} | ${esc(tp.display_name)} |`;
  });

  const comment = (rt.comment || '').trim();
  const intro =
    comment ||
    `${rt.name}：源 \`${rt.source_object_type_id}\` → 目标 \`${rt.target_object_type_id}\`（类型：${rt.type || 'direct'}）。`;

  const body = `---
type: relation_type
id: ${rt.id}
name: ${rt.name}
source_object_type_id: ${rt.source_object_type_id}
target_object_type_id: ${rt.target_object_type_id}
${yamlTags(rt.tags)}
---

## RelationType: ${rt.id}

${intro}${extraRules[rt.id] || ''}

### 业务规则

- 关联类型：\`${rt.type || 'direct'}\`。
- 映射字段见下表；跨对象时间过滤、降级链等全局口径见 \`network.bkn\` 与 \`SKILL.md\`。

### Endpoint

| Source | Target | Type |
|--------|--------|------|
| ${rt.source_object_type_id} | ${rt.target_object_type_id} | ${rt.type || 'direct'} |

### Mapping Rules

| Source Property | Source Display Name | Target Property | Target Display Name |
|----------------|---------------------|-----------------|----------------------|
${mapRows.join('\n')}
`;

  writeFileSync(join(root, 'bkn/relation_types', file), body, 'utf8');
  console.log('Wrote', file);
}

console.log('Done.');
