---
title: GitHub Shopify Repos 来源包
type: source_index
updated: 2026-06-28
verification_status: local_readonly_snapshot
---

# GitHub Shopify Repos 来源包

- captured_at: `2026-06-28T08:57:42+0800`
- method: GitHub 搜索页方向 + GitHub API 初筛 + `git ls-remote` HEAD + raw README/License 只读抓取;P0 官方仓库追加 `git clone --depth 1 --filter=blob:none --no-checkout` + `git ls-tree` 结构快照。
- scope: Shopify 官方与强相关社区 Storefront、Theme、App、API、Checkout、MCP/Agent 仓库。
- non-goals: 不执行第三方代码、不安装依赖、不调用 provider、不写 Shopify 店铺、不使用 GitHub token。P0 结构快照只做 blobless/no-checkout 浅层 tree 读取。

## 文件

- `manifest_2026-06-28.json`: 结构化候选元数据。
- `候选仓库矩阵_2026-06-28.md`: 人读矩阵。
- `repos/*/source_summary.md`: 单仓库只读摘要、HEAD 前缀、README/License sha256 前缀。
- `p0_structure_manifest_2026-06-28.json`: P0 官方仓库 git tree 结构化快照。
- `P0官方仓库结构快照_2026-06-28.md`: P0 官方仓库结构级人读摘要。

## 验证状态

本来源包只能证明本地只读快照与 GitHub 可访问内容,不能证明官方推荐、最新产品策略或代码安全。社区 MCP/Admin API 工具默认进入 `needs_security_review`。
