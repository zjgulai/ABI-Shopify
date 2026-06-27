---
title: AI 能力地图
stage: 90-AI能力地图
layer: 横切层
tags: [ai, 工具链, sidekick, magic, 能力地图]
sources: [周报, twitter, shopify官方, inbox]  # 三源已融合 + 2026官方账号深化 + inbox资料包
status: verified      # 三源萃取完成
updated: 2026-06-27
summary: 横切全流程的“AI工具与能力索引”:你的10步AI工具链在此落位。
---

# 🧠 AI 能力地图

> **节点定位**:横切全流程的“AI工具与能力索引”:你的10步AI工具链在此落位。

## 1. 本节点要解决什么
维护 AI 工具与能力的总索引,将“AI开店10步”工具链映射到 0-10 各节点,并跟踪 Shopify 原生 AI 能力(Sidekick/Magic 等)。

## 2. 核心子主题
- AI 开店 10 步工具链映射表
- Shopify 原生 AI(Sidekick / Magic / Flow AI 等)
- 各节点推荐工具与替代品
- 工具成本/能力/接口对比
- 可编排为自动化的能力清单
- T6 多源深挖执行队列(字幕/帖子/清单 → 草稿 → 人审入库)

## 3. 真实业务细节(来源:数字化中心周报)
<!-- enrich:周报 -->
**已用模型/工具(内部实测)**:图像生成 nano banana、扩图 seedream5.0、视频生成模型选型、销量预测模型;大模型横评 ChatGPT / Kimi / 通义千问 / DeepSeek / 腾讯元宝 / 自研「路小特」〔周报01·李礼、刘华丽·2026-03〕。

**平台与工程**:AI 应用开发平台、AI Code Review、AI Skills 部门提效、AI coding harness rules/skills、UI 设计规范智能体〔周报01·朱远鹏、周健、柯创城〕。

**营销 AI**:视频中心 1.0/2.0、TikTok 广告视频分析(G 3.5 flash)、AI 广告生图系统〔周报03·魏诺亚 / 周报02·周桥生〕。

> **对自动化的启示**:公司内部 AI 能力已覆盖「图像/视频/预测/Agent/Coding」,可与外部工具链(你的 10 步 AI 开店图)互补编排。本节点维护完整工具映射表(见 §5)。

## 4. 发力点(来源:Twitter 书签)
<!-- enrich:twitter -->
**模型选型(书签观点,供参考非定论)**:编程方向 Codex GPT-5.5 / Claude Opus 4.6 / Composer 2.5;写作方向 Gemini 3.1 Pro / DeepSeek V4〔Twitter @MaxForAI〕。
**团队扫盲**:AI 11 核心名词速览——模型参数/Token/上下文窗口/Prompt/幻觉/RAG/Embedding/Tool Calling/MCP/Agent/Computer Use〔Twitter @cheery9998〕,可直接作为本库「术语表」。
> **发力点**:维护「模型/工具选型表 + 术语表」,并与你的 10 步 AI 开店图合并为统一能力地图(见 §5)。

## 5. Shopify 官方能力 & AI 工具
<!-- enrich:shopify官方 -->
**Shopify 原生 AI 能力清单(2026)**:
- **Sidekick**(管理助手):Pulse 主动洞察、按需出图、自然语言建 Flow、App Extensions(Data/Action)、Saved Skills(25 条 `/` 触发、可分享)、多模态(语音/共享屏幕/Apple Watch);WAU 同比 4×〔Shopify 官方〕。
- **Shopify Magic**:免费内容生成(描述/邮件/标题)+ 销售下滑多步分析。
- **Shopify Flow**:无代码自动化(全付费计划)。
- **Storefront MCP / Dev MCP / Shopify Catalog**:代理式数据与开发接口。
- **AI Toolkit**(MIT 开源,Claude Code 插件)。
- **Campaign Autopilot**(AI 跨渠道投放)。
- **Store AI / Agentic Storefront、UCP**(与 Google 共建)。
- **Hydrogen 2026.4 + Oxygen**(原生 MCP)。
- **发布节奏**:每年两次 Editions(Winter '26 于 2025-12-10、Spring '26 于 2026-06-17,各 150+ 更新)〔Shopify 官方〕。
> 与你的 10 步 AI 开店图合并:内部模型见 §3,外部模型选型见 §4,平台原生能力见此 §5。


> **【2026 深化】** Spring '26 = **「The Everywhere Edition」**(150+ 更新);Shopify ML(@ShopifyEng):把 LLM 蒸馏成更小更快更准的模型、**Tangent**(自治 ML 流水线 Agent)、亿级商品聚类。详见 [代理式商务技术栈](../02-建站与基础设施/Shopify代理式商务技术栈2026.md)。

## 6. SOP 与自动化要点
维护动作:能力地图 + 模型选型表 + 术语表,随每次 Editions 更新一次;标注「可被编排为自动化」的能力。

## 7. 关联节点
- [[10-自动化编排]]
- [[01-选品与市场调研]]
- [[04-内容与素材生产]]

## 8. Inbox 独立站实操资料包补充(2026-06-27)
<!-- enrich:inbox -->
新增资料包已形成专题文档:[内部资料萃取 · 独立站实操资料包](内部资料萃取_独立站实操资料包.md)。它把 15 个本地文件归类到 00-10 与 90-92,其中重复 PPT 按唯一内容去重,`listing优化模板.xlsx` 按结构+样本级抽取处理。

`workflow01.png` 提供了 Codex AI Agent 亚马逊全链路自动化的角色模型:选品、Listing、广告初始化、广告诊断、店铺经营 Agent,并强调“AI 作业 + 人工决策”双向避险。这与本库 `10-自动化编排` 的人审闸模型一致。
