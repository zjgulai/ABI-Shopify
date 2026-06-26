# -*- coding: utf-8 -*-
import json,os,re,glob
import os
KB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+os.sep
def parse(path):
    t=open(path,encoding="utf-8").read(); meta={}; body=t
    if t.startswith("---"):
        e=t.find("\n---",3); fm=t[3:e]; body=t[e+4:]
        for ln in fm.splitlines():
            m=re.match(r"\s*([A-Za-z_]+):\s*(.*)",ln)
            if m:
                k=m.group(1); v=re.sub(r"\s{2,}#.*$","",m.group(2)).strip()
                if v.startswith("[") and v.endswith("]"): v=[x.strip() for x in v[1:-1].split(",") if x.strip()]
                meta[k]=v
    body=re.sub(r"<!--.*?-->","",body,flags=re.S)
    return meta,body.strip()

# nodes
nodes=[]
for d in sorted(glob.glob(KB+"[0-9]*/")):
    p=os.path.join(d,"README.md")
    if not os.path.exists(p): continue
    meta,body=parse(p)
    code=os.path.basename(d.rstrip("/"))
    secs=re.split(r"\n(?=## )",body)
    goal=""; subs=[]
    for s in secs:
        if s.startswith("## 1."): goal=re.sub(r"## 1\..*?\n","",s,1).strip()[:200]
        if s.startswith("## 2."):
            subs=[l.strip("- ").strip() for l in s.splitlines() if l.strip().startswith("- ")]
    docs=[]
    for sub in sorted(glob.glob(os.path.join(d,"*.md"))):
        if os.path.basename(sub)=="README.md": continue
        sm,sb=parse(sub)
        docs.append({"title":sm.get("title",os.path.basename(sub)[:-3]),"md":sb})
    nodes.append({"code":code,"num":code[:2],"name":code[2:].lstrip("-"),
        "layer":meta.get("layer",""),"summary":meta.get("summary",""),
        "sources":meta.get("sources",[]) if isinstance(meta.get("sources"),list) else [],
        "goal":goal,"subtopics":subs[:8],"docs":docs,"md":body})

# tool selection table
toolsel={}
selpath=KB+"90-AI能力地图/AI工具选型_每节点.md"
if os.path.exists(selpath):
    _,b=parse(selpath)
    for ln in b.splitlines():
        m=re.match(r"\|\s*(\d{2})\s+([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|",ln)
        if m: toolsel[m.group(1)]={"native":m.group(3).strip(),"external":m.group(4).strip(),"accio":m.group(5).strip(),"tip":m.group(6).strip()}

# 10-step
steps=[["1","找产品","Helium 10 · Jungle Scout","01"],["2","看市场趋势","Google Trends · Perplexity","01"],
["3","分析竞品","ChatGPT · Claude","01"],["4","写 Listing","ChatGPT · DeepSeek","03"],
["5","多语翻译","DeepL · Gemini","03"],["6","做主图和 A+","Midjourney · Canva · PS","04"],
["7","剪广告影片","CapCut · Runway · Kling","04"],["8","做配音","ElevenLabs","04"],
["9","做音乐/氛围音","Suno","04"],["10","自动化营运","Shopify · Zapier · Make","10"]]

# capabilities from KG
G=json.load(open(KB+"_kg/graph.json",encoding="utf-8"))
lab={e["id"]:e["label"] for e in G["entities"]}
caps={}
for e in G["entities"]:
    if e["type"]=="ShopifyCapability":
        sup=[lab[r["target"]] for r in G["relations"] if r["type"]=="SUPPORTS" and r["source"]==e["id"]]
        caps[e["label"]]=sup
# roadmap
roadmap=[
{"phase":"P0 · 今天-明天","when":"P0","items":["T1 修复全部商业图堆叠并逐图核验","T2 网站迭代:专题文档渲染 + 下一步 P0/P1/P2 + 页脚 8 源","T3 输出完整 PRD 文档"]},
{"phase":"P1 · 1-2 周","when":"P1","items":["T4 检索生产化:bge-m3/OpenAI + Chroma/Qdrant + Neo4j + MCP","T5 网站上线腾讯云:页面手动录入 DeepSeek API Key 并验证 HTTPS 问答","T6 多源深挖:视频字幕萃取 + 抖音/小红书来源入图谱/RAG"]},
{"phase":"P2 · 1 月+","when":"P2","items":["T7 接 AI-Toolkit/UCP 测试店受控写","按《全自动运营蓝图》把节点 skill 化、编排化","保留人审闸、审计日志与回滚"]},
]
nextplan=[
{"t":"P0 · 收口可用","d":"T1 修图、T2 网站迭代、T3 完整 PRD;今天-明天完成可读可验收闭环。"},
{"t":"P1 · 生产化准备","d":"T4 检索升级、T5 腾讯云上线、T6 多源深挖;1-2 周推进。"},
{"t":"P2 · 自动化闭环","d":"T7 测试店接 AI-Toolkit/UCP 受控写,再按《全自动运营蓝图》编排化。"},
]
# chunks
chunks=[]
for ln in open(KB+"_rag/chunks.jsonl",encoding="utf-8"):
    o=json.loads(ln); chunks.append({"doc":o["doc_title"],"sec":o["section"],"stage":o.get("stage",""),
        "src":o.get("sources",[]),"file":o["source_file"],"text":o["text"]})

data={"nodes":nodes,"toolsel":toolsel,"steps":steps,"caps":caps,"roadmap":roadmap,"nextplan":nextplan,
      "chunks":chunks,"stats":{"nodes":len(nodes),"chunks":len(chunks),
      "entities":len(G["entities"]),"relations":len(G["relations"])}}
out=KB+"site/kb_data.js"
open(out,"w",encoding="utf-8").write("window.KB="+json.dumps(data,ensure_ascii=False)+";")
print("kb_data.js:",os.path.getsize(out)//1024,"KB | nodes",len(nodes),"chunks",len(chunks),"caps",len(caps),"toolsel",len(toolsel))
print("sample node:",nodes[2]["num"],nodes[2]["name"],"| subs:",len(nodes[2]["subtopics"]),"| toolsel02:",bool(toolsel.get("02")))
