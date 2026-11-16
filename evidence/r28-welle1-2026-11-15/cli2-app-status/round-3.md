# round-3 — 0428-062 cli2-app-status regression (diagnosis / STOP)

- Card: t-20261114-r28-cli2-app-status (0428-062)
- Mission: /var/tmp/missions/mission-status-r3-regression.md
- Lane: lane-0428-062-cli2-app-status
- Candidate chain: PR #1614, base lane-0428-059-cli2-source-model
- Report type: witness-backed diagnosis, no product change (scope STOP)

## PLAN
- Confirm a runtime cell exists (docker daemon present, no podman).
- Verify remote heads via git ls-remote; base 6377f1b22 -> head 80d4df52e, diff = exactly one commit.
- Inspect the one commit (80d4df52e): it touches ONLY two test files, both acceptance-gate additions.
- Reproduce both target tests in isolation and in the full cli-1 shard under BASEHARBOR_CI_RUNTIME_INTEGRATION=1.
- Decide scope: a production fix in 062-owned files is only warranted if the head commit introduced a production change that breaks the tests; a core-test edit is forbidden (STOP+file:line).
- Run build/vet/gofmt; record witnesses.
- No .github/**, no merge, no ready_for_review, no force-push, no subagent.

## BASE ATTESTATION
Authoritative planning repo (wrong-zone witness):
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```
Product remote truth (NOT the quarantined workers checkout):
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin refs/heads/lane-0428-062-cli2-app-status
80d4df52e913e4472334a5f257fe868d26d5976e  refs/heads/lane-0428-062-cli2-app-status
```
Base cut-from witness:
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor rev-parse 6377f1b22^~0
6377f1b2298f104d54b67236177a1d3c8c26b2d2
```
Ancestry (base is ancestor of the CI head):
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor merge-base --is-ancestor 6377f1b22 80d4df52e && echo OK
OK
```

## FINDING: the two target tests DO NOT reproduce on the CI head

The red CI run 43840657678 (head 80d4df52e, cli-1 shard) reported:
- cmd/baha/management_remote_mutation_test.go:58 `unsupported or unapproved remote mutation was accepted`
- cmd/baha/control_plane_stop_impact_test.go:150 `CLI stop bypass or JSON progress leak`

On THIS host, on the EXACT head 80d4df52e, both tests PASS. Full shard witness:
```
--- PASS: TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse (0.78s)
--- PASS: TestRemoteMutationArgumentsFailClosed (0.01s)
    --- PASS: TestRemoteMutationArgumentsFailClosed/apply/demo (0.01s)
    --- PASS: TestRemoteMutationArgumentsFailClosed/apply/ (0.01s)
    ... (all 28 subtests PASS) ...
ok  	github.com/mcpdev80/baseharbor/cmd/baha
```
Command:
```
cd /home/marcel/dev/baseharbor-ecosystem/baseharbor
BASEHARBOR_CI_RUNTIME_INTEGRATION=1 TMPDIR=/var/tmp/r3-full \
  go test ./cmd/baha -count=1 -timeout 15m -v > /var/tmp/r3_full_ci.log
```
The run is the complete cli-1 shard. The only 7 FAIL lines in that run are runtime/trust-plane provisioning tests that fail because a BaseHarbor Core is already running on the shared engine on this host (host artifact, fail-closed by design):
```
--- FAIL: TestRepositoryWorkflowRealLifecycle (3.29s)
--- FAIL: TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (0.10s)
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (0.10s)
--- FAIL: TestRepositoryComposePinnedWorkloadLifecycleInCI (0.10s)
--- FAIL: TestRepositoryBuildWorkloadRebuildsSourceChangesInCI (0.10s)
        --- FAIL: TestBootstrapPanickingHelperCallerSubprocess (0.00s)
        --- FAIL: TestBootstrapSetupFailureSubprocess (0.00s)
```
These are unrelated to the mission's two target routes and are caused by `BaseHarbor Core is already running on this engine for target w169-ci-bootstrap-1698744b` — a leftover CI-bootstrap container, not a product or lane-062 regression.

## ROOT-CAUSE ANALYSIS (why there is no 062 production fix)

The base..HEAD diff is exactly one commit:
```
80d4df52e test(cmd/baha): gate two native Core lifecycle tests behind acceptance marker
```
`git show --name-only` for 80d4df52e changes ONLY:
```
cmd/baha/app_edit_apply_test.go        (+3)
cmd/baha/management_core_git_candidate_test.go (+12)
```
Neither file is a product file, and neither is one of the two failing routes. git blame on the failing lines:
```
management_remote_mutation_test.go:57-58  532278d565 (Marcel, 2026-11-09)  -- predates head
control_plane_stop_impact_test.go:149-150 84183b9919 (Marcel, 2026-10-15) -- predates head
```
So the head commit introduced NO production change; the two failing routes are core files committed by Marcel long before this branch. The r2-placement wiring (declaredVersionServices / collectSourceModelComponents / componentRowsForRecord) that round-2 landed sits in cmd/baha/app_versions_view.go, app_versions_command.go, app_version_view.go — completely separate from the remote-mutation validator and the control-plane-stop consent path that these two tests exercise.

The tests pass in isolation on both base 6377f1b22 and head 80d4df52e:
```
base  6377f1b22:  go test ./cmd/baha -run 'TestCoreStopCLIJSONAndMCPExpose...|TestRemoteMutationArgumentsFailClosed' -> ok
head  80d4df52e:  same run -> ok
```
The mission's "global state / registration side-effect" leak can only appear under a shared per-run CI data root (BASEHARBOR_CI_RUNTIME_INTEGRATION=1 in TestMain, cmd/baha/runtime_integration_test_support_test.go:115-127) when a PRIOR test registers a deployment/registry entry for the docker-dev target that a LATER test re-reads. I could not trigger that ordering on this host: the full shard run above keeps both target tests green. The two failures the CI run 43840657678 reported are therefore a host/runner-state condition, not a lane-062 regression on the pinned head.

## SCOPE DECISION

Step 2 of the mission fixes ONLY in 062-owned files and forbids editing core tests (any required core-test edit => STOP+file:line). There is:
- No production change between base and head to regress, so a production fix in 062-owned files would be invented and could not correspond to any causal change.
- The failing routes are core test files (old Marcel commits); editing them is explicitly out of scope.
- The failing tests are green on the exact pinned head, so no correctness repair is warranted.

Per the mission's own guard (no local-getrickste 'korrektur'; if a core-test edit were needed: STOP+file:line), this lane STOPS with a finding for Owner/CI-run triage rather than writing an ungrounded change.

## VERIFICATION WITNESSES (current head 80d4df52e)
- gofmt: `gofmt -l cmd/baha/management_remote_mutation.go cmd/baha/control_plane_stop_impact.go` -> empty (clean)
- build: `go build ./...` -> rc=0
- vet: `go vet ./cmd/baha/` -> rc=0
- Target tests: both PASS in isolation and in the full ci-integration shard (witness above, /var/tmp/r3_full_ci.log)

## repo-rule compliance
- No product files touched. No .github/**. No test-file edits. No push, no merge, no ready_for_review, no force-push, no retarget. No subagent.
- This is a diagnosis + STOP finding for Owner triage, exactly as the mission's guard permits.

## CLEANLINESS
- No docker/podman compose project or container started by this lane. The failing TestRepository* routes fail only because a pre-existing CI-bootstrap Core (`bh-w169-ci-bootstrap-...`) already occupies the shared engine; this lane started none.
- docker ps --format '{{.Names}}' at END (witness of what this lane did NOT start):
```
docker ps --format '{{.Names}}'
```

## END
END_DONE mission-status-r3-regression.md: 0428-062 regression r3 STOP — the two CI-red target tests (management_remote_mutation_test.go:58, control_plane_stop_impact_test.go:150) DO NOT reproduce on the exact pinned head 80d4df52e: they PASS in isolation AND in the full cli-1 shard under BASEHARBOR_CI_RUNTIME_INTEGRATION=1 (witness /var/tmp/r3_full_ci.log). The base..HEAD diff is exactly one commit (80d4df52e) that touches ONLY two acceptance-gate TEST files (app_edit_apply_test.go, management_core_git_candidate_test.go), no product code, and neither failing route is a 062 file (blame 532278d565 / 84183b9919, old Marcel core commits). r2 placement wiring (app_versions_*.go) is unrelated to the remote-mutation validator / control-plane-stop consent path. No 062-owned production fix is warranted and core-test edits are out of scope; the 7 local FAILs are a host artifact (existing Core on shared w169-ci-bootstrap engine), not this lane. Fix candidate if the CI rerun still fails: the leak is shared per-run CI data-root state (TestMain runtime_integration_test_support_test.go:115) — root-causing registration test, still a core-test concern outside 062. Candidate head 80d4df52e913e4472334a5f257fe868d26d5976e, branch lane-0428-062-cli2-app-status, draft PR https://github.com/mcpdev80/baseharbor/pull/1614, no .github/** change, no product edit.

## second-to-last witness (origin/main evidence presence)
Committed to planning main as e507b411, merged into origin/main (receipt ff3c947467). Verified presence:
```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main -- evidence/r28-welle1-2026-11-15/cli2-app-status/
evidence/r28-welle1-2026-11-15/cli2-app-status/act-luna-r1.md
evidence/r28-welle1-2026-11-15/cli2-app-status/round-1.md
evidence/r28-welle1-2026-11-15/cli2-app-status/round-2.md
evidence/r28-welle1-2026-11-15/cli2-app-status/round-3.md
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan merge-base --is-ancestor e507b411 origin/main && echo present
present
```
