# -*- coding: utf-8 -*-
"""把知识库检索暴露为 MCP 服务,任何 Agent(如 Claude Code)都能调用。
运行:pip install mcp && python mcp_server.py  (先 python cli.py build 建好索引)
可选环境变量:KB_EMBEDDER,KB_VECTOR_STORE,KB_GRAPH_BACKEND。"""
from mcp.server.fastmcp import FastMCP
import retriever as R
mcp=FastMCP("shopify-kb"); _r=None
def r():
    global _r
    if _r is None: _r=R.Retriever()
    return _r
@mcp.tool()
def kb_status()->dict:
    """返回当前索引与图谱后端状态,用于 Agent 自检。"""
    return r().status()
@mcp.tool()
def kb_search(query:str,k:int=5,stage:str="",source:str="",tag:str="")->list:
    """语义检索 Shopify 经营知识库,返回带 stage/source/file 元数据的片段。"""
    return [{"score":round(s,3),"doc":d["doc_title"],"section":d["section"],"stage":d["stage"],
             "file":d["source_file"],"text":d["text"][:500]} for s,d in r().search(query,k,stage or None,source or None,tag or None)]
@mcp.tool()
def kb_ask(query:str,k:int=5)->dict:
    """混合检索:语义召回 + 命中节点的知识图谱关联(Shopify 能力 / 真实项目 / 下一节点)。"""
    hits,ge=r().ask(query,k)
    return {"hits":[{"score":round(s,3),"doc":d["doc_title"],"section":d["section"],"file":d["source_file"]} for s,d in hits],
            "graph":({"stage":ge[0],"capabilities":ge[1],"projects":ge[2],"next":ge[3]} if ge else {})}
if __name__=="__main__": mcp.run()
