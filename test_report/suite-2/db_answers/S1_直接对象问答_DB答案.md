# S1 直接对象问答 — 数据库查询答案

> 查询方式: kweaver dataview query (mdl-uniquery SQL)
> 测试时间: 2026-03-26 18:28:48

---

## Q01

**问题**: 旋风基础版整机（UAV-XF-BASIC）目前在中央成品仓的库存有多少台？

**SQL**:
```sql
SELECT quantity, warehouse_name, snapshot_month FROM mysql_mhggp0vj."tem"."inventory_event" WHERE item_code='UAV-XF-BASIC' AND warehouse_name LIKE '%中央成品%'
```

**查询耗时**: 290ms | **返回行数**: 1

**数据**:
```json
[
  {
    "quantity": 866,
    "warehouse_name": "中央成品仓",
    "snapshot_month": "2023-05"
  }
]
```

---

## Q02

**问题**: 采购订单PO-2024040001预计什么时候到货？

**SQL**:
```sql
SELECT purchase_order_number, planned_arrival_date FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2024040001'
```

**查询耗时**: 293ms | **返回行数**: 1

**数据**:
```json
[
  {
    "planned_arrival_date": "2024-06-05",
    "purchase_order_number": "PO-2024040001"
  }
]
```

---

## Q03

**问题**: 发货单SH-202305-0001预计什么时候送达客户？

**SQL**:
```sql
SELECT shipment_number, estimated_delivery_date FROM mysql_mhggp0vj."tem"."shipment_event" WHERE shipment_number='SH-202305-0001'
```

**查询耗时**: 295ms | **返回行数**: 1

**数据**:
```json
[
  {
    "shipment_number": "SH-202305-0001",
    "estimated_delivery_date": "2023-05-30"
  }
]
```

---

## Q04

**问题**: 发货单SH-202305-0002最终实际是哪天签收的？

**SQL**:
```sql
SELECT shipment_number, actual_delivery_date FROM mysql_mhggp0vj."tem"."shipment_event" WHERE shipment_number='SH-202305-0002'
```

**查询耗时**: 299ms | **返回行数**: 1

**数据**:
```json
[
  {
    "shipment_number": "SH-202305-0002",
    "actual_delivery_date": "2023-05-28"
  }
]
```

---

## Q05

**问题**: 广州绿野农技技术有限公司的销售订单SO-202303-00001当前处于什么状态？

**SQL**:
```sql
SELECT sales_order_number, order_status, customer_name FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE sales_order_number='SO-202303-00001'
```

**查询耗时**: 294ms | **返回行数**: 3

**数据**:
```json
[
  {
    "sales_order_number": "SO-202303-00001",
    "order_status": "已发货",
    "customer_name": "广州绿野农技技术有限公司"
  },
  {
    "sales_order_number": "SO-202303-00001",
    "order_status": "已发货",
    "customer_name": "广州绿野农技技术有限公司"
  },
  {
    "customer_name": "广州绿野农技技术有限公司",
    "sales_order_number": "SO-202303-00001",
    "order_status": "已发货"
  }
]
```

---

## Q06

**问题**: 广州绿野农技技术有限公司这个客户是我们的重点客户吗？

**SQL**:
```sql
SELECT customer_code, customer_name, is_named_customer FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_name LIKE '%广州绿野%'
```

**查询耗时**: 285ms | **返回行数**: 1

**数据**:
```json
[
  {
    "customer_code": "CUST-10001",
    "customer_name": "广州绿野农技技术有限公司",
    "is_named_customer": "否"
  }
]
```

---

## Q07

**问题**: 西安沃土植保科技有限公司和我们签合同了吗？

**SQL**:
```sql
SELECT customer_code, customer_name, has_contract FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_name LIKE '%西安沃土%'
```

**查询耗时**: 315ms | **返回行数**: 1

**数据**:
```json
[
  {
    "customer_code": "CUST-10002",
    "customer_name": "西安沃土植保科技有限公司",
    "has_contract": "是"
  }
]
```

---

## Q08

**问题**: 索尼半导体解决方案这家供应商的采购风险评级是多少？

**SQL**:
```sql
SELECT supplier_code, supplier_name, risk_level FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_name LIKE '%索尼%'
```

**查询耗时**: 297ms | **返回行数**: 1

**数据**:
```json
[
  {
    "supplier_code": "SUP-021",
    "supplier_name": "索尼半导体解决方案",
    "risk_level": "低"
  }
]
```

---

## Q09

**问题**: 博世传感器技术有限公司的货一般要等多少天才能到？

