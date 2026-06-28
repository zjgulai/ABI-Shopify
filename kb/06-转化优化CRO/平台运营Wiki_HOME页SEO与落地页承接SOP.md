---
title: 平台运营 Wiki 萃取 · HOME 页 SEO 与落地页承接 SOP
stage: 06-转化优化CRO
layer: 流程阶段
tags: [platform-operations-wiki, HOME页SEO, CRO, 落地页, E-E-A-T, Core Web Vitals]
sources: [platform-operations-wiki, E104, E098, E056, E057]
status: verified
updated: 2026-06-27
summary: 将独立站 HOME 页 SEO、信息层级、E-E-A-T、速度移动端和广告意图承接整合为 CRO 检查表。
verification_status: local_source_only
---

# 平台运营 Wiki 萃取 · HOME 页 SEO 与落地页承接 SOP

## 1. 抽取边界

本篇主源为 E104 `独立站HOME页SEO最强布局（实用干货）.docx`,并融合 DTC 页面承接和 AI 视觉营销资料。Google SEO、Core Web Vitals、E-E-A-T、结构化数据等规则可能变化,当前只标记为本地资料来源,需在执行 SEO 项目前再核对官方文档。

## 2. 独立站 HOME 页 SEO

源资料把 HOME 页 SEO 拆成关键词、页面内容、用户体验、可信度、内链、外链和技术问题七类:

| 模块 | 操作 | ABI 产物 |
|---|---|---|
| 关键词 | 选择一个主要关键词和若干次要关键词,避免过窄或堆词 | `home_keyword_map` |
| 标题/描述 | 标题标签包含主要关键词和品牌名,描述说明价值并提高点击 | `seo_meta_draft` |
| H1/H2/正文 | H1 说明业务和核心关键词,H2/H3 拆分服务/产品/场景 | `home_content_outline` |
| 视觉 | 用图片、视频、截图解释产品价值,减少大段文本压力 | `visual_asset_request` |
| 结构化数据 | Organization 等 schema 帮助搜索引擎理解业务 | `schema_markup_draft` |
| UX | 导航、页脚、页面速度、移动体验和弹窗控制 | `ux_cro_checklist` |
| 监测 | GA/GSC/SEMrush 等跟踪自然流量、CTR、排名、转化 | `seo_monitoring_plan` |

〔来源:platform-operations-wiki · E104〕

## 3. 首页信息层级

首页不应只做品牌展示,也不应堆满产品。更稳妥的信息层级:

1. 首屏:一句话定位、核心人群、主利益点、主 CTA。
2. 问题/场景:用户为什么需要这个产品或方案。
3. 产品/类目入口:用清晰分类连接到高价值集合页或 PDP。
4. 证据:评论、媒体、认证、案例、UGC、前后对比。
5. 教育内容:指南、FAQ、使用教程、博客入口。
6. 信任与政策:物流、退换货、支付安全、联系方式、隐私。
7. 内链:把权重导向核心类目、明星产品、内容专题和联系页。

对 ABI 的要求:
- 建站 Agent 输出首页草案时,必须带 `primary_keyword`、`primary_cta`、`trust_assets`、`internal_links`。
- 素材 Agent 输出图片时,必须说明图像服务哪个页面区块和哪个转化疑虑。
- 数据 Agent 后续用 GSC/GA4 验证曝光、CTR、跳出率、停留时长和转化率。

## 4. 落地页承接

不同渠道流量意图不同,承接页要区分:

| 流量来源 | 用户意图 | 推荐承接 |
|---|---|---|
| Google Search | 明确问题或品类需求 | SEO 文章、集合页、PDP、对比页 |
| Meta/TikTok 冷启动 | 被素材激发兴趣 | 场景落地页、短视频同款页、首购优惠 |
| KOL/UGC | 信任红人或内容 | Creator Store Front、红人推荐集合、UGC PDP 区块 |
| Reddit/社区 | 寻找真实经验和对比 | FAQ、对比页、博客问答、透明披露页 |
| EDM/会员 | 已有关系和促销意图 | 活动页、会员专享、复购推荐 |

同一产品不应所有渠道都落到同一个 PDP。ABI 的 `05 -> 06` 接口应携带 `traffic_intent` 和 `content_asset_id`,让落地页按意图生成。

## 5. 视觉 CRO

AI 视觉营销资料可抽象为“3 秒理解”原则:
- 主图或首屏图必须让用户不用读长文也能理解产品核心价值。
- 附图或页面模块按“场景 -> 功能 -> 证据 -> 对比 -> 使用方式 -> 信任”递进。
- 不只展示参数,要把参数翻译成用户结果。
- 视频、动图和截图应辅助决策,而不是作为装饰。

〔来源:platform-operations-wiki · E056/E057〕

## 6. CRO 验收指标

HOME 页和落地页优化后至少跟踪:
- SEO:主要/次要关键词排名、自然曝光、CTR、自然流量。
- UX:页面加载、移动端可点击性、布局稳定性、跳出率。
- 转化:CTA 点击、集合页点击、PDP 到达、加购、结账、购买。
- 可信度:FAQ 点击、政策页点击、评论/UGC 区块互动。
- 渠道差异:按 UTM 拆分渠道 CVR、AOV、退款和 LTV。

如果某个关键词排名提升但转化不升,优先检查搜索意图与页面承接是否匹配,而不是继续堆关键词。
