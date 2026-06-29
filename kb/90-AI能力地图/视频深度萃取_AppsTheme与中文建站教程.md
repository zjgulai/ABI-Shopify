---
title: 视频深度萃取 · Apps/Theme 与中文建站教程
stage: 90-AI能力地图
layer: 横切层
tags: [youtube, t6, shopify-apps, theme-development, 中文教程, 建站SOP]
sources: [youtube, browser-harness, 用户提供]
source_paths:
  - ../../tmp/t6_apps_theme_batch_20260629/raw/16_1EgjCxk0-kM_Best_Apps_For_Shopify_Dropshipping_as_a_Beginner_metadata.json
  - ../../tmp/t6_apps_theme_batch_20260629/raw/29_aKIHLrdsv8o_Top_Shopify_Apps_You_NEED_for_More_Sales_in_2025_metadata.json
  - ../../tmp/t6_apps_theme_batch_20260629/raw/39_okSKWf8PBNY_Shopify_Theme_Development_-_Build_a_theme_from_scratch_metadata.json
  - ../../tmp/t6_apps_theme_batch_20260629/raw/42_1o6cKeK24Mw_Shopify_2026_metadata.json
status: verified
verification_status: page_metadata_chapters_v0_1
updated: 2026-06-29
summary: 基于 browser-harness 只读复核 Ac Hampton Apps 短视频、Code with Chris Theme 开发长课和梧桐小讲堂中文 Shopify 建站教程,补充 Apps 选型、Theme 工程路径和中文新人 onboarding SOP。
---

# 视频深度萃取 · Apps/Theme 与中文建站教程

> 证据边界:本批使用真实 Chrome + browser-harness 只读打开播放页。没有下载视频,没有调用外部 provider,没有写外部平台。`1EgjCxk0-kM` 与 `aKIHLrdsv8o` 是 Ac Hampton Apps 短视频,页面可读信息较少;`okSKWf8PBNY` 和 `1o6cKeK24Mw` 打开后真实作者分别为 `Code with Chris the Freelancer` 与 `梧桐小讲堂`,按跨频道资料入库。

## 0. 证据表

| 清单序号 | video_id | 页面标题 | browser-harness 页面作者 | 时长 | 证据等级 | 入库状态 |
|---:|---|---|---|---:|---|---|
| 16 | `1EgjCxk0-kM` | Best Apps For Shopify Dropshipping as a Beginner! | Ac Hampton | 10 秒 | 页面说明 + 可见字幕片段;转写未读出 | imported_v0.1 |
| 29 | `aKIHLrdsv8o` | Top Shopify Apps You NEED for More Sales in 2025 | Ac Hampton | 60 秒 | 页面说明 + 可见字幕片段;转写未读出 | imported_v0.1 |
| 39 | `okSKWf8PBNY` | Shopify Theme Development - Build a theme from scratch | Code with Chris the Freelancer | 13,934 秒 | 页面说明 + 章节目录 | imported_cross_channel_v0.1 |
| 42 | `1o6cKeK24Mw` | Shopify 零基础建站新手教程【2026最新版】 | 梧桐小讲堂 | 4,948 秒 | 页面说明 + 中文章节目录 | imported_cross_channel_v0.1 |

## 1. Apps 选型:从“推荐清单”降级为“能力审计”

本批两条 Apps 视频都是 Ac Hampton 页面事实,但只读证据未返回完整推荐清单:

- `1EgjCxk0-kM`:10 秒短视频;页面说明主要是课程、社群、Shopify、AutoDS、Minea 等链接。
- `aKIHLrdsv8o`:60 秒短视频;页面说明主张 `Top 10 Shopify Apps` 可帮助 scale、increase conversions、improve customer experience,但未列出完整 app 名称。

因此 ABI 不应把它们写成“Ac Hampton 推荐 app 清单”,而应沉淀为 Apps 选型审计框架:

| App 能力层 | 典型问题 | 进入 ABI 前的证据 |
|---|---|---|
| 履约/供应商 | 是否需要连接 AutoDS、供应商、tracking、库存同步? | 商品来源、订单量、tracking 回填字段、退款风险 |
| CRO/upsell | 是否提升 AOV、bundle、post-purchase、cart drawer 或 sticky CTA? | 基线 AOV/CVR、实验假设、回滚方式 |
| 评论/社会证明 | 是否导入 review、UGC、Q&A 或评分? | 授权来源、导入字段、展示位置、反虚假评论检查 |
| 客服/消息 | 是否接 Shopify Inbox、FAQ、AI 客服或邮件自动化? | 客服知识库、隐私字段、人工升级路径 |
| 数据/归因 | 是否改变 pixel、UTM、server-side event 或报表口径? | 数据字段、事件定义、去重逻辑、权限范围 |
| 页面/主题 | 是否注入脚本、app block、section 或 theme asset? | 性能影响、主题兼容性、卸载残留检查 |

### App 审计卡

正式接入任何 Shopify App 前,ABI 经营作战台应生成一张 `app_intake_card`:

