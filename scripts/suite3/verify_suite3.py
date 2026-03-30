# -*- coding: utf-8 -*-
"""Regression checks for suite-3 gold metrics (stdlib + compute_answers)."""
from __future__ import absolute_import, print_function

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from compute_answers import compute_facts, load_all  # noqa: E402


# Expected values from compute_answers.py run on ref/suite-3/supplychaindata_1 (2026-03-26 baseline)
EXPECTED = {
    "inv_p0001_wh001_202305_qty": 866.0,
    "mrp_mds_202604_001_line_count": 27,
    "mrp_mds_202604_001_shortage_material_count": 21,
    "inv_m0001_all_wh_202305_qty_sum": 1215.0,
    "bom_uav_xf_basic_direct_line_count": 6,
    "bom_uav_xf_basic_max_depth_levels": 4,
    "forecast_row_count": 12,
    "supplier_entity_count": 44,
    "material_entity_count": 125,
    "product_entity_count": 10,
    "warehouse_count": 5,
    "inv_wh001_202305_shortage_flag_rows": 6,
    "mrp_mds_202604_001_max_availabledate": "2026-04-28",
}


def main():
    tables = load_all()
    facts = compute_facts(tables)
    errors = []
    for k, exp in EXPECTED.items():
        got = facts.get(k)
        if got != exp:
            errors.append("%s: expected %r got %r" % (k, exp, got))
    if errors:
        print("VERIFY FAILED:")
        for e in errors:
            print(" ", e)
        sys.exit(1)
    print("verify_suite3: OK (%d keys)" % len(EXPECTED))
    return 0


if __name__ == "__main__":
    main()
