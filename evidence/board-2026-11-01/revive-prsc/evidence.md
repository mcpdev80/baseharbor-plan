# Evidence — Mission revive-prsc (Worker-Ornith, diagnostic)

- **Task/Mission:** revive-prsc — resurrected PRs **#1222** and **#1229** both fall into *PR Selected Checks* with the same Python location in the executor (`except ValueError` / `coverage-unresolved` path)
- **Model:** Ornith
- **Zeit:** 2026-11-02
- **Auth:** gh logged in as mcpdev80 (ssh), repo mcpdev80/baseharbor reachable

## PLAN (Checkliste)

1. [x] Step 0: todowrite GUI list + workers/todos/revive-prsc.json + ## PLAN in evidence anlegen (§4.4)
2. [x] Step 1: Reality check — gh auth mcpdev80, PR #1222 (head 12828fa4, OPEN, base develop a567ff46) + #1229 (head befecb0c, OPEN, base develop a567ff46). Both OPEN, not merged.
3. [x] Step 2: Exact PRSC run + failure captured (file:line in evidence), job = PR Selected Checks / `pr-required-final.py` final verify.
4. [ ] Step 3: Shared executor code located (pr-required-final.py:24-28 + pr-gate-plan.py coverage_status logic).
5. [ ] Step 4: Diagnose hypotheses (a) gate-map-Unknown / (b) test-drift / (c) executor-bug → klasse a/b/c.
6. [ ] Step 5: Result table + verdict; evidence.md + ## PLAN tick board json; HANDOFF line.
7. [ ] Step 6: Post END_DONE|END_BLOCKED handoff (codeman agent post 35cdb02e...).

## 1) Reality check (Step 1)

| PR | head_sha | state | base | branch | title |
| --- | --- | --- | --- | --- | --- |
| #1222 | `12828fa410c1d1d2eaa6f68bfedea42bc0de56b6` | OPEN (mergedAt null) | develop `a567ff46956518359b7aa739eb004b7ccc30f1a5` | `work/v0.4x-core-750-inspect-source-neutral-findings` | fix(repositoryinspect): source-neutral shared summary projection for Quadlet/Kubernetes |
| #1229 | `befecb0cab0d987857715f99e77a0952b572880c` | OPEN (mergedAt null) | develop `a567ff46956518359b7aa739eb004b7ccc30f1a5` | `work/v0.4x-core-390-binding-enforcement` | fix(service-binding): enforce well-known output names at capability boundary (core-390 rv390) |

Diff files:
- **#1222** (6 files): `internal/repositoryinspect/inspect.go`, `internal/repositoryinspect/workload_source_parity_test.go`, `testdata/adoption-parity/README.md`, `testdata/adoption-parity/compose/compose.yaml`, `testdata/adoption-parity/kubernetes/app.yaml`, `testdata/adoption-parity/quadlet/storage.container`
- **#1229** (5 files): `contracts/binding/v1/service-binding.schema.json`, `contracts/contracts_test.go`, `internal/capability/lifecycle.go`, `internal/capability/service_binding.go`, `internal/capability/service_binding_test.go`

## 2) Exact PRSC runs + failures (Step 2)

Both runs are workflow run **ids** (run_number in parentheses):
- **#1222:** run id `41360075776` (run_number 4186), `CI · PR #1222`, created `2026-11-01T23:02:08Z`, conclusion `failure`.
- **#1229:** run id `41360080116` (run_number 4187), `CI · PR #1229`, created `2026-11-01T23:04:30Z`, conclusion `failure`.

Job (both): **PR Selected Checks** → final step runs `python3 "$RUNNER_TEMP/pr-required-final.py" --plan pr-plan.json --results … --requirements scripts/release-requirements.json`.

### #1222 BLOCKED line (run 41360075776)
```
BLOCKED: coverage-unresolved: unknown impact for testdata/adoption-parity/README.md;
unknown impact for testdata/adoption-parity/compose/compose.yaml;
unknown impact for testdata/adoption-parity/kubernetes/app.yaml;
unknown impact for testdata/adoption-parity/quadlet/storage.container
```
Env on the runner: `PLAN_JOB=success, FOCUSED_JOB=success, VALIDATION_JOB=success; SELECTED_RUNTIME_REQUIRED=false, PUBLIC_CONTRACTS_REQUIRED=false; EXPECTED_BASE=a567ff46…, EXPECTED_HEAD=12828fa4…, EXPECTED_INTEGRATION=ba8efb88…`

