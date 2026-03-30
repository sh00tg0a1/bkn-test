#!/usr/bin/env python3.12
"""
Suite-2 全量测试脚本：连接 hd_supply MySQL 数据库，逐题查询并输出答案。
运行前先执行 explore_schema.py 确认表名和字段名，然后根据实际 schema 调整查询。

用法:
    python3.12 scripts/suite2/run_all_questions.py          # 运行全部
    python3.12 scripts/suite2/run_all_questions.py S1       # 只跑 S1
    python3.12 scripts/suite2/run_all_questions.py S1 S2    # 跑 S1+S2
"""
from __future__ import annotations
import json
import os
import sys
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from db_config import get_connection

REPORT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "test_report", "suite-2", "db_answers"
)
os.makedirs(REPORT_DIR, exist_ok=True)


def q(cur, sql, params=None):
    """Execute SQL and return list of dicts."""
    cur.execute(sql, params or ())
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def scalar(cur, sql, params=None):
    cur.execute(sql, params or ())
    row = cur.fetchone()
    return row[0] if row else None


# ---------------------------------------------------------------------------
# IMPORTANT: The queries below use GUESSED table/column names based on the
# test-case answers. After running explore_schema.py, replace them with the
# actual names found in the database.
#
# Naming convention assumed (adjust after schema exploration):
#   products, materials, bom, customers, suppliers,
#   purchase_orders, sales_orders, inventory,
#   warehouses, factories, production_orders,
#   shipments (产品发货物流单), material_deliveries (物料发货单),
#   material_requisitions (物料领料单)
# ---------------------------------------------------------------------------


