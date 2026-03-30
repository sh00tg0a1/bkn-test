# Suite-3 脚本说明

| 脚本 | 说明 |
|------|------|
| `data_loader.py` | 无第三方依赖，加载 `ref/suite-3/supplychaindata_1/*.csv` |
| `compute_answers.py` | 汇总关键指标 JSON（用于金标验算） |
| `verify_suite3.py` | 回归校验关键指标与基线一致 |
| `generate_suite3_markdown.py` | 生成 `test-cases/suite-3/` 下 cases、questions、answers 共 15 个 md 文件 |

```bash
python3 scripts/suite3/compute_answers.py
python3 scripts/suite3/verify_suite3.py
python3 scripts/suite3/generate_suite3_markdown.py
```
