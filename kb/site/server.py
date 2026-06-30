# -*- coding: utf-8 -*-
"""安全后端:DeepSeek RAG 问答。API Key 由页面手动录入并随请求转发;服务端不保存。
运行:  pip install flask  &&  python server.py  → http://localhost:8000
可选:  DEEPSEEK_MODEL=deepseek-v4-pro(默认 deepseek-v4-flash);
       DEEPSEEK_API_KEY 可作为本地 fallback,部署时不必配置。"""
import os,sys,json,urllib.request
from flask import Flask,request,jsonify,send_from_directory
HERE=os.path.dirname(os.path.abspath(__file__))
DEPLOY_STATUS_PATH=os.path.join(HERE,"deploy_status.json")
sys.path.insert(0,os.path.join(HERE,"..","_rag","kb_index"))
KEY=os.environ.get("DEEPSEEK_API_KEY"); MODEL=os.environ.get("DEEPSEEK_MODEL","deepseek-v4-flash")
try:
    import retriever as R; _r=R.Retriever(); print("✓ retriever loaded")
except Exception as e:
    _r=None; print("! retriever unavailable (先在 kb_index 跑 python cli.py build):",e)
app=Flask(__name__,static_folder=None)
@app.get("/api/health")
def health(): return jsonify(ok=True,retriever=_r is not None,model=MODEL,server_key_set=bool(KEY),client_key_supported=True)

def _deploy_status_file():
    allow={
        "release","local_commit","remote_branch_sha","deployed_at",
        "index_sha256","kb_data_sha256","chunks_sha256",
        "compose_project","compose_files","source","boundary"
    }
    try:
        with open(DEPLOY_STATUS_PATH,encoding="utf-8") as f:
            data=json.load(f)
        if not isinstance(data,dict):
            return {}
        return {k:data[k] for k in allow if k in data}
    except Exception:
        return {}

@app.get("/api/deploy-status")
def deploy_status():
    data=_deploy_status_file()
    runtime={"retriever":_r is not None,"model":MODEL,"server_key_set":bool(KEY),"client_key_supported":True}
    if _r:
        try:
            status=_r.status()
            if isinstance(status,dict):
                safe={k:status[k] for k in status if k in {"backend","chunks","chunks_loaded","embedder","store","model","vector_dim","graph_backend"}}
                manifest=status.get("manifest")
                if isinstance(manifest,dict):
                    safe["manifest"]={k:manifest[k] for k in manifest if k in {"index_version","embedder","store","model","chunks","graph_backend_default"}}
                runtime["retriever_status"]=safe
        except Exception:
            runtime["retriever_status_unavailable"]=True
    data.update(ok=True,status_file=bool(data),runtime=runtime)
    return jsonify(data)

@app.post("/api/chat")
def chat():
    b=request.get_json(force=True); q=b.get("question","")
    api_key=(b.get("api_key") or KEY or "").strip()
    if not api_key: return jsonify(error="请先在页面填入 DeepSeek API Key")
    cites=[]
    if _r:
        hits=_r.search(q,6)
        ctx="\n\n".join(f"[{i+1}] ({d['doc_title']}›{d['section']})\n{d['text']}" for i,(s,d) in enumerate(hits))
        cites=[f"{d['doc_title']}›{d['section']}" for s,d in hits[:4]]
        messages=[{"role":"system","content":"你是 Shopify 独立站 AI 经营知识库问答助手。只依据【知识库片段】用中文简洁专业作答;无法回答时说明并建议查看相关节点。"},
                  {"role":"user","content":f"【知识库片段】\n{ctx}\n\n【问题】{q}"}]
    else:
        messages=b.get("messages",[{"role":"user","content":q}])
    try:
        req=urllib.request.Request("https://api.deepseek.com/chat/completions",
            data=json.dumps({"model":MODEL,"messages":messages,"temperature":0.3}).encode(),
            headers={"Content-Type":"application/json","Authorization":"Bearer "+api_key})
        with urllib.request.urlopen(req,timeout=90) as r:
            j=json.loads(r.read()); return jsonify(answer=j["choices"][0]["message"]["content"],cites=cites)
    except Exception as e:
        return jsonify(error=f"DeepSeek 调用失败:{e}")
@app.get("/")
def idx(): return send_from_directory(HERE,"index.html")
@app.get("/<path:p>")
def st(p): return send_from_directory(HERE,p)
if __name__=="__main__":
    print(f"→ http://localhost:8000  (model={MODEL}, client_key_supported=True, server_key_set={bool(KEY)})")
    app.run(port=8000)
