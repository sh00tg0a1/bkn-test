# S4 4跳问答 — 数据库查询答案

> 查询方式: kweaver dataview query (mdl-uniquery SQL)
> 测试时间: 2026-03-26 18:31:39

---

## Q01

**问题**: 广州绿野订购的产品BOM物料有高风险供应商吗？

**SQL**:
```sql
SELECT DISTINCT su.supplier_name, su.risk_level, po.material_code FROM mysql_mhggp0vj."tem"."sales_order_event" so JOIN mysql_mhggp0vj."tem"."bom_event" b ON so.product_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id WHERE so.customer_name LIKE '%广州绿野%'
```

**查询耗时**: 290ms | **返回行数**: 7

**数据**:
```json
[
  {
    "supplier_name": "常州雷达测高仪制造厂",
    "risk_level": "低",
    "material_code": "PART-RADAR-ALT"
  },
  {
    "risk_level": "低",
    "material_code": "PART-SPRAYER-16L",
    "supplier_name": "深圳农业喷洒系统公司"
  },
  {
    "supplier_name": "索尼半导体解决方案",
    "risk_level": "低",
    "material_code": "PART-CAM-FPV"
  },
  {
    "supplier_name": "深圳农业喷洒系统公司",
    "risk_level": "低",
    "material_code": "PART-SPRAYER-20L"
  },
  {
    "risk_level": "低",
    "material_code": "PART-FRAME-HEX-CF",
    "supplier_name": "东莞碳纤维复合材料厂"
  },
  {
    "material_code": "PART-SPRAYER-30L",
    "supplier_name": "深圳农业喷洒系统公司",
    "risk_level": "低"
  },
  {
    "supplier_name": "东莞碳纤维复合材料厂",
    "risk_level": "低",
    "material_code": "PART-FRAME-HEX-CF-HD"
  }
]
```

---

## Q02

**问题**: 广州绿野订购产品BOM物料库存够不够(>500)？

**SQL**:
```sql
SELECT b.child_code, b.child_name, COALESCE(SUM(inv.quantity),0) as inv_qty FROM mysql_mhggp0vj."tem"."sales_order_event" so JOIN mysql_mhggp0vj."tem"."bom_event" b ON so.product_code=b.parent_code LEFT JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON b.child_code=inv.item_code WHERE so.customer_name LIKE '%广州绿野%' GROUP BY b.child_code, b.child_name
```

**查询耗时**: 299ms | **返回行数**: 17

**数据**:
```json
[
  {
    "inv_qty": "25599",
    "child_code": "PART-RADAR-ALT",
    "child_name": "雷达测高仪"
  },
  {
    "child_code": "PART-SPRAYER-16L",
    "child_name": "16升智能喷洒系统",
    "inv_qty": "8804"
  },
  {
    "child_code": "PART-RC-IND",
    "child_name": "工业遥控器",
    "inv_qty": "19040"
  },
  {
    "inv_qty": "8664",
    "child_code": "ASSY-BAT-DUAL",
    "child_name": "双电池冗余系统"
  },
  {
    "child_code": "ASSY-PWR-TQ",
    "child_name": "高扭矩动力系统总成",
    "inv_qty": "22780"
  },
  {
    "child_code": "PART-CAM-FPV",
    "child_name": "FPV图传相机",
    "inv_qty": "8288"
  },
  {
    "child_code": "ASSY-FC-RTK",
    "child_name": "RTK高精度飞控总成",
    "inv_qty": "31836"
  },
  {
    "child_code": "ASSY-BODY-IND-01",
    "child_name": "工业级强化机身总成",
    "inv_qty": "6440"
  },
  {
    "child_code": "PART-SPRAYER-20L",
    "child_name": "20升智能喷洒系统",
    "inv_qty": "8532"
  },
  {
    "child_code": "PART-BAT-12S-16000",
    "child_name": "12S16000mAh工业电池",
    "inv_qty": "3507"
  },
  {
    "inv_qty": "10194",
    "child_code": "PART-FRAME-HEX-CF",
    "child_name": "六轴碳纤维机架"
  },
  {
    "child_code": "PART-SPRAYER-30L",
    "child_name": "30升智能喷洒系统",
    "inv_qty": "5098"
  },
  {
    "child_name": "12S22000mAh重载电池",
    "inv_qty": "2374",
    "child_code": "PART-BAT-12S-22000"
  },
  {
    "child_name": "3016碳纤螺旋桨",
    "inv_qty": "5742",
    "child_code": "PART-PROP-3016-CF"
  },
  {
    "inv_qty": "8578",
    "child_code": "PART-ESC-60A",
    "child_name": "60A电调"
  },
  {
    "child_code": "PART-MOTOR-5010-PRO",
    "child_name": "5010重载无刷电机",
    "inv_qty": "5986"
  },
  {
    "child_code": "PART-FRAME-HEX-CF-HD",
    "child_name": "六轴重载碳纤维机架",
    "inv_qty": "7696"
  }
]
```

