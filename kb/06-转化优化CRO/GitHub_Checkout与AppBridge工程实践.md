---
title: GitHub Checkout 与 App Bridge 工程实践
stage: 06-转化优化CRO
layer: 流程节点
tags: [github, checkout, ui-extensions, app-bridge, polaris, cro, testing]
sources: [github-shopify-repos, Shopify/ui-extensions, Shopify/polaris-tokens, Shopify/polaris-viz, ctrlaltdylan/mock-bridge]
source_paths:
  - ../_sources/github-shopify-repos/README.md
  - ../_sources/github-shopify-repos/repos/Shopify__ui-extensions/source_summary.md
  - ../_sources/github-shopify-repos/repos/ctrlaltdylan__mock-bridge/source_summary.md
status: local_readonly_snapshot
verification_status: local_readonly_snapshot
updated: 2026-06-28
summary: 把 Checkout UI Extensions、App Bridge 测试 mock、Polaris token/viz 的 GitHub 信号转化为 CRO 工程边界和验收清单。
---

# GitHub Checkout 与 App Bridge 工程实践

## 来源批次

本页来自 [`_sources/github-shopify-repos`](../_sources/github-shopify-repos/README.md) 的只读快照。Checkout、UI Extension、App Bridge、Polaris 都属于强版本敏感区域,本页只做工程归纳,具体 API 以 Shopify 官方文档和测试店验证为准。

## 仓库信号

| 仓库 | 本轮状态 | 可萃取内容 | 风险边界 |
|---|---|---|---|
| [`Shopify/ui-extensions`](https://github.com/Shopify/ui-extensions) | imported | 公共 UI extension API 定义,README 强调 versioned API、typed JavaScript API、host surface target、sandboxed rendering | 版本敏感;不能离开目标 surface 和 API version 直接套用 |
| [`ctrlaltdylan/mock-bridge`](https://github.com/ctrlaltdylan/mock-bridge) | merged | 本地 mock Shopify Admin/App Bridge,用于 embedded app 浏览器测试 | 社区测试工具;不能替代真实 App Bridge 和 Shopify Admin 验收 |
| [`Shopify/polaris-tokens`](https://github.com/Shopify/polaris-tokens) | merged | Polaris design tokens 包,README 标题为 legacy | 只作历史/设计 token 参考,不写成当前主线 |
| [`Shopify/polaris-viz`](https://github.com/Shopify/polaris-viz) | merged | 数据可视化系统历史资料 | README 有 deprecation notice,不能当作新项目依赖推荐 |

## CRO 工程落点

### Checkout / UI Extension

UI Extension 适合做结账、客户账户、订单状态等 Shopify 一方 UI surface 上的轻量扩展。它不是普通前端组件库,每个扩展都要明确:

- `target`: 插入哪个 Shopify surface。
- `capabilities`: 能读写哪些 host data 或调用哪些 imperative API。
- `api_version`: 当前目标 API 版本。
- `merchant_config`: 商家可配置项。
- `fallback`: API 不可用、网络失败或扩展被禁用时的降级路径。

适合承接的 CRO 问题:

- 结账前后的信任信息、赠品提示、订阅/保修/加购提醒。
- 订单状态页、客户账户页的复购和服务承接。
- 与 app 后端联动的轻量营销组件。

不适合承接:

- 绕过 Shopify checkout 规则。
- 未授权读取客户敏感信息。
- 在生产 checkout 里直接实验未审批逻辑。

### App Bridge / Embedded App 测试

`mock-bridge` 的价值在于把 embedded app 的本地浏览器测试前移,避免所有交互都依赖真实 Shopify Admin、2FA、captcha 或嵌入环境。

推荐测试分层:

1. 本地组件和路由测试: 可使用 mock App Bridge。
2. Embedded app smoke: 验证 iframe、导航、toast/modal、auth redirect、session refresh。
3. 测试店 E2E: 验证真实 Admin/App Bridge 行为。
4. 生产只读检查: 只检查可见状态和配置,不写数据。

## 验收清单

- 每个 extension 都有 `target`、API version、权限、降级说明。
- 每个 CRO 实验都有指标定义: add-to-cart、checkout started、conversion、AOV、refund/complaint side effect。
- App Bridge mock 测试只作为 local smoke,最终必须有测试店或真实嵌入环境证据。
- Polaris 相关依赖先核对当前官方状态;legacy/deprecated 只能做迁移或历史参考。
- 任何影响 checkout、customer account、order status 的变更都需要人工审批和回滚方案。

## 和 ABI 节点的对应

- `06-转化优化CRO`: checkout/账户/订单状态扩展,信任与复购承接。
- `07-数据与归因`: CRO 指标、实验归因、数据看板。
- `10-自动化编排`: extension scaffold、mock 测试、CI smoke。
- `91-合规与风控`: 客户信息、支付/订单相关 surface、生产写入边界。
- `92-组织与SOP`: 实验审批、测试店验收、回滚 SOP。
