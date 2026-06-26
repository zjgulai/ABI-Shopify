# -*- coding: utf-8 -*-
import argparse,sys; import retriever as R
def main():
    ap=argparse.ArgumentParser(description="KB 生产检索 CLI"); sub=ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    s=sub.add_parser("search"); s.add_argument("q"); s.add_argument("-k",type=int,default=5); s.add_argument("--stage"); s.add_argument("--source"); s.add_argument("--tag")
    a=sub.add_parser("ask"); a.add_argument("q"); a.add_argument("-k",type=int,default=5)
    args=ap.parse_args()
    if args.cmd=="build": print("indexed chunks:",R.build_index())
    elif args.cmd=="search":
        for sc,d in R.Retriever().search(args.q,args.k,args.stage,args.source,args.tag):
            print(f"[{sc:.3f}] {d['doc_title']} › {d['section']} 〔{d['source_file']}〕\n   "+d['text'].replace(chr(10),' ')[:130]+"…")
    elif args.cmd=="ask":
        hits,ge=R.Retriever().ask(args.q,args.k); print("== 语义召回(LSA 嵌入)==")
        for sc,d in hits: print(f"[{sc:.3f}] {d['doc_title']} › {d['section']}")
        if ge and (ge[1] or ge[2] or ge[3]):
            print(f"\n== 图谱关联({ge[0]})==")
            if ge[1]: print("  Shopify 能力:"," / ".join(ge[1]))
            if ge[2]: print("  真实项目:"," / ".join(ge[2]))
            if ge[3]: print("  下一节点:"," / ".join(ge[3]))
    else: ap.print_help()
main()
