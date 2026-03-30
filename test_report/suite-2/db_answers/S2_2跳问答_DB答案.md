# S2 2跳问答 — 数据库查询答案

> 查询方式: kweaver dataview query (mdl-uniquery SQL)
> 测试时间: 2026-03-26 18:22:11

---

## Q01

**问题**: 采购订单PO-2024040001买的是什么物料？零件还是组件？

**SQL**:
```sql
SELECT po.purchase_order_number, po.material_code, po.material_name, m.material_type, m.is_assembly FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."material_entity" m ON po.material_code=m.material_code WHERE po.purchase_order_number='PO-2024040001'
```

**查询耗时**: 315ms | **返回行数**: 1

**数据**:
```json
[
  {
    "material_code": "PART-CAM-FIX-12MP",
    "material_name": "1200万像素固定相机",
    "material_type": "零件",
    "is_assembly": "否",
    "purchase_order_number": "PO-2024040001"
  }
]
```

---

## Q02

**问题**: 采购订单PO-2024040001的供应商交货周期一般是多久？

**SQL**:
```sql
SELECT po.purchase_order_number, po.supplier_name, su.lead_time_avg FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id WHERE po.purchase_order_number='PO-2024040001'
```

**查询耗时**: 286ms | **返回行数**: 1

**数据**:
```json
[
  {
    "purchase_order_number": "PO-2024040001",
    "supplier_name": "索尼半导体解决方案",
    "lead_time_avg": 60
  }
]
```

---

## Q03

**问题**: 采购订单PO-2024040001的供应商有没有供货风险？

**SQL**:
```sql
SELECT po.purchase_order_number, su.supplier_name, su.supplier_code, su.risk_level, su.supplier_tier FROM mysql_mhggp0vj."tem"."purchase_order_event" po JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON po.supplier_id=su.supplier_id WHERE po.purchase_order_number='PO-2024040001'
```

**查询耗时**: 297ms | **返回行数**: 1

**数据**:
```json
[
  {
    "supplier_code": "SUP-021",
    "risk_level": "低",
    "supplier_tier": "战略",
    "purchase_order_number": "PO-2024040001",
    "supplier_name": "索尼半导体解决方案"
  }
]
```

---

## Q04

**问题**: 销售订单SO-202303-00001卖的是哪款产品？还在产吗？

**SQL**:
```sql
SELECT so.sales_order_number, so.product_code, p.product_name, p.status FROM mysql_mhggp0vj."tem"."sales_order_event" so JOIN mysql_mhggp0vj."tem"."product_entity" p ON so.product_code=p.product_code WHERE so.sales_order_number='SO-202303-00001'
```

**查询耗时**: 288ms | **返回行数**: 3

**数据**:
```json
[
  {
    "sales_order_number": "SO-202303-00001",
    "product_code": "UAV-JF-ENT-AG",
    "product_name": "极风农业版整机",
    "status": "Active"
  },
  {
    "sales_order_number": "SO-202303-00001",
    "product_code": "UAV-BF-IND-H20",
    "product_name": "霸风20L植保无人机",
    "status": "Active"
  },
  {
    "product_name": "霸风30L植保无人机",
    "status": "Active",
    "sales_order_number": "SO-202303-00001",
    "product_code": "UAV-BF-IND-H30"
  }
]
```

---

## Q05

**问题**: 广州绿野农技是哪个级别的客户？SO-202303-00001是否加急？

**SQL**:
```sql
SELECT cu.customer_name, cu.customer_level, so.is_urgent, so.sales_order_number FROM mysql_mhggp0vj."tem"."customer_entity" cu JOIN mysql_mhggp0vj."tem"."sales_order_event" so ON cu.customer_id=so.customer_id WHERE cu.customer_name LIKE '%广州绿野%' AND so.sales_order_number='SO-202303-00001'
```

**查询耗时**: 316ms | **返回行数**: 3

