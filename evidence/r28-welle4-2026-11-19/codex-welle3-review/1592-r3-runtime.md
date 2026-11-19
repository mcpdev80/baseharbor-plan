# CODEX-REVIEW — PR #1592 / 0428-088 runtime witness qualification

Date: 2026-11-19  
Role: CODEX-REVIEW  
PR head: `c452f705c2dac4d807da3146ddadd716ee66a467`  
Current develop: `deeeb64778b3f6109d3a8e49fd652d490901e89c`  
Exact-head hosted CI: [44456253144](https://github.com/mcpdev80/baseharbor/actions/runs/44456253144)

## Runtime witness

The baha-docker evidence qualifies the previously missing runtime behavior: the isolated smoke ran on exact head `c452f705c`; Perses `v0.55.1` used the plugin tmpfs while the container root remained read-only; `GET /api/v1/plugins` returned 32 `PluginModule` entries and all 32 reported `status.isLoaded=true`. This directly falsifies the prior zero-module failure condition. The exact-head PR run `44456253144` is terminal SUCCESS.

## Acceptance status

**Runtime behavior: ACCEPTED. Overall card: NOT ACCEPTED for merge yet.** The evidence itself records that the changed `TestPersesRuntimeSmokeDockerIsolated` requires `BASEHARBOR_PERSES_RUNTIME_SMOKE=1`, while no existing workflow sets that variable or maps this test to a selected native gate. The task's test-to-CI rule requires an executable mapped CI/native-gate route for changed tests; the green PR run skips the runtime gate. Resolve the owner-scope coverage finding (or record an explicit authorized task exception) before final acceptance. No `.github/**` edit is assigned to this lane.

Current develop has moved past the candidate: `git ls-remote` confirms PR head `c452f705c...` and develop `deeeb6477...`; compare reports diverged (24 commits ahead, 9 behind, merge base `ec592fd38`). After coverage disposition, hop monotonically and obtain fresh exact-head CI before merge.

## END

END_RUNTIME_WITNESS_ACCEPTED / END_CARD_HOLD: the 32/32 loaded-plugin witness is valid; CI routing for the changed smoke test and a fresh post-hop exact-head run remain outstanding. No new run was started in this review.
