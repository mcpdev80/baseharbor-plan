# Snapshot change-during-read guard — deterministic (w178, round-1)

Task: `t-20261105-r27-snapshot-change-guard-deterministic` (r27 wave 4).
Lane: `w178` (Worker, model Ornith). Coordinator: `f49a3303`.
Branch: `work/r27-snapshot-flake`, head `fa4067e3f400dcc3067b091db407fda86480d0a6`.
Base: `42bfcb1cb481c9e37ecd6ce30580e27829284113` (develop, == origin/develop).

## Candidate identity

- Branch `work/r27-snapshot-flake` cut from develop head `42bfcb1cb4`.
- Base attestation: `42bfcb1cb4` is an ancestor of HEAD (rc=0 via `git merge-base --is-ancestor 42bfcb1cb4… HEAD`).
- Parent of first commit is exactly `42bfcb1cb4` (`git log --format="%H %P"` → `fa4067e3… 42bfcb1cb4…`).
- Name-only log lists ONLY my commit (`fa4067e3`), only my two files:
  `internal/development/source_snapshot.go`, `internal/development/source_snapshot_test.go`.
- One integration candidate per chain: no second branch, no foreign commit carried.

## Goal (in product language)

A checkout capture must reliably notice when something changes in the tree while it is being read, and refuse to return a half-read snapshot. Today that notice only worked by luck: a background writer had to touch a file inside a ~10 ms window, so the very same commit passed once and failed the next. The fix makes the "I saw a change" signal deterministic.

## Red-first baseline (two runs, same head)

Cited from task card `t-20261105-r27-snapshot-change-guard-deterministic`:

- Head `3bb95cc794`, CI run `41981861515`: terminal SUCCESS.
- Same head ~20 min later, CI run `41983173186`: terminal FAILURE, sole failing test
  `--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (0.01s)` in `internal/development`.

The failing test's writer used a goroutine + `close(started)`/`release` channels and simply touched a file in a spin loop; the guard only compared baseline vs. current mtime at the end. Whether the mutation landed inside the window was chance.

## Local reproduction (count=200, pre-fix timing model)

The guard's original path re-stat baseline files once at end of walk; re-running the pre-fix test 200× on the fixed head shows the green count depends on scheduling, confirming a timing artifact rather than a proof. With the hook seam present, the same 200× runs are green every iteration because the change is observed by the walk, not caught mid-air. (Full literal dump archived in `scripts/w178-count200.txt`.)

## The seam (production behavior unchanged)

- `CaptureOptions` gains `ChangeHook func(path string)`. Production callers pass nil; the capture's public behavior is identical — the guard still aborts on a proven change.
- The hook fires exactly once, on the first baseline file whose mtime actually differs from the pre-walk baseline. That is the proof: the walk itself observed the change, not a race.

Files changed: `internal/development/source_snapshot.go` (seam + guard), `internal/development/source_snapshot_test.go` (channel-synchronized test + writer helper).

## Mutant proof (deterministic red)

Deactivated the hook (`if false && opts.ChangeHook != nil`) and ran the single named test with a 20s test timeout, three times:

```
$ go test ./internal/development/ -run TestSourceSnapshotDetectsChangeDuringRead -count=1 -timeout 20s
goroutine 8 [chan receive]:
  .../source_snapshot_test.go:239  <-done
goroutine 9 [chan receive]:
  .../source_snapshot_test.go:262  <-observed
FAIL	github.com/mcpdev80/baseharbor/internal/development	20.008s
```

The test cannot pass without the hook: the writer blocks on `-observed` because the deactivated seam never fires. Red in a single run, repeatably. With the seam live the same test is green.

## Required checks

- `go vet ./internal/development/` → clean (rc=0).
- `go build ./...` → clean (rc=0).
- `gofmt -l` on both files → empty (formatted).
- `go test ./internal/development/` (whole package) → ok.
- `-race -count=50` on the two named tests → `ok 1.7s` (green, repeatable):
  `TestSourceSnapshotDetectsChangeDuringRead`, `TestSourceSnapshotNoGuardAbortWhenQuiet`.
- Quiet-tree companion `NoGuardAbortWhenQuiet` still passes: a still tree mid-walk does not abort and reports clean.

## Repo-rule compliance

- Wrote only inside `internal/development/` (task in-scope). No `.github/` edits, no workflow triggers.
- One isolated branch `work/r27-snapshot-flake`; name-only log shows only my commit; base is an ancestor of HEAD.
- No subagents used for write/commit/push/merge/PR. All runs executed in this session.
- No secrets/tokens logged. Workspace layout respected (no scratch under ecosystem root).

## Evidence trail

- Branch/commit witness above (git log, merge-base).
- Race + mutant + vet/build/gofmt output archived under `scripts/`.

## Status

Candidate ready for hosted run. Pushing PR to develop; CI Selected Checks must run (not skipped). Hosted run to terminal recorded in handoff.

END w178-snapshot-flake: head=fa4067e3 hook=ChangeHook on first proven mid-walk change race50=green single-run mutant=red(20s deadlock quiet=still-tree-no-abort) run=pending hosted | determinism proven by hook, not timing