**数据**:
```json
[
  {
    "is_urgent": "否",
    "sales_order_number": "SO-202303-00001",
    "customer_name": "广州绿野农技技术有限公司",
    "customer_level": "T3"
  },
  {
    "customer_name": "广州绿野农技技术有限公司",
    "customer_level": "T3",
    "is_urgent": "否",
    "sales_order_number": "SO-202303-00001"
  },
  {
    "customer_name": "广州绿野农技技术有限公司",
    "customer_level": "T3",
    "is_urgent": "否",
    "sales_order_number": "SO-202303-00001"
  }
]
```

---

## Q06

**问题**: 发货单SH-202305-0001发的是哪款产品？库存单价多少？

**SQL**:
```sql
SELECT sh.shipment_number, sh.product_code, sh.product_name, inv.unit_price FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."inventory_event" inv ON sh.product_code=inv.item_code WHERE sh.shipment_number='SH-202305-0001'
```

**查询耗时**: 285ms | **返回行数**: 1

**数据**:
```json
[
  {
    "shipment_number": "SH-202305-0001",
    "product_code": "UAV-XF-BASIC",
    "product_name": "旋风基础版整机",
    "unit_price": 38369.77
  }
]
```

---

## Q07

**问题**: 发货单SH-202305-0001从哪个仓库发出？有没有冷链？

**SQL**:
```sql
SELECT sh.shipment_number, sh.warehouse_name, wh.warehouse_code, wh.has_cold_storage FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON sh.warehouse_id=wh.warehouse_id WHERE sh.shipment_number='SH-202305-0001'
```

**查询耗时**: 284ms | **返回行数**: 1

**数据**:
```json
[
  {
    "has_cold_storage": "否",
    "shipment_number": "SH-202305-0001",
    "warehouse_name": "中央成品仓",
    "warehouse_code": "WH-华中-01"
  }
]
```

---

## Q08

**问题**: 生产工单MO-202305001在哪个工厂生产？多少员工？

**SQL**:
```sql
SELECT prd.production_order_number, fac.factory_name, fac.employee_count FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."factory_entity" fac ON prd.factory_id=fac.factory_id WHERE prd.production_order_number='MO-202305001'
```

**查询耗时**: 280ms | **返回行数**: 1

**数据**:
```json
[
  {
    "production_order_number": "MO-202305001",
    "factory_name": "深圳天翼无人机总装厂",
    "employee_count": 350
  }
]
```

---

## Q09

**问题**: 生产工单MO-202305001生产什么产品？BOM版本？

**SQL**:
```sql
SELECT DISTINCT prd.production_order_number, prd.output_code, prd.output_name, b.bom_version FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."bom_event" b ON prd.output_code=b.parent_code WHERE prd.production_order_number='MO-202305001'
```

**查询耗时**: 285ms | **返回行数**: 1

**数据**:
```json
[
  {
    "bom_version": "V2.0",
    "production_order_number": "MO-202305001",
    "output_code": "UAV-XF-BASIC",
    "output_name": "旋风基础版整机"
  }
]
```

---

## Q10

**问题**: 库存记录INV0000001存在哪个仓库？有没有自动化分拣？

**SQL**:
```sql
SELECT inv.inventory_id, inv.warehouse_name, wh.warehouse_code, wh.has_sorting_system FROM mysql_mhggp0vj."tem"."inventory_event" inv JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON inv.warehouse_id=wh.warehouse_id WHERE inv.inventory_id='INV0000001'
```

**查询耗时**: 344ms | **返回行数**: 1

**数据**:
```json
[
  {
    "warehouse_name": "中央成品仓",
    "warehouse_code": "WH-华中-01",
    "has_sorting_system": "是",
    "inventory_id": "INV0000001"
  }
]
```

---

## Q11

**问题**: 旋风基础版整机（UAV-XF-BASIC）目前的库存总价值？

**SQL**:
```sql
SELECT item_code, SUM(total_price) as total_value, SUM(quantity) as total_qty, unit_price FROM mysql_mhggp0vj."tem"."inventory_event" WHERE item_code='UAV-XF-BASIC' GROUP BY item_code, unit_price
```

