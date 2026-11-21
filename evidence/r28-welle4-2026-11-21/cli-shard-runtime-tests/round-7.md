# 0428-215 — Podman test fixture store alignment

## Exact evidence

PR #1743 head `fc79b74627d12fd7c5096621069480861069797e`, exact run [44878287581](https://github.com/mcpdev80/baseharbor/actions/runs/44878287581), terminal failed.

| Exact SHA | Test ID | Gate | Trigger | Result |
| --- | --- | --- | --- | --- |
| `fc79b74627d12fd7c5096621069480861069797e` | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · podman` (job 136767910929) | existing `operator_` selector and owner native script | FAIL: direct Podman inspect sees expected network + labels; provider `InspectProjectResources` returns `[]`, nil |
| `fc79b74627d12fd7c5096621069480861069797e` | `KeycloakSingleNativeRouteTests.test_foreign_core_network_test_selects_both_existing_pr_native_runtimes` | `PR · Focused Python` (job 136767910811) | selector regression | PASS |

Podman failure output shows `network-list="baseharbor-…-default\npodman"`, `inventory=[]`, and both direct-inspect labels equal the expected project. This excludes a missing network name or dropped labels.

## Root cause and correction

`internal/runtime/command_env.go:9-19` removes `XDG_CONFIG_HOME` and `XDG_DATA_HOME` from Podman subprocesses. The test had created and inspected its fixture with ordinary `exec.CommandContext`, inheriting the runner's isolated XDG paths; BaseHarbor then queried Podman's default store and correctly saw no fixture. Existing direct Podman fixture code in `cmd/baha/installation_destroy_native_test.go:213-220` explicitly removes the same variables.

Head `57e7941772ce85dbc60bad7faddd3613c3191c4c` now uses that established Podman command environment for create, direct inspect, failure-only listing, and cleanup. Local focused Go invocation compiles and reports the expected opt-in skip because this workstation has no isolated native daemon. Exact PR run [44878727267](https://github.com/mcpdev80/baseharbor/actions/runs/44878727267) was queued at publication; native test pass without skip is still required on both runtimes.

## Remaining gate evidence

Run 44878287581's full CI also has failing CLI shards on the shared operator-auth seam and unrelated existing native lifecycle failures. These do not establish a failure in the 0428-215 product behavior; they do prevent treating that overall PR run as green. #1615 remains excluded.
