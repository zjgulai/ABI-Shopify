# -*- coding: utf-8 -*-
import os, re, json, glob, hashlib
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"_rag"); os.makedirs(OUT,exist_ok=True)

def parse_fm(txt):
    meta={}; body=txt
    if txt.startswith("---"):
        end=txt.find("\n---",3)
        if end!=-1:
            fm=txt[3:end]; body=txt[end+4:]
            for line in fm.splitlines():
                m=re.match(r"\s*([A-Za-z_]+):\s*(.*)", line)
                if not m: continue
                k,v=m.group(1),m.group(2).strip()
                v=re.sub(r"\s{2,}#.*$","",v).strip()
                if v.startswith("[") and v.endswith("]"):
                    v=[x.strip() for x in v[1:-1].split(",") if x.strip()]
                else:
                    v=v.strip().strip('"')
                meta[k]=v
    return meta, body

def chunks_from(path):
    rel=os.path.relpath(path,ROOT)
    meta,body=parse_fm(open(path,encoding="utf-8").read())
    title=meta.get("title") or os.path.basename(path)
    # split by level-2 headings
    parts=re.split(r"\n(?=## )", body)
    out=[]
    for i,part in enumerate(parts):
        text=part.strip()
        if len(text)<15: continue
        hm=re.match(r"##\s+(.*)", text)
        section=hm.group(1).strip() if hm else "(intro)"
        # clean body text (strip the heading line for the field but keep in text)
        cid=hashlib.md5((rel+"#"+str(i)+section).encode()).hexdigest()[:12]
        out.append({
            "id":cid,
            "doc_title":title,
            "section":section,
            "stage":meta.get("stage",""),
            "layer":meta.get("layer",""),
            "tags":meta.get("tags",[]) if isinstance(meta.get("tags",[]),list) else [],
            "sources":meta.get("sources",[]) if isinstance(meta.get("sources",[]),list) else [],
            "summary":meta.get("summary",""),
            "source_file":rel,
            "text":text,
            "char_len":len(text),
        })
    return out

allc=[]
for p in sorted(glob.glob(ROOT+"/**/*.md",recursive=True)):
    if "/_rag/" in p: continue
    allc.extend(chunks_from(p))

with open(os.path.join(OUT,"chunks.jsonl"),"w",encoding="utf-8") as f:
    for c in allc:
        f.write(json.dumps(c,ensure_ascii=False)+"\n")

# stats
docs=len(set(c["source_file"] for c in allc))
lens=[c["char_len"] for c in allc]
avg_len=sum(lens)//len(lens) if lens else 0
stages=sorted(set(c["stage"] for c in allc if c["stage"]))
readme=f"""---
title: RAG 切块层说明
type: meta
updated: 2026-06-30
summary: 知识库的 RAG 就绪切块。chunks.jsonl 每行一个块,含 stage/tags/sources/summary 元数据,可直接做向量化与按节点路由。
---

# _rag — RAG 切块层

- **chunks.jsonl**:{len(allc)} 个块,来自 {docs} 个文档;每行一个 JSON。
- 切块粒度:按 Markdown 的 `## 一级小节`,每块尽量自洽。
- 字段:`id, doc_title, section, stage, layer, tags[], sources[], summary, source_file, text, char_len`。
- 用法:对 `text` 做 embedding;用 `stage/tags/sources` 做过滤与按节点路由;`summary` 可作卡片/重排序信号。
- 平均块长 ≈ {avg_len} 字符(min {min(lens)} / max {max(lens)})。

> 重建命令:见 `_build/build_rag.py`(本仓库脚本,解析 frontmatter + 按小节切块)。
"""
open(os.path.join(OUT,"README.md"),"w",encoding="utf-8").write(readme)

print("chunks:",len(allc),"| docs:",docs)
print("avg_len:",avg_len,"min:",min(lens),"max:",max(lens))
print("stages covered:",len(stages))
# validate jsonl
ok=sum(1 for _ in open(os.path.join(OUT,"chunks.jsonl"),encoding="utf-8"))
print("\njsonl lines:",ok,"= chunks:",ok==len(allc))
