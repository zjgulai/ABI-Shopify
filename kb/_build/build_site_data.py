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
{"phase":"P0 · 已收口","when":"P0","items":["T1/T2/T3/T5 已形成本地或生产证据","页脚 9 源 + ABI,站点统计 366 chunks / 220 entities / 639 relations","代码与知识库已提交并可按 release 目录部署"]},
{"phase":"P1 · 继续深挖","when":"P1","items":["T6 视频字幕深度萃取:优先 Ac Hampton P0/P1 队列","抖音/小红书维持粘贴清单或字幕→离线草稿→人审入库","页面手动录入 DeepSeek API Key 后做真实 provider 问答验收"]},
{"phase":"P2 · 受控写闭环","when":"P2","items":["T7 接 AI-Toolkit/UCP 测试店真实读写","Shopify 测试店授权 + mutation 预览 + 人审批准","按《全自动运营蓝图》把节点 skill 化、编排化"]},
]
nextplan=[
{"t":"P0 · 发布收口","d":"本地 KB/RAG/KG/site 已重建;线上使用 BAAI/bge-small-zh-v1.5 + Chroma + Neo4j,服务器不保存 DeepSeek Key。"},
{"t":"P1 · 内容扩充","d":"继续 T6 视频字幕与抖音/小红书多源入库;只用可复核文本、字幕或用户粘贴材料。"},
{"t":"P2 · 自动化闭环","d":"T7 等测试店授权后接 AI-Toolkit/UCP,先只读,再经人审做低风险测试写入。"},
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
