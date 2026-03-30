# S3 3跳问答 — 数据库查询答案

> 查询方式: kweaver dataview query (mdl-uniquery SQL)
> 测试时间: 2026-03-26 18:30:20

---

## Q01

**问题**: SO-202303-00001的产品BOM中零件类子项？

**SQL**:
```sql
SELECT DISTINCT b.child_code, b.child_name, m.material_type, b.scrap_rate FROM mysql_mhggp0vj."tem"."sales_order_event" so JOIN mysql_mhggp0vj."tem"."bom_event" b ON so.product_code=b.parent_code JOIN mysql_mhggp0vj."tem"."material_entity" m ON b.child_code=m.material_code WHERE so.sales_order_number='SO-202303-00001' AND m.material_type='零件'
```

**查询耗时**: 293ms | **返回行数**: 13

**数据**:
```json
[
  {
    "child_code": "PART-RADAR-ALT",
    "child_name": "雷达测高仪",
    "material_type": "零件",
    "scrap_rate": 0.03
  },
  {
    "child_code": "PART-SPRAYER-16L",
    "child_name": "16升智能喷洒系统",
    "material_type": "零件",
    "scrap_rate": 0.03
  },
  {
    "child_code": "PART-RC-IND",
    "child_name": "工业遥控器",
    "material_type": "零件",
    "scrap_rate": 0.01
  },
  {
    "scrap_rate": 0.01,
    "child_code": "PART-CAM-FPV",
    "child_name": "FPV图传相机",
    "material_type": "零件"
  },
  {
    "material_type": "零件",
    "scrap_rate": 0.01,
    "child_code": "PART-SPRAYER-20L",
    "child_name": "20升智能喷洒系统"
  },
  {
    "scrap_rate": 0,
    "child_code": "PART-BAT-12S-16000",
    "child_name": "12S16000mAh工业电池",
    "material_type": "零件"
  },
  {
    "scrap_rate": 0.01,
    "child_code": "PART-FRAME-HEX-CF",
    "child_name": "六轴碳纤维机架",
    "material_type": "零件"
  },
  {
    "child_code": "PART-SPRAYER-30L",
    "child_name": "30升智能喷洒系统",
    "material_type": "零件",
    "scrap_rate": 0.02
  },
  {
    "child_code": "PART-BAT-12S-22000",
    "child_name": "12S22000mAh重载电池",
    "material_type": "零件",
    "scrap_rate": 0.02
  },
  {
    "child_code": "PART-PROP-3016-CF",
    "child_name": "3016碳纤螺旋桨",
    "material_type": "零件",
    "scrap_rate": 0.03
  },
  {
    "child_name": "60A电调",
    "material_type": "零件",
    "scrap_rate": 0,
    "child_code": "PART-ESC-60A"
  },
  {
    "child_name": "5010重载无刷电机",
    "material_type": "零件",
    "scrap_rate": 0.03,
    "child_code": "PART-MOTOR-5010-PRO"
  },
  {
    "material_type": "零件",
    "scrap_rate": 0,
    "child_code": "PART-FRAME-HEX-CF-HD",
    "child_name": "六轴重载碳纤维机架"
  }
]
```

---

## Q02

**问题**: SO-202303-00001产品BOM物料有在途采购订单吗？

**SQL**:
```sql
SELECT DISTINCT po.purchase_order_number, po.material_code, po.material_name, po.document_status FROM mysql_mhggp0vj."tem"."sales_order_event" so JOIN mysql_mhggp0vj."tem"."bom_event" b ON so.product_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code WHERE so.sales_order_number='SO-202303-00001' AND po.document_status!='已关闭'
```

**查询耗时**: 297ms | **返回行数**: 20

