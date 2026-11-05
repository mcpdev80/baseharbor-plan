# CODEX-REVIEW — snapshot change guard, PR #1387 round 6

- Review timestamp: 2026-11-05 23:20 UTC.
- Reviewer: Codex, GPT-6-Luna channel, review pane `codeman-ab08e19f`.
- Verdict: **ACCEPT** for the exact candidate below.
- Task: `t-20261105-r27-snapshot-change-guard-deterministic` (owner `coord-welle5`, worker lane `w200`, status `review`).
- Candidate: `d0e0bdc6e84772453156c86606770da1ea9986b2`.
- PR #1387: OPEN, base `develop`, branch `work/r27-snapshot-flake`; GitHub head equals the candidate.
- Remote witnesses: `git ls-remote origin refs/heads/work/r27-snapshot-flake` returned `d0e0bdc6e84772453156c86606770da1ea9986b2`; develop is `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`. `git merge-base --is-ancestor origin/develop <candidate>` returned rc=0.
- Dependencies `t-20261017-release-0-4-27-updates` and `t-20261018-r27-candidate-pack` both have `kanban_status: closed`.
- PR diff against develop contains only `internal/development/source_snapshot.go` and `internal/development/source_snapshot_test.go`.
- Candidate blobs: `source_snapshot.go` `186988d261a2626ad62f560953ef4431680983e5`; `source_snapshot_test.go` `0762389ff111d22884dc19bc14610fc9e78dec02`.

## Acceptance checks performed independently

1. Race-50, including the during-read regression and the late-mutation/Layer-2 regression:
   `GOCACHE=/tmp/codex-r1387f-gocache go test -race -count=50 ./internal/development -run '^(TestSourceSnapshotDetectsChangeDuringRead|TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation)$'`
   Result: `ok github.com/mcpdev80/baseharbor/internal/development 1.880s`.
2. Quiet-tree companion:
   `GOCACHE=/tmp/codex-r1387f-gocache go test -race -count=20 ./internal/development -run '^TestSourceSnapshotNoGuardAbortWhenQuiet$'`
   Result: `ok .../internal/development 1.054s`.
3. Discrimination direction 1, isolated Layer-1 mutant (removed only the `MutationAcked(relSlash)` acknowledgement): `TestSourceSnapshotDetectsChangeDuringRead` failed at 5.01s with the named sentinel `change-during-read MutationAcked never fired on the mutated path within the local bound` (exit 1).
4. Discrimination direction 2, isolated Layer-2 mutant (removed only the `verifyFinalBaseline` call): `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation` failed at 5.01s with the same named acknowledgement-miss sentinel (exit 1).
5. Counterprobe, unchanged candidate, no writer mutation:
   `GOCACHE=/tmp/codex-r1387f-gocache go test -race -count=20 ./internal/development -run '^TestSourceSnapshotFinalBaselineNoMutationStaysGreen$'`
   Result: `ok .../internal/development 1.201s`.

The two mutants were applied only in separate temporary worktrees under `/tmp`; no product branch or candidate file was changed. The late-mutation test waits until `aaa.bin` has passed Layer 1, changes its mtime, and blocks until Layer 2 acknowledges that exact path. The separate no-mutation control stays green. This demonstrates both mutant directions and a discriminating unchanged control, rather than relying on timing or a generic timeout.

## Code and hosted-gate review

- Layer 1 takes a fresh `os.Lstat` after reading a regular file, compares its mtime with the walk-start baseline, and aborts on divergence. The synchronous `MutationAcked` callback runs only on that observed divergence.
- Layer 2 (`verifyFinalBaseline`) remains after the walk and rechecks baseline paths; its synchronous acknowledgement names the exact changed path before the capture aborts.
- `CaptureOptions.MutationAcked` is nil at every production call site found in the repository; the repository-wide Go search found no call sites outside the snapshot implementation and its tests. With nil hooks, the public snapshot metadata and capture path retain their existing behavior. The two-file write set leaves other capture and application paths untouched.
- Hosted run [42125295757](https://github.com/mcpdev80/baseharbor/actions/runs/42125295757) is terminal `completed / success` on the exact candidate. `PR Selected Checks` completed successfully and its check-run app id is `15368`. Required jobs `PR · Source format`, `PR · Trusted Plan`, `Workflow policy`, `PR · Focused Python`, `PR · Validation · go-build`, `PR · Validation · go-unit-tests`, `PR · Validation · go-vet`, and `PR Selected Checks` succeeded. Optional unrelated HA/release/runtime jobs were skipped.
- PR state rechecked: OPEN, mergeable, exact head. No PR action was performed.

## repo-rule compliance

Read-only candidate review plus temporary isolated mutation experiments only. No source file, branch, PR, task card, or generated planning view was edited. Only this review receipt is being published to the planning repository; unrelated pre-existing working-tree changes are not staged.
