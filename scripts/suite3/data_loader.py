# -*- coding: utf-8 -*-
"""Load suite-3 supply chain CSVs (stdlib only, Python 3.7+)."""
from __future__ import absolute_import, print_function

import csv
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT, "ref", "suite-3", "supplychaindata_1")


def _read_csv(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        r = csv.DictReader(f)
        return list(r)


def load_all():
    files = [
        "bom_event_202603261810.csv",
        "customer_entity_202603261810.csv",
        "factory_entity_202603261811.csv",
        "forecast_event_202603261821.csv",
        "inventory_event_202603261811.csv",
        "material_entity_202603261811.csv",
        "material_procurement_event_202603261812.csv",
        "material_requisition_event_202603261812.csv",
        "mrp_plan_order_event_202603261821.csv",
        "product_entity_202603261815.csv",
        "production_order_event_202603261815.csv",
        "purchase_order_event_202603261815.csv",
        "purchase_requisition_event_202603261821.csv",
        "sales_order_event_202603261816.csv",
        "shipment_event_202603261816.csv",
        "supplier_entity_202603261819.csv",
        "warehouse_entity_202603261820.csv",
    ]
    out = {}
    for fn in files:
        out[fn] = _read_csv(fn)
    return out


def to_float(x, default=0.0):
    if x is None or x == "":
        return default
    try:
        return float(x)
    except ValueError:
        return default


def to_int(x, default=0):
    if x is None or x == "":
        return default
    try:
        return int(float(x))
    except ValueError:
        return default