**数据**:
```json
[
  {
    "document_status": "已收货",
    "purchase_order_number": "PO-2023030046",
    "material_code": "PART-SPRAYER-16L",
    "material_name": "16升智能喷洒系统"
  },
  {
    "purchase_order_number": "PO-2023030098",
    "material_code": "PART-SPRAYER-30L",
    "material_name": "30升智能喷洒系统",
    "document_status": "已收货"
  },
  {
    "purchase_order_number": "PO-2023040082",
    "material_code": "PART-FRAME-HEX-CF",
    "material_name": "六轴碳纤维机架",
    "document_status": "已收货"
  },
  {
    "purchase_order_number": "PO-2023040084",
    "material_code": "PART-FRAME-HEX-CF",
    "material_name": "六轴碳纤维机架",
    "document_status": "已收货"
  },
  {
    "purchase_order_number": "PO-2023050040",
    "material_code": "PART-SPRAYER-16L",
    "material_name": "16升智能喷洒系统",
    "document_status": "已收货"
  },
  {
    "material_code": "PART-SPRAYER-16L",
    "material_name": "16升智能喷洒系统",
    "document_status": "已收货",
    "purchase_order_number": "PO-2023060044"
  },
  {
    "material_name": "30升智能喷洒系统",
    "document_status": "已收货",
    "purchase_order_number": "PO-2023060105",
    "material_code": "PART-SPRAYER-30L"
  },
  {
    "material_name": "20升智能喷洒系统",
    "document_status": "已收货",
    "purchase_order_number": "PO-2023080093",
    "material_code": "PART-SPRAYER-20L"
  },
  {
    "purchase_order_number": "PO-2023080094",
    "material_code": "PART-FRAME-HEX-CF-HD",
    "material_name": "六轴重载碳纤维机架",
    "document_status": "已收货"
  },
  {
    "purchase_order_number": "PO-2023100050",
    "material_code": "PART-RADAR-ALT",
    "material_name": "雷达测高仪",
    "document_status": "已收货"
  },
  {
    "purchase_order_number": "PO-2023120041",
    "material_code": "PART-SPRAYER-16L",
    "material_name": "16升智能喷洒系统",
    "document_status": "已收货"
  },
  {
    "material_name": "六轴碳纤维机架",
    "document_status": "已收货",
    "purchase_order_number": "PO-2023120085",
    "material_code": "PART-FRAME-HEX-CF"
  },
  {
    "material_name": "六轴碳纤维机架",
    "document_status": "已收货",
    "purchase_order_number": 
```

---

## Q03

**问题**: 发货单SH-202305-0001对应的销售订单客户等级？

**SQL**:
```sql
SELECT sh.shipment_number, sh.sales_order_number, cu.customer_name, cu.customer_level FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."customer_entity" cu ON sh.customer_code=cu.customer_code WHERE sh.shipment_number='SH-202305-0001'
```

**查询耗时**: 289ms | **返回行数**: 1

**数据**:
```json
[
  {
    "customer_level": "T3",
    "shipment_number": "SH-202305-0001",
    "sales_order_number": "SO-202305-6923",
    "customer_name": "南京云仓配送科技有限公司"
  }
]
```

---

## Q04

**问题**: UAV-XF-BASIC BOM物料中哪些当前有库存(quantity>0)？

**SQL**:
```sql
SELECT b.child_code, b.child_name, inv.warehouse_name, inv.quantity FROM mysql_mhggp0vj."tem"."bom_event" b JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON b.child_code=inv.item_code WHERE b.parent_code='UAV-XF-BASIC' AND inv.quantity>0
```

**查询耗时**: 282ms | **返回行数**: 9

