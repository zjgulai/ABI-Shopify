---
title: 广告诊断 SOP
stage: 07-数据与归因
layer: 流程阶段
tags: [inbox, 广告诊断, Placement, Search Term, Search Impression Share, SA, DSP, UTM, Attribution, Agent]
sources: [inbox:S05, inbox:S10, inbox:S11, inbox:S12, inbox:S13]
status: verified
updated: 2026-06-30
summary: 将 inbox 广告报告、广告结构推断和 SA/DSP 作战资料整理为可执行的广告诊断 Agent 规则库。
verification_status: local_source_only
source_package: kb/_sources/inbox-independent-site
---

# 广告诊断 SOP

## 1. 抽取边界

本 SOP 来自 `/Users/pray/project/shopify/inbox/` 的广告与 Listing 资料包:

| extract_id | 来源 | 本文采用内容 | 验证状态 |
|---|---|---|---|
| inbox:S05 | `listing优化模板.xlsx` | 关键词库、竞品库、评价/QA 与广告关键词字段 | `local_source_only` |
| inbox:S10 | `GMV千万美金广告作战方案(1).xmind` | SA/DSP 指标、搜索/详情页/站外流量拆解 | `local_source_only` |
| inbox:S11 | `广告高阶打法&数据分析.docx` | 年度复盘、广告×Deal、可复制操盘体系 | `needs_external_verification` |
| inbox:S12 | `手把手带你做广告报告分析.docx` | Placement、Search Term、Search Impression Share、商机探测器分析链路 | `local_source_only` |
| inbox:S13 | `推测规律总结&广告拆解逻辑.xmind` | 用搜索词数量、波动和集中度推断广告结构 | `local_source_only` |

资料大多来自 Amazon 广告语境,本 SOP 只迁移“诊断方法、字段和证据链”。不得把 Amazon SA/DSP 报表字段直接写成 Shopify 后台功能;迁移到 Shopify/DTC 时应映射到 Meta、Google、GA4、GSC、Shopify Orders、UTM、coupon 和 creator_id。

## 2. 第一性原则

广告优化不能从 ACOS/ROI 这类结果指标直接跳到动作。正确顺序是:

`看报表 -> 识别变化 -> 定位层级 -> 判断原因 -> 选择动作 -> 人审 -> 执行 -> 复盘`

关键约束:
- 任何“加预算、降竞价、否词、换素材、换落地页”的建议都必须带证据。
- 指标异常先判断样本量、时间窗口、促销/库存/价格/页面变更,再判断投放结构。
- 广告数据必须和 PDP/落地页、库存、价格、Review、素材、站外活动一起看。
- Agent 只能产出诊断草案和动作建议;预算、投放上线、否词批量写入和外部平台操作需要人审。

## 3. 诊断输入

最小输入包:

| 数据 | 字段 |
|---|---|
| 商品事实 | SKU、价格、毛利、库存、主图、Review/评分、核心卖点、PDP 链接 |
| 广告结构 | campaign、ad_group、keyword、match_type、placement、creative_id、budget、bid |
| 广告结果 | impressions、clicks、CTR、CPC、spend、orders、CVR、revenue、ACOS/ROAS |
| 搜索词 | search_term、keyword、match_type、clicks、orders、spend、sales、rank |
| 站内承接 | sessions、add_to_cart、checkout、purchase、bounce/engagement、page speed |
| 站外活动 | UTM、coupon、creator_id、deal_id、content_asset_id |
| 环境变量 | 促销、价格、库存、竞品活动、节假日、Listing 改版、素材更新 |

如果只给结果指标,诊断输出必须标记为 `insufficient_evidence`。

## 4. Placement Report 诊断

Placement 的本质是判断同一商品在不同流量位置的“意图强度”和“承接质量”。

| 现象 | 可能原因 | 优先动作 |
|---|---|---|
| Top of Search CTR 高、CVR 高 | 高意图关键词匹配,页面承接好 | 适度提高权重/预算,保护核心词 |
| Top of Search CTR 高、CVR 低 | 主图/标题吸引点击,但价格、Review、PDP 或 Offer 不承接 | 先查 PDP/价格/Review/优惠,不要只加预算 |
| Product Page CTR 低、CVR 高 | 曝光少但比较场景有效 | 可小幅测试详情页相关投放,补对比素材 |
| Rest of Search 花费高、转化弱 | 普通搜索流量意图分散 | 收紧关键词、拆分预算、否定无效词 |
| 某版位突然下滑 | 竞品、预算、库存、价格或算法变化 | 拉日维度,对照外部事件和 Listing 变更 |

输出字段:
- `best_placement`
- `weak_placement`
- `evidence_window`
- `sample_size_ok`
- `page_or_offer_gap`
- `recommended_bid_budget_change`

## 5. Search Term Report 诊断

搜索词报告回答三个问题:钱花到哪里,这些词是否代表真实意图,下一步该放大还是退出。

| 搜索词类型 | 判断方式 | 动作 |
|---|---|---|
| 高转化词 | clicks/orders 足够,ACOS/ROAS 可接受 | Exact 化,单独预算,监控排名和份额 |
| 高点击低转化词 | clicks 足够但无订单或 CVR 弱 | 判断意图不准还是 PDP 承接不足,必要时否定 |
| 高花费无订单词 | 超过阈值仍无订单 | 降价/否定/拆分,保留人审原因 |
| 低点击高转化词 | 样本小但有订单 | 小预算观察,不要过早放大 |
| 品牌词/竞品词 | 与品牌防守或竞品截流相关 | 单独拆分,避免污染泛词判断 |

