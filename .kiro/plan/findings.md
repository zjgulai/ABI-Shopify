---
title: Shopify KB 网站增量设计发现记录
updated: 2026-06-28
---

# 发现记录

## 当前站点结构

- `kb/site/index.html` 已有总架构、全景图、AI 开店 10 步、全流程节点、AI 能力地图、知识库检索、DeepSeek RAG 问答、路线图。
- `kb/_build/build_site_data.py` 当前只输出 `nodes/toolsel/steps/caps/roadmap/nextplan/chunks/stats`。
- 页面上的新增来源主要藏在节点 modal 和搜索结果里,尚未形成独立决策界面。

## 高价值内容

- GitHub P0 官方仓库结构可转成工程仓库地图: Theme、Hydrogen、App Template、UI Extension、MCP/CLI。
- platform-operations-wiki 可转成增长作战室: SEO、Meta、Reddit GEO、YouTube/PR、KOL、Affiliate、Deal。
- AI 工作流可转成 Agent 工作流库: 市场洞察、素材、红人联盟、SEO/GEO、广告诊断、经营复盘。
- 风控资料可转成红线闸: Admin API、店铺写入、Checkout、社区发帖、UGC 授权、广告预算、折扣佣金。

## 当前约束

- 本轮只做本地页面与数据生成,不做外部 provider 调用。
- `inbox/`、`tmp/` 是本地输入/一次性证据目录,保持未跟踪。
