---
title: T4b 生产检索启用 TODO
type: plan
updated: 2026-06-27
summary: 将 Shopify KB 从轻量 LSA/numpy/json 默认链路升级为可验收的 bge/Chroma/Neo4j 生产检索后端,并保留回滚路径。
---

# T4b 生产检索启用 TODO

## 目标

在不污染其他应用的前提下,为当前 `shopify-kb` 独立 Docker project 启用生产检索后端:
- 语义嵌入:`sentence-transformers` + BAAI bge 系列模型。
- 向量库:Chroma 文件级持久向量库。
- 图谱:独立 Neo4j 容器,仅在 `shopify-kb-net` 内部暴露。
- 评测:LSA baseline vs 生产候选后端 A/B smoke。

## TODO

- [x] 资源审计:确认服务器内存、磁盘、现有 Docker 服务与当前 release。
- [x] Dockerfile 增加 build args:`INSTALL_VECTOR_EXTRAS`,`KB_EMBEDDER`,`KB_VECTOR_STORE`,`KB_ST_MODEL`。
- [x] 新增 `requirements.vector.txt`,把 `sentence-transformers/chromadb/neo4j` 与默认部署依赖分离。
- [x] 新增 `entrypoint.sh`,在 Neo4j 模式下等待 bolt 端口并按需导入图谱。
- [x] 新增 `docker-compose.vector.yml`,启用 app vector build + `shopifykb-neo4j` 内网容器。
- [x] 新增 `compare_retrieval.py`,输出 baseline/candidate 的 `pass_rate/top1_rate/MRR`。
- [x] 本地默认链路回归:`python cli.py build` + `eval_retrieval.py`。
- [x] 本地 compose config 校验:vector args、Neo4j 服务、回环端口均存在。
- [ ] 服务器 shared `.env` 生成 `NEO4J_PASSWORD`,并设置 `SHOPIFY_KB_EMBEDDER/ST_MODEL/VECTOR_STORE`。
- [ ] 发布新 release 并用 `docker-compose.vector.yml` 重建。
- [ ] 容器内验收:`cli.py status/doctor`,`eval_retrieval.py`,`compare_retrieval.py`,Neo4j 关系查询。
- [ ] 公开站点验收:`/api/health`,页面手动 Key 仍可用,`kb_data.js` 包含最新 T4b 状态。

## 验收口径

- 默认轻量路径仍可运行:不带 vector override 时仍是 `LSA + numpy + JSON graph`。
- 生产候选路径可运行:带 vector override 时 manifest 显示 `embedder=st`,`store=chroma`,`graph_backend=Neo4jGraphStore`。
- Neo4j 不暴露主机端口,只挂 `shopify-kb-net`。
- A/B smoke 产出 baseline/candidate 指标;若候选没有明显优于 baseline,不得声称“质量已显著提升”,只能记录为“生产后端已启用且无关键召回退化”。
- 服务器不保存 DeepSeek API Key;页面手动录入 Key 的边界保持不变。
