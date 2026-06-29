---
title: AI 素材生产与授权 SOP
stage: 04-内容与素材生产
layer: 流程阶段
tags: [AI素材, UGC, KOL, 授权, 广告素材, 素材库]
sources: [周报, twitter, shopify官方, inbox, platform-operations-wiki]
status: local_material_needs_external_verification
updated: 2026-06-28
summary: 把 AI 生成、UGC/KOL 素材、广告短视频和官网/PDP 素材纳入统一 brief、授权、标注、复用和人审流程。
---

# AI 素材生产与授权 SOP

> 适用范围:独立站首页、PDP、广告、EDM、社媒、SEO/GEO、红人/UGC 复用素材。
> 边界:本 SOP 基于本地资料萃取和内部周报经验整理;平台广告规则、音乐/图片模型条款、UGC 使用权条款执行前需要外部核验。

## 1. 输入

| 输入 | 最小字段 | 来源节点 |
|---|---|---|
| 商品资料 | SKU、卖点、规格、目标人群、禁用宣称 | [[03-商品上架与Listing]] |
| 渠道需求 | 渠道、版位、尺寸、时长、目标动作、预算边界 | [[05-营销与引流]] |
| 品牌约束 | 色彩、语气、禁用词、竞品避让、合规风险 | [[00-战略与定位]] / [[91-合规与风控]] |
| 现有素材 | UGC、KOL 返稿、历史广告、官网图、评论截图 | [[04-内容与素材生产]] |
| 授权记录 | 使用范围、地区、期限、是否允许广告投放、署名要求 | [[91-合规与风控]] |

## 2. 标准流程

### 2.1 生成素材 brief

每条素材任务必须先写成 brief,不要直接让模型自由发挥。

必填字段:
- `asset_goal`:转化、信任、解释、对比、召回、活动。
- `channel_surface`:首页、PDP、Meta Ads、Google Ads、TikTok、YouTube、EDM、Reddit、联盟红人。
- `audience`:人群、使用场景、痛点和购买阻力。
- `message`:主卖点、证据、禁止夸大点。
- `format`:图片、短视频、长视频切片、banner、对比图、FAQ 图。
- `rights_needed`:官网使用、广告使用、社媒 repost、EDM、地区、期限。
- `review_owner`:品牌、法务/合规、投放、运营。

### 2.2 生产与标注

| 步骤 | 操作 | 输出 |
|---|---|---|
| 脚本 | 用卖点、痛点、FAQ 生成 3-5 个角度 | `script_variants` |
| 分镜 | 把脚本拆成 hook、problem、proof、CTA | `storyboard` |
| 生成 | 使用 AI 图/视频/配音/剪辑工具生成初稿 | `asset_draft` |
| 标注 | 给素材打标签:卖点、场景、情绪、渠道、素材类型 | `asset_tags` |
| 人审 | 审品牌、授权、功效宣称、平台风险 | `review_record` |
| 入库 | 存入素材库,记录来源和授权 | `asset_register` |

素材标签建议:
- `product_feature`:核心功能或利益点。
- `persona`:目标用户类型。
- `scene`:使用场景。
- `proof`:评论、认证、测试、前后对比、专家背书。
- `hook_type`:痛点、结果、好奇、对比、反常识。
- `rights_status`:owned、ugc_authorized、creator_paid、needs_review、blocked。

### 2.3 授权校验

UGC、KOL、达人返稿、用户评论截图和第三方音乐/图片进入广告或官网前,至少要校验:

| 项 | 校验问题 |
|---|---|
| 使用范围 | 是否允许官网、广告、EDM、社媒二创、SEO 内容页使用 |
| 时间 | 授权期限是否覆盖活动周期和广告投放周期 |
| 地域 | 授权地区是否覆盖目标市场 |
| 人物/肖像 | 是否包含人物肖像、未成年人、医疗/健康敏感场景 |
| 素材来源 | 是否来自可追溯原始文件,是否允许二次剪辑 |
| 署名 | 是否需要保留 creator 名称、链接或 disclaimer |
| 撤回 | creator 撤回授权或平台下架时如何替换 |

授权不完整时,状态必须写为 `manual_review_required` 或 `blocked`,不要进入广告投放和官网发布。

## 3. 输出物

| 输出物 | 说明 |
|---|---|
| `creative_brief` | 单条素材任务 brief |
| `storyboard` | 短视频或图文分镜 |
| `asset_register` | 素材资产台账,含来源和授权 |
| `creative_test_matrix` | 渠道、角度、素材、落地页、UTM 的测试矩阵 |
| `review_record` | 品牌、合规、授权、人审记录 |
| `reuse_plan` | 广告、官网、EDM、SEO、社媒复用路线 |

## 4. 验收

- 每个素材都有来源、生成方式、授权状态和人审记录。
- 广告素材与落地页卖点一致,UTM 和素材标签能在 [[07-数据与归因]] 复盘。
- UGC/KOL 素材进入广告或官网前,`ad_usage_allowed` 为明确允许。
- AI 生成素材没有使用未授权品牌、人物、音乐、平台水印或竞品素材。
- 敏感宣称、效果对比、医疗/健康、儿童和价格优惠由人工确认。

## 5. 风险闸

| 风险 | 处理 |
|---|---|
| 模型生成虚假场景或夸大效果 | 回到商品资料和认证证据,无法证明就删除 |
| 自然 UGC 被当成广告授权素材 | 重新签署广告/官网使用授权 |
| 素材跨渠道复用超出授权范围 | 按渠道重新建授权记录 |
| 音乐、字体、图片来源不可追溯 | 替换为自有或明确授权素材 |
| 平台广告规则变化 | 执行前外部核验,状态保持 `needs_external_verification` |

## 6. 与站点作战台的连接

- Journey `站外全域增长` 读取本 SOP 的 `creative_test_matrix`。
- Journey `Creator Store Front / 联盟红人` 读取本 SOP 的 `asset_register`。
- `SOP Playbook Library` 中本 SOP 的默认状态应为 `local_material_needs_external_verification`。
- `Evidence & Trust Center` 中平台规则和授权条款仍需外部核验。

## 7. 来源

- `kb/04-内容与素材生产/README.md`
- `kb/91-合规与风控/平台运营Wiki_社区营销与素材授权风控.md`
- `kb/05-营销与引流/平台运营Wiki_独立站全域流量增长SOP.md`
- `kb/90-AI能力地图/内部资料萃取_独立站实操资料包.md`
- `kb/_sources/platform-operations-wiki/README.md`
