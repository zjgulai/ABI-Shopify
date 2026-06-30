---
title: Shopify KB 一键发布自动化计划与验收
type: deployment_plan
date: 2026-06-30
target: platform.shopify.lute-tlz-dddd.top
status: implemented
boundary: no-provider-call-no-shopify-store-access-no-secret-output
---

# Shopify KB 一键发布自动化计划与验收

## 1. 目标

将手动发布流程固化为 `scripts/deploy_shopify_kb.sh`,让一次发布同时覆盖:

- 本地 RAG / site data 重建。
- 本地检索评测与 JS 语法检查。
- tracked 工作区洁净检查。
- 新 release 目录上传与 manifest 写入。
- `shopify-kb` 独立 compose project 重建。
- 容器 health 轮询。
- 服务器文件哈希、公网静态哈希和 `/api/health` 验收。
- 可用时执行 Playwright 配置中心 smoke。

## 2. 第一性原理边界

线上是否为最新产品形态,不能只看页面能否打开。必须同时满足:

| 层级 | 验收 |
|---|---|
| Source | Git HEAD 与远端分支一致 |
| Generated data | `kb/site/kb_data.js` 与 `kb/_rag/chunks.jsonl` 已由当前 source 重建并提交 |
| Release | `/opt/shopify-kb/current` 指向当前 release |
| Runtime | `shopifykb-app` healthy,检索后端已加载 |
| Public | 公网 `/api/health` 与静态文件哈希匹配 |
| Browser | `#config` 配置中心桌面/移动端 smoke 通过 |

## 3. TODO

- [x] 保留当前生产拓扑:方案 B behind-proxy + vector。
- [x] 新增 `scripts/deploy_shopify_kb.sh`。
- [x] 默认不复制 `.env`、不复制根目录 SSH key、服务器仍软链 `/opt/shopify-kb/shared/.env`。
- [x] 默认要求 tracked 工作区洁净,避免 manifest 指向无法复现的工作区状态。
- [x] 默认重建 `build_rag.py`、`build_site_data.py`、`cli.py build` 和 `eval_retrieval.py --min-pass-rate 1.0`。
- [x] 上传后写 `DEPLOY_MANIFEST.txt`,记录 release、commit、远端分支 SHA、三个关键 sha256。
- [x] 健康检查到 `shopifykb-app=healthy` 后再跑公网验收。
- [x] 可用时运行 Playwright 配置中心 smoke。

## 4. 使用方式

预演:

```bash
scripts/deploy_shopify_kb.sh --dry-run
```

正式发布:

```bash
scripts/deploy_shopify_kb.sh
```

仅验证脚本参数和远端流程时可临时跳过本地重建或浏览器 smoke:

```bash
scripts/deploy_shopify_kb.sh --dry-run --skip-rebuild --skip-git-clean-check --skip-playwright
```

## 5. 红线

- 不在服务器 `.env` 写 DeepSeek API Key。
- 不登录 Shopify。
- 不读取店铺。
- 不写店铺。
- 不输出密钥值。
- 不触碰其他 compose project、容器、Nginx 配置或系统服务。

## 6. 验收记录模板

每次发布后至少记录:

- release 名。
- Git commit 和远端分支 SHA。
- `index.html` / `kb_data.js` / `chunks.jsonl` sha256。
- `/api/health` 关键字段。
- `shopifykb-app` / `shopifykb-neo4j` health。
- Playwright smoke 结论。
