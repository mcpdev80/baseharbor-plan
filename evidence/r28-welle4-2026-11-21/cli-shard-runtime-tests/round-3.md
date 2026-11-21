# 0428-215 implementation and exact gate route (round 3)

## Candidate

- Product PR: https://github.com/mcpdev80/baseharbor/pull/1743
- Candidate SHA: `47549ca1451e4f913ea0961ff9712cb1e03193a0`
- Base: `develop` at `40cb28c758b02960356434b630086a341ebe1738`
- Exact PR workflow run: [44875389702](https://github.com/mcpdev80/baseharbor/actions/runs/44875389702) (queued at evidence creation).

## Change

- Added `cmd/baha/operator_core_network_binding_native_test.go`, test ID `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork`.
- The opt-in test creates a same-name Docker/Podman native network with only a user-controlled Compose project label. It calls `prepareCoreDefaultNetworkBinding` and requires the protected-owner refusal, while asserting the network was not marked external/adopted.
- Added an exact `require_pass` entry and opt-in variable to `scripts/ci-owner-node-native.sh`; the existing script runs in both native Docker and Podman matrix cells and rejects test skips.
- Added a selector regression to `scripts/test_ci_keycloak_single_route.py`. It checks that the `operator_` candidate path matches the existing owner/node path regex from the base workflow and that the native script requires the exact test ID. No workflow file edit is required for this existing base-branch selector.

## Local verification

- `bash scripts/test-ci-impact-selectors.sh` — PASS.
- `python3 scripts/test_pr_gate_coverage.py` — 36 tests PASS.
- `python3 scripts/test_ci_keycloak_single_route.py` — 6 tests PASS.
- `go test ./cmd/baha -run '^TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork$' -count=1 -v` — compiles, expected opt-in SKIP because this machine does not provide an isolated Docker/Podman acceptance daemon. Hosted gate must reject skips and supply the behavioral proof.
- `git diff --check` — PASS.
- `scripts/ci-fast-check.sh` — fails the inherited `TestMCPRegistrationCIInProcessDiscoverAndInvoke` operator-auth fixture. This is the external #1615 auth seam, not a failure in the changed files; no changes made to that lane.

## Test-to-gate binding

| Test ID | Required gate | Exact candidate evidence |
| --- | --- | --- |
| `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · docker` | Run 44875389702 pending |
| `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · podman` | Run 44875389702 pending |
| selector regression test | `PR · Focused Python` | Run 44875389702 pending |

Do not accept/close this task until both native cells show the exact test PASS (not skip), planner/workflow-policy checks pass, and required selected PR checks are evaluated. Other PRs still expose shared required-shard failures; the 0428-215-owned cases are already green on PR #1740 run 44868911131 as recorded in round 2. No claim is made that the overall PR is mergeable while any unrelated required gate remains red.
