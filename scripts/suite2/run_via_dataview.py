#!/usr/bin/env python3.12
"""
Suite-2: Answer all 100 questions via kweaver dataview query (SQL over mdl-uniquery).
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from datetime import datetime

# 须与 dataview 所属数据源在 Vega 侧的 catalog 一致，否则报 catalog name not match
# 数据源 supply_chain_data_v1 (90b93fb3-4d8e-42db-8c1a-84f8658364f6)：mysql_1j6tsjwo."supply_chain_data"
VIEW_ID = "9d2a06d1-d906-491e-a513-698332ce3751"  # warehouse_entity，同上数据源
C = 'mysql_1j6tsjwo."supply_chain_data"'

T = dict(
    P=f'{C}."product_entity"',
    M=f'{C}."material_entity"',
    B=f'{C}."bom_event"',
    CU=f'{C}."customer_entity"',
    SU=f'{C}."supplier_entity"',
    PO=f'{C}."purchase_order_event"',
    SO=f'{C}."sales_order_event"',
    INV=f'{C}."inventory_event"',
    WH=f'{C}."warehouse_entity"',
    FAC=f'{C}."factory_entity"',
    PRD=f'{C}."production_order_event"',
    SH=f'{C}."shipment_event"',
    MP=f'{C}."material_procurement_event"',
    MR=f'{C}."material_requisition_event"',
)

REPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "test_report", "suite-2", "db_answers")
os.makedirs(REPORT_DIR, exist_ok=True)


def run_sql(sql: str) -> dict:
    result = subprocess.run(
        ["kweaver", "dataview", "query", VIEW_ID, "--sql", sql],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip() or result.stdout.strip()}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": f"JSON parse error: {result.stdout[:300]}"}


def ask(qid: str, question: str, sql: str) -> dict:
    print(f"  {qid}: {question[:50]}...", end=" ", flush=True)
    r = run_sql(sql)
    if "error" in r:
        print(f"ERR: {r['error'][:80]}")
    else:
        n = len(r.get("entries", []))
        print(f"OK ({n} rows)")
    return {"qid": qid, "question": question, "sql": sql, "result": r}


# ===================== S1: 直接对象问答 =====================
def run_s1():
    results = []
    a = lambda qid, q, sql: results.append(ask(qid, q, sql))

    a("Q01", "旋风基础版整机（UAV-XF-BASIC）目前在中央成品仓的库存有多少台？",
      f"SELECT quantity, warehouse_name, snapshot_month FROM {T['INV']} WHERE item_code='UAV-XF-BASIC' AND warehouse_name LIKE '%中央成品%'")

    a("Q02", "采购订单PO-2024040001预计什么时候到货？",
      f"SELECT purchase_order_number, planned_arrival_date FROM {T['PO']} WHERE purchase_order_number='PO-2024040001'")

    a("Q03", "发货单SH-202305-0001预计什么时候送达客户？",
      f"SELECT shipment_number, estimated_delivery_date FROM {T['SH']} WHERE shipment_number='SH-202305-0001'")

    a("Q04", "发货单SH-202305-0002最终实际是哪天签收的？",
      f"SELECT shipment_number, actual_delivery_date FROM {T['SH']} WHERE shipment_number='SH-202305-0002'")

    a("Q05", "广州绿野农技技术有限公司的销售订单SO-202303-00001当前处于什么状态？",
      f"SELECT sales_order_number, order_status, customer_name FROM {T['SO']} WHERE sales_order_number='SO-202303-00001'")

    a("Q06", "广州绿野农技技术有限公司这个客户是我们的重点客户吗？",
      f"SELECT customer_code, customer_name, is_named_customer FROM {T['CU']} WHERE customer_name LIKE '%广州绿野%'")

    a("Q07", "西安沃土植保科技有限公司和我们签合同了吗？",
      f"SELECT customer_code, customer_name, has_contract FROM {T['CU']} WHERE customer_name LIKE '%西安沃土%'")

    a("Q08", "索尼半导体解决方案这家供应商的采购风险评级是多少？",
      f"SELECT supplier_code, supplier_name, risk_level FROM {T['SU']} WHERE supplier_name LIKE '%索尼%'")

    a("Q09", "博世传感器技术有限公司的货一般要等多少天才能到？",
      f"SELECT supplier_code, supplier_name, lead_time_avg FROM {T['SU']} WHERE supplier_name LIKE '%博世%'")

    a("Q10", "芯源微电子股份有限公司的付款条件是什么？",
      f"SELECT supplier_code, supplier_name, payment_terms FROM {T['SU']} WHERE supplier_name LIKE '%芯源%'")

    a("Q11", "生产工单MO-202305001计划什么时候完工？",
      f"SELECT production_order_number, planned_finish_date, production_order_id FROM {T['PRD']} WHERE production_order_number='MO-202305001'")

    a("Q12", "生产工单MO-202305001目前的工单状态是什么？",
      f"SELECT production_order_number, work_order_status FROM {T['PRD']} WHERE production_order_number='MO-202305001'")

    a("Q13", "采购订单PO-2024040001这笔单子含税总金额是多少？",
      f"SELECT purchase_order_number, total_amount_tax, purchase_quantity, unit_price_tax FROM {T['PO']} WHERE purchase_order_number='PO-2024040001'")

    a("Q14", "采购订单PO-2023040002是谁负责跟进的？",
      f"SELECT purchase_order_number, buyer FROM {T['PO']} WHERE purchase_order_number='PO-2023040002'")

    a("Q15", "采购订单PO-2024040001目前单据状态是什么？",
      f"SELECT purchase_order_number, document_status FROM {T['PO']} WHERE purchase_order_number='PO-2024040001'")

    a("Q16", "销售订单SO-202303-00001给客户的折扣是多少？",
      f"SELECT sales_order_number, line_number, product_code, discount_rate FROM {T['SO']} WHERE sales_order_number='SO-202303-00001'")

    a("Q17", "销售订单SO-202303-00001承诺的交货日期是哪天？",
      f"SELECT sales_order_number, line_number, planned_delivery_date FROM {T['SO']} WHERE sales_order_number='SO-202303-00001'")

    a("Q18", "发货单SH-202305-0001用的是哪家物流？",
      f"SELECT shipment_number, logistics_provider FROM {T['SH']} WHERE shipment_number='SH-202305-0001'")

    a("Q19", "物料发货单PO-202303-961422的验收结果是什么？",
      f"SELECT procurement_number, inspection_status FROM {T['MP']} WHERE procurement_number='PO-202303-961422'")

    a("Q20", "中央成品仓有没有仓库管理系统（WMS）？",
      f"SELECT warehouse_id, warehouse_name, has_wms, wms_system FROM {T['WH']} WHERE warehouse_id='WH001'")

    a("Q21", "深圳天翼无人机总装厂目前有哪几条生产线在运行？",
      f"SELECT factory_id, factory_name, production_lines FROM {T['FAC']} WHERE factory_id='FAC001'")

    a("Q22", "入门塑料机身总成（ASSY-BODY-PLA-01）是自制件还是外购件？",
      f"SELECT material_code, material_name, material_type, is_assembly FROM {T['M']} WHERE material_code='ASSY-BODY-PLA-01'")

    a("Q23", "1200万像素固定相机（PART-CAM-FIX-12MP）的计量单位是什么？",
      f"SELECT material_code, material_name, unit FROM {T['M']} WHERE material_code='PART-CAM-FIX-12MP'")

    a("Q24", "霸风20L植保无人机（UAV-BF-IND-H20）的销售计量单位是什么？",
      f"SELECT product_code, product_name, main_unit FROM {T['P']} WHERE product_code='UAV-BF-IND-H20'")

    a("Q25", "领料单REQ-MO202305001-P0001-30的发料状态是什么？",
      f"SELECT requisition_number, status, material_name, material_code FROM {T['MR']} WHERE requisition_number='REQ-MO202305001-P0001-30'")

    return results


# ===================== S2: 2跳问答 =====================
def run_s2():
    results = []
    a = lambda qid, q, sql: results.append(ask(qid, q, sql))

    a("Q01", "采购订单PO-2024040001买的是什么物料？零件还是组件？",
      f"SELECT po.purchase_order_number, po.material_code, po.material_name, m.material_type, m.is_assembly FROM {T['PO']} po JOIN {T['M']} m ON po.material_code=m.material_code WHERE po.purchase_order_number='PO-2024040001'")

    a("Q02", "采购订单PO-2024040001的供应商交货周期一般是多久？",
      f"SELECT po.purchase_order_number, po.supplier_name, su.lead_time_avg FROM {T['PO']} po JOIN {T['SU']} su ON po.supplier_id=su.supplier_id WHERE po.purchase_order_number='PO-2024040001'")

    a("Q03", "采购订单PO-2024040001的供应商有没有供货风险？",
      f"SELECT po.purchase_order_number, su.supplier_name, su.supplier_code, su.risk_level, su.supplier_tier FROM {T['PO']} po JOIN {T['SU']} su ON po.supplier_id=su.supplier_id WHERE po.purchase_order_number='PO-2024040001'")

    a("Q04", "销售订单SO-202303-00001卖的是哪款产品？还在产吗？",
      f"SELECT so.sales_order_number, so.product_code, p.product_name, p.status FROM {T['SO']} so JOIN {T['P']} p ON so.product_code=p.product_code WHERE so.sales_order_number='SO-202303-00001'")

    a("Q05", "广州绿野农技是哪个级别的客户？SO-202303-00001是否加急？",
      f"SELECT cu.customer_name, cu.customer_level, so.is_urgent, so.sales_order_number FROM {T['CU']} cu JOIN {T['SO']} so ON cu.customer_id=so.customer_id WHERE cu.customer_name LIKE '%广州绿野%' AND so.sales_order_number='SO-202303-00001'")

    a("Q06", "发货单SH-202305-0001发的是哪款产品？库存单价多少？",
      f"SELECT sh.shipment_number, sh.product_code, sh.product_name, inv.unit_price FROM {T['SH']} sh JOIN {T['INV']} inv ON sh.product_code=inv.item_code WHERE sh.shipment_number='SH-202305-0001'")

    a("Q07", "发货单SH-202305-0001从哪个仓库发出？有没有冷链？",
      f"SELECT sh.shipment_number, sh.warehouse_name, wh.warehouse_code, wh.has_cold_storage FROM {T['SH']} sh JOIN {T['WH']} wh ON sh.warehouse_id=wh.warehouse_id WHERE sh.shipment_number='SH-202305-0001'")

    a("Q08", "生产工单MO-202305001在哪个工厂生产？多少员工？",
      f"SELECT prd.production_order_number, fac.factory_name, fac.employee_count FROM {T['PRD']} prd JOIN {T['FAC']} fac ON prd.factory_id=fac.factory_id WHERE prd.production_order_number='MO-202305001'")

    a("Q09", "生产工单MO-202305001生产什么产品？BOM版本？",
      f"SELECT DISTINCT prd.production_order_number, prd.output_code, prd.output_name, b.bom_version FROM {T['PRD']} prd JOIN {T['B']} b ON prd.output_code=b.parent_code WHERE prd.production_order_number='MO-202305001'")

    a("Q10", "库存记录INV0000001存在哪个仓库？有没有自动化分拣？",
      f"SELECT inv.inventory_id, inv.warehouse_name, wh.warehouse_code, wh.has_sorting_system FROM {T['INV']} inv JOIN {T['WH']} wh ON inv.warehouse_id=wh.warehouse_id WHERE inv.inventory_id='INV0000001'")

    a("Q11", "旋风基础版整机（UAV-XF-BASIC）目前的库存总价值？",
      f"SELECT item_code, SUM(total_price) as total_value, SUM(quantity) as total_qty, unit_price FROM {T['INV']} WHERE item_code='UAV-XF-BASIC' GROUP BY item_code, unit_price")

    a("Q12", "物料发货单PO-202303-961422是哪家供应商？几级？",
      f"SELECT mp.procurement_number, mp.supplier_name, su.supplier_code, su.supplier_tier FROM {T['MP']} mp JOIN {T['SU']} su ON mp.supplier_code=su.supplier_code WHERE mp.procurement_number='PO-202303-961422'")

    a("Q13", "物料发货单PO-202303-961422入了哪个仓库？有RFID吗？",
      f"SELECT mp.procurement_number, mp.warehouse_name, wh.warehouse_code, wh.has_rfid FROM {T['MP']} mp JOIN {T['WH']} wh ON mp.warehouse_id=wh.warehouse_id WHERE mp.procurement_number='PO-202303-961422'")

    a("Q14", "领料单REQ-MO202305001-P0001-10从哪个仓库领料？面积多大？",
      f"SELECT mr.requisition_number, mr.warehouse_name, wh.warehouse_code, wh.storage_area_sqm FROM {T['MR']} mr JOIN {T['WH']} wh ON mr.warehouse_id=wh.warehouse_id WHERE mr.requisition_number='REQ-MO202305001-P0001-10'")

    a("Q15", "领料单REQ-MO202305001-P0001-10领的什么物料？是组件吗？",
      f"SELECT mr.requisition_number, mr.material_name, m.material_code, m.is_assembly FROM {T['MR']} mr JOIN {T['M']} m ON mr.material_code=m.material_code WHERE mr.requisition_number='REQ-MO202305001-P0001-10'")

    a("Q16", "领料单REQ-MO202305001-P0001-10给哪个工厂领料？什么类型？",
      f"SELECT mr.requisition_number, mr.factory_name, fac.factory_code, fac.factory_type FROM {T['MR']} mr JOIN {T['FAC']} fac ON mr.factory_id=fac.factory_id WHERE mr.requisition_number='REQ-MO202305001-P0001-10'")

    a("Q17", "旋风基础版整机（UAV-XF-BASIC）BOM V2.0用了哪些物料？",
      f"SELECT child_code, child_name, quantity, scrap_rate, child_type FROM {T['B']} WHERE parent_code='UAV-XF-BASIC' AND bom_version='V2.0'")

    a("Q18", "1200万像素固定相机（PART-CAM-FIX-12MP）被用在哪款产品上？",
      f"SELECT b.parent_code, p.product_name, b.bom_version, b.quantity, b.scrap_rate FROM {T['B']} b JOIN {T['P']} p ON b.parent_code=p.product_code WHERE b.child_code='PART-CAM-FIX-12MP'")

    a("Q19", "广州绿野SO-202303-00001总共花了多少钱？",
      f"SELECT sales_order_number, line_number, product_code, total_amount, subtotal_amount FROM {T['SO']} WHERE sales_order_number='SO-202303-00001'")

    a("Q20", "旋风基础版整机（UAV-XF-BASIC）在中央成品仓什么时候入库的？",
      f"SELECT item_code, warehouse_name, earliest_storage_date, batch_number FROM {T['INV']} WHERE item_code='UAV-XF-BASIC' AND warehouse_name LIKE '%中央成品%'")

    a("Q21", "采购订单PO-2023040002的到货数量是多少？都入库了吗？",
      f"SELECT purchase_order_number, purchase_quantity, accumulated_arrival_tax, accumulated_storage_tax, document_status FROM {T['PO']} WHERE purchase_order_number='PO-2023040002'")

    a("Q22", "发货单SH-202305-0003是发给哪个客户的？是重点客户吗？",
      f"SELECT sh.shipment_number, sh.customer_name, cu.customer_code, cu.is_named_customer FROM {T['SH']} sh JOIN {T['CU']} cu ON sh.customer_code=cu.customer_code WHERE sh.shipment_number='SH-202305-0003'")

    a("Q23", "生产工单MO-202305002在哪条生产线？所在工厂总产能多少？",
      f"SELECT prd.production_order_number, prd.production_line, fac.factory_name, fac.total_capacity FROM {T['PRD']} prd JOIN {T['FAC']} fac ON prd.factory_id=fac.factory_id WHERE prd.production_order_number='MO-202305002'")

    a("Q24", "标准智能电池2S3000mAh（PART-BAT-2S-3000）在BOM中损耗率多少？",
      f"SELECT parent_code, child_code, child_name, scrap_rate, bom_version FROM {T['B']} WHERE child_code='PART-BAT-2S-3000'")

    a("Q25", "发货单SH-202305-0004的交付状态是什么？货到了吗？",
      f"SELECT shipment_number, delivery_status, actual_delivery_date, customer_name FROM {T['SH']} WHERE shipment_number='SH-202305-0004'")

    return results


# ===================== S3: 3跳问答 =====================
def run_s3():
    results = []
    a = lambda qid, q, sql: results.append(ask(qid, q, sql))

    a("Q01", "SO-202303-00001的产品BOM中零件类子项？",
      f"SELECT DISTINCT b.child_code, b.child_name, m.material_type, b.scrap_rate FROM {T['SO']} so JOIN {T['B']} b ON so.product_code=b.parent_code JOIN {T['M']} m ON b.child_code=m.material_code WHERE so.sales_order_number='SO-202303-00001' AND m.material_type='零件'")

    a("Q02", "SO-202303-00001产品BOM物料有在途采购订单吗？",
      f"SELECT DISTINCT po.purchase_order_number, po.material_code, po.material_name, po.document_status FROM {T['SO']} so JOIN {T['B']} b ON so.product_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code WHERE so.sales_order_number='SO-202303-00001' AND po.document_status!='已关闭'")

    a("Q03", "发货单SH-202305-0001对应的销售订单客户等级？",
      f"SELECT sh.shipment_number, sh.sales_order_number, cu.customer_name, cu.customer_level FROM {T['SH']} sh JOIN {T['CU']} cu ON sh.customer_code=cu.customer_code WHERE sh.shipment_number='SH-202305-0001'")

    a("Q04", "UAV-XF-BASIC BOM物料中哪些当前有库存(quantity>0)？",
      f"SELECT b.child_code, b.child_name, inv.warehouse_name, inv.quantity FROM {T['B']} b JOIN {T['INV']} inv ON b.child_code=inv.item_code WHERE b.parent_code='UAV-XF-BASIC' AND inv.quantity>0")

    a("Q05", "PART-CAM-FIX-12MP采购订单有没有交期延误？",
      f"SELECT purchase_order_number, planned_arrival_date, required_date FROM {T['PO']} WHERE material_code='PART-CAM-FIX-12MP'")

    a("Q06", "MO-202305001领料物料从哪些仓库出库？有自动分拣吗？",
      f"SELECT DISTINCT mr.warehouse_name, wh.warehouse_code, wh.has_sorting_system FROM {T['MR']} mr JOIN {T['WH']} wh ON mr.warehouse_id=wh.warehouse_id WHERE mr.production_order_number='MO-202305001'")

    a("Q07", "ASSY-BODY-PLA-01的供应商有高风险的吗？",
      f"SELECT DISTINCT mp.supplier_name, su.supplier_code, su.risk_level FROM {T['MP']} mp JOIN {T['SU']} su ON mp.supplier_code=su.supplier_code WHERE mp.material_code='ASSY-BODY-PLA-01'")

    a("Q08", "广州绿野农技的订单发货用了哪些物流商？",
      f"SELECT DISTINCT sh.logistics_provider FROM {T['SH']} sh WHERE sh.customer_name LIKE '%广州绿野%'")

    a("Q09", "UAV-XF-BASIC库存在哪些仓库？仓库负责人？",
      f"SELECT DISTINCT inv.warehouse_name, wh.warehouse_code, wh.manager_name FROM {T['INV']} inv JOIN {T['WH']} wh ON inv.warehouse_id=wh.warehouse_id WHERE inv.item_code='UAV-XF-BASIC'")

    a("Q10", "SUP-021的货发到了哪些仓库？什么类型？",
      f"SELECT DISTINCT mp.warehouse_name, wh.warehouse_code, wh.warehouse_type FROM {T['MP']} mp JOIN {T['WH']} wh ON mp.warehouse_id=wh.warehouse_id WHERE mp.supplier_code='SUP-021'")

    a("Q11", "FAC001生产的产品里哪些库存超过1000台？",
      f"SELECT prd.output_code, prd.output_name, SUM(inv.quantity) as total_qty FROM {T['PRD']} prd JOIN {T['INV']} inv ON prd.output_code=inv.item_code WHERE prd.factory_id IN (SELECT factory_id FROM {T['FAC']} WHERE factory_id='FAC001') GROUP BY prd.output_code, prd.output_name HAVING SUM(inv.quantity)>1000")

    a("Q12", "领料单REQ-MO202305001-P0001-30物料的采购供应商？",
      f"SELECT mr.material_code, mr.material_name, po.purchase_order_number, po.supplier_name FROM {T['MR']} mr JOIN {T['PO']} po ON mr.material_code=po.material_code WHERE mr.requisition_number='REQ-MO202305001-P0001-30'")

    a("Q13", "PART-CAM-FIX-12MP来料验收状态分布？",
      f"SELECT inspection_status, COUNT(*) as cnt FROM {T['MP']} WHERE material_code='PART-CAM-FIX-12MP' GROUP BY inspection_status")

    a("Q14", "UAV-BF-IND-H30在哪个工厂生产？工厂认证？",
      f"SELECT DISTINCT prd.output_code, fac.factory_name, fac.factory_code, fac.certification FROM {T['PRD']} prd JOIN {T['FAC']} fac ON prd.factory_id=fac.factory_id WHERE prd.output_code='UAV-BF-IND-H30'")

    a("Q15", "西安沃土（CUST-10002）有没有运输中的发货单？",
      f"SELECT sh.shipment_number, sh.delivery_status, sh.product_name FROM {T['SH']} sh WHERE sh.customer_code='CUST-10002' AND sh.delivery_status='运输中'")

    a("Q16", "PART-BAT-2S-3000用在哪些产品上？库存总量？",
      f"SELECT b.parent_code, p.product_name, SUM(inv.quantity) as total_qty FROM {T['B']} b JOIN {T['P']} p ON b.parent_code=p.product_code LEFT JOIN {T['INV']} inv ON p.product_code=inv.item_code WHERE b.child_code='PART-BAT-2S-3000' GROUP BY b.parent_code, p.product_name")

    a("Q17", "CUST-10148历史所有订单总金额？",
      f"SELECT SUM(total_amount) as grand_total, COUNT(*) as order_count FROM {T['SO']} WHERE customer_id IN (SELECT customer_id FROM {T['CU']} WHERE customer_code='CUST-10148')")

    a("Q18", "PO-2024110005采购物料被用在哪些产品上？产品类型？",
      f"SELECT DISTINCT b.parent_code, p.product_name, p.product_type FROM {T['PO']} po JOIN {T['B']} b ON po.material_code=b.child_code JOIN {T['P']} p ON b.parent_code=p.product_code WHERE po.purchase_order_number='PO-2024110005'")

    a("Q19", "UAV-XF-BASIC-PLUS的发货单有多少已签收？",
      f"SELECT delivery_status, COUNT(*) as cnt FROM {T['SH']} WHERE product_code='UAV-XF-BASIC-PLUS' GROUP BY delivery_status")

    a("Q20", "WH002收到的物料有没有采购风险高的？",
      f"SELECT DISTINCT mp.material_code, mp.material_name, su.supplier_name, su.risk_level FROM {T['MP']} mp JOIN {T['SU']} su ON mp.supplier_code=su.supplier_code WHERE mp.warehouse_id IN (SELECT warehouse_id FROM {T['WH']} WHERE warehouse_id='WH002')")

    a("Q21", "SUP-004供的物料被用在哪些产品BOM里？有库存吗？",
      f"SELECT DISTINCT po.material_code, b.parent_code, p.product_name, COALESCE(inv.quantity, 0) as inv_qty FROM {T['PO']} po JOIN {T['B']} b ON po.material_code=b.child_code JOIN {T['P']} p ON b.parent_code=p.product_code LEFT JOIN {T['INV']} inv ON p.product_code=inv.item_code WHERE po.supplier_id IN (SELECT supplier_id FROM {T['SU']} WHERE supplier_code='SUP-004')")

    a("Q22", "SH-202305-0003收货方还有哪些未发货订单？",
      f"SELECT so.sales_order_number, so.product_code, so.order_status FROM {T['SH']} sh JOIN {T['SO']} so ON sh.customer_code IN (SELECT customer_code FROM {T['CU']} WHERE customer_id=so.customer_id) WHERE sh.shipment_number='SH-202305-0003' AND so.order_status!='已发货'")

    a("Q23", "MO-202305003产品BOM物料采购总金额？",
      f"SELECT SUM(po.total_amount_tax) as total_purchase FROM {T['PRD']} prd JOIN {T['B']} b ON prd.output_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code WHERE prd.production_order_number='MO-202305003'")

    a("Q24", "WH001里的产品有哪些还有未完成的销售订单？",
      f"SELECT DISTINCT inv.item_code, inv.item_name, so.sales_order_number, so.order_status FROM {T['INV']} inv JOIN {T['SO']} so ON inv.item_code=so.product_code WHERE inv.warehouse_id IN (SELECT warehouse_id FROM {T['WH']} WHERE warehouse_id='WH001') AND so.order_status!='已发货'")

    a("Q25", "UAV-XF-BASIC BOM中损耗率>0的物料库存够几台？",
      f"SELECT b.child_code, b.child_name, b.scrap_rate, b.quantity as qty_per, COALESCE(SUM(inv.quantity), 0) as total_inv FROM {T['B']} b LEFT JOIN {T['INV']} inv ON b.child_code=inv.item_code WHERE b.parent_code='UAV-XF-BASIC' AND b.scrap_rate>0 GROUP BY b.child_code, b.child_name, b.scrap_rate, b.quantity")

    return results


# ===================== S4: 4跳问答 =====================
def run_s4():
    results = []
    a = lambda qid, q, sql: results.append(ask(qid, q, sql))

    a("Q01", "广州绿野订购的产品BOM物料有高风险供应商吗？",
      f"SELECT DISTINCT su.supplier_name, su.risk_level, po.material_code FROM {T['SO']} so JOIN {T['B']} b ON so.product_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code JOIN {T['SU']} su ON po.supplier_id=su.supplier_id WHERE so.customer_name LIKE '%广州绿野%'")

    a("Q02", "广州绿野订购产品BOM物料库存够不够(>500)？",
      f"SELECT b.child_code, b.child_name, COALESCE(SUM(inv.quantity),0) as inv_qty FROM {T['SO']} so JOIN {T['B']} b ON so.product_code=b.parent_code LEFT JOIN {T['INV']} inv ON b.child_code=inv.item_code WHERE so.customer_name LIKE '%广州绿野%' GROUP BY b.child_code, b.child_name")

    a("Q03", "SH-202305-0001产品BOM物料的采购订单有逾期的吗？",
      f"SELECT po.purchase_order_number, po.material_code, po.planned_arrival_date, po.required_date FROM {T['SH']} sh JOIN {T['B']} b ON sh.product_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code WHERE sh.shipment_number='SH-202305-0001' AND po.planned_arrival_date>po.required_date")

    a("Q04", "FAC001生产的所有产品发货物流商占比？",
      f"SELECT sh.logistics_provider, COUNT(*) as cnt FROM {T['PRD']} prd JOIN {T['SH']} sh ON prd.output_code=sh.product_code WHERE prd.factory_id IN (SELECT factory_id FROM {T['FAC']} WHERE factory_id='FAC001') GROUP BY sh.logistics_provider ORDER BY cnt DESC")

    a("Q05", "WH001里的产品客户里有多少T1大客户？",
      f"SELECT COUNT(DISTINCT cu.customer_code) as t1_count FROM {T['INV']} inv JOIN {T['SO']} so ON inv.item_code=so.product_code JOIN {T['CU']} cu ON so.customer_id=cu.customer_id WHERE inv.warehouse_id IN (SELECT warehouse_id FROM {T['WH']} WHERE warehouse_id='WH001') AND cu.customer_level='T1'")

    a("Q06", "PART-CAM-FIX-12MP被用在哪些产品上？T1级客户？",
      f"SELECT DISTINCT cu.customer_name, cu.customer_code, cu.customer_level FROM {T['B']} b JOIN {T['SH']} sh ON b.parent_code=sh.product_code JOIN {T['CU']} cu ON sh.customer_code=cu.customer_code WHERE b.child_code='PART-CAM-FIX-12MP' AND cu.customer_level='T1'")

    a("Q07", "SUP-021供的零件用在哪些产品？哪些工厂生产？认证？",
      f"SELECT DISTINCT p.product_name, fac.factory_name, fac.certification FROM {T['PO']} po JOIN {T['B']} b ON po.material_code=b.child_code JOIN {T['P']} p ON b.parent_code=p.product_code JOIN {T['PRD']} prd ON p.product_code=prd.output_code JOIN {T['FAC']} fac ON prd.factory_id=fac.factory_id WHERE po.supplier_id IN (SELECT supplier_id FROM {T['SU']} WHERE supplier_code='SUP-021')")

    a("Q08", "CUST-10003订购产品BOM物料来料验收情况？",
      f"SELECT DISTINCT mp.material_code, mp.material_name, mp.inspection_status FROM {T['SO']} so JOIN {T['B']} b ON so.product_code=b.parent_code JOIN {T['MP']} mp ON b.child_code=mp.material_code WHERE so.customer_id IN (SELECT customer_id FROM {T['CU']} WHERE customer_code='CUST-10003')")

    a("Q09", "MO-202305001产品BOM物料采购供应商哪些月结30天？",
      f"SELECT DISTINCT su.supplier_name, su.supplier_code, su.payment_terms FROM {T['PRD']} prd JOIN {T['B']} b ON prd.output_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code JOIN {T['SU']} su ON po.supplier_id=su.supplier_id WHERE prd.production_order_number='MO-202305001' AND su.payment_terms LIKE '%30%'")

    a("Q10", "UAV-XF-BASIC BOM物料库存在哪些仓库？有AGV吗？",
      f"SELECT DISTINCT b.child_code, inv.warehouse_name, wh.warehouse_code, wh.has_agv, wh.agv_count FROM {T['B']} b JOIN {T['INV']} inv ON b.child_code=inv.item_code JOIN {T['WH']} wh ON inv.warehouse_id=wh.warehouse_id WHERE b.parent_code='UAV-XF-BASIC'")

    a("Q11", "FAC001生产产品的客户里有多少是重点客户？",
      f"SELECT COUNT(DISTINCT cu.customer_code) as named_count FROM {T['PRD']} prd JOIN {T['SH']} sh ON prd.output_code=sh.product_code JOIN {T['CU']} cu ON sh.customer_code=cu.customer_code WHERE prd.factory_id IN (SELECT factory_id FROM {T['FAC']} WHERE factory_id='FAC001') AND cu.is_named_customer='是'")

    a("Q12", "ASSY-BODY-PLA-01供应商发货入库仓库里还有哪些产品？销售订单总金额？",
      f"SELECT DISTINCT inv.item_code, inv.item_name, SUM(so.total_amount) as so_total FROM {T['MP']} mp JOIN {T['INV']} inv ON mp.warehouse_id=inv.warehouse_id JOIN {T['SO']} so ON inv.item_code=so.product_code WHERE mp.material_code='ASSY-BODY-PLA-01' GROUP BY inv.item_code, inv.item_name")

    a("Q13", "SUP-021供的所有物料被用在哪些产品？运输中发货单数？",
      f"SELECT COUNT(*) as in_transit FROM {T['PO']} po JOIN {T['B']} b ON po.material_code=b.child_code JOIN {T['SH']} sh ON b.parent_code=sh.product_code WHERE po.supplier_id IN (SELECT supplier_id FROM {T['SU']} WHERE supplier_code='SUP-021') AND sh.delivery_status='运输中'")

    a("Q14", "FAC001生产产品BOM中有损耗物料(scrap_rate>0)？库存充足吗？",
      f"SELECT DISTINCT b.child_code, b.child_name, b.scrap_rate, COALESCE(SUM(inv.quantity),0) as inv_qty FROM {T['PRD']} prd JOIN {T['B']} b ON prd.output_code=b.parent_code LEFT JOIN {T['INV']} inv ON b.child_code=inv.item_code WHERE prd.factory_id IN (SELECT factory_id FROM {T['FAC']} WHERE factory_id='FAC001') AND b.scrap_rate>0 GROUP BY b.child_code, b.child_name, b.scrap_rate")

    a("Q15", "广州绿野的发货仓库里还有哪些其他产品？在哪些工厂生产？",
      f"SELECT DISTINCT inv.item_code, inv.item_name, fac.factory_name FROM {T['SH']} sh JOIN {T['INV']} inv ON sh.warehouse_id=inv.warehouse_id JOIN {T['PRD']} prd ON inv.item_code=prd.output_code JOIN {T['FAC']} fac ON prd.factory_id=fac.factory_id WHERE sh.customer_name LIKE '%广州绿野%'")

    a("Q16", "UAV-XF-BASIC BOM供应商里哪些也给其他产品供货？",
      f"SELECT DISTINCT su.supplier_name, su.supplier_code, b2.parent_code as other_product FROM {T['B']} b1 JOIN {T['PO']} po ON b1.child_code=po.material_code JOIN {T['SU']} su ON po.supplier_id=su.supplier_id JOIN {T['PO']} po2 ON su.supplier_id=po2.supplier_id JOIN {T['B']} b2 ON po2.material_code=b2.child_code WHERE b1.parent_code='UAV-XF-BASIC' AND b2.parent_code!='UAV-XF-BASIC'")

    a("Q17", "WH002收到的物料被用在哪些产品？有多少加急销售订单？",
      f"SELECT COUNT(*) as urgent_count FROM {T['MP']} mp JOIN {T['B']} b ON mp.material_code=b.child_code JOIN {T['SO']} so ON b.parent_code=so.product_code WHERE mp.warehouse_id IN (SELECT warehouse_id FROM {T['WH']} WHERE warehouse_id='WH002') AND so.is_urgent='是'")

    a("Q18", "SUP-001供的物料库存在哪些仓库？发货客户里有T2的吗？",
      f"SELECT DISTINCT cu.customer_name, cu.customer_code, cu.customer_level FROM {T['PO']} po JOIN {T['INV']} inv ON po.material_code=inv.item_code JOIN {T['SH']} sh ON inv.warehouse_id=sh.warehouse_id JOIN {T['CU']} cu ON sh.customer_code=cu.customer_code WHERE po.supplier_id IN (SELECT supplier_id FROM {T['SU']} WHERE supplier_code='SUP-001') AND cu.customer_level='T2'")

    a("Q19", "UAV-XF-PRO-A的客户还下了哪些其他产品订单？有库存吗？",
      f"SELECT DISTINCT so2.product_code, so2.product_name, COALESCE(inv.quantity,0) as inv_qty FROM {T['SH']} sh JOIN {T['SO']} so2 ON sh.customer_code IN (SELECT customer_code FROM {T['CU']} WHERE customer_id=so2.customer_id) LEFT JOIN {T['INV']} inv ON so2.product_code=inv.item_code WHERE sh.product_code='UAV-XF-PRO-A' AND so2.product_code!='UAV-XF-PRO-A'")

    a("Q20", "基础飞控总成(ASSY-FC-BASIC)供应商发货入库仓库里还有哪些产品？生产工单优先级？",
      f"SELECT DISTINCT inv.item_code, inv.item_name, prd.priority FROM {T['MP']} mp JOIN {T['INV']} inv ON mp.warehouse_id=inv.warehouse_id JOIN {T['PRD']} prd ON inv.item_code=prd.output_code WHERE mp.material_code='ASSY-FC-BASIC'")

    a("Q21", "CUST-10130收到的产品BOM物料采购订单中已收货的有几笔？",
      f"SELECT po.purchase_order_number, po.material_code, po.document_status FROM {T['SH']} sh JOIN {T['B']} b ON sh.product_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code WHERE sh.customer_code='CUST-10130' AND po.document_status='已收货'")

    a("Q22", "FAC001领料物料的采购供应商年产能合计？",
      f"SELECT DISTINCT su.supplier_name, su.supplier_code, su.annual_capacity FROM {T['MR']} mr JOIN {T['PO']} po ON mr.material_code=po.material_code JOIN {T['SU']} su ON po.supplier_id=su.supplier_id WHERE mr.factory_id IN (SELECT factory_id FROM {T['FAC']} WHERE factory_id='FAC001')")

    a("Q23", "PO-2024040001供应商的所有物料被哪些产品BOM引用？库存合计？",
      f"SELECT DISTINCT b.parent_code, p.product_name, COALESCE(SUM(inv.quantity),0) as inv_qty FROM {T['PO']} po JOIN {T['SU']} su ON po.supplier_id=su.supplier_id JOIN {T['PO']} po2 ON su.supplier_id=po2.supplier_id JOIN {T['B']} b ON po2.material_code=b.child_code JOIN {T['P']} p ON b.parent_code=p.product_code LEFT JOIN {T['INV']} inv ON p.product_code=inv.item_code WHERE po.purchase_order_number='PO-2024040001' GROUP BY b.parent_code, p.product_name")

    a("Q24", "SH-202305-0002产品BOM物料采购供应商有高风险的吗？",
      f"SELECT DISTINCT su.supplier_name, su.supplier_code, su.risk_level FROM {T['SH']} sh JOIN {T['B']} b ON sh.product_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code JOIN {T['SU']} su ON po.supplier_id=su.supplier_id WHERE sh.shipment_number='SH-202305-0002' AND su.risk_level='高'")

    a("Q25", "WH001存放产品BOM中有损耗物料的供应商风险等级分布？",
      f"SELECT su.risk_level, COUNT(DISTINCT su.supplier_code) as cnt FROM {T['INV']} inv JOIN {T['B']} b ON inv.item_code=b.parent_code JOIN {T['PO']} po ON b.child_code=po.material_code JOIN {T['SU']} su ON po.supplier_id=su.supplier_id WHERE inv.warehouse_id IN (SELECT warehouse_id FROM {T['WH']} WHERE warehouse_id='WH001') AND b.scrap_rate>0 GROUP BY su.risk_level")

    return results


def format_report(sid, title, results, answers_ref):
    lines = [f"# {sid} {title} — 数据库查询答案\n"]
    lines.append(f"> 查询方式: kweaver dataview query (mdl-uniquery SQL)")
    lines.append(f"> 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")

    ok_count = 0
    for item in results:
        qid = item["qid"]
        r = item["result"]
        lines.append(f"## {qid}\n")
        lines.append(f"**问题**: {item['question']}\n")
        lines.append(f"**SQL**:\n```sql\n{item['sql']}\n```\n")

        if "error" in r:
            lines.append(f"**结果**: ERROR — {r['error']}\n")
        else:
            entries = r.get("entries", [])
            ms = r.get("overall_ms", "?")
            lines.append(f"**查询耗时**: {ms}ms | **返回行数**: {len(entries)}\n")
            if entries:
                lines.append("**数据**:\n```json")
                lines.append(json.dumps(entries, ensure_ascii=False, indent=2, default=str)[:2000])
                lines.append("```\n")
                ok_count += 1
            else:
                lines.append("**数据**: (无结果)\n")

        lines.append("---\n")

    lines.append(f"\n## 小结\n")
    lines.append(f"- 成功查询: {ok_count}/{len(results)}")
    lines.append(f"- 查询出错或无结果: {len(results) - ok_count}/{len(results)}\n")
    return "\n".join(lines)


def main():
    target = set(sys.argv[1:]) if len(sys.argv) > 1 else {"S1", "S2", "S3", "S4"}

    groups = {
        "S1": ("S1", "直接对象问答", run_s1),
        "S2": ("S2", "2跳问答", run_s2),
        "S3": ("S3", "3跳问答", run_s3),
        "S4": ("S4", "4跳问答", run_s4),
    }

    all_results = {}
    for key in sorted(target):
        if key not in groups:
            continue
        sid, title, func = groups[key]
        print(f"\n{'='*60}")
        print(f" {sid} {title}")
        print(f"{'='*60}")
        results = func()
        all_results[key] = results

        report = format_report(sid, title, results, None)
        out = os.path.join(REPORT_DIR, f"{sid}_{title}_DB答案.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n  Report saved: {out}")

    print(f"\n{'='*60}")
    print(" ALL DONE")
    print(f"{'='*60}")
    for key in sorted(all_results):
        res = all_results[key]
        ok = sum(1 for r in res if "error" not in r["result"] and r["result"].get("entries"))
        print(f"  {key}: {ok}/{len(res)} queries returned data")


if __name__ == "__main__":
    main()
