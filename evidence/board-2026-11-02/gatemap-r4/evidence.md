# gatemap-r4 evidence

Mission: `coordinator/missions/gatemap-r4.txt`
Lane: `gatemap-r4` (Ornith worker) · Repo `baseharbor` · Base `origin/develop` @ `edd0978264`
Started: 2026-11-02

## Context

PR #1265 correctly plants the two Lifecycle gates (atomic/docker/lifecycle,
atomic/podman/lifecycle), BUT `coverage_status='unresolved'` for three files that
drive the App-Apply/Promotion path:

- `internal/application/manifest.go` — renders the concrete Manifest with its
  Provider / SQL / Valkey / Identity / TLS / readiness resolution.
- `internal/application/manifest_parse.go` — parses and validates the Manifest.
- `internal/application/v0425_contract_test.go` — pins the v0.4.25 contract.

Planner classifies all three as `application-implementation-unresolved` (Planner
rule ~1454-1510 family; pattern known from #1259/#1262/#1264). The manifest parser
controls the App-Apply/Promotion path — the existing Lifecycle gates REALISE exactly
this path.

Repo paths at repo root (no `scripts/` prefix — mission's `scripts/` is a doc-norm).

## ## PLAN

- Step 0: workers/todos/gatemap-r4.json + ## PLAN in evidence (board JSON carries the plan; todo-write GUI tool not bound in this worker env)
- Step 1: Reality check — gh auth (mcpdev80, ssh), fetch origin/develop @ edd09782, create isolated worktree gatemap-r4 @ edd09782 (base >=edd09782)
- Step 2: Local planner.py simulation BEFORE: all 3 files → coverage_status='unresolved', selected_gates=[], area 'application-implementation-unresolved' catch-all
- Step 3: Design — GATEMAP_R4_MANIFEST_FILES frozenset; 'application-manifest-lifecycle' branch before the internal/application/ catch-all; bind EXISTING atomic/docker/lifecycle + atomic/podman/lifecycle (no new gate, no wildcard). Scope: only the two scripts files.
- Step 4: Implemented binding + constant in scripts/pr-gate-plan.py exactly as designed.
- Step 5: Planner tests +2 / updated 4 (manifest.go → footprint.go bundling partner). Baseline 184 → 186, ALL PASS.
- Step 6: Simulation AFTER: coverage_status='resolved', selected_gates unchanged, unresolved_coverage=[]. Go vet ./internal/application/... clean.
- Step 7: Committed work/gatemap-r4-bind-manifest-lifecycle @ 980b0c64, pushed, PR #1266 against develop.
- Step 8: Own PR #1266 CI terminal-green; pr-planner-tests + PRSC SUCCESS.
- Step 9: Post END_DONE handoff; record PR nr, head SHA, tests=186/186, before/after sim.

## Repo-rule compliance

- STOP (mission): only scripts/pr-gate-plan.py + test_pr_gate_plan.py; NO .github/*; no workflows; no merge; no subagent/codeman-Spawn. ✓
- AGENTS 4.2: changes hit exactly the three unbound application paths — no widening.
- #1259/#1262 pattern: bind to the EXISTING native lifecycle gates (atomic/docker/lifecycle, atomic/podman/lifecycle), reference existing gates, NO new gate, NO wildcard over internal/application/*.
- AGENTS 4.3: isolated worktree + branch work/gatemap-r4-bind-manifest-lifecycle, Claim published via branch/commit.
- AGENTS 5.2: no self-merge (worker STOP). Candidate left MERGEABLE for CODEX-MERGE / Owner.

## Before / after simulation (planner.py, local)

| File | before | after fix |
| --- | --- | --- |
| internal/application/manifest.go | unresolved (selected_gates=[]) | resolved → {atomic/docker/lifecycle, atomic/podman/lifecycle} |
| internal/application/manifest_parse.go | unresolved (selected_gates=[]) | resolved → {atomic/docker/lifecycle, atomic/podman/lifecycle} |
| internal/application/v0425_contract_test.go | unresolved (selected_gates=[]) | resolved → {atomic/docker/lifecycle, atomic/podman/lifecycle} |

After: `selected_gates` UNCHANGED (same two lifecycle tokens), `coverage_status='resolved'`, `unresolved_coverage=[]`.

## Planner tests (local, before / after)

- Baseline (origin/develop, clean): **184** planner tests, all pass.
- After this change: **186** (baseline 184 + 2 new), all pass.
- New: `test_gatemap_r4_manifest_paths_bind_lifecycle_gates` (resolved, selected_gates == both lifecycle gates, `go test ./internal/application/... ./contracts/...` required) + `test_gatemap_r4_other_application_file_stays_unresolved` (footprint.go / provider_union.go stay fail-closed unresolved → no widening).
- Updated (4): `test_application_and_capability_production_remain_unresolved` (dropped manifest.go from the unresolved list), `test_docker_engine_bundled_with_unreviewed_stays_unresolved`, `test_cli_docker_engine_bundled_with_unreviewed_stays_unresolved`, `test_shared_backends_bundled_with_unreviewed_stays_unresolved` (swapped manifest.go → footprint.go as the genuinely-unreviewed bundling partner), `test_unrelated_application_file_stays_unresolved` (manifest.go → footprint.go + docker-lifecycle negative assert).

## PR #1266 — CI terminal state

| Gate | Result |
| --- | --- |
| PR · Trusted Plan (PRSC) | SUCCESS (coverage resolved, no coverage-unresolved) |
| PR Selected Checks | SUCCESS (0 failures) |
| PR · Validation · pr-planner-tests | SUCCESS (186/186) |
| PR · Validation · ci-executor-verifier-tests | SUCCESS |
| PR · Validation · ci-policy | SUCCESS |
| PR · Focused Python | SUCCESS |
| Workflow policy | SUCCESS |
| Release Source Preflight | SKIPPED (not a release PR) |
| Targeted HA · docker/podman | SKIPPED |
| PR · Selected Runtime | SKIPPED |

Run #4207, Run-ID **41380125724** (CI · Source & Quality), conclusion=success.
HEAD SHA: `980b0c6432d4733cca539236156e553eca7269d3`
PR: https://github.com/mcpdev80/baseharbor/pull/1266 · base develop · mergeStateStatus: MERGEABLE (branch pending — NOT merged; worker STOP forbids merge).

## END

END_DONE gatemap-r4: pr=1266 head=980b0c64 tests=186/186 sim=unresolved→resolved (selected_gates unchanged). Manifest parser paths (manifest.go, manifest_parse.go, v0425_contract_test.go) bound to the two EXISTING native lifecycle gates (atomic/docker/lifecycle, atomic/podman/lifecycle) via GATEMAP_R4_MANIFEST_FILES + 'application-manifest-lifecycle' branch before the internal/application/ catch-all; no new gate, no wildcard. PR #1266 against develop — PRSC Run #4207 (Run-ID 41380125724) all SUCCESS / 0 failures incl. pr-planner-tests 186/186, coverage_status resolved. Candidate left MERGEABLE for CODEX-MERGE/Owner (worker STOP forbids merge).
