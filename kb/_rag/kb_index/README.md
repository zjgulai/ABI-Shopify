# kb_index — 生产检索包(RAG + 知识图谱)

把知识库接成"可问答的运营 Agent"。**开箱即用**:仅需 numpy,默认离线 LSA 嵌入。

## 快速开始(本地开源 · 数据不出门)
```bash
pip install -r requirements.txt          # 仅 numpy 即可跑
python cli.py build                       # 读 ../chunks.jsonl 建持久索引到 index_store/
python cli.py ask "怎么做广告投放"          # 语义召回 + 图谱关联
python cli.py search "Accio Work" --source shopify官方 -k 5
```

## 暴露为 MCP 服务(给 Claude Code 调用)
```bash
pip install mcp && python mcp_server.py    # 提供 kb_search / kb_ask 两个工具
```

## 升级到"真·生产"(三处替换,接口不变)
1. **嵌入**:把 `retriever.LSAEmbedder` 换成 bge-m3 / Qwen3-Embedding(`sentence-transformers`)或 `OpenAIEmbedder`。中文优先 bge-m3。
2. **向量库**:把 `index_store`(numpy)换成 **Chroma**(文件级、最省事)或 **Qdrant/pgvector**(规模+强过滤),保留 `stage/tags/sources` 作为 payload 过滤。
3. **图谱**:把 `graph_expand` 的 JSON 遍历换成 **Neo4j**(`_kg/*.json` 可直接导入),支持多跳推理。

## 设计
- 切块来自 `../chunks.jsonl`(159 块,带元数据);图谱来自 `../../_kg/graph.json`。
- `ask` = 向量召回 → 取主导 `stage` → 1 跳图扩展(SUPPORTS 能力 / BELONGS_TO 项目 / NEXT 节点)→ 拼上下文。
- 架构全图见 `../检索方案_RAG+KG.md`。