---

## Q03

**问题**: SH-202305-0001产品BOM物料的采购订单有逾期的吗？

**SQL**:
```sql
SELECT po.purchase_order_number, po.material_code, po.planned_arrival_date, po.required_date FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."bom_event" b ON sh.product_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code WHERE sh.shipment_number='SH-202305-0001' AND po.planned_arrival_date>po.required_date
```

**查询耗时**: 285ms | **返回行数**: 0

**数据**: (无结果)

---

## Q04

**问题**: FAC001生产的所有产品发货物流商占比？

**SQL**:
```sql
SELECT sh.logistics_provider, COUNT(*) as cnt FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."shipment_event" sh ON prd.output_code=sh.product_code WHERE prd.factory_id IN (SELECT factory_id FROM mysql_mhggp0vj."tem"."factory_entity" WHERE factory_id='FAC001') GROUP BY sh.logistics_provider ORDER BY cnt DESC
```

**查询耗时**: 295ms | **返回行数**: 8

**数据**:
```json
[
  {
    "logistics_provider": "京东物流",
    "cnt": 15
  },
  {
    "logistics_provider": "申通快递",
    "cnt": 11
  },
  {
    "logistics_provider": "中通快递",
    "cnt": 10
  },
  {
    "logistics_provider": "顺丰速运",
    "cnt": 9
  },
  {
    "logistics_provider": "百世快递",
    "cnt": 8
  },
  {
    "cnt": 8,
    "logistics_provider": "德邦物流"
  },
  {
    "logistics_provider": "圆通速递",
    "cnt": 6
  },
  {
    "logistics_provider": "韵达快递",
    "cnt": 6
  }
]
```

---

## Q05

**问题**: WH001里的产品客户里有多少T1大客户？

**SQL**:
```sql
SELECT COUNT(DISTINCT cu.customer_code) as t1_count FROM mysql_mhggp0vj."tem"."inventory_event" inv JOIN mysql_mhggp0vj."tem"."sales_order_event" so ON inv.item_code=so.product_code JOIN mysql_mhggp0vj."tem"."customer_entity" cu ON so.customer_id=cu.customer_id WHERE inv.warehouse_id IN (SELECT warehouse_id FROM mysql_mhggp0vj."tem"."warehouse_entity" WHERE warehouse_id='WH001') AND cu.customer_level='T1'
```

**查询耗时**: 324ms | **返回行数**: 1

**数据**:
```json
[
  {
    "t1_count": 22
  }
]
```

---

## Q06

**问题**: PART-CAM-FIX-12MP被用在哪些产品上？T1级客户？

**SQL**:
```sql
SELECT DISTINCT cu.customer_name, cu.customer_code, cu.customer_level FROM mysql_mhggp0vj."tem"."bom_event" b JOIN mysql_mhggp0vj."tem"."shipment_event" sh ON b.parent_code=sh.product_code JOIN mysql_mhggp0vj."tem"."customer_entity" cu ON sh.customer_code=cu.customer_code WHERE b.child_code='PART-CAM-FIX-12MP' AND cu.customer_level='T1'
```

**查询耗时**: 279ms | **返回行数**: 0

**数据**: (无结果)

---

## Q07

**问题**: SUP-021供的零件用在哪些产品？哪些工厂生产？认证？

