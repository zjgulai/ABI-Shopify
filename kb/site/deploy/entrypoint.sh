#!/bin/sh
set -eu

if [ "${KB_GRAPH_BACKEND:-json}" = "neo4j" ]; then
  python - <<'PY'
import os
import socket
import time
from urllib.parse import urlparse

uri = os.environ.get("NEO4J_URI", "bolt://shopifykb-neo4j:7687")
u = urlparse(uri)
host = u.hostname or "shopifykb-neo4j"
port = u.port or 7687
deadline = time.time() + int(os.environ.get("NEO4J_WAIT_SECONDS", "90"))
while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=3):
            print(f"neo4j_socket_ready={host}:{port}")
            raise SystemExit(0)
    except OSError:
        time.sleep(2)
raise SystemExit(f"neo4j_socket_not_ready={host}:{port}")
PY

  if [ "${KB_GRAPH_IMPORT_ON_START:-0}" = "1" ]; then
    python /app/_rag/kb_index/neo4j_export.py --apply
  fi
fi

exec "$@"