**数据**:
```json
[
  {
    "child_code": "ASSY-BODY-PLA-01",
    "child_name": "入门塑料机身总成",
    "warehouse_name": "中央成品仓",
    "quantity": 151
  },
  {
    "warehouse_name": "中央成品仓",
    "quantity": 206,
    "child_code": "ASSY-FC-BASIC",
    "child_name": "基础飞控总成"
  },
  {
    "child_code": "ASSY-PWR-STD",
    "child_name": "标准动力系统总成",
    "warehouse_name": "中央成品仓",
    "quantity": 258
  },
  {
    "child_code": "ASSY-BODY-PLA-01",
    "child_name": "入门塑料机身总成",
    "warehouse_name": "电子材料仓",
    "quantity": 3370
  },
  {
    "child_code": "ASSY-FC-BASIC",
    "child_name": "基础飞控总成",
    "warehouse_name": "电子材料仓",
    "quantity": 3743
  },
  {
    "quantity": 821,
    "child_code": "PART-CAM-FIX-12MP",
    "child_name": "1200万像素固定相机",
    "warehouse_name": "电子材料仓"
  },
  {
    "warehouse_name": "电子材料仓",
    "quantity": 2881,
    "child_code": "ASSY-PWR-STD",
    "child_name": "标准动力系统总成"
  },
  {
    "child_code": "PART-BAT-2S-3000",
    "child_name": "标准智能电池2S3000mAh",
    "warehouse_name": "配件仓",
    "quantity": 1080
  },
  {
    "child_code": "PART-RC-BASIC",
    "child_name": "基础遥控器",
    "warehouse_name": "配件仓",
    "quantity": 4380
  }
]
```

---

## Q05

**问题**: PART-CAM-FIX-12MP采购订单有没有交期延误？

**SQL**:
```sql
SELECT purchase_order_number, planned_arrival_date, required_date FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE material_code='PART-CAM-FIX-12MP'
```

**查询耗时**: 288ms | **返回行数**: 7

**数据**:
```json
[
  {
    "purchase_order_number": "PO-2023010007",
    "planned_arrival_date": "2023-03-14",
    "required_date": "2023-03-20"
  },
  {
    "purchase_order_number": "PO-2023020004",
    "planned_arrival_date": "2023-04-29",
    "required_date": "2023-05-05"
  },
  {
    "purchase_order_number": "PO-2023040002",
    "planned_arrival_date": "2023-06-06",
    "required_date": "2023-06-22"
  },
  {
    "purchase_order_number": "PO-2023090006",
    "planned_arrival_date": "2023-11-23",
    "required_date": "2023-12-08"
  },
  {
    "planned_arrival_date": "2024-06-05",
    "required_date": "2024-06-10",
    "purchase_order_number": "PO-2024040001"
  },
  {
    "planned_arrival_date": "2024-06-13",
    "required_date": "2024-06-20",
    "purchase_order_number": "PO-2024040003"
  },
  {
    "purchase_order_number": "PO-2024110005",
    "planned_arrival_date": "2025-01-23",
    "required_date": "2025-01-27"
  }
]
```

---

## Q06

**问题**: MO-202305001领料物料从哪些仓库出库？有自动分拣吗？

**SQL**:
```sql
SELECT DISTINCT mr.warehouse_name, wh.warehouse_code, wh.has_sorting_system FROM mysql_mhggp0vj."tem"."material_requisition_event" mr JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON mr.warehouse_id=wh.warehouse_id WHERE mr.production_order_number='MO-202305001'
```

**查询耗时**: 306ms | **返回行数**: 3

**数据**:
```json
[
  {
    "warehouse_name": "深圳天翼中央成品仓库",
    "warehouse_code": "WH-华中-01",
    "has_sorting_system": "是"
  },
  {
    "warehouse_name": "深圳天翼配件仓库",
    "warehouse_code": "WH-华中-03",
    "has_sorting_system": "否"
  },
  {
    "has_sorting_system": "否",
    "warehouse_name": "深圳天翼电子材料仓库",
    "warehouse_code": "WH-华南-02"
  }
]
```

---

## Q07

**问题**: ASSY-BODY-PLA-01的供应商有高风险的吗？

**SQL**:
```sql
SELECT DISTINCT mp.supplier_name, su.supplier_code, su.risk_level FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON mp.supplier_code=su.supplier_code WHERE mp.material_code='ASSY-BODY-PLA-01'
```

**查询耗时**: 278ms | **返回行数**: 1

**数据**:
```json
[
  {
    "supplier_code": "SUP-035",
    "risk_level": "中",
    "supplier_name": "北京智能视觉科技公司"
  }
]
```

