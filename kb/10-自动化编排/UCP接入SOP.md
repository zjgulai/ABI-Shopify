---
title: UCP 接入 SOP — 让商品被 AI Agent 发现并成交
stage: 10-自动化编排
layer: 流程阶段
tags: [ucp, catalog-api, ap2, mcp, agentic-commerce, sop]
sources: [shopify官方, web]
status: verified
updated: 2026-06-26
summary: Universal Commerce Protocol 接入可执行 SOP:注册 Agent profile→调公共 MCP→实现发现/购物车/结账/支付(AP2),让独立站商品进入 AI 渠道并成交。
---

# 🔌 UCP 接入 SOP

> 目标:让你的 Shopify 商品/店铺**被 AI Agent 发现、加购、结账**(代理式商务)。UCP 由 Google+Shopify 等共建(Apache 2.0),**无需审批**。

## 1. 适用判断
- 想让商品出现在 AI 购物渠道(如 Copilot 等)并在对话内成交 → 做。
- 仅自有站 DTC、暂不接 AI 渠道 → 可缓,先把 Catalog 数据规范好(见 [[03-商品上架与Listing]])。

## 2. 开发者侧接入(无需审批)
1. **注册 Agent profile**:在 Shopify **Developer Dashboard** 注册 agent profile(不用申请/审批)。
2. **调用公共 MCP 端点**:连 Storefront/Catalog MCP,即可走「product search → checkout」全流程。
3. **实现 UCP 核心能力**:Catalog Search/Lookup · Cart Building · Identity Linking(**OAuth 2.0**)· Checkout · Order Management。
4. **传输任选**:REST / JSON-RPC / **MCP** / A2A。
5. **支付**:**AP2(Agent Payments Protocol)**——payment mandates + verifiable credentials。

## 3. 商家侧(让"我的"商品进 AI 渠道)
- **Catalog 数据规范化**:用 **Catalog API** 让商品标准化、实时准确(价格/库存),AI 才能正确发现与展示。
- **政策/FAQ 齐全**:Storefront MCP 的 `search_shop_policies_and_faqs` 会被 Agent 调用。
- **开通 Shop Pay**:支持对话内结账。

## 4. 人审 / 合规闸(见 [[91-合规与风控]])
- 支付授权(AP2 mandate)、身份链接(OAuth)、订单管理需**审计日志**。
- 价格/库存必须实时准确(避免 Agent 报错单)。
- 资金动作:本助手不替你执行;授权与上线由你确认。

## 5. 验证
用 Claude Code + MCP 跑一遍:搜品 → 加购 → 结账(测试店铺),确认 profile/能力可被外部 Agent 调用。

真实店铺读写前,按 `AI-Toolkit_UCP测试店受控写验收Runbook.md` 先完成测试店授权、只读检查、写入预案、人审批准、低风险写入、写后复查与回滚记录。

### 来源
- shopify.dev《Build commerce agents with UCP》https://shopify.dev/docs/agents · 《About Catalogs》https://shopify.dev/docs/agents/catalog
- ucp.dev 与 Core Concepts:http://ucp.dev/documentation/core-concepts/
- Google Developers《Under the Hood: UCP》https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/
- Shopify Engineering《Building the UCP (2026)》https://shopify.engineering/ucp
