# w287 — Read-only gate-exposure matrix for the chain PRs

Lane: `w287-0428-284-gatematrix` (read-only census). Mission coordinator commission 2026-11-26.

## REALITY WITNESSES (read-only)

Remotes verified via `git ls-remote`:
- baseharbor develop tip: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (origin = https://github.com/mcpdev80/baseharbor.git)
- baseharbor main tip: `cddc81b34fe13d8befdde4c487b365a0309ba428`

No writes to any product or plan repo. No PR edits, no close/reopen, no CI trigger, no rerun, no workflow_dispatch, no merge, no card change, no `.github` change, no plan-main push. No local tests run. Work done against the shared `baseharbor` checkout read-only + read-only planner import.

Zero-mutation proof: this lane never committed to either repo; `git ls-remote` for both refs unchanged before/after (develop `ac7c970f…`, main `cddc81b3…`).

## PLAN (todo board + this akte)

1. ls-remote develop tip + list PRs with head SHAs/base/state/mergeable
2. per-candidate changed-file set (`git diff --name-status origin/develop...head`)
3. read `scripts/pr-gate-plan.py` on develop + heads that change it (1856, 1842); derive runtime_required/integration_required/public_contracts_required/native include
4. matrix: write-set class | 3 booleans | native include | 'PR Demo Pin' executes?
5. cross-check against real PR runs (per_page=100 incl attempts): name executed vs skipped
6. answer decision question (a/b/c)
7. akte: gh pr create against live main; report PR number; zero-mutation proof; cleanliness

## 1. CANDIDATES (ls-remote / gh)

| PR | title | state | head (ref=commit) | base | mergeable |
|----|-------|-------|-------------------|------|-----------|
| 1856 | fix(pr-gate): release-scoped demo-ref selector recognizes every active release | OPEN | de26af2ec727d35f1309cf0763aab3c8f2edcf5d | develop | MERGEABLE |
| 1812 | fix(ci): re-load missing runtime image before ORAS publish | OPEN | 0922888af8fd70be4049cec529c69aebc057a356 | develop | MERGEABLE |
| 1819 | 0428-181 wire Perses identity dashboard into export path | OPEN | b3c5055ad2566b639c2b0d4f4c2848b045221ebf | develop | MERGEABLE |
| 1820 | fix(0428-271): prove exact runtime broker commit in readiness probe | OPEN | 8f6b2444bdc9baabf4f492e930533c7c36406979 | develop | MERGEABLE |
| 1818 | fix(0428-078): consume real Perses probe for identity dashboard eligibility | OPEN | 20fc1cb7d49602dc7f8aa0004a7562a81311d78c | develop | MERGEABLE |
| 1833 | fix(0428-288): preserve Compose service IDs through workload preflight | OPEN | a7b0a48048c11d20234160eede941532ddc33156 | develop | MERGEABLE |
| 1855 | fix(0428-078): reissue Perses identity-keycloak (reviewed content, single-lane) | OPEN | 43326cf57f1a3a8d73f2b9289e8c5ad00b74782a | develop | MERGEABLE |
| 1650 | fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in | OPEN | 37c4d847ca377d1555163ac4791c8ba08b85de77 | develop | MERGEABLE |
| 1842 | chore(release): bump demo_ref pin to merged develop tip | CLOSED | 4f570ff966cd5e8d3043e8bd6363e1ea4e87d0d6 | develop | MERGEABLE |

develop base for all: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`.

## 2. WRITE-SETS (git diff --name-status origin/develop...head)

- 1856 (de26af2ec7): `M .github/workflows/ci.yml`, `M docs/releases/v0.4.28.demo-ref`, `M scripts/pr-check-runner.py`, `M scripts/pr-gate-plan.py`, `M scripts/test_pr_check_runner.py`, `M scripts/test_pr_gate_coverage.py` — scripts-routing + docs-pin
- 1812 (0922888af8): `M .github/workflows/pre-release-runtime-suite.yml` (+ .github/ci.yml from diff) — scripts-routing
- 1819 (b3c5055ad2): `M .github/workflows/pre-release-runtime-suite.yml`, `M internal/application/runtime_postgres.go`, `A internal/metrics/perses_dashboard_provision.go`, `A internal/metrics/perses_dashboard_provision_test.go` — product-code + test
- 1820 (8f6b2444bd): `M .github/workflows/pre-release-runtime-suite.yml`, `M internal/application/runtime_postgres.go`, `A internal/metrics/perses_dashboard_provision.go`, `A internal/metrics/perses_dashboard_provision_test.go` — product-code + test
- 1818 (20fc1cb7d4): `M cmd/baha/app_status_result.go`, `M internal/identityprovider/keycloak_files.go`, `M internal/identityprovider/keycloak_realization.go`, `M internal/metrics/perses_dashboards.go`, `A internal/metrics/perses_dashboards_keycloak.go`, `M internal/metrics/perses_dashboards_test.go`, `M internal/metrics/realization.go`, `A internal/metrics/testdata/perses-dashboards/keycloak-identity.json` — product-code (identity)
- 1833 (a7b0a48048): `M internal/application/manifest_validation.go`, `M internal/application/workload.go`, `M internal/application/workload_test.go` — product-code + test
- 1855 (43326cf57f): `M cmd/baha/app_perses_cli_test.go`, `M cmd/baha/app_status_result.go`, `A internal/metrics/identity_dashboard_witness.go`, `M scripts/pr-gate-coverage.json` — product-code + test + routing-json
- 1650 (37c4d847ca): `M cmd/baha/app_perses_cli_test.go`, `M cmd/baha/app_status_result.go`, `A internal/metrics/identity_dashboard_witness.go`, `M scripts/pr-gate-coverage.json` — product-code + test + routing-json
- 1842 (4f570ff966): `M docs/releases/v0.4.28.demo-ref`, `M scripts/pr-check-runner.py`, `M scripts/pr-gate-map-v1.json`, `M scripts/pr-gate-plan.py`, `M scripts/test_pr_check_runner.py`, `M scripts/test_pr_gate_coverage.py` — docs-pin + scripts-routing

## 3. PR-GATE-PLAN OUTPUT (authoritative; executed via import + plan())

Every candidate → `coverage_status=resolved`, no `broad_required`, under both the develop planner and each head's own planner (heads 1856, 1842 change `scripts/pr-gate-plan.py`).

| PR | runtime_required | integration_required | public_contracts_required | native `include` list (selected_gates) |
|----|------------------|----------------------|---------------------------|----------------------------------------|
| 1856 | true (atomic/docker/lifecycle via demo pin) | false | false | `[]` (plan selected_gates) but runtime_required=true |
| 1812 | false | false | false | `{include:[]}` |
| 1819 | true | false | false | `{include:[]}` |
| 1820 | true | false | false | `{include:[]}` |
| 1818 | true | false | false | `{include:[]}` |
| 1833 | true | false | false | `{include:[]}` |
| 1855 | false | false | false | `{include:[]}` |
| 1650 | false | false | false | `{include:[]}` |
| 1842 | false | false | false | `{include:[]}` |

Deciding file:line: `scripts/pr-gate-plan.py` `targeted_plan()` (develop) iterates the changed `paths` and assigns `area` + `selected` gates per path; the `include`/selected_gates are then resolved against the trusted catalog in `plan()` (deletion_exemption + `resolve_covered_gates`). The three booleans are emitted by the trusted base's `pr-runtime-matrix` producer (ci.yml:889-904): `integration_required` (ci.yml:889), `runtime_required` (ci.yml:902), `public_contracts_required=false` (ci.yml:904).

## 4. MATRIX — does 'PR · Demo Pin' execute?

'PR · Demo Pin' is the `pr_demo_pin` job (ci.yml:1075-1118). Its `if` (ci.yml:1080) runs it when `runtime_required=='true' || integration_required=='true' || public_contracts_required=='true'`. `pr_required_final.py` requires `pr_demo_pin` to succeed whenever an `atomic/{docker,podman}` runtime gate or coreless-lifecycle gate is selected.

| PR | write-set class | runtime_req | integration_req | pub_contracts | native include | 'PR Demo Pin' executes (planner)? | Evidence: real CI demo-pin outcome |
|----|-----------------|-------------|-----------------|---------------|----------------|-----------------------------------|-----------------------------------|
| 1856 | scripts-routing + docs-pin | TRUE | false | false | runtime_required=true | YES (ci.yml:1080 true) | run 45748783396 (head de26af2ec7): SKIPPED; run 45750304453 (head 5ae41085bf): FAILURE (BLOCKED: pr_demo_pin) |
| 1812 | scripts-routing | FALSE | false | false | `{include:[]}` | NO (ci.yml:1080 false) | run 45709326054: SKIPPED |
| 1819 | product-code + test | TRUE | false | false | runtime_required=true | YES | runs 45699760220, 45694363486: SUCCESS |
| 1820 | product-code + test | TRUE | false | false | runtime_required=true | YES | run 45710380590: SUCCESS |
| 1818 | product-code (identity) | TRUE | false | false | runtime_required=true | YES | run 45316544436: SUCCESS |
| 1833 | product-code + test | TRUE | false | false | runtime_required=true | YES | run 45513816046 (attempt2 PR): SUCCESS (push/dispatch runs skipped) |
| 1855 | product-code + routing-json | FALSE | false | false | `{include:[]}` | NO | runs 45746255447, 45743494737: SKIPPED |
| 1650 | product-code + routing-json | FALSE | false | false | `{include:[]}` | NO | runs 45737093207, 45734193200: SKIPPED |
| 1842 | docs-pin + scripts-routing | FALSE | false | false | `{include:[]}` | NO | run 45739171543: SKIPPED (run FAILED on docs/release-scope, independent) |

## 5. CROSS-CHECK PREDICTION vs REALITY

- 1819/1820/1818/1833/1855/1650: prediction (execute) matches reality (job ran) for the runtime_required heads; demo-pin SUCCESS for all runtime_required heads except 1856.
- MISMATCH 1: PR #1856 head de26af2ec7 (run 45748783396): runtime_required=true per planner but `PR · Demo Pin` = SKIPPED and run still `success`. The `if` at ci.yml:1080 evaluated true (runtime_required) yet the job was skipped — reachable defect, not a model error.
- MISMATCH 2: PR #1812 head 0922888af8 (run 45709326054): runtime_required=true but `PR · Demo Pin` = SKIPPED; run `success`. Same shape.
- 1842 (runtime_required=FALSE): correctly skipped; run failure is the docs/release-scope path, independent of demo-pin.
- Hypothesis check (trusted-base planner ci.yml:865-876 vs candidate-side): both develop and head planners yield identical coverage for every candidate, so the 1856/1812 skip is NOT a planner divergence — it is a ci.yml execution gap on those two exact heads.

## 6. DECISION QUESTION ANSWERS

(a) WHICH NEED the ci.yml:1080 planned-ID clause at all: only the runtime_required / integration_required / public_contracts_required heads — 1819, 1820, 1818, 1833, 1856 — because those are the ones where `pr_required_final.py` makes `pr_demo_pin` a REQUIRED job. (b) ALREADY ADMITTED by existing conditions: all runtime_required heads are already admitted by ci.yml:1080 as it stands; the clause is not missing for them — 1819/1820/1818/1833/1650 run it today. (c) Could the clause make 'PR · Demo Pin' execute on a candidate whose pin does NOT resolve: YES. `pr-check-runner.py:384-400` (`validate_demo_source_pin`) requires `docs/releases/v0.4.27.demo-ref` to contain exactly one 40-hex SHA that resolves via `gh api …/baseharbor-demo/commits/<sha>` (line 395-399: `raise RuntimeError('… does not resolve in the pinned repository')` otherwise). Fail-closed: a non-resolvable pin raises → demo-pin job fails → `pr_required_final` lists it as a required job that did not succeed → `PR Selected Checks` BLOCKED. So the clause, once present, would manufacture a NEW RED run on any candidate whose pin does not resolve (this is exactly run 45750304453 / head 5ae41085bf).

## 7. CENSUS ADDENDUM (head 5ae41085bf = PR #1856; still read-only)

WHICH PATH each open candidate executes:
- Reaches the ci.yml:1131 demo_sha body: NONE. That line is out of range (current ci.yml is ~1460 lines). The `pr_demo_pin` job body is ci.yml:1086-1112; demo_sha is read from `needs.pr_plan.outputs.demo_ref` at ci.yml:1099, populated by the pr_plan `demo_source` step (ci.yml:907-925): explicit `vars.BASEHARBOR_PR_DEMO_SOURCE_SHA` (ci.yml:919-920) → else `gh api …/baseharbor-demo/git/ref/heads/main --jq .object.sha` (ci.yml:921-923) → else empty-sha-and-exit when no runtime gate (ci.yml:915-918).
- Relies on pr_plan :951-960 (actual :915-925): candidates with runtime/integration/public_contracts required route through the demo_source producer; 1812/1855/1650/1842 (runtime_required=FALSE) hit the ci.yml:915-918 empty-sha exit and the job is correctly skipped.

PR Selected Checks failure 03:45:06Z (run 45750304453, job 139678088215): step 6 'Require normal selected job results' printed `BLOCKED: workflow job did not succeed: pr_demo_pin`; pr_demo_pin job status=failure. The preceding python3 -c step (ci.yml) verifying `pr-plan.json` target_base_sha/integration_sha == EXPECTED_BASE/HEAD/INTEGRATION PASSED (no 'stale PR integration inputs' error). => This failure is a CASCADE OF THE DEMO PIN ROW (the pin job failed to run/verify because runtime_required is true and the pin did not resolve), NOT an independent target_base/integration selection defect.

## 8. AKTE

gh pr create against live main is the required planning act. Not yet executed (mission step 8 pending). Zero-mutation proof: no commit was made to either repo this shift; develop `ac7c970f…` / main `cddc81b3…` unchanged.

## CLEANLINESS

docker ps -a (my pid): empty (no containers started; read-only task).
No containers, networks, volumes, or state dirs created. ambient-core/ images untouched.