# ===== S1: 直接对象问答 =====
def s1_questions(cur):
    results = []

    # Q01: 旋风基础版整机（UAV-XF-BASIC）在中央成品仓的库存
    try:
        rows = q(cur, """
            SELECT i.quantity, i.warehouse_code, w.warehouse_name
            FROM inventory i
            JOIN warehouses w ON i.warehouse_code = w.warehouse_code
            WHERE i.material_code = 'UAV-XF-BASIC'
              AND w.warehouse_code = 'WH001'
        """)
        if not rows:
            rows = q(cur, """
                SELECT i.* FROM inventory i
                WHERE i.material_code LIKE '%XF-BASIC%'
                  AND i.warehouse_code = 'WH001'
            """)
        ans = f"查询结果: {json.dumps(rows, ensure_ascii=False, default=str)}"
        total = sum(r.get('quantity', 0) for r in rows)
        ans += f"\n库存数量: {total}台"
        results.append(("Q01", "旋风基础版整机在中央成品仓库存", ans))
    except Exception as e:
        results.append(("Q01", "旋风基础版整机在中央成品仓库存", f"ERROR: {e}"))

    # Q02: 采购订单PO-2024040001预计到货时间
    try:
        rows = q(cur, """
            SELECT * FROM purchase_orders
            WHERE po_number LIKE '%PO-2024040001%' OR po_number LIKE '%2024040001%'
        """)
        if not rows:
            rows = q(cur, "SELECT * FROM purchase_orders LIMIT 3")
            ans = f"未找到PO-2024040001，采样数据: {json.dumps(rows, ensure_ascii=False, default=str)[:300]}"
        else:
            ans = f"planned_arrival_date: {rows[0].get('planned_arrival_date', 'N/A')}"
        results.append(("Q02", "PO-2024040001预计到货时间", ans))
    except Exception as e:
        results.append(("Q02", "PO-2024040001预计到货时间", f"ERROR: {e}"))

    # Q03: 发货单SH-202305-0001预计送达
    try:
        rows = q(cur, """
            SELECT * FROM shipments
            WHERE shipment_number LIKE '%SH-202305-0001%' OR shipment_number LIKE '%202305-0001%'
        """)
        if rows:
            ans = f"estimated_delivery_date: {rows[0].get('estimated_delivery_date', 'N/A')}"
        else:
            ans = "未找到该发货单"
        results.append(("Q03", "SH-202305-0001预计送达", ans))
    except Exception as e:
        results.append(("Q03", "SH-202305-0001预计送达", f"ERROR: {e}"))

    # Q04: 发货单SH-202305-0002实际签收日期
    try:
        rows = q(cur, """
            SELECT * FROM shipments
            WHERE shipment_number LIKE '%SH-202305-0002%'
        """)
        if rows:
            ans = f"actual_delivery_date: {rows[0].get('actual_delivery_date', 'N/A')}"
        else:
            ans = "未找到该发货单"
        results.append(("Q04", "SH-202305-0002实际签收日期", ans))
    except Exception as e:
        results.append(("Q04", "SH-202305-0002实际签收日期", f"ERROR: {e}"))

    # Q05: SO-202303-00001订单状态
    try:
        rows = q(cur, """
            SELECT * FROM sales_orders
            WHERE so_number LIKE '%SO-202303-00001%'
        """)
        if rows:
            ans = f"order_status: {rows[0].get('order_status', 'N/A')}"
        else:
            ans = "未找到该销售订单"
        results.append(("Q05", "SO-202303-00001订单状态", ans))
    except Exception as e:
        results.append(("Q05", "SO-202303-00001订单状态", f"ERROR: {e}"))

    # Q06: 广州绿野是否重点客户
    try:
        rows = q(cur, """
            SELECT * FROM customers
            WHERE customer_name LIKE '%广州绿野%' OR customer_code = 'CUST-10001'
        """)
        if rows:
            ans = f"is_named_customer: {rows[0].get('is_named_customer', 'N/A')}"
        else:
            ans = "未找到该客户"
        results.append(("Q06", "广州绿野是否重点客户", ans))
    except Exception as e:
        results.append(("Q06", "广州绿野是否重点客户", f"ERROR: {e}"))

    # Q07: 西安沃土是否签合同
    try:
        rows = q(cur, """
            SELECT * FROM customers
            WHERE customer_name LIKE '%西安沃土%' OR customer_code = 'CUST-10002'
        """)
        if rows:
            ans = f"has_contract: {rows[0].get('has_contract', 'N/A')}"
        else:
            ans = "未找到该客户"
        results.append(("Q07", "西安沃土是否签合同", ans))
    except Exception as e:
        results.append(("Q07", "西安沃土是否签合同", f"ERROR: {e}"))

    # Q08: 索尼半导体风险评级
    try:
        rows = q(cur, """
            SELECT * FROM suppliers
            WHERE supplier_name LIKE '%索尼%' OR supplier_code = 'SUP-021'
        """)
        if rows:
            ans = f"risk_level: {rows[0].get('risk_level', 'N/A')}"
        else:
            ans = "未找到该供应商"
        results.append(("Q08", "索尼半导体风险评级", ans))
    except Exception as e:
        results.append(("Q08", "索尼半导体风险评级", f"ERROR: {e}"))

    # Q09: 博世传感器平均交期
    try:
        rows = q(cur, """
            SELECT * FROM suppliers
            WHERE supplier_name LIKE '%博世%' OR supplier_code = 'SUP-004'
        """)
        if rows:
            ans = f"lead_time_avg: {rows[0].get('lead_time_avg', 'N/A')}天"
        else:
            ans = "未找到该供应商"
        results.append(("Q09", "博世传感器平均交期", ans))
    except Exception as e:
        results.append(("Q09", "博世传感器平均交期", f"ERROR: {e}"))

    # Q10: 芯源微电子付款条件
    try:
        rows = q(cur, """
            SELECT * FROM suppliers
            WHERE supplier_name LIKE '%芯源%' OR supplier_code = 'SUP-001'
        """)
        if rows:
            ans = f"payment_terms: {rows[0].get('payment_terms', 'N/A')}"
        else:
            ans = "未找到该供应商"
        results.append(("Q10", "芯源微电子付款条件", ans))
    except Exception as e:
        results.append(("Q10", "芯源微电子付款条件", f"ERROR: {e}"))

    # Q11: MO-202305001计划完工日期
    try:
        rows = q(cur, """
            SELECT * FROM production_orders
            WHERE work_order_number LIKE '%MO-202305001%'
        """)
        if rows:
            ans = f"planned_finish_date: {rows[0].get('planned_finish_date', 'N/A')}"
        else:
            ans = "未找到该生产工单"
        results.append(("Q11", "MO-202305001计划完工日期", ans))
    except Exception as e:
        results.append(("Q11", "MO-202305001计划完工日期", f"ERROR: {e}"))

    # Q12: MO-202305001工单状态
    try:
        rows = q(cur, """
            SELECT * FROM production_orders
            WHERE work_order_number LIKE '%MO-202305001%'
        """)
        if rows:
            ans = f"work_order_status: {rows[0].get('work_order_status', 'N/A')}"
        else:
            ans = "未找到该生产工单"
        results.append(("Q12", "MO-202305001工单状态", ans))
    except Exception as e:
        results.append(("Q12", "MO-202305001工单状态", f"ERROR: {e}"))

    # Q13: PO-2024040001含税总金额
    try:
        rows = q(cur, """
            SELECT * FROM purchase_orders
            WHERE po_number LIKE '%PO-2024040001%'
        """)
        if rows:
            ans = f"total_amount_tax: {rows[0].get('total_amount_tax', 'N/A')}元"
        else:
            ans = "未找到该采购订单"
        results.append(("Q13", "PO-2024040001含税总金额", ans))
    except Exception as e:
        results.append(("Q13", "PO-2024040001含税总金额", f"ERROR: {e}"))

    # Q14: PO-2023040002采购员
    try:
        rows = q(cur, """
            SELECT * FROM purchase_orders
            WHERE po_number LIKE '%PO-2023040002%'
        """)
        if rows:
            ans = f"buyer: {rows[0].get('buyer', 'N/A')}"
        else:
            ans = "未找到该采购订单"
        results.append(("Q14", "PO-2023040002采购员", ans))
    except Exception as e:
        results.append(("Q14", "PO-2023040002采购员", f"ERROR: {e}"))

    # Q15: PO-2024040001单据状态
    try:
        rows = q(cur, """
            SELECT * FROM purchase_orders
            WHERE po_number LIKE '%PO-2024040001%'
        """)
        if rows:
            ans = f"document_status: {rows[0].get('document_status', 'N/A')}"
        else:
            ans = "未找到该采购订单"
        results.append(("Q15", "PO-2024040001单据状态", ans))
    except Exception as e:
        results.append(("Q15", "PO-2024040001单据状态", f"ERROR: {e}"))

    # Q16: SO-202303-00001折扣
    try:
        rows = q(cur, """
            SELECT * FROM sales_orders
            WHERE so_number LIKE '%SO-202303-00001%'
        """)
        if rows:
            ans = f"discount_rate: {rows[0].get('discount_rate', 'N/A')}"
        else:
            ans = "未找到该销售订单"
        results.append(("Q16", "SO-202303-00001折扣", ans))
    except Exception as e:
        results.append(("Q16", "SO-202303-00001折扣", f"ERROR: {e}"))

    # Q17: SO-202303-00001交货日期
    try:
        rows = q(cur, """
            SELECT * FROM sales_orders
            WHERE so_number LIKE '%SO-202303-00001%'
        """)
        if rows:
            ans = f"planned_delivery_date: {rows[0].get('planned_delivery_date', 'N/A')}"
        else:
            ans = "未找到该销售订单"
        results.append(("Q17", "SO-202303-00001交货日期", ans))
    except Exception as e:
        results.append(("Q17", "SO-202303-00001交货日期", f"ERROR: {e}"))

    # Q18: SH-202305-0001物流商
    try:
        rows = q(cur, """
            SELECT * FROM shipments
            WHERE shipment_number LIKE '%SH-202305-0001%'
        """)
        if rows:
            ans = f"logistics_provider: {rows[0].get('logistics_provider', 'N/A')}"
        else:
            ans = "未找到该发货单"
        results.append(("Q18", "SH-202305-0001物流商", ans))
    except Exception as e:
        results.append(("Q18", "SH-202305-0001物流商", f"ERROR: {e}"))

    # Q19: PO-202303-961422验收结果
    try:
        rows = q(cur, """
            SELECT * FROM material_deliveries
            WHERE delivery_number LIKE '%PO-202303-961422%'
        """)
        if rows:
            ans = f"inspection_status: {rows[0].get('inspection_status', 'N/A')}"
        else:
            ans = "未找到该物料发货单"
        results.append(("Q19", "PO-202303-961422验收结果", ans))
    except Exception as e:
        results.append(("Q19", "PO-202303-961422验收结果", f"ERROR: {e}"))

    # Q20: 中央成品仓WMS
    try:
        rows = q(cur, """
            SELECT * FROM warehouses
            WHERE warehouse_code = 'WH001'
        """)
        if rows:
            ans = f"has_wms: {rows[0].get('has_wms', 'N/A')}, wms_system: {rows[0].get('wms_system', 'N/A')}"
        else:
            ans = "未找到该仓库"
        results.append(("Q20", "中央成品仓WMS", ans))
    except Exception as e:
        results.append(("Q20", "中央成品仓WMS", f"ERROR: {e}"))

    # Q21: FAC001生产线
    try:
        rows = q(cur, """
            SELECT * FROM factories
            WHERE factory_code = 'FAC001'
        """)
        if rows:
            ans = f"production_lines: {rows[0].get('production_lines', 'N/A')}"
        else:
            ans = "未找到该工厂"
        results.append(("Q21", "FAC001生产线", ans))
    except Exception as e:
        results.append(("Q21", "FAC001生产线", f"ERROR: {e}"))

    # Q22: ASSY-BODY-PLA-01是自制还是外购
    try:
        rows = q(cur, """
            SELECT * FROM materials
            WHERE material_code = 'ASSY-BODY-PLA-01'
        """)
        if rows:
            ans = f"is_assembly: {rows[0].get('is_assembly', 'N/A')}, material_type: {rows[0].get('material_type', 'N/A')}"
        else:
            ans = "未找到该物料"
        results.append(("Q22", "ASSY-BODY-PLA-01自制/外购", ans))
    except Exception as e:
        results.append(("Q22", "ASSY-BODY-PLA-01自制/外购", f"ERROR: {e}"))

    # Q23: PART-CAM-FIX-12MP计量单位
    try:
        rows = q(cur, """
            SELECT * FROM materials
            WHERE material_code = 'PART-CAM-FIX-12MP'
        """)
        if rows:
            ans = f"unit: {rows[0].get('unit', 'N/A')}"
        else:
            ans = "未找到该物料"
        results.append(("Q23", "PART-CAM-FIX-12MP计量单位", ans))
    except Exception as e:
        results.append(("Q23", "PART-CAM-FIX-12MP计量单位", f"ERROR: {e}"))

    # Q24: UAV-BF-IND-H20销售计量单位
    try:
        rows = q(cur, """
            SELECT * FROM products
            WHERE product_code = 'UAV-BF-IND-H20'
        """)
        if not rows:
            rows = q(cur, "SELECT * FROM products WHERE product_code LIKE '%BF-IND-H20%'")
        if rows:
            ans = f"main_unit: {rows[0].get('main_unit', 'N/A')}"
        else:
            ans = "未找到该产品"
        results.append(("Q24", "UAV-BF-IND-H20销售单位", ans))
    except Exception as e:
        results.append(("Q24", "UAV-BF-IND-H20销售单位", f"ERROR: {e}"))

    # Q25: REQ-MO202305001-P0001-30领料状态
    try:
        rows = q(cur, """
            SELECT * FROM material_requisitions
            WHERE requisition_number LIKE '%REQ-MO202305001-P0001-30%'
        """)
        if rows:
            ans = f"status: {rows[0].get('status', 'N/A')}"
        else:
            ans = "未找到该领料单"
        results.append(("Q25", "REQ-MO202305001-P0001-30领料状态", ans))
    except Exception as e:
        results.append(("Q25", "REQ-MO202305001-P0001-30领料状态", f"ERROR: {e}"))

    return results


