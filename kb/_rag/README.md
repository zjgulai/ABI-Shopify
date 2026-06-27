---
title: RAG 切块层说明
type: meta
updated: 2026-06-25
summary: 知识库的 RAG 就绪切块。chunks.jsonl 每行一个块,含 stage/tags/sources/summary 元数据,可直接做向量化与按节点路由。
---

# _rag — RAG 切块层

- **chunks.jsonl**:298 个块,来自 61 个文档;每行一个 JSON。
- 切块粒度:按 Markdown 的 `## 一级小节`,每块尽量自洽。
- 字段:`id, doc_title, section, stage, layer, tags[], sources[], summary, source_file, text, char_len`。
- 用法:对 `text` 做 embedding;用 `stage/tags/sources` 做过滤与按节点路由;`summary` 可作卡片/重排序信号。
- 平均块长 ≈ 369 字符(min 18 / max 8538)。

> 重建命令:见 `_build/build_rag.py`(本仓库脚本,解析 frontmatter + 按小节切块)。
