# Round 3 evidence — journal wiring (card t-20261018-r27, lane w202)

## Summary

Round 2 candidate `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170` (PR #1393) was REJECTed
by CODEX review `review-1393a.md`: the order cell was serial (process 2 launched
after process 1 fully exited) and mutant B lost a write in an in-memory slice
instead of on the real filesystem path. Round 3 fixes exactly those two findings:

- The order cell now launches BOTH real child processes before a shared barrier,
  so both are alive and writing the SAME on-disk journal during a real concurrency
  window (no `p1.Wait()` before process 2 starts).
- Mutant B now loses a real journal line on the on-disk path (the append-only file
  is rewritten without writer B's line) and the genuine order cell is run against
  the surviving journal => it goes RED; the unmutated control stays GREEN.

The production `handleExecute` / crash-resume seam and `store.go` are untouched
(round-2 points 1 + 5 confirmed: crash/handleExecute not in scope).

## PLAN

- Read mission + review-1393a.md + target files; confirm both findings are real and crash/handleExecute are out of scope.
- Establish green baseline: focused local run of the 5 cells on head ecae5f0d.
- Rewrite the order cell so both child processes are launched before the barrier release and write the same on-disk journal while both are alive.
- Rewrite mutant B so the write-loss is a real filesystem-path loss (delete a real journal line) and run the genuine order cell on the surviving journal => real RED; unmutated control => GREEN.
- Run all 5 cells: green baseline + both real RED witnesses locally.
- Re-run `-race -count=20` on the truly-parallel order-cell build.
- Commit round-3 fix + tests on `work/r27-journal-wiring`; push; verify `ls-remote` == new head verbatim; hosted CI terminal on new head.
- Publish evidence to origin/main (ls-tree witness); bring down any compose on this host (none); END DONE to coordinator.

## Base attestation

- Branch under edit: `work/r27-journal-wiring` (PR #1393)
- Base ref cut from `develop`: `3d8fc207deabc2840bcfd888f46d2394cc5a7d36` (short `3d8fc207`)
- `origin/develop` (3d8fc207) is an ancestor of HEAD (verified with `git merge-base --is-ancestor`); the exact merge-base of develop and the candidate is `3d8fc207`, i.e. the candidate develops directly on develop.
- Remote witness BEFORE changes: `git ls-remote origin refs/heads/work/r27-journal-wiring` == `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170` (== round-2 head, the current PR head).

## Scope

- Editable: `internal/machinehttp/execution_ordered_journal_test.go`, `internal/machinehttp/execution_mutants_test.go` (the two cells the review found non-discriminating).
- NOT touched (review points 1 + 5 confirmed in scope as-is): `internal/machinehttp/execution_crash_resume_test.go` (real `handleExecute` seam) and `internal/machinehttp/store.go` / `internal/machinehttp/handler.go` production blobs.
- No `.github/**` edits, no workflow_dispatch/rerun.
- No subagents; every step executed inside this own session (AGENTS 4.8 / owner directive 2026-11-04).
- Evidence lives only in baseharbor-plan; no `.evidence/` dir, no main-branch writes.

## Repo-rule compliance

- Scope: tests only in `internal/machinehttp/`.
- No product-repo evidence, no `.github` edits, no rerun.
- Runtime/capability/delivery kept separate; no compose/container on this host (Go tests only).

## Focused local run (green baseline)

Environment: dedicated `GOCACHE`/`TMPDIR` under the worktree (the shared `/tmp` tmpfs
is full cluster-wide with other lanes' scratch; this avoids the quota without touching
another lane's files).

Command:
`go test ./internal/machinehttp/ -run '^(TestCrashDuringApplyLeavesRunningUncertainAfterRestart|TestRestartReconcilesReissueToOriginalExecution|TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA_JournalWriteMakesResumeReal|TestMutantB_WrongOrderIsDetectable)$' -count=1 -v`

Result (all PASS, matches round-2 green):

- TestCrashDuringApplyLeavesRunningUncertainAfterRestart PASS — real POST /execute through `handleExecute`, SIGKILL mid-Apply, reopen SAME root => running/uncertain.
- TestRestartReconcilesReissueToOriginalExecution PASS — identical re-issue reconciles to the SAME execution id, still running.
- TestMutantA_JournalWriteMakesResumeReal PASS — baseline green; MUTANT A RED witness logged.
- TestMutantB_WrongOrderIsDetectable PASS — baseline green; MUTANT B RED witness logged.
- TestTwoProcessesWriteJournalOrderedInProvenanceOrder PASS — (round-2 serial build; see rewrite below).

## FINDINGS (both confirmed real in round-2 code)

- Order cell is serial: round-2 `TestTwoProcessesWriteJournalOrderedInProvenanceOrder` starts process 1, waits for its readiness marker, releases it, then calls `p1.Wait()` (process 1 fully exits) and only THEN launches process 2 (lines ~115-138 of round-2 `execution_ordered_journal_test.go`). Process 2 starts after process 1 has terminated; this is a serialized pair of real processes, not a real shared-journal concurrency window.
- Mutant B is in-memory: round-2 `orderedCellWouldFail` (`execution_mutants_test.go`) builds an in-memory `[]string` by filtering out writer B's line and only checks `len(lines) != 2`. No journal line is actually lost on the on-disk path and the genuine order-cell assertion is not applied to a mutated journal.

## END

END_PENDING w202-journal-wiring-r3: working on head ecae5f0d; round-3 fix in progress (order cell made truly concurrent, mutant B made a real filesystem write-loss).
