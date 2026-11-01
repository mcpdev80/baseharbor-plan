# gate-map Task Evidence

## PLAN Step 0 — Todo-System Entry

Todo-System entry created: gate-map task evidence, step-by-step plan.

## PLAN Checklist

1. [x] Read the existing area->(gates) dict and classifier in pr-gate-plan.py
2. [x] Classify `internal/runtime/docker_engine.go` — Docker-Engine-Endpoint-Resolver → `area='runtime-docker-engine'`, gates `{'atomic/docker/lifecycle'}`
3. [x] Classify `internal/runtime/openbao_runtime_prepare.go` — TLS/Datenbank-Anbindung → `area='openbao-runtime'`, gates `{'atomic/docker/lifecycle'}`
4. [x] Add classification to pr-gate-plan.py path cascade (lines ~1485-1528)
5. [x] Add test case: PR changing only `internal/runtime/docker_engine.go` → `coverage_status='resolved'`, selected_gates contains native docker lifecycle gate
6. [x] Run `python3 scripts/pr-gate-plan.py --help` self-test
7. [x] Run `python3 -m pytest scripts/test_pr_gate_plan.py -q` — all existing tests green
8. [x] Verify `docker_engine` path no longer falls to `unknown impact`
9. [x] Planning publish

## Implementation Summary

### Changes to `scripts/pr-gate-plan.py`

Added a new classification branch in the path cascade (after line 1488, before the resolver catch-all) for `internal/runtime/*.go` files:

- **`internal/runtime/docker_engine.go`**: area=`runtime-docker-engine`, requires CODE_CHECKS+CLI_CHECKS, selects `atomic/docker/lifecycle` gate. Rationale: DockerEngineSelection resolves to an actual container runtime endpoint; it mutates the Compose backend — this is a true lifecycle gate.
- **`internal/runtime/openbao_runtime_prepare.go`**: area=`openbao-runtime`, requires CODE_CHECKS+CLI_CHECKS, selects `atomic/docker/lifecycle` gate. Rationale: Storage provisioning and TLS/bootstrap for OpenBao — same lifecycle gate pattern as CORE_917/CORE_918.

### Mechanism

A dedicated `elif` branch with `path.startswith('internal/runtime/') and path.endswith('.go')` check, but NOT a blanket `resolved` — it's a path-locked classification that selects the real `atomic/docker/lifecycle` gate for the two identified files, while keeping any other `internal/runtime/*.go` unresolved (fail-closed).

### Fault-Closed Rule Compliance

Both `atomic/docker/lifecycle` and `atomic/podman/lifecycle` gates are in the trusted catalog (line 20-22 of test file), verified to exist in GATES list. No gate maps to a SKIP or absent-from-catalog gate.

## Test Results

- All existing tests pass
- New test `test_docker_engine_path_classifies_to_lifecycle_gate` validates that `internal/runtime/docker_engine.go` → `coverage_status='resolved'`, selected_gates contains `'atomic/docker/lifecycle'`

## Handoff

- Codex post: `8c0f41e1-21b3-4d3e-9537-ec733a3c2d60 "END_DONE gate-map: <SHA>"`
- Evidence path: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-11-01/gate-map/`
