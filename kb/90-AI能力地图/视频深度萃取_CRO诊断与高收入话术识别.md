---
title: 视频深度萃取 · CRO诊断与高收入话术识别
stage: 90-AI能力地图
layer: 横切层
tags: [youtube, 深度萃取, cro, no-sales, 高收入话术, 风控, t6]
sources: [youtube, browser-harness, 用户提供]
status: verified
updated: 2026-06-29
verification_status: mixed_ui_transcript_and_page_metadata
summary: 基于 browser-harness 对 Ac Hampton e7oiWBn7KwU 与 Austin Rabin uRHm5WpPJyU 做只读复核,沉淀 Shopify 未出单诊断树、CRO实验顺序、流量质量判断和高收入标题的证据分层/夸大识别框架。
---

# 视频深度萃取 · CRO诊断与高收入话术识别

> 证据边界:本批使用用户授权的真实 Chrome + browser-harness 只读访问 YouTube 播放页。没有下载视频、没有调用 provider、没有写外部平台。`e7oiWBn7KwU` 读到 UI 转写段落;`uRHm5WpPJyU` 只读到播放页元数据、页面说明和章节,因此后者按内容级 v0.1 处理。

## 0. 证据表

| 清单序号 | video_id | 页面标题 | browser-harness 页面作者 | 时长 | 证据等级 | 入库状态 |
|---:|---|---|---|---:|---|---|
| 11 | `e7oiWBn7KwU` | The TRUTH To Why You Aren't Making Sales With Your Shopify Store | Ac Hampton | 891 秒 | UI 转写 111 段 + 页面说明/章节 | imported |
| 44 | `uRHm5WpPJyU` | $278K in 30 days on shopify (with proof) just copy my exact store. | Austin Rabin | 1,321 秒 | 页面说明 + 2 段章节;转写段落未读出 | imported_cross_channel_v0.1 |

**归因修正**:`uRHm5WpPJyU` 出现在 Ac Hampton Shopify 搜索清单中,但播放页作者字段为 `Austin Rabin`。本库保留它作为“高收入标题/案例拆解”的风控样例,不计入 Ac Hampton 频道深度覆盖。

## 1. Ac Hampton · 未出单 CRO 诊断树

**章节结构**
- `0:00` Intro
- `1:45` Social Proof Of Your Dropshipping Product
- `3:00` Competitor Traffic
- `6:18` Amount Of Traffic
- `9:13` A/B Testing For Your Shopify Store
- `10:37` Customer Experience
- `12:13` Quality Of Information
- `14:16` Outro

**核心判断**

Ac Hampton 的诊断顺序不是直接改页面,而是先排除“产品需求、流量质量、流量数量”三个前置变量,再进入页面和 offer 实验。这对 ABI 的价值很直接:未出单诊断必须先分层,否则容易把产品/流量问题误判成页面问题。

| 诊断层 | 视频中做法 | ABI 可落地字段 |
|---|---|---|
| 产品与需求 | 用 Google Trends、竞品评论、竞品广告评论判断消费者是否真的在找这个产品 | `demand_signal`、`seasonality`、`competitor_social_proof` |
| 竞品流量 | 用 Similarweb 类工具看竞品访问量和广告活跃度,只作方向性估计 | `competitor_traffic_estimate`、`competitor_ads_active` |
| 流量质量 | 区分便宜点击和有购买意图的流量;广告目标会影响访客质量 | `campaign_objective`、`qualified_session_ratio` |
| 流量数量 | 在样本量不足时不要过早判定 CRO;视频以约 500 sessions 作为进入 CVR 观察的经验线 | `sessions_threshold`、`sample_size_status` |
| 广告疲劳 | 同质化广告会导致点击下降;应从 Amazon/竞品评论里提炼新使用场景 | `creative_angle_source`、`ad_fatigue_flag` |
| A/B 实验 | 单次只改一个变量,观察数天后与原版本对比 | `experiment_variable`、`baseline`、`variant`、`observation_window` |
| 客户体验 | 货币、sticky add-to-cart、reviews、upsell、图片质量、颜色一致性影响信任 | `trust_widgets`、`visual_consistency`、`purchase_friction` |
| 信息质量 | 首屏 3 秒内说明价值;内容要按消费者最关心的 feature/benefit 组织 | `above_fold_message`、`benefit_order`、`skim_readability` |

## 2. 未出单诊断 SOP

ABI 可把这条视频沉淀为 `06-CRO` 的“未出单诊断树”:

