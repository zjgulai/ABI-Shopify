#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build T6 multi-source intake drafts from user-provided JSON/JSONL.

This script is intentionally offline: it does not fetch external pages and does
not call an LLM/provider. It turns pasted transcripts, post lists, or source
notes into reviewable Markdown drafts that can later be promoted into the KB.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable


SECTION_TITLES = [
    "一句话主旨",
    "核心步骤 / SOP",
    "用到的工具 / App / 平台",
    "关键数据 / 案例 / 数字",
    "坑与反例",
    "对应节点",
    "可落地要点",
    "辨别夸大",
]


DEFAULT_PLACEHOLDER = "待根据用户提供的字幕、清单或帖子正文萃取；禁止仅凭标题补写事实。"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create T6 multi-source Markdown intake drafts from JSON/JSONL."
    )
    parser.add_argument("input", type=Path, help="JSON array or JSONL file with source items.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("kb/drafts/t6_multisource"),
        help="Output directory for draft Markdown files.",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Also write _index.md in the output directory.",
    )
    return parser.parse_args()


def load_items(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError(f"input is empty: {path}")

    if raw[0] in "[{":
        data = json.loads(raw)
        if isinstance(data, dict):
            data = data.get("items", [data])
        if not isinstance(data, list):
            raise ValueError("JSON input must be an array, an object, or an object with items[].")
        return [ensure_item(item, idx + 1) for idx, item in enumerate(data)]

    items: list[dict[str, Any]] = []
    for idx, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        items.append(ensure_item(json.loads(line), idx))
    return items


def ensure_item(value: Any, idx: int) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"item #{idx} must be a JSON object")
    if not str(value.get("title", "")).strip():
        raise ValueError(f"item #{idx} is missing required field: title")
    return value


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def first_text(item: dict[str, Any], fields: Iterable[str]) -> str:
    for field in fields:
        value = item.get(field)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def stable_hash(item: dict[str, Any]) -> str:
    seed = json.dumps(item, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]


def slugify(title: str, digest: str) -> str:
    ascii_title = title.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
    if not slug:
        slug = "item"
    return f"{slug[:72].strip('-')}-{digest}"


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(yaml_scalar(value) for value in values) + "]"


def render_frontmatter(item: dict[str, Any], source_type: str, platform: str) -> str:
    title = str(item["title"]).strip()
    tags = ["t6", "多源深挖", platform, source_type]
    sources = [platform]
    status = str(item.get("status") or "draft").strip()
    summary = (
        f"{platform} 来源《{title}》的 T6 多源萃取草稿；原始材料来自用户粘贴，"
        "待按 8 段结构人审补全。"
    )
    return "\n".join(
        [
            "---",
            f"title: {yaml_scalar(title)}",
            "stage: 90-AI能力地图",
            "layer: 横切层",
            f"tags: {yaml_list(tags)}",
            f"sources: {yaml_list(sources)}",
            f"status: {yaml_scalar(status)}",
            f"updated: {date.today().isoformat()}",
            f"summary: {yaml_scalar(summary)}",
            "---",
            "",
        ]
    )


def render_item(item: dict[str, Any]) -> str:
    title = str(item["title"]).strip()
    platform = str(item.get("platform") or "unknown").strip().lower()
    source_type = str(
        item.get("source_type") or ("transcript" if item.get("transcript") else "source_note")
    ).strip().lower()
    url = str(item.get("url") or "").strip()
    channel = str(item.get("channel") or item.get("author") or "").strip()
    published = str(item.get("published") or item.get("date") or "").strip()
    nodes = as_list(item.get("nodes"))
    tools = as_list(item.get("tools"))
    claims = as_list(item.get("claims"))
    raw_text = first_text(item, ["transcript", "content", "notes", "body", "summary"])

    node_text = "、".join(f"[[{node}]]" for node in nodes) if nodes else DEFAULT_PLACEHOLDER
    tools_text = "\n".join(f"- {tool}" for tool in tools) if tools else f"- {DEFAULT_PLACEHOLDER}"
    claims_text = "\n".join(f"- {claim}" for claim in claims) if claims else f"- {DEFAULT_PLACEHOLDER}"

    lines = [render_frontmatter(item, source_type, platform)]
    lines.extend(
        [
            f"# {title}",
            "",
            "> 输入边界: 本文件由 `kb/tools/t6_multisource_intake.py` 从用户提供材料生成；未联网抓取；未调用模型；状态为待人审草稿。",
            "",
            "## 0. 来源登记",
            f"- 平台: {platform}",
            f"- 类型: {source_type}",
            f"- 标题: {title}",
            f"- 链接: {url or '待补'}",
            f"- 作者/频道: {channel or '待补'}",
            f"- 发布时间: {published or '待补'}",
            f"- 初始节点映射: {node_text}",
            "",
        ]
    )

    for idx, section in enumerate(SECTION_TITLES, 1):
        lines.append(f"## {idx}. {section}")
        if idx == 3:
            lines.append(tools_text)
        elif idx == 4:
            lines.append(claims_text)
        elif idx == 6:
            lines.append(f"- {node_text}")
        else:
            lines.append(f"- {DEFAULT_PLACEHOLDER}")
        lines.append("")

    lines.extend(
        [
            "## 9. 原始材料",
            "```text",
            raw_text or "待补：请粘贴字幕、帖子正文、评论摘要或人工整理清单。",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_index(out_dir: Path, written: list[tuple[Path, dict[str, Any]]]) -> None:
    rows = []
    for path, item in written:
        platform = str(item.get("platform") or "unknown").strip().lower()
        source_type = str(item.get("source_type") or "source_note").strip().lower()
        title = str(item["title"]).replace("|", "\\|")
        rows.append(f"| [{title}]({path.name}) | {platform} | {source_type} | draft |")

    body = "\n".join(
        [
            "---",
            'title: "T6 多源深挖草稿索引"',
            "stage: 90-AI能力地图",
            "layer: 横切层",
            'tags: ["t6", "多源深挖", "index"]',
            'sources: ["用户粘贴"]',
            'status: "draft"',
            f"updated: {date.today().isoformat()}",
            'summary: "由 t6_multisource_intake.py 生成的多源材料草稿索引；仅作人审与后续入库入口。"',
            "---",
            "",
            "# T6 多源深挖草稿索引",
            "",
            "| 标题 | 平台 | 类型 | 状态 |",
            "|---|---|---|---|",
            *rows,
            "",
        ]
    )
    (out_dir / "_index.md").write_text(body, encoding="utf-8")


def main() -> int:
    args = parse_args()
    items = load_items(args.input)
    if not items:
        raise ValueError("no items found")

    args.out.mkdir(parents=True, exist_ok=True)
    written: list[tuple[Path, dict[str, Any]]] = []
    for item in items:
        digest = stable_hash(item)
        path = args.out / f"{slugify(str(item['title']), digest)}.md"
        path.write_text(render_item(item), encoding="utf-8")
        written.append((path, item))

    if args.index:
        write_index(args.out, written)

    for path, _item in written:
        print(path)
    if args.index:
        print(args.out / "_index.md")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
