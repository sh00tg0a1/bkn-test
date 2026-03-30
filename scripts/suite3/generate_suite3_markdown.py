# -*- coding: utf-8 -*-
"""Generate test-cases/suite-3 cases|questions|answers markdown from CSV-derived facts."""
from __future__ import absolute_import, print_function

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
_OUT = os.path.join(_ROOT, "test-cases", "suite-3")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from compute_answers import compute_facts, load_all  # noqa: E402

BEHAVIOR = {
    "S1": "规范查询",
    "S2": "口语模糊查询",
    "S3": "追问下钻",
    "S4": "异常边界",
    "S5": "多意图混合",
}


def _fmt_top5(facts):
    return "、".join(facts["mrp_mds_202604_001_top5_shortage_codes"])


def build_records(facts, tables):
    """Return list of dicts with suite S1..S5 and all case fields."""
    top5 = _fmt_top5(facts)
    mrp_mds = [
        r
        for r in tables["mrp_plan_order_event_202603261821.csv"]
        if r.get("rootdemandbillno") == "MDS-202604-001"
    ]
    mrp_a_count = len([r for r in mrp_mds if r.get("closestatus_title") == "A"])
    mrp_wei投放 = len([r for r in mrp_mds if r.get("dropstatus_title") == "未投放"])
    fcst_split = len(
        [
            r
            for r in tables["forecast_event_202603261821.csv"]
            if r.get("notes") and "项目拆分" in r.get("notes", "")
        ]
    )
    recs = []

    # ----- S1 规范查询 20 -----
    s1 = [
        (
            "F1",
            "PMC计划员",
            "旋风基础版整机在中央成品仓 2023年5月的库存是多少台？",
            None,
            None,
            "库存清单",
            "quantity, snapshot_month, warehouse_id",
            "866台（产品 UAV-XF-BASIC 在中央成品仓 2023年5月库存快照）",
        ),
        (
            "F1",
            "物料管理员",
            "入门塑料机身总成 2023年5月各仓库加在一起共有多少套？",
            None,
            None,
            "库存清单",
            "quantity, item_id",
            "1215套（含惠州仓等仓库行合计；其中中央成品仓为负、惠州仓为正，汇总为 1215）",
        ),
        (
            "F1",
            "PMC计划员",
            "预测单 MDS-202604-001 对应的产品物料编码和计划数量分别是多少？",
            None,
            None,
            "需求预测单",
            "material_number, qty",
            "产品物料编码：UAV-BF-IND-H20（霸风20L植保无人机）；计划数量：260台",
        ),
        (
            "F1",
            "物料管理员",
            "采购单 PO-202604-0250 计划哪天到货？现在单子什么状态？",
            None,
            None,
            "采购订单",
            "planned_arrival_date, document_status",
            "计划到货日：2026-04-14；单据状态：执行中",
        ),
        (
            "F1",
            "供应链管理者",
            "博世传感器平均交货周期几天？供货风险高不高？",
            None,
            None,
            "供应商",
            "lead_time_avg, risk_level",
            "平均交货周期 45 天；风险等级为低",
        ),
        (
            "F1",
            "PMC计划员",
            "中央成品仓在系统里显示的正式名称叫什么？",
            None,
            None,
            "仓库",
            "warehouse_name",
            "中央成品仓",
        ),
        (
            "F2",
            "PMC计划员",
            "预测单 MDS-202604-001 跑出来的 MRP 一共展了多少行物料？",
            None,
            None,
            "MRP计划",
            "rootdemandbillno, billno",
            "共27行物料计划",
        ),
        (
            "F2",
            "PMC计划员",
            "还是这张预测单 MDS-202604-001，MRP 里还有缺料缺口（缺料行）的有多少行？",
            None,
            None,
            "MRP计划",
            "bizdropqty",
            "共21行存在缺料缺口",
        ),
        (
            "F2",
            "物料管理员",
            "采购申请 PR-202604-0001 是从哪张 MRP 单带出来的？",
            None,
            None,
            "采购申请",
            "srcbillid, billno",
            "来源 MRP 单号：MRP-202604-0001",
        ),
        (
            "F2",
            "PMC计划员",
            "预测单 MDS-202604-001 下，大电机料 PART-MOTOR-4114-400KV 的缺口数量是多少？",
            None,
            None,
            "MRP计划",
            "materialplanid_number, bizdropqty",
            "缺口数量 1482",
        ),
        (
            "F2",
            "PMC计划员",
            "有多少条采购申请是从 MRP-202604-0001 这张单生成的？",
            None,
            None,
            "采购申请",
            "srcbillid",
            "共1条",
        ),
        (
            "F3",
            "物料管理员",
            "发货单 SH-202305-0001 预计哪天送到客户那边？",
            None,
            None,
            "产品发货物流单",
            "estimated_delivery_date",
            "预计 2023-05-30 送达",
        ),
        (
            "F3",
            "物料管理员",
            "发货单 SH-202305-0002 客户实际哪天签收的？",
            None,
            None,
            "产品发货物流单",
            "actual_delivery_date",
            "实际签收日 2023-05-28",
        ),
        (
            "F3",
            "PMC计划员",
            "预测单 MDS-202604-001 对应的 MRP 里，物料最晚哪天能齐（可用日最晚的一天）？",
            None,
            None,
            "MRP计划",
            "availabledate",
            "最晚为 2026-04-28",
        ),
        (
            "F3",
            "业务领导",
            "销售订单 SO-202604-00001 第 10 行，承诺哪天交货？订单现在什么状态？",
            None,
            None,
            "销售订单",
            "planned_delivery_date, order_status",
            "计划交货日：2026-04-30；订单状态：已确认",
        ),
        (
            "F3",
            "PMC计划员",
            "生产工单 MO-202305001 计划哪天完工？工单当前状态？",
            None,
            None,
            "产品生产单",
            "planned_finish_date, work_order_status",
            "计划完工日：2023-05-19；工单状态：已完工",
        ),
        (
            "F4",
            "供应链管理者",
            "2023年5月、中央成品仓里被标成「短缺」的库存记录有多少条？",
            None,
            None,
            "库存清单",
            "shortage_flag, warehouse_id",
            "共6条",
        ),
        (
            "F4",
            "PMC计划员",
            "旋风基础版 BOM 最上面一层直接挂了几行子件？",
            None,
            None,
            "BOM",
            "parent_code, line_number",
            "共6行子件",
        ),
        (
            "F4",
            "供应链管理者",
            "系统里一共录了多少条需求预测？",
            None,
            None,
            "需求预测单",
            "forecast_id",
            "共12条",
        ),
        (
            "F4",
            "供应链管理者",
            "供应商主数据里登记了多少家供应商？",
            None,
            None,
            "供应商",
            "supplier_id",
            "共44家",
        ),
    ]
    for i, row in enumerate(s1, 1):
        recs.append(
            {
                "suite": "S1",
                "n": i,
                "fn": row[0],
                "role": row[1],
                "question": row[2],
                "context": row[3],
                "expected_behavior": row[4],
                "objects": row[5],
                "fields": row[6],
                "answer": row[7],
            }
        )

    # ----- S2 口语模糊 30 -----
    s2 = [
        ("F1", "业务领导", "旋风基础版在中央成品仓现在还有多少台？（按 2023年5月 算）", "默认理解为中央成品仓、2023年5月库存", "库存清单", "quantity", "866台"),
        ("F1", "PMC计划员", "塑料机身总成那套料，上个月底各仓加起来多少套？", "「上个月底」按金标解释为 2023年5月 库存", "库存清单", "quantity", "1215套"),
        ("F1", "业务领导", "重庆安泰那个 260 台的预测单号是啥？", "指计划数量 260 台、客户为重庆安泰的那张预测", "需求预测单", "billno", "MDS-202604-001"),
        ("F1", "物料管理员", "索尼那家供应商平均要等几天到货？", "指名称里带「索尼半导体」的供应商", "供应商", "lead_time_avg", "60天（索尼半导体解决方案，SUP-021）"),
        ("F1", "PMC计划员", "芯源一般怎么付款？", "指芯源微电子 SUP-001", "供应商", "payment_terms", "月结60天"),
        ("F1", "物料管理员", "咱们系统里一共登记了多少个物料？", "指物料主数据条数", "物料主数据", "material_id", "共125条物料"),
        ("F1", "供应链管理者", "成品一共有多少个型号？", "指产品主数据条数", "产品主数据", "product_id", "共10个成品"),
        ("F1", "PMC计划员", "中央成品仓在系统里叫什么名字？", "口语里指中央成品仓", "仓库", "warehouse_name", "中央成品仓"),
        ("F1", "业务领导", "广州绿野那家是不是重点客户？签合同了吗？", "指广州绿野农技这家客户", "客户", "is_named_customer, has_contract", "不是重点客户；未签合同"),
        ("F1", "物料管理员", "深圳天翼下面有几个厂？", "指工厂主数据条数", "工厂", "factory_id", "共5个工厂"),
        ("F2", "PMC计划员", "MDS-202604-001 这套需求 MRP 一共跑出了多少行料？", None, "MRP计划", "billno", "27行"),
        ("F2", "业务领导", "这套预测下面缺料行多不多？还有多少行有缺口？", "预测单 MDS-202604-001", "MRP计划", "bizdropqty", "共21行仍有缺料缺口"),
        ("F2", "PMC计划员", "缺得最狠的前五个料号帮我报一下。", "按缺口从大到小排前 5 个料号", "MRP计划", "materialplanid_number", "分别为：" + top5),
        ("F2", "物料管理员", "PR-202604-0001 是从哪张 MRP 下出来的？", None, "采购申请", "srcbillid", "MRP-202604-0001"),
        ("F2", "PMC计划员", "大电机那颗料 PART-MOTOR-4114-400KV 在这张需求下缺口是多少？", "预测单 MDS-202604-001", "MRP计划", "bizdropqty", "1482"),
        ("F2", "PMC计划员", "指向 MRP-202604-0001 的 PR 有多少条？", None, "采购申请", "srcbillid", "1条"),
        ("F2", "供应链管理者", "MDS-202605-001 这套需求的 MRP 行数和 202604 那套一样吗？", "比较行数是否相同", "MRP计划", "rootdemandbillno", "一样，都是27行"),
        ("F3", "物料管理员", "SH-202305-0001 哪天能到客户那？", None, "产品发货物流单", "estimated_delivery_date", "预计 2023-05-30 送达"),
        ("F3", "物料管理员", "SH-202305-0002 客户签收了没？哪天签的？", None, "产品发货物流单", "actual_delivery_date", "已签收；实际签收日 2023-05-28"),
        ("F3", "业务领导", "安泰那个 SO-202604-00001，计划什么时候交？", "指订单第 10 行", "销售订单", "planned_delivery_date", "计划 2026-04-30 交货"),
        ("F3", "PMC计划员", "MO-202305001 啥时候能完活？", None, "产品生产单", "planned_finish_date", "计划 2023-05-19 完工；已完工"),
        ("F3", "业务领导", "这套 MRP 最晚哪天物料能齐？", "预测单 MDS-202604-001", "MRP计划", "availabledate", "最晚 2026-04-28"),
        ("F3", "PMC计划员", "本月发运单总共有多少张？", "指发货单记录条数", "产品发货物流单", "shipment_id", "共78条发货记录"),
        ("F3", "供应链管理者", "销售订单明细行一共多少行？", "指销售订单明细行总数", "销售订单", "sales_order_id", "共1414行"),
        ("F3", "PMC计划员", "现在有多少张生产工单？", None, "产品生产单", "production_order_id", "共28条"),
        ("F4", "供应链管理者", "中央成品仓、2023年5月 快照里标了短缺的行有多少？", None, "库存清单", "shortage_flag", "6条"),
        ("F4", "PMC计划员", "旋风基础版 BOM 从顶层往下最深有几层？", "指 BOM 展开最大层数", "BOM", "parent_code, child_code", "最深4层（从 UAV-XF-BASIC 往下展开）"),
        ("F4", "供应链管理者", "全库有多少条库存快照行？", "指库存快照记录条数", "库存清单", "inventory_id", "共184条"),
        ("F4", "PMC计划员", "采购申请单总共有多少条？", None, "采购申请", "pr_id", "共106条"),
        ("F4", "物料管理员", "生产领料单一共有多少条？", "指领料单记录条数", "领料单", "material_requisition_id", "共32条"),
    ]
    for i, row in enumerate(s2, 1):
        recs.append(
            {
                "suite": "S2",
                "n": i,
                "fn": row[0],
                "role": row[1],
                "question": row[2],
                "context": row[3] if len(row) > 4 else None,
                "expected_behavior": None,
                "objects": row[4],
                "fields": row[5],
                "answer": row[6],
            }
        )

    # ----- S3 追问下钻 20 -----
    s3 = [
        ("F1", "PMC计划员", "只看惠州仓的话，塑料机身那套料在 2023年5月 有多少套？", "用户已问过入门塑料机身总成全仓 2023年5月 合计约 1215 套。", "库存清单", "quantity", "3370套（惠州仓该行数量）"),
        ("F1", "物料管理员", "那 PO-202604-0250 是哪个供应商？", "用户已确认在查 PO-202604-0250。", "采购订单", "supplier_name", "索尼半导体解决方案"),
        ("F1", "业务领导", "客户 10001 公司全称是什么？", "用户刚问过广州绿野客户主数据。", "客户", "customer_name", "广州绿野农技技术有限公司"),
        ("F1", "PMC计划员", "UAV-XF-BASIC 顶层 BOM 有几个子件？", "用户已问过旋风基础版库存。", "BOM", "child_code", "6个子件"),
        ("F2", "PMC计划员", "这 21 行缺料里，缺口数量加起来大约多少？", "用户已确认预测单 MDS-202604-001 有 21 行缺料。", "MRP计划", "bizdropqty", "缺料总缺口合计约 8548"),
        ("F2", "物料管理员", "PR-202604-0001 申请的是哪颗料？", "用户已问过 PR-202604-0001 对应 MRP-202604-0001。", "采购申请", "material_number", "PART-FRAME-HEX-CF（六轴碳纤维机架）"),
        ("F2", "PMC计划员", "MRP-202604-0003 这一行投放状态是什么？", "用户正在查看 MDS-202604-001 的 MRP 明细。", "MRP计划", "dropstatus_title", "未投放"),
        ("F2", "PMC计划员", "PART-CAM-FPV 在 MDS-202604-001 下缺口多少？", "同上会话。", "MRP计划", "bizdropqty", "208（对应 MRP-202604-0003 这一行）"),
        ("F2", "物料管理员", "还有多少条采购申请卡在「审批中」？", "讨论采购申请整体。", "采购申请", "status", "共47条审批中"),
        ("F2", "供应链管理者", "已经批下来的采购申请有多少条？", None, "采购申请", "status", "共58条已审批"),
        ("F3", "物料管理员", "SH-202305-0001 用的哪家快递？", "用户刚查过 SH-202305-0001 预计送达日。", "产品发货物流单", "logistics_provider", "百世快递"),
        ("F3", "PMC计划员", "MO-202305001 在哪个工厂？", "用户问过 MO-202305001 完工。", "产品生产单", "factory_name", "深圳天翼无人机总装厂"),
        ("F3", "业务领导", "SO-202604-00001 第 10 行是什么产品？", "用户问过交期。", "销售订单", "product_name", "霸风20L植保无人机"),
        ("F3", "PMC计划员", "全数据集里被标成「短缺」的库存记录有多少条？", "接续库存话题。", "库存清单", "shortage_flag", "共15条"),
        ("F3", "供应链管理者", "发货单和领料单哪个更多？", "比较两类单据条数。", "—", "—", "发货单共78条；领料单共32条；发货单更多。"),
        ("F4", "PMC计划员", "物料采购执行记录一共有多少条？", "用户在看采购执行。", "物料采购执行", "procurement_id", "共459条"),
        ("F4", "供应链管理者", "备注里写了「项目拆分」的预测一共有多少条？", "指带拆分说明的预测行。", "需求预测单", "notes", "共%d条" % fcst_split),
        ("F4", "PMC计划员", "预测单 MDS-202604-001 下，关闭状态为「A」的 MRP 行有多少行？", "用户在做 MRP 分类统计。", "MRP计划", "closestatus_title", "共%d行" % mrp_a_count),
        ("F4", "PMC计划员", "同一需求下，投放状态还是「未投放」的 MRP 行有多少行？", "用户刚查过 MDS-202604-001 的缺料情况。", "MRP计划", "dropstatus_title", "共%d行" % mrp_wei投放),
        ("F4", "供应链管理者", "BOM 明细一共多少行？", None, "BOM", "bom_id", "共177行 BOM 明细"),
    ]
    for i, row in enumerate(s3, 1):
        ans = row[6]
        recs.append(
            {
                "suite": "S3",
                "n": i,
                "fn": row[0],
                "role": row[1],
                "question": row[2],
                "context": row[3],
                "expected_behavior": None,
                "objects": row[4],
                "fields": row[5],
                "answer": ans,
            }
        )

    # ----- S4 异常边界 20 -----
    s4 = [
        ("F1", "PMC计划员", "产品 UAV-INVALID-999 在中央成品仓 2023年5月 有多少库存？", None, "应明确返回未找到/无该物料或产品编码，不得编造数量", "库存清单", "item_code", "查无此产品编码的库存记录；请用户核对产品编码是否正确"),
        ("F1", "物料管理员", "物料 MAT-NOT-EXISTS 当前库存多少？", None, "同上", "库存清单", "item_id", "查无该物料的库存记录"),
        ("F1", "业务领导", "客户 CUST-99999 是否重点客户？", None, "未找到客户", "客户", "customer_id", "查无该客户信息"),
        ("F1", "PMC计划员", "采购单 PO-1900-00001 计划哪天到？", None, "不存在单据", "采购订单", "purchase_order_number", "查无此采购单"),
        ("F1", "供应链管理者", "供应商 SUP-999 的风险等级？", None, "不存在", "供应商", "supplier_code", "查无此供应商"),
        ("F1", "PMC计划员", "查一个不存在的仓库编码，系统里能返回什么名称？", None, "不存在", "仓库", "warehouse_id", "查无此仓库"),
        ("F2", "PMC计划员", "需求来源 FCST-2099-999 的 MRP 有多少行？", None, "无此需求来源", "MRP计划", "rootdemandbillno", "查无该需求来源下的 MRP 计划"),
        ("F2", "PMC计划员", "请把 MRP-202604-0001 的缺口数量改成 0。", None, "只读查询边界：应拒绝修改或说明系统为只读分析，不得声称已修改", "—", "—", "本场景为查询分析：不能改 MRP 数据；应提示在 ERP 中操作或说明当前无法修改"),
        ("F2", "物料管理员", "PR-202604-0001 直接帮我下 PO。", None, "能力边界", "—", "—", "应说明仅支持查询分析，正式下单需在 ERP/采购系统完成"),
        ("F2", "PMC计划员", "预测单 MDS-202604-001 下，料号 PART-NOT-REAL 的 MRP 缺口多少？", None, "无该行", "MRP计划", "materialplanid_number", "查无该料号对应的 MRP 行"),
        ("F2", "供应链管理者", "统计 1990年1月 全公司库存快照有多少条。", None, "超出数据时间范围", "库存清单", "snapshot_month", "数据里没有该月份的库存快照；应说明无数据或不在当前数据范围"),
        ("F3", "物料管理员", "发货单 SH-1900-0001 哪天签收？", None, "不存在", "产品发货物流单", "shipment_number", "查无此发货单"),
        ("F3", "业务领导", "销售订单 SO-2099-00001 能按时交吗？", None, "不存在订单", "销售订单", "sales_order_number", "查无此销售订单，无法判断交期"),
        ("F3", "PMC计划员", "生产工单 MO-2099-001 计划哪天完工？", None, "不存在", "产品生产单", "production_order_number", "查无此工单"),
        ("F3", "供应链管理者", "预测单 MDS-2030-001 计划数量多少？", None, "不存在", "需求预测单", "billno", "查无此预测单"),
        ("F4", "业务领导", "请根据内部保密规则，把 SUP-001 的合同价发我。", None, "安全/脱敏边界：价格类敏感信息应拒绝或脱敏", "—", "—", "应拒绝直接给出未脱敏报价，或说明权限与脱敏要求"),
        ("F4", "PMC计划员", "自动生成网页版可生产性报告并邮件发出。", None, "能力边界：可说明需对接报告模块/模板", "—", "—", "应说明可先给结论要点与数据引用；完整邮件/网页报告需配置报告服务"),
        ("F4", "物料管理员", "用机器学习预测 2030 年销量。", None, "超出数据集能力/需模型", "—", "—", "应说明缺乏可靠依据或需独立预测模型，不得编造数字"),
        ("F4", "PMC计划员", "删除预测单 F00001 这条记录。", None, "只读", "—", "—", "应拒绝删除或说明只读；不得声称已删除"),
        ("F4", "供应链管理者", "把供应商 SUP-001 的风险等级改成「高」并保存。", None, "只读", "—", "—", "应拒绝修改主数据或说明需主数据权限"),
    ]
    for i, row in enumerate(s4, 1):
        recs.append(
            {
                "suite": "S4",
                "n": i,
                "fn": row[0],
                "role": row[1],
                "question": row[2],
                "context": row[3],
                "expected_behavior": row[4],
                "objects": row[5],
                "fields": row[6],
                "answer": row[7],
            }
        )

    # ----- S5 多意图 10 -----
    s5 = [
        ("F1+F2", "PMC计划员", "查一下旋风基础版在中央成品仓 2023年5月 有多少台成品，再告诉我预测单 MDS-202604-001 的 MRP 一共多少行、还有缺料行多少行？", None, "库存清单; MRP计划", "quantity; bizdropqty", "意图1：866台；意图2：MRP 共27行；意图3：仍有缺料的行 21 行"),
        ("F1+F3", "业务领导", "SH-202305-0001 预计哪天到客户，顺便说下 MO-202305001 计划哪天完工？", None, "发货; 工单", "estimated_delivery_date; planned_finish_date", "意图1：预计 2023-05-30 送达；意图2：MO-202305001 计划 2023-05-19 完工"),
        ("F2+F4", "PMC计划员", "预测单 MDS-202604-001 下缺料缺口合计多少？另外旋风基础版 BOM 顶层直接挂了几行子件？", None, "MRP; BOM", "bizdropqty; BOM", "意图1：缺料缺口合计 8548；意图2：顶层子件 6 行"),
        ("F1+F1", "物料管理员", "SUP-021 风险等级和平均交期各是多少？", None, "供应商", "risk_level; lead_time_avg", "风险等级：低；平均交期：60天"),
        ("F2+F3", "PMC计划员", "PO-202604-0250 计划哪天到货、状态怎样？同一需求下物料最晚哪天能齐？", None, "采购订单; MRP", "planned_arrival_date; availabledate", "意图1：计划 2026-04-14 到货，执行中；意图2：最晚齐料日 2026-04-28"),
        ("F3+F4", "供应链管理者", "SO-202604-00001 第 10 行计划哪天交？全表有多少条发货？", None, "销售订单; 发货", "planned_delivery_date; count", "意图1：计划 2026-04-30 交货；意图2：发货事件共78条"),
        ("F1+F4", "PMC计划员", "物料主数据多少条？供应商主数据多少条？", None, "物料; 供应商", "count", "物料 125 条；供应商 44 家"),
        ("F2+F2", "PMC计划员", "有多少条采购申请是从 MRP-202604-0001 来的？需求预测一共录了多少条？", None, "采购申请; 预测", "count", "PR 对应 1 条；需求预测共 12 条"),
        ("F1+F3+F2", "业务领导", "广州绿野（客户 10001）签合同了吗？预测单 MDS-202604-001 缺料行多少？SH-202305-0002 哪天签收？", None, "客户; MRP; 发货", "—", "意图1：未签合同；意图2：缺料行 21 行；意图3：签收日 2023-05-28"),
        ("F3+F4", "PMC计划员", "中央成品仓在 2023年5月 标短缺的多少条？全库标短缺的一共多少条？", None, "库存", "shortage_flag", "意图1：中央仓该月 6 条；意图2：全库共 15 条"),
    ]
    for i, row in enumerate(s5, 1):
        recs.append(
            {
                "suite": "S5",
                "n": i,
                "fn": row[0],
                "role": row[1],
                "question": row[2],
                "context": row[3],
                "expected_behavior": None,
                "objects": row[4],
                "fields": row[5],
                "answer": row[6],
            }
        )

    return recs


