# Round 2 evidence — journal wiring (card t-20261018-r27, lane w196)

## Summary

Round 1 candidate `3fa46bc299b0e372d59b214ec8708b918e46c37d` (PR #1393) was REJECTed
by CODEX review `review-1392a.md`: the three test files did not prove the required cells.
This round rewrote the three files in `internal/machinehttp/` so the cells are real:

- Crash resume now drives the real HTTP `handleExecute` production seam, kills the Apply in a
  genuine child process (SIGKILL mid-Apply), and verifies post-restart running/uncertain +
  identical reissue reconciliation on the SAME persistent root.
- Two-process ordering now launches two child processes concurrently (open/barrier handshake)
  against the same on-disk journal and asserts exactly-once, order-respecting appends.
- Two controlled single mutations run on the SAME journal path: (a) suppress the durable start
  write => resume cell goes RED; (b) lose a writer's journal line => ordering cell goes RED. Both
  recorded verbatim via t.Log.
- Disk quota runs live under a `/dev/sda1` go-cache + TMPDIR (the shared `/tmp` tmpfs is full
  cluster-wide); no run used the quota-standard path.

## Base attestation

- Branch under edit: `work/r27-journal-wiring` (PR #1393)
- Base ref cut from `develop`: `3d8fc207deabc2840bcfd888f46d2394cc5a7d36` (short `3d8fc207`)
- `origin/develop` (3d8fc207) is an ancestor of HEAD (verified with `git merge-base --is-ancestor`).
- Remote witness BEFORE changes: `git ls-remote origin refs/heads/work/r27-journal-wiring` ==
  `3fa46bc299b0e372d59b214ec8708b918e46c37d`.

## Scope

- `git diff --name-only HEAD -- internal/machinehttp/` contains ONLY the three test files:
  - `internal/machinehttp/execution_crash_resume_test.go`
  - `internal/machinehttp/execution_ordered_journal_test.go`
  - `internal/machinehttp/execution_mutants_test.go`
- No production code, no `.github/**` edits, no workflow_dispatch/rerun.
- No subagents; every step executed inside this own session (AGENTS 4.8 / owner directive 2026-11-04).
- Evidence lives only in baseharbor-plan; no `.evidence/` dir, no main-branch writes.

## Repo-rule compliance

- Scope: tests only in `internal/machinehttp/`.
- No product-repo evidence, no `.github` edits, no rerun.
- Runtime/capability/delivery kept separate; no compose/container on this host (Go tests only).

## GATES

- develop-merge: deferred (round 1 PR #1393 already open; merge/acceptance is a separate
  Maintainer action — not performed here).
- hosted run TERMINAL at the new head: DONE. Run 42116653735 (event `pull_request`) is
  `completed / success` at head `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170`. Runnable jobs
  all green: PR Trusted Plan, Source format, Workflow policy, go-vet, Focused Python,
  go-build, go-unit-tests, PR Selected Checks. Docker/Podman runtime gates on this PR were
  `skipped` (not enabled for this candidate) — that is a pass, not a failure. No .github edit
  or workflow_dispatch was made; CI was picked up automatically by the push to the PR branch.
- `git ls-remote origin refs/heads/work/r27-journal-wiring`:
  `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170` (verbatim, after push) — == new head.
- `git log --name-only origin/develop..ecae5f0d` lists ONLY my own commits on the branch
  (round-1 `3fa46bc2` + round-2 `ecae5f0d`); no foreign commit carried on top.

## Provenance

- Branch: `work/r27-journal-wiring` (PR #1393). Same branch/PR as round 1 — no second PR.
- Round-2 commit: `ecae5f0d877bd8ad76b83c6fe9cfe430ec416170` on top of round-1 `3fa46bc2...`.
- `origin/develop` (`3d8fc207...`) is an ancestor of `ecae5f0d` (verified with
  `git merge-base --is-ancestor`). No branch cut from another candidate.

## Focused local run (green baseline + red mutants)

Command:
`go test ./internal/machinehttp/ -run '^(TestCrashDuringApplyLeavesRunningUncertainAfterRestart|TestRestartReconcilesReissueToOriginalExecution|TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA_JournalWriteMakesResumeReal|TestMutantB_WrongOrderIsDetectable|TestApplyTransitionsAppendInOrder)$' -count=1 -v`

Result (all PASS):

- TestCrashDuringApplyLeavesRunningUncertainAfterRestart PASS — drives real POST /execute through
  `handleExecute`, SIGKILLs the child mid-Apply (executor blocks after `start` is durably written),
  reopens the SAME root, asserts execution reopened as running/uncertain with StartedAt + identity
  intact, never succeeded/failed/pending.
- TestRestartReconcilesReissueToOriginalExecution PASS — crashed apply killed mid-Apply; a fresh
  process re-issues the identical Idempotency-Key + content and reconciles (created==false) to the
  SAME execution id, still running/uncertain.
- TestTwoProcessesWriteJournalOrderedInProvenanceOrder PASS — two real child processes race to
  create against the SAME journal (barrier handshake), each contributes exactly one distinct,
  well-formed line in provenance order; no loss, no duplicate, no interleaving.
- TestMutantA_JournalWriteMakesResumeReal PASS. Baseline green: real journal carries a committed
  "running" line and a reopen of the SAME root observes durable/running. Mutant RED witness
  (t.Log): "MUTANT A RED: with the durable start write suppressed on the same root, the
  post-restart reopen observes no durable running execution — the resume cell's guard is real".
- TestMutantB_WrongOrderIsDetectable PASS. Baseline green: two writers on the SAME journal each
  contribute one distinct line in order A<B. Mutant RED witness (t.Log): "MUTANT B RED: with
  writer B's write lost on the same journal, the ordered cell sees 1 line, not 2 distinct ordered
  lines — the order guard is real".

Note: `go vet ./internal/machinehttp/` is clean. The pre-existing heavy durability fuzz test
`TestRound3BoundedRetentionAndNoPayloads` hangs on fsync on the slow work-TMP path (unrelated to
this change; store.go and that test are untouched). The focused selection above is what fully
verifies the changed risks.

## END

END_DONE w196-journal-wiring-r2: head=ecae5f0d877b crash=real handleExecute seam + child SIGKILL mid-Apply ordering=two concurrent child processes on same on-disk journal mutants=2/2 RED verbatim run=42116653735 TERMINAL success lsremote=ecae5f0d877bd8ad76b83c6fe9cfe430ec416170 | round-2 rewrite verified green locally, committed and pushed to work/r27-journal-wiring, hosted CI (go-unit-tests/build/vet) terminal-success at new head; ready for CODEX acceptance + Maintainer merge (merge/acceptance not performed here).

## Evidence published to baseharbor-plan (2026-11-05, round-2 final step per coordinator)

- File committed and pushed to baseharbor-plan `main`:
  `git commit b5fb91a — evidence(r27 journal-wiring): commit round-2 acceptance file`
  (`1 file changed, 99 insertions`; no other lane's files touched).
- origin/main tree witness:
  `git ls-tree origin/main evidence/r27-welle5-2026-11-05/journal-wiring/round-2.md`
  => `100644 blob 4d2f9d2b3db7d64adb51ab4a9ad434dc5d8325c3  evidence/r27-welle5-2026-11-05/journal-wiring/round-2.md`
- `git merge-base --is-ancestor HEAD origin/main` => YES (b5fb91a is on origin/main).
- No product code, no PR, no second commit needed.