```json
{
  "app_name": "",
  "use_case": "fulfillment|cro|reviews|support|analytics|theme",
  "shopify_permissions": [],
  "data_touched": ["orders", "customers", "products", "theme", "checkout"],
  "theme_injection": "none|app_block|script|asset",
  "baseline_metric": "",
  "success_metric": "",
  "rollback_plan": "",
  "billing_model": "",
  "privacy_review": "pending",
  "test_store_required": true,
  "approval_required": true
}
```

## 2. Theme 工程路径:Code with Chris 长课 v0.1

`okSKWf8PBNY` 虽出现在 Shopify 搜索清单中,但播放页作者为 `Code with Chris the Freelancer`,不是 Ac Hampton。页面说明和章节可支撑 Theme 工程路径 v0.1:

| 章节 | 主题 | ABI 落点 |
|---|---|---|
| `0:00` | Introduction | 明确主题开发目标和边界 |
| `6:08` | Project / Store Setup | 测试店、CLI、本地预览、版本管理 |
| `9:27` | Laying the foundation | theme 目录、Liquid、templates、sections、snippets、assets |
| `1:05:24` | Introducing JSON into our theme | JSON templates / schema / Online Store 2.0 配置化 |
| `2:07:53` | Introducing Blocks into our theme | section blocks、merchant-editable content、复用组件 |
| `2:48:45` | Introducing Javascript into our theme | 渐进增强、交互、性能和卸载边界 |
| `3:50:55` | Conclusion | 发布前检查和后续学习 |

### Theme 开发检查表

1. 先判定是 `Theme`、`Hydrogen` 还是 `Theme + App/Extension` 混合模式。
2. Theme 开发必须先接测试店或本地 preview,不得直接改生产主题。
3. 主题结构要分层:layout、templates、sections、snippets、assets、locales、config。
4. JSON template 和 section schema 要服务商家可编辑,不要把所有内容写死进 Liquid。
5. Blocks 用于模块化商品卖点、FAQ、UGC、对比表、集合入口和落地页承接。
6. JavaScript 只做必要交互,并记录性能影响、依赖、降级方案和卸载残留。
7. 上线前必须做移动端、速度、SEO metadata、collection/PDP、cart、policy page 和 analytics 检查。

## 3. 中文 Shopify 建站 onboarding:梧桐小讲堂 v0.1

`1o6cKeK24Mw` 打开后作者为 `梧桐小讲堂`。它不是 Ac Hampton 视频,但对中文新手 onboarding 很有价值。页面说明和章节覆盖:

| 章节 | 内容 | ABI 节点 |
|---|---|---|
| `5:11` | Shopify 后台介绍 | 02 |
| `5:51` / `7:58` / `17:51` | 更换主题、修改主题、细节元素 | 02 / 06 |
| `20:36` / `28:28` | 新增产品、商品可变参数 | 03 |
| `31:20` | 产品 SEO 优化设置 | 03 / 06 |
| `33:55` | Collection 分类 | 03 |
| `42:53` | 产品详情页面设计 | 03 / 06 |
| `47:19` / `48:52` | 其他页面、导航条 | 02 / 06 |
| `53:37` | Policy 页面 | 02 / 91 |
| `59:06` | Theme Settings | 02 |
| `1:02:44` / `1:04:36` | 收款、商店基础设定 | 02 / 91 |
| `1:08:12` / `1:13:47` | 运费、指定产品运费 | 08 |
| `1:16:32` | 关联域名发布商店 | 02 |

### 中文新人任务包

ABI 可把该教程抽象为“中文新人 Shopify 建站任务包”:

1. 账号与后台:熟悉 Admin、Settings、billing、staff、market/language 基础入口。
2. 主题与导航:选择主题、编辑 header/footer、导航菜单、首页 section。
3. 商品与集合:创建产品、变体、图片、SEO、collection 与模板。
4. 页面与政策:About、Contact、FAQ、Shipping、Return、Privacy、Terms。
5. 收款与物流:payment、shipping profile、product-specific shipping、tax 边界。
6. 发布前检查:domain、password、移动端、测试订单、邮件通知、客服入口。

## 4. 对 ABI 经营作战台的增量

| 增量模块 | 内容 | 目标落点 |
|---|---|---|
| App 审计卡 | 权限、数据、脚本注入、计费、指标、回滚 | 02 / 06 / 07 / 91 |
| Theme 工程任务 | setup、Liquid、JSON template、blocks、JS、发布检查 | 02 / 03 / 06 / 10 |
| 中文 onboarding | 后台、主题、产品、SEO、collection、政策、收款、运费、域名 | 02 / 03 / 06 / 08 / 91 |
| 跨频道归因闸 | 播放页作者优先于搜索清单来源 | 90 / 91 |

## 5. 后续补强

- Apps 视频若要升级为转写级,需要 Chrome UI 转写面板稳定返回正文或用户提供字幕;当前不写 app 名称推荐清单。
- Theme 长课若要升级为逐字稿级,需完整字幕或课程笔记;当前只保留章节结构和工程路径。
- 中文教程适合作为 `02-建站与基础设施` 的新手任务包,但具体 Shopify 后台 UI 可能随版本变化,执行前需用测试店复核。
