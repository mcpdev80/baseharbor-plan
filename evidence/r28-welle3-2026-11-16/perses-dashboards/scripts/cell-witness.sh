#!/usr/bin/env bash
# 0428-082 round-5 cell witness (baha-docker, rootless docker 29.8.1).
# Proves Luna batch18 unproof (b): a deploy-path-materialized Prometheus
# answering the dashboard's real /api/v1/query through the PRODUCT
# verification entry point (metricsprovider.PersesInfraDashboardAvailabilityAt
# — the call cmd/baha/app_status_result.go makes from `baha status --json` —
# and VerifyPersesInfraDashboardAt itself). No hand-made fake provider state:
# every file under the state root comes from `baha app apply/up`.
#
# Usage (on the cell host):
#   BASE=$HOME/lanes/w082-r5 SHA=<40-hex head> bash cell-witness.sh
# Prereq: $BASE/repo = clone of mcpdev80/baseharbor with the SHA fetchable,
#         $BASE/cellwitness_test.go = the perses_infra_cell-tagged witness
#         (internal/metrics/perses_infra_cell_witness_test.go), ORAS on PATH.
# Idempotent teardown on EXIT. Prints machine-checkable CELL/RESULT lines.
set -euo pipefail

SHA="${SHA:-dda073da4a495f61d2f754ae37a0262225f68df8}"
BASE="${BASE:-$HOME/lanes/w082-r5}"
REPO="$BASE/repo"
ZONE="$BASE/witness"
export PATH="$HOME/.local/bin:$PATH"

log() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*"; }

BOOT="$(cat "$BASE/last-boot" 2>/dev/null || true)"
teardown() {
  local rc=$?
  set +e
  export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock
  export BASEHARBOR_STATE_DIR="$ZONE/state" XDG_CONFIG_HOME="$ZONE/config"
  [ -n "${BOOT:-}" ] && export BASEHARBOR_TARGET="$BOOT"
  cd "$ZONE/app" 2>/dev/null && "$BASE/baha-built" app destroy --yes >/dev/null 2>&1
  cd "$ZONE" && "$BASE/baha-built" destroy --yes >/dev/null 2>&1
  docker ps -aq --filter "name=w082r5" | xargs -r docker rm -f >/dev/null 2>&1
  docker network ls -q --filter "name=w082r5" | xargs -r docker network rm >/dev/null 2>&1
  docker volume ls -q --filter "name=w082r5" | xargs -r docker volume rm >/dev/null 2>&1
  log "teardown done (exit $rc); containers now: $(docker ps -a --format '{{.Names}}' | wc -l)"
  exit $rc
}
trap teardown EXIT

log "before: $(docker ps -a --format '{{.Names}}' | wc -l) containers"
rm -rf "$ZONE"; mkdir -p "$ZONE/state" "$ZONE/app" "$ZONE/config"
export XDG_CONFIG_HOME="$ZONE/config"

cd "$REPO"
git cat-file -e "$SHA" || { log "SHA $SHA not fetched"; exit 1; }
git checkout -q --detach "$SHA"
log "repo HEAD: $(git rev-parse HEAD)"

log "build baha (deploy-path CLI) at the verified SHA"
go build -o "$BASE/baha-built" ./cmd/baha

log "trust plane: fresh bootstrap target + control-plane-only Core (precedent: cmd/baha/runtime_integration_test_support_test.go)"
BOOT="w082r5-ci-$(date +%s)"
export BASEHARBOR_STATE_DIR="$ZONE/state"
export BASEHARBOR_METRICS_ENABLED=true
export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock
# One management Core per engine: remove leftovers of this zone by name.
docker ps -aq --filter "name=w082r5" | xargs -r docker rm -f >/dev/null 2>&1
echo "$BOOT" > "$BASE/last-boot"
"$BASE/baha-built" target create "$BOOT" --runtime-provider docker --access local --access-provider local --reference local --default 2>&1 | tail -1
"$BASE/baha-built" up --control-plane-only --yes 2>&1 | tail -3
log "control plane Core up on target $BOOT"
export BASEHARBOR_TARGET="$BOOT"

