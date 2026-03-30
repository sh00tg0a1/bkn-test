# -*- coding: utf-8 -*-
"""
Compute gold-standard facts from ref/suite-3/supplychaindata_1 CSVs.
Run: python3 scripts/suite3/compute_answers.py
"""
from __future__ import absolute_import, print_function

import json
import os
import sys

# Allow import when cwd is project root or scripts/suite3
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from data_loader import DATA_DIR, load_all, to_float, to_int  # noqa: E402


def _rows_by_key(rows, key, val):
    return [r for r in rows if r.get(key) == val]


def compute_facts(tables):
    """Return dict of reusable facts for suite-3 QA gold answers."""
    bom = tables["bom_event_202603261810.csv"]
    inv = tables["inventory_event_202603261811.csv"]
    prod = tables["product_entity_202603261815.csv"]
    mat = tables["material_entity_202603261811.csv"]
    fcst = tables["forecast_event_202603261821.csv"]
    mrp = tables["mrp_plan_order_event_202603261821.csv"]
    po = tables["purchase_order_event_202603261815.csv"]
    pr = tables["purchase_requisition_event_202603261821.csv"]
    mrp_proc = tables["material_procurement_event_202603261812.csv"]
    wh = tables["warehouse_entity_202603261820.csv"]
    sup = tables["supplier_entity_202603261819.csv"]
    cust = tables["customer_entity_202603261810.csv"]
    mo = tables["production_order_event_202603261815.csv"]
    so = tables["sales_order_event_202603261816.csv"]
    ship = tables["shipment_event_202603261816.csv"]
    mreq = tables["material_requisition_event_202603261812.csv"]

    facts = {}

    # --- Product P0001 / UAV-XF-BASIC inventory ---
    p1_inv = [
        r
        for r in inv
        if r.get("item_type") == "Product"
        and r.get("item_code") == "UAV-XF-BASIC"
        and r.get("warehouse_id") == "WH001"
        and r.get("snapshot_month") == "2023-05"
    ]
    facts["inv_p0001_wh001_202305_qty"] = sum(to_float(r.get("quantity")) for r in p1_inv)

    # --- Forecast MDS-202604-001 rows ---
    f_mds = [r for r in fcst if r.get("billno") == "MDS-202604-001"]
    facts["forecast_mds_202604_001_count"] = len(f_mds)
    facts["forecast_mds_202604_001_qty_sum"] = sum(to_float(r.get("qty")) for r in f_mds)

    # --- MRP for root demand MDS-202604-001 ---
    mrp_mds = [r for r in mrp if r.get("rootdemandbillno") == "MDS-202604-001"]
    facts["mrp_mds_202604_001_line_count"] = len(mrp_mds)

    def short(r):
        return to_float(r.get("bizdropqty", 0)) > 0

    short_rows = [r for r in mrp_mds if short(r)]
    facts["mrp_mds_202604_001_shortage_material_count"] = len(short_rows)
    facts["mrp_mds_202604_001_shortage_bizdropqty_sum"] = sum(
        to_float(r.get("bizdropqty")) for r in short_rows
    )

    # Top 5 shortage by bizdropqty
    short_sorted = sorted(short_rows, key=lambda x: to_float(x.get("bizdropqty")), reverse=True)
    facts["mrp_mds_202604_001_top5_shortage_codes"] = [
        r.get("materialplanid_number") for r in short_sorted[:5]
    ]

    # Warehouse count
    facts["warehouse_count"] = len(wh)

    # Supplier SUP-001
    sup001 = [r for r in sup if r.get("supplier_code") == "SUP-001"]
    if sup001:
        facts["sup_001_payment_terms"] = sup001[0].get("payment_terms")
        facts["sup_001_lead_time_avg"] = sup001[0].get("lead_time_avg")

    # BOM depth for P0001: max levels from bom rows parent P0001
    bom_p1 = [r for r in bom if r.get("parent_code") == "UAV-XF-BASIC" or r.get("parent_id") == "P0001"]
    # file uses parent_code UAV-XF-BASIC for product
    bom_p1 = [r for r in bom if r.get("parent_code") == "UAV-XF-BASIC"]
    facts["bom_uav_xf_basic_direct_line_count"] = len(bom_p1)

    # BOM max line_number for structure
    # Count distinct child under parent
    children = set(r.get("child_code") for r in bom_p1)
    facts["bom_uav_xf_basic_direct_children"] = len(children)

    # Purchase orders for material PART-IMU-ADIS16505 linked to MRP (sample)
    po_imu = [r for r in po if "PART-IMU" in (r.get("material_code") or "")]
    facts["po_count_imu_material"] = len(po_imu)

    # PRs for MRP-202604-0001
    pr_mrp = [r for r in pr if r.get("srcbillid") == "MRP-202604-0001"]
    facts["pr_count_for_mrp_202604_0001"] = len(pr_mrp)

    # Customer CUST-10001 style: customer_id 10001
    c10001 = [r for r in cust if r.get("customer_id") == "10001"]
    if c10001:
        facts["cust_10001_named"] = c10001[0].get("is_named_customer")
        facts["cust_10001_contract"] = c10001[0].get("has_contract")

    # Materials total
    facts["material_entity_count"] = len(mat)

    # M0001 total qty 2023-05 all warehouses (Material item_id)
    m0001_inv = [
        r
        for r in inv
        if r.get("item_type") == "Material"
        and r.get("item_id") == "M0001"
        and r.get("snapshot_month") == "2023-05"
    ]
    facts["inv_m0001_all_wh_202305_qty_sum"] = sum(to_float(r.get("quantity")) for r in m0001_inv)

    # Shortage rows WH001 2023-05
    wh1_short = [
        r
        for r in inv
        if r.get("warehouse_id") == "WH001"
        and r.get("snapshot_month") == "2023-05"
        and (r.get("shortage_flag") or "").strip() == "是"
    ]
    facts["inv_wh001_202305_shortage_flag_rows"] = len(wh1_short)

    # Max availabledate MDS-202604-001
    dates_mds = [r.get("availabledate") for r in mrp_mds if r.get("availabledate")]
    facts["mrp_mds_202604_001_max_availabledate"] = max(dates_mds) if dates_mds else ""

    # Supplier SUP-021 Sony
    s21 = [r for r in sup if r.get("supplier_code") == "SUP-021"]
    if s21:
        facts["sup_021_risk"] = s21[0].get("risk_level")
        facts["sup_021_lead"] = s21[0].get("lead_time_avg")

    # BOM max depth: count distinct levels - bom may have line_number; compute max depth from multi-level
    # Simple: count rows where parent chains exist - use max of nested children under UAV-XF-BASIC
    def bom_depth_for_product():
        by_parent = {}
        for r in bom:
            p = r.get("parent_code") or ""
            c = r.get("child_code") or ""
            by_parent.setdefault(p, []).append(c)
        # BFS from UAV-XF-BASIC
        from collections import deque

        root = "UAV-XF-BASIC"
        depth = 0
        q = deque([(root, 0)])
        seen = set()
        max_d = 0
        while q:
            node, d = q.popleft()
            max_d = max(max_d, d)
            for ch in by_parent.get(node, []):
                if (node, ch) in seen:
                    continue
                seen.add((node, ch))
                q.append((ch, d + 1))
        return max_d

    facts["bom_uav_xf_basic_max_depth_levels"] = bom_depth_for_product()

    # Suppliers count
    facts["supplier_entity_count"] = len(sup)

    # Products total
    facts["product_entity_count"] = len(prod)

    # Forecast rows total
    facts["forecast_row_count"] = len(fcst)

    # MRP rows for MDS-202605-001
    mrp_mds605 = [r for r in mrp if r.get("rootdemandbillno") == "MDS-202605-001"]
    facts["mrp_mds_202605_001_line_count"] = len(mrp_mds605)

    # Inventory shortage flags
    inv_short = [r for r in inv if (r.get("shortage_flag") or "").strip() == "是"]
    facts["inventory_shortage_rows"] = len(inv_short)

    # First PO for planned_arrival_date sample
    if po:
        facts["sample_po_first_planned_arrival"] = po[0].get("planned_arrival_date")

    # Shipment count
    facts["shipment_count"] = len(ship)

    # Sales order count (lines)
    facts["sales_order_line_count"] = len(so)

    # Production orders
    facts["production_order_count"] = len(mo)

    # Material requisitions
    facts["material_requisition_count"] = len(mreq)

    # Procurement events
    facts["material_procurement_count"] = len(mrp_proc)

    return facts


def main():
    tables = load_all()
    facts = compute_facts(tables)
    print(json.dumps(facts, ensure_ascii=False, indent=2))
    return facts


if __name__ == "__main__":
    main()