**查询耗时**: 289ms | **返回行数**: 1

**数据**:
```json
[
  {
    "item_code": "UAV-XF-BASIC",
    "total_value": 33228222.98,
    "total_qty": "866",
    "unit_price": 38369.77
  }
]
```

---

## Q12

**问题**: 物料发货单PO-202303-961422是哪家供应商？几级？

**SQL**:
```sql
SELECT mp.procurement_number, mp.supplier_name, su.supplier_code, su.supplier_tier FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."supplier_entity" su ON mp.supplier_code=su.supplier_code WHERE mp.procurement_number='PO-202303-961422'
```

**查询耗时**: 287ms | **返回行数**: 1

**数据**:
```json
[
  {
    "procurement_number": "PO-202303-961422",
    "supplier_name": "北京智能视觉科技公司",
    "supplier_code": "SUP-035",
    "supplier_tier": "核心"
  }
]
```

---

## Q13

**问题**: 物料发货单PO-202303-961422入了哪个仓库？有RFID吗？

**SQL**:
```sql
SELECT mp.procurement_number, mp.warehouse_name, wh.warehouse_code, wh.has_rfid FROM mysql_mhggp0vj."tem"."material_procurement_event" mp JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON mp.warehouse_id=wh.warehouse_id WHERE mp.procurement_number='PO-202303-961422'
```

**查询耗时**: 294ms | **返回行数**: 1

**数据**:
```json
[
  {
    "warehouse_code": "WH-华南-02",
    "has_rfid": "是",
    "procurement_number": "PO-202303-961422",
    "warehouse_name": "电子材料仓"
  }
]
```

---

## Q14

**问题**: 领料单REQ-MO202305001-P0001-10从哪个仓库领料？面积多大？

**SQL**:
```sql
SELECT mr.requisition_number, mr.warehouse_name, wh.warehouse_code, wh.storage_area_sqm FROM mysql_mhggp0vj."tem"."material_requisition_event" mr JOIN mysql_mhggp0vj."tem"."warehouse_entity" wh ON mr.warehouse_id=wh.warehouse_id WHERE mr.requisition_number='REQ-MO202305001-P0001-10'
```

**查询耗时**: 285ms | **返回行数**: 1

**数据**:
```json
[
  {
    "requisition_number": "REQ-MO202305001-P0001-10",
    "warehouse_name": "深圳天翼中央成品仓库",
    "warehouse_code": "WH-华中-01",
    "storage_area_sqm": 20000
  }
]
```

---

## Q15

**问题**: 领料单REQ-MO202305001-P0001-10领的什么物料？是组件吗？

**SQL**:
```sql
SELECT mr.requisition_number, mr.material_name, m.material_code, m.is_assembly FROM mysql_mhggp0vj."tem"."material_requisition_event" mr JOIN mysql_mhggp0vj."tem"."material_entity" m ON mr.material_code=m.material_code WHERE mr.requisition_number='REQ-MO202305001-P0001-10'
```

**查询耗时**: 300ms | **返回行数**: 1

**数据**:
```json
[
  {
    "is_assembly": "是",
    "requisition_number": "REQ-MO202305001-P0001-10",
    "material_name": "入门塑料机身总成",
    "material_code": "ASSY-BODY-PLA-01"
  }
]
```

---

## Q16

**问题**: 领料单REQ-MO202305001-P0001-10给哪个工厂领料？什么类型？

**SQL**:
```sql
SELECT mr.requisition_number, mr.factory_name, fac.factory_code, fac.factory_type FROM mysql_mhggp0vj."tem"."material_requisition_event" mr JOIN mysql_mhggp0vj."tem"."factory_entity" fac ON mr.factory_id=fac.factory_id WHERE mr.requisition_number='REQ-MO202305001-P0001-10'
```

**查询耗时**: 286ms | **返回行数**: 1