---

## Q08

**问题**: 广州绿野农技的订单发货用了哪些物流商？

**SQL**:
```sql
SELECT DISTINCT sh.logistics_provider FROM mysql_mhggp0vj."tem"."shipment_event" sh WHERE sh.customer_name LIKE '%广州绿野%'
```

**查询耗时**: 297ms | **返回行数**: 1

**数据**:
```json
[
  {
    "logistics_provider": "京东物流"
  }
]
```

---

## Q09

**问题**: UAV-XF-BASIC库存在哪些仓库？仓库负责人？

**SQL**:
```sql
SELECT DISTINCT inv.warehouse_name, wh.warehouse_code, wh.manager_name FROM mysql_mhggp0vj."tem"."inventory_event" inv JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON inv.warehouse_id=wh.warehouse_id WHERE inv.item_code='UAV-XF-BASIC'
```

**查询耗时**: 281ms | **返回行数**: 1

**数据**:
```json
[
  {
    "warehouse_name": "中央成品仓",
    "warehouse_code": "WH-华中-01",
    "manager_name": "张建国"
  }
]
```

---

## Q10

**问题**: SUP-021的货发到了哪些仓库？什么类型？

**SQL**:
```sql
SELECT DISTINCT mp.warehouse_name, wh.warehouse_code, wh.warehouse_type FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON mp.warehouse_id=wh.warehouse_id WHERE mp.supplier_code='SUP-021'
```

**查询耗时**: 293ms | **返回行数**: 1

**数据**:
```json
[
  {
    "warehouse_name": "电子材料仓",
    "warehouse_code": "WH-华南-02",
    "warehouse_type": "原材料仓"
  }
]
```

---

## Q11

**问题**: FAC001生产的产品里哪些库存超过1000台？

**SQL**:
```sql
SELECT prd.output_code, prd.output_name, SUM(inv.quantity) as total_qty FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON prd.output_code=inv.item_code WHERE prd.factory_id IN (SELECT factory_id FROM mysql_mhggp0vj."tem"."factory_entity" WHERE factory_id='FAC001') GROUP BY prd.output_code, prd.output_name HAVING SUM(inv.quantity)>1000
```

**查询耗时**: 290ms | **返回行数**: 9

**数据**:
```json
[
  {
    "output_name": "旋风增强版整机",
    "total_qty": "4232",
    "output_code": "UAV-XF-BASIC-PLUS"
  },
  {
    "total_qty": "4926",
    "output_code": "UAV-XF-PRO-A",
    "output_name": "巡风摄影版整机"
  },
  {
    "output_name": "巡风探索版整机",
    "total_qty": "5974",
    "output_code": "UAV-XF-PRO-B"
  },
  {
    "total_qty": "3035",
    "output_code": "UAV-XF-PRO-C",
    "output_name": "巡风全能版整机"
  },
  {
    "total_qty": "4348",
    "output_code": "UAV-JF-ENT-AG",
    "output_name": "极风农业版整机"
  },
  {
    "output_name": "极风测绘版整机",
    "total_qty": "2739",
    "output_code": "UAV-JF-ENT-SV"
  },
  {
    "output_code": "UAV-JF-ENT-SC",
    "output_name": "极风安防版整机",
    "total_qty": "1039"
  },
  {
    "output_code": "UAV-BF-IND-H20",
    "output_name": "霸风20L植保无人机",
    "total_qty": "2662"
  },
  {
    "output_code": "UAV-BF-IND-H30",
    "output_name": "霸风30L植保无人机",
    "total_qty": "3254"
  }
]
```

---

## Q12

**问题**: 领料单REQ-MO202305001-P0001-30物料的采购供应商？

**SQL**:
```sql
SELECT mr.material_code, mr.material_name, po.purchase_order_number, po.supplier_name FROM mysql_mhggp0vj."tem"."material_requisition_event" mr JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON mr.material_code=po.material_code WHERE mr.requisition_number='REQ-MO202305001-P0001-30'
```

