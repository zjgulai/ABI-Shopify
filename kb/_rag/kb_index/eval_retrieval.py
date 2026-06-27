# -*- coding: utf-8 -*-
"""小型离线检索评测。

用途:验证当前 index_store 的召回是否覆盖关键业务问题。该脚本不调用外部模型;
如果索引是 ST/OpenAI 构建的,会按对应 manifest 加载 query embedder。
"""
import argparse
import json
import sys

import retriever as R


CASES = [
    {
        "query": "AI Toolkit Dev MCP 怎么自然语言建站改店",
        "any_stage": ["02-建站与基础设施", "90-AI能力地图", "10-自动化编排"],
    },
    {
        "query": "PRD 人审闸 测试店 受控写 上架改价",
        "any_file": ["PRD_ABI智能化独立站.md", "迭代方案与PRD_TODO.md"],
    },
    {
        "query": "Accio Work RFQ 选品 供应商 数据桥 导入 Shopify",
        "any_stage": ["01-选品与市场调研"],
    },
    {
        "query": "Shopify Functions 满赠 折扣 结账校验 CRO",
        "any_stage": ["06-转化优化CRO"],
    },
    {
        "query": "UCP Catalog Agent profile Shop Pay AP2",
        "any_stage": ["10-自动化编排"],
    },
]


def hit_ok(hit, case):
    _, doc = hit
    if "any_stage" in case and doc.get("stage") in case["any_stage"]:
        return True
    if "any_file" in case and doc.get("source_file") in case["any_file"]:
        return True
    return False


def evaluate(retriever, k):
    rows = []
    passed = 0
    top1 = 0
    reciprocal_rank_total = 0.0
    for idx, case in enumerate(CASES, 1):
        hits = retriever.search(case["query"], k)
        first_rank = None
        for rank, hit in enumerate(hits, 1):
            if hit_ok(hit, case):
                first_rank = rank
                break
        ok = first_rank is not None
        passed += int(ok)
        top1 += int(first_rank == 1)
        if first_rank:
            reciprocal_rank_total += 1.0 / first_rank
        rows.append({"case": idx, "query": case["query"], "ok": ok, "first_rank": first_rank, "hits": hits})
    total = len(CASES)
    return {
        "rows": rows,
        "pass_rate": passed / total,
        "top1_rate": top1 / total,
        "mrr": reciprocal_rank_total / total,
        "passed": passed,
        "total": total,
    }


def print_report(report):
    for row in report["rows"]:
        marker = "PASS" if row["ok"] else "MISS"
        print(f"\n[{marker}] case {row['case']}: {row['query']}")
        for score, doc in row["hits"][:3]:
            print(f"  {score:.3f} | {doc.get('stage','')} | {doc['doc_title']} | {doc['source_file']}")
    print(
        "\npass_rate={:.2f} ({}/{}) top1_rate={:.2f} mrr={:.2f}".format(
            report["pass_rate"],
            report["passed"],
            report["total"],
            report["top1_rate"],
            report["mrr"],
        )
    )


def jsonable(report):
    rows = []
    for row in report["rows"]:
        rows.append(
            {
                "case": row["case"],
                "query": row["query"],
                "ok": row["ok"],
                "first_rank": row["first_rank"],
                "top_hits": [
                    {
                        "score": round(score, 4),
                        "stage": doc.get("stage", ""),
                        "doc_title": doc["doc_title"],
                        "source_file": doc["source_file"],
                    }
                    for score, doc in row["hits"][:3]
                ],
            }
        )
    return {
        "pass_rate": report["pass_rate"],
        "top1_rate": report["top1_rate"],
        "mrr": report["mrr"],
        "passed": report["passed"],
        "total": report["total"],
        "rows": rows,
    }


def main():
    ap = argparse.ArgumentParser(description="KB retrieval quality smoke")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--min-pass-rate", type=float, default=0.6)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    retriever = R.Retriever()
    report = evaluate(retriever, args.k)
    payload = {"backend": retriever.status()["manifest"], "report": jsonable(report)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("backend:", payload["backend"])
        print_report(report)
    if report["pass_rate"] < args.min_pass_rate:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
