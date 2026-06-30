#!/usr/bin/env bash
set -euo pipefail

HOST="101.34.52.232"
USER_NAME="ubuntu"
DOMAIN="https://platform.shopify.lute-tlz-dddd.top"
REMOTE_ROOT="/opt/shopify-kb"
COMPOSE_PROJECT="shopify-kb"
SSH_KEY="ai_video.pem"
MIN_PASS_RATE="1.0"
HEALTH_ATTEMPTS="24"
HEALTH_SLEEP="5"
DRY_RUN=0
SKIP_REBUILD=0
SKIP_GIT_CLEAN_CHECK=0
SKIP_PUBLIC_CHECK=0
SKIP_PLAYWRIGHT=0

usage() {
  cat <<'USAGE'
Usage: scripts/deploy_shopify_kb.sh [options]

Deploy the Shopify KB site to the Tencent Cloud release layout:
  /opt/shopify-kb/releases/<release>/kb
  /opt/shopify-kb/current -> /opt/shopify-kb/releases/<release>

Options:
  --host HOST                 SSH host. Default: 101.34.52.232
  --user USER                 SSH user. Default: ubuntu
  --domain URL                Public URL. Default: https://platform.shopify.lute-tlz-dddd.top
  --remote-root PATH          Remote release root. Default: /opt/shopify-kb
  --ssh-key PATH              SSH private key. Default: ai_video.pem
  --min-pass-rate VALUE       Local RAG eval minimum. Default: 1.0
  --health-attempts N         Remote app health attempts. Default: 24
  --health-sleep SECONDS      Remote app health interval. Default: 5
  --dry-run                   Run local checks and print planned release only.
  --skip-rebuild              Skip local RAG/site rebuild.
  --skip-git-clean-check      Allow tracked working-tree changes.
  --skip-public-check         Skip public URL hash and health checks.
  --skip-playwright           Skip browser smoke.
  -h, --help                  Show this help.

Boundaries:
  - Only rsyncs kb/ into a new release directory.
  - Does not copy .env, API keys, or root-level private keys.
  - Keeps runtime .env as a symlink to /opt/shopify-kb/shared/.env.
  - Uses compose project shopify-kb with behind-proxy + vector files.
USAGE
}

die() {
  printf 'deploy_stop: %s\n' "$*" >&2
  exit 1
}

log() {
  printf '[deploy] %s\n' "$*"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --host) HOST="${2:?missing --host value}"; shift 2 ;;
    --user) USER_NAME="${2:?missing --user value}"; shift 2 ;;
    --domain) DOMAIN="${2:?missing --domain value}"; shift 2 ;;
    --remote-root) REMOTE_ROOT="${2:?missing --remote-root value}"; shift 2 ;;
    --ssh-key) SSH_KEY="${2:?missing --ssh-key value}"; shift 2 ;;
    --min-pass-rate) MIN_PASS_RATE="${2:?missing --min-pass-rate value}"; shift 2 ;;
    --health-attempts) HEALTH_ATTEMPTS="${2:?missing --health-attempts value}"; shift 2 ;;
    --health-sleep) HEALTH_SLEEP="${2:?missing --health-sleep value}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --skip-rebuild) SKIP_REBUILD=1; shift ;;
    --skip-git-clean-check) SKIP_GIT_CLEAN_CHECK=1; shift ;;
    --skip-public-check) SKIP_PUBLIC_CHECK=1; shift ;;
    --skip-playwright) SKIP_PLAYWRIGHT=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
cd "$REPO_ROOT"

if [ ! -f "$SSH_KEY" ]; then
  die "SSH key not found: $SSH_KEY"
fi

SSH_TARGET="${USER_NAME}@${HOST}"
SSH_OPTS=(-i "$SSH_KEY" -o StrictHostKeyChecking=accept-new)
SHORT_SHA="$(git rev-parse --short HEAD)"
FULL_SHA="$(git rev-parse HEAD)"
REMOTE_BRANCH_SHA="$(git rev-parse "origin/$(git branch --show-current)" 2>/dev/null || printf 'unknown')"
RELEASE="$(date +%Y%m%dT%H%M)-${SHORT_SHA}"