**SQL**:
```sql
SELECT DISTINCT p.product_name, fac.factory_name, fac.certification FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."bom_event" b ON po.material_code=b.child_code JOIN mysql_mhggp0vj."tem"."product_entity" p ON b.parent_code=p.product_code JOIN mysql_mhggp0vj."tem"."production_order_event" prd ON p.product_code=prd.output_code JOIN mysql_mhggp0vj."tem"."factory_entity" fac ON prd.factory_id=fac.factory_id WHERE po.supplier_id IN (SELECT supplier_id FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_code='SUP-021')
```

**结果**: ERROR — fetch failed: Client network socket disconnected before secure TLS connection was established
Hint: use --insecure (-k) to skip TLS verification for self-signed certificates.

---

## Q08

**问题**: CUST-10003订购产品BOM物料来料验收情况？

**SQL**:
```sql
SELECT DISTINCT mp.material_code, mp.material_name, mp.inspection_status FROM mysql_mhggp0vj."tem"."sales_order_event" so JOIN mysql_mhggp0vj."tem"."bom_event" b ON so.product_code=b.parent_code JOIN mysql_mhggp0vj."tem"."material_procurement_event" mp ON b.child_code=mp.material_code WHERE so.customer_id IN (SELECT customer_id FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_code='CUST-10003')
```

**查询耗时**: 312ms | **返回行数**: 33

**数据**:
```json
[
  {
    "material_code": "PART-CAM-FPV",
    "material_name": "FPV图传相机",
    "inspection_status": "验收中"
  },
  {
    "material_code": "ASSY-FC-RTK",
    "material_name": "RTK高精度飞控总成",
    "inspection_status": "验收中"
  },
  {
    "material_code": "ASSY-PWR-TQ",
    "material_name": "高扭矩动力系统总成",
    "inspection_status": "已验收"
  },
  {
    "inspection_status": "待验收",
    "material_code": "ASSY-FC-RTK",
    "material_name": "RTK高精度飞控总成"
  },
  {
    "material_code": "PART-FRAME-HEX-CF-HD",
    "material_name": "六轴重载碳纤维机架",
    "inspection_status": "已验收"
  },
  {
    "material_code": "ASSY-PWR-TQ",
    "material_name": "高扭矩动力系统总成",
    "inspection_status": "验收中"
  },
  {
    "material_name": "工业遥控器",
    "inspection_status": "已验收",
    "material_code": "PART-RC-IND"
  },
  {
    "material_code": "ASSY-BAT-DUAL",
    "material_name": "双电池冗余系统",
    "inspection_status": "待验收"
  },
  {
    "material_code": "PART-FRAME-HEX-CF",
    "material_name": "六轴碳纤维机架",
    "inspection_status": "验收中"
  },
  {
    "material_code": "PART-MOTOR-5010-PRO",
    "material_name": "5010重载无刷电机",
    "inspection_status": "待验收"
  },
  {
    "material_code": "PART-MOTOR-5010-PRO",
    "material_name": "5010重载无刷电机",
    "inspection_status": "验收中"
  },
  {
    "material_code": "PART-SPRAYER-16L",
    "material_name": "16升智能喷洒系统",
    "inspection_status": "验收中"
  },
  {
    "material_code": "PART-SPRAYER-30L",
    "material_name": "30升智能喷洒系统",
    "inspection_status": "待验收"
  },
  {
    "material_name": "5010重载无刷电机",
    "inspection_status": "已验收",
    "material_code": "PART-MOTOR-5010-PRO"
  },
  {
    "material_code": "PART-BAT-12S-22000",
    "material_name": "12S22000mAh重载电池",
    "inspection_status": "验收中"
  },
  {
    "material_code": "PART-SPRAYER-20L",
    "material_name": "20升智能喷洒系统",
    "inspection_status": "已验收"
  },
  {
    "material_code": "PART-SPRAYER-16L",
    "material_name": "16升智能喷洒系统",
    "inspection_status": "已验收"
  },
  {
    "inspection_status": "验收中",
    "material_code": "
```

---

## Q09

**问题**: MO-202305001产品BOM物料采购供应商哪些月结30天？

**SQL**:
```sql
SELECT DISTINCT su.supplier_name, su.supplier_code, su.payment_terms FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."bom_event" b ON prd.output_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id WHERE prd.production_order_number='MO-202305001' AND su.payment_terms LIKE '%30%'
```

