# -*- coding: utf-8 -*-
"""小型离线检索评测。

用途:验证当前 index_store 的召回是否覆盖关键业务问题。该脚本不调用外部模型;
如果索引是 ST/OpenAI 构建的,会按对应 manifest 加载 query embedder。
"""
import argparse
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


def main():
    ap = argparse.ArgumentParser(description="KB retrieval quality smoke")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--min-pass-rate", type=float, default=0.6)
    args = ap.parse_args()

    retriever = R.Retriever()
    passed = 0
    print("backend:", retriever.status()["manifest"])
    for idx, case in enumerate(CASES, 1):
        hits = retriever.search(case["query"], args.k)
        ok = any(hit_ok(hit, case) for hit in hits)
        passed += int(ok)
        marker = "PASS" if ok else "MISS"
        print(f"\n[{marker}] case {idx}: {case['query']}")
        for score, doc in hits[:3]:
            print(f"  {score:.3f} | {doc.get('stage','')} | {doc['doc_title']} | {doc['source_file']}")

    rate = passed / len(CASES)
    print(f"\npass_rate={rate:.2f} ({passed}/{len(CASES)})")
    if rate < args.min_pass_rate:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
