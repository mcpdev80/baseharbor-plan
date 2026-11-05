# CODEX-REVIEW — snapshot change guard, PR #1387 round 5

- Review date: 2026-11-05
- Verdict: **REJECT** — the endcheck-removed test is red, but the assertion is not discriminating: it also goes red when no writer mutation occurs.
- Candidate: `0298871895c19ed2844751ac9a4a141c7250d2a3`
- Base: `develop` `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`; `git merge-base --is-ancestor origin/develop <candidate>` returned rc=0.
- PR #1387 is open, branch `work/r27-snapshot-flake`. `git ls-remote origin refs/heads/work/r27-snapshot-flake` returned exactly `0298871895c19ed2844751ac9a4a141c7250d2a3`.
- Hosted run [42106254196](https://github.com/mcpdev80/baseharbor/actions/runs/42106254196): terminal `completed / success` at the exact candidate.
- `git diff --name-only origin/develop...<candidate>`: exactly `internal/development/source_snapshot.go` and `internal/development/source_snapshot_test.go`.

## Checks performed

1. Race-50: `go test -race -count=50 ./internal/development -run '^(TestSourceSnapshotDetectsChangeDuringRead|TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation)$'` — `ok github.com/mcpdev80/baseharbor/internal/development 2.165s`.
2. Quiet-20: `go test -race -count=20 ./internal/development -run '^TestSourceSnapshotNoGuardAbortWhenQuiet$'` — `ok github.com/mcpdev80/baseharbor/internal/development 1.096s`.
3. Hook-removed mutant, isolated worktree, single run of `TestSourceSnapshotDetectsChangeDuringRead` — red after 5.01s, literal sentinel: `change-during-read hook never fired within the local bound`.
4. Final-endcheck-removed mutant, isolated worktree, single run of `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation` — red, literal assertion: `source_snapshot_test.go: expected final baseline-path verification to abort the capture on a late mutation of an already-visited file`.
5. **Discriminating-control failure:** in the isolated endcheck-mutant worktree I additionally replaced the writer goroutine with a no-op that only receives `firstRead` and never changes `aaa.bin`. The same test still went red with the exact same final-baseline assertion. Therefore the literal red from check 4 does not prove that the endcheck caught a late write; the test can fail when there was no write at all.

## Review details

- The test signals `firstRead` from `ChangeHook` after `aaa.bin` passed the per-file guard. The callback sets `sawRead` and sends to a buffered channel, then returns. The writer waits on that channel and loops `os.Chtimes` until `CaptureSource` returns. There is no writer-to-walk acknowledgement that at least one mutation actually completed before the final sweep (or before a mutant returns). `sawRead` only records the walk event; it is not evidence of a write. The final assertion checks `err != nil`, not a writer mutation witness.
- This explains why the endcheck mutant is red even with the writer disabled: the mutant returns a successful snapshot (`err == nil`) and the test fails its `err == nil` assertion regardless of whether any file changed. The test does not currently distinguish “endcheck caught a late mutation” from “test never performed a mutation.”
- The writer uses a channel receive as a start gate and no sleep-polling, but the required two-sided barrier is incomplete. A real write-confirmation signal must be observed before the capture can proceed beyond the consumed-path event, and the test must fail with a separate named sentinel if no mutation was made.
- Production guard review: Layer 1 uses a fresh `os.Lstat` after file read and calls the hook only on a detected mismatch; Layer 2 `verifyFinalBaseline` remains after the walk. `ChangeHook` is supplied only by the two tests in this repository. `SourceSnapshot` and `snapshotFile` fields and the file append/blob shape are unchanged; the production path adds only the consumed-path bookkeeping and has no hook callback when `ChangeHook == nil`.

## Correction recipe

1. Make the late-mutation test prove a real changed identity before `CaptureSource` can continue from the consumed-path event. Use a test-local channel acknowledgement or an equivalent synchronous test barrier after `aaa.bin` passed Layer 1; record/verify the actual mutation and return a distinct named failure if it did not happen. Do not rely on filler count or scheduling.
2. With that barrier in place, rerun the baseline regression and quiet test; then remove `verifyFinalBaseline` in an isolated mutant and show that the now-proven late mutation yields the named final-sweep assertion. Keep the hook-removed mutant as its own isolated run with the local-bound sentinel.
3. Repeat race-50 and quiet-20, restore the unmutated candidate, and verify terminal hosted success at the resulting exact SHA.

The review used isolated worktrees for both mutations and the no-write control. Candidate source and PR were not changed. No PR action was performed.

## Remote publication witness

- Before this receipt amendment, `git ls-tree origin/main -- evidence/r27-welle4-2026-11-05/snapshot-flake/review-1387e.md` returned `100644 blob 226790c80ed44be6f0fbe705e27ff39a53dcb1d2 evidence/r27-welle4-2026-11-05/snapshot-flake/review-1387e.md` at `origin/main` `fdbd402e80af7131d321e36f84b5cb40a0b6a5d0`.
- The receipt amendment was committed and pushed; final `fetch origin main` and `ls-tree origin/main` verified the updated akte path on the remote.