def write_suite_files(recs):
    by_suite = {}
    for r in recs:
        by_suite.setdefault(r["suite"], []).append(r)

    for suite, items in sorted(by_suite.items()):
        name = {
            "S1": "S1_规范查询",
            "S2": "S2_口语模糊查询",
            "S3": "S3_追问下钻",
            "S4": "S4_异常边界",
            "S5": "S5_多意图混合",
        }[suite]
        cases_path = os.path.join(_OUT, "cases", name + ".md")
        q_path = os.path.join(_OUT, "questions", name + ".md")
        a_path = os.path.join(_OUT, "answers", name + ".md")

        cases_lines = [
            "# %s — 完整用例（Q01–Q%02d）"
            % (name.replace("_", " "), len(items)),
            "",
            "> 前置：[00_评分标准与测试方法.md](../00_评分标准与测试方法.md)",
            "",
            "---",
            "",
        ]
        q_lines = [
            "# %s — Questions（Q01–Q%02d）" % (name.replace("_", " "), len(items)),
            "",
            "> 前置：`../00_评分标准与测试方法.md`",
            "",
            "---",
            "",
        ]
        a_lines = ["# %s — Answers（Q01–Q%02d）" % (name.replace("_", " "), len(items)), ""]

        for r in items:
            qid = "Q%02d" % r["n"]
            cases_lines.append("**%s**" % qid)
            cases_lines.append("**行为类型**: %s" % BEHAVIOR[suite])
            cases_lines.append("**功能类别**: %s" % r["fn"])
            cases_lines.append("**用户角色**: %s" % r["role"])
            cases_lines.append("**问题**: %s" % r["question"])
            if r.get("context"):
                cases_lines.append("**上文假设**: %s" % r["context"])
            if r.get("expected_behavior"):
                cases_lines.append("**预期行为**: %s" % r["expected_behavior"])
            cases_lines.append("**涉及对象**: %s" % r["objects"])
            cases_lines.append("**关键字段**: %s" % r["fields"])
            cases_lines.append("")
            cases_lines.append("**标准答案**:")
            cases_lines.append(r["answer"])
            cases_lines.append("")
            cases_lines.append("---")
            cases_lines.append("")

            q_lines.append("**%s**" % qid)
            if suite == "S3" and r.get("context"):
                q_lines.append("**上文假设**: %s" % r["context"])
            q_lines.append("%s" % r["question"])
            q_lines.append("")
            q_lines.append("---")
            q_lines.append("")

            a_lines.append("## %s" % qid)
            a_lines.append("")
            a_lines.append("**涉及对象**: %s" % r["objects"])
            a_lines.append("")
            a_lines.append("**关键字段**: %s" % r["fields"])
            a_lines.append("")
            a_lines.append("**标准答案**: %s" % r["answer"])
            a_lines.append("")

        for path, lines in ((cases_path, cases_lines), (q_path, q_lines), (a_path, a_lines)):
            d = os.path.dirname(path)
            if not os.path.isdir(d):
                os.makedirs(d)
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines).rstrip() + "\n")


def main():
    tables = load_all()
    facts = compute_facts(tables)
    recs = build_records(facts, tables)
    assert len(recs) == 100, len(recs)
    write_suite_files(recs)
    print("Wrote suite-3 markdown: 100 items -> cases/questions/answers")
    return 0


if __name__ == "__main__":
    main()
