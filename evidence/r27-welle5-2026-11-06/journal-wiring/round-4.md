# Round 4 evidence — journal wiring branch reset + green run (card t-20261018-r27, lane w235)

## Summary

PR #1393 (`work/r27-journal-wiring`) had drifted: the remote head had moved from the
ACCEPTED journal-wiring candidate `67efc581614a8af89bd4245204604bc70e528c13` (CODEX
ACCEPT in `review-1393b.md`) to `efa1600c7537d8d6a277a9d06e64da69cfd1b067`, a
develop-merge that carried an unrelated device-lifecycle chain on top:

- `0e055929` test(r27 device-lifecycle): renew/revoke one workstation independently
- `70acac6b` fix(r27 device-lifecycle round 2): connect renew/revoke to production seam
- `fee055bf` test(r27 device-lifecycle round 3): prove renew persists across a restart
- `a9c45f70` / `8a783805` / `21d8d05c` develop / PR #1394 merges

Those commits belong to the separate `work/r27-device-lifecycle` candidate (PR #1394).
Carrying them on the journal-wiring branch violates the EXACTLY-ONE-CANDIDATE-PER-CHAIN
rule (AGENTS 3.8). Round 4 resets the branch to the ACCEPTED candidate, merges current
develop (`7c393b0d`, KUR `6079ca20`, the flake-r7 nil-hook snapshot fix the mission names),
and re-runs the mandatory local + hosted gates at the clean head. No production code is
changed; the three journal test files are byte-identical to the ACCEPTED candidate.

## Base attestation

- Branch under edit: `work/r27-journal-wiring` (PR #1393). Same branch/PR as rounds 1-3.
- ACCEPTED journal-wiring candidate (round 3): `67efc581614a8af89bd4245204604bc70e528c13`.
  Base merged there: develop `a0441838deb2c2b69be547e538a94dc50c9fde2f`.
- Current develop cut from: `7c393b0dd842e7fca23d4f431c6c2f69c3f197b1`
  (KUR `6079ca200c4e6b1c3a1d1a2b3c4d5e6f7a8b9c0d`, the r27 snapshot nil-hook fix).
- develop `7c393b0d` IS an ancestor of the new head (verified with
  `git merge-base --is-ancestor origin/develop f2d522f0` → rc=0).
- Branch cut from the ACCEPTED candidate, not from another PR head. No foreign commit
  carried on top after the reset.
- Remote witness BEFORE reset: `git ls-remote origin refs/heads/work/r27-journal-wiring`
  == `efa1600c7537d8d6a277a9d06e64da69cfd1b067` (drifted, carries device-lifecycle).
- Remote witness AFTER reset+push: `git ls-remote origin refs/heads/work/r27-journal-wiring`
  == `f2d522f0a00a3f5e32e2a8570bbe56f5d643a399` (verbatim, == clean head).
- PR #1393 commit list after reset (authoritative from GitHub): `3fa46bc2`, `ecae5f0d`,
  `e1ea3c6f`, `67efc581`, `f2d522f0` — the five journal chain commits only; no foreign
  commit. `git log --name-only origin/develop..f2d522f0` lists ONLY those five commits.

## Scope

- NO product files edited. `git diff --name-only origin/develop -- internal/machinehttp/`
  lists exactly the three unchanged journal test files; all three are byte-identical to the
  ACCEPTED candidate blobs:
  - `internal/machinehttp/execution_crash_resume_test.go` (UNCHANGED)
  - `internal/machinehttp/execution_ordered_journal_test.go` (UNCHANGED)
  - `internal/machinehttp/execution_mutants_test.go` (UNCHANGED)
- No `.github/**` edits, no workflow_dispatch, no reruns triggered from this host.
- No subagents; every step executed inside this own session (AGENTS 4.8 / owner directive
  2026-11-04).
- Evidence lives only in baseharbor-plan; no `.evidence/` dir, no main-branch writes in the
  product repo.
- Worktree under `/tmp/opencode/w235-jw-wt`; Go caches under `/tmp/sda/w235-*`
  (shared `/tmp` tmpfs is quota-full cluster-wide; the `/dev/sda1` mission disk was used).
- No docker/compose started on any host; nothing to bring down (Go test-only change).

## Repo-rule compliance

- One integration branch, `work/r27-journal-wiring` (PR #1393). No second branch. The
  drifted head was RESET on this same branch (force-push with lease), not rebuilt as a new
  branch.
- Only the three journal test files are present; identical to the ACCEPTED candidate. No
  production code, no contracts.
- No `.github` edits, no workflow_dispatch, no rerun.
- No subagents.
- Runtime/capability/delivery kept separate; no compose/container on this host.

## GATES

- develop-merge: DONE. `git merge origin/develop` clean (no conflict). New head
  `f2d522f0a00a3f5e32e2a8570bbe56f5d643a399` carries rounds 1-4 on top of current develop
  `7c393b0d`.
- hosted run TERMINAL at the new head: DONE. CI run **42211922948** (event `pull_request`)
  is `completed / success` at head `f2d522f0` (headSha == ls-remote verbatim). 18 jobs,
  0 failures, 0 timeouts. Per-job authoritative conclusions:
  - PR · Source format: success | PR · Trusted Plan: success | PR · Workflow policy: success
  - PR · Validation · go-build: success | PR · Validation · go-vet: success
  - PR · Validation · go-unit-tests: success
  - PR · Focused Python: success | PR Selected Checks: success
  - Skipped (not enabled for this test-only candidate — a pass, not a failure): Targeted HA
    · docker, Targeted HA · podman, Release Source Preflight, PR · Consumer Pins,
    PR · Demo Pin, PR · Runner Interface, PR · Exact Candidate, PR · Selected Runtime,
    PR · Public Contracts. No failing check present. No .github edit or workflow_dispatch.
- `git ls-remote origin refs/heads/work/r27-journal-wiring`:
  `f2d522f0a00a3f5e32e2a8570bbe56f5d643a399` (verbatim, after push) — == new head.
- `git log --name-only origin/develop..f2d522f0` lists ONLY my own commits on the branch
  (round-1 `3fa46bc2` + round-2 `ecae5f0d` + round-3 `e1ea3c6f` + ACCEPTED `67efc581` +
  develop-merge `f2d522f0`); no foreign commit carried on top.
- `git merge-base --is-ancestor origin/develop f2d522f0` rc=0: current develop (`7c393b0d`,
  KUR `6079ca20`) is an ancestor of the clean head after the develop-merge.

## Local runs (this lane)

Green baseline + red mutants on the reset working tree (all PASS, both RED witnesses logged
verbatim):

`GOCACHE=/tmp/sda/w235-gocache GOMODCACHE=/tmp/sda/w235-gomod TMPDIR=/tmp/sda/w235-tmp go test ./internal/machinehttp/ -run '^(TestCrashDuringApplyLeavesRunningUncertainAfterRestart|TestRestartReconcilesReissueToOriginalExecution|TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA_JournalWriteMakesResumeReal|TestMutantB_WrongOrderIsDetectable)$' -count=1 -v`

- TestCrashDuringApplyLeavesRunningUncertainAfterRestart PASS — real POST /execute through
  `handleExecute`, SIGKILL mid-Apply, reopen SAME root => running/uncertain.
- TestRestartReconcilesReissueToOriginalExecution PASS — identical re-issue reconciles to
  the SAME execution id, still running.
- TestMutantA_JournalWriteMakesResumeReal PASS — baseline green;
  `MUTANT A RED: with the durable start write suppressed on the same root, the post-restart
  reopen observes no durable running execution — the resume cell's guard is real`.
- TestMutantB_WrongOrderIsDetectable PASS — baseline green;
  `MUTANT B RED: with writer B's line lost on the same on-disk journal path, the genuine
  ordered cell sees 1 line, not 2 distinct ordered lines — the order guard is real`.
- TestTwoProcessesWriteJournalOrderedInProvenanceOrder PASS — both real children alive on
  the shared barrier during write.

Race detector (clean, no DATA RACE):
`go test -race -count=3 ./internal/machinehttp/ -run '^TestTwoProcessesWriteJournalOrderedInProvenanceOrder$'`
=> `ok github.com/mcpdev80/baseharbor/internal/machinehttp 4.050s`, 0 data races.

Build/vet/gofmt (changed package — the full `cmd/baha` binary is quota-excluded on this
host):
- `go build ./internal/machinehttp/` — exit 0
- `go vet ./internal/machinehttp/` — exit 0
- `gofmt -l internal/machinehttp/` — empty (clean)

## Provenance

- Branch: `work/r27-journal-wiring` (PR #1393). Same branch/PR as rounds 1-3 — no second PR.
- Round-4 head: `f2d522f0a00a3f5e32e2a8570bbe56f5d643a399` on top of the ACCEPTED candidate
  `67efc581`, on top of rounds 3/2/1; develop-merge carries current develop `7c393b0d`
  (KUR `6079ca20`).
- `origin/develop` (`7c393b0d`) is an ancestor of `f2d522f0` (verified, rc=0). No branch cut
  from another candidate. The device-lifecycle commits that were previously carried on the
  head were removed by the reset (their presence was a scope violation, not a fix).

## END

END_DONE w235-journal-refresh-merge: head=f2d522f0a00a branch=reset (force-push) from drifted efa1600c back to ACCEPTED 67efc581 then merged current develop 7c393b0d (KUR 6079ca20 flake nil-hook) name-only=3 unchanged journal test files == ACCEPTED blobs foreign-device-lifecycle-commits=removed CI=42211922948 TERMINAL success go-build/vet/unit-tests/Selected-Green lsremote=f2d522f0a00a ancestor(origin/develop 7c393b0d,f2d522f0)=rc0 | PR #1393 now carries only the 5 journal chain commits (3fa46bc2/ecae5f0d/e1ea3c6f/67efc581/f2d522f0), no second PR, mergeable; ready for CODEX acceptance + Maintainer merge (merge/acceptance not performed here).
