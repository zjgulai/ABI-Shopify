---
title: Codex 交接执行手册 · ABI 智能化独立站
type: handoff
updated: 2026-06-27
summary: ABI 智能化独立站 Codex 执行手册:仓库结构、可移植构建脚本、T1–T7 状态、命令、验收与红线。
---

# 🤝 Codex 交接执行手册 · ABI 智能化独立站

> 当前事实层:整套知识库+产品已落地,CodeGraph 已初始化,腾讯云站点已上线到 `platform.shopify.lute-tlz-dddd.top`。T1/T2/T3/T4/T5 已有本地或生产证据;T4b 线上实际模型为 `BAAI/bge-small-zh-v1.5 + Chroma + Neo4j`,`bge-m3` 因轻量 CPU 资源限制未作为生产模型;T6 已补执行队列与离线入库工具但内容级扩充仍待用户提供字幕/清单;T7 已补测试店受控写 Runbook,真实读写必须测试店与人审授权。

## 0. 环境与一键重建
- 仓库根:`<repo>/kb`(本机为 `/Users/pray/project/shopify/kb`)。
- 依赖:`python3` + `numpy`(检索/数据)、`flask`(网站后端)、`matplotlib`(改图,可选)、`node`(JS 语法校验,可选)。
- **构建脚本在 `kb/_build/`(已路径可移植,KB 从脚本位置推导)**:
  - `build_rag.py` → 重建 `_rag/chunks.jsonl`
  - `build_site_data.py` → 重建 `site/kb_data.js`(已含各节点 `docs` 专题文档)
  - `diag_*.py` + `NotoSansSC-*.ttf` → 重渲染 `_diagrams/`
- **一键重建**:
  ```bash
  cd kb/_build && python build_rag.py
  cd ../_rag/kb_index && python cli.py build      # 重建检索索引
  cd ../../_build && python build_site_data.py    # 重建网站数据
  ```

## 1. 仓库结构(关键)
```
kb/
├─ 00–10 / 90–92 /…/README.md     14 节点(每节点含若干专题 .md)
├─ _rag/chunks.jsonl + kb_index/  检索:retriever.py / cli.py / mcp_server.py / index_store
├─ _kg/graph.json(+entities/relations/mermaid)   知识图谱
├─ _diagrams/                     5 张商业图(png/pdf)+ 商业图全集_5页.pdf
├─ site/                          index.html / kb_data.js / server.py / deploy/ / 部署SOP.md
├─ skills/ + marketplace/         Claude Code skills + 一键装插件
├─ tools/accio_to_shopify.py      选品→Shopify 数据桥
├─ _build/                        ★可移植构建脚本(本手册用)
└─ 迭代方案与PRD_TODO.md / 项目总览与收敛.md
```

## 2. 任务 T1–T7(执行 → 测试 → 验收)

### ✅ T1 商业图堆叠修复(P0)
- 状态:脚本坐标已采用修复版,当前生成 5 张 PNG/PDF 商业图与 `商业图全集_5页.pdf`。
- 本轮补充:图脚本中的 RAG 块数量改为从 `_rag/chunks.jsonl` 动态读取,避免统计漂移。
- 验收:重跑 `diag_*.py` 后检查 `_diagrams/*.png` 无明显重叠/出血。

### ✅ T2 网站迭代(P0)
状态:节点专题文档渲染、`openDoc`、P0/P1/P2 路线图、页脚 9 源 + ABI、页面手动录入 DeepSeek API Key 已落地。保留实现参考:
1. **前端渲染专题文档**(`site/index.html`,`showNode(i)` 函数内):
   ```js
   if(n.docs&&n.docs.length){h+=`<h3>本节点专题文档</h3><div class="chips">`+
     n.docs.map((dd,j)=>`<span class="chip" style="cursor:pointer" onclick="openDoc(${i},${j})">📄 ${esc(dd.title)}</span>`).join('')+`</div>`;}
   ```
   并在 `openMD` 函数旁新增:
   ```js
   function openDoc(i,j){document.getElementById('mbody').innerHTML=md(K.nodes[i].docs[j].md);document.getElementById('modal').style.display='block';window.scrollTo(0,0)}
   ```
2. **下一步 P0/P1/P2**:`_build/build_site_data.py` 的 `roadmap` / `nextplan` 已同步。
3. **页脚 9 源 + ABI**:`index.html` 已写入 9 信息源说明;`kb_data.js` 包含 `sources`。
4. 重建:`cd kb/_build && python build_site_data.py`。
- **测试**:`awk '/<script>$/{f=1;next}/<\/script>/{f=0}f' site/index.html|node --check -` JS 无误。
- **验收**:浏览器开 `site/index.html` → 点节点 02 能看到并打开「Shopify 代理式商务技术栈2026 / Hydrogen脚手架SOP」;下一步显示 P0/P1/P2;页脚显示 9 源 + ABI。

### ✅ T3 完整 PRD(P0)
- 文件:`kb/PRD_ABI智能化独立站.md`。
- 内容:背景、产品定位、用户角色、范围、总体架构、14 节点功能需求、非功能需求、里程碑、验收、风险。
- **验收**:14 节点 + 横切层全覆盖,每节点字段齐全;重建 RAG/site 后可检索到。

