# CODEX-REVIEW — journal wiring, PR #1393 round 3

- Review timestamp: 2026-11-05 23:51 UTC.
- Reviewer: Codex, GPT-6-Luna channel, review pane `codeman-ab08e19f`.
- Verdict: **ACCEPT** for exact candidate `67efc581614a8af89bd4245204604bc70e528c13`.
- Task: `t-20261018-r27-journal-wiring`, owner `coord-welle5` (lane w202), status `review`.
- PR #1393 is OPEN, base `develop`, branch `work/r27-journal-wiring`; PR head and remote branch both equal the candidate.
- Dependencies `t-20261017-release-0-4-27-updates`, `t-20261018-r27-execution-journal`, `t-20261018-r27-mutation-lock`, and `t-20261022-r27-ci-authority` are accepted.
- Current `develop` is `21d8d05cf1acf04729077e05eb350fcd3bb018ed`. The candidate carries the accepted `a0441838` develop merge and is six commits behind / four commits ahead of current develop. Per the round-3 mission, this base drift belongs to the later merge stage; no develop integration or PR action was performed during this read-only review.
- Hosted run [42130410241](https://github.com/mcpdev80/baseharbor/actions/runs/42130410241) is terminal `completed / success` on the exact candidate. `PR Selected Checks` completed successfully from GitHub Actions app `15368`.
- `git ls-remote origin refs/heads/work/r27-journal-wiring` returned exactly `67efc581614a8af89bd4245204604bc70e528c13`.
- `git diff --name-status origin/develop...<candidate>` contains exactly three expected journal test files: `execution_crash_resume_test.go`, `execution_mutants_test.go`, and `execution_ordered_journal_test.go`.

## Rechecks of the two round-2 findings

1. **Concurrent child processes:** The parent starts process 1 and process 2 before writing the shared barrier file, and does not wait for process 1 before starting process 2. Both child modes use the same persistent journal root and block on that barrier before creating their record. After release the parent waits for both. There is no serial `p1.Wait()` / then `p2.Start()` sequence from round 2. The real two-process cell is green in the focused run below and under race-20.
2. **Mutant B is a filesystem mutation:** The test first establishes two distinct durable writer records on disk. It then rewrites the actual `journal/journal.jsonl` without writer B's line, reopens the store from the same root, confirms writer B is absent and the file has one line, and records the expected red from the one-line detector. This is not an in-memory-only slice edit. The unchanged two-process cell remains green as the control.

## Independent local execution

In an isolated worktree at the candidate SHA, with only the Go build cache redirected to `/tmp`:

`GOCACHE=/tmp/codex-r1393b-gocache go test ./internal/machinehttp/ -run '^(TestCrashDuringApplyLeavesRunningUncertainAfterRestart|TestRestartReconcilesReissueToOriginalExecution|TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA_JournalWriteMakesResumeReal|TestMutantB_WrongOrderIsDetectable)$' -count=1 -v`

Result: all five tests passed. The crash/reissue cells passed through their HTTP/handler restart path. The test log recorded both witnesses:

- `MUTANT A RED: with the durable start write suppressed on the same root, the post-restart reopen observes no durable running execution — the resume cell's guard is real`
- `MUTANT B RED: with writer B's line lost on the same on-disk journal path, the genuine ordered cell sees 1 line, not 2 distinct ordered lines — the order guard is real`

The unmutated real two-process cell passed in this same focused run, providing the green counterprobe. Repeated independently:

`GOCACHE=/tmp/codex-r1393b-gocache go test -race -count=20 ./internal/machinehttp/ -run '^TestTwoProcessesWriteJournalOrderedInProvenanceOrder$'`

Result: `ok github.com/mcpdev80/baseharbor/internal/machinehttp 21.261s`.

## Crash cell and #1373 production blobs

- `execution_crash_resume_test.go` candidate blob is `64b3e1e76a3afa6b1e5a51c01b44477836da1440`, unchanged from round-2 head `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170`.
- Production `store.go` candidate and current develop blob: `b87cca57c180b4ef79c5ee0db544ae02410872eb`.
- Production `handler.go` candidate and current develop blob: `060397d92ca550b7a7c323416a2828c1b6c85a2b`.
- The round-3 changes do not alter the #1373 journal store or handler production blobs; the changed journal paths are regression tests.
- Candidate test blobs: `execution_ordered_journal_test.go` `41b7e2f9e2786b56cb949cda2569dc5585786665`; `execution_mutants_test.go` `08cce16d00bd4402f87872a74ada0409e9515707`.

## repo-rule compliance

Read-only review only. Local checks ran in an isolated temporary worktree; no candidate file, branch, task card, PR, or production code was changed. This receipt is the only file to be added to planning `main`; existing uncommitted planning changes remain untouched. No merge was performed.
