#!/bin/sh
set -eu

if [ ! -f /app/_rag/kb_index/index_store/manifest.json ]; then
  cd /app/_rag/kb_index
  python cli.py build --embedder lsa --store numpy
fi

if [ "${KB_RUNTIME_BUILD_ON_START:-0}" = "1" ]; then
  need_runtime_build="$(
    python - <<'PY'
import json
import os

path = "/app/_rag/kb_index/index_store/manifest.json"
try:
    manifest = json.load(open(path, encoding="utf-8"))
except Exception:
    manifest = {}

desired_embedder = (os.environ.get("KB_EMBEDDER") or "lsa").strip().lower()
desired_store = (os.environ.get("KB_VECTOR_STORE") or "numpy").strip().lower()
desired_model = (os.environ.get("KB_ST_MODEL") or "").strip()
current_model = (manifest.get("model") or "").strip()

needs_model = desired_embedder not in {"", "lsa"} and desired_model and current_model != desired_model
need = (
    (manifest.get("embedder") or "").lower() != desired_embedder
    or (manifest.get("store") or "").lower() != desired_store
    or needs_model
)
print("1" if need else "0")
PY
  )"

  if [ "$need_runtime_build" = "1" ]; then
    echo "runtime_index_build_start embedder=${KB_EMBEDDER:-lsa} store=${KB_VECTOR_STORE:-numpy} model=${KB_ST_MODEL:-}"
    if [ -n "${KB_ST_MODEL:-}" ] && [ "${KB_EMBEDDER:-lsa}" != "lsa" ]; then
      if cd /app/_rag/kb_index && python cli.py build --embedder "${KB_EMBEDDER:-lsa}" --store "${KB_VECTOR_STORE:-numpy}" --model "$KB_ST_MODEL"; then
        echo "runtime_index_build_ready"
      elif [ "${KB_RUNTIME_BUILD_REQUIRED:-0}" = "1" ]; then
        exit 1
      else
        echo "runtime_index_build_unavailable; continuing with existing index"
      fi
    else
      if cd /app/_rag/kb_index && python cli.py build --embedder "${KB_EMBEDDER:-lsa}" --store "${KB_VECTOR_STORE:-numpy}"; then
        echo "runtime_index_build_ready"
      elif [ "${KB_RUNTIME_BUILD_REQUIRED:-0}" = "1" ]; then
        exit 1
      else
        echo "runtime_index_build_unavailable; continuing with existing index"
      fi
    fi
  fi
fi

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

cd /app/site
exec "$@"