**查询耗时**: 276ms | **返回行数**: 0

**数据**: (无结果)

---

## Q10

**问题**: UAV-XF-BASIC BOM物料库存在哪些仓库？有AGV吗？

**SQL**:
```sql
SELECT DISTINCT b.child_code, inv.warehouse_name, wh.warehouse_code, wh.has_agv, wh.agv_count FROM mysql_mhggp0vj."tem"."bom_event" b JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON b.child_code=inv.item_code JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON inv.warehouse_id=wh.warehouse_id WHERE b.parent_code='UAV-XF-BASIC'
```

**查询耗时**: 290ms | **返回行数**: 9

**数据**:
```json
[
  {
    "warehouse_name": "电子材料仓",
    "warehouse_code": "WH-华南-02",
    "has_agv": "是",
    "agv_count": 8,
    "child_code": "ASSY-BODY-PLA-01"
  },
  {
    "warehouse_code": "WH-华中-01",
    "has_agv": "是",
    "agv_count": 15,
    "child_code": "ASSY-BODY-PLA-01",
    "warehouse_name": "中央成品仓"
  },
  {
    "agv_count": 8,
    "child_code": "ASSY-FC-BASIC",
    "warehouse_name": "电子材料仓",
    "warehouse_code": "WH-华南-02",
    "has_agv": "是"
  },
  {
    "has_agv": "是",
    "agv_count": 15,
    "child_code": "ASSY-FC-BASIC",
    "warehouse_name": "中央成品仓",
    "warehouse_code": "WH-华中-01"
  },
  {
    "warehouse_name": "电子材料仓",
    "warehouse_code": "WH-华南-02",
    "has_agv": "是",
    "agv_count": 8,
    "child_code": "PART-CAM-FIX-12MP"
  },
  {
    "warehouse_code": "WH-华南-02",
    "has_agv": "是",
    "agv_count": 8,
    "child_code": "ASSY-PWR-STD",
    "warehouse_name": "电子材料仓"
  },
  {
    "warehouse_code": "WH-华中-01",
    "has_agv": "是",
    "agv_count": 15,
    "child_code": "ASSY-PWR-STD",
    "warehouse_name": "中央成品仓"
  },
  {
    "child_code": "PART-BAT-2S-3000",
    "warehouse_name": "配件仓",
    "warehouse_code": "WH-华中-03",
    "has_agv": "否",
    "agv_count": 0
  },
  {
    "child_code": "PART-RC-BASIC",
    "warehouse_name": "配件仓",
    "warehouse_code": "WH-华中-03",
    "has_agv": "否",
    "agv_count": 0
  }
]
```

---

## Q11

**问题**: FAC001生产产品的客户里有多少是重点客户？

**SQL**:
```sql
SELECT COUNT(DISTINCT cu.customer_code) as named_count FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."shipment_event" sh ON prd.output_code=sh.product_code JOIN mysql_mhggp0vj."tem"."customer_entity" cu ON sh.customer_code=cu.customer_code WHERE prd.factory_id IN (SELECT factory_id FROM mysql_mhggp0vj."tem"."factory_entity" WHERE factory_id='FAC001') AND cu.is_named_customer='是'
```

**查询耗时**: 290ms | **返回行数**: 1

**数据**:
```json
[
  {
    "named_count": 30
  }
]
```

---

## Q12

**问题**: ASSY-BODY-PLA-01供应商发货入库仓库里还有哪些产品？销售订单总金额？

**SQL**:
```sql
SELECT DISTINCT inv.item_code, inv.item_name, SUM(so.total_amount) as so_total FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON mp.warehouse_id=inv.warehouse_id JOIN mysql_mhggp0vj."tem"."sales_order_event" so ON inv.item_code=so.product_code WHERE mp.material_code='ASSY-BODY-PLA-01' GROUP BY inv.item_code, inv.item_name
```

**查询耗时**: 289ms | **返回行数**: 0

**数据**: (无结果)

---

## Q13

**问题**: SUP-021供的所有物料被用在哪些产品？运输中发货单数？