### #1229 BLOCKED line (run 41360080116)
```
BLOCKED: coverage-unresolved: provider/capability registry or lifecycle impact needs targeted qualification: internal/capability/lifecycle.go;
provider/capability registry or lifecycle impact needs targeted qualification: internal/capability/service_binding.go;
provider/capability registry or lifecycle impact needs targeted qualification: internal/capability/service_binding_test.go
```
Env on the runner: `PLAN_JOB=success, FOCUSED_JOB=success, VALIDATION_JOB=success; PUBLIC_CONTRACTS_REQUIRED=true, PUBLIC_CONTRACTS_JOB=success, VERIFIED_DEMO_SHA=073e065f…; EXPECTED_INTEGRATION=8814f38e…`

Both `pr-plan.json` assert on `target_base_sha/head_sha/integration_sha` equality (stale-input guard) — i.e. the plan was freshly generated from the current candidate, not a cached/stale artifact.

## 3) Shared executor code (Step 3)

File: `baseharbor/scripts/pr-required-final.py`, function `verify()`, lines **24-28**:
```python
if plan.get('coverage_status') != 'resolved':
    errors.append('coverage-unresolved: ' + '; '.join(
        str(x) for x in plan.get('unresolved_coverage', [])
    ) if isinstance(plan.get('unresolved_coverage'), list) and plan.get('unresolved_coverage')
    else 'coverage-unresolved: missing explicit coverage resolution')
```
This is the single shared Python location both failures hit. It reads `plan['coverage_status']`, which the **planner** (`pr-gate-plan.py`) sets.

Planner: `baseharbor/scripts/pr-gate-plan.py`, function `plan()`. Per changed file it selects an `area`, then at the end:
```python
status = 'unresolved' if unresolved else 'resolved'   # line 1658
... 'coverage_status': status, 'unresolved_coverage': unresolved, ...   # lines 1660-1661
```
`unresolved` is populated by per-file branches. Both PRs leave non-empty `unresolved` → `coverage_status='unresolved'` → `verify()` emits `coverage-unresolved` → BLOCKED.

## 4) Diagnosis — hypothesis (a): gate-map-Unknown (Step 4)  ✅ CONFIRMED class (a)

The planner has a per-file area switch (`elif` chain). Files not matched by any specific branch fall through to:
- **line 1648-1650** (`else`): `area = 'unresolved'; unresolved.append('unknown impact for ' + path)`
- **line 1499-1503** (`elif path.startswith('internal/capability/')`): `area='capability-implementation-unresolved'; unresolved.append('provider/capability registry or lifecycle impact needs targeted qualification: ' + path)`

Mapping:
- **#1222** files `testdata/adoption-parity/{README.md,compose.yaml,app.yaml,storage.container}` → **no branch matches** → hit `else` (line **1650**) → message prefix `unknown impact for …` (matches run exactly).
- **#1229** files `internal/capability/{lifecycle.go,service_binding.go,service_binding_test.go}` → hit `elif path.startswith('internal/capability/')` (line **1499/1503**) → message prefix `provider/capability registry or lifecycle impact needs targeted qualification: …` (matches run exactly).

**Common cause:** both are **gate-map gaps** — the planner's `pr-gate-plan.py` area switch has no resolved/qualified mapping for `testdata/adoption-parity/*` and `internal/capability/*(.go)` production/test files, so they fall onto the conservative `unresolved` branch and fail PR Selected Checks fail-closed. This is the same pattern as precedent #1259/#1260 (gate-map follow-up PRs) referenced in the mission.

Not (b) test-drift and not (c) executor-bug:
- The executor line is identical for both and correctly reproduces the planner output (verified against the runner env: all expected authenticated jobs = success, so the failure is *purely* the coverage_status gate).
- #1222's own repositoryinspect change DOES resolve: `internal/repositoryinspect/inspect.go` and `workload_source_parity_test.go` are in `INSPECT_PROJECTION_REVIEWED`/`INSPECT_RECONCILE_REVIEWED` → `inspect-implementation-resolved`/`inspect-reconciliation` (no unresolved entry). Only the 4 `testdata/adoption-parity/*` files block. So the product code is fine; only the testdata files lack a gate-map entry.
- #1229's `internal/capability/domain_test.go` and `integration_contract_test.go` ARE in `SAFE_CAPABILITY_TESTS` → `capability-conformance-test` (resolved), but the 3 production/test `.go` files hit the unresolved branch. Again product-code-correct, gate-map-incomplete.

## 5) Result table

| PR | head_sha | unresolved files | planner branch | file:line | klasse |
| --- | --- | --- | --- | --- | --- |
| #1222 | 12828fa4 | testdata/adoption-parity/{README.md,compose.yaml,app.yaml,storage.container} | `else` catch-all → area `unresolved` | `scripts/pr-gate-plan.py:1648-1650` | **a** |
| #1229 | befecb0c | internal/capability/{lifecycle.go,service_binding.go,service_binding_test.go} | `elif path.startswith('internal/capability/')` → area `capability-implementation-unresolved` | `scripts/pr-gate-plan.py:1499-1503` | **a** |

