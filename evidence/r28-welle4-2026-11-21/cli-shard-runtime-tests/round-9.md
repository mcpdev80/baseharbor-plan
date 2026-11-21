# 0428-215 exact acceptance — 2026-11-21

- PR: [#1743](https://github.com/mcpdev80/baseharbor/pull/1743), merged normally as `4da7ce94b015d5bbd3a8006311785ade5f97b530`.
- Exact candidate SHA: `f0f25e49753ad6b06b490072739437eeec42de8a`, based on current `develop` `c2c94ad115ffa33e91efcd1be1fae6fc2bba7046`.
- Test ID: `github.com/mcpdev80/baseharbor/cmd/baha::TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork`.
- Mapping: `scripts/ci-owner-node-native.sh` explicitly invokes this exact test through `require_pass`; the same script runs in both existing native `PR · Native Keycloak/Core` cells. The script rejects a missing PASS, any skip, and any failure.
- Docker gate: `PR · Native Keycloak/Core · docker`, job `136795363531`, PASS. Log records the exact test PASS, no skip.
- Podman gate: `PR · Native Keycloak/Core · podman`, job `136795363590`, PASS. Log records the exact test PASS, no skip.
- Exact hosted run: [44887314441](https://github.com/mcpdev80/baseharbor/actions/runs/44887314441), terminal SUCCESS. `PR · Go unit · cli-0..3`, `PR · Validation · pr-planner-tests`, workflow policy, source format, and aggregate `PR Selected Checks` also PASS.
