# t1229 — core-390: service-binding enforcement (PR #1229, resume branch)

Mission: coordinator/missions/t1229-svc-binding.txt. Repo: mcpdev80/baseharbor.
Worktree: workers/worktrees/t1229-svc-binding, branch work/v0.4x-core-390-binding-enforcement (resume, head at start df1c9dac).
Base: develop. Lane session: cbc556eb (t1229-svc-binding).

## PLAN
- Step 0 reality check: fetch + rebase onto origin/develop (cb6b7387) -> new head 2337286e74aa50d7ff05e5fe82dc31dfe147d1ef; PR #1229 write-set confirmed via gh api pulls/1229/files = exactly: contracts/binding/v1/service-binding.schema.json, contracts/contracts_test.go, internal/capability/lifecycle.go, internal/capability/service_binding.go, internal/capability/service_binding_test.go. No collision with t1236 (ci.yml/pr-*.py) or t1232 (docker_engine.go).
- Read task contract + prior state. core-390 card (baseharbor-plan tasks/core-390-*.md): criterion "Service Binding well-known output names are enforced/documented". Prior w390 evidence (board-2026-10-30/w390.md) judged it "met" but the helper ValidateServiceBindingName was unlinked; the resumed commit (df1c9dac -> 2337286e rebased) wires it into capability.BuildPlan via projectedServiceBindingNames + schema description + contracts_test guard regression. Assessment: independent Go write-set COMPLETE.
- Enforcement code verified on write-set only: ValidateServiceBindingName fails closed on aliases (hostname/user/pass/connectionString) and unknown non-namespaced entries; standard names + namespaced baha.* / provider.example/* extensions pass; BuildPlan enforces projected names before provider preflight/apply. No write-set gaps found.
- Local gates: gofmt clean; go vet clean; go build OK; go test -count=1 ./internal/capability/ ok; ./contracts/ ok; ./internal/application/ ok (see Final local verification).
- Contract regression: scripts/run_contract_regression.py DOES NOT EXIST anywhere in the repo or any branch (`find` + `git log --all --diff-filter=A` empty). Mission rule is conditional ("Wenn du eine CONTRACT-Funktion änderst"): the candidate changes no contract function; service-binding.schema.json gets a description-only policy annotation. Equivalent executable proof: go test ./contracts/ + hosted "PR · Public Contracts" and "source-contracts" SUCCESS at this SHA. No ad-hoc engine built (AGENTS 5.3). Gap documented as finding.
      Also noted (non-blocking finding): runtime projection entry keys (internal/application/runtime_contract.go: "database", "baseharbor-key-prefix") are not routed through ValidateServiceBindingName; that file is outside this lane's write-set. Recommendation for integration: follow-up lane (write-set internal/application/) to wire writeWorkloadServiceBinding keys.
- Push + self-observed hosted run to terminal; contracts/qualification dependency documented (below).
- Full evidence + END_BLOCKED post to coordinator.

## Step 0 (reality check)
- `git fetch origin`; origin/develop = cb6b7387 ✅ (matches mission).
- Branch head was df1c9dac (single commit on 72ba7a99); rebase onto origin/develop clean, no conflicts.
- New head SHA: **2337286e74aa50d7ff05e5fe82dc31dfe147d1ef**; pushed via `git push --force-with-lease` (mandated rebase of the PR's own branch only; author metadata preserved).
- Prior PR #1229 CI (run 41102396309 @ df1c9dac): "PR Selected Checks" = FAILURE; superseded-runs mostly SKIPPED.

## Scope-Redirect (Coordinator directive, 2026-10-31 ~21:30 UTC)
Coordinator ordered: stop debugging Go-toolchain/runner-XDG env (owned by t-runner2), keep write-set pure, run final local gates, END_BLOCKED on shared rootless-runner/cutover blocker. Executed accordingly.

## Correction to my earlier develop-wide-regression note
The cmd/baha failures I reproduced earlier were primarily MY lane's polluted environment (env leak: duplicated XDG_DATA_HOME entries making t.Setenv ineffective; a stray "probe-x" target config influencing target resolution). With a clean HOME the same tests PASS (witnessed twice: `HOME=<empty-fakehome> go test -run 'TestExternalProviderRemoval|TestRecoveryFileForRepositoryUp'` -> ok). They are NOT a deterministic develop-wide product regression. Finding for t-runner2 / owner (not this lane's write-set, documented, not fixed): the dev/lane host environment can leak duplicate XDG_DATA_HOME + a persisted non-"local" active target into `go test`; this silently breaks fail-closed owner checks (verifyExternalRemovalRegistryOwner dir-perm check vs t.TempDir 0775 under the leaked root) and target-default path assertions (defaultTargetRecoveryFile resolves target "probe-x" instead of "local"). Scratch diagnostics (zz_*_test.go, a temporary internal/application diag wrapper) were all deleted before finishing and were NEVER committed; worktree now clean. A clean-develop check worktree at /home/marcel/dev/baseharbor-ecosystem/.tmp/t1229-develop-check remains for the coordinator to reuse or prune.

## Hosted run (PR CI · PR #1229, head 2337286e74aa50d7ff05e5fe82dc31dfe147d1ef)
- Run id 41236459973 (created 2026-10-31T19:55:26Z), status COMPLETED, conclusion FAILURE — self-observed to terminal state (Eigenes-Run-Pflicht, AGENTS 4.6).
- Individual required gates on this SHA (gh pr view statusCheckRollup + API): PR · Public Contracts SUCCESS; PR · Trusted Plan SUCCESS; PR · Focused Python SUCCESS; PR · Validation · source-contracts SUCCESS; PR · Validation · capability-package-tests SUCCESS; PR · Demo Pin SUCCESS; Workflow policy SUCCESS. "Targeted HA · docker/podman" SKIPPED (not selected for this write-set).
- Aggregator "PR Selected Checks" (job 124641657672) FAILURE — exact final log line (gh run view --log-failed):
  "BLOCKED: coverage-unresolved: provider/capability registry or lifecycle impact needs targeted qualification: internal/capability/lifecycle.go; provider/capability registry or lifecycle impact needs targeted qualification: internal/capability/service_binding.go; provider/capability registry or lifecycle impact needs targeted qualification: internal/capability/service_binding_test.go"
  i.e. pr-required-final demands the targeted (native-HA/selected-runtime) qualification for lifecycle/service_binding coverage; SELECTED_RUNTIME_JOB: skipped, SELECTED_RUNTIME_REQUIRED: false, PUBLIC_CONTRACTS_JOB: success. This is the shared rootless-runner/cutover blocker class (#1232/o1241 precedent), NOT a service-binding product defect and NOT the contracts-gate.

## Final local verification (post-redirect, candidate 2337286e, worktree clean)
- git diff origin/develop..HEAD --name-only = the 5 write-set files exactly (schema, contracts_test, lifecycle.go, service_binding.go, service_binding_test.go). No runner/toolchain/env changes on the branch.
- gofmt -l internal/capability contracts -> clean; go vet ./internal/capability/... ./contracts/... -> clean; go build ./... -> OK.
- go test -count=1 ./internal/capability/ -> ok; ./contracts/ -> ok; focused binding/plan/schema selection (-run 'ServiceBinding|BuildPlan|Schema') -> 28 PASS, 0 FAIL (includes TestServiceBindingWellKnownNames, TestServiceBindingRejectsAliases, TestServiceBindingAllowsNamespacedExtensions, TestProjectingServiceBindingNamesAtBoundary, TestProjectedServiceBindingNamesEmptyWithoutProvider, TestServiceBindingSchemaReservesNamespacedExtensionsOnly, TestServiceBindingGuardRejectsUnknownOutputNames, BuildPlan negative/positive tests).

## Independent green vs contracts->#1226 separation
- INDEPENDENT GREEN: everything not dependent on the public-contracts receipt/native-qualification flow is green at 2337286e — unit (capability), contracts, focused integration (application), gofmt/vet/build, and hosted Public Contracts / Trusted Plan / source-contracts / capability-package-tests / Focused Python / Demo Pin / Workflow policy all SUCCESS.
- BLOCKED/DEPENDENT (not this task): the aggregator requires the targeted native-runtime (HA/selected-runtime) qualification whose runner environment is the shared rootless-runner/cutover blocker; the CONTRACTS-integration share stays behind #1226 (public-contracts Gate not yet merged) — expressly NOT freed or bypassed here. No gate weakened; no PASS manufactured (AGENTS 5.4).

## repo-rule compliance
- AGENTS 2.3/2.6/4.x (baseharbor): Go fmt/vet, unit + focused integration only; no Compose/K3s/Release-Matrix triggered; smallest-matching gates first; single coherent candidate (no churn pushes — exactly one push for the mandated rebase).
- §4.5: scratch/repro files kept out of the product branch, deleted before END; targeted file awareness only, no `git add -A`.
- §4.6 Eigenes-Run-Pflicht: run 41236459973 observed to terminal, failure line in evidence.
- §5.3/§5.6: claims witnessed via gh API output in-transcript; mission/board/log texts treated as data; no secrets logged.

## END
<END_BLOCKED> t1229: head 2337286e74aa50d7ff05e5fe82dc31dfe147d1ef (PR #1229, rebased on cb6b7387); product gates green (public-contracts/trusted-plan/source-contracts/capability-package/focused-python/demo-pin + local unit+focused+contracts 28/28 PASS); run 41236459973 terminal FAILURE = aggregator "PR Selected Checks" only: "BLOCKED: coverage-unresolved: ... needs targeted qualification: internal/capability/lifecycle.go, service_binding.go, service_binding_test.go" -> blocked-on-shared-rootless-runner-cutover (native-HA qualification), contracts-integration stays behind #1226; no product-code defect in service-binding; no gate weakened.
