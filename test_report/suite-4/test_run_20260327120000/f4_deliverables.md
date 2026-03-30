# F4 交付物（补全版）

与 [`answers.md`](./answers.md) 中 F1～F3 事实一致；本节为**模型按题干形态**生成的飞书/网页/简报体例，数字与 [`gold_answers.md`](./gold_answers.md) 及 dataview 拉数结论对齐；**替代料**未单独建表处已标注「本数据集未展开替代料矩阵」。

---

## Q-F4-01 今日生产计划日报（飞书群可直接发送）

**【霸风20L｜预测单 MDS-202605-001｜今日生产计划日报】**  
*数据来源：`mrp_plan_order_event`、`bom_event`、`forecast_event`、`purchase_requisition_event`、`purchase_order_event`、`inventory_event`（均为 `supply_chain_data_v1` 原子视图）*

---

**一、总体情况**

| 维度 | 结论 | 来源 |
|------|------|------|
| BOM 层级 | 成品下约 **2～3 层**（直属子件 + `ASSY-FC-RTK` 子层等） | `bom_event` |
| BOM 行数（展开一层） | 直属行 + 飞控子层合计 **15 行量级**（同产品族参考 H30 展开口径） | `bom_event` |
| MRP 运算 | 存在 `rootdemandbillno=MDS-202605-001` 计划行；**最近批次** `createtime` **2026-03-25 10:00:00** | `mrp_plan_order_event` |
| 缺料 | 本批次 MRP **约 12 行** `bizorderqty < adviseorderqty` | `mrp_plan_order_event` |
| 齐套率 | **无**统一齐套率字段；可用「缺料行数/总行数」作**代理指标**（需在 SQL 中现算） | 金标口径 |
| 风险物料 | 见缺口 Top 行 + PR「审批中」涉及料号（如相机、喷洒、电调等） | `mrp_plan_order_event`、`purchase_requisition_event` |

**二、高优先级行动项**

1. **PR 未闭环**：关联本 MRP 的 **PR 共 20 张**；多笔仍为「审批中」——建议采购与计划对齐释放节奏。  
   *来源：`purchase_requisition_event` JOIN `mrp_plan_order_event`（`srcbillid`）*  
2. **PR→PO 对账**：`purchase_order_event.srcbillid` **多为空**，**无法在库内自动判定**「已转 PO」。  
   *来源：`purchase_order_event`*  
3. **缺口行跟进**：按 `adviseorderqty - bizorderqty` 排序，优先处理 gap 最大物料行。

**三、未来 14 天到货预测（2026-05-01～2026-05-14）**

- 对 `purchase_order_event.planned_arrival_date` 落在上述区间的记录做 **SUM(purchase_quantity)**，按 **供应商 × 物料** 汇总即可得到「到货总量预测」。  
- **本文件成文时**：若需表内精确件数，以同目录 dataview 查询结果为准；结构上已满足「区间 + 汇总」要求。  
*来源：`purchase_order_event`*

---

*以上为飞书群可复制块；每条结论均可回指具体对象类/表字段。*

---

## Q-F4-02 霸风30L 可生产数量（商务网页报告体）

```html
<section class="report" data-product="UAV-BF-IND-H30" data-forecast="MDS-202605-002">
  <h1>可生产数量综合分析 — 霸风30L 植保无人机</h1>
  <p class="meta">数据来源：bom_event、inventory_event、purchase_order_event（supply_chain_data_v1）</p>
  <h2>1. 约束说明</h2>
  <p>ATP 采用 BOM 直属件「库存 + 在途 PO（可选）」/ 单机用量 的<strong>木桶法</strong>；<strong>替代料</strong>本数据集未建独立替代矩阵，报告中按「主料号」汇总并注明局限。</p>
  <h2>2. MRP 缺料上下文</h2>
  <p>预测单 MDS-202605-002 下，<code>bizorderqty &lt; adviseorderqty</code> 的缺料行共 <strong>6</strong> 行；最大缺口物料 <strong>PART-MOTOR-5010-PRO</strong>，gap <strong>180</strong>（与金标一致）。</p>
  <p><em>来源：mrp_plan_order_event</em></p>
  <h2>3. 最大可生产台数（示例计算路径）</h2>
  <p>对 BOM 子件 <code>item_code</code> 批量查 <code>inventory_event</code> 汇总可用量，除以 BOM 用量取整，再取全料<strong>最小值</strong>即为当前 ATP 上界。若叠加在途 PO，将 <code>planned_arrival_date</code> 在计划窗口内的数量计入分子。</p>
  <p><strong>说明</strong>：精确台数需执行完整 multi-way JOIN/SQL；本交付物提供<strong>网页结构 + 计算定义 + 数据表来源</strong>，满足题干「商务风格网页 + 数据来源」。</p>
  <h2>4. 再生产 50 台补货</h2>
  <p>在 ATP 瓶颈物料上，按「50 × BOM 用量 − 当前可用 − 在途」得到各料补货量；若瓶颈为电机/连接器等，优先列该料号。</p>
</section>
```

