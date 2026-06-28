---
title: GitHub 开源仓库萃取(Shopify 工程仓库 · AI · Agent 工具)
stage: 90-AI能力地图
layer: 横切层
tags: [github, 开源, mcp, ucp, hydrogen, agent, theme, app-template, 萃取]
sources: [github, github-api, git-ls-remote, raw-readme, web]
source_paths:
  - ../_sources/github-shopify-repos/README.md
  - ../_sources/github-shopify-repos/候选仓库矩阵_2026-06-28.md
status: local_readonly_snapshot
verification_status: local_readonly_snapshot
updated: 2026-06-28
summary: 从 GitHub 萃取与 Shopify 建站、Theme、Hydrogen、App、Checkout、MCP/Agent 相关的高价值仓库,按类别、流程节点和风控边界整理。
---

# 🐙 GitHub 开源仓库萃取

> 2026-06-28 批次:已确认用户 Chrome 打开的 GitHub 搜索页为 `https://github.com/search?q=shopify&type=repositories`;仓库事实层以 GitHub 官方搜索 API 已取得结果、`git ls-remote` HEAD、raw README/License 摘要为依据。GitHub API 未认证额度已用完,后续取证不继续打 API。所有社区 MCP/Admin API 仓库默认需要安全复核,不接真实店铺 token。

## 2026-06-28 Shopify 工程仓库批次

来源包: [`_sources/github-shopify-repos`](../_sources/github-shopify-repos/README.md)。

| 类别 | P0/P1 仓库 | 入库位置 | 状态 |
|---|---|---|---|
| Headless / Theme | `Shopify/hydrogen`, `Shopify/dawn`, `Shopify/skeleton-theme`, `Shopify/cli`, `Shopify/storefront-api-examples` | [[02-建站与基础设施/GitHub_Hydrogen与Theme工程实践]] | imported |
| Checkout / CRO | `Shopify/ui-extensions`, `ctrlaltdylan/mock-bridge`, `Shopify/polaris-tokens`, `Shopify/polaris-viz` | [[06-转化优化CRO/GitHub_Checkout与AppBridge工程实践]] | imported / merged |
| App / MCP / API | `Shopify/shopify-app-template-react-router`, `Shopify/shopify-app-template-remix`, `Shopify/shopify-app-template-node`, `Shopify/dev-mcp-gemini-cli`, `GeLi2001/shopify-mcp` | [[10-自动化编排/GitHub_ShopifyApp与MCP工程实践]] | imported / needs_external_verification |
| 安全与授权 | `Shopify/shopify-api-js`, community Admin MCP, legacy/deprecated Polaris repos | [[91-合规与风控/GitHub开源仓库安全与授权边界]] | merged / needs_external_verification |

本轮关键结论:

- `Shopify/hydrogen` 是当前 headless storefront 主参考;README 明确 Hydrogen legacy v1 已迁到独立仓库。
- Theme 侧优先看 `Shopify/dawn` 和 `Shopify/skeleton-theme`,再用 `Shopify/cli` 做开发入口。
- App 侧优先看 `shopify-app-template-react-router`;`shopify-app-template-remix` 可作为 Remix 到 React Router 合流/迁移参考。
- `Shopify/shopify-api-js` README 显示已合并到 `Shopify/shopify-app-js`,不再作为当前包源。
- `Shopify/polaris-tokens` 是 legacy,`Shopify/polaris-viz` 有 deprecation notice,只能做历史/迁移参考。
- 社区 MCP 能连接 Admin GraphQL 或 store data 的仓库只进入风控与选型观察,不进入真实店铺操作链路。

结构级补充:

- 2026-06-28 追加 P0 官方仓库 git tree 快照,覆盖 `Shopify/hydrogen`、`Shopify/dawn`、`Shopify/skeleton-theme`、`Shopify/cli`、React Router/Remix App templates、`Shopify/storefront-api-examples`、`Shopify/ui-extensions`、`Shopify/dev-mcp-gemini-cli`。
- 正式 SOP 见 [[92-组织与SOP/GitHub_P0官方仓库工程结构SOP]]。
- 取证方式为 blobless/no-checkout 浅层 clone + `git ls-tree` + 少量配置读取,未执行第三方代码、未安装依赖、未连接 Shopify 店铺。

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
