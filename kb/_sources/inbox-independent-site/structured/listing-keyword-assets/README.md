---
title: listing优化模板关键词资产结构化导出
type: source_asset
source_id: inbox:S05
updated: 2026-06-30
verification_status: local_source_only
summary: 从 listing优化模板.xlsx 的 5.关键词库 工作表导出 801 行全量关键词资产,并保留上下文工作表 CSV 与原始列回溯字段。
---

# listing优化模板关键词资产结构化导出

## 1. 来源与边界

- 来源文件: `kb/_sources/inbox-independent-site/originals/listing优化模板.xlsx`
- 来源 ID: `inbox:S05`
- sha256 前缀: `6a39b95bb34d`
- 导出脚本: `kb/tools/export_listing_keyword_assets.py`
- 读取方式: 本地只读解析 workbook cached values;Excel UI 扩展与条件格式不参与结构化导出。

边界:
- 未调用外部 provider,未登录 Shopify,未读取/写入任何店铺。
- 搜索量、购买量、PPC 竞价、ABA 排名、ASIN 和广告字段均来自本地模板快照,生产使用前必须重新拉取最新平台数据。
- 本目录是结构化资产导出区,不是实时广告或平台报表。

## 2. 导出规模

| 指标 | 数量 |
|---|---:|
| workbook 工作表 | 20 |
| 上下文 CSV 导出 | 12 |
| `5.关键词库` 原始字段 | 42 |
| 关键词资产行 | 801 |
| JSONL 资产行 | 801 |
| CSV 行数 | 802(含表头) |
| bridge 行数 | 1199 |

## 3. 行布局识别

`5.关键词库` 后半段存在紧凑布局,不能按单一表头盲映射。导出脚本按逐行证据识别布局:

| row_layout | 行数 | 识别依据 |
|---|---:|---|
| `rich_top_asin_col33` | 218 | `#1 ASIN` 从第 33 列开始,流量词类型在第 14 列 |
| `compact_metric_col6_top_asin_col25` | 228 | `#1 ASIN` 从第 25 列开始,第 6 列是综合分公式/数值 |
| `compact_type_col6_top_asin_col25` | 355 | `#1 ASIN` 从第 25 列开始,第 6 列是流量词类型 |

## 4. 资产文件

| 文件 | 用途 |
|---|---|
| `keyword_assets_full.csv` | BI/人工审查用宽表;含标准化关键词字段、布局、来源与风险边界 |
| `keyword_assets_full.jsonl` | RAG/Agent 用全量记录;额外保留 `raw_columns` 原始列回溯 |
| `keyword_assets_summary.json` | 行数、布局、词层级、缺失字段、Top 搜索/购买词摘要 |
| `keyword_traffic_type_bridge.csv` | 一个关键词到多个流量词类型的桥表 |
| `keyword_traffic_type_summary.csv` | 流量词类型聚合,仅保留已知类型 |
| `sheet_inventory.csv` | workbook 20 个工作表的 used row/column 清单 |
| `workbook_profile.json` | 来源 SHA、大小、导出清单、边界与 keyword summary |
| `sheet_exports/*.csv` | 关键词库与 11 个上下文工作表的表格化导出 |

## 5. 标准化字段

核心字段包括:
- 来源: `keyword_asset_id`,`source_id`,`source_sha256_12`,`source_sheet`,`source_row`,`row_layout`
- 关键词: `keyword`,`keyword_translation`,`keyword_tier`,`traffic_word_type_raw`,`traffic_word_types`
- 需求与竞价: `monthly_search_volume`,`monthly_purchase_volume`,`purchase_rate`,`spr`,`ppc_bid`,`suggested_bid_range`
- 竞争结构: `product_count`,`supply_demand_ratio`,`ad_competitor_count`,`click_concentration`,`top3_asin_conversion_share`
- ASIN 证据: `top1_asin` 至 `top3_asin`,`top10_asin`
- 回溯: JSONL 的 `raw_columns` 保留 42 个原始列值。

## 6. Agent 使用建议

1. 先用 `keyword_tier` 粗分 head/mid/long_tail,不要只按搜索量选词。
2. 对 `traffic_word_types` 拆分后的多标签词,分别映射 SEO、SP、品牌、视频和 HR 推荐词用途。
3. 对 `row_layout=compact_metric_col6_top_asin_col25` 的 228 行,流量词类型原始为空,不要臆造渠道类型。
4. 使用 `top*_asin` 做竞品反查时,必须重新复核 ASIN 当前状态、类目和可售性。
5. 上线 PDP、广告或 Search/Shopping 埋词前,必须用最新平台数据刷新搜索量、竞价和排名。
