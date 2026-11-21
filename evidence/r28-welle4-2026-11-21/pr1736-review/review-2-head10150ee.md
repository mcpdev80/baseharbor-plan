# CODEX-REVIEW — PR #1736 second review

## PLAN
1. Verify the live #1736 head with ls-remote first and stop if it differs from the assigned SHA.
2. Verify exact run 44940073029 terminal state and enumerate executed versus skipped cells.
3. Verify Docker and Podman coreless lifecycle gate coverage for env destroy.
4. Verify planner full-bundle selection and regression tests keep registration-only paths unresolved/open.
5. Verify the native lifecycle test is assigned to exactly one application shard.
6. Record the prior per-case receipt finding as an owner-scope open item, not blocking.
7. Publish only this evidence from the lane-owned Planning worktree; review-only, no merge/close/comment.

## Planning remote
`git -C /home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt remote -v`:
```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Exact candidate and run

First remote witness, `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1736/head refs/heads/develop`:

```text
513488eeb6d788f0e5eec054be89807505f05e08 refs/heads/develop
10150ee7164bbc8767136e540eb966c3baab930b refs/pull/1736/head
```

The candidate head matches the assigned exact SHA. Fresh `gh pr view 1736` reports OPEN, non-draft, MERGEABLE, `mergeStateStatus=BEHIND`, base `develop`; develop has advanced beyond the mission's recorded `1080986fe73`. This is base lag only. The Owner assigned the follow-on hop to another lane; it is not an in-content review finding here.

Run `44940073029` (`pull_request`) is terminal `completed/success` on exact head `10150ee7164bbc8767136e540eb966c3baab930b`. It had 95 jobs: 22 success, 73 skipped, 0 failed, 0 cancelled, 0 incomplete. Skipped cells are not passes. `PR Selected Checks` job `136959286024` completed success and enforced selected native acceptance, full selected Go-shard coverage, and normal selected-job results.

Trusted plan artifact `plan-1736-r2/pr-plan.json` SHA-256: `9b4a6fe5c488513d6f7abbfe4b1d39013de4065fad69be367201b33be37a7ab3`. It identifies the exact head, target and merge-base `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`, `coverage_status=resolved`, `broad_required=false`, no unresolved coverage, and exactly these selected gates: `integration/docker/coreless-lifecycle` and `integration/podman/coreless-lifecycle`.

## Owner spot-check

### Docker and Podman coverage

`scripts/pr-gate-coverage.json:1452-1484` maps command registration, `env_destroy.go`, the native integration test, and machine coverage to both Docker and Podman coreless lifecycle surfaces. The runtime-specific integration-test row names `TestEnvironmentDestroyNativeLifecycle`. The gate records at `:2770-2789` are the two distinct focused PR gates: `integration/docker/coreless-lifecycle` and `integration/podman/coreless-lifecycle`.

Both gates actually ran on this exact head. Four shard cells plus each selected-gate aggregate passed:

| Runtime | Executed cells | Aggregate |
| --- | --- | --- |
| Docker | core-capability `136955210058`; foundation `136955210065`; application `136955210090`; identity-backend `136955210150` — all success | `136959259011` success |
| Podman | core-capability `136955209837`; foundation `136955209887`; application `136955209858`; identity-backend `136955209849` — all success | `136958492714` success |

### Full-bundle and fail-closed planner behavior

`scripts/pr-gate-plan.py:1229-1240` selects both gates and CLI checks for the complete registration plus implementation plus named-test bundle. The implementation-only path at `:1369-1373` also selects both gates. `scripts/test_pr_gate_plan.py:3131-3154` supplies the full bundle fixture and asserts resolved coverage, both gates, and CLI/deployment package checks. Its companion `test_registration_paths_alone_remain_unresolved` at `:3156-3160` confirms registration-only changes stay unresolved/open rather than being silently accepted.

Both planner suites ran in CI: required `PR · Validation · pr-planner-tests` job `136955169651` passed (215 tests); the candidate-added advisory job `136955169636` also passed and reports its candidate command included `scripts/test_pr_gate_coverage.py` (253 tests total). Candidate-added checks are advisory under the Owner CI policy, but they ran and reported successfully in this PR.

### Unique application-shard assignment

`scripts/pre-release-integration.py:73-78,92-98` registers the optional `TestEnvironmentDestroyNativeLifecycle` under exactly the `application` shard. Dynamic selection at `:149-169` adds it only when its source exists, and `validate_coreless_shard_partition` at `:172-193` rejects omissions or duplicate assignments. `scripts/test_pre_release_integration.py:187-213` creates a fixture source and asserts Docker and Podman both select the test exactly once in `application` and zero times in every other shard. The module is included in the required `ci-executor-tests` suite (`scripts/pr-check-runner.py:104-113,225-238`); job `136955169747` passed. The exact candidate does not contain `cmd/baha/env_destroy_integration_test.go` (GitHub Contents API returned 404 at the candidate, and also at current develop), so the optional native test itself was not executed in this run. The checked-in synthetic routing regression did execute through the CI executor suite; the native assignment is ready to activate when the product test source arrives.

## Receipt item

The previous review's per-case CI receipt finding remains an **open item, owner-scope receipt-tooling**. The exact run and selected cells are verified above; shard jobs expose aggregate receipts, not a named per-case receipt for every test. Per the Owner clarification for this task, this item does not block this candidate's verdict.

## Verdict — CODEX-REVIEW only

**APPROVE** exact head `10150ee7164bbc8767136e540eb966c3baab930b`, run `44940073029`. The three requested checks pass: both coreless lifecycle gates are mapped and ran; complete-bundle selection requires both gates while registration-only paths remain unresolved; and the optional native test is assigned exactly once to the application shard by a CI-tested routing rule. The candidate is behind current develop and requires the separate Owner-directed hop before later merge; that is not a defect in this frozen review.

## repo-rule compliance

- Read-only review of exact GitHub source, artifacts, plan, and run logs; no product file changes.
- No `.github/**` or `scripts/**` edits by this reviewer, no workflow dispatch/rerun, no local suite tests, no VM test, no merge/close/comment, no subagents.
- Native selected gates ran on GitHub-hosted CI. The optional named env-destroy test source is absent at this exact head; no claim is made that this test itself executed.

## cleanliness

Before review finalization, `docker ps -a --no-trunc` was recorded by shell PID 340596 at `/home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt/docker-before-1736-review2.txt`. This review started no containers or compose projects.

Fresh freeze check after evidence preparation:

```text
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1736/head refs/heads/develop
513488eeb6d788f0e5eec054be89807505f05e08 refs/heads/develop
10150ee7164bbc8767136e540eb966c3baab930b refs/pull/1736/head
```

The exact run remains `completed/success` at that candidate: 95 jobs, 22 success, 73 skipped, zero failure/cancelled/incomplete. Docker after snapshot, shell PID 356073, is recorded at `/home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt/docker-after-1736-review2.txt`; it has the same eight pre-existing `bh-itest-*` containers, all exited.

END codex-rev-1747 DONE — CODEX-REVIEW APPROVE; head `10150ee7164bbc8767136e540eb966c3baab930b`; run `44940073029` (95 jobs: 22 success, 73 skipped, 0 failed); plan-sha `9b4a6fe5c488513d6f7abbfe4b1d39013de4065fad69be367201b33be37a7ab3`; receipt: owner-scope open item; merge: not performed (review-only).
