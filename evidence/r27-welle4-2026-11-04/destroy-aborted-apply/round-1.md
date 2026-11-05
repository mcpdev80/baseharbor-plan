# r27 Welle 4 (2026-11-04) — destroy-after-aborted-apply — round 1

Lane: w154 (Worker). Coord: f49a3303. Card: t-20261104-r27-destroy-after-aborted-apply (round 1).

## PLAN

- read mission + prior evidence; understand never-delivered vs aborted-apply state
- fetch real remote; confirm develop ea3fb38e; ls-remote target branch witness
- create worktree under /tmp/opencode, session_move, branch work/r27-destroy-aborted-apply from develop
- write red-first regression: provider-change-abort => destroy must rc=0 (red on develop ea3fb38e)
- implement state-oriented fix (derive destroy set from what exists; no fixed runtime.env assumption)
- green on head; #1375 never-delivered still rc=0; normal apply+destroy unchanged
- gegenprobe: aborted apply with correct digests => delivery ready rc=0 OR clean documented error
- mandatory checks: go test ./cmd/baha ./internal/deployment, build, vet, gofmt
- commit, push branch, hosted CI run to terminal
- PR: name-only, log line, real ls-remote witness; publish END_DONE to f49a3303

## Repo-rule compliance

- No .github edited. No AGENTS.md or other tracked product file edited. No subagents (Owner directive 2026-11-04).
- Only two source files touched: cmd/baha/app_workload.go, internal/application/telemetry_authorization.go.
- One new test file: cmd/baha/w154_destroy_aborted_apply_test.go.
- Branch work/r27-destroy-aborted-apply cut from develop (512dcd72). ea3fb38e confirmed ancestor.
- Worktree under /tmp/opencode/w154-destroy-aborted-apply-wt (fixed workspace layout).

## The bug (state-oriented reproduction)

Kern differentiation from the closed #1375:
- #1375 = deployment.json MISSING entirely (never-delivered). destroy retires via the never-delivered path.
- THIS = deployment.json IS PRESENT with applied-intent + last_applied_ref, but the stage runtime
  (state/<environment>/runtime/runtime.env) was never materialized because a provider-change aborted
  mid-apply at the double-confirmation choke, before EnsureRuntime ran. Record left in stuck "applying".

Reproduction (red on develop ea3fb38e): drive the REAL CLI destroy against a stuck-apply state
(reconstructed via the public deployment API: deployment.json present, last_applied_ref set,
state "applying", runtime dir absent). Observed failing on develop:

  rc = read application runtime environment: open .../state/demo/runtime/runtime.env: no such file or directory

Exact failing call chain (captured via stack trace):

  executeApplicationDestroyLifecycle
    -> retireRuntimePreservingData
      -> stopRepositoryWorkload
        -> materializeRepositoryWorkload
          -> MaterializeWorkloadFromCompose
            -> materializeWorkloadFromComposePath
              -> readWorkloadRuntimeEnv  (calls readRuntimeEnv)
                -> readRuntimeEnv  <-- FAILS: runtime.env missing

The destroy path assumed a fixed runtime.env that was never materialized.

## The fix (state-oriented, derive from ownership, not a fixed filename)

1. internal/application/telemetry_authorization.go — readWorkloadRuntimeEnv:
   When the runtime.env is absent (os.ErrNotExist), return empty values instead of a hard error.
   An absent runtime.env means no prior bindings were materialized; a present-but-corrupt file still
   fails closed. Only affects the non-OTLP path (OTLP keeps its protected-owner verification).

2. cmd/baha/app_workload.go — stopRepositoryWorkload:
   Guard with an ownership check on the materialized runtime directory (files.Dir): if it was never
   materialized (os.IsNotExist), there are no owned workload containers to stop — return (false, nil)
   instead of failing. A present-but-unstat-able dir (permission error) still fails.

Why this is correct and not a silent no-op:
- Healthy path: EnsureRuntime always materializes runtime.env + the runtime dir before the workload
  is ever materialized, so both call sites see the files present. No behavior change for deliveries.
- Stuck path: the runtime directory absent is the ownership evidence that the runtime was never
  materialized. Deriving the destroy set from what exists on disk (record + directory contents) retires
  cleanly with rc=0, exactly as the mission requires ("leite die zerstoerungs-menge aus den Dingen ab,
  die wirklich existieren").

## Evidence

(1) NEW regression (exactly this cell): TestW154DestroyAfterProviderChangeAbortReturnsZero
    - RED on develop ea3fb38e: rc=read application runtime environment: .../runtime.env: no such file or directory
    - GREEN on head: rc=0, no runtime left behind.
    - Proven via git stash (fix reverted -> test fails; fix restored -> test passes), same session, no subagent.

(2) UNCHANGED cases:
    - #1375 never-delivered (TestW138*) still rc=0 (passed in same run).
    - Normal apply+delivery+destroy unchanged: workload/destroy/retire/apply/telemetry/runtime suites pass.
    - Blob-identical check for deployment_record.go: not modified in this change (git diff --stat shows only
      app_workload.go + telemetry_authorization.go + the new test).

(3) GEGENPROBE: provider-change ABORT mid-apply, second run with correct two confirmations => delivery
    reaches ready rc=0 OR documented clean error, no stuck state. VERIFIED: stuck retire leaves a
    decidable "runtime-retired" record (not stuck "applying"); a fresh apply re-resolves cleanly
    (TestW154GegenProbeAbortedApplyRecoversOnSecondRun, green).

## Hosted CI (own-run duty, AGENTS 4.6)

- PR: #1382 https://github.com/mcpdev80/baseharbor/pull/1382
  base=develop, head=work/r27-destroy-aborted-apply, headSha=942e3cc562b83e8d1f7907213f471087a88bdd3f
- CI run #41937967623: conclusion=success, status=completed (24 jobs: 14 success, 10 skipped, 0 failed).
- Key validation jobs all green: go-build, go-vet, cli-build, cli-vet, cli-gofmt, cli-guided-tests,
  cli-package-tests, go-unit-tests, source-contracts, PR · Trusted Plan, PR · Focused Python,
  Workflow policy, PR · Source format.
- go-unit-tests job #126951175136: success/completed (regression + against-probe run green on the
  hosted shared runner, not just locally).
- Skipped jobs are condition-gated (Release Source Preflight, Targeted HA docker/podman, Demo Pin,
  Public Contracts, Selected Runtime, Runner Interface, Consumer Pins, Exact Candidate) and do not
  apply to this focused fix.
- Run #41937967623 observed to terminal state via `gh run watch` (status=completed, conclusion=success).

## Session evidence

- head sha: 942e3cc562b83e8d1f7907213f471087a88bdd3f
- branch work/r27-destroy-aborted-apply on origin: 942e3cc562b83e8d1f7907213f471087a88bdd3f (ls-remote witness)
- regression red on develop ea3fb38e: yes (stash-verified: rc=read application runtime environment: .../runtime.env: no such file or directory)
- regression green on head: yes (rc=0, no runtime left behind)
- ls-remote develop: 512dcd721ac3fb739bfd4cb0b990fd68d6794762
- ls-remote work/r27-destroy-aborted-apply: 942e3cc562b83e8d1f7907213f471087a88bdd3f
- PR: https://github.com/mcpdev80/baseharbor/pull/1382
- CI run: https://github.com/mcpdev80/baseharbor/actions/runs/41937967623
