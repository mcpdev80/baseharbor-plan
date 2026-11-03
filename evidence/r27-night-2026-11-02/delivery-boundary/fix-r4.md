# FIX r5 — PR #1333 / t-20261018-r27-delivery-boundary

Lane: w8-delivery-r7 | Coordinator: f49a3303 | Coord tick base: 4e8e67d8 (develop Vorfahr)
Reviewer: Codex GPT-6, re-review review-1333e2.md, head 4e8e67d877980eda8333c0dd4659e0c0c4eb4457
Date: 2026-11-03

## PLAN

1. Fix point 2 (first-save conflict semantics) in `internal/deployment/deployment_store.go`
2. Add explicit first-save caller-conflict tests
3. Point 3: align EN/DE ADR 0022 + delivery-provider-v1 spec to record-save guarantee
4. End: merge origin/develop; verify `grep -E '^(\.github|scripts/|cmd/)'` diff is empty
5. Tests: `TMPDIR=/tmp go test ./internal/deployment ./internal/delivery` + build/vet
6. Push FF, ls-remote, write this evidence, post END to f49a3303

## Work

### Point 2 — conflict semantics (fixed)

The candidate evaluated the guard on the caller-supplied `record.Observed.Conflict` on
first save: the caller's `Conflict` was only cleared/overwritten when `previousExists`.
On a first save `previousExists==false`, so a caller-supplied `Conflict=true` was honoured
and caused a false rejection — exactly what review point 2 called out.

Fix (minimal, in `SaveDeploymentRecord`): on a first save the caller-supplied
`Observed.Conflict` is now explicitly discarded (`guardRecord.Observed.Conflict = false`),
and on a subsequent save the persisted/previous value governs (`= previous.Observed.Conflict`).
`refuseOneWriterMutation` always evaluates only `guardRecord`, which carries the
authoritative (previous) conflict and never the caller value.

Semantics now: `conflict = previous.conflict OR store-own-revelation`; caller field
ignored at both first and subsequent saves.

Tests added to `internal/deployment/one_writer_guard_test.go`:
- `TestFirstSaveCallerConflictTruePasses` — first save, caller Conflict=true, baseharbor owner => must pass (no rejection from caller field).
- `TestFirstSaveCallerConflictFalsePasses` — first save, caller Conflict=false => must pass.
- `TestFirstSaveCallerConflictDiscardedUnderStoredFalse` — first save caller=true persists Conflict=false (store cannot invent a conflict).
- `TestFirstSaveDelegatedCallerConflictPasses` — delegated first save with caller Conflict=true must pass.

### Point 3 — EN/DE deferral (verified + aligned)

review-1333e2.md point 3 flagged lines 34/50 (EN/DE ADR) as still saying "BaseHarbor
refuses apply/observe and rejects competing reconcilers before apply". Checked the current
candidate (4e8e67d8) — the ADR and spec already defer active reconciliation to record-save.
Verified current wording; corrected residual "refuses to apply or observe" phrasing to
"refuses to persist an apply or observation at record save" in both EN and DE, and added the
explicit deferred-dependency sentence to the DE ADR so EN and DE carry identical meaning.

## repo-rule compliance

- Scope: only `internal/deployment/deployment_store.go` (1-line guard fix) + one test file
  (`one_writer_guard_test.go`) + two ADR files and one spec file. No cmd/, no scripts/, no
  .github/. No new files. Matches task decision (store hook + one regression test file allowed).
- End-of-task guard: merged origin/develop into worktree before final diff; `grep -E '^(\.github|scripts/|cmd/)'` on the branch diff is empty.

## Tests

- `XDG_DATA_HOME=/tmp/bh1333e2-data XDG_CONFIG_HOME=/tmp/bh1333e2-config TMPDIR=/tmp GOCACHE=/tmp/bh-r7-gocache go test ./internal/deployment ./internal/delivery` => PASS
- `go build ./... && go vet ./internal/deployment ./internal/delivery` => clean

## End-of-task

- merged origin/develop into worktree before final diff; `grep -E '^(\.github|scripts/|cmd/)'` on the branch diff is empty.
- pushed far-forward, confirmed SHA via `git ls-remote`, posted END to f49a3303.
