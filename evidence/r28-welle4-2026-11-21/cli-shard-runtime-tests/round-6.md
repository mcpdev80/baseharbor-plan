# 0428-215 — Podman network inventory diagnosis

## Exact run and result

PR #1743 head `c506624d14e3c6939c204da12926cd0416daf3ca`, exact PR run [44877364076](https://github.com/mcpdev80/baseharbor/actions/runs/44877364076), completed with failures.

| Exact SHA | Test ID | Gate | Trigger | Result |
| --- | --- | --- | --- | --- |
| `c506624d14e3c6939c204da12926cd0416daf3ca` | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · docker` (job 136764956159) | existing base `operator_` selector and owner native script | PASS at 06:52:01Z; later job failure is a separate existing `TestControlPlaneSingleDefaultNativeRuntimeInCI` failure |
| `c506624d14e3c6939c204da12926cd0416daf3ca` | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · podman` (job 136764956155) | existing base selector and same owner native script | FAIL at 06:52:17Z; direct native inspect confirms expected name and both Compose labels, but `prepareCoreDefaultNetworkBinding` returns nil |
| `c506624d14e3c6939c204da12926cd0416daf3ca` | `KeycloakSingleNativeRouteTests.test_foreign_core_network_test_selects_both_existing_pr_native_runtimes` | `PR · Focused Python` (job 136764956113) | changed selector regression test | PASS |

Podman failure output (exact fields):

```text
unowned native network must be refused with protected-owner diagnostic;
files={DefaultNetworkExternal:false ... Project:bh-foreign-network-1795243937779652722-shared
ResourceProject:baseharbor-foreign-network-1795243937779652722} err=<nil>
native-labels="baseharbor-foreign-network-1795243937779652722-default|bh-foreign-network-1795243937779652722-shared|bh-foreign-network-1795243937779652722-shared"
```

## Diagnosis step

The labels and network name are present in Podman's direct inspect output. The next candidate adds the provider's own `InspectProjectResources` result and error to the failure diagnostic, so the next exact native run identifies whether the provider inventory path is omitting this network or failing to resolve the runtime binding. No product behavior or workflow was changed in this diagnostic commit.

## Current exact candidate

Head `2281886ef45ff1628d5e6f0778b2da3c9527e460`; PR run [44877777956](https://github.com/mcpdev80/baseharbor/actions/runs/44877777956) was queued at publication. Closeout still requires the new test to PASS without skip on both native runtimes and required jobs to become terminal; neither criterion is met yet.
