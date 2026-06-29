---
title: 知识图谱(_kg)说明
type: meta
updated: 2026-06-29
summary: Shopify AI 全链路经营知识图谱:实体+关系,可视化为 Mermaid,可导入图库做检索/推理。
---

# _kg — 知识图谱

把知识库结构化为**实体 + 关系**,与 [[_rag]] 的文本切块互补:RAG 管"语义召回",KG 管"结构推理/关联追溯"。

## 文件
- `entities.json` — 260 个实体。字段:`id, type, label, props`。
- `relations.json` — 785 条关系。字段:`source, type, target`。
- `graph.json` — 实体+关系合集(一次性加载)。
- `pipeline.mermaid` — 全流程 + 横切层 + 复购回流(可视化)。
- `capability_map.mermaid` — Shopify 原生能力 → 支撑的流程节点。

## 实体类型(12)
以 `entities.json` 为准;当前包含 AIStep / Concept / Org / Project / Repo / ShopifyCapability / Skill / Source / Stage / Team / Tool / Video。

## 关系类型(19)
以 `relations.json` 为准;当前包含 APPLIES_TO、BELONGS_TO、CO_BUILT_WITH、CROSSCUTS、DISCOVERY_LAYER_OF、ENABLES、ENABLED_BY、ENRICHES、FEEDS_BACK、INCLUDES、INTEGRATES、MAPS_TO_STAGE、NEXT、OWNED_BY、PART_OF、SERVES、SUPPORTS、TEACHES、USES_TOOL。

## Schema(主要边)
- `Stage -NEXT-> Stage`(流程顺序);`Stage(横切) -CROSSCUTS-> Stage`;`Stage09 -FEEDS_BACK-> Stage01/05`(复购闭环)
- `ShopifyCapability -SUPPORTS-> Stage`;`Catalog -DISCOVERY_LAYER_OF-> UCP`;`UCP -CO_BUILT_WITH-> Google`
- `AIStep -MAPS_TO_STAGE-> Stage`;`AIStep -USES_TOOL-> Tool`(你的 10 步图)
- `Source -ENRICHES-> Stage`(多源溯源,含 platform-operations-wiki);`Concept -APPLIES_TO-> Stage`;`Concept -ENABLED_BY-> Capability`
- `Project -BELONGS_TO-> Stage`;`Project -OWNED_BY-> Team`(周报真实项目)

## 导入图库(可选)
JSON 可通过 `../_rag/kb_index/neo4j_export.py` 转 Neo4j:
```bash
cd ../_rag/kb_index
python neo4j_export.py                         # dry-run
python neo4j_export.py --write-cypher /tmp/shopify_kb_graph.cypher
# 配置 NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD 后才可写入:
python neo4j_export.py --apply
```
也可用 networkx/pyvis 直接加载 `graph.json` 做查询与可视化。
