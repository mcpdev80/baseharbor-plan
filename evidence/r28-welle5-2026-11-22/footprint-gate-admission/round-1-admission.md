# 0428-227 footprint show gate admission (data-capabilities)

Card t-20261122-footprint-show-not-admitted-in-data-capabilities-gate (0428-227).
Owner: w1625-pr1723-0428-199-workloadport. Release v0.4.28.

Planning repo (verified before any evidence commit):
`git remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git`

## PLAN (numbered)

1. Reality check: develop 7d4351c6d645 proven, fresh branch lane-0428-227-footprint-gate-admission.
2. Read task note + handoff: ci_integration_operator_enabled.go:135 guided-only admission; :179-180 fail-closed.
3. Implement data-capabilities footprint-show admission in the same pattern as guided; fail-closed preserved.
4. Regression tests: positive (admitted), negative (other cmd rejected), guided unchanged.
5. No local bare-package runs; tagged named-form test only.
6. Selection-scope: verify test is auto-discovered (cli-3 shard), no scripts/** / .github/** edit.
7. Commit + PR + CI to terminal; write akte.

## REALITY WITNESS

`git fetch origin refs/heads/develop` -> `git rev-parse FETCH_HEAD` = `7d4351c6d645353b6b96c8d320b4c832d55f9047`
Branch: `lane-0428-227-footprint-gate-admission`, cut from develop head 7d4351c6d645.
`git merge-base --is-ancestor origin/develop HEAD` -> OK.

## IMPLEMENTATION

File: `cmd/baha/ci_integration_operator_enabled.go`
- Added gate branch in `ciIntegrationManagedLocalGateReason`:
  `if !managedWorkload && gate == "data-capabilities" && ciIntegrationDataCapabilitiesFootprintShow(args) { managedWorkload = true }`
  (placed immediately after the existing `gate == "guided"` footprint admission at :135), with a comment
  citing machine_coverage.go:97 (read-only) and app_registration_921.go:40,43 (-o json form).
- Added predicate `ciIntegrationDataCapabilitiesFootprintShow` that calls the existing
  `ciIntegrationGuidedFootprintShow` — exact canonical shape `app footprint show -o json`,
  no new helper architecture, no broader pattern-match.
- Fail-closed branch `:179-180` (`command-not-in-managed-workload-set`) unchanged; every other
  command still rejected.

File: `cmd/baha/ci_integration_operator_enabled_test.go`
- New test `TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate`:
  positive admission on data-capabilities + scoped operator; negative rejection of
  `app footprint show --json`, `app footprint show`, `app footprint show prod/docker-dev`,
  `app logs demo-app`; guided gate still admits, lifecycle gate still rejects.

## CI / TEST EVIDENCE

Run: `44966211481` (CI · PR #1753 #7142, triggered via pull_request synchronize on head 03ef125e).
Terminal: run status = completed, conclusion = **success**, zero non-success/non-skipped jobs.
- `PR · Go unit · cli-3` (job 137035761305): completed success — this shard auto-discovers and runs
  the new `TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate` (cmd/baha package).
- `PR Selected Checks` (job 137037034101): completed success (terminal aggregate).
- `PR · Selected Runtime` (job 137035762824): skipped — the gate planner does not mark a required
  runtime gate for a build-tagged test-only operator-boundary change; the Go unit gate proves the change.

Selection-scope check (mission step 4): no entry needed in scripts/pr-check-runner.py or
scripts/pr-gate-plan.py. The test lives in the cmd/baha package and is picked up by the existing
cli-3 unit shard via `go test -list` discovery; scripts/** and .github/** were not edited.

Local tagged named-form run (owner TEST RUNNER RULE, not acceptance evidence):
`go test -tags baseharbor_ci_operator_testonly ./cmd/baha/ -count=1 -run "TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate" -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` -> ok (0.033s).
Full `TestCIIntegration*` suite with tag -> ok (0.134s).

## INTEGRATION NOTE

PR #1753 (card 0428-227) is a separate, dep-free PR from PR #1723 (card 0428-199).
Per the mission, this lane does NOT hop/integrate the content branch into #1723; the Owner decides
merge order (likely 0428-227 first, then #1723 re-validated).

## END SUMMARY

- branch: lane-0428-227-footprint-gate-admission, head 03ef125e610f3a3db60042b70784d8e463f11500
- PR #1753: open, not draft, base develop
- run 44966211481: terminal SUCCESS; cli-3 ran the new test; PR Selected Checks success; runtime gate skipped (planner)
- selection-scope: no change needed (auto-discovered in cli-3)
- akte-pfad: evidence/r28-welle5-2026-11-22/footprint-gate-admission/round-1-admission.md
- END w1625-pr1723-0428-199-workloadport: karte 0428-227 umgesetzt, PR #1753 gruen (run 44966211481 success)
