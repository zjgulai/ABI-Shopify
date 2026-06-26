---
title: 建站与基础设施
stage: 02-建站与基础设施
layer: 流程阶段
tags: [建站, shopify, 支付, 站群, hydrogen, cms]
sources: [周报, twitter, shopify官方]  # 三源已融合 + 2026官方账号深化
status: verified      # 三源萃取完成
updated: 2026-06-25
summary: 把店“立起来”:从域名到支付到多站点的技术底座。
---

# 🏗️ 建站与基础设施

> **节点定位**:把店“立起来”:从域名到支付到多站点的技术底座。

## 1. 本节点要解决什么
完成 Shopify 店铺与基础设施搭建:主题/前端、域名、支付、税费、物流配置、App与组件、多站点与多区域架构、CMS,形成可扩展的建站底座。

## 2. 核心子主题
- Shopify 店铺初始化与套餐选择
- 主题 vs Headless(Hydrogen/Storefront API)选型
- 域名、DNS 与品牌邮箱
- 支付配置(Shopify Payments / PayPal / Stripe / 本地支付)
- 税费、配送与区域设置
- App 与组件生态(评价/弹窗/订阅/会员等)
- 多站点与站群架构、多区域与多语言(如东南亚站点拆分)
- CMS / 内容模型与帮助中心

## 3. 真实业务细节(来源:数字化中心周报)
<!-- enrich:周报 -->
**多站点/站群架构(关键)**:这是一个多店铺、多区域的 Shopify 站群——按区域拆分站点(东南亚会员中心站点拆分、H1 欧洲及其他区站点拆分计划),单周可发布 12 个站点〔周报01·站点产品组 / 周报03·软件运维组〕;切换支持 IP 强制跳转、主站东南亚市场关闭,以及广告/会员/EDM 人群数据的平稳迁移〔周报01·陈进/站点产品组·2026-03〕。

**Shopify 平台底座**:Shopify 发版、上线规则初始化与新店铺授权〔周报01·骆汉松/后端开发组·2026-02〕;采用 **Shopify Functions** 做会员价/折扣(function discount,测试店铺安装验证)〔周报01·张乐平/网站开发组·2026-03〕;主题侧性能优化并合入正式主题。

**CMS 与内容基建**:自建「用户研究系统-CMS 侧」、AIGC 外部内容引入(云盘→KMS 同步)、figma 新增 CMS 素材插件〔周报01·廖志龙/营销产品组、周桥生/平台研发组·2026-03〕。

**发布与环境**:分支名触发不同站点环境的流水线、独立站新增前后端服务与多站点发布、k8s 部署 + 健康检查自动上线与告警〔周报01/03·软件运维组〕。

> **对自动化的启示**:建站不是「一个站」,而是「一套可复制的多区域站群 + CMS + Functions + 发布流水线」——这是「一键开站」自动化的现实底座。

## 4. 发力点(来源:Twitter 书签)
<!-- enrich:twitter -->
**平台级利好(本知识库最关键的两条书签)**:
- Shopify 把店铺后台**读写权限全面开放给 AI Agent**——产品/订单/库存/SEO/图片「想改什么改什么」(背书数据:3780 亿美元年 GMV、560 万店铺)〔Twitter @AYi_AInotes〕。
- Shopify 官方发布 **AI Toolkit**——「用你喜欢的 Agent 管理店铺」,支持 Claude Code、Codex、Cursor、VS Code 等〔Twitter @Shopify〕。
> **发力点**:把「建站/改店」做成**对话式**——用编码 Agent + Shopify 官方 Toolkit/MCP 直接读写店铺,实现「一句话开站 / 上架 / 改 SEO / 换图」。这正是你「一键式建站」的官方落点(平台能力细节见 §5,编排方式见 [[10-自动化编排]])。

## 5. Shopify 官方能力 & AI 工具
<!-- enrich:shopify官方 -->
**用 AI 直接「建/改店」的官方栈(核心)**:
- **Shopify AI Toolkit**(MIT 开源):打包官方 MCP server 栈 + agent skills + Claude Code 插件进一个命名空间——可从 Claude Code/Codex/Cursor/VS Code 直接操作店铺〔Shopify 官方 · AI Toolkit〕。这正是书签里 @Shopify 那条的落地。
- **Dev MCP Server**:覆盖全平台,支持脚手架建应用、跑 GraphQL、在 Admin/UI Extensions/Liquid/Hydrogen 生成「经校验」的代码〔Shopify 官方〕。
- **Storefront MCP**:把 AI 助手接到实时店铺数据,内置 search_shop_catalog、update_cart、get_order_status 等工具〔Shopify 官方〕。
- **建站架构**:主题 vs Headless——Hydrogen(React,日历版本 2026.4.0)+ Oxygen(免费托管,Winter '26 起原生支持 MCP,是当前唯一原生支持 MCP 的运行时);2026 推荐「核心结账保持原生 + UI 扩展定制」〔Shopify 官方 / Hydrogen〕。
- **Shopify Functions + Checkout Extensibility**(Plus):对应周报里的 function discount / cart transform / checkout validation function。
> **发力点**:把「一键开站」实现为「AI Toolkit + Dev MCP 脚手架建站 → 主题/Hydrogen 选型 → Functions 定制」。


> **【2026 深化】** UCP + Catalog API + **agent-first Hydrogen**(预览,框架/运行时无关)+ MCP 家族 + AI Toolkit,构成「Agent 脚手架建站」的新底座。完整深度文档见 [Shopify 代理式商务技术栈(2026)](Shopify代理式商务技术栈2026.md)。

## 6. SOP 与自动化要点
流程:需求 → AI Toolkit 脚手架 → 主题/Hydrogen 选型 → 支付/物流/税 → 站群配置 → 发布。**可自动化**:脚手架、代码生成、多站点发布流水线;**人审**:支付/合规/域名配置。

## 7. 关联节点
- [[03-商品上架与Listing]]
- [[08-订单履约与供应链]]
- [[10-自动化编排]]
