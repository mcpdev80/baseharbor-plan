# 0428-279: #171 + #1826 diff, dependency and disposition (read-only)

## PLAN
- 1. Record origin/develop SHAs for baseharbor-demo and baseharbor; remote -v witnesses
- 2. #171 live state: gh pr view 171, ls-remote headRefName, pr diff --name-only + annotation hunk
- 3. Check whether 025ce84 content already in demo develop (ancestry + content diff); search destructiveHint in origin/develop log/tests/mcp
- 4. #1826 live state: gh pr view 1826, gh pr checks 1826, ls-remote lane-0428-279-mcpcontract, pr diff --name-only
- 5. Establish dependency: does #1826 consume the #171 annotation; determine real order #171 -> #1826 -> change-2 or independent
- 6. Re-confirm static/mcp blocker: ci_integration_operator_enabled.go:96-103 lines; outline change-2 (A+B2) minimal files/owner-scope flags as Befund
- 7. Disposition recommendation for #171 and #1826 (worker-actionable vs owner-blocked split) with proof
- 8. Cross-check write-set disjointness of #1826 vs #1812/#1819/#1820 and #1823 secret_*
- 9. Write this evidence file in baseharbor-plan, commit+push targeted add, origin/main witness
- 10. END post to coordinator session

## 0. Remote / base witnesses (read-only)

baseharbor-demo:
- origin URL: https://github.com/mcpdev80/baseharbor-demo.git
- origin/develop: c23bd9ac58919302ffad3a43f43afb1a34bfbc96
- origin/main: df4867c7540774eba8b8811cb64946b4adc0c8ab
- PR #171 headRefName: lane-0428-279-mcpcontract-fix @ 025ce84e5d12838ca5622dc69161623350948f08

baseharbor:
- lane-origin URL: https://github.com/mcpdev80/baseharbor.git (also as 'origin' and 'https://github.com/mcpdev80/baseharbor.git' anonymous fetch)
- origin/develop / lane-origin/develop: f14fb87c8f5afd91168e4f174d620c9f00e6341e
- PR #1826 headRefName: lane-0428-279-mcpcontract @ 6589a37b00273913e9e14fd9832e93b72630f106
- refs/pull/1826/head: 6589a37b00273913e9e14fd9832e93b72630f106

## 1. #171 live state and content-equality

gh pr view 171 (json):
{"baseRefName":"main","headRefName":"lane-0428-279-mcpcontract-fix","headRefOid":"025ce84e5d12838ca5622dc69161623350948f08","isDraft":false,"mergeStateStatus":"DIRTY","mergeable":"CONFLICTING","reviewDecision":"","state":"OPEN","title":"test(mcp): add baseharbor.app.pull to demo MCP contract expectations (0428-279)"}

git ls-remote origin refs/heads/lane-0428-279-mcpcontract-fix:
025ce84e5d12838ca5622dc69161623350948f08	refs/heads/lane-0428-279-mcpcontract-fix

gh pr diff 171 --name-only:
- tests/guided/drive.py
- tests/guided/new_edit.py
- tests/guided/test_consent_capture.py
- tests/mcp/run.sh

gh pr checks 171:
no checks reported on the 'lane-0428-279-mcpcontract-fix' branch

git merge-base --is-ancestor 025ce84 origin/develop:
no

