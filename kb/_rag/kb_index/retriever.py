# -*- coding: utf-8 -*-
"""生产检索:可插拔嵌入(默认离线 LSA)+ 持久索引 + 图谱1跳扩展。
生产替换:把 LSAEmbedder 换成 STEmbedder(bge-m3)或 OpenAIEmbedder;把 meta/向量换 Chroma/Qdrant;图换 Neo4j。"""
import json,os,re,math,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); RAG=os.path.dirname(HERE); KB=os.path.dirname(RAG)
CHUNKS=os.path.join(RAG,"chunks.jsonl"); GRAPH=os.path.join(KB,"_kg","graph.json"); STORE=os.path.join(HERE,"index_store")

def toks(s):
    s=(s or "").lower(); out=re.findall(r"[a-z0-9]+",s)
    han=re.findall(r"[一-鿿]",s); out+=han+[han[i]+han[i+1] for i in range(len(han)-1)]
    return out

class LSAEmbedder:
    """离线潜在语义嵌入(TF-IDF + 截断SVD),零外部依赖。"""
    def __init__(self,dim=160): self.dim=dim
    def fit(self,texts):
        df={}; docs=[]
        for t in texts:
            c={}
            for w in toks(t): c[w]=c.get(w,0)+1
            docs.append(c)
            for w in c: df[w]=df.get(w,0)+1
        self.vocab={w:i for i,w in enumerate([w for w,d in df.items() if d>=2])}
        V=len(self.vocab); N=len(docs); self.idf=np.zeros(V)
        for w,i in self.vocab.items(): self.idf[i]=math.log(1+N/df[w])
        X=np.zeros((N,V),dtype=np.float32)
        for r,c in enumerate(docs):
            for w,f in c.items():
                j=self.vocab.get(w)
                if j is not None: X[r,j]=(1+math.log(f))*self.idf[j]
        X/=(np.linalg.norm(X,axis=1,keepdims=True)+1e-9)
        k=min(self.dim,N-1); U,S,Vt=np.linalg.svd(X,full_matrices=False)
        self.Vk=Vt[:k]; self.Sk=S[:k]; self.doc_emb=U[:,:k]*S[:k]
        self.doc_emb/=(np.linalg.norm(self.doc_emb,axis=1,keepdims=True)+1e-9); return self
    def embed_query(self,q):
        V=len(self.vocab); x=np.zeros(V,dtype=np.float32); c={}
        for w in toks(q): c[w]=c.get(w,0)+1
        for w,f in c.items():
            j=self.vocab.get(w)
            if j is not None: x[j]=(1+math.log(f))*self.idf[j]
        x/=(np.linalg.norm(x)+1e-9); qk=(x@self.Vk.T)/(self.Sk+1e-9)
        return qk/(np.linalg.norm(qk)+1e-9)
    def save(self,p): np.savez(p,Vk=self.Vk,Sk=self.Sk,doc_emb=self.doc_emb,idf=self.idf,vocab=np.array(list(self.vocab.keys())))
    def load(self,p):
        z=np.load(p,allow_pickle=True); self.Vk=z["Vk"];self.Sk=z["Sk"];self.doc_emb=z["doc_emb"];self.idf=z["idf"]
        self.vocab={w:i for i,w in enumerate(z["vocab"].tolist())}; return self

def build_index():
    os.makedirs(STORE,exist_ok=True)
    chunks=[json.loads(l) for l in open(CHUNKS,encoding="utf-8")]
    emb=LSAEmbedder().fit([c["text"]+" "+c.get("doc_title","")+" "+c.get("summary","") for c in chunks])
    emb.save(os.path.join(STORE,"lsa.npz"))
    json.dump(chunks,open(os.path.join(STORE,"meta.json"),"w",encoding="utf-8"),ensure_ascii=False)
    return len(chunks)

class Retriever:
    def __init__(self):
        self.emb=LSAEmbedder().load(os.path.join(STORE,"lsa.npz"))
        self.meta=json.load(open(os.path.join(STORE,"meta.json"),encoding="utf-8"))
        self.G=json.load(open(GRAPH,encoding="utf-8")); self.lab={e["id"]:e["label"] for e in self.G["entities"]}
    def search(self,q,k=5,stage=None,source=None,tag=None):
        sims=self.emb.doc_emb@self.emb.embed_query(q); out=[]
        for i in np.argsort(-sims):
            d=self.meta[i]
            if stage and stage not in (d.get("stage") or ""): continue
            if source and source not in (d.get("sources") or []): continue
            if tag and tag not in (d.get("tags") or []): continue
            out.append((float(sims[i]),d))
            if len(out)>=k: break
        return out
    def graph_expand(self,sid):
        f=lambda ty,key:[self.lab[r[key]] for r in self.G["relations"] if r["type"]==ty and r[("target" if key=="source" else "source")]==sid]
        return f("SUPPORTS","source"),f("BELONGS_TO","source"),f("NEXT","target")
    def ask(self,q,k=5):
        hits=self.search(q,k); from collections import Counter
        st=Counter(d["stage"] for s,d in hits if d.get("stage")).most_common(1)
        ge=("stage_"+st[0][0][:2],)+self.graph_expand("stage_"+st[0][0][:2]) if st else None
        return hits,ge
