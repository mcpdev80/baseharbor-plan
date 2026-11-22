# PR #1736 exact-head independent review — fa527b439472b66736e242944a3ef7e48ab200db

## PLAN

1. Refresh PR #1736 head/base, full diff, and exact hosted run 44974816298 through GitHub remote evidence.
2. Read the relevant Planning task contract and repository review rules; map acceptance criteria to the candidate diff.
3. Inspect the full source/test changes and verify the exact selected Docker and Podman coreless-lifecycle jobs actually executed and passed.
4. Record an exact-head verdict, findings and limitations; publish this review to Planning origin/main.
5. No local tests or product/PR changes; preserve the separate #1752 and #1753 holds.

## Exact refs and task contract

- Planning task: `t-20261114-r28-cli2-env-delete` / card 0428-055; state `wait`. The card's latest `wait_reason` assigns the environment-destroy implementation fix and exact Docker/Podman test execution to #1627 first. This is a review of #1736's trusted routing contribution only; it does not accept the product task or clear that sequencing condition.
- Planning remote identity, verified before publication: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Product remote witnesses from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1736/head`:
  - `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop`
  - `fa527b439472b66736e242944a3ef7e48ab200db refs/pull/1736/head`
- GitHub PR API confirms #1736 is OPEN, non-Draft, head `fa527b439472b66736e242944a3ef7e48ab200db`, base `develop` at `6209874428f08dc3e90d6e29a42b30683ce9932a`, mergeable true. The run's `head_sha`, PR head SHA, and base SHA agree.

## Diff review

The exact PR diff is six files, 245 insertions and 2 deletions; no `.github/**` files change.

- `scripts/pr-gate-coverage.json` registers command wiring, `env_destroy.go`, the runtime-specific `TestEnvironmentDestroyNativeLifecycle`, machine-coverage registration, generated CLI indexes, and deployment-scope implementation/test under both Docker and Podman `coreless-lifecycle` surfaces. The named integration test is explicitly marked `runtime_specific` and required by name.
- `scripts/pr-gate-plan.py` adds the coverage regression file to planner validation; routes only the complete env-destroy bundle through the bounded CLI/doc/deployment checks plus both native gates; and leaves registration-only edits unresolved. Other generic/mixed registration changes retain the previous conservative behavior.
- `scripts/pre-release-integration.py` makes the named test optional only until its source and exact function declaration exist in the checked-out candidate. Once present, it is assigned exactly once to the application shard, gets the env-destroy acceptance variable, and runs with a 12-minute timeout. An empty shard and a missing required non-optional test still fail closed.
- The coverage regression asserts the env-destroy test maps to both native gates with no unresolved coverage and asserts the catalog's runtime-specific/name metadata.
- Planner regressions assert a complete implementation/registration/docs/test/deployment-scope bundle resolves to both native gates and that registration-only changes remain unresolved.
- Pre-release regressions use a temporary source fixture to prove the optional test is enabled and assigned only to the application shard for both runtimes. The existing partition validator catches duplicate or missing assignment.

No blocking source/routing defect found. The new product test source is not part of #1736 itself, so its native assertions cannot execute in this routing PR; that is a documented follow-on gate requirement for #1627, not evidence that #1736 ran the absent test.

## Exact hosted run

GitHub Actions run [44974816298](https://github.com/mcpdev80/baseharbor/actions/runs/44974816298) is `completed / success`, event `pull_request`, exact `head_sha=fa527b439472b66736e242944a3ef7e48ab200db`, base `6209874428f08dc3e90d6e29a42b30683ce9932a`. It used the synthetic merge commit `96687058682ba8525f9ee77fdff0e198b52b6bf0` for execution.

- `PR Selected Checks`, job 137065607140: SUCCESS. Its log prints `PR Selected Checks: PASS` and the selected integration matrix contains both `integration/docker/coreless-lifecycle` and `integration/podman/coreless-lifecycle`.
- Docker selected coreless job 137065338922: SUCCESS; its four executed shard jobs (foundation 137062317406, application 137062317428, core-capability 137062317476, identity-backend 137062317492) all completed successfully. Each reports the exact selected lifecycle gate execution step completed successfully.
- Podman selected coreless job 137065587687: SUCCESS; its four executed shard jobs (foundation 137062317714, core-capability 137062317716, identity-backend 137062317733, application 137062317744) all completed successfully.
- Candidate-added checks (advisory), job 137062282046: SUCCESS. The log reports candidate `pr-planner-tests` PASS, `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pr_gate_coverage.py scripts/test_pre_release_runtime_reuse.py`, `Ran 253 tests`, `OK`.
- Focused Python job 137062282066: SUCCESS. Trusted-plan job 137062225907 and workflow-policy job 137062225632: SUCCESS. The selected native jobs above are executed; unrelated matrix checks show `skipped` and are not counted as passing evidence.
- No local tests were run.

## Verdict

**APPROVE — exact head `fa527b439472b66736e242944a3ef7e48ab200db`.** The trusted planner/catalog changes are narrowly scoped, retain fail-closed behavior for incomplete registration changes, and prove the intended source-to-Docker/Podman gate mapping. The exact-head hosted aggregate and all selected Docker/Podman coreless shards passed. No blocking findings.

This is the independent content verdict recorded in Planning evidence only; no GitHub review event, approval, merge, close, or PR-state change was made. The environment-destroy product test itself is absent from this routing candidate by design and must execute on both runtimes in #1627 before the environment-deletion task can be accepted. The Planning task remains in `wait` under its current sequencing note.

## repo-rule compliance

Read-only product review only. No local tests, product code/workflow changes, PR comments/reviews, approval events, draft/ready changes, merges, closes or subagents. Planning evidence and the review board were updated. Planning remote was verified as `https://github.com/mcpdev80/baseharbor-plan.git` before publication.

## cleanliness

- `docker ps -a` before review work, own shell PID 1749058: seven pre-existing containers, all exited; no containers were started or changed by this review.
- `docker ps -a` after review work, own shell PID 1752755: the same seven pre-existing containers remained, all exited (`bh-itest-1c3f4e6d-12470-edit-runtime-integration-dev-api-1`, `bh-itest-7daed22f-28345-shared-openbao-1`, `bh-itest-7daed22f-28345-shared-openbao-member-1-1`, `bh-itest-7daed22f-28345-shared-postgres-init-1`, `bh-itest-7daed22f-28345-shared-postgres-1`, `bh-itest-7daed22f-28345-shared-postgres-member-1-1`, `bh-itest-7daed22f-28345-shared-openbao-admin-1`). No containers were started or changed by this review.

## END codex-rev-1747 DONE

Exact-head independent review is APPROVE with no blocking findings; review evidence is being published. Candidate SHA: `fa527b439472b66736e242944a3ef7e48ab200db`.

## Publication witness

Output of `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/coreless-validation/review-1736-headfa527b439.md'`:

`evidence/r28-welle5-2026-11-22/coreless-validation/review-1736-headfa527b439.md`
