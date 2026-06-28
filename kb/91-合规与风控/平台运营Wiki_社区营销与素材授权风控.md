---
title: 平台运营 Wiki 萃取 · 社区营销与素材授权风控
stage: 91-合规与风控
layer: 横切层
tags: [platform-operations-wiki, 风控, Reddit, Facebook, KOL, UGC, 素材授权, 联盟营销]
sources: [platform-operations-wiki, E012, E014, E015, E046, E076, E080, E081]
status: verified
updated: 2026-06-27
summary: 为 Reddit、Facebook、YouTube、PR、KOL、UGC、联盟和素材复用建立前置风险检查与人审边界。
verification_status: local_source_only
---

# 平台运营 Wiki 萃取 · 社区营销与素材授权风控

## 1. 抽取边界

本篇来自 platform-operations-wiki 的社区、红人、PR、联盟和素材策略资料。资料中涉及平台规则和算法解释的部分具时效性,执行前需另查官方或一手规则；本篇只沉淀风险类别和人审清单。

## 2. Reddit/GEO 风控

Reddit 资料强调社区信任优先。迁入 ABI 后,Reddit 或 GEO 任务必须经过以下检查:

- 是否选择了相关 Subreddit 和真实问题帖。
- 是否阅读并记录版规。
- 是否用中立、完整、可独立引用的回答解决问题。
- 是否披露与品牌或产品的关联。
- 是否避免重复链接、硬广、隐藏推广、投票操控和批量复制回答。
- 是否控制品牌提及比例,以贡献内容为主。

任何涉及品牌发布、链接、产品推荐或账号身份的 Reddit 动作,默认 `manual_review_required=true`。

〔来源:platform-operations-wiki · E080〕

## 3. Facebook/Meta 社群与素材风控

Facebook 群组和 Meta 素材资料可抽象出两条风控线:

| 风险 | 表现 | ABI 处理 |
|---|---|---|
| 社群滥用 | 新号直接发商业链接、重复发帖、伪装普通用户、诱导评价 | 阻断,需人工重写为社区贡献内容 |
| 素材误导 | 夸大功效、虚假对比、未经授权媒体/UGC、伪造权威背书 | 阻断,需法务/品牌/投放人审 |
| 账号关联 | 多账号环境混乱、异常登录、强关联操作 | 记录为高风险,不得自动化执行 |
| 算法误读 | 把未核验算法观点当确定规则 | 标记 `needs_external_verification` |

Facebook Andromeda 素材策略可以作为“语义多样性测试假设”,但不能写成官方算法事实。〔来源:platform-operations-wiki · E081〕

## 4. KOL/UGC/YouTube 授权

红人内容要先确认授权范围,再复用到广告、官网、EDM、SEO 或 Amazon/Shopify 页面:

必填字段:
- `creator_id`
- `platform`
- `content_url`
- `usage_scope`
- `usage_duration`
- `ad_usage_allowed`
- `whitelisting_allowed`
- `edit_allowed`
- `territory`
- `compensation`
- `approval_record`

如果授权只覆盖自然发布,不得自动复用到付费广告或官网页面。

YouTube 红人筛选可看粉丝数、发布频率、点赞评论、同类视频和评论质量,但联系信息、价格和频道状态必须实时核验。〔来源:platform-operations-wiki · E015〕

## 5. PR 与联盟风控

PR 和联盟不只是获客,也会影响品牌可信度和合规:
- PR 文章不得伪造媒体背书或隐藏商业合作关系。
- 联盟佣金、折扣码和 Cookie 归因规则必须透明记录。
- Creator Store Front 页面要保留品牌一致性,但不能伪造红人独立评价。
- Deal/促销不得使用虚假原价、虚假折扣、刷票或多账号操控。

灰色或高风险动作即使在源资料中出现,也不进入 ABI 自动化能力;只能记录为风险案例。〔来源:platform-operations-wiki · E046/E076〕

## 6. 人审闸

以下动作必须人审:
- 外部社区发帖或评论。
- 广告上线、扩预算、修改预算。
- 使用红人/UGC/竞品素材。
- 设置折扣码、佣金、联盟规则。
- 使用媒体 Logo、奖项、认证或第三方背书。
- 任何医疗、功效、安全、婴童、隐私或金融相关声明。

审批记录至少包含:任务 ID、操作者、素材/文案版本、来源、风险检查结果、审批人、审批时间和回滚方式。
