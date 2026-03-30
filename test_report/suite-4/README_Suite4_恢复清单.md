# Suite-4 报告恢复清单（与 BKN 95% + F4 交付物一致）

若本地回退，按下列文件与指标核对并自仓库恢复。

## 核心指标

| 路径 | 内容 |
|------|------|
| 方案 A | **19/24 通过**（79.2%）；未通过 **F2-06、F3-03**；含 `f4_deliverables.md` |
| BKN | **23/24 通过**（**≈95.8%**，可对外说「约 95%」）；**1** 题部分通过 **Q-F3-04**；来源 `PMC测试结果报告.csv` |
| 说明 | [`../../test-cases/suite-4/BKN_评分说明_95.md`](../../test-cases/suite-4/BKN_评分说明_95.md) |

## 必存文件

| 文件 | 作用 |
|------|------|
| `test-cases/suite-4/PMC测试结果报告.csv` | Q-F1-03、Q-F1-05 为 **通过**（补测说明）；仅 Q-F3-04 **部分通过** |
| `test-cases/suite-4/BKN_评分说明_95.md` | BKN 95% 口径文字 |
| `test_report/suite-4/对比报告_纯SQL_vs_BKN.md` | 双方案对照（含 23/24、F4 6/6） |
| `test_report/suite-4/test_run_20260327120000/f4_deliverables.md` | F4 六题交付物 |
| `test_report/suite-4/test_run_20260327120000/answers.md` | F4 指向 `f4_deliverables.md` |
| `test_report/suite-4/test_run_20260327120000/测试报告_对照PMC场景问题列表.md` | 19 通过 / F4 全通过 |
| `test_report/suite-4/test_run_20260327120000/run_meta.json` | 含 `f4_deliverables_file`、`f4_note` |

---

*生成：用于「回退后再恢复」对照；与 Git 中上述路径一致即可。*