**SQL**:
```sql
SELECT COUNT(*) as in_transit FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."bom_event" b ON po.material_code=b.child_code JOIN mysql_mhggp0vj."tem"."shipment_event" sh ON b.parent_code=sh.product_code WHERE po.supplier_id IN (SELECT supplier_id FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_code='SUP-021') AND sh.delivery_status='运输中'
```

**查询耗时**: 284ms | **返回行数**: 1

**数据**:
```json
[
  {
    "in_transit": 75
  }
]
```

---

## Q14

**问题**: FAC001生产产品BOM中有损耗物料(scrap_rate>0)？库存充足吗？

**SQL**:
```sql
SELECT DISTINCT b.child_code, b.child_name, b.scrap_rate, COALESCE(SUM(inv.quantity),0) as inv_qty FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."bom_event" b ON prd.output_code=b.parent_code LEFT JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON b.child_code=inv.item_code WHERE prd.factory_id IN (SELECT factory_id FROM mysql_mhggp0vj."tem"."factory_entity" WHERE factory_id='FAC001') AND b.scrap_rate>0 GROUP BY b.child_code, b.child_name, b.scrap_rate
```

**查询耗时**: 280ms | **返回行数**: 29

**数据**:
```json
[
  {
    "inv_qty": "821",
    "child_code": "PART-CAM-FIX-12MP",
    "child_name": "1200万像素固定相机",
    "scrap_rate": 0.01
  },
  {
    "child_code": "PART-BAT-2S-3000",
    "child_name": "标准智能电池2S3000mAh",
    "scrap_rate": 0.03,
    "inv_qty": "1080"
  },
  {
    "inv_qty": "4380",
    "child_code": "PART-RC-BASIC",
    "child_name": "基础遥控器",
    "scrap_rate": 0.01
  },
  {
    "child_code": "PART-CAM-FIX-20MP",
    "child_name": "2000万像素固定相机",
    "scrap_rate": 0.01,
    "inv_qty": "759"
  },
  {
    "inv_qty": "1440",
    "child_code": "PART-BAT-3S-4000",
    "child_name": "增强智能电池3S4000mAh",
    "scrap_rate": 0.03
  },
  {
    "scrap_rate": 0.01,
    "inv_qty": "2693",
    "child_code": "PART-RC-ADV",
    "child_name": "高级遥控器"
  },
  {
    "child_code": "PART-CAM-GIMBAL-1INCH",
    "child_name": "1英寸三轴云台相机",
    "scrap_rate": 0.01,
    "inv_qty": "1198"
  },
  {
    "child_code": "PART-BAT-4S-5200",
    "child_name": "高容智能电池4S5200mAh",
    "scrap_rate": 0.01,
    "inv_qty": "2478"
  },
  {
    "child_code": "PART-RC-PRO",
    "child_name": "专业遥控器",
    "scrap_rate": 0.01,
    "inv_qty": "10956"
  },
  {
    "child_code": "PART-AVOID-VISION",
    "child_name": "视觉避障系统",
    "scrap_rate": 0.02,
    "inv_qty": "4491"
  },
  {
    "child_code": "PART-CAM-ZOOM",
    "child_name": "变焦相机模组",
    "scrap_rate": 0.01,
    "inv_qty": "949"
  },
  {
    "child_code": "PART-AVOID-ENHANCED",
    "child_name": "增强避障系统（视觉+红外）",
    "scrap_rate": 0.03,
    "inv_qty": "5280"
  },
  {
    "child_code": "VIRT-CAM-SEL",
    "child_name": "相机配置选择件",
    "scrap_rate": 0.03,
    "inv_qty": "3182"
  },
  {
    "child_code": "PART-BAT-4S-5200",
    "child_name": "高容智能电池4S5200mAh",
    "scrap_rate": 0.03,
    "inv_qty": "1239"
  },
  {
    "child_name": "FPV图传相机",
    "scrap_rate": 0.01,
    "inv_qty": "3552",
    "child_code": "PART-CAM-FPV"
  },
  {
    "child_code": "PART-RC-IND",
    "child_name": "工业遥控器",
    "scrap_rate": 0.01,
    "inv_qty": "13600"
  },
  {
    "inv_qty": "4402",

```

