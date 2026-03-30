# S1 直接对象问答 — dataview 原始结果

> 运行时间: 2026-03-26 22:47:48
> 数据源: `90b93fb3-4d8e-42db-8c1a-84f8658364f6`
> dataview: `9d2a06d1-d906-491e-a513-698332ce3751`
> 命令: `kweaver dataview query <view-id> --sql "..."`

---

## S1-Q01

**问题**: 旋风基础版整机（UAV-XF-BASIC）目前在中央成品仓的库存有多少台？

**SQL**:
```sql
SELECT quantity, warehouse_name, snapshot_month FROM mysql_mhggp0vj."tem"."inventory_event" WHERE item_code='UAV-XF-BASIC' AND warehouse_name LIKE '%中央成品%'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q02

**问题**: 采购订单PO-2024040001预计什么时候到货？

**SQL**:
```sql
SELECT purchase_order_number, planned_arrival_date FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2024040001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q03

**问题**: 发货单SH-202305-0001预计什么时候送达客户？

**SQL**:
```sql
SELECT shipment_number, estimated_delivery_date FROM mysql_mhggp0vj."tem"."shipment_event" WHERE shipment_number='SH-202305-0001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q04

**问题**: 发货单SH-202305-0002最终实际是哪天签收的？

**SQL**:
```sql
SELECT shipment_number, actual_delivery_date FROM mysql_mhggp0vj."tem"."shipment_event" WHERE shipment_number='SH-202305-0002'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q05

**问题**: 广州绿野农技技术有限公司的销售订单SO-202303-00001当前处于什么状态？

**SQL**:
```sql
SELECT sales_order_number, order_status, customer_name FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE sales_order_number='SO-202303-00001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q06

**问题**: 广州绿野农技技术有限公司这个客户是我们的重点客户吗？

**SQL**:
```sql
SELECT customer_code, customer_name, is_named_customer FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_name LIKE '%广州绿野%'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q07

**问题**: 西安沃土植保科技有限公司和我们签合同了吗？

**SQL**:
```sql
SELECT customer_code, customer_name, has_contract FROM mysql_mhggp0vj."tem"."customer_entity" WHERE customer_name LIKE '%西安沃土%'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q08

**问题**: 索尼半导体解决方案这家供应商的采购风险评级是多少？

**SQL**:
```sql
SELECT supplier_code, supplier_name, risk_level FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_name LIKE '%索尼%'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q09

**问题**: 博世传感器技术有限公司的货一般要等多少天才能到？

**SQL**:
```sql
SELECT supplier_code, supplier_name, lead_time_avg FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_name LIKE '%博世%'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q10

**问题**: 芯源微电子股份有限公司的付款条件是什么？

**SQL**:
```sql
SELECT supplier_code, supplier_name, payment_terms FROM mysql_mhggp0vj."tem"."supplier_entity" WHERE supplier_name LIKE '%芯源%'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q11

**问题**: 生产工单MO-202305001计划什么时候完工？

**SQL**:
```sql
SELECT production_order_number, planned_finish_date, production_order_id FROM mysql_mhggp0vj."tem"."production_order_event" WHERE production_order_number='MO-202305001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q12

**问题**: 生产工单MO-202305001目前的工单状态是什么？

**SQL**:
```sql
SELECT production_order_number, work_order_status FROM mysql_mhggp0vj."tem"."production_order_event" WHERE production_order_number='MO-202305001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q13

**问题**: 采购订单PO-2024040001这笔单子含税总金额是多少？

**SQL**:
```sql
SELECT purchase_order_number, total_amount_tax, purchase_quantity, unit_price_tax FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2024040001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q14

**问题**: 采购订单PO-2023040002是谁负责跟进的？

**SQL**:
```sql
SELECT purchase_order_number, buyer FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2023040002'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q15

**问题**: 采购订单PO-2024040001目前单据状态是什么？

**SQL**:
```sql
SELECT purchase_order_number, document_status FROM mysql_mhggp0vj."tem"."purchase_order_event" WHERE purchase_order_number='PO-2024040001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q16

**问题**: 销售订单SO-202303-00001给客户的折扣是多少？

**SQL**:
```sql
SELECT sales_order_number, line_number, product_code, discount_rate FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE sales_order_number='SO-202303-00001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q17

**问题**: 销售订单SO-202303-00001承诺的交货日期是哪天？

**SQL**:
```sql
SELECT sales_order_number, line_number, planned_delivery_date FROM mysql_mhggp0vj."tem"."sales_order_event" WHERE sales_order_number='SO-202303-00001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q18

**问题**: 发货单SH-202305-0001用的是哪家物流？

**SQL**:
```sql
SELECT shipment_number, logistics_provider FROM mysql_mhggp0vj."tem"."shipment_event" WHERE shipment_number='SH-202305-0001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q19

**问题**: 物料发货单PO-202303-961422的验收结果是什么？

**SQL**:
```sql
SELECT procurement_number, inspection_status FROM mysql_mhggp0vj."tem"."material_procurement_event" WHERE procurement_number='PO-202303-961422'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q20

**问题**: 中央成品仓有没有仓库管理系统（WMS）？

**SQL**:
```sql
SELECT warehouse_id, warehouse_name, has_wms, wms_system FROM mysql_mhggp0vj."tem"."warehouse_entity" WHERE warehouse_id='WH001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q21

**问题**: 深圳天翼无人机总装厂目前有哪几条生产线在运行？

**SQL**:
```sql
SELECT factory_id, factory_name, production_lines FROM mysql_mhggp0vj."tem"."factory_entity" WHERE factory_id='FAC001'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q22

**问题**: 入门塑料机身总成（ASSY-BODY-PLA-01）是自制件还是外购件？

**SQL**:
```sql
SELECT material_code, material_name, material_type, is_assembly FROM mysql_mhggp0vj."tem"."material_entity" WHERE material_code='ASSY-BODY-PLA-01'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q23

**问题**: 1200万像素固定相机（PART-CAM-FIX-12MP）的计量单位是什么？

**SQL**:
```sql
SELECT material_code, material_name, unit FROM mysql_mhggp0vj."tem"."material_entity" WHERE material_code='PART-CAM-FIX-12MP'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q24

**问题**: 霸风20L植保无人机（UAV-BF-IND-H20）的销售计量单位是什么？

**SQL**:
```sql
SELECT product_code, product_name, main_unit FROM mysql_mhggp0vj."tem"."product_entity" WHERE product_code='UAV-BF-IND-H20'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---

## S1-Q25

**问题**: 领料单REQ-MO202305001-P0001-30的发料状态是什么？

**SQL**:
```sql
SELECT requisition_number, status, material_name, material_code FROM mysql_mhggp0vj."tem"."material_requisition_event" WHERE requisition_number='REQ-MO202305001-P0001-30'
```

**结果**: ERROR — HTTP 500 Internal Server Error
{"error_code":"Uniquery.DataView.InternalError.FetchDataFromVegaFailed","description":"从 vega-gateway-pro 服务或数据连接服务获取数据失败","solution":"请重试该操作，若再次出现该错误请提交工单或联系技术支持工程师。","error_link":"暂无","error_details":"query data from vega gateway error: {\"error_code\":\"Public.BadRequest\",\"error_link\":\"暂无\",\"error_details\":\"catalog name not match\",\"description\":\"参数错误\",\"solution\":\"暂无\"}"}

---


## 小结
- 有数据行: 0/25
- 本段 dataview 调用次数: 25