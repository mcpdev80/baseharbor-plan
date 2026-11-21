# 0428-208 develop CI evidence

ROLE: Worker (evidence-gathering, no product file changed).
CARD: t-20261121-static-gate-registration (0428-208), OR new evidence card per mission instruction.

## PLAN

1. Measure develop head via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`.
2. Get the exact "CI · Source & Quality" workflow name/id via `gh workflow list --repo mcpdev80/baseharbor`.
3. Dispatch the workflow on develop: `gh workflow run "CI · Source & Quality" --repo mcpdev80/baseharbor --ref develop`.
4. Find the new run by matching `event == workflow_dispatch` AND `headSha == measured develop head`; record run-id.
5. Watch to terminal (4.6); per cell name + conclusion; per red cell per-job log, byte count, distinct `--- FAIL:` names.
6. Write this evidence with ls-remote, workflow-list, dispatch, run-id/event/headSha, per-cell table, missing-test names, sum, verdict line, PLAN, cleanliness, repo-rule compliance.
7. Confirm evidence path on `origin/main` before END; post END_DONE to coordinator with candidate SHA.

## 1. develop head (ls-remote witness)

Command: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
Output:
```
dea88c8f2caa2db93c1216c619993e444080a9d2	refs/heads/develop
```

measured develop head = `dea88c8f2caa2db93c1216c619993e444080a9d2`

## 2. workflow identity (gh workflow list witness)

Command: `gh workflow list --repo mcpdev80/baseharbor --json name,id`
Filtered (CI · Source & Quality):
```
{"id":352609139,"name":"CI · Source & Quality"}
```
exact workflow name (verbatim): `CI · Source & Quality`
exact workflow id: `352609139`

## 3. dispatch command

Command: `gh workflow run "CI · Source & Quality" --repo mcpdev80/baseharbor --ref develop`
Result: dispatched, no error.

## 4. run assignment witness (event + headSha both match)

Command: `gh run list --repo mcpdev80/baseharbor --workflow "CI · Source & Quality" --limit 5 --json databaseId,status,conclusion,headSha,event`
Matching row (event == workflow_dispatch AND headSha == measured develop head):
```
{"conclusion":"","databaseId":44913143056,"event":"workflow_dispatch","headSha":"dea88c8f2caa2db93c1216c619993e444080a9d2","status":"in_progress"}
```
run-id = `44913143056`
event = `workflow_dispatch`
headSha = `dea88c8f2caa2db93c1216c619993e444080a9d2` (== measured develop head)
run url = https://github.com/mcpdev80/baseharbor/actions/runs/44913143056

## 5. per-cell table (run 44913143056, watch to terminal)

terminal state: run status `completed`, run conclusion `failure`.

| job (cell) | conclusion | note |
| --- | --- | --- |
| Workflow policy | success | workflow-policy gate (byte witness below) |
| validate | failure | only unit/package tests ran; other cells skipped (develop is not a PR; matrix cells gated behind PR Selected Checks) |
| PR · Exact full Pre-Release | skipped | develop-only |
| PR · Native Keycloak/Core · ${{ matrix.runtime }} | skipped | develop-only |
| PR · Main release source | skipped | develop-only |
| PR · Native · ${{ matrix.id }} | skipped | develop-only |
| PR · Runner Interface | skipped | develop-only |
| PR · Demo Pin | skipped | develop-only |
| PR · Main release Go · ${{ matrix.shard }} | skipped | develop-only |
| Targeted HA · podman | skipped | develop-only |
| PR · Source format | skipped | develop-only |
| PR · Native gate plan | skipped | develop-only |
| PR · Go unit · ${{ matrix.shard }} | skipped | develop-only |
| PR · Focused Python | skipped | develop-only |
| PR · Consumer Pins | skipped | develop-only |
| Targeted HA · docker | skipped | develop-only |
| Release Source Preflight | skipped | develop-only |
| PR · Trusted Plan | skipped | develop-only |
| PR · Selected Runtime | skipped | develop-only |
| PR · Candidate-added checks (advisory) | skipped | develop-only |
| PR · Public Contracts | skipped | develop-only |
| PR · Exact Candidate | skipped | develop-only |
| PR · Validation · ${{ matrix.check }} | skipped | develop-only |
| PR · Selected Core-less · ${{ matrix.runtime }} | skipped | develop-only |
| PR · Draft source and routing | skipped | develop-only |
| PR · Draft Go · ${{ matrix.shard }} | skipped | develop-only |
| PR Selected Checks | skipped | develop-only |
| PR · Main release checks | skipped | develop-only |

Only two cells ran: `Workflow policy` (success) and `validate` (failure). All matrix cells are skipped because this is a `workflow_dispatch` on the `develop` branch head, not a PR — the unit-test matrix runs under `PR Selected Checks`, which did not fire for a dispatch. The `validate` job's own step 14 `Run unit and package tests` is the only failing step.

### validate job: step results

- steps 1-13 (Set up job .. Validate source readability): success
- step 14 `Run unit and package tests`: FAILURE
- steps 15-19: skipped (native integration gated behind the failing unit step)
- step 20 `Cleanup persistent runner state`: success
- steps 37-41 (post / stop / complete): success

### red-cell per-job log witness

- job id of the red cell: `136873016970` (validate)
- log fetched via `gh api repos/mcpdev80/baseharbor/actions/jobs/136873016970/logs`
- log byte count: 124366 bytes (BOM-stripped)

distinct top-level `--- FAIL:` names from the single validate job log (counted from that one log only): 14

```
TestBahaStatusHostContainersDashboardsExposesUnavailable
TestBahaStatusInfrastructureDashboardsExposesEveryPanel
TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace
TestDeterministicInitDoesNotPersistUnneededSourceSelection
TestDeterministicInitPersistsAmbiguousSourceSelectionPositive
TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds
TestGuidedInitDeterministicPositionalEnvironmentAliases
TestGuidedInitExplicitFlagsKeepDeterministicPath
TestGuidedInitInteractiveCanAcceptDetectedDefaults
TestGuidedInitQuickDoesNotPromoteHeuristicSecrets
TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent
TestQuickInitPreservesWorkloadOnlyRepository
TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload
TestSharedBackendReconcileRejectsSecondProcess
```

subtest failures (nested, counted separately, all under the positional-alias test): 2
```
TestGuidedInitDeterministicPositionalEnvironmentAliases/-e
TestGuidedInitDeterministicPositionalEnvironmentAliases/--environment
```

total `--- FAIL:` lines in the log: 16 (14 top-level + 2 nested subtests)
single shared failure reason across the 13 command tests: `target "company-dev" is not configured`
one distinct reason for the fourteenth: `second process was not rejected fail-closed on the shared provider owner; exit=exit status 1 output:` (TestSharedBackendReconcileRejectsSecondProcess, application_lifecycle_lock_test.go:155)

package result line in the same log:
```
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	400.032s
ok  	github.com/mcpdev80/baseharbor/conformance/provider/v1	0.317s
ok  	github.com/mcpdev80/baseharbor/contracts	1.047s
... (remaining packages ok; see full log) ...
```

## 6. root cause (read-only ci.yml witness, not edited)

`gh api repos/mcpdev80/baseharbor/contents/.github/workflows/ci.yml?ref=dea88c8f2caa2db93c1216c619993e444080a9d2`
Relevant trigger surface (verbatim, lines 6-11):
```
  workflow_dispatch:
  push:
    branches:
      - 'runtime-validation/ci/**'
      - 'runtime-validation/source-preflight/**'
      - 'runtime-validation/ha/**'
