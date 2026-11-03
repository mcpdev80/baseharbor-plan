# w33 evidence — appid-repo-workflow-proof (native TestRepositoryWorkflowRealLifecycle)

## Result: END BLOCKED — no authentic native PASS receipt retrievable; cannot self-qualify without CI changes

Lane: w33 (coord f49a3303). Card: t-20261023-appid-repo-workflow-proof (state: active).
Candidate SHA: 1c921c47abebe096535a309edb2be014e1682e01 (origin develop HEAD, 2026-11-03).
Worktree: /tmp/opencode/w33-appid-proof-wt, branch work/r27-appid-proof from origin/develop.
Source repo: mcpdev80/baseharbor.

## What was investigated (READ-only, no reruns, no workflow edits)

- gh run list / gh api actions/workflow_runs: total_count 1535 across repo; per-run check-run detail API-hidden (404) for this account.
- docker-runtime-acceptance.yml ("Runtime · Docker Core") — the workflow that runs the named test as a true native Docker lifecycle with BASEHARBOR_CI_RUNTIME_INTEGRATION=1 and a real rootless engine: 0 workflow runs ever (verified on the Actions runs page).
- podman-acceptance.yml: 29 runs, all cancelled/failed (latest 41462793027 head 6ce07ec4 cancelled after 1h13m).
- ci.yml "CI · Source & Quality": 815 runs. The named test runs in the PR lifecycle gate only if app_repository_integration_test.go changed between base and candidate (pre-release-runtime-suite.yml lines 257-279, $changed guard). Spot-checked PR #1333 (head f5183ded4b9b306ca4228a527e0c954556705d01, job 125837744889 "docker · lifecycle" succeeded) — #1333 did NOT modify app_repository_integration_test.go, so the named test was SKIPPED, not executed. Succeeded = skip-pass, not a native PASS receipt.

## Contract facts (from card + source at candidate SHA)

- cmd/baha/app_repository_integration_test.go line 16-18: t.Skip unless BASEHARBOR_CI_RUNTIME_INTEGRATION=1; then Resolve(ctx) must succeed on a real compose runtime or Skipf; otherwise full app init/apply lifecycle executes.
- Acceptance requires: a real native run (not skipped), bound to exact candidate SHA + run/attempt + source identity, no CI-green substitution.

## Local reproduction at candidate SHA (read-only-ish, did not push, no CI)

- go build ./... -> rc=0. go vet ./cmd/baha -> rc=0. gofmt clean.
- Without env: TestRepositoryWorkflowRealLifecycle -> SKIP (requires BASEHARBOR_CI_RUNTIME_INTEGRATION=1). PASS.
- With BASEHARBOR_CI_RUNTIME_INTEGRATION=1 on this workspace's docker (engine 29.8.1, non-rootless-hosted): the test ACTUALLY RUNS (real docker compose, real postgres scram-sha-256) and FAILS after ~99s — postgres-member auth fails (FATAL: password authentication failed for user "postgres"). This is a real runtime, not a skip — but it fails because this desktop environment cannot stand up the compose stack the CI runner can.
- git status of worktree: only _scan*.py scripts (untracked), no product or .github/scripts writes. Ancestry rc=0: origin/develop IS ancestor of HEAD; HEAD == origin/develop (1c921c47).

## Exact source integrity (candidate SHA 1c921c47)

- sha256 cmd/baha/app_repository_integration_test.go = ca6f3fe4e8341e70e2523504f693f6409d6d02b4c581284bda7761994d8276c7
- write-set clean: no .github/scripts changes; no product edits.

## Scope decision (per mission w33-appid-proof.txt)

- Mission: if no authentic PASS retrievable, attempt the smallest existing Docker acceptance workflow that truly executes the named lifecycle on the fixed candidate through its supported trigger; do NOT launch hosted runs that would need CI-file changes — else END_BLOCKED with reason.
- The only workflow that runs the named test on a fixed develop SHA through its supported trigger is docker-runtime-acceptance.yml, and it has never fired (0 runs). ci.yml only runs it on PRs where the test file changed, and #1055/#1333 neither changed the file nor is a develop integration. podman runs are failed/cancelled. The task explicitly forbids rewriting the develop candidate SHA (owned by the integration lane) and forbids CI-green substitution.
- Therefore the acceptance receipt is not retrievable and cannot be self-qualified without new CI changes, which the mission forbids.

## Handoff: END BLOCKED to f49a3303

Blocker: no authentic native TestRepositoryWorkflowRealLifecycle PASS on a fixed develop SHA exists; the sole Docker-core workflow that would produce it has 0 runs, and the task forbids CI-file changes and candidate-SHA rewrites to manufacture one. Open scope question for Owner:
1) Authorize a fresh, scope-locked CI workflow (or a one-time workflow_dispatch on the fixed develop SHA via a trusted actor / independent App/PAT credentials) to produce a genuine receipt — or
2) Accept a locally-executed PASS on the fixed candidate SHA under a fully isolated rootless Docker engine (host-level, matching the CI runner) as the receipt, with exact-source + ancestry proof, or
3) Record the task as blocked pending an authenticated hosted run.
All three options are Owner decisions; this lane will not unilaterally open CI files, push, or open a draft PR.

Worktree and evidence preserved at /tmp/opencode/w33-appid-proof-wt and this file. No CI changes made; no PR opened; no SHA rewritten.
