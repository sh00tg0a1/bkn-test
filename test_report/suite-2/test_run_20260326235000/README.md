# Suite-2 CLI 拉数结果

- **目录**: `Sx_Qyy.json` — 每题一次 `kweaver dataview query` 的 `--pretty` JSON 输出。
- **元数据**: `run_meta.json`（调用次数、dataview id、token=0）。
- **Catalog**: 与数据源 `supply_chain_data_v1` 一致，表前缀为 `mysql_1j6tsjwo."supply_chain_data"."<表名>"`；勿混用其他环境的 `mysql_*."tem"`。

复现单题示例：

```bash
kweaver dataview query 9d2a06d1-d906-491e-a513-698332ce3751 \
  --sql "SELECT warehouse_id FROM mysql_1j6tsjwo.\"supply_chain_data\".\"warehouse_entity\" LIMIT 1" \
  --pretty
```