**查询耗时**: 275ms | **返回行数**: 7

**数据**:
```json
[
  {
    "material_name": "1200万像素固定相机",
    "purchase_order_number": "PO-2023010007",
    "supplier_name": "索尼半导体解决方案",
    "material_code": "PART-CAM-FIX-12MP"
  },
  {
    "material_name": "1200万像素固定相机",
    "purchase_order_number": "PO-2023020004",
    "supplier_name": "索尼半导体解决方案",
    "material_code": "PART-CAM-FIX-12MP"
  },
  {
    "material_code": "PART-CAM-FIX-12MP",
    "material_name": "1200万像素固定相机",
    "purchase_order_number": "PO-2023040002",
    "supplier_name": "索尼半导体解决方案"
  },
  {
    "material_code": "PART-CAM-FIX-12MP",
    "material_name": "1200万像素固定相机",
    "purchase_order_number": "PO-2023090006",
    "supplier_name": "索尼半导体解决方案"
  },
  {
    "material_code": "PART-CAM-FIX-12MP",
    "material_name": "1200万像素固定相机",
    "purchase_order_number": "PO-2024040001",
    "supplier_name": "索尼半导体解决方案"
  },
  {
    "supplier_name": "索尼半导体解决方案",
    "material_code": "PART-CAM-FIX-12MP",
    "material_name": "1200万像素固定相机",
    "purchase_order_number": "PO-2024040003"
  },
  {
    "material_name": "1200万像素固定相机",
    "purchase_order_number": "PO-2024110005",
    "supplier_name": "索尼半导体解决方案",
    "material_code": "PART-CAM-FIX-12MP"
  }
]
```

---

## Q13

**问题**: PART-CAM-FIX-12MP来料验收状态分布？

**SQL**:
```sql
SELECT inspection_status, COUNT(*) as cnt FROM mysql_mhggp0vj."tem"."material_procurement_event" WHERE material_code='PART-CAM-FIX-12MP' GROUP BY inspection_status
```

**查询耗时**: 281ms | **返回行数**: 3

**数据**:
```json
[
  {
    "inspection_status": "待验收",
    "cnt": 1
  },
  {
    "inspection_status": "验收中",
    "cnt": 1
  },
  {
    "inspection_status": "已验收",
    "cnt": 1
  }
]
```

---

## Q14

**问题**: UAV-BF-IND-H30在哪个工厂生产？工厂认证？

**SQL**:
```sql
SELECT DISTINCT prd.output_code, fac.factory_name, fac.factory_code, fac.certification FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."factory_entity" fac ON prd.factory_id=fac.factory_id WHERE prd.output_code='UAV-BF-IND-H30'
```

**查询耗时**: 298ms | **返回行数**: 1

**数据**:
```json
[
  {
    "output_code": "UAV-BF-IND-H30",
    "factory_name": "深圳天翼无人机总装厂",
    "factory_code": "SZ-TIANYI-ASSY",
    "certification": "ISO9001,ISO14001"
  }
]
```

---

## Q15

**问题**: 西安沃土（CUST-10002）有没有运输中的发货单？

**SQL**:
```sql
SELECT sh.shipment_number, sh.delivery_status, sh.product_name FROM mysql_mhggp0vj."tem"."shipment_event" sh WHERE sh.customer_code='CUST-10002' AND sh.delivery_status='运输中'
```

**查询耗时**: 288ms | **返回行数**: 1

**数据**:
```json
[
  {
    "shipment_number": "SH-202305-0006",
    "delivery_status": "运输中",
    "product_name": "旋风基础版整机"
  }
]
```

---

## Q16

**问题**: PART-BAT-2S-3000用在哪些产品上？库存总量？

**SQL**:
```sql
SELECT b.parent_code, p.product_name, SUM(inv.quantity) as total_qty FROM mysql_mhggp0vj."tem"."bom_event" b JOIN mysql_mhggp0vj."tem"."product_entity" p ON b.parent_code=p.product_code LEFT JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON p.product_code=inv.item_code WHERE b.child_code='PART-BAT-2S-3000' GROUP BY b.parent_code, p.product_name
```