run_local_rebuild() {
  if [ "$SKIP_REBUILD" -eq 1 ]; then
    log "skip local rebuild"
    return
  fi

  log "rebuild RAG chunks and site data"
  (cd kb/_build && python3 build_rag.py && python3 build_site_data.py)
  log "build local retrieval index and eval"
  (cd kb/_rag/kb_index && python3 cli.py build && python3 eval_retrieval.py --min-pass-rate "$MIN_PASS_RATE")
  log "check generated JavaScript"
  node --check kb/site/kb_data.js >/dev/null
  awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' kb/site/index.html | node --check - >/dev/null
}

check_tracked_clean() {
  if [ "$SKIP_GIT_CLEAN_CHECK" -eq 1 ]; then
    log "skip tracked git clean check"
    return
  fi
  git diff --quiet || die "tracked files changed; commit regenerated files before deploy"
  git diff --cached --quiet || die "staged changes exist; commit or unstage before deploy"
}

sha256_file() {
  shasum -a 256 "$1" | awk '{print $1}'
}

run_local_rebuild
check_tracked_clean

INDEX_SHA="$(sha256_file kb/site/index.html)"
KB_DATA_SHA="$(sha256_file kb/site/kb_data.js)"
CHUNKS_SHA="$(sha256_file kb/_rag/chunks.jsonl)"

log "release=$RELEASE"
log "commit=$FULL_SHA"
log "remote_branch_sha=$REMOTE_BRANCH_SHA"
log "index_sha256=$INDEX_SHA"
log "kb_data_sha256=$KB_DATA_SHA"
log "chunks_sha256=$CHUNKS_SHA"

if [ "$DRY_RUN" -eq 1 ]; then
  log "dry run complete; no remote changes made"
  exit 0
fi

REMOTE_SCRIPT="$(mktemp)"
TMP_PUBLIC_DIR="$(mktemp -d)"
cleanup() {
  rm -f "$REMOTE_SCRIPT"
  rm -rf "$TMP_PUBLIC_DIR"
}
trap cleanup EXIT

cat >"$REMOTE_SCRIPT" <<'REMOTE_SCRIPT_BODY'
#!/usr/bin/env bash
set -euo pipefail

release="$1"
remote_root="$2"
compose_project="$3"
local_commit="$4"
remote_branch_sha="$5"
index_sha="$6"
kb_data_sha="$7"
chunks_sha="$8"
health_attempts="$9"
health_sleep="${10}"

release_dir="${remote_root}/releases/${release}"
mkdir -p "${release_dir}/kb/site/deploy"
ln -sfn "${remote_root}/shared/.env" "${release_dir}/kb/site/deploy/.env"
test -f "${release_dir}/kb/site/deploy/.env"

cat >"${release_dir}/DEPLOY_MANIFEST.txt" <<EOF
release=${release}
local_commit=${local_commit}
remote_branch_sha=${remote_branch_sha}
deployed_at=$(date -Iseconds)
index_sha256=${index_sha}
kb_data_sha256=${kb_data_sha}
chunks_sha256=${chunks_sha}
compose_project=${compose_project}
compose_files=docker-compose.yml,docker-compose.behind-proxy.yml,docker-compose.vector.yml
EOF

cd "${release_dir}/kb/site/deploy"
docker compose -p "${compose_project}" \
  -f docker-compose.yml \
  -f docker-compose.behind-proxy.yml \
  -f docker-compose.vector.yml \
  config --quiet

ln -sfn "${release_dir}" "${remote_root}/current"
cd "${remote_root}/current/kb/site/deploy"
docker compose -p "${compose_project}" \
  -f docker-compose.yml \
  -f docker-compose.behind-proxy.yml \
  -f docker-compose.vector.yml \
  up -d --build

for i in $(seq 1 "${health_attempts}"); do
  status="$(docker inspect -f '{{.State.Health.Status}}' shopifykb-app 2>/dev/null || printf starting)"
  printf 'app_health[%s]=%s\n' "$i" "$status"
  if [ "$status" = "healthy" ]; then
    break
  fi
  sleep "${health_sleep}"
done

final_status="$(docker inspect -f '{{.State.Health.Status}}' shopifykb-app 2>/dev/null || printf missing)"
test "$final_status" = "healthy"
curl -fsS http://127.0.0.1:8088/api/health >/tmp/shopify_kb_health.json
cat "${remote_root}/current/DEPLOY_MANIFEST.txt"
printf '\nlocal_health='
cat /tmp/shopify_kb_health.json
printf '\n'
REMOTE_SCRIPT_BODY

log "create remote release directory"
ssh "${SSH_OPTS[@]}" "$SSH_TARGET" "mkdir -p '${REMOTE_ROOT}/releases/${RELEASE}/kb'"

