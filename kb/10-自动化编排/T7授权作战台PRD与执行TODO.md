---
title: T7 授权作战台 PRD 与执行 TODO
type: prd
layer: 流程阶段
stage: 10-自动化编排
tags: [t7, authorization-workbench, shopify-cli, test-store, approval, evidence-ledger]
sources: [执行说明, T7测试店授权前置包, AI-Toolkit_UCP测试店受控写验收Runbook]
status: local_ready_auth_required
summary: 将网站配置中心升级为 T7 授权作战台,统一承接测试店域名、本地 preflight、现场授权、只读复核、mutation preview、人审批准、执行记录和回滚证据。
---

# T7 授权作战台 PRD 与执行 TODO

## 1. 产品目标

把当前 `#config` 从“配置与授权中心”升级为 T7 授权作战台,让用户能在网站中完成真实 Shopify 测试店读写前的所有准备动作:

- 保存非敏感本地配置:测试店域名、审批人、低风险写入目标、计划变更。
- 生成本地命令:`t7_test_store_preflight.py`、`shopify auth login`、`shopify auth whoami`。
- 生成审批文本:只读连接审批、低风险写入审批。
- 维护本地证据台账:preflight、现场授权、只读连接、mutation preview、人审批准、执行结果、回滚记录。
- 展示授权阶段:未配置、前置就绪、待现场授权、只读复核、待人审写入、写后复查。

## 2. 不做什么

- 不在网页或服务器保存 Shopify token、password、private key。
- 不从线上服务器执行 `shopify auth login`。
- 不调用 Shopify Admin API。
- 不读取真实店铺数据。
- 不写入测试店或生产店。
- 不把本地 preflight 说成真实授权完成。

## 3. 页面信息架构

| 区块 | 功能 | 验收 |
|---|---|---|
| 状态卡 | 汇总 DeepSeek Key、测试店域名、preflight、读写授权 | 状态能随本地配置和证据台账变化 |
| 授权阶段 | 6 步阶段:本地配置、preflight、现场授权、只读、preview/人审、写后复查 | 每步有状态、证据和下一动作 |
| 本地配置 | 保存测试店域名、审批人、变更目标、变更说明和三条确认 | 只写入浏览器 localStorage |
| 命令与审批 | 输出 preflight、auth、whoami、审批文本和授权包 JSON | 可复制,不含密钥 |
| 前置清单 | 展示测试店、CLI、插件、Runbook、人审、回滚等检查项 | 勾选状态持久化在本浏览器 |
| 操作剧本 | 展示只读连接、mutation preview、受控写入、回滚复查 | 每个剧本写明输入、输出、边界 |
| 证据台账 | 分类记录 preflight/auth/read/preview/approval/execute/rollback | 支持本地追加、导出、清空 |

## 4. TODO

- [x] 扩展 `configurationCenter` 数据模型:状态阶梯、清单、操作剧本、证据动作。
- [x] 升级 `#config` 页面标题、说明和布局。
- [x] 增加授权阶段卡片。
- [x] 增加本地前置清单。
- [x] 增加操作剧本卡片。
- [x] 增强证据台账:动作类型、状态字段、导出 JSON。
- [x] 增强命令输出:授权包 JSON 和风险边界。
- [x] 重建 RAG 与站点数据。
- [x] 本地和线上 smoke 验收。

## 5. 验收口径

- `#config` 页面能看到“T7 授权作战台”。
- 保存测试店域名后,状态卡从待输入变为本地就绪。
- 勾选前置清单后,本地浏览器能保留勾选状态。
- 证据台账能记录 action/status/note,并拦截疑似密钥格式。
- 命令输出包含 preflight、`shopify auth login`、`shopify auth whoami` 和审批文本。
- 公网版本仍返回 `server_key_set=false`。
- 页面 smoke 不需要 DeepSeek Key,不触发 provider call,不触发 Shopify 登录或店铺读写。
