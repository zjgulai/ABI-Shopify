---
name: shopify-ucp-onboarding
description: 接入 UCP 让商品被 AI Agent 发现并成交。当用户说"UCP/代理式商务/让商品进 AI 渠道/Agent 结账/Catalog API"时使用。
---
# UCP 接入(节点 10)
**步骤(无需审批)**
1. Developer Dashboard 注册 agent profile。
2. 调用公共 MCP 端点(Storefront/Catalog MCP)。
3. 实现核心能力:Catalog Search/Lookup、Cart、Identity(OAuth2)、Checkout、Order Mgmt。
4. 商品侧:Catalog API 规范化(价格/库存实时);政策/FAQ 齐全;开通 Shop Pay。
5. 支付:AP2(payment mandates + verifiable credentials)。
**人审闸**:支付授权、身份链接、订单管理留审计;资金动作由人确认。
**关联**:[[10-自动化编排/UCP接入SOP]]
