---
title: Codex 交接执行手册 · ABI 智能化独立站
type: handoff
updated: 2026-06-26
summary: 把未完成任务 T2–T7 交给 Codex 执行的精确手册:仓库结构、可移植构建脚本、每任务的文件级改动/命令/验收、通用重建与红线。
---

# 🤝 Codex 交接执行手册 · ABI 智能化独立站

> 由助手交接。已完成:整套知识库+产品(60+ 文档、RAG 281 块、知识图谱 213 实体/593 关系、5 张商业图、网站+DeepSeek 后端、腾讯云部署包、Claude Code 插件、Accio 数据桥)、T1 图堆叠修复。**以下 T2–T7 待 Codex 执行。**

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

## 2. 任务 T2–T7(执行 → 测试 → 验收)

### ▶ T2 网站迭代(P0)
**数据侧已就绪**:`build_site_data.py` 已为每节点生成 `docs:[{title,md}]`;`kb_data.js` 已含。仍需:
1. **前端渲染专题文档**(`site/index.html`,`showNode(i)` 函数内,在"查看完整文档"按钮前插入):
   ```js
   if(n.docs&&n.docs.length){h+=`<h3>本节点专题文档</h3><div class="chips">`+
     n.docs.map((dd,j)=>`<span class="chip" style="cursor:pointer" onclick="openDoc(${i},${j})">📄 ${esc(dd.title)}</span>`).join('')+`</div>`;}
   ```
   并在 `openMD` 函数旁新增:
   ```js
   function openDoc(i,j){document.getElementById('mbody').innerHTML=md(K.nodes[i].docs[j].md);document.getElementById('modal').style.display='block';window.scrollTo(0,0)}
   ```
2. **下一步换 P0/P1/P2**(`_build/build_site_data.py` 的 `roadmap=[...]` 改为《迭代方案与PRD_TODO.md》§D 的 P0/P1/P2;`nextplan` 同步)。
3. **页脚 8 源 + ABI**(`index.html` `<footer>` 文案;可用 `K.sources` 渲染,需在 build_site_data 的 `data` 加 `"sources":[…8源…]`)。
4. 重建:`cd kb/_build && python build_site_data.py`。
- **测试**:`awk '/<script>$/{f=1;next}/<\/script>/{f=0}f' site/index.html|node --check -` JS 无误。
- **验收**:浏览器开 `site/index.html` → 点节点 02 能看到并打开「Shopify 代理式商务技术栈2026 / Hydrogen脚手架SOP」;下一步显示 P0/P1/P2;页脚显示 8 源 + ABI。

### ▶ T3 完整 PRD(P0)
- 基于 `迭代方案与PRD_TODO.md` §C「每节点主-副工具×实现方法」核心表,扩写为 `kb/PRD_ABI智能化独立站.md`。
- 结构:1 背景 2 产品定位与商业价值 3 用户角色 4 范围(In/Out)5 总体架构(引用 `_diagrams/00_ABI总架构`)6 **各节点功能需求**(每节点:主工具/副工具/实现方法/输入/输出/人审闸/验收标准/依赖)7 非功能需求(性能/安全/合规/可维护/数据隐私)8 里程碑 9 验收 10 风险。
- **验收**:14 节点 + 横切层全覆盖,每节点字段齐全;重建 RAG/site 后可检索到。

### ▶ T4 检索生产化(P1)
- `kb/_rag/kb_index/retriever.py`:新增 `STEmbedder`(`sentence-transformers`,模型 `BAAI/bge-m3`)与 `OpenAIEmbedder`,把 `build_index`/`Retriever` 默认嵌入由 `LSAEmbedder` 切换(保留接口)。`index_store` 可换 **Chroma**(`chromadb`,文件级)。`_kg/*.json` 可导入 **Neo4j**。
- 命令:`pip install sentence-transformers chromadb` → `python cli.py build` → `pip install mcp && python mcp_server.py`。
- **验收**:同义/中文 query 召回质量明显优于 LSA;`kb_search/kb_ask` MCP 可被 Claude Code 调用。

### ▶ T5 网站上线(P1,需账号操作)
- 按 `kb/site/部署SOP.md`:DNS A 记录 → 腾讯云防火墙 80/443 → `cd site/deploy && cp .env.example .env`(仅模型配置,不填 Key,`chmod 600`)→ `docker compose -p shopify-kb up -d --build` → 在网站页面手动录入 DeepSeek API Key。
- **验收**:`https://platform.shopify.lute-tlz-dddd.top/api/health` 返回 ok;页面手动录入 API Key 后问答可用。**Key 不入镜像/git/服务器 env。**

### ▶ T6 多源深挖(P1,持续)
- 视频字幕:按 `kb/90-AI能力地图/视频深度萃取_模板与说明.md` 的 8 段结构逐条萃取,写入对应节点/专题文档。
- 新增源(抖音/小红书等):仿 `_build` 思路写入 `_kg/graph.json`(Source+条目)→ 重建 RAG/site。
- **验收**:高价值视频有内容级萃取(非仅标题);新源进图谱与检索。

### ▶ T7 接 AI-Toolkit / UCP(P2,需测试店)
- `/plugin marketplace add <repo>/kb/marketplace` → `/plugin install shopify-ai-kb@shopify-ai-kb-marketplace`。
- `claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest` → `shopify auth login`(**测试店**)。
- 跑「读店铺数据 → 受控写(人审)」;UCP:Developer Dashboard 注册 agent profile。
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
- 不绕过外站抓取限制(GitHub/YouTube/Reddit 等);多源走「粘贴→归类」。
- **密钥只走环境变量,绝不入镜像/git/前端。**
- 收入类宣传仅作打法参考,合规/选型把关(节点 91)。
