# CODEX-REVIEW — snapshot change guard, PR #1400 round 7

- Review date: 2026-11-06.
- Reviewer: Codex, review pane `codeman-ab08e19f`.
- Verdict: **REJECT** for exact candidate `1c84f5fe43c9ec59dd464915133fedc44901c107`.
- Task: `t-20261105-r27-snapshot-change-guard-deterministic`.
- PR #1400 is OPEN; API head equals the reviewed candidate; base is `develop`.
- Role: CODEX-REVIEW, read-only. No PR action.

## Remote identity and integration

`git ls-remote origin refs/heads/develop refs/heads/work/r27-flake-r7` returned:

- develop: `ea656d1fcfce9ee14145a8dfaffb9e993fd29497`
- candidate: `1c84f5fe43c9ec59dd464915133fedc44901c107`

`git merge-base --is-ancestor origin/develop HEAD` returned **rc=1**. The current develop tip includes the recently merged #1395 commit and is not an ancestor of this PR candidate. This misses the mission's required develop-ancestor gate; PR API reported `mergeStateStatus=UNSTABLE` at review time. The candidate's name-only diff against the merge base contains exactly:

- `internal/development/source_snapshot.go`
- `internal/development/source_snapshot_test.go`

The write set is limited to those two files, but the branch must first integrate the current develop tip and receive fresh exact-head checks.

## Causal acknowledgement and local cells

The round-7 code introduces `MutationPending` and the bounded wait in `afterMutationWait` / `waitForMutation`. When that callback returns a live channel, the implementation waits for the writer's close and re-stats; the deterministic test writer closes it immediately after `os.Chtimes`. The changed test makes the acknowledgement channel buffered and wires the pending channel for the two mutation cells.

Independent run:

```text
GOTMPDIR=<workspace temp> GOCACHE=<workspace .gocache> go test -p 2 ./internal/development -race -run '^(TestSourceSnapshotDetectsChangeDuringRead|TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation)$' -count=20
ok github.com/mcpdev80/baseharbor/internal/development 1.401s
```

The initial attempt using the read-only default Go cache failed before compilation; the workspace-cache run above completed successfully. The temporary build directory was removed afterward.

The empty-hook quiet cell also passes:

```text
GOTMPDIR=<workspace temp> GOCACHE=<workspace .gocache> go test -p 2 ./internal/development -run '^TestSourceSnapshotNoGuardAbortWhenQuiet$' -count=1
ok github.com/mcpdev80/baseharbor/internal/development 0.006s
```

## Blocking nil-hook defect

`CaptureSource` first records the fresh per-file `os.Lstat` result in `nowNano` (around `source_snapshot.go:328-330`), then unconditionally overwrites it with `afterMutationWait(...)` (around line 335). `afterMutationWait` returns the original baseline `identity` when `MutationPending == nil` (around lines 407-410). Since ordinary production `CaptureOptions` leaves this test-only hook unset, the fresh observation is discarded and the Layer-1 per-file divergence check becomes inert for the default nil-hook path. `TestSourceSnapshotNoGuardAbortWhenQuiet` proves only that an unchanged nil-hook capture does not panic; it does not test that a nil-hook capture still observes a changed path.

The earlier per-file `Lstat` result must be preserved when the hook is nil (and when it returns nil), while the causal wait may replace it only after its own valid re-stat. Add a regression that changes a baseline path at the per-file barrier with `MutationPending` nil and verifies capture rejects the changed tree. Re-run the race-20 matrix and required hosted gates after the fix and develop integration.

## Hosted evidence

Both requested attempts are independently visible in GitHub Actions at the exact head `1c84f5fe43c9ec59dd464915133fedc44901c107`:

- Run `42172734295`, attempt 1: terminal success; `PR · Validation · go-unit-tests` job `127744286927` and `PR Selected Checks` job `127746880410` succeeded.
- Run `42172734295`, attempt 2: terminal success; `PR · Validation · go-unit-tests` job `127749031811` and `PR Selected Checks` job `127751724606` succeeded.

A separate later same-head run `42175476921` was still in progress (`go-unit-tests` job `127752911235`) when checked; it is not counted as either requested green. The `validate`/compose-family issue documented as foreign in `round-7.md` was not attributed to this candidate.

## Review conclusion and correction recipe

The causal wait is exercised by both local race cells, both requested hosted attempts are green, and the quiet nil-hook cell does not panic. Acceptance is still blocked by (1) the nil-hook overwrite, which disables the existing Layer-1 observation for default production options, and (2) current `develop` not being an ancestor of the candidate. Preserve the fresh `Lstat` value on nil-hook paths, add the nil-hook mutation regression, integrate `ea656d1fcfce` into the PR branch, and rerun the exact-head gates before review.

## repo-rule compliance

Read-only review of PR #1400. No candidate source, branch, task note, or generated planning view was changed. Only this review receipt is being added to Planning `main`; unrelated pre-existing local edits to `releases/v0.4.27.md` and `roadmap/cards.md` were left unstaged and untouched.