---

## Q15

**问题**: 广州绿野的发货仓库里还有哪些其他产品？在哪些工厂生产？

**SQL**:
```sql
SELECT DISTINCT inv.item_code, inv.item_name, fac.factory_name FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON sh.warehouse_id=inv.warehouse_id JOIN mysql_mhggp0vj."tem"."production_order_event" prd ON inv.item_code=prd.output_code JOIN mysql_mhggp0vj."tem"."factory_entity" fac ON prd.factory_id=fac.factory_id WHERE sh.customer_name LIKE '%广州绿野%'
```

**查询耗时**: 293ms | **返回行数**: 10

**数据**:
```json
[
  {
    "item_code": "UAV-XF-BASIC",
    "item_name": "旋风基础版整机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "item_code": "UAV-XF-BASIC-PLUS",
    "item_name": "旋风增强版整机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "item_code": "UAV-XF-PRO-A",
    "item_name": "巡风摄影版整机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "item_code": "UAV-XF-PRO-B",
    "item_name": "巡风探索版整机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "item_code": "UAV-XF-PRO-C",
    "item_name": "巡风全能版整机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "item_code": "UAV-JF-ENT-AG",
    "item_name": "极风农业版整机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "item_code": "UAV-JF-ENT-SV",
    "item_name": "极风测绘版整机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "factory_name": "深圳天翼无人机总装厂",
    "item_code": "UAV-JF-ENT-SC",
    "item_name": "极风安防版整机"
  },
  {
    "item_code": "UAV-BF-IND-H20",
    "item_name": "霸风20L植保无人机",
    "factory_name": "深圳天翼无人机总装厂"
  },
  {
    "item_code": "UAV-BF-IND-H30",
    "item_name": "霸风30L植保无人机",
    "factory_name": "深圳天翼无人机总装厂"
  }
]
```

---

## Q16

**问题**: UAV-XF-BASIC BOM供应商里哪些也给其他产品供货？

**SQL**:
```sql
SELECT DISTINCT su.supplier_name, su.supplier_code, b2.parent_code as other_product FROM mysql_mhggp0vj."tem"."bom_event" b1 JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b1.child_code=po.material_code JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id JOIN mysql_mhggp0vj."tem"."purchase_order_event" po2 ON su.supplier_id=po2.supplier_id JOIN mysql_mhggp0vj."tem"."bom_event" b2 ON po2.material_code=b2.child_code WHERE b1.parent_code='UAV-XF-BASIC' AND b2.parent_code!='UAV-XF-BASIC'
```

**查询耗时**: 318ms | **返回行数**: 9

**数据**:
```json
[
  {
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021",
    "other_product": "UAV-XF-BASIC-PLUS"
  },
  {
    "other_product": "UAV-XF-PRO-A",
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021"
  },
  {
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021",
    "other_product": "UAV-XF-PRO-B"
  },
  {
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021",
    "other_product": "VIRT-CAM-SEL"
  },
  {
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021",
    "other_product": "UAV-JF-ENT-AG"
  },
  {
    "supplier_code": "SUP-021",
    "other_product": "UAV-JF-ENT-SV",
    "supplier_name": "索尼半导体解决方案"
  },
  {
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021",
    "other_product": "UAV-JF-ENT-SC"
  },
  {
    "supplier_code": "SUP-021",
    "other_product": "UAV-BF-IND-H20",
    "supplier_name": "索尼半导体解决方案"
  },
  {
    "other_product": "UAV-BF-IND-H30",
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021"
  }
]
```

---

## Q17

**问题**: WH002收到的物料被用在哪些产品？有多少加急销售订单？

**SQL**:
```sql
SELECT COUNT(*) as urgent_count FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."bom_event" b ON mp.material_code=b.child_code JOIN mysql_mhggp0vj."tem"."sales_order_event" so ON b.parent_code=so.product_code WHERE mp.warehouse_id IN (SELECT warehouse_id FROM mysql_mhggp0vj."tem"."warehouse_entity" WHERE warehouse_id='WH002') AND so.is_urgent='是'
```

**查询耗时**: 313ms | **返回行数**: 1

**数据**:
```json
[
  {
    "urgent_count": 388
  }
]
```

