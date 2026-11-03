# Evidence: w9-delivery-r8 — PR #1333 docs-only ADR 0022 fix

**Role:** Worker (Lane w9-delivery-r8). Coord f49a3303.
**Task:** t-20261018-r27-delivery-boundary (micro doc-only).
**Base:** `3d8b6b7cc77252ba5a86132a99c68cd3abc11af5` (work/r27-delivery-boundary).

## END LINE
- LANE w9-delivery-r8: DONE — ADR 0022 DE/EN record-save fix committed on PR #1333.

## PLAN
1. Own worktree on work/r27-delivery-boundary (base 3d8b6b7c) — done
2. Read mission + review-1333f; confirm DE/EN bug scope, drop point-3 write-set (task note resolves it) — done
3. Fix DE duplicated/incomplete sentence (lines 34-38) to one complete record-save sentence — in progress
4. Align EN section 2 + consequences to record-save behavior (sinngleich)
5. EN/DE consistency check + docs/link check
6. One commit, only docs/de/decisions/0022-* + docs/decisions/0022-*
7. Send: merge origin/develop; diff grep -E '^(.github|scripts/|cmd/)' empty; tests green
8. push, ls-remote, write evidence, END an f49a3303

## repo-rule compliance
- Mission scope (t-20261018-r27-delivery-boundary): docs-only, one commit touching only ADR 0022 markdown. No code, no merge of unrelated changes.
- review-1333f point 2 recipe followed: fix duplicated sentence + conditional/negation, align EN/DE ADR sections and consequences to record-save behavior, retain named authority/state-owner deferral.
- review-1333f point 3 (write-set): explicitly obsolete per task note coordinator note (2026-11-03, r1333f) — "authorized one regression file covers preferences_retention_test.go alongside one_writer_guard_test.go". Out of my doc-only scope; dropped as instructed by mission ("kartennote regression-file scope wurde SOEBEN publiziert — damit erledigt").
- STOP per mission: nothing else changed — no code, no merge.

## Fix details
- DE docs/de/decisions/0022.md lines 34-38: duplicated/incomplete sentence `genau ein Besitzer in portable Intent ausdrückbar ist. Der Guard sitzt in` / `Besitzer in portable Intent ausdrückbar ist. Der Guard sitzt in` collapsed to ONE complete record-save sentence with the condition retained.
- DE consequences line 51: "vor dem Anwenden" → record-save aligned (was asserting rejected before apply, contradicting deferred active-reconciler observation).
- EN docs/decisions/0022.md section 2 + consequences aligned EN/DE (sinngleich): record-save behavior, deferred active-reconciler observation retained.

## Send / CI
- Merge: origin/develop up-to-date (already at head).
- Diff gate: `git diff --name-only origin/work/r27-delivery-boundary HEAD` → only the two ADR 0022 markdown files; `grep -E '^(\.github|scripts/|cmd/)'` empty. PASS.
- Tests: `go test ./internal/deployment ./internal/delivery` → both `ok` (green, unchanged). GOCACHE=/tmp/bh-w9-gocache2.
- Push: `git push origin work/r27-delivery-boundary` → `3d8b6b7c..6df94554`. FF.
- ls-remote: `6df9455491a5e791fd141aa33ab36c7e50379cdc refs/heads/work/r27-delivery-boundary`; PR #1333 head `6df94554...` confirmed; PR OPEN, MERGEABLE, base=develop, no reviewDecision.
- Note: PR #1333 also carries other lanes' product code (w7-delivery-r6) — out of my doc-only lane scope. Did not merge the whole PR. My doc commit is delivered to the correct PR head.
- push FF, ls-remote, no run-logs.

## Notes
- PR #1333 mergeStateStatus=UNSTABLE (GitHub field; open review request) but mergeable, reviewDecision empty.
- review-1333f point 3 (write-set / two test files) obsolete per task-note coordinator note (2026-11-03 r1333f) — outside doc-only scope; dropped as instructed.
