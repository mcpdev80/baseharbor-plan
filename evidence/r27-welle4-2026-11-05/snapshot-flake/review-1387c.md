# CODEX-REVIEW — PR #1387 round 3

## Candidate and scope

- PR: [#1387](https://github.com/mcpdev80/baseharbor/pull/1387)
- Reviewed head: `e2d87906a5103db132e0d86e935387680426245b`
- PR state at review: open; base `develop`; candidate head matched the mission.
- Reviewed files: `internal/development/source_snapshot.go` and `internal/development/source_snapshot_test.go`.
- Mission: `coordinator/missions/codex-r1387c.txt`.

## Verification evidence

- Hosted run [42057573429](https://github.com/mcpdev80/baseharbor/actions/runs/42057573429) completed `success` at the exact reviewed head. Its `PR Selected Checks` job completed `success`.
- Local exact-candidate command: `GOCACHE=/dev/shm/gocache-review1387c TMPDIR=/dev/shm/gotmp-review1387c go test -race -count=50 ./internal/development -run '^(TestSourceSnapshotDetectsChangeDuringRead|TestSourceSnapshotNoGuardAbortWhenQuiet)$'` — `ok github.com/mcpdev80/baseharbor/internal/development 1.534s`.
- The first invocation failed before tests ran because the temporary build area hit `disk quota exceeded`; rerunning with the command-local `/dev/shm` cache and temporary directory completed successfully.
- Hook-disabled mutant, isolated in `/tmp/review1387c-mutant`, command `go test -race -count=3 ./internal/development -run '^TestSourceSnapshotDetectsChangeDuringRead$'` — all three invocations failed at `source_snapshot_test.go:247` with the named sentinel `change-during-read hook never fired within the local bound` (5.01s per invocation), rather than a generic Go timeout.
- The quiet companion was included in the 50-count race run, exceeding the requested race-20 coverage.
- Read-only capture-path review: `CaptureSource` still routes regular-file bytes through `readFileBounded`, keeps ignore/default-exclusion and symlink handling in the walk, and does not change the `snapshotFile` blob metadata shape. No production call site supplies `ChangeHook`.

## Finding — blocking

The new in-walk check only compares a regular file's mtime when the walk reaches that file (`source_snapshot.go`, around lines 313–320). The prior post-walk sweep over every baseline path was removed. A writer can therefore modify a file after that file has passed its per-file check while the walk is still processing later files; the current code returns a snapshot instead of aborting. This weakens the existing change-during-capture guard and violates the capture-behavior acceptance criterion.

The event hook also receives the synthetic `__walk_started__` value before any change is observed (`source_snapshot.go`, around lines 282–287), despite its option comment promising a callback only for an observed identity difference. The test uses that callback as a start signal, so the event-observation seam and walk-start synchronization are conflated.

## Verdict and correction recipe

**REJECT.** Keep the in-walk event notification for deterministic observation, but restore a final baseline-path verification before returning the snapshot. Add a regression that changes an already-visited file while a later file is still being captured and asserts the capture aborts. Separate walk-start synchronization from the documented change hook so the hook only reports a real changed path. Then rerun the two named tests under `-race -count=50`, the quiet companion under `-race -count=20`, the hook-disabled mutant three times with the named sentinel, and hosted checks at the resulting exact head. Stop if any required check is red or if the final sweep does not detect the late mutation.

## Repo-rule compliance

This was a read-only, SHA-exact review. No product source, PR, or branch was changed. The only write is this requested review record. No PR action was taken.
