# Snapshot change-during-read guard — EREIGNIS semantics (w187, round-3)

Task: `t-20261105-r27-snapshot-change-guard-deterministic` (r27 wave 4).
Lane: `w187` (Worker, model Ornith-Laptop). Coordinator: `f49a3303`.
Branch: `work/r27-snapshot-flake` (PR #1387), remote head `27cf86c3396b3886bbbb9b0a4b23be57ce82fd93`.

## Base attestation (Owner requirement)

- Current remote head (pre-this-round commit): `27cf86c3396b3886bbbb9b0a4b23be57ce82fd93` (other session's round-2 evidence act on the same card).
- Develop refresh merged: `a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3`.
- Attestation: `git merge-base --is-ancestor a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3 HEAD` → rc=0 (a53c10a7 is an ancestor of my HEAD after the merge).
- Attestation: `git merge-base --is-ancestor 27cf86c3396 HEAD` → rc=0 (current remote head is an ancestor of my HEAD).
- FINAL ls-remote witness: `work/r27-snapshot-flake` -> `e2d87906a5103db132e0d86e935387680426245b`.
- My code commit `6471c6a0` is exactly one commit stacked ON TOP of remote head `27cf86c3396`, touching only the two card files.

## Goal (in product language)

The source-snapshot capture must *prove* it saw a change during the read, not merely time-box it. The current guard fired a `ChangeHook("__walk_started__")` at walk start and then relied on a **final mtime comparison** of every baseline path after the walk finished. On CI-hosted filesystems that mtime-delta proof does not reliably fire, so the hosted run 42050483534 went terminal FAILURE. Round-3 rebuilds the hook on EREIGNIS semantics: the capture path itself emits a change event the instant the walk observes a baseline path diverge *during the walk*, and the test waits on that event (deterministic channel barrier) — mtime stays only as an extra layer, never as the sole proof.

## The change (round-3 only)

Two card files, write-set = `internal/development/source_snapshot.go` + `source_snapshot_test.go`. No `.github`, no subagents, no second branch.

- `source_snapshot.go` (production, EREIGNIS seam inside the capture walk): walk-start `ChangeHook("__walk_started__")` retained; new per-file identity baseline `baselineIdent` (path -> mtime ns); **two-pass recheck inside the production walk** — after reading each regular file the walk re-stats the path and, on the first baseline divergence observed during the walk, emits `ChangeHook(relSlash)` (the event a caller waits on) and aborts; capture path and tests share the same seam (no test-only switch). One extra stat per regular file (runtime footnote, not a gate break). Removed dead helpers `baselineFiles` / `treeFileModTime`.
- `source_snapshot_test.go`: `TestSourceSnapshotDetectsChangeDuringRead` now waits boundedly on the *emitted event* (deterministic channel barrier); mtime remains only the extra layer.

## Before / on CI (hosted, the acceptance criterion)

- Before — run `42050483534` (terminal FAILURE, head before this round):
  `15:07:43 --- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.01s)`
  `source_snapshot_test.go:247: change-during-read hook never fired within the local bound`
- After — run `42057573429` (terminal SUCCESS, head `e2d87906`): `go-unit-tests` completed/success; also success: `go-vet`, `go-build`, `PR Selected Checks`, `PR · Source format`, `PR · Trusted Plan`, `Workflow policy`, `PR · Focused Python`. (Runtime gates skipped by the selected-checks mapping; the unit-tests gate is the acceptance criterion this round.)

## Mutant proof (fail-fast, named, wörtlich)

Disabled the divergence proof in the real source, ran the single named test 3x:

```
--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.00s)
    source_snapshot_test.go:247: change-during-read hook never fired within the local bound
FAIL
	github.com/mcpdev80/baseharbor/internal/development	5.009s
```
Runs 2 and 3 identical: named sentinel `errSnapshotHookDidNotFire` at the 5s test-local bound each — fail-fast, NOT the generic 10-minute timeout. Production restored after (live proof PASS 0.007s; `grep -c MUTANT` == 0). Quiet tree `-race -count=20` green. Full witness in `scripts/mutant-proof-r3.txt`.

## Required checks

- `go build ./internal/development/` → clean (rc=0). Whole module `-buildvcs=false ./...` → rc=0.
- `go vet ./...` (whole module) → clean (rc=0).
- `gofmt -l internal/development/` → empty (formatted).
- `-race -count=50` on `TestSourceSnapshotDetectsChangeDuringRead` → `ok 1.464s` (green).
- `-race -count=20` on `TestSourceSnapshotNoGuardAbortWhenQuiet` → `ok 1.063s` (green, quiet leader).
- Whole package `go test ./internal/development/` → `ok 15.651s`.
- Whole module `go test ./...` → clean (rc=0).
- Note: `-race` build runs against `/tmp` tmpfs; GOTMPDIR set to `/home/marcel/dev/baseharbor-ecosystem/.gotmp` when /tmpfs was under memory pressure (linker output-mapping `disk quota exceeded` without it).

## Divergence handled this round (shared branch)

- The remote head of `work/r27-snapshot-flake` moved from `d5ff9bc7` to `27cf86c3396` while I was away: a second worker on the **same card** wrote only the round-2 evidence act (`.evidence/.../round-2.md` publish + revert) — disjoint write-set from my two Go card files, confirmed (my event-barrier code was NOT on the remote before rebasing).
- Recovery per AGENTS §5.5 + mission: did NOT force-push over the other session; reset my branch to the current remote head `27cf86c3396`, re-created ONE clean commit `6471c6a0` (my code) on top of it, then merged develop `a53c10a7` (ancestor rc=0; no overlap with my write-set). Net: my code is exactly one commit stacked on the remote head, only my two card files changed vs that head.
- No second branch invented; single integration candidate per chain retained.

## Repo-rule compliance

- Write-set: only the two card files changed (Go). No `.github/` edits, no workflow triggers, no reruns.
- One working branch `work/r27-snapshot-flake` (PR #1387); shared-branch divergence handled per AGENTS §5.5; single integration candidate retained.
- No subagents. All runs executed in this session. Hosted run watched to terminal myself (§4.6).
- No secrets/tokens logged. Workspace layout respected (worktree under /tmp, caches under ecosystem/.gotmp/.gomodcache; no scratch under the ecosystem root beyond pre-existing artifacts).

## Evidence trail

- Branch/commit witness above (git log, merge-base, ls-remote).
- Mutant + race + vet/build/output archived under `scripts/mutant-proof-r3.txt`.
- Hosted run `42057573429` terminal SUCCESS witnessed via `gh run view … --json`.
- Before/after CI lines from runs `42050483534` (FAIL) and `42057573429` (SUCCESS).

## Status

Round-3 candidate complete: event-barrier change-during-read guard (EREIGNIS) inside the production capture walk; the post-walk mtime-only proof that failed on CI is gone. Hosted run `42057573429` terminal SUCCESS at head `e2d87906` (go-unit-tests + go-vet + go-build + PR Selected Checks green); local `-race -count=50` green, quiet leader green, mutant fails fast with the named sentinel.

## CI

- Hosted run `42057573429` → terminal SUCCESS @ `e2d87906` (go-unit-tests / go-vet / go-build / PR Selected Checks / Source format / Trusted Plan / Workflow policy all success).
- Before: run `42050483534` → terminal FAILURE `TestSourceSnapshotDetectsChangeDuringRead (5.01s) … change-during-read hook never fired within the local bound`.

## END

END w187-snapshot-flake-r3: head=e2d87906a510 hook=EREIGNIS-barre ChangeHook(relSlash) beim walk-internen baseline-divergenzevents (production-walk, kein test-only switch) hosted=42057573429 TERMINAL SUCCESS go-unit-tests+go-vet+go-build+PR-Selected-Checks gruen race50=gruen(1.464s) mutante=3x rot benannter sentinel errSnapshotHookDidNotFire@5s quiet20=gruen lsremote=e2d87906a510 | shared-branch-divergence (andere session schrieb round-2 evidence act) per AGENTS 5.5 geloest: reset auf 27cf86c + single commit 6471c6a0 + develop a53c10a7 merge (ancestor rc=0), ein kandidat pro kette
