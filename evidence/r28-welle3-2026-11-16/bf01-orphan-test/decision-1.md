# 0428-096 · BF-01 orphan test — decision + verification (coord-authored, evidence-only)

## Decision

DROP the test (no restore of the `StateRoot*` chain). bf-03 supersedes bf-01's
state-root-owned target-selection chain; keeping a bf-01-only isolation test would
pin a dead contract. Source finding: live-verify round-4 ## FINDINGS item 2
(evidence/r28-welle1-2026-11-15/live-verify/round-4.md:213).

## Verification witnesses (fetched 2026-11-16)

- `git ls-tree origin/develop -- cmd/baha/target_selection_state_dir_isolation_test.go` => EMPTY (absent on develop).
- Sweep over ALL persistent lane refs (refs/heads/lane*, w*, refs/heads welle-family): file ABSENT on every branch (loop of ls-tree checks, zero hits).
- History: introduced 18c922e37, last touched 13e096fc6; throwaway union already carried the drop as `0760469d0` (orphan-test drop) per live-verify round-4 line 6.
- => The orphan is not present in any promotable ref; the card's outcome (no unreachable leftover test on any integration path) is already TRUE in the world. No product PR required.

## Consequence for future unions

If a union/stack branch recreates the bf-01 chain, it must NOT recreate the test file;
bf-03 semantics (organization-state placement) are covered by their own tests.
