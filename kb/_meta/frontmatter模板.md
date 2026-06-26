---
title: Frontmatter 元数据规范
type: meta
updated: 2026-06-25
summary: 每篇文档统一的 YAML frontmatter 字段定义,供人读与 AI 检索/路由共用。
---

# Frontmatter 元数据规范(人 + AI 双用)

每篇 `.md` 顶部统一带如下 YAML:

```yaml
---
title: 文档标题
stage: 02-建站与基础设施      # 所属节点编号-名
layer: 流程阶段 | 横切层
tags: [shopify, 支付, 站群]   # 工具/团队/主题标签
sources: [周报, shopify官方]  # 已融合的信息源
status: scaffold | enriched | verified
updated: YYYY-MM-DD
summary: 一句话摘要(<=60字,用于向量检索与卡片展示)
---
```

## 字段说明
- **stage / layer**:供 Agent 按流程节点路由。
- **tags**:横切检索(按工具或团队聚合)。
- **sources**:标识该篇融合了哪些源,便于审计与补全。
- **status**:`scaffold` 仅骨架;`enriched` 已注入三源;`verified` 已自检。
- **summary**:作为 embedding 友好的摘要句。

## 来源标注行(正文内)
萃取的事实尽量在句末加来源,格式:
`〔来源:周报01 · 梁庆玲/站点产品组 · 2026-03〕` 或 `〔来源:Shopify 官方文档〕` / `〔来源:Twitter @handle〕`。