**SQL**:
```sql
SELECT supplier_code, supplier_name, lead_time_avg FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_name LIKE '%博世%'
```

**查询耗时**: 289ms | **返回行数**: 1

**数据**:
```json
[
  {
    "lead_time_avg": 45,
    "supplier_code": "SUP-004",
    "supplier_name": "博世传感器技术有限公司"
  }
]
```

---

## Q10

**问题**: 芯源微电子股份有限公司的付款条件是什么？

**SQL**:
```sql
SELECT supplier_code, supplier_name, payment_terms FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_name LIKE '%芯源%'
```

**查询耗时**: 290ms | **返回行数**: 1

**数据**:
```json
[
  {
    "supplier_code": "SUP-001",
    "supplier_name": "芯源微电子股份有限公司",
    "payment_terms": "月结60天"
  }
]
```

---

## Q11

**问题**: 生产工单MO-202305001计划什么时候完工？

**SQL**:
```sql
SELECT production_order_number, planned_finish_date, production_order_id FROM mysql_mhggp0vj."tem"."production_order_event" WHERE production_order_number='MO-202305001'
```

**查询耗时**: 307ms | **返回行数**: 1

**数据**:
```json
[
  {
    "production_order_number": "MO-202305001",
    "planned_finish_date": "2023-05-19",
    "production_order_id": "PO0000007"
  }
]
```

---

## Q12

**问题**: 生产工单MO-202305001目前的工单状态是什么？

**SQL**:
```sql
SELECT production_order_number, work_order_status FROM mysql_mhggp0vj."tem"."production_order_event" WHERE production_order_number='MO-202305001'
```

**查询耗时**: 296ms | **返回行数**: 1

**数据**:
```json
[
  {
    "production_order_number": "MO-202305001",
    "work_order_status": "已完工"
  }
]
```

---

## Q13

**问题**: 采购订单PO-2024040001这笔单子含税总金额是多少？

**SQL**:
```sql
SELECT purchase_order_number, total_amount_tax, purchase_quantity, unit_price_tax FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2024040001'
```

**查询耗时**: 282ms | **返回行数**: 1

**数据**:
```json
[
  {
    "unit_price_tax": 99.28,
    "purchase_order_number": "PO-2024040001",
    "total_amount_tax": 198857.84,
    "purchase_quantity": 2003
  }
]
```

---

## Q14

**问题**: 采购订单PO-2023040002是谁负责跟进的？

**SQL**:
```sql
SELECT purchase_order_number, buyer FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2023040002'
```

**查询耗时**: 283ms | **返回行数**: 1

**数据**:
```json
[
  {
    "purchase_order_number": "PO-2023040002",
    "buyer": "赵六"
  }
]
```

---

## Q15

**问题**: 采购订单PO-2024040001目前单据状态是什么？

**SQL**:
```sql
SELECT purchase_order_number, document_status FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2024040001'
```

**查询耗时**: 286ms | **返回行数**: 1

**数据**:
```json
[
  {
    "purchase_order_number": "PO-2024040001",
    "document_status": "已关闭"
  }
]
```

---

## Q16

**问题**: 销售订单SO-202303-00001给客户的折扣是多少？

**SQL**:
```sql
SELECT sales_order_number, line_number, product_code, discount_rate FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE sales_order_number='SO-202303-00001'
```

**查询耗时**: 296ms | **返回行数**: 3

**数据**:
```json
[
  {
    "sales_order_number": "SO-202303-00001",
    "line_number": 10,
    "product_code": "UAV-JF-ENT-AG",
    "discount_rate": "4.0%"
  },
  {
    "product_code": "UAV-BF-IND-H20",
    "discount_rate": "6.9%",
    "sales_order_number": "SO-202303-00001",
    "line_number": 20
  },
  {
    "product_code": "UAV-BF-IND-H30",
    "discount_rate": "7.6%",
    "sales_order_number": "SO-202303-00001",
    "line_number": 30
  }
]
```

---

## Q17

**问题**: 销售订单SO-202303-00001承诺的交货日期是哪天？

**SQL**:
```sql
SELECT sales_order_number, line_number, planned_delivery_date FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE sales_order_number='SO-202303-00001'
```

**查询耗时**: 287ms | **返回行数**: 3

**数据**:
```json
[
  {
    "sales_order_number": "SO-202303-00001",
    "line_number": 10,
    "planned_delivery_date": "2023-05-12"
  },
  {
    "line_number": 20,
    "planned_delivery_date": "2023-05-16",
    "sales_order_number": "SO-202303-00001"
  },
  {
    "line_number": 30,
    "planned_delivery_date": "2023-04-13",
    "sales_order_number": "SO-202303-00001"
  }
]
```

