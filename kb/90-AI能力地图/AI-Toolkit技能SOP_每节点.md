---
title: Shopify AI-Toolkit 技能 × 每节点可执行 SOP
stage: 90-AI能力地图
layer: 横切层
tags: [ai-toolkit, skills, sop, mcp, claude-code, 可执行]
sources: [github, shopify官方, web]
status: verified
updated: 2026-06-26
summary: 把 Shopify-AI-Toolkit 的技能(约16–19个,随版本增长)拆成每个流程节点的可执行 SOP:何时用、用哪个 skill、怎么调、产出、人审闸。
---

# 🛠️ Shopify AI-Toolkit 技能 × 每节点可执行 SOP

> 来源:`Shopify/Shopify-AI-Toolkit`(MIT)。技能数量随版本增长(早期 16 个 skill 文件,2026 版约 19 个);以下技能名以官方 `skills/` 目录与 shopify.dev 为准(本助手未能直抓 github/shopify.dev 页面——均被 Cloudflare 反爬,故不臆造具体数字,按权威检索归纳)。

## 0. 启用与安全(先读)
- **启用**(约 5 分钟):按仓库 README 把 AI-Toolkit 作为 **Claude Code 插件 / MCP** 安装 → 用 **Shopify CLI 登录授权**你的店铺 → 在 Claude Code/Cursor/Codex 中即可用自然语言驱动这些 skill。
- **安全红线**:`shopify-admin-execution` 是**唯一能"真改店铺"的技能**(改商品/库存/配置)——它"没有撤销键"。**所有 execution 类操作必须走人审闸**(见 [[10-自动化编排]] / [[91-合规与风控]]);读/校验类技能可放手。
- 建议:先用**测试店铺**跑通,再切生产;execution 前让 Agent 先 dry-run / 打印将执行的 GraphQL mutation 供你确认。

## 1. 技能清单(按用途分组)
| 组 | 技能 | 作用 |
|----|------|------|
| 读/查 | `shopify-admin` · `shopify-storefront-graphql` · `shopify-dev` | Admin/Storefront GraphQL 查询;Dev MCP 拉文档/schema |
| **执行(真改)** | `shopify-admin-execution` | 经 Shopify CLI 对店铺做真实变更(商品/库存/配置) |
| 建站/前端 | `shopify-liquid` · `shopify-hydrogen` · `shopify-custom-data` | 主题(含模板校验)、headless、metafields/metaobjects |
| 结账/逻辑 | `shopify-functions` | 折扣/满赠/结账校验/购物车变换 |
| UI 扩展(Polaris) | Admin · Checkout · Customer-account · POS · App-home | 各场景 UI 组件扩展 |
| 客户/支付/应用 | `shopify-customer` · `shopify-payments-apps` · `shopify-partner` · `shopify-app-store-review` | 客户账户、支付应用、合作伙伴、应用过审 |
| 入门 | `shopify-onboarding-dev` · `shopify-onboarding-merchant` | 开发者/商家上手流程 |

## 2. 每节点可执行 SOP
| 节点 | 用到的 skills | 可执行 SOP(触发 → 调用 → 产出 → 人审) |
|------|--------------|------|
| [[02-建站与基础设施]] | shopify-dev, shopify-liquid, shopify-hydrogen, UI-admin/app-home, shopify-onboarding-dev | 「建店面」:`shopify-dev` 拉 schema/文档 → `shopify-liquid`/`shopify-hydrogen` 脚手架主题或 headless → 内置 **code validation** 校验 → 部署。人审:支付/域名/合规配置 |
| [[03-商品上架与Listing]] | shopify-admin(读), shopify-admin-execution(写), shopify-custom-data, shopify-storefront-graphql | 「批量上架」:`shopify-admin` 查现有结构 → 生成文案(Magic/外部)→ `shopify-custom-data` 建 metafields(PDP 字段)→ `shopify-admin-execution` 批量创建/更新商品。**人审:上架前确认 mutation** |
| [[06-转化优化CRO]] | shopify-functions, UI-checkout | 「上满赠/折扣/结账校验」:`shopify-functions` 写 function → 本地 validate → 部署 → AB。人审:实验上线 |
| [[08-订单履约与供应链]] | shopify-admin-execution | 「改库存/订单」:`shopify-admin` 查 → `shopify-admin-execution` 调整库存/履约状态。**人审:库存/退款/取消** |
| [[09-客户与会员运营]] | shopify-customer, UI-customer-account | 「会员/账户」:`shopify-customer` + customer-account UI 扩展定制会员中心。人审:权限/数据 |
| [[10-自动化编排]] | shopify-admin-execution, shopify-dev, 全部 | 编排层(Claude Code + CLAUDE.md 规范)按事件调用各 skill;**所有 execution 经人审闸**;读/校验自动化 |
| [[00-战略与定位]]/[[01-选品与市场调研]] | shopify-onboarding-merchant | 商家上手/基础配置向导 |
| [[92-组织与SOP]] | shopify-onboarding-dev, shopify-app-store-review | 开发上手流程、(若做 App)过审流程标准化 |

## 3. 其它高价值仓库的"怎么用"(深挖要点)
- **UCP(`universal-commerce-protocol/ucp`)**:在 Developer Dashboard 注册 Agent profile → 通过 REST/JSON-RPC 或 MCP 暴露 Capabilities → 用 **Catalog API** 让商品进入 AI 渠道;支付走 **AP2**。落点:[[10-自动化编排]]。
- **Dev MCP(随 AI-Toolkit)**:连到 Claude Code 后,让 Agent 实时查 Shopify 文档/GraphQL schema 并生成"经校验"的代码——建站期强烈建议常开。
- **Hydrogen(`Shopify/hydrogen`)**:`/api/mcp` 已内置 Storefront MCP 代理;用 `shopify-hydrogen` skill 脚手架,部署到 Oxygen/Vercel。
- **agent-reach / Horizon**:做"多平台信息雷达"补充选品/VOC(见 [[01-选品与市场调研]]/[[07-数据与归因]]);**合规优先用 Chrome 已登录会话或官方 API**(见 [[91-合规与风控]])。

## 4. 落地建议
把第 2 节每行作为一个**可复用 Agent skill / Runbook** 沉淀进 [[10-自动化编排]];execution 类统一接"人审 + 操作日志";先测试店铺、后生产。
