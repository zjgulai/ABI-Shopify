---
title: Hydrogen 脚手架 SOP — Agent-first headless 建站
stage: 02-建站与基础设施
layer: 流程阶段
tags: [hydrogen, oxygen, headless, mcp, scaffold, sop]
sources: [shopify官方, web]
status: verified
updated: 2026-06-26
summary: Shopify Hydrogen(agent-first)脚手架到部署的可执行 SOP:何时上 headless、create 命令、连店、Storefront MCP 代理、Oxygen/Vercel 部署。
---

# ⚡ Hydrogen 脚手架 SOP(Agent-first headless)

> 何时用:主题(Online Store 2.0)满足不了的**深度定制 / 长期 headless** 项目;否则先用主题起步更快、更省维护。

## 1. 脚手架
```bash
# 快速试(本地 mock 数据,先看效果)
npm create @shopify/hydrogen@latest -- --quickstart --mock-shop
# 正式项目(交互选择 语言/样式/路由)
npm create @shopify/hydrogen@latest
# 常用 flags: --install-deps --path --language ts --styling tailwind
```

## 2. 连接店铺
- 用 **Shopify CLI** 登录并 link 到你的店:`shopify hydrogen link`(或在 `.env` 配 `PUBLIC_STOREFRONT_API_TOKEN` 等);开发期可继续用 `--mock-shop`。

## 3. Agent-first 开发(本库重点)
- 装 **AI-Toolkit**,用 `shopify-hydrogen` skill 让 Claude Code/Codex **脚手架 + 补全 + 校验**(Dev MCP 实时查 schema,生成"经校验"代码)。见 [[90-AI能力地图/AI-Toolkit技能SOP_每节点]]。
- 新版 Hydrogen **agent-first、框架/运行时无关**:`/api/mcp` 内置 **Storefront MCP 代理**,可让买家侧 Agent 直接接店铺数据。
- 本地开发:`npm run dev`。

## 4. 部署
- **Oxygen(Shopify 托管,免费)**:`npm i -g @shopify/oxygen` → `shopify hydrogen deploy`(或 GitHub Actions CI/CD)。Oxygen 已原生支持 MCP。
- **Vercel / Cloudflare / Node / Deno**:新版运行时无关,可部署到任意 `fetch` 环境。

## 5. 人审闸
- 上线、绑定域名、支付/结账改动 → 人审;核心结账保持 Shopify 原生(用 Functions/UI 扩展定制,见 [[06-转化优化CRO]])。

## 6. 选型提醒
- 新版 all-new Hydrogen 当前为**预览**,生产前评估稳定性;不确定就先主题 + Functions/UI 扩展。

### 来源
- hydrogen.shopify.dev · shopify.dev《Getting started with Hydrogen and Oxygen》https://shopify.dev/docs/storefronts/headless/hydrogen/getting-started
- npm `@shopify/hydrogen` / `@shopify/oxygen`