**数据**:
```json
[
  {
    "requisition_number": "REQ-MO202305001-P0001-10",
    "factory_name": "深圳天翼无人机总装厂",
    "factory_code": "SZ-TIANYI-ASSY",
    "factory_type": "总装工厂"
  }
]
```

---

## Q17

**问题**: 旋风基础版整机（UAV-XF-BASIC）BOM V2.0用了哪些物料？

**SQL**:
```sql
SELECT child_code, child_name, quantity, scrap_rate, child_type FROM mysql_mhggp0vj."tem"."bom_event" WHERE parent_code='UAV-XF-BASIC' AND bom_version='V2.0'
```

**查询耗时**: 298ms | **返回行数**: 6

**数据**:
```json
[
  {
    "scrap_rate": 0,
    "child_type": "Material",
    "child_code": "ASSY-BODY-PLA-01",
    "child_name": "入门塑料机身总成",
    "quantity": 1
  },
  {
    "quantity": 1,
    "scrap_rate": 0,
    "child_type": "Material",
    "child_code": "ASSY-FC-BASIC",
    "child_name": "基础飞控总成"
  },
  {
    "quantity": 1,
    "scrap_rate": 0.01,
    "child_type": "Material",
    "child_code": "PART-CAM-FIX-12MP",
    "child_name": "1200万像素固定相机"
  },
  {
    "scrap_rate": 0,
    "child_type": "Material",
    "child_code": "ASSY-PWR-STD",
    "child_name": "标准动力系统总成",
    "quantity": 1
  },
  {
    "child_type": "Material",
    "child_code": "PART-BAT-2S-3000",
    "child_name": "标准智能电池2S3000mAh",
    "quantity": 1,
    "scrap_rate": 0.03
  },
  {
    "quantity": 1,
    "scrap_rate": 0.01,
    "child_type": "Material",
    "child_code": "PART-RC-BASIC",
    "child_name": "基础遥控器"
  }
]
```

---

## Q18

**问题**: 1200万像素固定相机（PART-CAM-FIX-12MP）被用在哪款产品上？

**SQL**:
```sql
SELECT b.parent_code, p.product_name, b.bom_version, b.quantity, b.scrap_rate FROM mysql_mhggp0vj."tem"."bom_event" b JOIN mysql_mhggp0vj."tem"."product_entity" p ON b.parent_code=p.product_code WHERE b.child_code='PART-CAM-FIX-12MP'
```

**查询耗时**: 281ms | **返回行数**: 1

**数据**:
```json
[
  {
    "quantity": 1,
    "scrap_rate": 0.01,
    "parent_code": "UAV-XF-BASIC",
    "product_name": "旋风基础版整机",
    "bom_version": "V2.0"
  }
]
```

---

## Q19

**问题**: 广州绿野SO-202303-00001总共花了多少钱？

**SQL**:
```sql
SELECT sales_order_number, line_number, product_code, total_amount, subtotal_amount FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE sales_order_number='SO-202303-00001'
```

**查询耗时**: 300ms | **返回行数**: 3

**数据**:
```json
[
  {
    "sales_order_number": "SO-202303-00001",
    "line_number": 10,
    "product_code": "UAV-JF-ENT-AG",
    "total_amount": 349155.33,
    "subtotal_amount": 308987.02
  },
  {
    "sales_order_number": "SO-202303-00001",
    "line_number": 20,
    "product_code": "UAV-BF-IND-H20",
    "total_amount": 483776.07,
    "subtotal_amount": 428120.42
  },
  {
    "product_code": "UAV-BF-IND-H30",
    "total_amount": 1108679.52,
    "subtotal_amount": 981132.32,
    "sales_order_number": "SO-202303-00001",
    "line_number": 30
  }
]
```

---

## Q20

**问题**: 旋风基础版整机（UAV-XF-BASIC）在中央成品仓什么时候入库的？

