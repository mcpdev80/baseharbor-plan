# 0428-215 — isolate the ownership test from unrelated native auth setup

## Candidate and run

- PR #1743: https://github.com/mcpdev80/baseharbor/pull/1743
- Exact head: `a131256c285e257837e402a9ba0fe037f0835bbe`
- Base: `develop` at `40cb28c758b02960356434b630086a341ebe1738`
- Exact run: [44876072403](https://github.com/mcpdev80/baseharbor/actions/runs/44876072403), queued when this note was written.

## Prior attempts and correction

- Run [44875389702](https://github.com/mcpdev80/baseharbor/actions/runs/44875389702), head `47549ca1`: the native script reached an earlier `TestControlPlaneSingleDefaultNativeRuntimeInCI` teardown failure before it could execute the new test. The test was moved directly after native runtime reset and before that broader lifecycle case.
- Run [44875693455](https://github.com/mcpdev80/baseharbor/actions/runs/44875693455), head `1e43e254`: the new test now ran first, but both native cells showed `create isolated target: Managed-environment machine operations require an authenticated BaseHarbor operator.` The test used the CLI mutation path to create a Target, coupling the ownership assertion to a separate authorization prerequisite.
- Current head `a131256c` uses existing `configureIsolatedEmptyRuntimeTarget` test setup directly, so the test creates no CLI Target mutation and tests only native network ownership. The native name and forgeable Compose owner label remain the inputs under test.

## Current exact test route

| Exact SHA | Test ID | Mapped gate | Trigger | Actual result |
| --- | --- | --- | --- | --- |
| `a131256c285e257837e402a9ba0fe037f0835bbe` | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · docker` | `operator_core_network_binding_native_test.go` matches existing base-workflow `operator_` selector; exact PR run | 44876072403 pending |
| `a131256c285e257837e402a9ba0fe037f0835bbe` | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` | `PR · Native Keycloak/Core · podman` | same exact selector and `scripts/ci-owner-node-native.sh` | 44876072403 pending |
| `a131256c285e257837e402a9ba0fe037f0835bbe` | `KeycloakSingleNativeRouteTests.test_foreign_core_network_test_selects_both_existing_pr_native_runtimes` | `PR · Focused Python` | changed existing selector regression test | 44876072403 pending |

## Shared gate context

- Run [44868911131](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131) on PR #1740 demonstrates the previous native Docker and Podman cells were green, while its single CLI-0 failure belonged to #1739. This is the before evidence from a different PR.
- PR #1734 run [44853938826](https://github.com/mcpdev80/baseharbor/actions/runs/44853938826) separately shows the Loki package shard green and only the inherited CLI/operator-auth shards red. It is not a claim that #1743 is mergeable.
- PR #1743 run 44876072403 is the after candidate; it must complete and the two exact native test events must be read from the logs. Earlier head attempts are superseded, not acceptance evidence.

## Local verification

The selector suite (6 tests), gate-coverage suite (36 tests), CI impact selector script, focused Go compilation, and `git diff --check` passed as recorded in round 3. The focused Go test locally reports its explicit opt-in skip; hosted Docker and Podman evidence is still mandatory. Do not close the card or merge the PR while run 44876072403 is pending or any required check is red.