cat > "$ZONE/app/compose.yaml" <<'YAML'
services:
  api:
    image: alpine:3.22
    command:
      - sh
      - -ec
      - |
        i=0
        while true; do
          { printf "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\napplication_info 1\nprocess_scrape_witness_counter %d\n" "$i"; sleep 1; } | nc -ll -p 8080
          i=$((i+1))
        done
YAML
cat > "$ZONE/app/baseharbor.yaml" <<'YAML'
version: 1
app:
  name: w082r5-witness
  environment: dev
metrics:
  sources:
    - name: application
      service: api
      port: 8080
      path: /metrics
services:
  observability:
    management_ui: true
    perses: true
YAML

cd "$ZONE/app"
log "baha app init (identity; authored manifest unchanged)"
"$BASE/baha-built" app init 2>&1 | tail -2
log "baha app plan (operator reviews this concrete impact before consent)"
"$BASE/baha-built" app plan 2>&1 | tail -20 || true
log "baha app apply (both consent gates: pty impact ack + candidate digest)"
ptyrun() { printf '%s\n' "yes" | script -qec "$1" /dev/null; }
digest=$(ptyrun "'$BASE/baha-built' app apply --skip-memory-preflight" 2>&1 | grep -oE 'confirm-candidate [0-9a-f]+' | tail -1 | awk '{print $2}') || true
[ -n "${digest:-}" ] || { log "apply printed no candidate digest"; exit 1; }
log "binding candidate consent digest $digest"
ptyrun "'$BASE/baha-built' app apply --confirm-candidate $digest --skip-memory-preflight" 2>&1 | tail -6 | tee "$ZONE/apply.out"
grep -q 'Error' "$ZONE/apply.out" && { log "apply still failing"; exit 1; }
log "baha app up"
BASEHARBOR_METRICS_ENABLED=true "$BASE/baha-built" app up 2>&1 | tail -4
log "give the scrape loop time to produce samples"
sleep 75

log "provider state (deploy path materialized):"
find "$BASEHARBOR_STATE_DIR" -path '*providers/prometheus*' \
  \( -name runtime.env -o -name runtime-sources.json -o -name compose.yaml -o -name ca.pem \) \
  -printf '%p %s\n' 2>/dev/null | sort
log "raw provider state snapshot (before teardown):"
{ echo "runtime-sources.json:"; cat "$BASEHARBOR_STATE_DIR/targets/$BOOT/providers/prometheus/shared/runtime-sources.json" 2>/dev/null;
  echo; echo "targets dir:"; ls "$BASEHARBOR_STATE_DIR/targets/$BOOT/providers/prometheus/shared/targets/" 2>/dev/null;
  echo "targets content:"; cat "$BASEHARBOR_STATE_DIR/targets/$BOOT/providers/prometheus/shared/targets/"*.json 2>/dev/null; } > "$ZONE/state.out" 2>&1 || true
cat "$ZONE/state.out"
log "prometheus containers:"
docker ps --format '{{.Names}} {{.Image}}' | grep -iE 'prom' || true

log "witness run (product verification path):"
cp "$BASE/cellwitness_test.go" "$REPO/internal/metrics/perses_infra_cell_witness_test.go"
( cd "$REPO" && BASEHARBOR_STATE_DIR="$BASEHARBOR_STATE_DIR" BASEHARBOR_METRICS_ENABLED=true \
  BASEHARBOR_TARGET="$BOOT" BAHA_CELL_MANIFEST="$ZONE/app/baseharbor.yaml" \
  go test -count=1 -tags perses_infra_cell -run 'TestPersesInfraDashboardCellWitness' -v ./internal/metrics 2>&1 ) \
  | tee "$ZONE/witness.out" | grep -E 'CELL|^--- (PASS|FAIL)|^(ok|FAIL)' | head -40

log "witness.out saved at $ZONE/witness.out"
