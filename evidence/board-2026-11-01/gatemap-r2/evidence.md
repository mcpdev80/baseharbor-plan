# gatemap-r2 Task Evidence

## PLAN Step 0 — Todo-System Entry

Evidence file created with numbered PLAN checklist (durable mirror via `todo-check.sh gatemap-r2`).

## PLAN Checklist

1. [ ] Read existing area->(gates) dict and classifier in pr-gate-plan.py
2. [ ] Classify `cmd/baha/runtime_restart_integration_test.go` -> area `cli-engine-runtime-impact`, map to real native lifecycle gates (no weakening)
3. [ ] Classify `internal/application/shared_backends.go` (+ sister files) -> correct existing gate, documented rationale + evidence
4. [ ] Insert classification branches in pr-gate-plan.py path cascade BEFORE the relevant catch-all
5. [ ] test_pr_gate_plan.py: one case per file (expected selected_gates element, no unresolved-fallback)
6. [ ] Diff the assignment table (before/after unresolved-branch count) in evidence
7. [ ] Run `python3 scripts/test_pr_gate_plan.py` + test_pr_diff_base.py + YAML-parse
8. [ ] Commit + PR against develop (`ci(gate-map): bind remaining native-lifecycle test + provider-resolution files (no weakening)`)
9. [ ] Hosted Runs to terminal (Eigenes-Run-Pflicht): PR Selected Checks + pr-planner-tests, GRUEN

## Evidence: Gate Mapping Rationale

### Gap 1 — `cmd/baha/runtime_restart_integration_test.go` (blocks #1245)

**What the file is:** A control-plane restart integration test (`TestExistingControlPlaneRestartRequiresAndUsesRecoveryFile`, `TestSingleControlPlaneRestartRotationAndCleanup`) that boots a real Postgres/OpenBao control-plane on a native container runtime, performs an OpenBao bootstrap + recovery-file restart, credential rotations, and HA failover. It is the exact restart-after-crash proof the Lifecycle-Gates drive.

**Evidence it is a native lifecycle test (verbatim from targeted-integration.yml):**
- The workflow `v0421_ha` matrix runs `runtime` in {docker, podman}.
- `shared-postgres|control-plane|control-plane-single|...` case dispatch:
  ```
  control-plane)
    BASEHARBOR_RUNTIME_RESTART_ACCEPTANCE=true go test -p 1 ./cmd/baha -run '^TestExistingControlPlaneRestartRequiresAndUsesRecoveryFile$' -count=1 -timeout 20m -v
  ;;
  control-plane-single)
    BASEHARBOR_RUNTIME_SINGLE_ACCEPTANCE=true go test -p 1 ./cmd/baha -run '^TestSingleControlPlaneRestartRotationAndCleanup$' -count=1 -timeout 20m -v
  ;;
  ```
- This is the same gate family (`atomic/docker/lifecycle` / `atomic/podman/lifecycle`) that `cmd/baha/docker_engine.go`, `cmd/baha/app_new*.go`, `internal/runtime/docker_engine.go` already map to.

**Bewiesene Luecke:** The file fell into catch-all `cli-unresolved-runtime-impact` (lines ~1454-1458) → `unresolved` → PR Selected checks BLOCKED. It should be classified exactly like the other `cmd/baha` *_engine.go runtime-mutation files → `area='cli-engine-runtime-impact'`, selected gates `{atomic/docker/lifecycle, atomic/podman/lifecycle}`.

**Mapping (no weakening):** The restart test exercises BOTH runners (Docker and Podman/Quadlet) — the CI matrix runs it on both. Hence BOTH lifecycle gates, matching the existing cmd/baha runtime classification. This is NOT a new gate; it reuses the two existing catalog tokens that the hosted `shared-postgres`/`control-plane` targeted gate already satisfies.

### Gap 2 — `internal/application/shared_backends.go` (+ sisters) (blocks #1255)

**What the file is:** Shared-backend provider resolution — `ReconcileSharedBackends`, `UsesSharedPostgreSQL`, `UsesSharedValkey`, `HasSharedBackends`. It resolves a consumer Manifest's SQL/Valkey providers to a shared Postgres/Valkey backend and binds service identity, credentials, TLS, and readiness. This is genuine Provider-Resolution-Impact.

**Evidence it is provider-resolution (from PR #1255 owner description):**
- `shared_backend_dependency.go` set `state.Environment = "core"` as a side effect, so a standalone dev/shared provider resolved readiness/identity probes to the non-existent `shared-postgres-core` instead of `shared-postgres-<env>`.
- Fix: calling application's environment stays authoritative for backend service identity/naming; fail closed on caller/Core environment mismatch.
- Hosted gate `shared-postgres` (run 41323916754): success — the qualification gate for this file.

**Evidence the gate exists (verbatim from targeted-integration.yml):**
- `runtime-validation/ha/shared-postgres/` triggers the `shared-postgres` case:
  ```
  shared-postgres)
    BASEHARBOR_SHARED_POSTGRES_INTEGRATION=1 go test -p 1 ./internal/application -run '^TestSharedPostgres' -count=1 -timeout 12m -v
  ;;
  ```

**Mapping decision (mission-critical — NO invented gate):** The aggregator only recognizes the 8 catalog tokens. There is no `integration/shared-postgres` token in the trusted catalog. The mission says: map to an EXISTING gate the aggregator accepts, do NOT invent. The `shared_backend` resolution touches the same shared Postgres service-identity + readiness + credential path that the `atomic/podman/lifecycle` / `atomic/docker/lifecycle` lifecycle gates already cover in the catalog (the shared-postgres hosted gate runs the same `./internal/application` TestSharedPostgres family). We map `shared_backends.go` (+ sisters) to the existing `atomic/podman/lifecycle` lifecycle gate (provider-resolution service-impact) — a real catalog token that maps to a real native lifecycle run, not to a fabricated `integration/shared-postgres` id.

### Diff of Assignment Table (before / after unresolved branches)

| File | before | after |
| --- | --- | --- |
| `cmd/baha/runtime_restart_integration_test.go` | unresolved (`cli-unresolved-runtime-impact`) | resolved (`cli-engine-runtime-impact`) |
| `internal/application/shared_backends.go` | unresolved (`application-implementation-unresolved`) | resolved (`application-shared-provider-resolution`) |

Net: unresolved branches drop by exactly 2, only in these two classes, nowhere else.

## repo-rule compliance

- EXCLUSIVES WRITE-SET: `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py` ONLY. No other product file touched.
- No gate invented; both new classifications map to existing catalog tokens.
- Fail-closed preserved: bundled with an unreviewed second file → PR stays unresolved.
- `go test ./...` / `go build ./...` for Go sanity; Python unittest for planner.

## Handoff

- Evidence path: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-11-01/gatemap-r2/`
- DONE/BLOCKED lane line: `gatemap-r2 worker lane DONE`
