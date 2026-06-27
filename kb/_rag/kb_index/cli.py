# -*- coding: utf-8 -*-
import argparse
import json

import retriever as R


def print_hit(score, doc):
    text = doc["text"].replace("\n", " ")[:130]
    print(f"[{score:.3f}] {doc['doc_title']} › {doc['section']} 〔{doc['source_file']}〕\n   {text}…")


def main():
    ap = argparse.ArgumentParser(description="KB 生产检索 CLI")
    sub = ap.add_subparsers(dest="cmd")

    b = sub.add_parser("build", help="构建持久检索索引")
    b.add_argument("--embedder", choices=["lsa", "st", "bge-m3", "openai"], default=None)
    b.add_argument("--store", choices=["numpy", "chroma"], default=None)
    b.add_argument("--model", help="ST/OpenAI 模型名,默认 bge-m3 或 text-embedding-3-large")

    sub.add_parser("status", help="查看当前索引 manifest 与后端")
    sub.add_parser("doctor", help="检查可选生产依赖与环境变量")

    s = sub.add_parser("search")
    s.add_argument("q")
    s.add_argument("-k", type=int, default=5)
    s.add_argument("--stage")
    s.add_argument("--source")
    s.add_argument("--tag")
    s.add_argument("--graph-backend", choices=["json", "neo4j"], default=None)

    a = sub.add_parser("ask")
    a.add_argument("q")
    a.add_argument("-k", type=int, default=5)
    a.add_argument("--graph-backend", choices=["json", "neo4j"], default=None)

    args = ap.parse_args()
    if args.cmd == "build":
        try:
            info = R.build_index(args.embedder, args.store, args.model)
        except RuntimeError as exc:
            raise SystemExit(f"build_unavailable: {exc}") from exc
        print(
            "indexed chunks: {chunks} | embedder={embedder} | store={store} | model={model}".format(
                **info
            )
        )
    elif args.cmd == "status":
        print(json.dumps(R.Retriever().status(), ensure_ascii=False, indent=2))
    elif args.cmd == "doctor":
        print(json.dumps(R.dependency_doctor(), ensure_ascii=False, indent=2))
    elif args.cmd == "search":
        for score, doc in R.Retriever(args.graph_backend).search(
            args.q,
            args.k,
            args.stage,
            args.source,
            args.tag,
        ):
            print_hit(score, doc)
    elif args.cmd == "ask":
        r = R.Retriever(args.graph_backend)
        hits, ge = r.ask(args.q, args.k)
        print(f"== 语义召回({r.manifest['embedder']} / {r.manifest['store']})==")
        for score, doc in hits:
            print(f"[{score:.3f}] {doc['doc_title']} › {doc['section']}")
        if ge and (ge[1] or ge[2] or ge[3]):
            print(f"\n== 图谱关联({ge[0]})==")
            if ge[1]:
                print("  Shopify 能力:", " / ".join(ge[1]))
            if ge[2]:
                print("  真实项目:", " / ".join(ge[2]))
            if ge[3]:
                print("  下一节点:", " / ".join(ge[3]))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