**查询耗时**: 289ms | **返回行数**: 1

**数据**:
```json
[
  {
    "product_name": "旋风基础版整机",
    "total_qty": "866",
    "parent_code": "UAV-XF-BASIC"
  }
]
```

---

## Q17

**问题**: CUST-10148历史所有订单总金额？

**SQL**:
```sql
SELECT SUM(total_amount) as grand_total, COUNT(*) as order_count FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE customer_id IN (SELECT customer_id FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_code='CUST-10148')
```

**查询耗时**: 290ms | **返回行数**: 1

**数据**:
```json
[
  {
    "grand_total": null,
    "order_count": 0
  }
]
```

---

## Q18

**问题**: PO-2024110005采购物料被用在哪些产品上？产品类型？

**SQL**:
```sql
SELECT DISTINCT b.parent_code, p.product_name, p.product_type FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."bom_event" b ON po.material_code=b.child_code JOIN mysql_mhggp0vj."tem"."product_entity" p ON b.parent_code=p.product_code WHERE po.purchase_order_number='PO-2024110005'
```

**查询耗时**: 300ms | **返回行数**: 1

**数据**:
```json
[
  {
    "product_type": "UAV",
    "parent_code": "UAV-XF-BASIC",
    "product_name": "旋风基础版整机"
  }
]
```

---

## Q19

**问题**: UAV-XF-BASIC-PLUS的发货单有多少已签收？

**SQL**:
```sql
SELECT delivery_status, COUNT(*) as cnt FROM mysql_mhggp0vj."tem"."shipment_event" WHERE product_code='UAV-XF-BASIC-PLUS' GROUP BY delivery_status
```

**查询耗时**: 292ms | **返回行数**: 3

**数据**:
```json
[
  {
    "delivery_status": "已签收",
    "cnt": 3
  },
  {
    "cnt": 2,
    "delivery_status": "运输中"
  },
  {
    "delivery_status": "已发货",
    "cnt": 1
  }
]
```

---

## Q20

**问题**: WH002收到的物料有没有采购风险高的？

**SQL**:
```sql
SELECT DISTINCT mp.material_code, mp.material_name, su.supplier_name, su.risk_level FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON mp.supplier_code=su.supplier_code WHERE mp.warehouse_id IN (SELECT warehouse_id FROM mysql_mhggp0vj."tem"."warehouse_entity" WHERE warehouse_id='WH002')
```

**查询耗时**: 296ms | **返回行数**: 50

