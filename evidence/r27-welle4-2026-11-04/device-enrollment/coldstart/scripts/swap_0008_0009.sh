#!/usr/bin/env bash
# 0008/0009 swap mutation probe (review-1371c R2).
#
# Copies the baseharbor repo to a disposable workdir, swaps the numeric
# prefixes 0008 <-> 0009 in BOTH the forward and .down.sql migration files,
# runs TestMigrationRollbackOwnsOnlyLatestChange against the swapped list, and
# prints the before/after test result. The test must follow the swapped list and
# stay GREEN: this proves the head-stage assertion reads owned artifacts from the
# selected stage's .down.sql rather than hardcoding the workstation tables.
#
# Usage: scripts/swap_0008_0009.sh <BASEHARBOR_WORKTREE> <DST_WORKDIR>
set -euo pipefail

SRC="${1:?pass baseharbor worktree as $1}"
DST="${2:?pass destination workdir as $2}"
DB_URL="${BASEHARBOR_TEST_DATABASE_URL:?BASEHARBOR_TEST_DATABASE_URL must be set}"

rm -rf "$DST"
mkdir -p "$DST"
# Copy the whole repo so the test binary compiles against the identical module
# graph. Destination lives on the large backing disk (/dev/sda1), not the small
# /tmp tmpfs, so the copy does not overflow temporary storage.
cp -a "$SRC/." "$DST/"

SWAP="$DST/internal/database/migrations"
# Swap 0008 <-> 0009 in BOTH forward and .down.sql pairs. Use an unused staging
# prefix (ZZZZ) so neither source name collides with the other during the loop.
for f in "$SWAP"/*; do
  case "$(basename "$f")" in
    0008_*) mv "$f" "${f/0008_/ZZZZ_}" ;;
    0009_*) mv "$f" "${f/0009_/0008_}" ;;
  esac
done
# The former 0008 files (now ZZZZ) become the new 0009.
for f in "$SWAP"/ZZZZ_*; do
  mv "$f" "${f/ZZZZ_/0009_}"
done

echo "=== swapped filenames ==="
ls -1 "$SWAP" | grep -E '^(0008|0009)_' || true

cd "$DST"
echo "=== SWAPPED-RUN test output (expect GREEN) ==="
GOCACHE="/home/marcel/dev/baseharbor-ecosystem/workers/.w146-cache/gocache" \
GOMODCACHE="/home/marcel/dev/baseharbor-ecosystem/workers/.w146-cache/gomodcache" \
TMPDIR="/home/marcel/dev/baseharbor-ecosystem/workers/.w146-cache/tmp" \
BASEHARBOR_TEST_DATABASE_URL="$DB_URL" \
go test ./internal/database -run 'TestMigrationRollbackOwnsOnlyLatestChange' -count=1 -v 2>&1 | grep -v '^go: download'
echo "SWAP_TEST_EXIT=${PIPESTATUS[0]}"
