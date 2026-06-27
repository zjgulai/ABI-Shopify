# kb_index — 生产检索包(RAG + 知识图谱)

把知识库接成"可问答的运营 Agent"。**开箱即用**:仅需 numpy,默认离线 LSA 嵌入 + JSON 图谱;生产环境可显式切到 bge-m3/OpenAI + Chroma + Neo4j。

## 快速开始(本地开源 · 数据不出门)
```bash
pip install -r requirements.txt
python cli.py build
python cli.py status
python cli.py doctor
python cli.py ask "怎么做广告投放"
python cli.py search "Accio Work" --source shopify官方 -k 5
python eval_retrieval.py --min-pass-rate 0.6
```

默认索引 manifest 写入 `index_store/manifest.json`:
- `embedder=lsa`
- `store=numpy`
- `graph_backend=json`

## 生产嵌入(可选)

### 本地 bge-m3 / sentence-transformers
```bash
pip install sentence-transformers
python cli.py build --embedder st --model BAAI/bge-m3 --store numpy
python eval_retrieval.py
```

说明:首次运行会下载模型,适合数据不出门的中文语义召回。若服务器内存/磁盘有限,先在本地构建评测,生产镜像继续用 LSA fallback。

### OpenAI embeddings
```bash
pip install openai
export OPENAI_API_KEY=...
python cli.py build --embedder openai --model text-embedding-3-large --store numpy
python eval_retrieval.py
```

说明:该路径会把切块文本发送到 OpenAI embedding API;只在已确认数据出境边界后使用。

## Chroma 向量库(可选)
```bash
pip install chromadb
python cli.py build --embedder st --model BAAI/bge-m3 --store chroma
python cli.py status
```

Chroma 会写入 `index_store/chroma/`,检索时仍按 `stage/source/tag` 做后过滤。默认 Docker 镜像不安装 Chroma,避免无需要时拉大运行环境。

## Neo4j 图谱(可选)
```bash
python neo4j_export.py                         # dry-run:只打印实体/关系数量
python neo4j_export.py --write-cypher /tmp/shopify_kb_graph.cypher

pip install neo4j
export NEO4J_URI=bolt://127.0.0.1:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=...
python neo4j_export.py --apply
KB_GRAPH_BACKEND=neo4j python cli.py ask "UCP 和 Catalog 的关系是什么"
```

未配置 `NEO4J_*` 时不会写入图库。

## 暴露为 MCP 服务(给 Claude Code 调用)
```bash
pip install mcp
python mcp_server.py
```

工具:
- `kb_status`:返回当前索引 manifest 与图谱后端。
- `kb_search`:语义检索,支持 `stage/source/tag`。
- `kb_ask`:语义召回 + 命中节点的 1 跳图谱关联。

## 设计
- 切块来自 `../chunks.jsonl`(当前 298 块,带元数据);图谱来自 `../../_kg/graph.json`。
- `ask` = 向量召回 → 取主导 `stage` → 1 跳图扩展(SUPPORTS 能力 / BELONGS_TO 项目 / NEXT 节点)→ 拼上下文。
- 当前已实现:LSA、sentence-transformers、OpenAI、numpy store、Chroma store、JSON graph、Neo4j graph 查询/导入辅助。
- 当前预留:Qdrant/pgvector。规模或强过滤要求上来后再接,不阻塞轻量生产化。
- 架构全图见 `../检索方案_RAG+KG.md`。