---

## Q18

**问题**: SUP-001供的物料库存在哪些仓库？发货客户里有T2的吗？

**SQL**:
```sql
SELECT DISTINCT cu.customer_name, cu.customer_code, cu.customer_level FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON po.material_code=inv.item_code JOIN mysql_mhggp0vj."tem"."shipment_event" sh ON inv.warehouse_id=sh.warehouse_id JOIN mysql_mhggp0vj."tem"."customer_entity" cu ON sh.customer_code=cu.customer_code WHERE po.supplier_id IN (SELECT supplier_id FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_code='SUP-001') AND cu.customer_level='T2'
```

**查询耗时**: 285ms | **返回行数**: 1

**数据**:
```json
[
  {
    "customer_name": "北京环境水务科技有限公司",
    "customer_code": "CUST-10162",
    "customer_level": "T2"
  }
]
```

---

## Q19

**问题**: UAV-XF-PRO-A的客户还下了哪些其他产品订单？有库存吗？

**SQL**:
```sql
SELECT DISTINCT so2.product_code, so2.product_name, COALESCE(inv.quantity,0) as inv_qty FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."sales_order_event" so2 ON sh.customer_code IN (SELECT customer_code FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_id=so2.customer_id) LEFT JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON so2.product_code=inv.item_code WHERE sh.product_code='UAV-XF-PRO-A' AND so2.product_code!='UAV-XF-PRO-A'
```

**查询耗时**: 296ms | **返回行数**: 7

**数据**:
```json
[
  {
    "inv_qty": 3254,
    "product_code": "UAV-BF-IND-H30",
    "product_name": "UAV-BF-IND-H30"
  },
  {
    "product_code": "UAV-JF-ENT-AG",
    "product_name": "UAV-JF-ENT-AG",
    "inv_qty": 4348
  },
  {
    "inv_qty": 2662,
    "product_code": "UAV-BF-IND-H20",
    "product_name": "UAV-BF-IND-H20"
  },
  {
    "product_code": "UAV-XF-PRO-B",
    "product_name": "UAV-XF-PRO-B",
    "inv_qty": 5974
  },
  {
    "product_code": "UAV-JF-ENT-SV",
    "product_name": "UAV-JF-ENT-SV",
    "inv_qty": 2739
  },
  {
    "inv_qty": 3035,
    "product_code": "UAV-XF-PRO-C",
    "product_name": "UAV-XF-PRO-C"
  },
  {
    "inv_qty": 4232,
    "product_code": "UAV-XF-BASIC-PLUS",
    "product_name": "UAV-XF-BASIC-PLUS"
  }
]
```

---

## Q20

**问题**: 基础飞控总成(ASSY-FC-BASIC)供应商发货入库仓库里还有哪些产品？生产工单优先级？

**SQL**:
```sql
SELECT DISTINCT inv.item_code, inv.item_name, prd.priority FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON mp.warehouse_id=inv.warehouse_id JOIN mysql_mhggp0vj."tem"."production_order_event" prd ON inv.item_code=prd.output_code WHERE mp.material_code='ASSY-FC-BASIC'
```

**查询耗时**: 301ms | **返回行数**: 0

**数据**: (无结果)

---

## Q21

**问题**: CUST-10130收到的产品BOM物料采购订单中已收货的有几笔？

**SQL**:
```sql
SELECT po.purchase_order_number, po.material_code, po.document_status FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."bom_event" b ON sh.product_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code WHERE sh.customer_code='CUST-10130' AND po.document_status='已收货'
```

**查询耗时**: 299ms | **返回行数**: 2

**数据**:
```json
[
  {
    "document_status": "已收货",
    "purchase_order_number": "PO-2023010007",
    "material_code": "PART-CAM-FIX-12MP"
  },
  {
    "purchase_order_number": "PO-2023040002",
    "material_code": "PART-CAM-FIX-12MP",
    "document_status": "已收货"
  }
]
```

---

## Q22

**问题**: FAC001领料物料的采购供应商年产能合计？

