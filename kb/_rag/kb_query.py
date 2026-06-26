#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线 RAG + 知识图谱 检索原型(零外部依赖)。
用法:
  python kb_query.py search "如何用AI自动建站" [--stage 02] [--source shopify官方] [-k 5]
  python kb_query.py graph stage_02            # 看某实体的关联(能力/相邻节点/项目)
  python kb_query.py ask "怎么做转化优化"        # 混合:语义召回 + 图谱关联
"""
import json,os,re,math,sys,argparse
BASE=os.path.dirname(os.path.abspath(__file__)); KB=os.path.dirname(BASE)
def load_chunks():
    return [json.loads(l) for l in open(os.path.join(BASE,"chunks.jsonl"),encoding="utf-8")]
def load_graph():
    return json.load(open(os.path.join(KB,"_kg","graph.json"),encoding="utf-8"))
def toks(s):
    s=(s or "").lower(); out=re.findall(r"[a-z0-9]+",s)
    han=re.findall(r"[一-鿿]",s)
    out+=han+[han[i]+han[i+1] for i in range(len(han)-1)]
    return out
class TFIDF:
    def __init__(self,docs):
        self.docs=docs; self.tv=[]; df={}
        for d in docs:
            c={}
            for t in toks(d["text"]+" "+d.get("doc_title","")+" "+d.get("summary","")): c[t]=c.get(t,0)+1
            self.tv.append(c)
            for t in c: df[t]=df.get(t,0)+1
        N=len(docs); self.idf={t:math.log(1+N/v) for t,v in df.items()}
        self.norm=[math.sqrt(sum((c.get(t,0)*self.idf.get(t,0))**2 for t in c)) or 1 for c in self.tv]
    def search(self,q,k=5,stage=None,source=None,tag=None):
        qc={}
        for t in toks(q): qc[t]=qc.get(t,0)+1
        qw={t:qc[t]*self.idf.get(t,0) for t in qc}; qn=math.sqrt(sum(v*v for v in qw.values())) or 1
        res=[]
        for i,d in enumerate(self.docs):
            if stage and stage not in (d.get("stage") or ""): continue
            if source and source not in (d.get("sources") or []): continue
            if tag and tag not in (d.get("tags") or []): continue
            c=self.tv[i]; dot=sum(qw.get(t,0)*c.get(t,0)*self.idf.get(t,0) for t in qw)
            sc=dot/(qn*self.norm[i])
            if sc>0: res.append((sc,d))
        res.sort(key=lambda x:-x[0]); return res[:k]
# graph helpers
def g_index(G):
    lab={e["id"]:e["label"] for e in G["entities"]}; typ={e["id"]:e["type"] for e in G["entities"]}
    return lab,typ
def relate(G,eid):
    lab,typ=g_index(G); out={"as_source":[],"as_target":[]}
    for r in G["relations"]:
        if r["source"]==eid: out["as_source"].append((r["type"],lab.get(r["target"],r["target"])))
        if r["target"]==eid: out["as_target"].append((lab.get(r["source"],r["source"]),r["type"]))
    return lab.get(eid,eid),out
def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd")
    s=sub.add_parser("search"); s.add_argument("q"); s.add_argument("-k",type=int,default=5)
    s.add_argument("--stage"); s.add_argument("--source"); s.add_argument("--tag")
    g=sub.add_parser("graph"); g.add_argument("eid")
    a=sub.add_parser("ask"); a.add_argument("q"); a.add_argument("-k",type=int,default=5)
    args=ap.parse_args()
    if args.cmd=="search":
        idx=TFIDF(load_chunks())
        for sc,d in idx.search(args.q,args.k,args.stage,args.source,args.tag):
            print(f"[{sc:.3f}] {d['doc_title']} › {d['section']}  〔{d['source_file']}〕")
            print("   "+d["text"].replace("\n"," ")[:140]+"…\n")
    elif args.cmd=="graph":
        G=load_graph(); name,rel=relate(G,args.eid)
        print(f"# {args.eid}  ({name})")
        print(" 出边:"); [print(f"   -{t}-> {x}") for t,x in rel["as_source"]]
        print(" 入边:"); [print(f"   {x} -{t}->") for x,t in rel["as_target"]]
    elif args.cmd=="ask":
        idx=TFIDF(load_chunks()); G=load_graph(); lab,_=g_index(G)
        hits=idx.search(args.q,args.k)
        print("== 语义召回(RAG)==")
        for sc,d in hits:
            print(f"[{sc:.3f}] {d['doc_title']} › {d['section']}\n   "+d["text"].replace("\n"," ")[:130]+"…")
        # dominant stage
        from collections import Counter
        st=Counter(d["stage"] for sc,d in hits if d.get("stage")).most_common(1)
        if st:
            sid="stage_"+st[0][0][:2]
            caps=[lab[r["source"]] for r in G["relations"] if r["type"]=="SUPPORTS" and r["target"]==sid]
            nxt=[lab[r["target"]] for r in G["relations"] if r["type"]=="NEXT" and r["source"]==sid]
            proj=[lab[r["source"]] for r in G["relations"] if r["type"]=="BELONGS_TO" and r["target"]==sid]
            print(f"\n== 图谱关联(KG · {lab.get(sid,sid)})==")
            if caps: print("  Shopify 能力:", " / ".join(caps))
            if proj: print("  真实项目:", " / ".join(proj))
            if nxt: print("  下一节点:", " / ".join(nxt))
    else: ap.print_help()
if __name__=="__main__": main()
