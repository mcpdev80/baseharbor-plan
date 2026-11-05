# CODEX-REVIEW — PR #1387 round 4

## Candidate and scope

- PR: [#1387](https://github.com/mcpdev80/baseharbor/pull/1387)
- Reviewed head: `d21badc6f4a202b5ff81022e0039adc095e079e3`
- Base: `develop` at `10e8d646f0136c62fde0f7b84968a42ae572ba68`.
- PR state: open; PR head, branch `ls-remote`, and mission SHA matched.
- Name-only diff: `internal/development/source_snapshot.go`, `internal/development/source_snapshot_test.go`.
- Reviewer session: `ab08e19f-3b4e-4bfd-80ce-8b0876941aad` (`codex-luna-ch`).

## Verification

- Hosted run [42083071514](https://github.com/mcpdev80/baseharbor/actions/runs/42083071514) completed `success` at the exact reviewed head. `PR Selected Checks`, `go-unit-tests`, build, and vet were successful.
- Local candidate command: `go test -race -count=50 ./internal/development -run '^(TestSourceSnapshotDetectsChangeDuringRead|TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation)$'` — `ok github.com/mcpdev80/baseharbor/internal/development 1.919s`.
- Quiet companion: `go test -race -count=20 ./internal/development -run '^TestSourceSnapshotNoGuardAbortWhenQuiet$'` — `ok github.com/mcpdev80/baseharbor/internal/development 1.058s`.
- Hook-removed mutant, single run: `TestSourceSnapshotDetectsChangeDuringRead` failed at `source_snapshot_test.go:248` after 5.00s with the named sentinel `change-during-read hook never fired within the local bound`.
- Final-endcheck-removed mutant, single run: `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation` **passed** (`ok ... 0.009s`). The mutant was made in an isolated scratch worktree and removed there after the run. The regression therefore does not prove that the post-walk endcheck is present.
- The production walk now obtains the current per-file identity with `os.Lstat(filePath)` after reading, rather than relying on `entry.Info()`. Inspection of the installed Go `os` implementation confirmed that a `DirEntry` can carry cached `FileInfo` from enumeration; an explicit Lstat is the correct fresh metadata read for this guard.
- Capture output/blob behavior review: the PR changes only the guard and its tests. `SourceSnapshot` fields and the regular-file path through `readFileBounded` and `snapshotFile` assembly remain unchanged.

## Finding — blocking

The final-baseline regression is also satisfied by the in-walk Lstat guard: its writer mutates `first.bin` continuously from before `CaptureSource` starts, so the per-file check can abort the capture before `verifyFinalBaseline` runs. Removing the final sweep leaves the test green, as the requested mutant confirms. This fails the mission's required named red proof for the endcheck and does not pin the late-mutation gap independently.

## Verdict and correction recipe

**REJECT.** Keep the production Lstat correction and both guard layers. Make the late-mutation regression synchronize the writer so it changes an already-visited file only after that file's per-file Lstat check has completed and while a later file remains in the walk. Use a named, sweep-specific failure signal so the endcheck-removed mutant fails while the full implementation passes. Then repeat the late-mutation test and its mutant once, along with the specified race-50, quiet-20, and exact-head hosted checks. Stop if disabling `verifyFinalBaseline` still leaves the test green.

## Repo-rule compliance

Read-only, SHA-exact review. No product source, branch, or PR was changed. The candidate and both mutants were run in isolated worktrees. This requested review record is the only write. No PR action was taken.
