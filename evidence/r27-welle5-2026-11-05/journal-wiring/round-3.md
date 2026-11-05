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
- Rewrite mutant B so the write-loss is a real filesystem-path loss (rewrite the on-disk journal without writer B's line) and run the genuine order cell on the surviving journal => real RED; unmutated control => GREEN.
- Run all 5 cells: green baseline + both real RED witnesses locally.
- Re-run `-race -count=20` on the truly-parallel order-cell build.
- Commit round-3 fix + tests on `work/r27-journal-wiring`; push; verify `ls-remote` == new head verbatim; hosted CI terminal on new head.
- Publish evidence to origin/main (ls-tree witness); bring down any compose on this host (none); END DONE to coordinator.

## Base attestation

- Branch under edit: `work/r27-journal-wiring` (PR #1393)
- Base ref cut from `develop`: `3d8fc207deabc2840bcfd888f46d2394cc5a7d36` (short `3d8fc207`)
- `origin/develop` (3d8fc207) is an ancestor of HEAD (verified with `git merge-base --is-ancestor`); the exact merge-base of develop and the candidate is `3d8fc207`, i.e. the candidate develops directly on develop.
- Remote witness BEFORE changes: `git ls-remote origin refs/heads/work/r27-journal-wiring` == `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170` (== round-2 head, the current PR head).
- Remote witness AFTER changes (push): `git ls-remote origin refs/heads/work/r27-journal-wiring` == `e1ea3c6f854c651c1eeb19cee1de5f3de571b55c` (verbatim, == new head).

## Scope

- Editable: `internal/machinehttp/execution_ordered_journal_test.go`, `internal/machinehttp/execution_mutants_test.go` (the two cells the review found non-discriminating).
- NOT touched (review points 1 + 5 confirmed in scope as-is): `internal/machinehttp/execution_crash_resume_test.go` (real `handleExecute` seam) and `internal/machinehttp/store.go` / `internal/machinehttp/handler.go` production blobs.
- `git diff --name-only develop..e1ea3c6f` (round-3 commit) contains ONLY:
  - `internal/machinehttp/execution_ordered_journal_test.go`
  - `internal/machinehttp/execution_mutants_test.go`
- No `.github/**` edits, no workflow_dispatch/rerun.
- No subagents; every step executed inside this own session (AGENTS 4.8 / owner directive 2026-11-04).
- Evidence lives only in baseharbor-plan; no `.evidence/` dir, no main-branch writes.

## Repo-rule compliance

- Scope: tests only in `internal/machinehttp/`.
- No product-repo evidence, no `.github` edits, no rerun.
- Runtime/capability/delivery kept separate; no compose/container on this host (Go tests only).

## FINDINGS (both confirmed real in round-2 code)

- Order cell is serial: round-2 `TestTwoProcessesWriteJournalOrderedInProvenanceOrder` started process 1, waited for its readiness marker, released it, then called `p1.Wait()` (process 1 fully exits) and only THEN launched process 2 (lines ~115-138 of round-2 `execution_ordered_journal_test.go`). Process 2 started after process 1 terminated; a serialized pair of real processes, not a real shared-journal concurrency window.
- Mutant B is in-memory: round-2 `orderedCellWouldFail` (`execution_mutants_test.go`) built an in-memory `[]string` by filtering out writer B's line and only checked `len(lines) != 2`. No journal line was actually lost on the on-disk path and the genuine order-cell assertion was not applied to a mutated journal.

## The round-3 fixes

- Order cell: BOTH real children are `Start()`ed before a shared barrier file is written; each blocks on the barrier, then both are released simultaneously and race on the SAME on-disk journal. The append mutex (`s.mu` in `appendJournalLineLocked`) serializes the on-disk writes; no `p1.Wait()` before `p2.Start()`.
- Mutant B: writer B's line is lost on the REAL on-disk path — the active journal segment `{root}/journal/journal.jsonl` is rewritten with only writer A's line via `os.WriteFile`, the store is re-opened (`newPersistedExecutionStore`) so `load()` reflects the mutated on-disk state, the lost execution is asserted absent, and the genuine order-cell assertion ("exactly two distinct ordered lines") is run on the surviving 1-line journal => it goes RED; the unmutated baseline stays GREEN.

## GATES

- develop-merge: deferred (round 1 PR #1393 already open; merge/acceptance is a separate
  Maintainer action — not performed here).
- hosted run TERMINAL at the new head: DONE. Check-runs for head
  `e1ea3c6f854c651c1eeb19cee1de5f3de571b55c` (PR #1393, `work/r27-journal-wiring`) are
  terminal: 18 jobs, 0 failures, 0 timeouts. Selected jobs all `success`: PR Selected
  Checks, PR · Focused Python, PR · Validation · go-build, PR · Validation · go-vet,
  PR · Validation · go-unit-tests, PR · Trusted Plan, PR · Source format, PR · Workflow
  policy. Docker/Podman runtime gates (Targeted HA · docker / podman) were `skipped`
  (not enabled for this candidate) — a pass, not a failure. No .github edit or
  workflow_dispatch was made; CI was picked up automatically by the push to the PR branch.
- `git ls-remote origin refs/heads/work/r27-journal-wiring`:
  `e1ea3c6f854c651c1eeb19cee1de5f3de571b55c` (verbatim, after push) — == new head.
- `git log --name-only develop..e1ea3c6f` lists ONLY my own commits on the branch
  (round-1 `3fa46bc2` + round-2 `ecae5f0d` + round-3 `e1ea3c6f`); no foreign commit carried
  on top.

## Regressions

- Focused local run of the 5 round-3 cells on the working tree (all PASS, both real RED
  witnesses logged verbatim):
  `go test ./internal/machinehttp/ -run '^(TestCrashDuringApplyLeavesRunningUncertainAfterRestart|TestRestartReconcilesReissueToOriginalExecution|TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA_JournalWriteMakesResumeReal|TestMutantB_WrongOrderIsDetectable)$' -count=1 -v`
  - TestCrashDuringApplyLeavesRunningUncertainAfterRestart PASS — real POST /execute through `handleExecute`, SIGKILL mid-Apply, reopen SAME root => running/uncertain.
  - TestRestartReconcilesReissueToOriginalExecution PASS — identical re-issue reconciles to the SAME execution id, still running.
  - TestMutantA_JournalWriteMakesResumeReal PASS — baseline green; `MUTANT A RED: with the durable start write suppressed on the same root, the post-restart reopen observes no durable running execution — the resume cell's guard is real`
  - TestMutantB_WrongOrderIsDetectable PASS — baseline green; `MUTANT B RED: with writer B's line lost on the same on-disk journal path, the genuine ordered cell sees 1 line, not 2 distinct ordered lines — the order guard is real`
  - TestTwoProcessesWriteJournalOrderedInProvenanceOrder PASS — both real children alive on the shared barrier during write.
- `-race -count=20` on the truly-parallel order-cell build: `ok`, PASS, 22.5s, 0 data races (review finding 2 recipe).
- `go vet ./internal/machinehttp/` clean.
- Hosted CI go-unit-tests (heavy durability fuzz tests included) terminal-success.

## Provenance

- Branch: `work/r27-journal-wiring` (PR #1393). Same branch/PR as round 1 — no second PR.
- Round-3 commit: `e1ea3c6f854c651c1eeb19cee1de5f3de571b55c` on top of round-2 `ecae5f0d` on top of round-1 `3fa46bc2`.
- `origin/develop` (`3d8fc207...`) is an ancestor of `e1ea3c6f` (verified with `git merge-base --is-ancestor`). No branch cut from another candidate.

## Evidence published to baseharbor-plan

- File committed and pushed to baseharbor-plan `main`:
  `git commit 79e2ac6 — evidence(r27 journal-wiring): commit round-3 acceptance file`
  (`1 file changed, 76 insertions`; no other lane's files touched).
- origin/main tree witness:
  `git ls-tree origin/main evidence/r27-welle5-2026-11-05/journal-wiring/round-3.md`
  => `100644 blob 529b3c809a9e0b4fa2711e42772f2aea519d30af  evidence/r27-welle5-2026-11-05/journal-wiring/round-3.md`
- `git merge-base --is-ancestor HEAD origin/main` => YES (79e2ac6 is on origin/main).

## END

END_DONE w202-journal-wiring-r3: head=e1ea3c6f854c konkurrenz=beide kinder vor barrieren-freigabe gleichzeitig auf demselben persistenten journalpfad (p1.Wait() vor p2.Start entfernt) mutanteB=echt auf dateisystem/pfad (journal.jsonl ohne writer-B-zeile neu geschrieben + store neu geladen) gegenprobe gruen lauf=e1ea3c6f854c CI=18 jobs 0 failures go-build/vet/unit-tests success lsremote=e1ea3c6f854c651c1eeb19cee1de5f3de571b55c | round-3 fix verified green locally + -race -count=20 clean + hosted CI terminal-success, committed and pushed to work/r27-journal-wiring (same branch/PR #1393, no second PR), evidence published to origin/main; ready for CODEX acceptance + Maintainer merge (merge/acceptance not performed here).