1. **先查产品需求**:Google Trends、搜索词、竞品评论、广告评论、Amazon/同类 marketplace reviews。若需求信号弱,先回 `01-选品与市场调研`。
2. **再查流量质量**:广告目标、来源渠道、UTM、点击意图、落地页匹配度。若流量是低意图点击,先回 `05-营销与引流`。
3. **再查样本量**:sessions、加购、checkout、purchase 是否足够判断。样本不足时先补流量或延长观察。
4. **再查 offer 和价格**:包邮门槛、折扣、定价、COGS、广告成本和利润空间。视频中的 `2.5x COGS` 只能作经验线,不能替代真实毛利模型。
5. **再做页面实验**:一次只改一个变量,例如首屏承诺、价格、shipping offer、CTA、reviews、sticky cart、图片质量。
6. **最后固化证据**:每次实验保留 `hypothesis / variant / metric / result / next_action`,进入 `07-数据与归因`。

**最低埋点要求**
- `sessions`
- `qualified_sessions`
- `add_to_cart`
- `checkout_started`
- `purchase`
- `conversion_rate`
- `source_medium / campaign / creative_id`
- `landing_page`
- `AOV / COGS / ad_spend / gross_margin`

## 3. Austin Rabin · 高收入标题样例 v0.1

**播放页事实**
- 页面作者:`Austin Rabin`
- 标题主张:30 天 Shopify 销售额 `278K`
- 案例对象:Haven Golf Company
- 页面说明提到:winning products、Shopify website、Facebook & Instagram ads、product pages、ad creatives、conversion optimization、sales breakdowns。
- 章节只有两段:`0:00 Monthly Case Study` 与 `11:15 Step by step copy the build`。
- 页面说明还引导复制 Shopify store theme,包括导入 products、images、descriptions、collections、apps。

**可沉淀价值**

这条不适合写成“复制即可增长”的 SOP,更适合作为 `91-合规与风控` 的高收入标题识别样例。它能帮助 ABI 在看类似案例时强制拆出事实层、缺失层和不可复制层。

| 层级 | 应抽取 | 必须追问 |
|---|---|---|
| Revenue claim | 销售额、时间窗口、截图/后台来源 | 是否含税/退款/取消单/未履约订单 |
| Profit reality | 毛利、COGS、运费、支付费、退货、客服、广告费 | 是否有净利、现金流和库存压力 |
| Traffic engine | Meta ads、creative、受众、预算、学习期 | 是否依赖短期素材/预算堆量 |
| Store clone | theme、products、images、descriptions、apps | 素材授权、品牌差异、产品同质化风险 |
| Case transferability | 品类、市场、季节、供应链、客单价 | 是否适合当前 ABI 品类和预算 |
| Compliance | 标题中的“proof”“copy my exact store” | 是否诱导收益承诺或侵权复制 |

## 4. 高收入话术识别 SOP

遇到 `$X in Y days/months`、`copy exact store`、`with proof` 类标题,ABI 应进入以下人审卡:

1. **先归因**:打开播放页确认真实作者和频道,不要只按搜索清单归属。
2. **拆 revenue**:只记录“页面主张”,不得写入财务预测。
3. **补利润口径**:没有 COGS、ad spend、refund、shipping、payment fee、inventory cashflow 时,不得称为可复制经营模型。
4. **查授权边界**:theme、product image、ad creative、description、brand copy 是否允许复制。
5. **拆渠道依赖**:Meta/Facebook/Instagram ads 案例需要 budget、creative fatigue、audience、landing page 和 attribution 才能复盘。
6. **只沉淀方法**:把案例拆成“产品页结构、素材角度、渠道承接、CRO checklist”,不要沉淀收益承诺。

## 5. 对 ABI 经营作战台的增量建议

| 增量模块 | 内容 | 目标落点 |
|---|---|---|
| 未出单诊断树 | 产品需求 → 流量质量 → 流量数量 → offer/价格 → 页面体验 → 信息质量 | `06-CRO` / `05-营销` / `07-数据` |
| CRO 实验卡 | hypothesis、single_variable、baseline、variant、observation_window、result | SOP 库 / Agent 工作流 |
| 高收入标题审查卡 | revenue claim、profit gap、traffic engine、authorization、transferability | `91-合规与风控` |
| 跨频道归因提醒 | 搜索清单命中不等于频道归属,必须以播放页作者字段为准 | T6 入库流程 |

## 6. 原始证据路径

- #11 页面元数据:`tmp/t6_cro_claims_batch_20260629/raw/11_metadata.json`
- #11 UI 转写:`tmp/t6_cro_claims_batch_20260629/raw/11_transcript.txt`
- #44 页面元数据:`tmp/t6_cro_claims_batch_20260629/raw/44_metadata.json`
- #44 页面章节/说明快照:`tmp/t6_cro_claims_batch_20260629/raw/44_transcript.txt`