**数据**:
```json
[
  {
    "risk_level": "中",
    "material_code": "PART-MCU-STM32H743",
    "material_name": "STM32H743高性能芯片",
    "supplier_name": "芯源微电子股份有限公司"
  },
  {
    "material_code": "PART-MCU-STM32F103",
    "material_name": "STM32F103控制芯片",
    "supplier_name": "德州仪器（TI）中国代理",
    "risk_level": "低"
  },
  {
    "risk_level": "低",
    "material_code": "PART-POWER-REG-3.3V",
    "material_name": "3.3V稳压芯片",
    "supplier_name": "德州仪器（TI）中国代理"
  },
  {
    "risk_level": "低",
    "material_code": "COMP-FC-CASE-AL",
    "material_name": "飞控铝合金外壳",
    "supplier_name": "德州仪器（TI）中国代理"
  },
  {
    "risk_level": "低",
    "material_code": "PART-MCU-STM32H753",
    "material_name": "STM32H753双核芯片",
    "supplier_name": "德州仪器（TI）中国代理"
  },
  {
    "supplier_name": "德州仪器（TI）中国代理",
    "risk_level": "低",
    "material_code": "PART-MCU-STM32F427",
    "material_name": "STM32F427主控芯片"
  },
  {
    "risk_level": "低",
    "material_code": "PART-POWER-REG-5V-3A",
    "material_name": "5V 3A稳压模块",
    "supplier_name": "德州仪器（TI）中国代理"
  },
  {
    "material_name": "5V稳压芯片",
    "supplier_name": "意法半导体（ST）亚太区",
    "risk_level": "中",
    "material_code": "PART-POWER-REG-5V"
  },
  {
    "material_code": "ASSY-PWR-STD",
    "material_name": "标准动力系统总成",
    "supplier_name": "意法半导体（ST）亚太区",
    "risk_level": "中"
  },
  {
    "risk_level": "中",
    "material_code": "PART-CRYSTAL-32K",
    "material_name": "32.768KHz晶振",
    "supplier_name": "意法半导体（ST）亚太区"
  },
  {
    "supplier_name": "博世传感器技术有限公司",
    "risk_level": "低",
    "material_code": "PART-BARO-DPS310",
    "material_name": "DPS310高精度气压计"
  },
  {
    "supplier_name": "深圳矽递科技有限公司",
    "risk_level": "中",
    "material_code": "PART-IMU-ADIS16505",
    "material_name": "ADIS16505工业级IMU"
  },
  {
    "material_name": "MPU6050六轴传感器",
    "supplier_name": "深圳矽递科技有限公司",
    "risk_level": "中",
    "material_code": "PART-IMU-MPU6050"
  },
  {
    "material_code": "COMP-ARM-CF-TUBE-HD",
    "material_name": "加强型碳纤维机臂",
    "supplier_name": "深圳矽递科
```

---

## Q21

**问题**: SUP-004供的物料被用在哪些产品BOM里？有库存吗？

**SQL**:
```sql
SELECT DISTINCT po.material_code, b.parent_code, p.product_name, COALESCE(inv.quantity, 0) as inv_qty FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."bom_event" b ON po.material_code=b.child_code JOIN mysql_mhggp0vj."tem"."product_entity" p ON b.parent_code=p.product_code LEFT JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON p.product_code=inv.item_code WHERE po.supplier_id IN (SELECT supplier_id FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_code='SUP-004')
```

**查询耗时**: 293ms | **返回行数**: 0

**数据**: (无结果)

---

## Q22

**问题**: SH-202305-0003收货方还有哪些未发货订单？

**SQL**:
```sql
SELECT so.sales_order_number, so.product_code, so.order_status FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."sales_order_event" so ON sh.customer_code IN (SELECT customer_code FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_id=so.customer_id) WHERE sh.shipment_number='SH-202305-0003' AND so.order_status!='已发货'
```

**查询耗时**: 314ms | **返回行数**: 0

**数据**: (无结果)

---

## Q23

**问题**: MO-202305003产品BOM物料采购总金额？

**SQL**:
```sql
SELECT SUM(po.total_amount_tax) as total_purchase FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."bom_event" b ON prd.output_code=b.parent_code JOIN mysql_mhggp0vj."tem"."purchase_order_event" po ON b.child_code=po.material_code WHERE prd.production_order_number='MO-202305003'
```

**查询耗时**: 304ms | **返回行数**: 1

**数据**:
```json
[
  {
    "total_purchase": 8910122.96
  }
]
```

---

## Q24

**问题**: WH001里的产品有哪些还有未完成的销售订单？

**SQL**:
```sql
SELECT DISTINCT inv.item_code, inv.item_name, so.sales_order_number, so.order_status FROM mysql_mhggp0vj."tem"."inventory_event" inv JOIN mysql_mhggp0vj."tem"."sales_order_event" so ON inv.item_code=so.product_code WHERE inv.warehouse_id IN (SELECT warehouse_id FROM mysql_mhggp0vj."tem"."warehouse_entity" WHERE warehouse_id='WH001') AND so.order_status!='已发货'
```

**查询耗时**: 295ms | **返回行数**: 50

