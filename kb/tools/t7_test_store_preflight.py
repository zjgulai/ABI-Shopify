#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T7 Shopify test-store preflight.

Local-only checks for the ABI Shopify T7 lane. This script does not login,
call Shopify, invoke npx packages, or print secret values.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

KB = Path(__file__).resolve().parents[1]
REPO = KB.parent

MIN_NODE = (22, 12, 0)
MIN_GIT = (2, 28, 0)
SENSITIVE_ENV = [
    "SHOPIFY_CLI_PARTNERS_TOKEN",
    "SHOPIFY_API_KEY",
    "SHOPIFY_API_SECRET",
    "SHOPIFY_ACCESS_TOKEN",
    "DEEPSEEK_API_KEY",
    "OPENAI_API_KEY",
    "NEO4J_PASSWORD",
]


def run_version(cmd: list[str]) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        out = subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5,
        )
    except Exception:
        return None
    return (out.stdout or "").strip().splitlines()[0] if out.stdout else ""


def parse_semver(text: str | None) -> tuple[int, int, int] | None:
    if not text:
        return None
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))


def version_ok(actual: tuple[int, int, int] | None, minimum: tuple[int, int, int]) -> bool:
    return bool(actual and actual >= minimum)


def command_check(name: str, cmd: list[str], minimum: tuple[int, int, int] | None = None) -> dict[str, Any]:
    raw = run_version(cmd)
    parsed = parse_semver(raw)
    exists = shutil.which(cmd[0]) is not None
    return {
        "name": name,
        "command": cmd[0],
        "exists": exists,
        "version": raw,
        "minimum": ".".join(map(str, minimum)) if minimum else None,
        "pass": exists and (version_ok(parsed, minimum) if minimum else True),
    }


def validate_store_domain(store: str | None) -> dict[str, Any]:
    if not store:
        return {
            "provided": False,
            "pass": False,
            "note": "manual_required: provide a development store domain before auth",
        }
    value = store.strip().lower().replace("https://", "").replace("http://", "").strip("/")
    ok = bool(re.fullmatch(r"[a-z0-9][a-z0-9-]*\.myshopify\.com", value))
    return {
        "provided": True,
        "domain": value,
        "pass": ok,
        "note": "looks_like_shopify_store_domain" if ok else "expected format: name.myshopify.com",
    }


def path_check(label: str, rel: str) -> dict[str, Any]:
    path = REPO / rel
    return {"label": label, "path": rel, "exists": path.exists(), "pass": path.exists()}


def build_report(store_domain: str | None) -> dict[str, Any]:
    checks = [
        command_check("Node.js", ["node", "--version"], MIN_NODE),
        command_check("npm", ["npm", "--version"]),
        command_check("npx", ["npx", "--version"]),
        command_check("Git", ["git", "--version"], MIN_GIT),
        command_check("Python", [sys.executable, "--version"]),
    ]
    paths = [
        path_check("shopify-ai-kb marketplace", "kb/marketplace/.claude-plugin/marketplace.json"),
        path_check("T7 controlled-write runbook", "kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md"),
        path_check("T7 preflight document", "kb/10-自动化编排/T7测试店授权前置包.md"),
        path_check("site data", "kb/site/kb_data.js"),
    ]
    env = {name: ("set" if os.environ.get(name) else "unset") for name in SENSITIVE_ENV}
    store = validate_store_domain(store_domain)
    local_pass = all(c["pass"] for c in checks) and all(p["pass"] for p in paths)
    return {
        "status": "local_pass_auth_required" if local_pass and store["pass"] else "manual_action_required",
        "boundary": {
            "network_calls": False,
            "shopify_login": False,
            "shopify_read": False,
            "shopify_write": False,
            "secret_values_printed": False,
        },
        "official_requirements_checked_at": "2026-06-30",
        "store_domain": store,
        "local_requirements": checks,
        "local_assets": paths,
        "sensitive_env_names": env,
        "next_manual_steps": [
            "Confirm the target is a development store or test store.",
            "Run shopify auth login only with the user present.",
            "Perform read-only connection verification before any mutation preview.",
            "Require explicit approval text before every low-risk test-store mutation.",
        ],
    }


def print_text(report: dict[str, Any]) -> None:
    print(f"status: {report['status']}")
    print("boundary: no network call, no Shopify login, no store read/write, no secret values printed")
    print("\nlocal requirements:")
    for item in report["local_requirements"]:
        mark = "PASS" if item["pass"] else "ACTION"
        minv = f" >= {item['minimum']}" if item.get("minimum") else ""
        print(f"- [{mark}] {item['name']}: {item.get('version') or 'missing'}{minv}")
    print("\nlocal assets:")
    for item in report["local_assets"]:
        mark = "PASS" if item["pass"] else "ACTION"
        print(f"- [{mark}] {item['path']}")
    store = report["store_domain"]
    print("\nstore domain:")
    print(f"- [{'PASS' if store['pass'] else 'ACTION'}] {store.get('domain') or 'not provided'} ({store['note']})")
    set_env = [k for k, v in report["sensitive_env_names"].items() if v == "set"]
    print("\nsensitive env names set:")
    print("- " + (", ".join(set_env) if set_env else "none"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Local-only T7 Shopify test-store preflight")
    ap.add_argument("--store-domain", help="Expected development store domain, e.g. abi-t7-smoke.myshopify.com")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args()
    report = build_report(args.store_domain)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