# ===== S2: 2跳问答 =====
def s2_questions(cur):
    results = []

    # Q01: PO-2024040001 物料 + 零件/组件
    try:
        rows = q(cur, """
            SELECT po.*, m.material_name, m.material_type, m.is_assembly
            FROM purchase_orders po
            JOIN materials m ON po.material_code = m.material_code
            WHERE po.po_number LIKE '%PO-2024040001%'
        """)
        results.append(("Q01", "PO-2024040001物料类型", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q01", "PO-2024040001物料类型", f"ERROR: {e}"))

    # Q02: PO-2024040001供应商交期
    try:
        rows = q(cur, """
            SELECT po.po_number, s.supplier_name, s.lead_time_avg
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_code = s.supplier_code
            WHERE po.po_number LIKE '%PO-2024040001%'
        """)
        results.append(("Q02", "PO-2024040001供应商交期", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q02", "PO-2024040001供应商交期", f"ERROR: {e}"))

    # Q03: PO-2024040001供应商风险
    try:
        rows = q(cur, """
            SELECT po.po_number, s.supplier_name, s.risk_level, s.supplier_tier
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_code = s.supplier_code
            WHERE po.po_number LIKE '%PO-2024040001%'
        """)
        results.append(("Q03", "PO-2024040001供应商风险", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q03", "PO-2024040001供应商风险", f"ERROR: {e}"))

    # Q04: SO-202303-00001产品+是否在产
    try:
        rows = q(cur, """
            SELECT so.so_number, so.product_code, p.product_name, p.status
            FROM sales_orders so
            JOIN products p ON so.product_code = p.product_code
            WHERE so.so_number LIKE '%SO-202303-00001%'
        """)
        results.append(("Q04", "SO-202303-00001产品状态", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q04", "SO-202303-00001产品状态", f"ERROR: {e}"))

    # Q05: 客户等级+是否加急
    try:
        rows = q(cur, """
            SELECT c.customer_name, c.customer_level, so.is_urgent
            FROM customers c
            JOIN sales_orders so ON c.customer_code = so.customer_code
            WHERE c.customer_name LIKE '%广州绿野%'
              AND so.so_number LIKE '%SO-202303-00001%'
        """)
        results.append(("Q05", "广州绿野客户等级+加急", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q05", "广州绿野客户等级+加急", f"ERROR: {e}"))

    # Q06: SH-202305-0001产品+库存单价
    try:
        rows = q(cur, """
            SELECT sh.shipment_number, sh.product_code, p.product_name, i.unit_price
            FROM shipments sh
            JOIN products p ON sh.product_code = p.product_code
            JOIN inventory i ON i.material_code = sh.product_code
            WHERE sh.shipment_number LIKE '%SH-202305-0001%'
        """)
        results.append(("Q06", "SH-202305-0001产品单价", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q06", "SH-202305-0001产品单价", f"ERROR: {e}"))

    # Q07: SH-202305-0001仓库+冷链
    try:
        rows = q(cur, """
            SELECT sh.shipment_number, w.warehouse_name, w.warehouse_code, w.has_cold_storage
            FROM shipments sh
            JOIN warehouses w ON sh.warehouse_code = w.warehouse_code
            WHERE sh.shipment_number LIKE '%SH-202305-0001%'
        """)
        results.append(("Q07", "SH-202305-0001仓库冷链", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q07", "SH-202305-0001仓库冷链", f"ERROR: {e}"))

    # Q08: MO-202305001工厂+员工数
    try:
        rows = q(cur, """
            SELECT po.work_order_number, f.factory_name, f.employee_count
            FROM production_orders po
            JOIN factories f ON po.factory_code = f.factory_code
            WHERE po.work_order_number LIKE '%MO-202305001%'
        """)
        results.append(("Q08", "MO-202305001工厂员工", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q08", "MO-202305001工厂员工", f"ERROR: {e}"))

    # Q09: MO-202305001产品+BOM版本
    try:
        rows = q(cur, """
            SELECT po.work_order_number, po.product_code, p.product_name, b.bom_version
            FROM production_orders po
            JOIN products p ON po.product_code = p.product_code
            JOIN bom b ON b.bom_material_code = po.product_code
            WHERE po.work_order_number LIKE '%MO-202305001%'
            GROUP BY b.bom_version
        """)
        results.append(("Q09", "MO-202305001产品BOM版本", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q09", "MO-202305001产品BOM版本", f"ERROR: {e}"))

    # Q10: INV0000001仓库+分拣设备
    try:
        rows = q(cur, """
            SELECT i.inventory_id, w.warehouse_name, w.has_sorting_system
            FROM inventory i
            JOIN warehouses w ON i.warehouse_code = w.warehouse_code
            WHERE i.inventory_id = 'INV0000001'
        """)
        results.append(("Q10", "INV0000001仓库分拣", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q10", "INV0000001仓库分拣", f"ERROR: {e}"))

    # Q11: UAV-XF-BASIC库存总价值
    try:
        rows = q(cur, """
            SELECT SUM(total_price) as total_value, SUM(quantity) as total_qty
            FROM inventory
            WHERE material_code = 'UAV-XF-BASIC'
        """)
        results.append(("Q11", "UAV-XF-BASIC库存总价值", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q11", "UAV-XF-BASIC库存总价值", f"ERROR: {e}"))

    # Q12: PO-202303-961422供应商+供应商级别
    try:
        rows = q(cur, """
            SELECT md.delivery_number, s.supplier_name, s.supplier_tier
            FROM material_deliveries md
            JOIN suppliers s ON md.supplier_code = s.supplier_code
            WHERE md.delivery_number LIKE '%PO-202303-961422%'
        """)
        results.append(("Q12", "PO-202303-961422供应商级别", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q12", "PO-202303-961422供应商级别", f"ERROR: {e}"))

    # Q13: PO-202303-961422入库仓库+RFID
    try:
        rows = q(cur, """
            SELECT md.delivery_number, w.warehouse_name, w.has_rfid
            FROM material_deliveries md
            JOIN warehouses w ON md.warehouse_code = w.warehouse_code
            WHERE md.delivery_number LIKE '%PO-202303-961422%'
        """)
        results.append(("Q13", "PO-202303-961422仓库RFID", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q13", "PO-202303-961422仓库RFID", f"ERROR: {e}"))

    # Q14: REQ-MO202305001-P0001-10仓库+面积
    try:
        rows = q(cur, """
            SELECT mr.requisition_number, w.warehouse_name, w.storage_area_sqm
            FROM material_requisitions mr
            JOIN warehouses w ON mr.warehouse_code = w.warehouse_code
            WHERE mr.requisition_number LIKE '%REQ-MO202305001-P0001-10%'
        """)
        results.append(("Q14", "REQ-P0001-10仓库面积", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q14", "REQ-P0001-10仓库面积", f"ERROR: {e}"))

    # Q15: REQ-MO202305001-P0001-10物料+是否组件
    try:
        rows = q(cur, """
            SELECT mr.requisition_number, m.material_name, m.is_assembly
            FROM material_requisitions mr
            JOIN materials m ON mr.material_code = m.material_code
            WHERE mr.requisition_number LIKE '%REQ-MO202305001-P0001-10%'
        """)
        results.append(("Q15", "REQ-P0001-10物料组件", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q15", "REQ-P0001-10物料组件", f"ERROR: {e}"))

    # Q16: REQ-MO202305001-P0001-10工厂+类型
    try:
        rows = q(cur, """
            SELECT mr.requisition_number, f.factory_name, f.factory_type
            FROM material_requisitions mr
            JOIN factories f ON mr.factory_code = f.factory_code
            WHERE mr.requisition_number LIKE '%REQ-MO202305001-P0001-10%'
        """)
        results.append(("Q16", "REQ-P0001-10工厂类型", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q16", "REQ-P0001-10工厂类型", f"ERROR: {e}"))

    # Q17: UAV-XF-BASIC BOM V2.0物料
    try:
        rows = q(cur, """
            SELECT b.child_code, b.child_name, b.quantity_per, b.scrap_rate
            FROM bom b
            WHERE b.bom_material_code = 'UAV-XF-BASIC' AND b.bom_version = 'V2.0'
        """)
        results.append(("Q17", "UAV-XF-BASIC BOM V2.0", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q17", "UAV-XF-BASIC BOM V2.0", f"ERROR: {e}"))

    # Q18: PART-CAM-FIX-12MP被用在哪个产品
    try:
        rows = q(cur, """
            SELECT b.bom_material_code, p.product_name, b.bom_version, b.quantity_per, b.scrap_rate
            FROM bom b
            JOIN products p ON b.bom_material_code = p.product_code
            WHERE b.child_code = 'PART-CAM-FIX-12MP'
        """)
        results.append(("Q18", "PART-CAM-FIX-12MP用于产品", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q18", "PART-CAM-FIX-12MP用于产品", f"ERROR: {e}"))

    # Q19: 广州绿野SO-202303-00001总金额
    try:
        rows = q(cur, """
            SELECT so.so_number, SUM(so.total_amount) as total
            FROM sales_orders so
            WHERE so.so_number LIKE '%SO-202303-00001%'
            GROUP BY so.so_number
        """)
        if not rows:
            rows = q(cur, """
                SELECT so_number, total_amount FROM sales_orders
                WHERE so_number LIKE '%SO-202303-00001%'
            """)
        results.append(("Q19", "SO-202303-00001总金额", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q19", "SO-202303-00001总金额", f"ERROR: {e}"))

    # Q20: UAV-XF-BASIC中央成品仓入库时间
    try:
        rows = q(cur, """
            SELECT earliest_storage_date, batch_no
            FROM inventory
            WHERE material_code = 'UAV-XF-BASIC' AND warehouse_code = 'WH001'
            ORDER BY earliest_storage_date
            LIMIT 1
        """)
        results.append(("Q20", "UAV-XF-BASIC入库时间", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q20", "UAV-XF-BASIC入库时间", f"ERROR: {e}"))

    # Q21: PO-2023040002到货数量+入库情况
    try:
        rows = q(cur, """
            SELECT po_number, purchase_quantity, accumulated_storage_tax,
                   accumulated_arrival_tax, document_status
            FROM purchase_orders
            WHERE po_number LIKE '%PO-2023040002%'
        """)
        results.append(("Q21", "PO-2023040002到货入库", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q21", "PO-2023040002到货入库", f"ERROR: {e}"))

    # Q22: SH-202305-0003客户+重点客户
    try:
        rows = q(cur, """
            SELECT sh.shipment_number, c.customer_name, c.is_named_customer
            FROM shipments sh
            JOIN customers c ON sh.customer_code = c.customer_code
            WHERE sh.shipment_number LIKE '%SH-202305-0003%'
        """)
        results.append(("Q22", "SH-202305-0003客户重点", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q22", "SH-202305-0003客户重点", f"ERROR: {e}"))

    # Q23: MO-202305002生产线+工厂产能
    try:
        rows = q(cur, """
            SELECT po.work_order_number, po.production_line, f.factory_name, f.total_capacity
            FROM production_orders po
            JOIN factories f ON po.factory_code = f.factory_code
            WHERE po.work_order_number LIKE '%MO-202305002%'
        """)
        results.append(("Q23", "MO-202305002生产线产能", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q23", "MO-202305002生产线产能", f"ERROR: {e}"))

    # Q24: PART-BAT-2S-3000 BOM损耗率
    try:
        rows = q(cur, """
            SELECT bom_material_code, child_code, child_name, scrap_rate
            FROM bom
            WHERE child_code = 'PART-BAT-2S-3000'
        """)
        results.append(("Q24", "PART-BAT-2S-3000损耗率", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q24", "PART-BAT-2S-3000损耗率", f"ERROR: {e}"))

    # Q25: SH-202305-0004交付状态
    try:
        rows = q(cur, """
            SELECT shipment_number, delivery_status, actual_delivery_date
            FROM shipments
            WHERE shipment_number LIKE '%SH-202305-0004%'
        """)
        results.append(("Q25", "SH-202305-0004交付状态", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q25", "SH-202305-0004交付状态", f"ERROR: {e}"))

    return results


# ===== S3: 3跳问答 =====
def s3_questions(cur):
    results = []

    # Q01: SO-202303-00001产品BOM零件子项
    try:
        rows = q(cur, """
            SELECT b.child_code, b.child_name, m.material_type, b.scrap_rate
            FROM sales_orders so
            JOIN bom b ON b.bom_material_code = so.product_code
            JOIN materials m ON b.child_code = m.material_code
            WHERE so.so_number LIKE '%SO-202303-00001%'
              AND m.material_type = '零件'
        """)
        results.append(("Q01", "SO-202303-00001 BOM零件", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q01", "SO-202303-00001 BOM零件", f"ERROR: {e}"))

    # Q02: SO-202303-00001产品BOM在途采购订单
    try:
        rows = q(cur, """
            SELECT DISTINCT po.po_number, po.material_code, po.document_status, m.material_name
            FROM sales_orders so
            JOIN bom b ON b.bom_material_code = so.product_code
            JOIN materials m ON b.child_code = m.material_code
            JOIN purchase_orders po ON po.material_code = m.material_code
            WHERE so.so_number LIKE '%SO-202303-00001%'
              AND po.document_status != '已关闭'
        """)
        results.append(("Q02", "SO-202303-00001在途PO", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q02", "SO-202303-00001在途PO", f"ERROR: {e}"))

    # Q03: SH-202305-0001→SO→客户等级
    try:
        rows = q(cur, """
            SELECT sh.shipment_number, so.so_number, c.customer_name, c.customer_level
            FROM shipments sh
            JOIN sales_orders so ON sh.so_number = so.so_number OR sh.customer_code = so.customer_code
            JOIN customers c ON so.customer_code = c.customer_code
            WHERE sh.shipment_number LIKE '%SH-202305-0001%'
        """)
        results.append(("Q03", "SH-202305-0001客户等级", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q03", "SH-202305-0001客户等级", f"ERROR: {e}"))

    # Q04: UAV-XF-BASIC BOM物料库存>0
    try:
        rows = q(cur, """
            SELECT b.child_code, b.child_name, i.warehouse_code, i.quantity
            FROM bom b
            JOIN inventory i ON b.child_code = i.material_code
            WHERE b.bom_material_code = 'UAV-XF-BASIC'
              AND i.quantity > 0
        """)
        results.append(("Q04", "UAV-XF-BASIC BOM有库存物料", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q04", "UAV-XF-BASIC BOM有库存物料", f"ERROR: {e}"))

    # Q05: PART-CAM-FIX-12MP采购订单延误
    try:
        rows = q(cur, """
            SELECT po_number, planned_arrival_date, required_date,
                   DATEDIFF(planned_arrival_date, required_date) as delay_days
            FROM purchase_orders
            WHERE material_code = 'PART-CAM-FIX-12MP'
        """)
        results.append(("Q05", "PART-CAM-FIX-12MP交期延误", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q05", "PART-CAM-FIX-12MP交期延误", f"ERROR: {e}"))

    # Q06: MO-202305001领料仓库+分拣
    try:
        rows = q(cur, """
            SELECT DISTINCT mr.warehouse_code, w.warehouse_name, w.has_sorting_system
            FROM material_requisitions mr
            JOIN warehouses w ON mr.warehouse_code = w.warehouse_code
            WHERE mr.work_order_number LIKE '%MO-202305001%'
        """)
        results.append(("Q06", "MO-202305001领料仓库分拣", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q06", "MO-202305001领料仓库分拣", f"ERROR: {e}"))

    # Q07: ASSY-BODY-PLA-01供应商高风险
    try:
        rows = q(cur, """
            SELECT DISTINCT s.supplier_name, s.supplier_code, s.risk_level
            FROM material_deliveries md
            JOIN suppliers s ON md.supplier_code = s.supplier_code
            WHERE md.material_code = 'ASSY-BODY-PLA-01'
        """)
        results.append(("Q07", "ASSY-BODY-PLA-01供应商风险", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q07", "ASSY-BODY-PLA-01供应商风险", f"ERROR: {e}"))

    # Q08: 广州绿野发货物流商
    try:
        rows = q(cur, """
            SELECT DISTINCT sh.logistics_provider
            FROM customers c
            JOIN sales_orders so ON c.customer_code = so.customer_code
            JOIN shipments sh ON sh.customer_code = c.customer_code
            WHERE c.customer_name LIKE '%广州绿野%'
        """)
        results.append(("Q08", "广州绿野物流商", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q08", "广州绿野物流商", f"ERROR: {e}"))

    # Q09: UAV-XF-BASIC库存仓库+负责人
    try:
        rows = q(cur, """
            SELECT DISTINCT i.warehouse_code, w.warehouse_name, w.manager_name
            FROM inventory i
            JOIN warehouses w ON i.warehouse_code = w.warehouse_code
            WHERE i.material_code = 'UAV-XF-BASIC'
        """)
        results.append(("Q09", "UAV-XF-BASIC仓库负责人", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q09", "UAV-XF-BASIC仓库负责人", f"ERROR: {e}"))

    # Q10: SUP-021物料发到仓库+类型
    try:
        rows = q(cur, """
            SELECT DISTINCT md.warehouse_code, w.warehouse_name, w.warehouse_type
            FROM material_deliveries md
            JOIN warehouses w ON md.warehouse_code = w.warehouse_code
            WHERE md.supplier_code = 'SUP-021'
        """)
        results.append(("Q10", "SUP-021仓库类型", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q10", "SUP-021仓库类型", f"ERROR: {e}"))

    # Q11: FAC001产品库存>1000
    try:
        rows = q(cur, """
            SELECT p.product_code, p.product_name, SUM(i.quantity) as total_qty
            FROM production_orders po
            JOIN products p ON po.product_code = p.product_code
            JOIN inventory i ON i.material_code = p.product_code
            WHERE po.factory_code = 'FAC001'
            GROUP BY p.product_code, p.product_name
            HAVING total_qty > 1000
        """)
        results.append(("Q11", "FAC001库存>1000产品", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q11", "FAC001库存>1000产品", f"ERROR: {e}"))

    # Q12: REQ-MO202305001-P0001-30物料→采购订单→供应商
    try:
        rows = q(cur, """
            SELECT mr.material_code, m.material_name, po.po_number, s.supplier_name
            FROM material_requisitions mr
            JOIN materials m ON mr.material_code = m.material_code
            JOIN purchase_orders po ON po.material_code = mr.material_code
            JOIN suppliers s ON po.supplier_code = s.supplier_code
            WHERE mr.requisition_number LIKE '%REQ-MO202305001-P0001-30%'
        """)
        results.append(("Q12", "REQ-P0001-30物料供应商", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q12", "REQ-P0001-30物料供应商", f"ERROR: {e}"))

    # Q13: PART-CAM-FIX-12MP来料验收状态分布
    try:
        rows = q(cur, """
            SELECT inspection_status, COUNT(*) as cnt
            FROM material_deliveries
            WHERE material_code = 'PART-CAM-FIX-12MP'
            GROUP BY inspection_status
        """)
        results.append(("Q13", "PART-CAM-FIX-12MP验收分布", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q13", "PART-CAM-FIX-12MP验收分布", f"ERROR: {e}"))

    # Q14: UAV-BF-IND-H30→工厂→认证
    try:
        rows = q(cur, """
            SELECT po.product_code, f.factory_name, f.certification
            FROM production_orders po
            JOIN factories f ON po.factory_code = f.factory_code
            WHERE po.product_code = 'UAV-BF-IND-H30'
        """)
        results.append(("Q14", "UAV-BF-IND-H30工厂认证", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q14", "UAV-BF-IND-H30工厂认证", f"ERROR: {e}"))

    # Q15: CUST-10002运输中发货单
    try:
        rows = q(cur, """
            SELECT sh.shipment_number, sh.delivery_status, sh.product_code
            FROM shipments sh
            WHERE sh.customer_code = 'CUST-10002'
              AND sh.delivery_status = '运输中'
        """)
        results.append(("Q15", "CUST-10002运输中发货", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q15", "CUST-10002运输中发货", f"ERROR: {e}"))

    # Q16: PART-BAT-2S-3000→BOM→产品→库存
    try:
        rows = q(cur, """
            SELECT b.bom_material_code, p.product_name, SUM(i.quantity) as total_qty
            FROM bom b
            JOIN products p ON b.bom_material_code = p.product_code
            LEFT JOIN inventory i ON i.material_code = p.product_code
            WHERE b.child_code = 'PART-BAT-2S-3000'
            GROUP BY b.bom_material_code, p.product_name
        """)
        results.append(("Q16", "PART-BAT-2S-3000产品库存", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q16", "PART-BAT-2S-3000产品库存", f"ERROR: {e}"))

    # Q17: CUST-10148所有订单总金额
    try:
        rows = q(cur, """
            SELECT SUM(total_amount) as grand_total, COUNT(*) as order_count
            FROM sales_orders
            WHERE customer_code = 'CUST-10148'
        """)
        results.append(("Q17", "CUST-10148订单总金额", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q17", "CUST-10148订单总金额", f"ERROR: {e}"))

    # Q18: PO-2024110005物料→BOM→产品类型
    try:
        rows = q(cur, """
            SELECT po.material_code, b.bom_material_code, p.product_name, p.product_type
            FROM purchase_orders po
            JOIN bom b ON b.child_code = po.material_code
            JOIN products p ON b.bom_material_code = p.product_code
            WHERE po.po_number LIKE '%PO-2024110005%'
        """)
        results.append(("Q18", "PO-2024110005物料产品类型", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q18", "PO-2024110005物料产品类型", f"ERROR: {e}"))

    # Q19: UAV-XF-BASIC-PLUS已签收发货单数
    try:
        rows = q(cur, """
            SELECT COUNT(*) as signed_count
            FROM shipments
            WHERE product_code = 'UAV-XF-BASIC-PLUS'
              AND delivery_status = '已签收'
        """)
        results.append(("Q19", "UAV-XF-BASIC-PLUS已签收", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q19", "UAV-XF-BASIC-PLUS已签收", f"ERROR: {e}"))

    # Q20: WH002物料采购风险高
    try:
        rows = q(cur, """
            SELECT DISTINCT md.material_code, m.material_name, s.supplier_name, s.risk_level
            FROM material_deliveries md
            JOIN materials m ON md.material_code = m.material_code
            JOIN suppliers s ON md.supplier_code = s.supplier_code
            WHERE md.warehouse_code = 'WH002'
              AND s.risk_level = '高'
        """)
        results.append(("Q20", "WH002高风险物料", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q20", "WH002高风险物料", f"ERROR: {e}"))

    # Q21: SUP-004物料→BOM→产品→库存
    try:
        rows = q(cur, """
            SELECT DISTINCT po.material_code, b.bom_material_code, p.product_name,
                   COALESCE(SUM(i.quantity), 0) as inv_qty
            FROM purchase_orders po
            JOIN bom b ON b.child_code = po.material_code
            JOIN products p ON b.bom_material_code = p.product_code
            LEFT JOIN inventory i ON i.material_code = p.product_code
            WHERE po.supplier_code = 'SUP-004'
            GROUP BY po.material_code, b.bom_material_code, p.product_name
        """)
        results.append(("Q21", "SUP-004物料产品库存", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q21", "SUP-004物料产品库存", f"ERROR: {e}"))

    # Q22: SH-202305-0003收货客户未发货订单
    try:
        rows = q(cur, """
            SELECT so.so_number, so.product_code, so.order_status
            FROM shipments sh
            JOIN sales_orders so ON so.customer_code = sh.customer_code
            WHERE sh.shipment_number LIKE '%SH-202305-0003%'
              AND so.order_status != '已发货'
        """)
        results.append(("Q22", "SH-202305-0003客户未发货订单", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q22", "SH-202305-0003客户未发货订单", f"ERROR: {e}"))

    # Q23: MO-202305003产品BOM物料采购总金额
    try:
        rows = q(cur, """
            SELECT SUM(po.total_amount_tax) as total_purchase
            FROM production_orders prd
            JOIN bom b ON b.bom_material_code = prd.product_code
            JOIN purchase_orders po ON po.material_code = b.child_code
            WHERE prd.work_order_number LIKE '%MO-202305003%'
        """)
        results.append(("Q23", "MO-202305003 BOM采购总额", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q23", "MO-202305003 BOM采购总额", f"ERROR: {e}"))

    # Q24: WH001产品未完成销售订单
    try:
        rows = q(cur, """
            SELECT DISTINCT i.material_code, p.product_name, so.so_number, so.order_status
            FROM inventory i
            JOIN products p ON i.material_code = p.product_code
            JOIN sales_orders so ON so.product_code = p.product_code
            WHERE i.warehouse_code = 'WH001'
              AND so.order_status != '已发货'
        """)
        results.append(("Q24", "WH001产品未完成SO", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q24", "WH001产品未完成SO", f"ERROR: {e}"))

    # Q25: UAV-XF-BASIC BOM损耗物料+库存够几台
    try:
        rows = q(cur, """
            SELECT b.child_code, b.child_name, b.scrap_rate, b.quantity_per,
                   COALESCE(SUM(i.quantity), 0) as total_inv,
                   FLOOR(COALESCE(SUM(i.quantity), 0) / (b.quantity_per * (1 + b.scrap_rate))) as can_produce
            FROM bom b
            LEFT JOIN inventory i ON i.material_code = b.child_code
            WHERE b.bom_material_code = 'UAV-XF-BASIC'
              AND b.scrap_rate > 0
            GROUP BY b.child_code, b.child_name, b.scrap_rate, b.quantity_per
        """)
        results.append(("Q25", "UAV-XF-BASIC损耗物料产能", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q25", "UAV-XF-BASIC损耗物料产能", f"ERROR: {e}"))

    return results


# ===== S4: 4跳问答 =====
def s4_questions(cur):
    results = []

    # Q01: 广州绿野产品BOM物料高风险供应商
    try:
        rows = q(cur, """
            SELECT DISTINCT s.supplier_name, s.risk_level, po.material_code
            FROM customers c
            JOIN sales_orders so ON c.customer_code = so.customer_code
            JOIN bom b ON b.bom_material_code = so.product_code
            JOIN purchase_orders po ON po.material_code = b.child_code
            JOIN suppliers s ON po.supplier_code = s.supplier_code
            WHERE c.customer_name LIKE '%广州绿野%'
              AND s.risk_level = '高'
        """)
        results.append(("Q01", "广州绿野BOM高风险供应商", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q01", "广州绿野BOM高风险供应商", f"ERROR: {e}"))

    # Q02: 广州绿野产品BOM物料库存>500
    try:
        rows = q(cur, """
            SELECT b.child_code, b.child_name, COALESCE(SUM(i.quantity), 0) as inv_qty,
                   CASE WHEN COALESCE(SUM(i.quantity), 0) > 500 THEN '充足' ELSE '不足' END as status
            FROM customers c
            JOIN sales_orders so ON c.customer_code = so.customer_code
            JOIN bom b ON b.bom_material_code = so.product_code
            LEFT JOIN inventory i ON i.material_code = b.child_code
            WHERE c.customer_name LIKE '%广州绿野%'
            GROUP BY b.child_code, b.child_name
        """)
        results.append(("Q02", "广州绿野BOM物料库存", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q02", "广州绿野BOM物料库存", f"ERROR: {e}"))

    # Q03: SH-202305-0001产品BOM物料逾期PO
    try:
        rows = q(cur, """
            SELECT po.po_number, po.material_code, po.planned_arrival_date, po.required_date,
                   DATEDIFF(po.planned_arrival_date, po.required_date) as delay
            FROM shipments sh
            JOIN bom b ON b.bom_material_code = sh.product_code
            JOIN purchase_orders po ON po.material_code = b.child_code
            WHERE sh.shipment_number LIKE '%SH-202305-0001%'
              AND po.planned_arrival_date > po.required_date
        """)
        results.append(("Q03", "SH-202305-0001 BOM逾期PO", json.dumps(rows, ensure_ascii=False, default=str)[:600]))
    except Exception as e:
        results.append(("Q03", "SH-202305-0001 BOM逾期PO", f"ERROR: {e}"))

    # Q04: FAC001产品物流商占比
    try:
        rows = q(cur, """
            SELECT sh.logistics_provider, COUNT(*) as cnt
            FROM production_orders po
            JOIN shipments sh ON sh.product_code = po.product_code
            WHERE po.factory_code = 'FAC001'
            GROUP BY sh.logistics_provider
            ORDER BY cnt DESC
        """)
        results.append(("Q04", "FAC001产品物流商占比", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q04", "FAC001产品物流商占比", f"ERROR: {e}"))

    # Q05: WH001产品客户T1数量
    try:
        rows = q(cur, """
            SELECT COUNT(DISTINCT c.customer_code) as t1_count
            FROM inventory i
            JOIN sales_orders so ON so.product_code = i.material_code
            JOIN customers c ON so.customer_code = c.customer_code
            WHERE i.warehouse_code = 'WH001'
              AND c.customer_level = 'T1'
        """)
        results.append(("Q05", "WH001产品T1客户数", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q05", "WH001产品T1客户数", f"ERROR: {e}"))

    # Q06: PART-CAM-FIX-12MP产品T1客户
    try:
        rows = q(cur, """
            SELECT DISTINCT c.customer_name, c.customer_code, c.customer_level
            FROM bom b
            JOIN shipments sh ON sh.product_code = b.bom_material_code
            JOIN customers c ON sh.customer_code = c.customer_code
            WHERE b.child_code = 'PART-CAM-FIX-12MP'
              AND c.customer_level = 'T1'
        """)
        results.append(("Q06", "PART-CAM-FIX-12MP T1客户", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q06", "PART-CAM-FIX-12MP T1客户", f"ERROR: {e}"))

    # Q07: SUP-021物料→产品→工厂→认证
    try:
        rows = q(cur, """
            SELECT DISTINCT p.product_name, f.factory_name, f.certification
            FROM purchase_orders po
            JOIN bom b ON b.child_code = po.material_code
            JOIN products p ON b.bom_material_code = p.product_code
            JOIN production_orders prd ON prd.product_code = p.product_code
            JOIN factories f ON prd.factory_code = f.factory_code
            WHERE po.supplier_code = 'SUP-021'
        """)
        results.append(("Q07", "SUP-021产品工厂认证", json.dumps(rows, ensure_ascii=False, default=str)[:400]))
    except Exception as e:
        results.append(("Q07", "SUP-021产品工厂认证", f"ERROR: {e}"))

    # Q08-Q25 follow the same pattern with increasing complexity
    for qnum in range(8, 26):
        qid = f"Q{qnum:02d}"
        try:
            results.append((qid, f"S4-{qid}（需schema后补全）", "PLACEHOLDER: 需先探索schema后调整SQL"))
        except Exception as e:
            results.append((qid, f"S4-{qid}", f"ERROR: {e}"))

    return results


def format_report(group_name, group_title, results):
    lines = [f"# {group_name} {group_title} — 数据库查询答案\n"]
    lines.append(f"> 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")

    for qid, desc, ans in results:
        lines.append(f"## {qid}\n")
        lines.append(f"**问题简述**: {desc}\n")
        lines.append(f"**查询结果**:\n```\n{ans}\n```\n")
        lines.append("---\n")

    ok = sum(1 for _, _, a in results if not a.startswith("ERROR") and a != "PLACEHOLDER: 需先探索schema后调整SQL")
    lines.append(f"\n## 小结\n")
    lines.append(f"- 已回答: {ok}/{len(results)}\n")
    lines.append(f"- 查询出错: {len(results) - ok}/{len(results)}\n")

    return "\n".join(lines)


def main():
    target_groups = set(sys.argv[1:]) if len(sys.argv) > 1 else {"S1", "S2", "S3", "S4"}

    conn = get_connection()
    cur = conn.cursor()

    groups = {
        "S1": ("S1", "直接对象问答", s1_questions),
        "S2": ("S2", "2跳问答", s2_questions),
        "S3": ("S3", "3跳问答", s3_questions),
        "S4": ("S4", "4跳问答", s4_questions),
    }

    for key in sorted(target_groups):
        if key not in groups:
            print(f"Unknown group: {key}")
            continue
        sid, title, func = groups[key]
        print(f"\n{'='*60}")
        print(f"Running {sid} {title}...")
        print(f"{'='*60}")

        try:
            results = func(cur)
        except Exception as e:
            print(f"FATAL: {traceback.format_exc()}")
            continue

        report = format_report(sid, title, results)
        out_file = os.path.join(REPORT_DIR, f"{sid}_{title}_DB答案.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved: {out_file}")

        for qid, desc, ans in results:
            status = "OK" if not ans.startswith("ERROR") else "ERR"
            print(f"  [{status}] {qid}: {desc}")

    cur.close()
    conn.close()
    print("\nDone!")


if __name__ == "__main__":
    main()