---

## Q18

**问题**: 发货单SH-202305-0001用的是哪家物流？

**SQL**:
```sql
SELECT shipment_number, logistics_provider FROM mysql_mhggp0vj."tem"."shipment_event" WHERE shipment_number='SH-202305-0001'
```

**查询耗时**: 296ms | **返回行数**: 1

**数据**:
```json
[
  {
    "shipment_number": "SH-202305-0001",
    "logistics_provider": "百世快递"
  }
]
```

---

## Q19

**问题**: 物料发货单PO-202303-961422的验收结果是什么？

**SQL**:
```sql
SELECT procurement_number, inspection_status FROM mysql_mhggp0vj."tem"."material_procurement_event" WHERE procurement_number='PO-202303-961422'
```

**查询耗时**: 296ms | **返回行数**: 1

**数据**:
```json
[
  {
    "procurement_number": "PO-202303-961422",
    "inspection_status": "已验收"
  }
]
```

---

## Q20

**问题**: 中央成品仓有没有仓库管理系统（WMS）？

**SQL**:
```sql
SELECT warehouse_id, warehouse_name, has_wms, wms_system FROM mysql_mhggp0vj."tem"."warehouse_entity" WHERE warehouse_id='WH001'
```

**查询耗时**: 302ms | **返回行数**: 1

**数据**:
```json
[
  {
    "wms_system": "SAP EWM",
    "warehouse_id": "WH001",
    "warehouse_name": "深圳天翼中央成品仓库",
    "has_wms": "是"
  }
]
```

---

## Q21

**问题**: 深圳天翼无人机总装厂目前有哪几条生产线在运行？

**SQL**:
```sql
SELECT factory_id, factory_name, production_lines FROM mysql_mhggp0vj."tem"."factory_entity" WHERE factory_id='FAC001'
```

**查询耗时**: 301ms | **返回行数**: 1

**数据**:
```json
[
  {
    "factory_name": "深圳天翼无人机总装厂",
    "production_lines": "总装线A,总装线B,总装线C",
    "factory_id": "FAC001"
  }
]
```

---

## Q22

**问题**: 入门塑料机身总成（ASSY-BODY-PLA-01）是自制件还是外购件？

**SQL**:
```sql
SELECT material_code, material_name, material_type, is_assembly FROM mysql_mhggp0vj."tem"."material_entity" WHERE material_code='ASSY-BODY-PLA-01'
```

**查询耗时**: 289ms | **返回行数**: 1

**数据**:
```json
[
  {
    "material_name": "入门塑料机身总成",
    "material_type": "组件",
    "is_assembly": "是",
    "material_code": "ASSY-BODY-PLA-01"
  }
]
```

---

## Q23

**问题**: 1200万像素固定相机（PART-CAM-FIX-12MP）的计量单位是什么？

**SQL**:
```sql
SELECT material_code, material_name, unit FROM mysql_mhggp0vj."tem"."material_entity" WHERE material_code='PART-CAM-FIX-12MP'
```

**查询耗时**: 288ms | **返回行数**: 1

**数据**:
```json
[
  {
    "material_name": "1200万像素固定相机",
    "unit": "个",
    "material_code": "PART-CAM-FIX-12MP"
  }
]
```

---

## Q24

**问题**: 霸风20L植保无人机（UAV-BF-IND-H20）的销售计量单位是什么？

**SQL**:
```sql
SELECT product_code, product_name, main_unit FROM mysql_mhggp0vj."tem"."product_entity" WHERE product_code='UAV-BF-IND-H20'
```

**查询耗时**: 297ms | **返回行数**: 1

**数据**:
```json
[
  {
    "product_name": "霸风20L植保无人机",
    "main_unit": "台",
    "product_code": "UAV-BF-IND-H20"
  }
]
```

---

## Q25

**问题**: 领料单REQ-MO202305001-P0001-30的发料状态是什么？

**SQL**:
```sql
SELECT requisition_number, status, material_name, material_code FROM mysql_mhggp0vj."tem"."material_requisition_event" WHERE requisition_number='REQ-MO202305001-P0001-30'
```

**查询耗时**: 290ms | **返回行数**: 1

**数据**:
```json
[
  {
    "material_name": "1200万像素固定相机",
    "material_code": "PART-CAM-FIX-12MP",
    "requisition_number": "REQ-MO202305001-P0001-30",
    "status": "已发料"
  }
]
```

---


## 小结

- 成功查询: 25/25
- 查询出错或无结果: 0/25
