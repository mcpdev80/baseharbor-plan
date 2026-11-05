# CODEX-REVIEW — PR #1387

- Candidate: `fa4067e3f400dcc3067b091db407fda86480d0a6`
- Base: `develop` at `42bfcb1cb481c9e37ecd6ce30580e27829284113`.
- PR #1387: OPEN, not draft, base `develop`, head exact candidate.
- `git ls-remote origin refs/heads/develop refs/heads/work/r27-snapshot-flake`: develop `42bfcb1cb481c9e37ecd6ce30580e27829284113`; candidate `fa4067e3f400dcc3067b091db407fda86480d0a6`.
- Name-only: `internal/development/source_snapshot.go`, `internal/development/source_snapshot_test.go`.
- Run `42010882741`: completed success on exact candidate.

## Independent checks

I ran the two named tests myself at the exact candidate:

```text
go test -race ./internal/development -run 'TestSourceSnapshotDetectsChangeDuringRead|TestSourceSnapshotNoGuardAbortWhenQuiet' -count=50
ok github.com/mcpdev80/baseharbor/internal/development 1.798s
```

The quiet companion also passed independently with `-race -count=20` (`ok`, 1.063s). It asserts the stable tree is returned without a guard abort.

I mutated the candidate by disabling the callback at `internal/development/source_snapshot.go:327`, then ran only `TestSourceSnapshotDetectsChangeDuringRead` once with `-timeout 3s`. It failed by panicking with `test timed out after 3s`; goroutines were stuck at the test's `<-done` (`source_snapshot_test.go:239`) and writer's `<-observed` (`:262`). Restored the candidate and verified no source diff remained. This is bounded only by the generic outer test timeout and gives a hang trace, not an assertion stating which required observation failed.

The guard still compares the baseline mtime with the current mtime and returns the same `SourceSnapshotError` when a change is observed. The new hook is only set by this test in the repository; nil-hook capture behavior is preserved. The PR's two-file write-set leaves all other capture paths/files untouched (the only changed paths are listed above). The guard still aborts on the changed capture; quiet capture remains accepted.

Historical red-baseline runs required by the mission:

- `41981861515`: completed success on `3bb95cc794a9c2aa167a149618065ec998e9d812`.
- `41983173186`: completed failure on that same older SHA, with `TestSourceSnapshotDetectsChangeDuringRead` as the reported failure (timing flake).
- Current required run `42010882741` is terminal success on the reviewed SHA.

## Verdict: REJECT

The deterministic ChangeHook fixes the race flake, and the control path is sound, but the test's disabled-hook mutant hangs until a broad test timeout. That is not a clear, bounded assertion of the missing observation. A deadlock makes the failure slower and less diagnostic, and can occupy test resources until the package timeout. The reported red mutant therefore does not meet the quality bar for a deterministic regression test.

## Recipe

- **File:** `internal/development/source_snapshot_test.go`, in `TestSourceSnapshotDetectsChangeDuringRead` and `writer`.
- **Change:** make the writer's wait for `observed` bounded with a short explicit test-level deadline and return a typed/result signal to the test; have the test assert that the hook observed the exact mutated baseline path and that capture returned the expected change-during-capture error. Ensure all goroutines exit on success and failure (for example, cancellation/release channel selected alongside the observation). Do not make the production guard wait on the hook.
- **Test requirement:** unchanged candidate passes both named tests under `-race -count=50`; quiet companion passes `-race -count=20`; disabling the hook fails the focused test once with an explicit assertion naming the missing observation, without a test-timeout panic or blocked goroutine.
- **Stop criterion:** stop and reject if the mutant can hang past the test's local bound, if the reported error is only the generic package timeout, if the assertion does not prove the expected path was observed, or if the guard aborts a quiet capture.

No PR action was taken.
