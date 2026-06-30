---
title: Shopify 配置中心版本腾讯云部署验收记录
type: deployment_evidence
date: 2026-06-30
target: platform.shopify.lute-tlz-dddd.top
release: 20260630T1148-8043768
boundary: production-readonly-smoke-no-provider-call-no-shopify-store-access
---

# Shopify 配置中心版本腾讯云部署验收记录

> 发布状态追加验收 release: `20260630T1148-8043768`。原 `20260630T0815-84bde79` 为配置中心首个线上验证版本,本文件保留历史记录并追加发布状态批次证据。当前生产 release 仍以 `/api/deploy-status` 为准。

## 1. 部署范围

- 目标服务器:`101.34.52.232 (VM-0-16-ubuntu)`。
- 目标域名:`https://platform.shopify.lute-tlz-dddd.top`。
- Release:`/opt/shopify-kb/releases/20260630T0815-84bde79`。
- `current` 指向:`/opt/shopify-kb/releases/20260630T0815-84bde79`。
- 本地提交:`84bde7989da0883d335cdc4e1575194466c21f05`。
- 远端分支 SHA:`cf23e76a0646ea6605153b51d9e43b2a2dfed48b`。

## 2. 隔离与边界

- 继续使用 compose project `shopify-kb`。
- 继续使用方案 B:app 只绑定 `127.0.0.1:8088`,由已有 `ai_video_nginx` 反代 80/443。
- 保留共享配置软链:`kb/site/deploy/.env -> /opt/shopify-kb/shared/.env`。
- 未向服务器写入 DeepSeek API Key。
- 未登录 Shopify,未读取店铺,未写店铺,未保存 Shopify token/password/private key。

## 3. 本地发布前检查

- `build_site_data.py`:site data `987KB`,nodes=14,chunks=640。
- `build_rag.py`:chunks=640,docs=119。
- `cli.py build`:indexed chunks=640,embedder=lsa,store=numpy。
- `eval_retrieval.py --min-pass-rate 1.0`:5/5,pass_rate=1.00,top1=0.60,MRR=0.68。
- `t7_test_store_preflight.py --store-domain abi-t7-smoke-20260630.myshopify.com`:status=`local_pass_auth_required`。
- 密钥样式扫描:仅命中文档占位示例,无真实密钥值。

## 4. 线上部署结果

- `shopifykb-app`:healthy,`127.0.0.1:8088->8000/tcp`。
- `shopifykb-neo4j`:healthy。
- `/api/health`:
  - ok=true
  - retriever=true
  - server_key_set=false
  - client_key_supported=true
  - model=`deepseek-v4-flash`
- app 日志:
  - `indexed chunks: 640 | embedder=st | store=chroma | model=BAAI/bge-small-zh-v1.5`
  - `entities=260 relations=785`
  - `neo4j_import=done`
- `docker exec ai_video_nginx nginx -t`:successful。

## 5. 线上页面验收

- HTTPS `/`:HTTP 200。
- HTTPS `/api/health`:HTTP 200。
- `kb_data.js`:stats nodes=14,chunks=640,entities=260,relations=785。
- `configurationCenter.storageKey`: `abi.shopify.config.v1`。
- Playwright 桌面 smoke:
  - `#config` 存在。
  - nav 中存在 `配置`。
  - `#configSummary` 有 4 个状态卡。
  - 输出区包含 `shopify auth login` 和 preflight 命令。
  - 页面含“不保存 Shopify token”边界文案。
- Playwright 表单 smoke:
  - 测试店域名仅写入浏览器 localStorage。
  - 能生成只读审批文本。
  - 能写入本地 evidence log。
  - Shopify token 样式文本被拦截,不会进入 evidence log。
- Playwright 移动端 smoke:
  - 390px 视口无横向溢出。
  - 移动菜单可见。
  - 配置中心 4 个状态卡可渲染。
- 控制台:0 error / 0 warning;仅 Chromium 对 DeepSeek Key 密码框的 verbose 提示。

## 6. 未完成边界

- T5 真实 provider 问答仍需用户在页面手动录入 DeepSeek API Key 后执行。
- T7 真实读店铺/写测试商品仍需用户创建或提供 Shopify development store,并现场执行 `shopify auth login` 与逐次人审授权。

## 7. 发布状态批次追加验收

- Release:`/opt/shopify-kb/releases/20260630T1148-8043768`。
- `current` 指向:`/opt/shopify-kb/releases/20260630T1148-8043768`。
- 本地提交与远端分支 SHA:`8043768f39c7924a56317d62eb9b6ed0ead4c3a5`。
- 部署时间:`2026-06-30T11:53:52+08:00`。
- `index.html` sha256:`7bde6d9e36b457f1e601810bfa93da862b74cd19a15cf8284c75b1999b9030b6`。
- `kb_data.js` sha256:`36d4a1c743e86996c8d5ea51fdfcca402dd0ae3a7bc5d8ba6cd7041241716e32`。
- `chunks.jsonl` sha256:`b9ad51af710df5aa99055e90093d246859b1eedeafdfc97595fa2d8fda5f15a8`。
- `/api/deploy-status`:
  - ok=true
  - status_file=true
  - release=`20260630T1148-8043768`
  - runtime.retriever=true
  - runtime.retriever_status.manifest.model=`BAAI/bge-small-zh-v1.5`
  - runtime.retriever_status.manifest.store=`chroma`
  - runtime.retriever_status.graph_backend=`Neo4jGraphStore`
  - runtime.retriever_status.chunks_loaded=647
  - server_key_set=false
- Playwright 线上 smoke:
  - `#config` 页面“线上发布状态”有 5 张卡。
  - 页面显示 release `20260630T1148-8043768`、commit 前缀、`647 chunks`、`BAAI/bge-small-zh-v1.5` 和 `server_key_set=false`。
  - 390px 移动视口无横向溢出。

边界不变:本批只做生产只读发布状态验收,未调用 provider,未登录 Shopify,未读取店铺,未写店铺,未输出密钥值。