**数据**:
```json
[
  {
    "order_status": "已取消",
    "item_code": "UAV-JF-ENT-AG",
    "item_name": "极风农业版整机",
    "sales_order_number": "SO-202404-00004"
  },
  {
    "sales_order_number": "SO-202303-00010",
    "order_status": "已取消",
    "item_code": "UAV-BF-IND-H20",
    "item_name": "霸风20L植保无人机"
  },
  {
    "item_code": "UAV-JF-ENT-AG",
    "item_name": "极风农业版整机",
    "sales_order_number": "SO-202303-00010",
    "order_status": "已取消"
  },
  {
    "item_code": "UAV-BF-IND-H30",
    "item_name": "霸风30L植保无人机",
    "sales_order_number": "SO-202303-00010",
    "order_status": "已取消"
  },
  {
    "sales_order_number": "SO-202303-00017",
    "order_status": "已取消",
    "item_code": "UAV-BF-IND-H30",
    "item_name": "霸风30L植保无人机"
  },
  {
    "order_status": "已取消",
    "item_code": "UAV-BF-IND-H20",
    "item_name": "霸风20L植保无人机",
    "sales_order_number": "SO-202303-00017"
  },
  {
    "item_code": "UAV-JF-ENT-AG",
    "item_name": "极风农业版整机",
    "sales_order_number": "SO-202303-00017",
    "order_status": "已取消"
  },
  {
    "order_status": "已取消",
    "item_code": "UAV-JF-ENT-AG",
    "item_name": "极风农业版整机",
    "sales_order_number": "SO-202303-00043"
  },
  {
    "sales_order_number": "SO-202303-00043",
    "order_status": "已取消",
    "item_code": "UAV-BF-IND-H30",
    "item_name": "霸风30L植保无人机"
  },
  {
    "order_status": "已取消",
    "item_code": "UAV-BF-IND-H30",
    "item_name": "霸风30L植保无人机",
    "sales_order_number": "SO-202304-00081"
  },
  {
    "item_name": "霸风20L植保无人机",
    "sales_order_number": "SO-202304-00081",
    "order_status": "已取消",
    "item_code": "UAV-BF-IND-H20"
  },
  {
    "item_code": "UAV-BF-IND-H20",
    "item_name": "霸风20L植保无人机",
    "sales_order_number": "SO-202404-00102",
    "order_status": "已取消"
  },
  {
    "item_name": "霸风30L植保无人机",
    "sales_order_number": "SO-202404-00102",
    "order_status": "已取消",
    "item_code": "UAV-BF-IND-H30"
  },
  {
    "item_code": "UAV-JF-ENT-AG",
    "item_name": "极风农业版整机",
    "sales_order_number": "SO-202309-00154",
    "
```

---

## Q25

**问题**: UAV-XF-BASIC BOM中损耗率>0的物料库存够几台？

**SQL**:
```sql
SELECT b.child_code, b.child_name, b.scrap_rate, b.quantity as qty_per, COALESCE(SUM(inv.quantity), 0) as total_inv FROM mysql_mhggp0vj."tem"."bom_event" b LEFT JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON b.child_code=inv.item_code WHERE b.parent_code='UAV-XF-BASIC' AND b.scrap_rate>0 GROUP BY b.child_code, b.child_name, b.scrap_rate, b.quantity
```

**查询耗时**: 289ms | **返回行数**: 3

**数据**:
```json
[
  {
    "child_code": "PART-CAM-FIX-12MP",
    "child_name": "1200万像素固定相机",
    "scrap_rate": 0.01,
    "qty_per": 1,
    "total_inv": "821"
  },
  {
    "scrap_rate": 0.03,
    "qty_per": 1,
    "total_inv": "1080",
    "child_code": "PART-BAT-2S-3000",
    "child_name": "标准智能电池2S3000mAh"
  },
  {
    "qty_per": 1,
    "total_inv": "4380",
    "child_code": "PART-RC-BASIC",
    "child_name": "基础遥控器",
    "scrap_rate": 0.01
  }
]
```

---


## 小结

- 成功查询: 23/25
- 查询出错或无结果: 2/25
