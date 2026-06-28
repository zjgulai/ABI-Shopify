---
title: GitHub P0 官方仓库工程结构 SOP
stage: 92-组织与SOP
layer: 横切层
tags: [github, p0, engineering-structure, hydrogen, theme, app-template, ui-extensions, sop]
sources: [github-shopify-repos, git-tree, Shopify/hydrogen, Shopify/dawn, Shopify/skeleton-theme, Shopify/cli, Shopify/shopify-app-template-react-router, Shopify/ui-extensions]
source_paths:
  - ../_sources/github-shopify-repos/P0官方仓库结构快照_2026-06-28.md
  - ../_sources/github-shopify-repos/p0_structure_manifest_2026-06-28.json
status: local_readonly_git_tree
verification_status: local_readonly_git_tree
updated: 2026-06-28
summary: 对 9 个 P0 Shopify 官方仓库做 git tree 级只读结构萃取,沉淀 Theme、Hydrogen、App template、CLI、Storefront API、UI Extensions 的工程组织和验收 SOP。
---

# GitHub P0 官方仓库工程结构 SOP

## 1. 取证边界

本篇来自 [`P0官方仓库结构快照_2026-06-28`](../_sources/github-shopify-repos/P0官方仓库结构快照_2026-06-28.md)。

方法:

- `git clone --depth 1 --filter=blob:none --no-checkout` 到 `tmp/github-p0-structure-20260628/`。
- `git ls-tree` 读取 tree。
- 少量 `git show HEAD:path` 读取配置文件和 `package.json`。

边界:

- 未执行第三方仓库代码。
- 未安装依赖。
- 未登录 GitHub。
- 未连接 Shopify 店铺。
- 未使用任何 token。

## 2. P0 仓库结构信号

| 仓库 | HEAD 前缀 | 结构信号 | 对 ABI 的含义 |
|---|---|---|---|
| `Shopify/hydrogen` | `b4df055281f6` | `packages/`, `templates/skeleton`, `cookbook/`, `e2e/`, `docs/`; package scripts 包含 `build`, `dev`, `ci:checks`, `build:templates` | Hydrogen 是框架 + 模板 + cookbook + E2E 的 monorepo,不能只看 starter;ABI 的 headless SOP 要同时覆盖模板、recipe、测试和部署 |
| `Shopify/dawn` | `83d5e6b4094d` | `assets/`, `sections/`, `snippets/`, `templates/`, `locales/`, `config/settings_schema.json`, `layout/theme.liquid` | Liquid Theme 的成熟结构参考,适合做 Online Store 2.0 主题基线 |
| `Shopify/skeleton-theme` | `a4f32d393b9e` | `sections/`, `templates/`, `blocks/`, `config/`, `layout/`, `locales/` | 最小主题骨架,适合 ABI 生成新主题时控制复杂度 |
| `Shopify/cli` | `53a96ee0f104` | `packages/app`, `packages/create-app`, `packages/theme`, `packages/ui-extensions-*`, `packages/e2e`; scripts 包含 build/deploy/test/changeset 类命令 | CLI 是 App/Theme/UI Extension 的开发入口,也是命令边界来源;执行前必须区分本地生成、测试店、远端写入 |
| `Shopify/shopify-app-template-react-router` | `2d32d3fcde35` | `app/`, `app/routes`, `app/shopify.server.ts`, `app/db.server.ts`, `prisma/schema.prisma`, `shopify.app.toml`, `Dockerfile`; scripts 包含 `dev`, `deploy`, `env`, `setup`, `lint` | 当前优先 App template;ABI App/MCP 自动化应从 route、server adapter、session storage、TOML 配置、人审写操作开始 |
| `Shopify/shopify-app-template-remix` | `e421374031a9` | 与 React Router 模板高度相似,含 `pnpm-workspace.yaml` | 作为 Remix 迁移与兼容参考,新项目优先核对 React Router 模板 |
| `Shopify/storefront-api-examples` | `0b3b8e9735ca` | 多框架示例: Angular、Ember、Node、React、Vanilla 等;含 e2e/test 目录 | 适合比较 Storefront API 客户端模式,但具体 API version 需再查官方 docs |
| `Shopify/ui-extensions` | `80040db41a35` | `packages/ui-extensions`, `packages/ui-extensions-tester`, `examples/testing/*`, 多个 `shopify.app.toml` 和 `shopify.extension.toml`; scripts 含 docs/build/deploy | UI Extension 必须按 surface、target、API version、测试 fixture 管理;不能只把它当普通前端组件 |
| `Shopify/dev-mcp-gemini-cli` | `02c1f74db1f8` | 极小扩展仓库: README、LICENSE、GitHub workflow | Dev MCP setup 类仓库更像安装/配置入口,不等于生产 Admin API 操作权限 |

