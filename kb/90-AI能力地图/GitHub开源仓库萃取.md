---
title: GitHub 开源仓库萃取(Shopify AI · 代理式商务 · Agent 工具)
stage: 90-AI能力地图
layer: 横切层
tags: [github, 开源, mcp, ucp, hydrogen, agent, 萃取]
sources: [github, web]
status: verified
updated: 2026-06-26
summary: 从 GitHub 萃取的与 Shopify AI 全链路经营相关的高价值开源仓库,按类别 + 对应流程节点 + 发力点整理。
---

# 🐙 GitHub 开源仓库萃取

> 本次用 web 检索萃取(Chrome 扩展按域名策略拦截了 github.com 直访,GitHub 又有 Cloudflare 反爬,故未直抓页面;以下基于官方/权威检索结果,不臆造 star 数)。

## A. Shopify 官方(建站 / Agent 接入)
- **`Shopify/Shopify-AI-Toolkit`**(MIT,2026-04-09 开源)— 把官方 **MCP server 栈 + 16 个 agent skills + Claude Code 插件**打成一个命名空间;让 Claude Code / Cursor / VS Code / Gemini CLI / Codex 直连 Shopify Admin API、文档、GraphQL schema、代码校验与真实店铺操作。16 skills 覆盖 Admin GraphQL 客户端、主题开发、headless、custom data、Functions、UI extensions。→ [[02-建站与基础设施]] / [[10-自动化编排]]。**发力点**:你「一句话建/改店」的官方落点。
- **`Shopify/hydrogen`**— headless 店面框架;已加 **Storefront MCP 代理**(`/api/mcp` → Storefront MCP),供 AI agent 接入。→ [[02-建站与基础设施]] / [[06-转化优化CRO]]。
- **Shopify Dev MCP / Storefront MCP**(官方)— 开发态(文档/schema/代码校验)与运营态(目录/购物车/政策/订单)的 Agent 接口。→ [[02-建站与基础设施]] / [[09-客户与会员运营]] / [[10-自动化编排]]。

## B. 代理式商务标准
- **`universal-commerce-protocol/ucp`**(Apache 2.0)— UCP 规范与文档。Google + Shopify 联合,Etsy/Wayfair/Target/Walmart 等 **20+ 伙伴**(含 Adyen/Amex/Mastercard/Stripe/Visa)。传输:REST / JSON-RPC + **AP2(Agent Payments)+ A2A + MCP**。2026-01-11 NRF 发布。→ [[10-自动化编排]] / [[09-客户与会员运营]] / [[01-选品与市场调研]]。**发力点**:让你的商品「被 AI 渠道发现并成交」的开放底座。
- **`Upsonic/awesome-ucp`**— UCP 资源/工具/实现 清单(追踪生态)。

## C. 社区 Shopify MCP / Hydrogen 工具
- **`commerce-atoms/mcp-hydrogen-kit`**— 只读 MCP 工具(路由发现、文件大纲、schema 查询、架构校验),「尊重边界」的 Agent 友好工具。→ [[02-建站与基础设施]]。
- **`QuentinCody/shopify-storefront-mcp-server`**、**`ramakay/ShopifyMockMCP`**(对接 Mock.shop 便于本地测试)— 社区 Storefront MCP 实现,做 PoC/选型参考。→ [[10-自动化编排]]。

## D. Agent / Skill / 多平台萃取(你书签关注的方向)
- **`Panniantong/agent-reach`**— 本地 CLI,给 Agent 读取 Twitter/Reddit/YouTube/GitHub/B站/小红书/抖音 的能力,零 API 费、cookie 本地存。→ [[07-数据与归因]] / [[01-选品与市场调研]] / [[09-客户与会员运营]]。**注意**:抓取属灰色,需评估各平台 ToS 与封号风险(见 [[91-合规与风控]]);本知识库的多平台扩展优先用 **Chrome(你已登录会话,只读)** 或官方 API。
- **`Thysrael/Horizon`**— AI 信息雷达,聚合 HN/Reddit/Twitter/GitHub,打分去重、双语简报。→ [[01-选品与市场调研]] / [[07-数据与归因]](选品/趋势雷达范式)。
- **Karpathy 的 `CLAUDE.md`**(单周 44k star,书签来源)、**`Njengah/claude-code-cheat-sheet`**、**Trellis**(Claude Code 持久记忆)— Agent 工程「规范 + 记忆」。→ [[10-自动化编排]] / [[92-组织与SOP]]。
- **`The-Swarm-Corp/AutoHedge`**(多 Agent 组队范式)、**`awesome-one-person-company`**(一人公司精益)、**universalDownloader**(多平台视频下载,素材采集)。→ 分别 [[10-自动化编排]] / [[00-战略与定位]] / [[04-内容与素材生产]]。

## 多平台扩展的下一步
- **GitHub**:已并入本库(本文)。
- **小红书 / 抖音 / Reddit**:可在 Chrome 扩展放行对应域名后,由我用**你已登录的会话只读萃取**(合规、无需第三方抓取代码);或走官方 API。
- 把以上仓库作为「能力来源」纳入 [[10-自动化编排]] 的工具层选型。