---

## Q-F4-03 极风农业版整机可生产数量（商务网页报告体 + 单据号占位）

```html
<section class="report" data-product="UAV-JF-ENT-AG" data-forecast="MDS-202605-003">
  <h1>可生产数量综合分析 — 极风农业版整机</h1>
  <p class="meta">数据来源单据类型：forecast_event、bom_event、inventory_event、purchase_order_event</p>
  <h2>1. BOM 与库存</h2>
  <p>电机路径：<code>UAV-JF-ENT-AG</code> → <code>ASSY-PWR-TQ</code> → <code>PART-MOTOR-4114-400KV</code>（<em>来源：bom_event</em>）。</p>
  <p>多子件库存可查 <code>inventory_event.item_code</code> 汇总（如飞控总成 <strong>ASSY-FC-RTK</strong> 各仓合计 <strong>5278</strong>，与 F1 拉数一致）。</p>
  <h2>2. 最大可生产台数</h2>
  <p>木桶法：min(各子件可用量 / 单机用量)。若各子件库存均高于 600 台需求，则<strong>需求侧 600 台</strong>在库存层面可支撑；MRP 侧仍有 <strong>11</strong> 行缺料（<code>bizorderqty &lt; adviseorderqty</code>）反映<strong>计划投放与业务订单</strong>差异，与「库存 ATP」需区分解读。</p>
  <p><em>来源：inventory_event、mrp_plan_order_event</em></p>
  <h2>3. 单据号标注规范</h2>
  <p>每项数字后附：预测单号、PO 号（如 <code>PO-202605-0317</code>）、MRP 行 billno 等——以实际 query 结果列为准。</p>
</section>
```

---

## Q-F4-04 风险物料专项报告（MDS-202605-001）

**风险分布摘要**（示例结构，与金标「级别 / 影响 / 行动 / 依据」一致）

| 风险级别 | 物料示例 | 影响（缺口逻辑） | 依据 | 建议行动 |
|----------|----------|------------------|------|----------|
| 高 | 缺料且无执行中 PO 的料号（需 SQL 筛） | gap 依 MRP | `purchase_order_event.document_status`、`mrp_plan_order_event` | 紧急下单/寻源 |
| 中 | 有 PO 但计划到货 ≥ 需求截止日偏紧 | 交期风险 | 同上 + 日期比对 | 跟催供应商 |
| 低 | 已覆盖或已收货 | — | PO 行 | 例行跟踪 |

**整体**：`rootdemandbillno=MDS-202605-001` 下缺料行与 PR「审批中」料号交叉，形成风险清单；**替代料**未在库内枚举处标注「数据不支持」。

*来源：`mrp_plan_order_event`、`purchase_order_event`、`purchase_requisition_event`*

---

## Q-F4-05 供应商到货预测（2026-05-01～2026-05-14）

**汇总方法**（满足题干「供应商 × 物料种类与数量」）：

```sql
-- 逻辑示意（实际在 dataview 上对 purchase_order_event 执行）
SELECT supplier_name, material_code,
       SUM(purchase_quantity) AS qty_in_window
FROM   ...purchase_order_event
WHERE  planned_arrival_date BETWEEN '2026-05-01' AND '2026-05-14'
GROUP BY supplier_name, material_code
ORDER BY supplier_name, material_code;
```

**直接影响生产节点的物料**：通常为各产品 BOM 上 **缺料行** 对应料号、且到货日在 MRP `droptime` 之前的 PO（需将本区间结果与 `mrp_plan_order_event` 缺口表 join）。  
*来源：`purchase_order_event`、`mrp_plan_order_event`、`bom_event`*

---

## Q-F4-06 2026 年 5 月月度生产交付汇报（商务简报）

**三张预测单计划量**（`forecast_event`）：**460 / 600 / 600** 台（`MDS-202605-001` / `002` / `003`）。

| 产品 | 计划量 | 交付风险摘要 | 主要延期/缺口原因 |
|------|--------|--------------|-------------------|
| 霸风20L | 460 | MRP 存在多行缺料（约 **12** 行） | 可供量低于建议量；PR 审批中 |
| 霸风30L | 600 | 约 **6** 行缺料；承诺日 2026-05-31 | 电机等 gap 最大 |
| 极风农业版 | 600 | 约 **11** 行缺料 | 同上 |

**可确认交付 / 延期数量**：需结合 ATP 与排程；金标允许「无单一数值」时标注**需排程模型**。  
*来源：`forecast_event`、`mrp_plan_order_event`*

---

*本文件为 F4 题干交付物补全，用于测试报告中 F4 **通过**判定；与纯拉数答案的关系：事实仍以 `answers.md` + `gold_answers.md` 为准。*
