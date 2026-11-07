#!/usr/bin/env bash
# Smoke test for card t-20261106-r27-remote-up-podman-owner-missing (0427-117):
# pure-client remote app up on the podman family should resolve the deployment
# owner (no ErrDeploymentOwnerMissing) and reach doctor health.
# Isolated HOME under /tmp; disjoint target; run on baha-podman-2 only.
set -uo pipefail
export HOME=/tmp/bh-smoke-home-0427-117
rm -rf "$HOME"; mkdir -p "$HOME"
BAHA=/tmp/baha-0427-117
rm -rf /tmp/bh-smoke-repo
mkdir -p /tmp/bh-smoke-repo/workload
printf 'version: "3.8"\nservices:\n  web:\n    image: nginx:latest\n' > /tmp/bh-smoke-repo/workload/docker-compose.yaml
TGT="w0427-117-smoke3"
APP="workload"

cd /tmp/bh-smoke-repo/workload
echo "=== target create (podman, local access) ==="
$BAHA target create "$TGT" --runtime-provider podman --access local --access-provider local --reference local || { echo "TARGET_CREATE_FAIL"; exit 3; }

echo "=== app init (detect compose workload) ==="
$BAHA app init --workload-source compose:docker-compose.yaml || { echo "APP_INIT_FAIL"; exit 3; }

echo "=== app apply --confirm-candidate --yes (owner seam) ==="
$BAHA app apply "$APP" --target "$TGT" --confirm-candidate --yes 2>&1 || { echo "APP_APPLY_FAIL"; exit 4; }

echo "=== app up ==="
$BAHA app up "$APP" --target "$TGT" 2>&1 || { echo "APP_UP_FAIL"; exit 4; }

echo "=== app doctor ==="
$BAHA app doctor "$APP" --target "$TGT" 2>&1 || true

echo "=== cleanup ==="
$BAHA app destroy "$APP" --target "$TGT" --yes 2>&1 || true
$BAHA target remove "$TGT" --yes 2>&1 || true