**SQL**:
```sql
SELECT DISTINCT su.supplier_name, su.supplier_code, su.annual_capacity FROM mysql_mhggp0vj."tem"."material_requisition_event" mr JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON mr.material_code=po.material_code JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id WHERE mr.factory_id IN (SELECT factory_id FROM mysql_mhggp0vj."tem"."factory_entity" WHERE factory_id='FAC001')
```

**查询耗时**: 303ms | **返回行数**: 2

**数据**:
```json
[
  {
    "supplier_name": "索尼半导体解决方案",
    "supplier_code": "SUP-021",
    "annual_capacity": "1896万件"
  },
  {
    "supplier_name": "北京智能视觉科技公司",
    "supplier_code": "SUP-035",
    "annual_capacity": "6637万件"
  }
]
```

---

## Q23

**问题**: PO-2024040001供应商的所有物料被哪些产品BOM引用？库存合计？

**SQL**:
```sql
SELECT DISTINCT b.parent_code, p.product_name, COALESCE(SUM(inv.quantity),0) as inv_qty FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id JOIN mysql_mhggp0vj."tem"."purchase_order_event" po2 ON su.supplier_id=po2.supplier_id JOIN mysql_mhggp0vj."tem"."bom_event" b ON po2.material_code=b.child_code JOIN mysql_mhggp0vj."tem"."product_entity" p ON b.parent_code=p.product_code LEFT JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON p.product_code=inv.item_code WHERE po.purchase_order_number='PO-2024040001' GROUP BY b.parent_code, p.product_name
```

**查询耗时**: 312ms | **返回行数**: 9

**数据**:
```json
[
  {
    "parent_code": "UAV-JF-ENT-SV",
    "product_name": "极风测绘版整机",
    "inv_qty": "19173"
  },
  {
    "parent_code": "UAV-JF-ENT-SC",
    "product_name": "极风安防版整机",
    "inv_qty": "11429"
  },
  {
    "product_name": "巡风探索版整机",
    "inv_qty": "47792",
    "parent_code": "UAV-XF-PRO-B"
  },
  {
    "product_name": "旋风基础版整机",
    "inv_qty": "6062",
    "parent_code": "UAV-XF-BASIC"
  },
  {
    "parent_code": "UAV-BF-IND-H30",
    "product_name": "霸风30L植保无人机",
    "inv_qty": "16270"
  },
  {
    "product_name": "霸风20L植保无人机",
    "inv_qty": "13310",
    "parent_code": "UAV-BF-IND-H20"
  },
  {
    "parent_code": "UAV-JF-ENT-AG",
    "product_name": "极风农业版整机",
    "inv_qty": "21740"
  },
  {
    "product_name": "旋风增强版整机",
    "inv_qty": "16928",
    "parent_code": "UAV-XF-BASIC-PLUS"
  },
  {
    "parent_code": "UAV-XF-PRO-A",
    "product_name": "巡风摄影版整机",
    "inv_qty": "14778"
  }
]
```

---

## Q24

**问题**: SH-202305-0002产品BOM物料采购供应商有高风险的吗？

**SQL**:
```sql
SELECT DISTINCT su.supplier_name, su.supplier_code, su.risk_level FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."bom_event" b ON sh.product_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id WHERE sh.shipment_number='SH-202305-0002' AND su.risk_level='高'
```

**查询耗时**: 314ms | **返回行数**: 0

**数据**: (无结果)

---

## Q25

**问题**: WH001存放产品BOM中有损耗物料的供应商风险等级分布？

**SQL**:
```sql
SELECT su.risk_level, COUNT(DISTINCT su.supplier_code) as cnt FROM mysql_mhggp0vj."tem"."inventory_event" inv JOIN mysql_mhggp0vj."tem"."bom_event" b ON inv.item_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id WHERE inv.warehouse_id IN (SELECT warehouse_id FROM mysql_mhggp0vj."tem"."warehouse_entity" WHERE warehouse_id='WH001') AND b.scrap_rate>0 GROUP BY su.risk_level
```

**查询耗时**: 293ms | **返回行数**: 2

**数据**:
```json
[
  {
    "risk_level": "中",
    "cnt": 1
  },
  {
    "risk_level": "低",
    "cnt": 5
  }
]
```

---


## 小结

- 成功查询: 18/25
- 查询出错或无结果: 7/25
