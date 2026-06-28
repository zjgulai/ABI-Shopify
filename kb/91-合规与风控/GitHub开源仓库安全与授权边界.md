---
title: GitHub 开源仓库安全与授权边界
stage: 91-合规与风控
layer: 横切层
tags: [github, license, security, mcp, admin-api, token, deprecated]
sources: [github-shopify-repos]
source_paths:
  - ../_sources/github-shopify-repos/README.md
  - ../_sources/github-shopify-repos/候选仓库矩阵_2026-06-28.md
status: local_readonly_snapshot
verification_status: local_readonly_snapshot
updated: 2026-06-28
summary: 为 Shopify GitHub 仓库萃取建立 license、token、Admin API、deprecated、社区 MCP 的红线与验收门槛。
---

# GitHub 开源仓库安全与授权边界

## 本轮事实

- 2026-06-28 本轮来源包包含 26 个候选仓库。
- GitHub API 未认证额度已用完,后续取证改用 `git ls-remote` 和 raw README/License。
- 多个仓库 README 暴露出状态风险:
  - `Shopify/shopify-api-js`: README 显示 repo 已合并到 `Shopify/shopify-app-js`。
  - `Shopify/polaris-tokens`: README 标题包含 `LEGACY`。
  - `Shopify/polaris-viz`: README 有 `Deprecation Notice`。
  - 社区 MCP 仓库可连接 Admin GraphQL 或执行 store data 操作,默认高风险。

## 状态口径

| 状态 | 含义 | 当前例子 |
|---|---|---|
| `imported` | 已入正式专题,可作为工程模式参考 | `Shopify/hydrogen`, `Shopify/dawn`, `Shopify/cli`, official app templates, `Shopify/ui-extensions` |
| `merged` | 已融合为方法或风险提示,不单独作为官方事实 | community Hydrogen templates, `mock-bridge`, Polaris historical materials |
| `copied_only` | 仅保留来源快照,不进入核心打法 | `julionc/awesome-shopify`, `vercel/commerce` |
| `needs_external_verification` | README 暴露 moved/deprecated/live-write/Admin GraphQL 等风险,实践前需再次核验 | `Shopify/shopify-api-js`, community Admin MCP |
| `skipped` | 本轮不入库 | 未命中候选范围的泛 commerce 仓库 |

## License 边界

- `MIT` 仓库可以作为实现参考,但仍要保留 attribution 和 license 文件。
- `custom/copyright`、source-available、未知 license 的仓库不得复制源码进入正式产品。
- 本知识库只保存摘要、HEAD 前缀、README/License sha256 前缀和工程模式,不保存大段源码。
- 任何要进入实际产品的代码,必须单独做 license review。

## Token 与数据边界

禁止事项:

- 把 Admin API token、Storefront token、customer account secret、private app credential 写入仓库。
- 让社区 MCP 直接连接真实生产店铺。
- 让 Agent 执行未经审批的 GraphQL mutation。
- 把客户、订单、支付、地址、邮箱、电话等敏感数据写入日志或 prompt。

允许事项:

- 读取公开 README、文档和 examples。
- 在本地 mock 或测试店做只读验证。
- 在 `.env.example` 里写变量名和说明。
- 对写操作生成 dry-run preview,等待人工审批。

## MCP/Admin API 风险等级

| 等级 | 场景 | 要求 |
|---|---|---|
| L0 | 读公开文档、schema、README | 可直接用于知识库萃取 |
| L1 | 读测试店非敏感数据 | 需要测试店、最小 scope、日志脱敏 |
| L2 | 写测试店数据 | 需要 dry-run、审批、回滚记录 |
| L3 | 读生产店数据 | 需要业务授权、最小 scope、审计 |
| L4 | 写生产店数据 | 默认禁止;必须明确授权、变更窗口、回滚方案和验收记录 |

## Deprecated / Legacy 处理

- README 明示 `Deprecated`、`LEGACY`、`moved` 的仓库,只能进入迁移参考或历史上下文。
- 不用 star 数抵消 deprecated 风险。
- 如果旧仓库指向新仓库,正式方案只引用新仓库;旧仓库保留为迁移证据。

## 入库验收门槛

1. 每个仓库有 `source_url`、HEAD 前缀、README 状态、license 状态、import status。
2. 每篇专题写清 `local_readonly_snapshot`,不把 README 信号升级成官方承诺。
3. 所有社区 MCP 标 `needs_external_verification` 或 `needs_security_review` 风险。
4. RAG/KG/site 重建通过后,再视为知识库入库完成。
