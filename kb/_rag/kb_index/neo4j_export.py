# -*- coding: utf-8 -*-
"""Neo4j 图谱导入辅助。

默认只做 dry-run;加 --write-cypher 输出可审计 Cypher;加 --apply 且配置
NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD 后才会写入 Neo4j。
"""
import argparse
import json
import os
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
KB = HERE.parents[1]
GRAPH = KB / "_kg" / "graph.json"


def qident(value):
    ident = re.sub(r"[^A-Za-z0-9_]", "_", value or "KGEntity")
    if not ident or ident[0].isdigit():
        ident = "KG_" + ident
    return ident


def load_graph():
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def cypher_literal(value):
    return json.dumps(value, ensure_ascii=False)


def build_cypher(graph):
    lines = [
        "CREATE CONSTRAINT kg_entity_id IF NOT EXISTS FOR (n:KGEntity) REQUIRE n.id IS UNIQUE;",
        "",
    ]
    for ent in graph["entities"]:
        label = qident(ent.get("type"))
        props = {
            "id": ent["id"],
            "kg_type": ent.get("type", ""),
            "label": ent.get("label", ""),
            "props_json": json.dumps(ent.get("props") or {}, ensure_ascii=False),
        }
        lines.append(
            "MERGE (n:KGEntity:`{label}` {{id:{id}}}) "
            "SET n.kg_type={kg_type}, n.label={label_value}, n.props_json={props_json};".format(
                label=label,
                id=cypher_literal(props["id"]),
                kg_type=cypher_literal(props["kg_type"]),
                label_value=cypher_literal(props["label"]),
                props_json=cypher_literal(props["props_json"]),
            )
        )
    lines.append("")
    for rel in graph["relations"]:
        rel_type = qident(rel.get("type"))
        lines.append(
            "MATCH (a:KGEntity {{id:{source}}}), (b:KGEntity {{id:{target}}}) "
            "MERGE (a)-[:`{rel_type}`]->(b);".format(
                source=cypher_literal(rel["source"]),
                target=cypher_literal(rel["target"]),
                rel_type=rel_type,
            )
        )
    return "\n".join(lines) + "\n"


def apply_neo4j(graph):
    uri = os.environ.get("NEO4J_URI")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD")
    if not uri or not password:
        raise SystemExit("NEO4J_URI 与 NEO4J_PASSWORD 必须设置;未写入。")
    try:
        from neo4j import GraphDatabase
    except Exception as exc:
        raise SystemExit(f"neo4j 包未安装;未写入: {exc}") from exc

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        session.run("CREATE CONSTRAINT kg_entity_id IF NOT EXISTS FOR (n:KGEntity) REQUIRE n.id IS UNIQUE")
        for ent in graph["entities"]:
            label = qident(ent.get("type"))
            session.run(
                f"MERGE (n:KGEntity:`{label}` {{id:$id}}) "
                "SET n.kg_type=$kg_type, n.label=$label, n.props=$props",
                id=ent["id"],
                kg_type=ent.get("type", ""),
                label=ent.get("label", ""),
                props=ent.get("props") or {},
            )
        for rel in graph["relations"]:
            rel_type = qident(rel.get("type"))
            session.run(
                f"MATCH (a:KGEntity {{id:$source}}), (b:KGEntity {{id:$target}}) "
                f"MERGE (a)-[:`{rel_type}`]->(b)",
                source=rel["source"],
                target=rel["target"],
            )
    driver.close()


def main():
    ap = argparse.ArgumentParser(description="Export/import Shopify KB graph to Neo4j")
    ap.add_argument("--write-cypher", help="输出 Cypher 文件路径")
    ap.add_argument("--apply", action="store_true", help="写入 Neo4j,需显式配置 NEO4J_*")
    args = ap.parse_args()

    graph = load_graph()
    print(f"entities={len(graph['entities'])} relations={len(graph['relations'])}")
    if args.write_cypher:
        out = Path(args.write_cypher)
        out.write_text(build_cypher(graph), encoding="utf-8")
        print(f"cypher_written={out}")
    if args.apply:
        apply_neo4j(graph)
        print("neo4j_import=done")
    if not args.write_cypher and not args.apply:
        print("dry_run=true")


if __name__ == "__main__":
    main()
