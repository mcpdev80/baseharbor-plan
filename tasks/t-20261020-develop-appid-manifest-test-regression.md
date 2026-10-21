---
id: t-20261020-develop-appid-manifest-test-regression
type: bug
areas: [ci, contract]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Flash (codeman w1-baseharbor)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1008"]
sources: []
blocker: "pr-gate-plan.py has no test-only lane: test fixture fix landed (#1008) but CI coverage gate fails closed (coverage_status=unresolved, empty selected_gates); needs a policy lane mapping audited _test.go fixture changes to static package validations."
resolution: ""
evidence: []
---

- [ ] t-20261020-develop-appid-manifest-test-regression · CI/Contract: develop integration tests author app.id in developer manifests; product fix landed (#1008) but CI coverage gate (pr-gate-plan.py) has no test-only lane and fails closed — blocked on policy lane #task #release/v0-4-26 #status/blocked #view/blocked #area/ci #area/contract #kind/bug
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor) · **Priority:** high  
    **PR:** [baseharbor#1008](https://github.com/mcpdev80/baseharbor/pull/1008)  
    **Blocker:** pr-gate-plan.py has no test-only lane: test fixture fix landed (\#1008) but CI coverage gate fails closed (coverage\_status=unresolved, empty selected\_gates); needs a policy lane mapping audited \_test.go fixture changes to static package val…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Flash (codeman w1-baseharbor)  
**Priority:** high  
**PRs:** [baseharbor#1008](https://github.com/mcpdev80/baseharbor/pull/1008)  
**Source:** 
<!-- /generated:links -->

## Goal

`origin/develop` (bb91fbc3) fails `TestRepositoryWorkflowRealLifecycle` because the test fixture writes `app.id` into a developer manifest while `parseAppField` (manifest_parse.go:260) rejects non-canonical `app.id` (contract: app.id is system-owned per #872). This breaks the mandatory docker-runtime check that #998 needs for its final CI.

## Scope

- Update the outdated developer-manifest fixture(s) to the accepted contract (no manual `app.id`; explicit canonical path only where genuinely required).
- Test-side changes only unless the parser itself contradicts the accepted #872 contract.
- Green docker-runtime integration evidence via CI (durable run, not VM one-off).

## Acceptance

1. `TestRepositoryWorkflowRealLifecycle` PASS in GitHub Actions on develop head.
2. No contract semantics change; parser behavior stays fail-closed for non-canonical app.id.
3. Independent local review + evidence links on this card.

## Handoff / status — 2026-10-20 (BLOCKED)

Product fix landed and pushed: branch `fix/t-20261020-develop-appid-manifest`
(HEAD `0e213d42`), draft PR #1008 (base `develop`):
https://github.com/mcpdev80/baseharbor/pull/1008

- Fixture diff: removed authored `app.id` from the 3 workload test fixtures in
  `cmd/baha/app_workload_integration_test.go` (lines 40/178/311); parser
  unchanged, stays fail-closed. `app apply`/`app init` generate the canonical
  identity.
- Added manifest regression tests (`internal/application/manifest_test.go`)
  proving both contract directions.
- Local: `go vet` + full `cmd/baha` (all pass except the pre-existing
  `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` compose/consent
  timeout, reproduced on clean develop) + `internal/application` pass. The
  compose/build workload integration tests need rootless docker (local socket is
  rootful; `DOCKER_MODE` override was removed in `d2bca4ea`); the underlying
  `app.id` error is proven by the parser unit check.

CI blocked (run `39430265422`, trusted plan `pr-plan.json`):
`coverage_status: unresolved`, `selected_gates: []`. All 4 static validations
(cli-build, cli-guided-tests, cli-vet, source-contracts) pass; `PR Selected
Checks` fails closed. Root cause is a pre-existing policy gap, not the product
fix: `scripts/pr-gate-plan.py` classifies every `cmd/baha/*.go` and
`internal/application/*.go` change (including test files) as needing a qualified
native runtime gate but emits an empty gate list, so `runtime_required` stays
false and the docker-runtime acceptance job never runs. `scripts/pr-required-final.py:24`
fails closed on `coverage_status != 'resolved'`.

Action for Marcel / Codex 6.1: add a lane in `pr-gate-plan.py` for audited
test-only fixture changes mapped to the static package validations already
emitted (`go test ./cmd/baha`, `go test ./internal/application/... ./contracts/...`,
`go vet`, `go build`), so the coverage gate resolves without an atomic runtime
matrix. Evidence: `evidence/board-2026-10-20/o1-appid-develop-fix.md`.

## Notes

Local evidence: `evidence/board-2026-10-19/p22-nativejob.md`. Found by p22 split triage on 2026-10-20; pre-existing on develop, surfaced via #998's mandatory CI.

### 2026-10-20 - lane status

- Fix delivered as draft PR #1008 (test-only, parser untouched). CI shows the coverage-unresolved bootstrap contradiction this card surfaced; o1 investigating legitimate green path vs documented wait-on-#1007.

### 2026-10-21 — CI policy correction in review

- Product fixture remains in draft PR [#1008](https://github.com/mcpdev80/baseharbor/pull/1008), source `0e213d42c74cfdb91964592c17e3914a848207b9`.
- Narrow CI policy correction is now published as draft [#1009](https://github.com/mcpdev80/baseharbor/pull/1009), source `a0dcacf93c9a6922163f2718f374f05e1e5e9e3e`.
- Exact two-file/status match, reviewed-source merge-chain proof and hosted validations; no generic `_test.go` exemption or native runtime bypass. Regression tests added for missing/extra/deleted/unreviewed/stale inputs.
- GitHub Actions run [39582522944](https://github.com/mcpdev80/baseharbor/actions/runs/39582522944) started; result pending when this handoff was written. Do not mark accepted or unblock core-921 until valid current CI and final Docker lifecycle evidence exist.
- Release v0.4.26 remains **active, not pre-release-ready**; next: qualify #1009, integrate policy, requalify #1008, run native Docker proof, then finish core-921, Podman recovery, core-922 and core-923.

### 2026-10-21 — CI policy accepted and merged

- [#1009](https://github.com/mcpdev80/baseharbor/pull/1009) merged into `develop` as `b7f920ab6b7890a1a9ca7fdf5b0631c172b13d34` after successful GitHub Actions [39582522944](https://github.com/mcpdev80/baseharbor/actions/runs/39582522944): Trusted Plan, workflow policy, planner tests, CI policy, focused Python, executor/verifier tests and PR Selected Checks all successful.
- #1008 product fixture remains open and needs fresh CI against updated trusted `develop`; native Docker acceptance and final release proof remain pending. Do not mark this task done based only on the policy merge.
