# PR #1725 review and merge state

ROLLE: REVIEW

## PLAN

1. Read the mission and confirm the exact candidate, task contract, scope, and acceptance criteria.
2. Refresh product and Planning remotes; verify ownership, branch provenance, and current candidate state.
3. Inspect the candidate diff, security path, hosted CI receipts, and prior lineage evidence.
4. Merge only if every criterion is satisfied; otherwise record a precise corrective recipe.
5. Publish this review in baseharbor-plan, update the live board, and post the final status.

## Verdict

BLOCKED: the PR was already merged before this review could be completed, and the mission's required test-execution receipt is absent from the exact-head run. I did not perform a merge. The code path inspected is fail-closed, and the current PR diff matches the three expected files, but the four named tests were not executed by the required hosted run. The merge therefore cannot be represented as having satisfied the mission's acceptance gate.

## Candidate and task contract

- Mission file: `/tmp/opencode/m_rev_1725.md.g`.
- Task: `t-20261120-shared-backend-state-version-message` (0428-201), already `accepted` and `closed` in planning when read. No task metadata was changed in this review.
- Mission candidate: PR #1725 head `835c235603ec9437664b9078a966a3d4467942a6`, base `b3df96348a`.
- Fresh product remote witness during this review, from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1725/head`:
  `b517b279c9533669c104dc6429c0a1934c508716 refs/heads/develop`
  `3f334347580f1fcbf14182bfc521ec688a0b55b2 refs/pull/1725/head`
- Read-only PR API state: closed and merged at `2026-11-23T08:37:39Z`; actual PR head was `3f334347580f1fcbf14182bfc521ec688a0b55b2`, base branch `develop`, base SHA `826d498fc1ae9524112d07477a8809798d8272a7`, merge commit `b517b279c9533669c104dc6429c0a1934c508716`. Thus the mission's stated head/base no longer matched the live PR when reviewed.
- The merge commit's parent is `826d498fc1ae9524112d07477a8809798d8272a7`; the current remote `develop` witness is the merge commit above. I did not observe a pre-merge `ls-remote` in this review session, so I do not claim a before/after merge witness from this session.
- GitHub's PR files endpoint listed exactly three changed paths: `internal/application/shared_backends.go`, `internal/application/shared_backends_state.go`, and `internal/application/shared_backends_test.go`. This matches the card write-set. No catalog file and no `.github/**` file appears in the PR file list.
- The prior Planning record `evidence/r28-welle5-2026-11-23/sweep-1725/final-hop.md` is incomplete: its run, merge and witness fields still contain placeholders. It does not supply the required test execution proof.

## Acceptance mapping

1. Diff scope: PASS for the live PR diff. It contains only the two shared-backend implementation files and their tests, as listed above.
2. Hosted execution: FAIL. Run `45136441345` completed successfully for actual head `3f334347580f1fcbf14182bfc521ec688a0b55b2`, but `PR · Go unit` job `137563850346` was skipped. In the exact run log, `PR Selected Checks` job `137575262405` shows `UNIT_SCOPE: none` and `UNIT_RESULT: skipped`. Searching the run log for `TestSharedBackendState` produced no test execution lines. The required four test functions in `internal/application/shared_backends_test.go` are `TestSharedBackendStateVersionMismatchNamesVersions`, `TestSharedBackendStateVersionMismatchIsDistinguishableFromCorruption`, `TestSharedBackendStateLoadReportsVersionReason`, and `TestSharedBackendStateCorrectVersionStillLoads`; none is evidenced as executed by this run. The mission explicitly requires `UNIT_SCOPE != none` in the owning hosted cell, so the successful aggregate does not satisfy this criterion.
3. Catalog and workflow scope: PASS for the observed PR diff. No catalog or `.github/**` path was changed. No workflow rerun or dispatch was initiated in this review.
4. Security and fail-closed behavior: PASS by code inspection. `internal/application/shared_backends_state.go:31-32` returns `SharedBackendStateVersionMismatch` when the stored version differs from version 3, before any fallback initialization; no migration, discard, or write occurs on that path. `internal/application/shared_backends.go` defines the typed mismatch and reports found version, expected version, and the supported next step. The tests assert mismatch distinction from corruption, the real load path's version reason, no state rewrite, and the correct-version happy path. No silent fallback or consent weakening was found in this diff. The code review does not substitute for the missing hosted test execution.

## CI witnesses

- Run `45136441345`: event `pull_request`, status `completed`, conclusion `success`, head `3f334347580f1fcbf14182bfc521ec688a0b55b2`; completed `2026-11-23T08:36:39Z`.
- `PR · Trusted Plan` job `137563748756`: success on that head.
- `PR Selected Checks` job `137575262405`: success on that head, GitHub Actions integration 15368.
- The selected Podman data-capabilities runtime job `137564428809` succeeded. It is not the Go unit test owner and does not establish execution of the four named tests.
- The successful aggregate's own log accepted the no-unit-test selection because it paired `UNIT_SCOPE: none` with `UNIT_RESULT: skipped`. This is internally consistent with that aggregate but fails the more specific card acceptance quoted in the mission.
- The PR had no submitted review records when queried. Since the PR was already merged, this review is a post-merge audit and cannot serve as a pre-merge independent review receipt.

## Corrective recipe and stop criterion

- Record a targeted CI-routing/gate finding for the changed base-cataloged test file: the trusted selection must reach a Go unit scope that executes all four named tests, and the exact hosted log must show their execution and pass results with `UNIT_SCOPE` other than `none`.
- Keep `.github/**` and shared planner files outside this review's write-set. If the route requires a shared planner, required-plan, or workflow change, report the precise owning file and change to its Owner rather than changing it in this review.
- Because the PR is already merged, do not rewrite or force-push its history. The Coordinator/Maintainer should track the missing durable test gate as a corrective card and decide whether a follow-up PR is required. Stop acceptance of the 0428-201 receipt until exact CI evidence exists.
- Stop criterion: exact-head hosted evidence for all four tests with non-`none` unit scope, plus a separate pre-merge review on any corrective candidate. No new run was requested by this review.

## repo-rule compliance

- Product source was inspected read-only. No product files, branches, PR fields, workflows, rulesets, releases, or tags were changed.
- No local tests were run. No Docker or Podman containers were started.
- Planning remote was verified before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- Only this review evidence file is owned by this session. The task card and unrelated untracked files were left untouched.

## CLEANLINESS

- Before review, shell PID `1183438`: `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`); no containers were listed.
- No container or compose project was started by this review.
- After review, shell PID `1214189`: `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`); no containers were listed.

## ROLLE: MERGE

Not performed in this session. The remote PR was already closed as merged before review completion. Remote merge SHA: `b517b279c9533669c104dc6429c0a1934c508716`.

END_BLOCKED codex-rev2-1736: PR #1725 already merged at b517b279c9533669c104dc6429c0a1934c508716; required hosted tests absent on head 3f334347580f1fcbf14182bfc521ec688a0b55b2.

## Planning validation

- `python3 scripts/plan.py check`: 697 tasks, 7 epics, 13 releases, 24 decisions; 0 errors and 10 pre-existing dependency warnings.
- Planning repository remote output before this evidence commit:
  `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`

## Origin evidence-path witness

- Final required `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1725/review-merge.md$'` output before this evidence push:
  `evidence/r28-welle5-2026-11-23/sweep-1725/review-merge.md`