log "rsync kb/ to remote release"
rsync -az --delete \
  --exclude '/site/deploy/.env' \
  --exclude '__pycache__/' \
  --exclude '.DS_Store' \
  -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new" \
  kb/ "${SSH_TARGET}:${REMOTE_ROOT}/releases/${RELEASE}/kb/"

REMOTE_SCRIPT_PATH="/tmp/shopify_kb_deploy_${RELEASE}.sh"
log "upload and run remote deploy script"
scp "${SSH_OPTS[@]}" "$REMOTE_SCRIPT" "${SSH_TARGET}:${REMOTE_SCRIPT_PATH}" >/dev/null
ssh "${SSH_OPTS[@]}" "$SSH_TARGET" \
  "bash '${REMOTE_SCRIPT_PATH}' '${RELEASE}' '${REMOTE_ROOT}' '${COMPOSE_PROJECT}' '${FULL_SHA}' '${REMOTE_BRANCH_SHA}' '${INDEX_SHA}' '${KB_DATA_SHA}' '${CHUNKS_SHA}' '${HEALTH_ATTEMPTS}' '${HEALTH_SLEEP}'; rc=\$?; rm -f '${REMOTE_SCRIPT_PATH}'; exit \$rc"

remote_hash() {
  local path="$1"
  ssh "${SSH_OPTS[@]}" "$SSH_TARGET" "shasum -a 256 '${REMOTE_ROOT}/current/kb/${path}' | awk '{print \$1}'"
}

log "verify remote release hashes"
[ "$(remote_hash site/index.html)" = "$INDEX_SHA" ] || die "remote index hash mismatch"
[ "$(remote_hash site/kb_data.js)" = "$KB_DATA_SHA" ] || die "remote kb_data hash mismatch"
[ "$(remote_hash _rag/chunks.jsonl)" = "$CHUNKS_SHA" ] || die "remote chunks hash mismatch"

if [ "$SKIP_PUBLIC_CHECK" -eq 0 ]; then
  log "verify public health and static hashes"
  curl -fsS --max-time 30 "${DOMAIN}/api/health" -o "${TMP_PUBLIC_DIR}/health.json"
  python3 - "${TMP_PUBLIC_DIR}/health.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1]))
assert data.get("ok") is True, data
assert data.get("retriever") is True, data
assert data.get("client_key_supported") is True, data
assert data.get("server_key_set") is False, data
PY
  curl -fsSL --max-time 30 "${DOMAIN}/" -o "${TMP_PUBLIC_DIR}/index.html"
  curl -fsSL --max-time 30 "${DOMAIN}/kb_data.js" -o "${TMP_PUBLIC_DIR}/kb_data.js"
  [ "$(sha256_file "${TMP_PUBLIC_DIR}/index.html")" = "$INDEX_SHA" ] || die "public index hash mismatch"
  [ "$(sha256_file "${TMP_PUBLIC_DIR}/kb_data.js")" = "$KB_DATA_SHA" ] || die "public kb_data hash mismatch"
fi

if [ "$SKIP_PLAYWRIGHT" -eq 0 ]; then
  PWCLI="${CODEX_HOME:-$HOME/.codex}/skills/playwright/scripts/playwright_cli.sh"
  if command -v npx >/dev/null 2>&1 && [ -x "$PWCLI" ]; then
    log "run Playwright config center smoke"
    "$PWCLI" open "${DOMAIN}/#config" --browser chromium >/dev/null
    "$PWCLI" eval "(() => { const text = document.body.innerText; const ok = text.includes('配置') && text.includes('授权') && (text.includes('DeepSeek API Key') || text.includes('页面手动录入')) && text.includes('测试店') && text.includes('人审'); if (!ok) throw new Error('config center smoke did not find required text'); return {title: document.title, url: location.href, bodyChars: text.length}; })()" >/dev/null
    "$PWCLI" resize 390 844 >/dev/null
    "$PWCLI" eval "(() => { const overflowX = document.documentElement.scrollWidth > innerWidth + 1; if (overflowX) throw new Error('mobile horizontal overflow'); return {width: innerWidth, scrollWidth: document.documentElement.scrollWidth}; })()" >/dev/null
    "$PWCLI" console
    rm -rf .playwright-cli
  else
    log "Playwright wrapper not available; skipped browser smoke"
  fi
fi

log "deploy complete: ${RELEASE}"