Agent 不应只说“否掉低效词”。必须输出:
- 触发阈值。
- 样本时间窗。
- 词与商品卖点是否匹配。
- 对应 PDP 是否解释该意图。
- 是否有库存、价格、Review 或促销异常。

## 6. Search Impression Share 与市场空间

展示份额用于判断核心词是否还有可扩量空间,以及订单下降是否来自竞争、预算或结构问题。

诊断规则:
- 展示份额下降且 CPC 上升:竞争加剧或竞品推量。
- 展示份额下降但 CPC 没变:预算不足、结构分散或排名/质量变化。
- 展示份额稳定但订单下降:检查 CVR、价格、库存、Review、页面改版和外部流量质量。
- 展示份额高但增长停滞:该词空间可能接近上限,需要找长尾词、场景词或新渠道。

商机/市场数据用于回答“要不要继续投”,而不仅是“怎么调竞价”:
- 市场容量是否足够。
- 新玩家是否快速进入。
- 点击和购买是否集中在少数品牌。
- 价格带和 Review 门槛是否与自身匹配。
- 广告增长是否会被毛利、库存或售后承接限制。

## 7. SA/DSP 与站外映射

资料中的 SA/DSP 指标可作为广告层级分类,但迁移到 Shopify/DTC 时需要映射:

| Amazon 语境 | 关注点 | Shopify/DTC 映射 |
|---|---|---|
| SA: impression share、CTR、click、CVR、ROI、CPC | 搜索曝光、点击和转化效率 | Google Ads、Microsoft Ads、GSC、GA4、Shopify Orders |
| DSP: DPVR、ACTR、DPV、ATC、Branded Search、ECPDPV、ECPATC | 站外展示、详情页访问、加购和品牌搜索 | Meta/TikTok/Display、GA4、Pixel、品牌词搜索、UTM |
| Deal/站外流量 | 短期爆发和排名/搜索联动 | Deal ID、coupon、UTM、direct/organic uplift、support load |
| Creator/UGC | 第三方信任与素材复用 | creator_id、content_asset_id、coupon、PDP video、ad creative |

## 8. 广告结构推断

当无法直接读取完整广告结构时,可以用搜索词分布做弱推断,但必须标注为 `inferred`:

| 观察 | 可能推断 | 风险 |
|---|---|---|
| 搜索词数量多、波动大、词根分散 | 自动广告或广泛匹配 | 可能混入季节、促销或竞品事件 |
| 搜索词长期稳定且高度集中 | 精准匹配或核心词稳定放量 | 需要核对 campaign 结构 |
| 固定词根在首尾延展 | 词组匹配可能性较高 | 需看匹配类型和否词 |
| 词序打乱或中间插词 | 广泛匹配可能性较高 | 需结合花费和转化判断 |
| 无关词/品牌词混入 | 自动宽泛、否词不足或结构污染 | 先拆分品牌/竞品/泛词 |

推断只用于提出检查方向,不能作为自动批量调整依据。

## 9. 动作决策树

| 症状 | 先查 | 再动作 |
|---|---|---|
| 花费上涨但订单不涨 | 样本量、Placement、Search Term、价格、Review、库存 | 收紧词、降弱版位、补 PDP 证据 |
| 点击下降 | 展示份额、竞价、预算、素材疲劳、排名 | 调预算/竞价、换素材、扩词 |
| CTR 高 CVR 低 | 页面承接、价格、Review、Offer、流量意图 | 改 PDP/落地页/优惠,或否掉错意图词 |
| CVR 高但曝光少 | 展示份额、预算、竞价、搜索量 | 小步加预算,拓展相邻词 |
| ACOS/ROAS 弱 | 毛利阈值、词/版位/素材/页面层级 | 按层级拆原因,不要一刀切停投 |
| Deal 后数据异常 | coupon、库存、客服、退款、自然搜索 uplift | 分渠道复盘,区分短期爆发与长期资产 |

## 10. Agent 输出契约

输入:

```json
{
  "time_window": "last_7d|last_14d|last_30d",
  "product": {},
  "ad_reports": {
    "placement": [],
    "search_terms": [],
    "impression_share": [],
    "campaign_summary": []
  },
  "store_metrics": {},
  "offsite_events": [],
  "constraints": {
    "budget_change_requires_approval": true,
    "external_write_allowed": false
  }
}
```

输出:

```json
{
  "diagnosis_status": "ready|insufficient_evidence|needs_human_review",
  "root_causes": [],
  "evidence": [],
  "recommended_actions": [],
  "risk_flags": [],
  "human_approval_required": true,
  "next_data_needed": []
}
```

动作建议必须包含:
- 证据来源和时间窗。
- 指标变化。
- 原因假设。
- 预期影响。
- 风险。
- 人审项。

## 11. 红线

- 不把 Amazon 报表字段直接当成 Shopify 官方能力。
- 不把课程里的算法或 GMV 目标当成事实。
- 不因单日异常自动调预算。
- 不在样本不足时给确定性结论。
- 不自动执行广告后台写操作、否词批量写入、预算调整或 Deal/站外发布。
- 不把刷量、刷票、隐藏推广或未授权素材复用写入任何 Agent 流程。
