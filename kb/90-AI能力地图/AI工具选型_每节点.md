---
title: 每节点 AI 工具选型(自建 / 原生 / 外包)
stage: 90-AI能力地图
layer: 横切层
tags: [选型, 工具, accio-work, shopify原生, build-vs-buy]
sources: [shopify官方, web]
status: verified
updated: 2026-06-26
summary: 每个流程节点的 AI 工具选型建议,三层原则:Shopify 原生优先 → 专用外部工具补 → Agent 业务团队(Accio Work)外包,并标注各自适配度。
---

# 🧰 每节点 AI 工具选型(自建 / 原生 / 外包)

## 选型三层原则
1. **Shopify 原生优先**:能用 Sidekick / Magic / Flow / MCP / Functions / Autopilot 解决的,优先原生——数据不出站、与店铺强绑定、维护成本低。
2. **专用外部工具补位**:原生不擅长的(深度选品、广告视频、配音/配乐),用单点最强工具。
3. **Agent 业务团队外包**:把"选品/采购/合规/跨市场营销"这类重流程、重数据的环节,外包给 **Accio Work**(Alibaba 的 agentic business team)等,作为被你编排层调度的"外部 Agent 团队"。

> **关于 Accio Work 的定位(重要)**:它强在 **B2B 选品/采购(RFQ+谈判)、100+ 市场合规(VAT/关税)、全球营销与物流**,且背靠阿里巴巴贸易数据。但它**围绕 Alibaba.com 生态,不是 Shopify 建站工具**。所以——**建站/转化/店铺运营走 Shopify 原生;选品/采购/合规/跨市场营销可重度用 Accio Work**。两者互补,不是二选一。数据归属与生态锁定见 [[91-合规与风控]]。

## 选型表

| 节点 | 原生/自建首选 | 专用外部工具 | Accio Work 适配 | 一句话建议 |
|------|--------------|-------------|:---:|-----------|
| 00 战略定位 | Claude / ChatGPT 研判 | Perplexity | 🟡 市场分析 | 战略人定,AI 出草稿 |
| 01 选品调研 | Shopify Catalog + Claude 分析 | Helium 10 / Jungle Scout / Google Trends | ✅ 强(选品+采购谈判+贸易数据) | **选品可重度用 Accio Work** |
| 02 建站基建 | **Shopify AI Toolkit + Dev MCP + agent-first Hydrogen**(Claude Code/Codex 脚手架) | 主题 / Online Store 2.0 | ❌ 不适用(非 Shopify 建站) | **AI 建站走 Shopify 原生,不用 Accio** |
| 03 上架 Listing | Shopify Magic + Catalog | ChatGPT / DeepSeek / DeepL / Gemini | ✅ 上架/多语 | Magic 为主,Accio 批量补 |
| 04 内容素材 | Sidekick 出图 | Midjourney / Canva / CapCut / Kling / ElevenLabs / Suno | 🟡 部分 | 站内 Sidekick + 外部视频链 |
| 05 营销引流 | **Campaign Autopilot** + Sidekick 扩展(Klaviyo) | Meta / TikTok / Klaviyo | ✅ 全球营销自动化 | Autopilot 为主,Accio 做跨市场 |
| 06 转化 CRO | Shopify Functions + Sidekick Pulse | AB 测试工具 | ❌ 弱 | 走 Shopify 原生 |
| 07 数据归因 | GA4/GTM + Sidekick Pulse | BigQuery / Looker | 🟡 | 自建数据层为主 |
| 08 履约供应链 | Shopify Flow + 海外仓 | 菜鸟 / FBA / WFS | ✅ 强(采购/合规/物流 100+ 市场) | 采购+合规可用 Accio |
| 09 会员运营 | Store AI + Storefront MCP | Klaviyo / Loop | 🟡 | Shopify 原生为主 |
| 10 自动化编排 | **AI Toolkit + MCP + Flow + 自建 Agent 编排** | Zapier / Make | 🟡 可作子团队 | 你的编排层调度,**把 Accio 当作一个"外部 Agent 团队"被编排** |

图例:✅ 适配强 · 🟡 部分适配 · ❌ 不适配

## 你问的"AI 建站"该选谁?
- **结论**:AI 建站选 **Shopify 原生路径**——用 **Shopify AI Toolkit + Dev MCP**,让 **Claude Code / Codex / Cursor** 脚手架出店面;长期重定制再上 **agent-first Hydrogen**。
- **不要**用 Accio Work 做建站——它不做 Shopify 站点;它的价值在选品/采购/合规/全球营销。
- 二者协作姿势:**Accio Work 帮你"找货+谈价+合规+铺市场",Shopify 原生帮你"把店建起来+运营自动化"**,在 [[10-自动化编排]] 由你的编排层统一调度。

## 与 [[90-AI能力地图]] / [[10-自动化编排]] 的关系
本表是"选型"视角;能力清单见 [[90-AI能力地图]] README §5,编排蓝图见 [[10-自动化编排]] 的《全自动运营蓝图》。