```
`develop` is not in the `push` branch list, so a plain push on develop never fires the workflow; the unit-test job only ran because this run was a `workflow_dispatch`. The 46 commits that the owner-merge of PR #1704 brought onto develop are therefore unit-test-unverified on develop. Owner-scope file: `.github/workflows/ci.yml` lines 7-11 — reported to owner, not edited.

## 7. regression witness (compare against a prior unit-tested head)

Counterfactual head: `fb841c2c27c9` (PR run 44912542526, conclusion success). Executed matrix jobs `PR · Go unit · cli-{0,1,2,3,packages,owner}` at that head.

- `gh api repos/mcpdev80/baseharbor/actions/jobs/{136871272685,136871272705,136871272708,136871272739,136871272762,136871272803}/logs` fetched, BOM-stripped.
- distinct `--- FAIL:` lines across those six logs: 0
- cli-0 summary line at that head:
```
PASS cli-0: 456 passed / 13 intentionally skipped / 469 discovered; CLI inventory total=1822
```

Conclusion: the 14 failing tests pass at `fb841c2c27c9` and fail at develop `dea88c8f2caa`. This is a regression introduced on develop (consistent with the ~46 commits landed by the PR #1704 owner-merge), not a pre-existing baseline.

## 8. verdict

- `gh run view 44913143056 --repo mcpdev80/baseharbor --json status,conclusion`:
```
{"conclusion":"failure","status":"completed"}
```
- develop IS red at head `dea88c8f2caa2db93c1216c619993e444080a9d2` in the unit tests: the `validate` job of hosted run 44913143056 (event=workflow_dispatch, headSha=dea88c8f2caa) fails with 14 distinct top-level `--- FAIL:` names in package `github.com/mcpdev80/baseharbor/cmd/baha` (16 total `--- FAIL:` lines including 2 nested subtests).
- develop is NOT green in the unit tests at this head.

## 9. cleanliness (docker ps -a, own pid)

before (pid 3957496):
```
CONTAINER ID   IMAGE     COMMAND   CREATED    STATUS    PORTS     NAMES
```
(none)

after (this evidence, no containers started on this host — hosted GitHub-runners only, no docker/podman test on the coordinator host per owner directive):
```
CONTAINER ID   IMAGE     COMMAND   CREATED    STATUS    PORTS     NAMES
```
(none)

## 10. repo-rule compliance

- No product file changed. No `.github/**` file touched (owner scope).
- No commit to baseharbor, no PR, no merge.
- No `go test ./...` / `go test ./cmd/baha/` on the coordinator host (hosted-run path only, per TEST RUNNER RULE).
- No subagents (4.8): every command ran in this session.
- No git stash; no `codeman agent post` into other sessions.
- Planning repo remote witness (before first evidence commit):
```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```
- Evidence path is baseharbor-plan only (see §11).

## 11. evidence on origin/main (pre-END witness)

as second-to-last action:
```
git -C baseharbor-plan fetch origin main
git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 0428-208-develop-ci-evidence
```
ACTUAL output (after commit 2865cab17, pushed 5066fad34..2865cab17):
```
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/r28-welle4-2026-11-21/develop-postmerge-ci/0428-208-develop-ci-evidence.md
```
evidence path IS present on origin/main. commit 2865cab17 on main; pushed to origin/main.

## END

END_DONE 0428-208-devci: develop head dea88c8f2caa2db93c1216c619993e444080a9d2 is RED in unit tests (run 44913143056, 14 distinct failing tests); evidence written to evidence/r28-welle4-2026-11-21/develop-postmerge-ci/0428-208-develop-ci-evidence.md
