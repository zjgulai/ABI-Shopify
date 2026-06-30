---
title: Listing 关键词资产库 · 全量结构化导出
stage: 03-商品上架与Listing
layer: 流程阶段
tags: [listing, PDP, 关键词, 广告关键词, search, ASIN, agent, 数据资产]
sources: [inbox:S05]
status: verified_local_source
updated: 2026-06-30
verification_status: local_source_only
source_package: kb/_sources/inbox-independent-site/structured/listing-keyword-assets
summary: 将 listing优化模板.xlsx 的 5.关键词库 全量结构化为 801 行关键词资产,服务 Listing/PDP、广告埋词、素材 brief、CRO 和 Agent 工作流。
---

# Listing 关键词资产库 · 全量结构化导出

## 1. 资产定位

本专题把 `listing优化模板.xlsx` 中 `5.关键词库` 从模板样本升级为可查询、可审计、可被 Agent 消费的结构化关键词资产。它不是实时平台数据,而是一个本地来源快照,适合用于 Listing 内容工厂的字段设计、关键词分层、PDP 埋词、广告关键词分组和素材 brief 初稿。

边界:
- 来源文件 sha256 前缀: `6a39b95bb34d`。
- 结构化导出路径: `kb/_sources/inbox-independent-site/structured/listing-keyword-assets/`。
- 未调用 provider,未登录 Shopify,未读取店铺,未写店铺。
- 搜索量、购买量、PPC 竞价、ABA 排名、ASIN、广告词类型均为本地模板快照;生产上线前必须重新拉取最新 Amazon/广告/Shopify 相关数据并复核。

## 2. 导出概览

| 资产 | 数量/状态 |
|---|---:|
| 关键词资产行 | 801 |
| 原始字段 | 42 |
| rich 布局 | 218 |
| compact metric 布局 | 228 |
| compact type 布局 | 355 |
| head 词 | 12 |
| mid 词 | 80 |
| long_tail 词 | 709 |
| 重复关键词 | 155 |

流量词类型聚合:

| 类型 | 关键词数 |
|---|---:|
| 自然搜索词 | 389 |
| SP广告词 | 262 |
| 视频广告词 | 242 |
| 品牌广告词 | 217 |
| HR推荐词 | 89 |

## 3. 文件入口

| 文件 | 用途 |
|---|---|
| `keyword_assets_full.csv` | 人工审查、BI、表格筛选 |
| `keyword_assets_full.jsonl` | RAG/Agent 直接消费;含 `raw_columns` 原始列回溯 |
| `keyword_assets_summary.json` | 概览统计、Top 搜索量/购买量关键词、缺失字段 |
| `keyword_traffic_type_bridge.csv` | 多标签流量词拆分桥表 |
| `keyword_traffic_type_summary.csv` | 流量词类型聚合 |
| `sheet_exports/*.csv` | 竞品库、卖点库、评价分析、QA、作图需求等上下文表 |

## 4. 字段字典

| 字段组 | 代表字段 | 用途 |
|---|---|---|
| 来源追溯 | `keyword_asset_id`,`source_sheet`,`source_row`,`source_sha256_12`,`row_layout` | 可回查 Excel 行与布局 |
| 关键词基础 | `keyword`,`keyword_translation`,`keyword_tier` | 标题、五点、PDP、广告分组 |
| 流量类型 | `traffic_word_type_raw`,`traffic_word_types` | 拆分自然/SP/品牌/视频/HR 推荐词 |
| 需求强度 | `monthly_search_volume`,`monthly_purchase_volume`,`purchase_rate`,`spr` | 需求优先级和词层级判断 |
| 竞价与广告 | `ppc_bid`,`suggested_bid_range` | 广告初始竞价参考,上线前必须刷新 |
| 竞争结构 | `product_count`,`supply_demand_ratio`,`ad_competitor_count`,`click_concentration`,`top3_asin_conversion_share` | 判断市场拥挤度和头部集中度 |
| ASIN 证据 | `top1_asin`,`top2_asin`,`top3_asin`,`top10_asin` | 竞品反查、卖点/素材对比 |
| 原始回溯 | `raw_columns` | 保留 42 列原始值,防止二次解释丢证据 |

## 5. 工作流接入

**Listing/PDP**
- head/mid 词用于标题、首屏卖点、集合页 title 与 H1 候选。
- long_tail 词用于 FAQ、用法场景、ALT、Search/Shopping feed 的补充覆盖。
- `purchase_rate` 高但搜索量中低的词,优先进入转化型 FAQ、对比模块或广告落地页。

**广告与素材**
- `SP广告词` 用于 SP/Shopping 搜索意图分组。
- `品牌广告词` 先做品牌/竞品边界复核,避免误投或侵权。
- `视频广告词` 映射到视频 hook、封面文案和第一屏卖点。
- `HR推荐词` 只能作为本地模板标签参考,需平台口径复核。

**Agent 输入**

```json
{
  "keyword_assets": "keyword_assets_full.jsonl",
  "filters": {
    "keyword_tier": ["head", "mid"],
    "traffic_word_types": ["自然搜索词", "SP广告词"],
    "verification_status": "local_source_only"
  },
  "required_human_checks": [
    "refresh_search_volume",
    "refresh_ppc_bid",
    "asin_current_status",
    "claim_compliance"
  ]
}
```

Agent 输出必须保留 `keyword_asset_id` 与 `source_row`,不能只输出关键词文本。

## 6. 质量与缺口

本轮结构化导出已处理的复杂点:
- `5.关键词库` 不是单一布局:脚本识别 3 种 row_layout,避免把紧凑布局的数值列误判为流量词类型。
- `keyword_traffic_type_summary.csv` 仅保留 5 个已知流量词类型,不接受数值污染。
- JSONL 保留 `raw_columns`,便于后续人工二次校验。

已知缺口:
- 228 行 `compact_metric_col6_top_asin_col25` 没有稳定的流量词类型字段。
- 43 行缺 `ppc_bid`,3 行缺 `monthly_purchase_volume`,1 行缺 `monthly_search_volume`。
- 模板里的 ASIN、ABA、竞价与搜索量存在时效性,不代表当前平台事实。

## 7. 验收口径

本资产被视为 T6 的“结构化关键词资产导出”完成,验收依据:
- `keyword_assets_full.csv`:802 行含表头。
- `keyword_assets_full.jsonl`:801 行。
- `keyword_traffic_type_summary.csv`:只包含自然搜索词、SP广告词、视频广告词、品牌广告词、HR推荐词。
- `workbook_profile.json`:记录 20 个工作表、12 个上下文 CSV 导出、来源 SHA 和本地只读边界。

后续任何真实上架、广告投放或 Shopify 写入,仍需走 T7 授权、人审和现场批准流程。