### ✅ T4 检索生产化(P1,已完成 T4b 线上启用)
- 已落地:`retriever.py` 支持 manifest 驱动的 `LSAEmbedder` / `STEmbedder` / `OpenAIEmbedder`,`numpy` / `Chroma` store,`JSON` / `Neo4j` graph backend;`mcp_server.py` 暴露 `kb_status` / `kb_search` / `kb_ask`。
- 新增:`eval_retrieval.py` 小型离线召回评测;`compare_retrieval.py` 做 LSA vs candidate A/B;`neo4j_export.py` 支持 dry-run、Cypher 导出与显式 `NEO4J_*` 写入。
- 部署新增:`site/deploy/docker-compose.vector.yml` 启用 vector extras + `shopifykb-neo4j`;`entrypoint.sh` 等待 Neo4j 并按需导入图谱;`requirements.vector.txt` 与默认运行依赖分离。
- 默认部署边界:不追加 `docker-compose.vector.yml` 时仍使用 `embedder=lsa, store=numpy, graph_backend=json`;线上生产已追加 vector override。
- 线上实际后端:`embedder=st`,`store=chroma`,`model=BAAI/bge-small-zh-v1.5`,`graph_backend=Neo4jGraphStore`,`vector_dim=512`,chunks 与当前 RAG manifest 一致。`bge-m3` 在轻量 CPU 前台构建超过 7 分钟导致站点不可用,未作为生产模型上线。
- 命令:
  ```bash
  cd kb/_rag/kb_index
  python cli.py build
  python cli.py doctor
  python eval_retrieval.py --min-pass-rate 0.6
  python compare_retrieval.py --candidate-embedder st --candidate-store chroma --candidate-model BAAI/bge-small-zh-v1.5
  python neo4j_export.py
  python neo4j_export.py --write-cypher /tmp/shopify_kb_graph.cypher
  ```
- 生产可选启用:
  ```bash
  cd kb/site/deploy
  docker compose -p shopify-kb -f docker-compose.yml -f docker-compose.behind-proxy.yml -f docker-compose.vector.yml up -d --build
  ```
- 已验收:默认 LSA 评测 `pass_rate=1.00(5/5)`;本地 compose config 已确认 vector args、Neo4j 服务和回环端口;本地当前图谱为 220 实体 / 639 关系(0 悬挂)。上一版线上 T4b 证据:`eval_retrieval.py` 为 `pass_rate=1.00(5/5), top1_rate=0.60, mrr=0.73`;A/B smoke 相比 LSA pass/top1 持平、MRR 略低;Neo4j 导入日志 213 实体 / 593 关系。新增 inbox SOP 上线后需重跑线上导入与 eval 复核。
- 线上公开检查:`/api/health` 返回 `client_key_supported=true`,`server_key_set=false`;页面仍为手动录入 DeepSeek API Key。

### ✅ T5 网站上线(P1)
- 已执行:腾讯云轻量服务器独立 Docker project `shopify-kb`;共享 nginx 反代 `platform.shopify.lute-tlz-dddd.top`;HTTPS 证书独立签发。
- 运行边界:服务器 `.env` 仅模型配置,不保存 `DEEPSEEK_API_KEY`;API Key 在网站页面手动录入。
- **验收**:`https://platform.shopify.lute-tlz-dddd.top/api/health` 返回 ok;无 key 调用 `/api/chat` 返回页面填 key 提示。真实 provider 问答需用户在页面输入 Key 后授权验证。

### ▶ T6 多源深挖(P1,持续/工具已落地)
- 已补:`kb/90-AI能力地图/T6多源深挖执行队列.md` 与 `kb/tools/t6_multisource_intake.py`。
- 视频字幕:按 `kb/90-AI能力地图/视频深度萃取_模板与说明.md` 的 8 段结构逐条萃取,写入对应节点/专题文档。
- 新增源(抖音/小红书等):先用离线工具把用户粘贴清单生成草稿;人审后写入 `_kg/graph.json`(Source+条目)→ 重建 RAG/site。
- 命令:
  ```bash
  python3 kb/tools/t6_multisource_intake.py /path/to/t6_sources.jsonl --out kb/drafts/t6_multisource --index
  ```
- 当前状态:已有 `视频深度萃取_精选.md` 三条内容级萃取,其中 Ac Hampton `vXmF10ZNmoo` 为 browser-harness 真实 Chrome 页面/章节/采样帧 v0.1;其余高价值视频完整逐字稿仍需稳定转写或用户提供字幕/清单。
- **验收**:高价值视频有内容级萃取(非仅标题);新源进图谱与检索。

### ▶ T7 接 AI-Toolkit / UCP(P2,Runbook 已落地/真实读写待授权)
- 已补:`kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md`。
- `/plugin marketplace add <repo>/kb/marketplace` → `/plugin install shopify-ai-kb@shopify-ai-kb-marketplace`。
- `claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest` → `shopify auth login`(**测试店**)。
- 跑「读店铺数据 → 受控写(人审)」;先写审批台账与回滚计划;UCP:Developer Dashboard 注册 agent profile。
- **验收**:测试店完成一次 AI 受控上架/改价(人审通过)。

## 3. 通用验收自检
```bash
python - <<'PY'
import json,glob,os
kb=os.path.dirname(os.path.abspath("."))  # 在 kb/ 下运行
print("chunks:",sum(1 for _ in open("_rag/chunks.jsonl",encoding="utf-8")))
G=json.load(open("_kg/graph.json",encoding="utf-8")); ids={e["id"] for e in G["entities"]}
print("KG dangling:",len([r for r in G["relations"] if r["source"] not in ids or r["target"] not in ids]))
PY
```
- 图无堆叠(肉眼核 `_diagrams/*.png`)· JS `node --check` · chunks 可解析 · 图谱 0 悬挂。

## 4. 红线(必须遵守)
- `execution`/真改店铺/支付/上线/数据采集 **一律人审 + 测试店先行**。
- 不绕过外站抓取限制(GitHub/YouTube/Reddit 等);YouTube 可用用户授权的真实 Chrome browser-harness 做只读页面/转写入口/采样帧复核,否则多源走「粘贴→归类」。
- **密钥只走环境变量,绝不入镜像/git/前端。**
- 收入类宣传仅作打法参考,合规/选型把关(节点 91)。
