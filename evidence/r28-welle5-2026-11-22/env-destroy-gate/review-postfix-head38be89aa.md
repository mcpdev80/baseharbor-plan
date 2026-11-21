# CODEX-REVIEW — PR #1627 / card 0428-055 / exact head 38be89aa4a034add6338cfbd3185e24bb72893a2

## PLAN

1. Read the owner-directed mission and pin the review to exact head 38be89aa4a034add6338cfbd3185e24bb72893a2; inspect its live hosted run without waiting for completion.
2. Verify current GitHub refs, PR metadata, and full diff against develop 42da7128e724a533349e93d3742cbd232ea48936.
3. Trace the three-fix chain from 8de37f58caa through 62dd38f9b6d and ac05cc4efbc to 38be89aa4a; decide whether the last fix matches production semantics.
4. Verify #1736 ancestry and exact-run Docker plus Podman lifecycle selection/execution status.
5. Record exact-head APPROVE with the required terminal-green caveat and exclude cancelled runs.
6. Publish only this evidence to Planning origin/main, confirm the path, update the board, and post END; do not merge or close.

## Planning repository

Verified actual Planning repo remote before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. Evidence path: `evidence/r28-welle5-2026-11-22/env-destroy-gate/review-postfix-head38be89aa.md`.

## Remote witnesses and PR state

Resolved product GitHub remote: `https://github.com/mcpdev80/baseharbor.git`. Fresh `git ls-remote` output:

```text
38be89aa4a034add6338cfbd3185e24bb72893a2 refs/heads/cli2-env-delete
42da7128e724a533349e93d3742cbd232ea48936 refs/heads/develop
38be89aa4a034add6338cfbd3185e24bb72893a2 refs/pull/1627/head
4c919fd61f3214fe435bafdc6281bf4bcb300022 refs/pull/1736/head
```

PR #1627 is OPEN, non-draft, base `develop`, head `cli2-env-delete` at `38be89aa4a034add6338cfbd3185e24bb72893a2`, author `mcpdev80` / Marcel Pfingstgräf, mergeable `MERGEABLE`, merge state `BLOCKED` while checks run. The product checkout’s `lane-origin`, `origin`, and `upstream` remotes were all verified to resolve to `https://github.com/mcpdev80/baseharbor.git`. `git merge-base --is-ancestor refs/review/codex-rev-1747/develop refs/review/codex-rev-1747/pr1627` succeeded.

The complete develop-to-candidate diff is 16 files, 1,805 insertions and 2 deletions: `cmd/baha/commands.go`, `cmd/baha/env_destroy.go`, `cmd/baha/env_destroy_integration_test.go`, `cmd/baha/machine_coverage.go`, four CLI/reference index docs, `internal/deployment/environment_destroy_scope.go`, its test, and `scripts/pr-gate-coverage.json`, `scripts/pr-gate-plan.py`, `scripts/pre-release-integration.py`, `scripts/test_pr_gate_coverage.py`, `scripts/test_pr_gate_plan.py`, and `scripts/test_pre_release_integration.py`. No workflow file changed.

## Three-fix chain and production semantics

1. At the earlier `8de37f58caa` candidate, the newly routed native environment-destroy test failed during workload preparation with `prepare native workload deployment inputs requires authenticated BaseHarbor operator`. The intervening `62dd38f9b6d` develop merge did not add the missing authenticated fixture. The failure was in test setup, before the environment-destroy behavior could be exercised.
2. `ac05cc4efbc` fixes fixture authentication: `cmd/baha/env_destroy_integration_test.go:29` wraps the main test context in `testOperatorContext`, and `:74` does the same for cleanup. `cmd/baha/test_operator_context_test.go:18-29` preserves an existing principal or installs a verified test principal plus membership/enforcement. This addresses the preparation and cleanup authentication failures.
3. `38be89aa4a034add6338cfbd3185e24bb72893a2` fixes the test’s consent-plan inputs. `cmd/baha/env_destroy_integration_test.go:110-116` builds consent using the selected target, runtime input, and `applicationStopModeKey=true`, then derives the `PlanID` from `buildApplicationStopPlan`. Production uses the same runtime input and target at `cmd/baha/env_destroy.go:164-165`; KEEP sets `applicationStopModeKey=true` in `executeEnvironmentScopedDestroy` at `:240-245`. The test now consents to the actual KEEP stop impact plan. The change does not bypass or weaken stale-consent validation; the prior rejection was correct because the test computed consent for a different plan. This is a production-semantics correction in the fixture, not a test-only green workaround.

The native regression asserts successful `env destroy prod --keep-data --yes`, removal of the environment identity, and retained stopped deployment ownership (`cmd/baha/env_destroy_integration_test.go:122-130` and following assertions). Scope collection is read-only and classifies by deployment application ID/environment, with unknown or mismatched identity handled fail-closed (`internal/deployment/environment_destroy_scope.go:116-207`). The CLI processes each verified scoped deployment and removes the environment identity only after successful lifecycle processing (`cmd/baha/env_destroy.go:170-175`).

## CI routing and exact run

