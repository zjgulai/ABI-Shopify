---
title: GitHub Shopify App 与 MCP 工程实践
stage: 10-自动化编排
layer: 流程节点
tags: [github, shopify-app, react-router, remix, admin-api, mcp, graphql, automation]
sources: [github-shopify-repos, Shopify/shopify-app-template-react-router, Shopify/shopify-app-template-remix, Shopify/shopify-api-js, Shopify/dev-mcp-gemini-cli, GeLi2001/shopify-mcp]
source_paths:
  - ../_sources/github-shopify-repos/README.md
  - ../_sources/github-shopify-repos/候选仓库矩阵_2026-06-28.md
status: local_readonly_snapshot
verification_status: local_readonly_snapshot
updated: 2026-06-28
summary: 从 Shopify 官方 App templates、Admin API SDK、Dev MCP setup 与社区 MCP 仓库中提炼 App/Agent 自动化编排的安全工程路径。
---

# GitHub Shopify App 与 MCP 工程实践

## 来源批次

本页基于 [`_sources/github-shopify-repos`](../_sources/github-shopify-repos/README.md) 的 26 仓库只读快照。MCP/Admin API 工具涉及真实店铺访问能力,本页默认 `no provider call`、`no live store write`、`needs_security_review`。

## 仓库信号

| 仓库 | 本轮状态 | 自动化价值 | 边界 |
|---|---|---|---|
| [`Shopify/shopify-app-template-react-router`](https://github.com/Shopify/shopify-app-template-react-router) | imported | 官方 React Router app template; README 指向 Shopify app docs 与 `shopify app init` 模板命令 | 当前优先 app template 参考 |
| [`Shopify/shopify-app-template-remix`](https://github.com/Shopify/shopify-app-template-remix) | imported | README 明确 Remix 已与 React Router 合并 | 作为迁移/历史兼容参考 |
| [`Shopify/shopify-app-template-node`](https://github.com/Shopify/shopify-app-template-node) | imported | Node + React app template 基础结构 | P1,需与当前 React Router 模板比较 |
| [`Shopify/shopify-api-js`](https://github.com/Shopify/shopify-api-js) | needs_external_verification | README 显示该 repo 已合并到 `Shopify/shopify-app-js`,但仍能说明 Admin/Storefront API 客户端职责 | 不作为当前包源;仅保留迁移信号 |
| [`Shopify/dev-mcp-gemini-cli`](https://github.com/Shopify/dev-mcp-gemini-cli) | imported | 官方 Dev MCP 接入 Gemini CLI,可代表“开发态文档/schema/指导”类 MCP | 不等于生产 Admin API 写入权限 |
| [`GeLi2001/shopify-mcp`](https://github.com/GeLi2001/shopify-mcp), [`colbymchenry/shopify-graphql-admin-mcp`](https://github.com/colbymchenry/shopify-graphql-admin-mcp) | needs_external_verification | 社区 MCP 可连 Admin GraphQL / store data | 高风险,必须安全评审,禁止直接接真实 token |

## App 自动化架构

一个可被 Agent 协作的 Shopify App,建议拆成四层:

1. App shell:
   - React Router/Remix 路由、embedded app layout、auth callback、session storage。
   - 由官方 app template 建立基础结构。
2. Shopify API adapter:
   - Admin GraphQL、REST、Storefront GraphQL 客户端。
   - 明确 online/offline token、scope、rate limit、retry、idempotency。
3. Domain service:
   - 商品、库存、订单、客户、折扣、内容、metaobject 等业务操作。
   - 所有写操作必须有 dry-run、preview、approval、audit log。
4. Agent/MCP facade:
   - 开发态: 读取 docs、schema、代码上下文、生成建议。
   - 运营态: 只读查询优先,写操作必须通过策略网关和人工审批。

## MCP 分层

| MCP 类型 | 可做 | 不可默认做 |
|---|---|---|
| Dev MCP | 读文档、读 API schema、代码校验、生成脚手架建议 | 直接改生产店铺 |
| Storefront MCP | 读商品目录、购物车、政策、前台结构 | 绕过店铺授权或顾客隐私边界 |
| Admin MCP | 查询/管理产品、订单、客户、库存、metaobject | 未审批的 GraphQL mutation、批量修改、真实客户数据导出 |
| Mock MCP / Mock Bridge | 本地测试和演示 | 代替真实 Shopify 行为验收 |

## 开发 SOP

1. 用官方 template 初始化 app,记录 template repo 和 HEAD 前缀。
2. 在本地 `.env.example` 只放变量名,不放任何 token。
3. 所有 Admin API 调用先写成 service 函数,再暴露给 UI/Agent。
4. 每个写操作必须有:
   - `dry_run`。
   - diff/preview。
   - explicit approval。
   - rollback 或补偿动作。
   - audit log。
5. MCP 工具先接 sandbox/test store;没有测试店时只能保留为设计和 mock。
6. 社区 MCP 先做源码安全检查:
   - 是否收集/上传 token。
   - 是否允许任意 GraphQL mutation。
   - 是否有外部遥测。
   - 是否把店铺数据写日志。
   - 是否支持只读模式和 scope 限制。

## 和 ABI 节点的对应

- `02-建站与基础设施`: CLI、app scaffold、embedded app 基础。
- `07-数据与归因`: API 数据读取、事件、报表、归因管道。
- `10-自动化编排`: App service、Agent facade、MCP、审批网关。
- `91-合规与风控`: token、scope、Admin GraphQL mutation、客户/订单数据。
- `92-组织与SOP`: app 初始化、code review、安全评审、测试店验收。
