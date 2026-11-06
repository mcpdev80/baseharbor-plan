#!/usr/bin/env bash
# Causal mutation harness for the round-4 management-host fix.
#
# Proves that the NEW production lock-lifetime line changed by this fix is what
# the new attach-contended regression guards. Records three SHA-256 levels:
#   L0  before mutation (production file, fix in place)
#   L1  under mutation (new bootstrap-lock bridge removed -> gap restored)
#   L2  after exact restoration
#
# The new regression TestManagementHostAttachContendedByBootstrapServer must be
# GREEN at L0, RED under the mutation at L1, and GREEN again at L2.
#
# The mutation is a MINIMAL, surgical edit of the NEW production line only:
# the attach path's `bunlock, berr := AcquireBootstrapLock(m.stateRoot)` guard
# is replaced so the bootstrap lock is NO LONGER checked on the attach path
# (exactly the round-3 behaviour). This is NOT a mutation of the pre-existing
# bootstrap guard in the missing/empty-root branch.
#
# Usage: mutation_mgmt_host.sh <worktree>
set -uo pipefail
WT="${1:?usage: mutation_mgmt_host.sh <worktree>}"
cd "$WT" || exit 2

F=internal/coreinstallation/management_host.go
TEST='TestManagementHostAttachContendedByBootstrapServer'

mutate() {
  # Replace the two new lines with a no-op bridge: the bootstrap lock is no
  # longer acquired on the attach path (round-3 gap restored).
  python3 - "$F" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
old = '''	bunlock, berr := AcquireBootstrapLock(m.stateRoot)
	if berr != nil {
		return false, nil, ErrManagementHostBootstrapContended
	}'''
new = '''	// MUTATION: bootstrap lock no longer checked on the attach path (round-3 gap restored).
	_ = m.stateRoot'''
assert old in s, "target production lines not found; aborting (do not proceed with a different candidate)"
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
PY
}

restore() {
  python3 - "$F" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
new = '''	// MUTATION: bootstrap lock no longer checked on the attach path (round-3 gap restored).
	_ = m.stateRoot'''
old = '''	bunlock, berr := AcquireBootstrapLock(m.stateRoot)
	if berr != nil {
		return false, nil, ErrManagementHostBootstrapContended
	}'''
assert new in s, "mutation marker not found; aborting"
s = s.replace(new, old, 1)
open(p, "w", encoding="utf-8").write(s)
PY
}

level_hash() { sha256sum "$F" | awk '{print $1}'; }

echo "=== L0: before mutation (fix in place) ==="
H0=$(level_hash)
echo "hash: $H0"
if go test ./internal/coreinstallation/ -run "^${TEST}$" -count=1 2>&1 | grep -q '^ok'; then echo "L0 test: GREEN"; else echo "L0 test: UNEXPECTED RED"; fi

echo "=== L1: under mutation ==="
mutate
H1=$(level_hash)
echo "hash: $H1"
if go test ./internal/coreinstallation/ -run "^${TEST}$" -count=1 2>&1 | grep -q '^ok'; then echo "L1 test: UNEXPECTED GREEN (mutation did not break the regression)"; else echo "L1 test: RED (mutation broke it - causal)"; fi

echo "=== L2: after exact restoration ==="
restore
H2=$(level_hash)
echo "hash: $H2"
if go test ./internal/coreinstallation/ -run "^${TEST}$" -count=1 2>&1 | grep -q '^ok'; then echo "L2 test: GREEN (restored)"; else echo "L2 test: RED after restore"; fi

echo "=== SUMMARY ==="
echo "L0 $H0"
echo "L1 $H1"
echo "L2 $H2"
[ "$H0" = "$H2" ] && echo "RESTORED-EXACT: L0==L2" || echo "RESTORE MISMATCH"