**SQL**:
```sql
SELECT item_code, warehouse_name, earliest_storage_date, batch_number FROM mysql_mhggp0vj."tem"."inventory_event" WHERE item_code='UAV-XF-BASIC' AND warehouse_name LIKE '%中央成品%'
```

**查询耗时**: 294ms | **返回行数**: 1

**数据**:
```json
[
  {
    "warehouse_name": "中央成品仓",
    "earliest_storage_date": "2023-04-30",
    "batch_number": "FG230501-001",
    "item_code": "UAV-XF-BASIC"
  }
]
```

---

## Q21

**问题**: 采购订单PO-2023040002的到货数量是多少？都入库了吗？

**SQL**:
```sql
SELECT purchase_order_number, purchase_quantity, accumulated_arrival_tax, accumulated_storage_tax, document_status FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2023040002'
```

**查询耗时**: 290ms | **返回行数**: 1

**数据**:
```json
[
  {
    "document_status": "已收货",
    "purchase_order_number": "PO-2023040002",
    "purchase_quantity": 3829,
    "accumulated_arrival_tax": 394673.22,
    "accumulated_storage_tax": 361703.69
  }
]
```

---

## Q22

**问题**: 发货单SH-202305-0003是发给哪个客户的？是重点客户吗？

**SQL**:
```sql
SELECT sh.shipment_number, sh.customer_name, cu.customer_code, cu.is_named_customer FROM mysql_mhggp0vj."tem"."shipment_event" sh JOIN mysql_mhggp0vj."tem"."customer_entity" cu ON sh.customer_code=cu.customer_code WHERE sh.shipment_number='SH-202305-0003'
```

**查询耗时**: 287ms | **返回行数**: 1

**数据**:
```json
[
  {
    "shipment_number": "SH-202305-0003",
    "customer_name": "青岛物流通配送集团有限公司",
    "customer_code": "CUST-10148",
    "is_named_customer": "否"
  }
]
```

---

## Q23

**问题**: 生产工单MO-202305002在哪条生产线？所在工厂总产能多少？

**SQL**:
```sql
SELECT prd.production_order_number, prd.production_line, fac.factory_name, fac.total_capacity FROM mysql_mhggp0vj."tem"."production_order_event" prd JOIN mysql_mhggp0vj."tem"."factory_entity" fac ON prd.factory_id=fac.factory_id WHERE prd.production_order_number='MO-202305002'
```

**查询耗时**: 286ms | **返回行数**: 1

**数据**:
```json
[
  {
    "factory_name": "深圳天翼无人机总装厂",
    "total_capacity": "50000台/年",
    "production_order_number": "MO-202305002",
    "production_line": "总装线A"
  }
]
```

---

## Q24

**问题**: 标准智能电池2S3000mAh（PART-BAT-2S-3000）在BOM中损耗率多少？

**SQL**:
```sql
SELECT parent_code, child_code, child_name, scrap_rate, bom_version FROM mysql_mhggp0vj."tem"."bom_event" WHERE child_code='PART-BAT-2S-3000'
```

**查询耗时**: 295ms | **返回行数**: 1

**数据**:
```json
[
  {
    "bom_version": "V2.0",
    "parent_code": "UAV-XF-BASIC",
    "child_code": "PART-BAT-2S-3000",
    "child_name": "标准智能电池2S3000mAh",
    "scrap_rate": 0.03
  }
]
```

---

## Q25

**问题**: 发货单SH-202305-0004的交付状态是什么？货到了吗？

**SQL**:
```sql
SELECT shipment_number, delivery_status, actual_delivery_date, customer_name FROM mysql_mhggp0vj."tem"."shipment_event" WHERE shipment_number='SH-202305-0004'
```

**查询耗时**: 298ms | **返回行数**: 1

**数据**:
```json
[
  {
    "shipment_number": "SH-202305-0004",
    "delivery_status": "已签收",
    "actual_delivery_date": "2023-05-23",
    "customer_name": "大连安控警用装备有限公司"
  }
]
```

---


## 小结

- 成功查询: 25/25
- 查询出错或无结果: 0/25