The changed test is durable in this PR’s CI route. `scripts/pr-gate-coverage.json:1460-1475` maps `cmd/baha/env_destroy_integration_test.go` to both `source.gate.integration.docker.coreless.lifecycle` and `source.gate.integration.podman.coreless.lifecycle`, with required test name `TestEnvironmentDestroyNativeLifecycle`. `scripts/pre-release-integration.py:73-78` assigns that test to the application shard; `:91-111` includes it only when its source exists and selects the exact Go test name; `:131-169` assigns it to the designated shard. The acceptance environment is set at `:263-265`. `scripts/test_pre_release_integration.py:187-213` asserts exactly one assignment to the application shard for each runtime. Planner routing tests cover both Coreless gates and fail closed on registration paths alone (`scripts/test_pr_gate_plan.py`, new `EnvironmentDestroyNativeGateRoutingTests`).

Exact hosted run `44960199639` is a `pull_request` run for exact head `38be89aa4a034add6338cfbd3185e24bb72893a2`. At the latest observation, status remained `in_progress` (updatedAt `2026-11-21T23:08:39Z`). `PR · Trusted Plan` completed successfully, including “Route only required Go tests into mandatory parallel shards.” Both selected `integration/docker/coreless-lifecycle · application` and `integration/podman/coreless-lifecycle · application` jobs were executing `Run exact selected Core-less lifecycle gate`; neither had a terminal conclusion. The `PR Selected Checks` aggregate was absent. The plan routed the test to both engines and execution started, but the two executions and aggregate are not yet passes.

Review verdict: **APPROVE, conditional** for exact head `38be89aa4a034add6338cfbd3185e24bb72893a2`. Acceptance is effective only if run `44960199639` reaches terminal green and both named application shards pass. This is not a claim that CI passed. Runs `44958801932`, `44958293233`, and `44957245330` are cancelled/superseded and excluded.

## #1736 dependency result

The mission-specified feature commit `1e2ba9d57868778d7c74ef68882f61bd1b01bb33` is an ancestor of #1627’s exact `38be89aa4a034add6338cfbd3185e24bb72893a2` candidate (`git merge-base --is-ancestor 1e2ba9d57868778d7c74ef68882f61bd1b01bb33 refs/review/codex-rev-1747/pr1627` succeeded). However, the fresh current #1736 PR head is `4c919fd61f3214fe435bafdc6281bf4bcb300022`, and `git merge-base --is-ancestor refs/review/codex-rev-1747/pr1736 refs/review/codex-rev-1747/pr1627` failed. The required feature commit is present, but current PR #1736’s new merge head is not contained in #1627. The current #1736 PR therefore is not wholly “in #1627” and still needs its own merge; no merge or close was performed. The separate #1736 review is now underway per its queued mission.

## repo-rule compliance

Reviewer-only. No product edits, local tests, container starts, workflow actions, PR comments, merge, or close. The exact-hosted run is the only test execution evidence relied upon.

## cleanliness

Docker after the read-only review, shell PID `732705`: eight pre-existing `bh-itest-*` containers were present, all exited (six exit 0, one exit 130, one exit 143). No containers or compose projects were started or changed.

END_BLOCKED codex-rev-1747: conditional APPROVE recorded for #1627 head 38be89aa4a034add6338cfbd3185e24bb72893a2; terminal green run 44960199639 remains required, and current #1736 head 4c919fd61f3 is not contained in #1627.

## PLAN — final #1627 candidate

1. Keep #1627 on hold; do not issue a verdict on superseded heads.
2. Refresh exact candidate b3b0c2c9efc43e9696c5eeda2a7164c88889e188 and run 44961334018.
3. Recheck ancestry of current #1736 head 4c919fd61f3214fe435bafdc6281bf4bcb300022 against final #1627 head b3b0c2c9efc43e9696c5eeda2a7164c88889e188.
4. Issue #1627 verdict only after run 44961334018 is terminal green; report status when it completes.


## Current #1627 hold — final candidate b3b0c2c9efc

The previous conditional verdict above concerns superseded head `38be89aa4a034add6338cfbd3185e24bb72893a2` and run `44960199639`, which was canceled. It is not a verdict on the current candidate. The current exact head is `b3b0c2c9efc43e9696c5eeda2a7164c88889e188`; exact run `44961334018` is still `in_progress` as last observed, with Docker and Podman application lifecycle jobs also `in_progress`. No verdict is issued for #1627 until that exact run reaches terminal green and both named engine jobs pass.

Current #1736 head `4c919fd61f3214fe435bafdc6281bf4bcb300022` is not an ancestor of b3, but its feature commit `10150ee7164bbc8767136e540eb966c3baab930b` is an ancestor. #1736’s separate review is APPROVE for its exact head/run; do not merge it before the #1627 exact run passes `TestEnvironmentDestroyNativeLifecycle` on both engines and #1627 lands.

END_BLOCKED codex-rev-1747: #1627 has no current verdict; exact run 44961334018 for b3b0c2c9efc43e9696c5eeda2a7164c88889e188 is still in progress.