git log --oneline 025ce84:
025ce84 test(mcp): remove baseharbor.app.pull from destructive set; it is SafetyMutating (destructiveHint=false) per product contract 0428-279
3cb6e20 test(mcp): add baseharbor.app.pull to demo MCP contract expectations (0428-279)
c23bd9a test(mcp): sync Perses tool contract expectations (#169)

Content comparison:
- git diff 025ce84 origin/develop --name-only shows tests/mcp/run.sh (and nothing else).
- git diff 025ce84 origin/develop -- tests/mcp/run.sh reveals two substantive deltas:
  1. Perses tools: in 025ce84 the perses.{status,enable,disable,remove} entries appear earlier (line 73-76) than in origin/develop (line 103-106); the destructive/read_only set membership of perses.status/remove is identical but placed differently.
  2. baseharbor.app.pull: added to expected in 025ce84 (and absent from read_only and destructive); absent from expected in origin/develop.
- Conclusion: 025ce84 is NOT an ancestor of origin/develop and its content is NOT equal to origin/develop; it is ahead by the expected-set addition plus a position change for perses.
- git log --oneline origin/develop --grep=destructiveHint -- tests/mcp: empty (no commit on develop contains "destructiveHint" in its message touching tests/mcp).
- git log --all --oneline -- tests/mcp/run.sh shows 3cb6e20 and 025ce84 as the only commits outside origin/develop that touch tests/mcp/run.sh.

## 2. #1826 live state and content

gh pr view 1826 (json):
{"baseRefName":"develop","headRefName":"lane-0428-279-mcpcontract","headRefOid":"6589a37b00273913e9e14fd9832e93b72630f106","isDraft":false,"mergeStateStatus":"BEHIND","mergeable":"MERGEABLE","reviewDecision":"","state":"OPEN","title":"docs(release): re-pin v0.4.28 demo-ref for static/mcp annotation fix (0428-279)"}

git ls-remote lane-origin refs/heads/lane-0428-279-mcpcontract:
6589a37b00273913e9e14fd9832e93b72630f106	refs/heads/lane-0428-279-mcpcontract

gh pr diff 1826 --name-only:
- docs/releases/v0.4.28.demo-ref

gh pr diff 1826:
diff --git a/docs/releases/v0.4.28.demo-ref b/docs/releases/v0.4.28.demo-ref
index 295815853..3be44e644 100644
--- a/docs/releases/v0.4.28.demo-ref
+++ b/docs/releases/v0.4.28.demo-ref
@@ -1 +1 @@
-c23bd9ac58919302ffad3a43f43afb1a34bfbc96
+025ce84e5d12838ca5622dc69161623350948f08

git log --oneline origin/develop..6589a37b:
6589a37b0 docs(release): re-pin v0.4.28 demo-ref to 025ce84 (demo fix: app.pull removed from destructive set, 0428-279)
a4dffedb9 docs(release): re-pin v0.4.28 demo-ref to demo fix that adds baseharbor.app.pull to static/mcp contract (0428-279)

git merge-base --is-ancestor f14fb87c8f5afd91168e4f174d620c9f00e6341e 6589a37b: no (the branch is not up-to-date with develop; mergeStateStatus=BEHIND).

gh pr checks 1826 (selected):
- PR Selected Checks: pass (run 45412208234, job 138512089129)
- PR · Go unit · packages / cli-0 / cli-1 / cli-2 / cli-3 / owner: pass
- PR · Focused Python: pass
- PR · Native gate plan: pass
- PR · Source format: pass
- PR · Trusted Plan: pass
- PR · Validation · go-build: pass
- PR · Validation · go-vet: pass
- Workflow policy: pass
- All other gates: skipping

## 3. Static/MCP blocker re-confirmation

cmd/baha/ci_integration_operator_enabled.go (at 6589a37b):
- 96: func ciIntegrationManagedLocalGateReason(args []string, target deployment.ResolvedTarget, targetErr error) string {
- 97: 	if targetErr != nil {
- 98: 		return "target-resolution-failed: " + targetErr.Error()
- 99: 	}
- 100: 	gate := strings.TrimSpace(os.Getenv("BASEHARBOR_DEMO_OPERATOR_GATE"))
- 101: 	runtime := strings.TrimSpace(os.Getenv("BASEHARBOR_TEST_RUNTIME"))
- 102: 	if gate == "" || gate != strings.TrimSpace(os.Getenv("GATE")) ||
- 103: 		(runtime != "docker" && runtime != "podman") || target.Name != "atomic-"+runtime+"-"+gate ||

runtime=static fails the "runtime != docker && runtime != podman" clause and therefore takes the "target-or-gate-mismatch" path: the test-only operator is NOT injected.

The demo static/mcp harness:
- baseharbor-demo/tests/mcp/run.sh asserts the server-emitted annotations.
- baseharbor-demo/tests/mcp/new-edit-static.py (the gate runner) invokes baha. Per the #1826 PR body it builds baha without -tags=baseharbor_ci_operator_testonly and does not set BASEHARBOR_DEMO_OPERATOR_GATE, so the synthetic-operator branch in the tagged file is never taken and the target-create step fails on the managed-operator boundary.

w95 option matrix (Befund, not execution):
- Option A (tag-build): add -tags=baseharbor_ci_operator_testonly to the baha build in tests/mcp/new-edit-static.py, or in the CI job that runs the static/mcp gate. File: line is in the demo repo / .github scope, so worker execution is blocked.
- Option B2 (demo-env): set BASEHARBOR_DEMO_OPERATOR_GATE, BASEHARBOR_TEST_RUNTIME, BASEHARBOR_TARGET, GATE in the static/mcp gate environment so that a tagged binary (option A) would be reached. Same scope restriction.
- Option B1 (REJECTED): would relax the operatorauth.LocalWorkloadOperation() fail-closed check in internal/operatorauth. Weaker than the contract.

## 4. Disposition recommendation

### #171 (baseharbor-demo)
- Obsolete / blocked:
  1. mergeable=CONFLICTING vs origin/develop (025ce84 not an ancestor, content diff exists).
  2. The PR body of #1826 explicitly says #171 "ADDs app.pull to the demo destructive set and would re-introduce this exact failure". Inspection of 025ce84:run.sh shows app.pull in expected but NOT in destructive (the "remove" commit is present); however, it also shows perses ordering different from origin/develop. The #171 branch is therefore stale relative to current develop and the #1826 body's claim is partially inaccurate.
  3. PR #171's base is main, not develop; it is missing the c23bd9a Perses sync.
  4. No CI checks are reported on the branch.
- Worker-actionable (under existing authorization): rebase lane-0428-279-mcpcontract-fix onto origin/develop, resolve the tests/mcp/run.sh conflict so that the final content is exactly 025ce84's app.pull-in-expected-and-not-destructive set, retarget the PR to develop if that matches the demo repo convention, and let CI run. If the result contradicts the #1826 body's annotation claim, that body needs updating.
- Strictly owner: no, unless the demo repo requires owner authorization for test contract changes.

### #1826 (baseharbor)
- Worker-actionable: rebase lane-0428-279-mcpcontract onto current develop (f14fb87c) and push. mergeStateStatus=BEHIND; the PR is otherwise MERGEABLE and its exact-head PR Selected Checks are green (run 45412208234).
- Owner-blocked: merge/close and the static/mcp gate qualification. Qualification depends on owner card 0428-283 / change-2 (static/mcp operator provisioning), which requires .github/** or product-auth changes (operator build tag / operator env contract) outside this card's write-set.

### Dependency chain
#171 (demo tests/mcp/run.sh content) -> #1826 (baseharbor docs/releases/v0.4.28.demo-ref re-pin) -> owner change-2 (0428-283 static/mcp operator provisioning).
The chain is real but not sequential in a blocking sense for the worker steps: both #171 and #1826 have independent rebase/refresh work that a worker can do today; the static/mcp gate cannot go green until owner change-2 lands.

## 5. Write-set disjointness

#1826 write-set (from gh pr diff --name-only):
- docs/releases/v0.4.28.demo-ref

#1812 write-set:
- .github/workflows/pre-release-runtime-suite.yml

#1819 write-set:
- internal/application/runtime_postgres.go
- internal/metrics/perses_dashboard_provision.go
- internal/metrics/perses_dashboard_provision_test.go

#1820 write-set:
- cmd/baha/app_broker.go
- cmd/baha/app_broker_compat_test.go

#1823 write-set (secret_*.go family):
- cmd/baha/secret_audit_test.go
- cmd/baha/secret_operations.go

Intersection with #1826: none. #1826 touches only docs/releases/v0.4.28.demo-ref; the chain PRs (#1812/#1819/#1820) and #1823 touch workflow, internal, cmd/baha and secret files respectively. Disjointness confirmed.

## 6. Cleanliness / policy

- No containers, images, compose projects, or networks were started or inspected on the host.
- No product tests, unit suites, scripts/ci-fast-check.sh, go test, or pytest were executed on the coordinator host.
- Only read-only git, gh, find, grep, sed, mkdir and file-write operations were used.
- The mission explicitly forbids PR/branch/CI modifications; none were made.

## repo-rule compliance

- Read-only desk: no edits, no PR changes, no CI trigger, no merge, no rebase.
- All claims are accompanied by file:line, gh JSON output, git ls-remote output or commit SHAs.
- Evidence file is in baseharbor-plan/evidence only.
- No subagents.

END DONE w110-0428-279-171826
