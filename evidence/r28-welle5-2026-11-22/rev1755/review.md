# PR #1755 review

## PLAN

149. Read /var/tmp/m/rev1755b.md.tail.g and the companion mission; capture the exact #1755 review scope and restrictions.
150. Refresh PR #1755 exact head/base and terminal hosted CI state from the verified GitHub remote.
151. Inspect the exact diff, requested acceptance points, authorship, ancestry, and required receipts without local tests.
152. Record the exact-head review findings/verdict in Planning evidence and validate the evidence.
153. Publish the evidence, verify its origin/main path, update the board, and post END.

## Review scope and exact state

- PR: https://github.com/mcpdev80/baseharbor/pull/1755
- Candidate reviewed: `558265019ffcd69b66a422180eafcc56cddd5d30`
- Task base / run merge base: `82825e95a6f6083702d0ba5401d97f356085c722`
- Run: `44985859511`, terminal `completed / success`, exact head matches candidate. Required `PR Selected Checks` job `137096549284` succeeded.
- Current live PR: merged at `2026-11-22T04:39:48Z`, merge commit/current develop `1ff16925c4e141d732459a34ddf0b7f49128a214`. Live `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1755/head` output:
  `1ff16925c4e141d732459a34ddf0b7f49128a214 refs/heads/develop`
  `558265019ffcd69b66a422180eafcc56cddd5d30 refs/pull/1755/head`
- GitHub compare of requested base to candidate: `ahead`, merge base equals requested base, with two commits: `ci(0428-228): select native gates for operator seams`; `ci(0428-228): execute operator seam gate`.
- Changed files: `.github/workflows/ci.yml`, `scripts/pr-check-runner.py`, `scripts/pr-gate-plan.py`, `scripts/pre-release-runtime-impact.json`, `scripts/test_pr_check_runner.py`, `scripts/test_pr_gate_plan.py`, `scripts/test_pre_release_runtime_reuse.py`.
- Planning repository remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

## Findings

- F1 — REQUEST CHANGES: the candidate adds the operator seam execution arm, but the exact successful run never selected it. `.github/workflows/ci.yml:1328-1331` executes `go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^TestCIIntegrationOperator' -count=1 -v` and hard-fails without a `--- PASS` line. `scripts/pr-gate-plan.py:1293-1299` selects `ci-integration-operator-seam-tests` only when a changed path is in `CI_INTEGRATION_OPERATOR_PATHS`; planner lines 156-160 define the three operator source/test paths. In the exact run’s `trusted-pr-plan` artifact (`14739712935`, `pr-plan.json`), `required_validation_checks` contains only `ci-actionlint`, `ci-executor-tests`, `ci-policy`, `pr-planner-tests`, and `receipt-execution-tests`; it omits `ci-integration-operator-seam-tests`, and `selected_gates` is empty. The job list confirms `validate` and `PR · Selected Runtime` were skipped. Thus the workflow case at 1328 was not reached and the tagged operator suite did not execute in run 44985859511. The planner test at `scripts/test_pr_gate_plan.py:3163-3184` checks that changing each mapped operator file requires the validation ID, and the runner unit test at `scripts/test_pr_check_runner.py:580-597` covers its tag profile; those checks passed via `pr-planner-tests` job `137096181843` and `ci-executor-tests` job `137096181799`, but neither is execution evidence for the new workflow arm or real operator suite. Recipe: make the operator-seam CI dispatch itself part of the exact PR gate-change qualification path (for example, include this validation ID when the operator seam routing/workflow definition changes) and assert that selection in a planner regression; rerun so the trusted plan contains the ID and its validation job reports the matching `TestCIIntegrationOperator` pass. Stop criterion: exact-head required plan names the validation, the hosted validation job executes it with the build tag, and its log contains the pass line. The PR is already merged; this review does not change PR state.

## Verified routing and test coverage

- `NATIVE_TEST_GATE_COMPONENTS` maps the three operator seam files, `test_operator_context_test.go`, and `application_lifecycle_lock_test.go` to Docker and Podman data-capabilities gates (`scripts/pr-gate-plan.py:145-164`). The init/wizard/Perses/repository-up test paths add both guided gates (`:165-174`); shared runtime test support adds both coreless-lifecycle gates as well (`:175-176`). The exact map contains the eight #1750 test paths and three operator seam paths requested.
- `scripts/pre-release-runtime-impact.json` matches the planner tuples for every key in the new map; `scripts/test_pre_release_runtime_reuse.py:380-385` asserts set equality for every key. The corresponding `test_native_test_gate_admission_matches_pre_release_impact` ran in passing `pr-planner-tests`.
- Runner registration at `scripts/pr-check-runner.py:34,67-69` associates the check with `^TestCIIntegrationOperator` and `baseharbor_ci_operator_testonly`; the executor passes those build flags to discovery and execution (`:259-280`). The unit regression at `scripts/test_pr_check_runner.py:580-597` exercises the tagged profile and passed in `ci-executor-tests`.
- Duplicate suite execution was not observed in this run: the dedicated validation name was absent and its job did not run; runtime jobs were skipped. The run therefore provides no evidence of a duplicate execution.
- All required checks reported by `gh pr checks 1755 --required` were successful. Relevant passing jobs: Source format `137096139574`, Trusted Plan `137096139711`, Native gate plan `137096139746`, Focused Python `137096181692`, Candidate-added checks (advisory) `137096181730`, five listed validation jobs including executor/planner, and aggregate `137096549284`. Skipped jobs are not counted as evidence that the operator suite ran.

## Review decision

REQUEST CHANGES for the exact candidate because F1 leaves the newly added workflow execution arm and real tagged suite unexecuted on its successful exact-head run. This is an independent review finding only; PR #1755 was already merged before this review completed.

No local tests were run. No product files, PR state, GitHub reviews/comments, workflow runs, or merge state were changed.

## cleanliness

- Before review, PID `2342852`: `docker ps -a` showed only pre-existing container `baha-prunit-db-2286133` (`a0d40c5bcc8e`), Postgres 18, Up; it was not started or changed by this review.

## END codex-rev-1747 BLOCKED

Candidate `558265019ffcd69b66a422180eafcc56cddd5d30`; verdict REQUEST CHANGES, finding F1: dedicated operator seam workflow branch absent from the exact successful run's selected validation list.
- After review, PID `2350391`: `docker ps -a` showed the same pre-existing container `baha-prunit-db-2286133` (`a0d40c5bcc8e`) Up; no container was created, stopped, or modified.
