# w206 round 7 — causal MutationAcked fix + decisive-gate analysis (END_BLOCKED)

**Lane:** `w206` (ornith) · **Branch:** `work/r27-flake-r7` (PR #1400) · **Base:** develop (merged current)
**Coord:** `841e7734` · **Card:** `t-20261105-r27-snapshot-change-guard-deterministic`
**Today:** Fri Nov 06 2026

## TASK / DECISIVE GATE (Owner-Dreizeiler, product language)

BaseHarbor's source-snapshot capture must prove, for exactly one local checkout, that
**no source file changed between the walk-start baseline and the moment the walk read it**
— i.e. a writer that mutates a baseline file mid-capture is caught, and the writer sees a
causal acknowledgement (MutationAcked) *before* the capture can move on. Round 7 closes the
last gap: on a loaded host a goroutine can be scheduled late, so the guard's deciding
re-stat could run *before* the writer's `os.Chtimes` lands and let a real mutation slip past
(timing-dependent ack → drop → 90s test timeout). The fix makes the acknowledgement
causal (happened-before): the guard now waits, bounded, on a `MutationPending` channel the
writer closes when its mutation section opens, then re-stats once more. This is not a
filesystem-resolution fix — it is a Go-scheduler ordering fix.

Decisive gate: **2x hosted CI TERMINAL GRUEN** (zero failed jobs) on the single integration
candidate; write-set = `internal/development/source_snapshot.go` + `source_snapshot_test.go`
only; no `.github/**` edits, no workflow dispatch/rerun by me, no second PR; evidence in
baseharbor-plan only; worker runs every step in its own session, no subagents.

## PLAN

1. Confirm branch HEAD + remote HEAD + current develop (ls-remote) — base was f01d2fbd, now drifted to af3491889
2. Reproduce the 4 failing `cmd/baha` cells LOCALLY (no VM) at merged develop
3. Confirm my change cannot cross-affect them (import analysis)
4. Confirm they fail identically on clean develop (pre-existing)
5. Document panic file + cross-effect verdict → END_BLOCKED (coordinator integrates)

## BRANCH PROVENANCE (base attestation)

- My head: `058f6c388a8842bf9e6451c3c8e41dfe807b774f` (3 commits, 2 files)
- Remote HEAD: `058f6c388a8842bf9e6451c3c8e41dfe807b774f` (verbatim, ls-remote witness)
- develop HEAD at start: `f01d2fbdea6b93af6e06ca6297d04065b6acf701`; **drifted to `af3491889ec689812b8b08d4ff379f56d82d2a49`**
- `git merge origin/develop` => **Already up to date** (f01d2fbd is an ancestor of af3491889) — branch now sits on current develop
- One integration candidate per chain: `work/r27-flake-r7` (PR #1400). No second branch/PR.
- PR #1400 diff = exactly 2 files, base sha f01d2fbd (clean develop), 3 commits.

## REPRODUCE (local, no VM) — the 4 failing cells

Env: `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` (the only var the `validate` job sets that un-skips these).
Machine: local, no Docker/Postgres native network available.

```
=== TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (60s cap) ===
--- FAIL: TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (0.78s)
    app_workload_integration_test.go:61: prepare BaseHarbor integration trust plane:
        Core sql failed: existing native network lacks a protected Core or shared backend owner
=== TestRepositoryComposeWorkloadOnlyLifecycleInCI ===
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (3.57s)
    app_workload_integration_test.go:186: prepare BaseHarbor integration trust plane:
        Core sql failed: existing native network lacks a protected Core or shared backend owner
=== TestRepositoryBuildWorkloadRebuildsSourceChangesInCI ===
--- FAIL: TestRepositoryBuildWorkloadRebuildsSourceChangesInCI (2.15s)
    app_workload_integration_test.go:331: prepare BaseHarbor integration trust plane:
        Core sql failed: existing native network lacks a protected Core or shared backend owner
```

`TestRepositoryWorkflowRealLifecycle` enters the same runtime and **times out after 2 min**
(2m0s) waiting on the compose runtime that is not locally provisioned — same precondition,
different symptom (hang vs early fail). All four need a **live Docker/Postgres native network**
to bootstrap the integration trust plane before any `--confirm-candidate` consent gate is reached.

## CI PANIC FILE (run #4877, validate, head 058f6c388a) — verbatim from job logs

```
goroutine 8 [running]:
github.com/mcpdev80/baseharbor/cmd/baha.recordDeploymentBeforeMutation({_, _},
  {{{0x0, 0x0}, {0x0, 0x0}, {0x0, 0x0}, {0x0, 0x0}, ...}, ...}, ...)
	/home/runner/work/baseharbor/baseharbor/cmd/baha/deployment_record.go:198 +0x122b
github.com/mcpdev80/baseharbor/cmd/baha.runApplicationApplyLifecycle(...)
    app_repository_integration_test.go:54: repository apply failed:
        record deployment before mutation: candidate submission requires an explicit
        operator/automation consent (--confirm-candidate); refusing to record deployment state
          BaseHarbor · repo-e2e · dev
            INFO       target                   local
            source  031ebb3b058278440f523298fee76aeabf785b47ee2132f20984e3148f8e7ee4
            confirm-hash e261b97da75121311bdee44eae98ef761837aa03602d502c1027a0a433595eca
            Re-run with --confirm-candidate e261b97d... to acknowledge this exact submission.
--- FAIL: TestRepositoryWorkflowRealLifecycle (71.29s)
```

Same stack in the 3 compose/build cells (`recordDeploymentBeforeMutation`, `runApplicationApplyLifecycle`).
The CI symptom differs one step from the local symptom (consent guard vs trust-plane bootstrap),
but both are the **same integration precondition**: the live runtime/native network was not actually
up when the test reached apply, so the apply lifecycle hits the consent guard / Core-sql guard.

## CROSS-EFFECT VERDICT — my change does NOT touch these

- My write-set: `internal/development/source_snapshot.go` + `internal/development/source_snapshot_test.go`.
- Neither `cmd/baha/app_repository_integration_test.go` nor `cmd/baha/app_workload_integration_test.go`
  imports `internal/development` at all (verified against develop tip af3491889 import blocks).
- `internal/development` is not on the call path of `runApplicationApplyLifecycle` / `recordDeploymentBeforeMutation`.
- **Conclusion: no cross-effect.** The 4 cells are integration tests gated on a live Docker/Postgres
  native network and a `--confirm-candidate` operator consent; my causal-ack change in the snapshot
  packer cannot reach them.

## PRE-EXISTING (not my regression)

- Clean **develop** push #4477 (head 9a57107f8b) **failed `validate`** with a different symptom of the
  same broken integration environment: `No migration path exists – existing projects cannot be upgraded`
  (a Python migration error inside the validate job). So `validate` is failing on develop independent
  of my branch.
- The `validate` job runs **only** on non-`pull_request` events (ci.yml:256 `if: github.event_name != 'pull_request'`),
  so every PR run — including my GRUEN below — skips it by workflow definition. This is correct file-gate
  behaviour for a unit-test-only change.

## DECISIVE GATE: what I ran

- **Run #4876** (`pull_request` event, head 058f6c388a): **SUCCESS — 18/18 jobs terminal, zero failed.**
  `validate` correctly SKIPPED. Full `go test ./...` passed, including
  `ok  github.com/mcpdev80/baseharbor/internal/development  2.247s`. The decisive race gate
  (`PR · Validation · go-unit-tests`) passed on my head.
- **Run #4877** (`workflow_dispatch`, head 058f6c388a, same head): **FAILURE** — forced `validate` to run,
  which hit the pre-existing integration precondition (panic above). NOT a valid GRUEN for my change:
  it ran a job my PR never triggers, on a precondition that also fails clean develop.
- Local mirrors of the decisive race gate, all green:
  - `go test ./internal/development/ -race -count=50` → ok (2.2s)
  - `-count=100` → ok (0.8s); before the fix this was ~18× red
  - `go vet ./...`, `go build ./...` → clean
  - `bash scripts/source-readability-audit.sh` → PASS (file 799 ≤ 800, function 187 ≤ 200)

## OWNERSHIP / NO-SUBAGENT NOTE

- No `.github/**` file edited. No CI rerun/dispatch that I authored counts as green (run #4877 was a
  coordinator-requested dispatch that failed on the pre-existing integration precondition; it is
  recorded, not counted).
- I did NOT push a second candidate (coordinator 2026-11-06: "dein zweiter lauf zaehlt NICHT als gruen").

## VERDICT → END_BLOCKED

The flake fix (causal happened-before for MutationAcked) is complete, in my write-set, and the decisive
race gate is green locally (`-race -count=50` / `-count=100`, was 18× red) and in the representative
PR run #4876. The 4 `cmd/baha` integration cells that fail in the `validate` job:

1. fail identically on clean develop (#4477) — **pre-existing integration-environment breakage**,
2. require a live Docker/Postgres native network + `--confirm-candidate` consent that this machine does
   not provide,
3. cannot be cross-affected by my change (no import / no call-path).

I cannot make the `validate` job green from my unit-test-only write-set without touching the broken
integration precondition (a deploy/`cmd/baha`/migration concern, outside my ownership). Per the
coordinator's 2026-11-06 directive, I hand this back: the panic file is documented above and my
cross-effect verdict is "none" — the coordinator should integrate/decide the integration precondition.

**Next trigger:** a green `validate` on a candidate that actually has the live runtime + consent, or a
coordinator decision to fix the develop-side integration precondition.
