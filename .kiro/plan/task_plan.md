---
title: Shopify KB 经营作战台 2.0 P1 执行计划
updated: 2026-06-30
status: active
---

# Shopify KB 网站增量设计执行计划

## 目标

在 PRD2.0 P0 已落地基础上,继续推进 P1:SOP 与内容补齐、增长归因字段、Agent 任务模板、Evidence 筛选和 P1 检索验收。

## 范围

- 新增 `04/08/09` 三篇最小专题 SOP,让节点从内容债进入可下钻覆盖。
- 改造 `kb/_build/build_site_data.py`,接入 P1 SOP、增长复盘指标、Agent 任务模板和新问答预设。
- 改造 `kb/site/index.html`,展示增长复盘指标、Agent 任务模板、Evidence 状态筛选和空内容债提示。
- 更新 `kb/site/README.md`,同步 P1 能力说明。
- 重建 `kb/site/kb_data.js` 与 RAG 索引。
- 本地静态页面和脚本验收。

## 非目标

- 不调用外部 provider。
- 不连接 Shopify 店铺。
- 不写测试店或生产店铺。
- 不修改 `inbox/`、`tmp/` 中的一次性输入和证据。

## 阶段

1. 内容层: 新增 AI 素材生产与授权、订单履约与库存同步、客户会员与 VOC 闭环三篇 SOP。已完成。
2. 数据层: P1 SOP 接入 `sopPlaybooks`,Growth 增加 metrics/cadence,Agent 增加 taskTemplate/handoff。已完成。
3. 页面层: Evidence 状态筛选、增长指标、Agent 模板和内容债空态。已完成。
4. 验收层: 构建、语法检查、检索评估、本地页面检查。已完成。

## 验收标准

- `python3 kb/_build/build_site_data.py` 可重建 `kb/site/kb_data.js`。
- `node --check kb/site/kb_data.js` 和 `node --check` 等价页面 JS 检查通过。
- 新模块可在本地静态预览渲染,浏览器控制台红项为 0。
- 页面能看到 12 个 SOP、Evidence 筛选器、增长复盘指标、Agent 任务模板和 P1 内容债空态。
- RAG 能召回 `AI 素材生产与授权 SOP`、`订单履约与库存同步 SOP`、`客户会员与 VOC 闭环 SOP`。
- 默认 RAG 构建和检索评估保持稳定。

## T7 前置批次

目标:在用户尚未提供 Shopify 测试店前,先把 T7 授权前置、官方口径、本地环境检查和人审文本补齐。

范围:
- 新增 `10-自动化编排/T7测试店授权前置包.md`。
- 新增 `tools/t7_test_store_preflight.py`,只做本地检查。
- 同步 Runbook、经营作战台数据、README、TODO 和交接手册。

非目标:
- 不登录 Shopify。
- 不创建店铺。
- 不读取或写入任何店铺。
- 不调用 provider。
- 不保存或输出任何密钥值。

验收:
- preflight 脚本可运行并清晰输出 `local_pass_auth_required` 或人工动作项。
- RAG/site 可重建。
- T7 前置关键词能被本地检索召回。

## T7 配置中心批次

目标:把 DeepSeek Key、Shopify 测试店域名、T7 preflight、授权文本和本地证据台账统一进网站配置页。

范围:
- 在 `kb/_build/build_site_data.py` 新增 `configurationCenter` 数据契约。
- 在 `kb/site/index.html` 新增 `#config` 配置与授权中心、导航入口、状态卡、命令/审批文本生成和浏览器本地证据台账。
- 更新站点 README、T7 前置包、Runbook 和 TODO。

非目标:
- 不实现 Shopify OAuth callback。
- 不保存 Shopify token/password/private key。
- 不从网站直接读写店铺。
- 不从线上服务器执行本机 preflight。
- 不把本地配置视为真实授权完成。

验收:
- 页面能保存测试店域名到当前浏览器并生成 preflight 命令。
- 页面能生成只读连接和低风险写入审批文本。
- 页面能维护本地 evidence log,且不上传服务器。
- RAG/site 可重建,默认检索评测保持 5/5。
- 桌面和移动端配置页无明显溢出。
