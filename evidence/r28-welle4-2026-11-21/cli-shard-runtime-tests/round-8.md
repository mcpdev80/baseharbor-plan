# 0428-215 round 8 — exact run 44878727267

- PR #1743 candidate: `57e7941772ce85dbc60bad7faddd3613c3191c4c`.
- Trigger: pull request; exact hosted workflow [44878727267](https://github.com/mcpdev80/baseharbor/actions/runs/44878727267).
- Test ID: `github.com/mcpdev80/baseharbor/cmd/baha::TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork`.
- Mapping: existing `PR · Native Keycloak/Core · docker` and `PR · Native Keycloak/Core · podman` cells; exact selected test is explicitly invoked in both.
- Docker log: test ran and PASSed (0.16s), without skip. The job then failed at the separate existing `TestControlPlaneSingleDefaultNativeRuntimeInCI`: integration target `w169-ci-bootstrap-9438a4f9` is not configured.
- Podman log: test ran and PASSed (0.22s), without skip. The job then failed at the same separate existing test: target `w169-ci-bootstrap-a755c994` is not configured.
- Exact run's four Go `cli-*` shards are red on managed-operator authentication fixture failures (e.g. `TestMCPRegistrationCIInProcessDiscoverAndInvoke` reports `authentication_failed`). This is the shared auth gate owned by the separate #1615 session; this sweep did not inspect or modify #1615 or its files.
- `PR · Focused Python`, workflow policy, trusted plan, source format, validation `cli-build`, `ci-policy`, `ci-executor-tests`, `source-contracts`, `receipt-execution-tests`, `cli-vet`, and `cli-gofmt` pass. `PR · Validation · pr-planner-tests` fails; native Docker/Podman and CLI shards fail; aggregate required checks are not green.
- Outcome: the 0428-215 regression itself is proven on both native runtimes. PR and card cannot be accepted/closed while the exact required run is red; retain Wait with the concrete next gate, not as a claim the new test is unimplemented.
