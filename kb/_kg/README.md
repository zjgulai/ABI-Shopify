---
title: 知识图谱(_kg)说明
type: meta
updated: 2026-06-27
summary: Shopify AI 全链路经营知识图谱:实体+关系,可视化为 Mermaid,可导入图库做检索/推理。
---

# _kg — 知识图谱

把知识库结构化为**实体 + 关系**,与 [[_rag]] 的文本切块互补:RAG 管"语义召回",KG 管"结构推理/关联追溯"。

## 文件
- `entities.json` — 213 个实体。字段:`id, type, label, props`。
- `relations.json` — 593 条关系。字段:`source, type, target`。
- `graph.json` — 实体+关系合集(一次性加载)。
- `pipeline.mermaid` — 全流程 + 横切层 + 复购回流(可视化)。
- `capability_map.mermaid` — Shopify 原生能力 → 支撑的流程节点。

## 实体类型(9)
以 `entities.json` 为准;当前包含 Stage/Source/Capability/Tool/Concept/Team/Project/Repo/Skill/Video 等类型。

## 关系类型(14)
以 `relations.json` 为准;当前包含 ENRICHES、SUPPORTS、CROSSCUTS、USES_TOOL、APPLIES_TO、BELONGS_TO、OWNED_BY、NEXT、MAPS_TO_STAGE、FEEDS_BACK、INTEGRATES、ENABLED_BY、CO_BUILT_WITH、DISCOVERY_LAYER_OF 等关系。

## Schema(主要边)
- `Stage -NEXT-> Stage`(流程顺序);`Stage(横切) -CROSSCUTS-> Stage`;`Stage09 -FEEDS_BACK-> Stage01/05`(复购闭环)
- `ShopifyCapability -SUPPORTS-> Stage`;`Catalog -DISCOVERY_LAYER_OF-> UCP`;`UCP -CO_BUILT_WITH-> Google`
- `AIStep -MAPS_TO_STAGE-> Stage`;`AIStep -USES_TOOL-> Tool`(你的 10 步图)
- `Source -ENRICHES-> Stage`(三源溯源);`Concept -APPLIES_TO-> Stage`;`Concept -ENABLED_BY-> Capability`
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