## 3. 工程结构分型

### Theme 型

适用仓库: `Dawn`, `skeleton-theme`。

标准目录:

- `layout/theme.liquid`
- `sections/`
- `snippets/`
- `templates/`
- `blocks/`
- `assets/`
- `locales/`
- `config/settings_schema.json`

ABI 生成或审核 Theme 时,先验目录骨架,再验页面:

1. 首页、集合页、商品页、搜索页、购物车、政策页模板是否齐全。
2. section schema 是否能被 Theme Editor 配置。
3. 多语言 locale 是否覆盖目标市场。
4. 资产和 snippet 是否可复用,避免把业务逻辑塞进单一模板。

### Hydrogen 型

适用仓库: `Shopify/hydrogen`。

标准结构:

- `templates/skeleton`: 起点模板。
- `packages/hydrogen`, `packages/hydrogen-react`: 核心包。
- `packages/create-hydrogen`: 脚手架入口。
- `packages/mini-oxygen`, `packages/remix-oxygen`: 运行/部署相关。
- `cookbook/recipes`: B2B、bundles、markets、metaobjects、GTM、infinite scroll 等 recipe。
- `e2e/`: 端到端测试和 fixtures。

ABI 采用 Hydrogen 时,不要只生成页面。最小可验收单元应包括:

1. route map。
2. Storefront API 查询边界。
3. env/schema。
4. SEO metadata/sitemap/robots。
5. preview/staging 部署。
6. E2E smoke。
7. 回滚方案。

### App Template 型

适用仓库: `shopify-app-template-react-router`, `shopify-app-template-remix`。

标准结构:

- `app/routes`
- `app/shopify.server.ts`
- `app/db.server.ts`
- `prisma/schema.prisma`
- `shopify.app.toml`
- `Dockerfile`
- `package.json scripts`: `dev`, `config:link`, `generate`, `deploy`, `env`, `setup`, `lint`

ABI App 自动化的最小组织方式:

1. Route 层只做页面和 action 入口。
2. Shopify adapter 层集中处理 auth/session/API client。
3. Domain service 层实现商品、订单、客户、库存、metaobject 等业务逻辑。
4. Agent/MCP facade 只调用 service,不直接散落 GraphQL mutation。
5. 写操作统一接 `dry_run -> preview -> approval -> execute -> audit_log`。

### UI Extension 型

适用仓库: `Shopify/ui-extensions`。

标准结构:

- `packages/ui-extensions`
- `packages/ui-extensions-tester`
- `examples/testing/*/shopify.app.toml`
- `examples/testing/*/extensions/*/shopify.extension.toml`
- surface docs 和 versioned API branch。

ABI 做 Checkout/CRO 扩展时,每个 extension 必须记录:

- surface。
- target。
- API version。
- permissions/capabilities。
- config。
- fixture。
- test store。
- rollback。

## 4. 命令与验收分层

不要把所有 `package.json scripts` 都视为安全本地命令。建议分层:

| 证据层 | 典型命令 | 风险 |
|---|---|---|
| local read-only | `git ls-tree`, `git show`, `node --check`, markdown/RAG 构建 | 不触达第三方系统 |
| local build/test | `npm run build`, `npm run lint`, `vitest`, `playwright` | 可能安装依赖或执行 package scripts,需先审 |
| Shopify dev auth | `shopify app dev`, `shopify app env`, `shopify theme dev` | 可能要求登录/店铺选择 |
| test store write | `shopify app deploy`, extension deploy, Admin API mutation | 需要测试店、人审和回滚 |
| production write | 生产主题/app/extension 发布或 Admin mutation | 默认禁止,除非明确授权 |

## 5. 未来代码生成准则

- Theme 生成: 以 `skeleton-theme` 控制最小结构,以 `Dawn` 校验成熟 section/schema 组织。
- Headless 生成: 以 `Hydrogen templates/skeleton` 起步,再按 cookbook recipe 加功能,不要一次性塞入复杂 CMS/搜索/推荐。
- App 生成: 以 React Router app template 为默认,Remix template 作为迁移参考。
- Checkout/CRO 生成: 以 UI Extension 的 target/API version 为第一约束,再谈组件。
- Dev MCP 接入: 只用于开发态 docs/schema/指导;Admin API 写操作必须另走安全评审。

## 6. 关联节点

- [[02-建站与基础设施/GitHub_Hydrogen与Theme工程实践]]
- [[06-转化优化CRO/GitHub_Checkout与AppBridge工程实践]]
- [[10-自动化编排/GitHub_ShopifyApp与MCP工程实践]]
- [[91-合规与风控/GitHub开源仓库安全与授权边界]]
