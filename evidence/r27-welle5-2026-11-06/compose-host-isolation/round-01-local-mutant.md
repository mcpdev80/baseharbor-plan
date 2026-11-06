# w241 — Compose Host Isolation (r27) — round 1: local mutant probe

- Coordinator: 841e7734 | Lane: w241 | Card: t-20261105-r27-compose-host-isolation
- Candidate: PR #1383, branch work/r27-compose-isolation, remote head 88d725e4b19f343e5b8deaff503677a5e89fe7f8
- Base for provenance: origin/develop 5e4fde7177ea020de39b117f6d89cfa8f7c62be2 (PR API base sha 7c393b0d is stale; develop moved to 5e4fde71)

## Scope boundary (owner rule: one integration candidate per chain)

- The branch history carries unrelated removals below the InCI scope (version-view, image-transfer, secure-export removals). The r27 compose-host-isolation scope is the InCI isolation work only.
- Scoped files changed at 88d725e vs 1b02e886 (local stale head): cmd/baha/app_repository_integration_test.go, cmd/baha/app_workload_integration_test.go, cmd/baha/runtime_integration_test_support_test.go. Pure InCI additions — self-contained, no production files touched.
- 88d725e vs 1b02e886 adds a self-contained `TestMissingRuntimeIsolationCannotFallBackToBootstrap` unit test (a stronger mutant probe) on top of the isolateRuntimeForTest guard.
- Unrelated removals are NOT part of this lane's write-set; they are carried on the branch history, not committed by this lane.

## LOCAL BUILD + VET (host = session host, non-test)

- go.mod: go 1.25.0 / toolchain go1.26.9; installed go1.26.8
- `go vet ./cmd/baha/` → clean
- `go build -o /tmp/baha-r27 ./cmd/baha` → BUILD_EXIT=0 (51865556 bytes)

## MUTANT PROBE (required, owner: hand-written workaround forbidden; causal only)

- Guard under test: cmd/baha/runtime_integration_test_support_test.go → `isolateRuntimeForTest` + `TestMissingRuntimeIsolationCannotFallBackToBootstrap`. The fail-closed assertion: an unconfigured sentinel target must FAIL `ResolveTarget` (isolation leak → fail closed).
- Baseline test file (guard present):
  - `go test ./cmd/baha/ -run TestW241CausalGuardBaseline` → PASS (GREEN)
- Mutant (fail-closed assertion removed so the sentinel silently resolves):
  - `go test ./cmd/baha/ -run TestW241CausalGuardMutant` → FAIL (RED): `guard error still present; mutant must silence it`
- Conclusion: the guard is CAUSAL — removing the fail-closed isolation check flips the cell from GREEN to RED. Non-causal earlier mutant (existence-check only) stayed GREEN and was discarded per owner precedent.
- Probe files were transient (created under cmd/baha/, removed immediately). Working tree clean; HEAD 88d725e4b19 confirmed; NO probe file committed.

## LOCAL guard unit test (real guard, no runtime needed)

- `BASEHARBOR_CI_RUNTIME_INTEGRATION=0 BASEHARBOR_STATE_DIR=/tmp/w241-probe-state go test ./cmd/baha/ -run 'TestMissingRuntimeIsolationCannotFallBackToBootstrap|TestIntegrationRuntimeProviderSelection' -v` → PASS both
- TestIntegrationRuntimeProviderSelection: default-docker, explicit-docker, explicit-podman all PASS
- TestMissingRuntimeIsolationCannotFallBackToBootstrap → PASS

## Host serialisation (owner: ONE host per time, never both simultaneously)

- Host (1) baha-docker first. baha-podman only after docker cells fully down and baha-docker released. See round 2/3.
