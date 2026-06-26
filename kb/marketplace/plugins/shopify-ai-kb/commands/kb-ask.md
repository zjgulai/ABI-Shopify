---
description: 用本地知识库(RAG+知识图谱)回答 Shopify 经营问题并给来源
---
针对问题:**$ARGUMENTS**

请在知识库根目录执行检索(首次需先 `cd _rag/kb_index && python cli.py build`),把环境变量 `SHOPIFY_KB_DIR` 指向知识库根(默认即本仓库根):
```bash
python "${SHOPIFY_KB_DIR:-.}/_rag/kb_index/cli.py" ask "$ARGUMENTS"
```
依据返回片段(带「来源/节点」)作答,逐条标注来源文件;若信息不足,建议查看对应节点 README,不要臆造。
