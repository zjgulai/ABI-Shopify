# -*- coding: utf-8 -*-
"""检索后端 A/B 评测。

默认流程:
1. 构建 baseline: LSA + numpy。
2. 构建 candidate: sentence-transformers + Chroma。
3. 输出 pass@k / top1 / MRR。
4. 保留 candidate 索引,供服务启动使用。
"""
import argparse
import json
import sys

import eval_retrieval
import retriever as R


def build_and_eval(embedder, store, model, k):
    manifest = R.build_index(embedder=embedder, store=store, model=model)
    retriever = R.Retriever()
    report = eval_retrieval.evaluate(retriever, k)
    return manifest, eval_retrieval.jsonable(report)


def main():
    ap = argparse.ArgumentParser(description="Compare Shopify KB retrieval backends")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--baseline-embedder", default="lsa")
    ap.add_argument("--baseline-store", default="numpy")
    ap.add_argument("--candidate-embedder", default="st")
    ap.add_argument("--candidate-store", default="chroma")
    ap.add_argument("--candidate-model", default=None)
    ap.add_argument("--min-candidate-pass-rate", type=float, default=0.6)
    ap.add_argument("--require-no-regression", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    baseline_manifest, baseline = build_and_eval(
        args.baseline_embedder,
        args.baseline_store,
        None,
        args.k,
    )
    candidate_manifest, candidate = build_and_eval(
        args.candidate_embedder,
        args.candidate_store,
        args.candidate_model,
        args.k,
    )
    result = {
        "baseline": {"manifest": baseline_manifest, "report": baseline},
        "candidate": {"manifest": candidate_manifest, "report": candidate},
        "delta": {
            "pass_rate": candidate["pass_rate"] - baseline["pass_rate"],
            "top1_rate": candidate["top1_rate"] - baseline["top1_rate"],
            "mrr": candidate["mrr"] - baseline["mrr"],
        },
        "candidate_left_active": True,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("== baseline ==")
        print(json.dumps(result["baseline"]["manifest"], ensure_ascii=False))
        print(
            "pass_rate={pass_rate:.2f} top1_rate={top1_rate:.2f} mrr={mrr:.2f}".format(
                **baseline
            )
        )
        print("\n== candidate ==")
        print(json.dumps(result["candidate"]["manifest"], ensure_ascii=False))
        print(
            "pass_rate={pass_rate:.2f} top1_rate={top1_rate:.2f} mrr={mrr:.2f}".format(
                **candidate
            )
        )
        print("\n== delta ==")
        print(json.dumps(result["delta"], ensure_ascii=False))

    if candidate["pass_rate"] < args.min_candidate_pass_rate:
        return 1
    if args.require_no_regression and candidate["mrr"] < baseline["mrr"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
