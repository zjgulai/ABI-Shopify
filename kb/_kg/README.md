---
title: 知识图谱(_kg)说明
type: meta
updated: 2026-06-25
summary: Shopify AI 全链路经营知识图谱:实体+关系,可视化为 Mermaid,可导入图库做检索/推理。
---

# _kg — 知识图谱

把知识库结构化为**实体 + 关系**,与 [[_rag]] 的文本切块互补:RAG 管"语义召回",KG 管"结构推理/关联追溯"。

## 文件
- `entities.json` — 105 个实体。字段:`id, type, label, props`。
- `relations.json` — 219 条关系。字段:`source, type, target`。
- `graph.json` — 实体+关系合集(一次性加载)。
- `pipeline.mermaid` — 全流程 + 横切层 + 复购回流(可视化)。
- `capability_map.mermaid` — Shopify 原生能力 → 支撑的流程节点。

## 实体类型(9)
Tool×29, ShopifyCapability×15, Stage×14, Concept×12, Project×12, AIStep×10, Team×8, Source×4, Org×1

## 关系类型(14)
ENRICHES×47, SUPPORTS×37, CROSSCUTS×33, USES_TOOL×31, APPLIES_TO×19, BELONGS_TO×12, OWNED_BY×12, NEXT×10, MAPS_TO_STAGE×10, FEEDS_BACK×2, INTEGRATES×2, ENABLED_BY×2, CO_BUILT_WITH×1, DISCOVERY_LAYER_OF×1

## Schema(主要边)
- `Stage -NEXT-> Stage`(流程顺序);`Stage(横切) -CROSSCUTS-> Stage`;`Stage09 -FEEDS_BACK-> Stage01/05`(复购闭环)
- `ShopifyCapability -SUPPORTS-> Stage`;`Catalog -DISCOVERY_LAYER_OF-> UCP`;`UCP -CO_BUILT_WITH-> Google`
- `AIStep -MAPS_TO_STAGE-> Stage`;`AIStep -USES_TOOL-> Tool`(你的 10 步图)
- `Source -ENRICHES-> Stage`(三源溯源);`Concept -APPLIES_TO-> Stage`;`Concept -ENABLED_BY-> Capability`
- `Project -BELONGS_TO-> Stage`;`Project -OWNED_BY-> Team`(周报真实项目)

## 导入图库(可选)
JSON 可直接转 Neo4j:`entities.json` → 节点(以 `type` 为 label、`id` 唯一);`relations.json` → 边(`type` 为关系类型)。或用 networkx/pyvis 直接加载 `graph.json` 做查询与可视化。
