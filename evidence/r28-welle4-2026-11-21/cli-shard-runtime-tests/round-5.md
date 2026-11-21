# 0428-215 — Podman native label fixture correction

## Prior exact run

- PR #1743 run [44876072403](https://github.com/mcpdev80/baseharbor/actions/runs/44876072403), head `a131256c285e257837e402a9ba0fe037f0835bbe`, is terminal on its native cells.
- Docker job 136761937069 logged `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` PASS exactly once, with the job later failing on a separate pre-existing native acceptance test.
- Podman job 136761937074 logged the same exact test as FAIL: the unowned same-name network was not detected, so `prepareCoreDefaultNetworkBinding` returned nil error.

## Finding and correction

BaseHarbor's existing Podman/Quadlet renderer emits both `com.docker.compose.project` and `io.podman.compose.project` labels (`internal/providers/runtime/podman/quadlet_render.go`, network rendering). The previous Podman fixture supplied only the latter. The test now supplies both labels on Docker and Podman; both are user controlled and neither proves protected owner inventory. This matches BaseHarbor's own rendered shape and preserves the requirement that labels alone do not grant ownership.

## Current exact candidate

- PR #1743 head: `9fad2086a53f2800ac1f40c1442295bde2ff3c35`.
- Exact PR run: [44876725420](https://github.com/mcpdev80/baseharbor/actions/runs/44876725420), pending when recorded.

| Exact SHA | Test ID | Gate | Trigger | Result |
| --- | --- | --- | --- | --- |
| `9fad2086a53f2800ac1f40c1442295bde2ff3c35` | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · docker` | existing base `operator_` path selector; owner native script | Run 44876725420 pending |
| `9fad2086a53f2800ac1f40c1442295bde2ff3c35` | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · podman` | existing base selector; same script | Run 44876725420 pending |
| `9fad2086a53f2800ac1f40c1442295bde2ff3c35` | `KeycloakSingleNativeRouteTests.test_foreign_core_network_test_selects_both_existing_pr_native_runtimes` | `PR · Focused Python` | changed selector regression test | Run 44876725420 pending |

The task stays active. Do not close or merge until both native test events PASS (not skip) and all required checks are terminal.