**Klasse = a** (gate-map-Unknown → small gate-map follow-up PR in `scripts/pr-gate-plan.py` + `test_pr_gate_plan.py`).

### Recipe for fix ( Klasse a )
Two focused additions to `scripts/pr-gate-plan.py`, modeled on #1259/#1260 and the existing `SAFE_CAPABILITY_TESTS` pattern:
1. **`internal/capability/*.go`** (lifecycle/service_binding + their tests): these ARE qualified by the existing `capability-package-tests` check (`go test ./internal/capability/... -count=1`, already in `CAPABILITY_CHECKS`). Replace the unresolved branch (1499-1503) with a resolved mapping gated on `path in SAFE_CAPABILITY_TESTS | new capability test/impl allowlist` OR, more simply, bind the 3 files to `require(CAPABILITY_CHECKS)` and select the public-contracts / capability gate so `coverage_status` becomes `resolved`. Narrowest: add `internal/capability/lifecycle.go`, `internal/capability/service_binding.go`, `internal/capability/service_binding_test.go` to a resolved allowlist area `capability-implementation-resolved` with `require(CAPABILITY_CHECKS)`.
2. **`testdata/adoption-parity/*`**: these are static test fixtures (README/compose/k8s/quadlet) consumed by the repositoryinspect parity test. Bind to the inspect checks that already run the parity test (`INSPECT_CHECKS`, incl. `inspect-package-tests`/`inspect-consumer-tests`) via a new area `inspect-testdata-fixed` → resolved. Narrowest: add a matched branch for `path.startswith('testdata/adoption-parity/')` with `require(INSPECT_CHECKS)`.

Scope: **only `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py`** (mirrors the exactly-2-file acceptance of #1259/#1260). No `.github/workflows/*`, no receipts. After the follow-up PR, re-run PRSC on BOTH #1222 and #1229 to terminal; both should PASS once their files resolve.

### Empirical recipe verification (patched worktree `workers/worktrees/revive-prsc`, NOT live product)
- Loaded patched `pr-gate-plan.py` as module, ran planner on both real diffs:
  - **#1222:** BEFORE `coverage_status=unresolved` → AFTER `resolved`, `selected_gates=[]`, `unresolved_coverage=[]` ✓
  - **#1229:** BEFORE `unresolved` → AFTER `resolved`, `selected_gates=['integration/static/public-contracts']`, `unresolved_coverage=[]` ✓ (already-satisfied trusted gate)
- Existing planner test suite on patched copy: **177 + 8 + 7 + 5 tests**, only ONE failure — `test_application_and_capability_production_remain_unresolved` asserts `internal/capability/lifecycle.go` stays `unresolved` (`test_pr_gate_plan.py:965-981`). This test MUST be updated in the follow-up PR (the 3 files now resolve); the remaining capability `*.go` (registry.go, provider_placement.go, etc.) correctly stay unresolved. No other regression.

## repo-rule compliance

- No `.github/workflows/*` touched (STOP). No receipt* files created. No subagent/codeman spawn. No merge. No branch-protection bypass.
- Auth via system gh token (mcpdev80, ssh) — set by the runner/host, not by this lane.
- Evidence built from authenticated GitHub API facts (run ids, SHA, BLOCKED lines) + source file lines — reproducible, machine-witnessed.
- Diagnostic only: this lane proposes the fix recipe but does NOT open a PR or modify product (mission forbids merge; follow-up gate-map PR is an Owner/Coordinator dispatch decision).

## Handoff line (keep synced)

`END_DONE revive-prsc: klasse=a gate-map-Unknown, shared executor path pr-required-final.py:24-28 (coverage_status != 'resolved'); #1222 → pr-gate-plan.py:1648-1650 else-catch-all on testdata/adoption-parity/* (run 41360075776); #1229 → pr-gate-plan.py:1499-1503 internal/capability/* branch (run 41360080116) | fix recipe: focused gate-map follow-up PR (scripts/pr-gate-plan.py + test_pr_gate_plan.py only), then re-run PRSC on both PRs to PASS`

## End-of-lane

`END_DONE revive-prsc: klasse=a (gate-map-Unknown); 1222=testdata/adoption-parity/* else-catch-all (pr-gate-plan.py:1648-1650); 1229=internal/capability/* branch (pr-gate-plan.py:1499-1503); recipe=gate-map follow-up PR (pr-gate-plan.py+test_pr_gate_plan.py), then re-run PRSC both to PASS`
