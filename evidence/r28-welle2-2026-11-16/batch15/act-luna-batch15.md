# CODEX-REVIEW — Luna batch 15

**ROLE: REVIEW** · 2026-11-16 · no merge, no GitHub review mutation.

**Mission:** `coordinator/mission-luna-batch15.md` · object 1 PR #1660 / card 0428-097; object 2 is status only.

**Session identity:** Codex session `09fd9bba-985e-4058-a1f8-2d544bd7c3b0`; Codeman reports CLI `0.167.0`, display model `GPT-6-Luna` (`source=screen`).

## Object 1 — #1660 candidate and CI

- Authenticated GitHub account: `mcpdev80`.
- PR #1660 is OPEN and DRAFT; base `develop` @ `13ffdd15d24fcfb4a379c834d25450ebb2737a6a`; head `lane-0428-097-keycloak-signal` @ `f709e14b58f55be9e6ef93323e31bb9166aa04e8`.
- Diff is limited to `internal/identityprovider/keycloak_realization.go` and `internal/identityprovider/keycloak_signal_registration_test.go`.
- Exact-head run `43929204510` is `pull_request`, completed SUCCESS on the exact head. Six jobs succeeded and 25 were skipped. The skipped jobs are not merge evidence; the PR remains draft.
- No local product tests were run by this reviewer.

## Review findings

The registration uses the existing observability registry path, not a second resolver. Successful Keycloak `Apply` invokes `registerKeycloakSignals()`. That method resolves provider placement and metrics policy, builds the `keycloak-metrics` runtime signal only when policy enables collection, and registers it through `observability.RegisterProviderSignals` using `capability.KeycloakIntegration`. Its registry ID is the exact `keycloak-metrics` identifier read by the identity witness. The policy gate preserves fail-closed behavior when metrics collection is disabled.

The new positive test enables metrics, calls the registration method, lists the registry for the resolved placement, and verifies the Keycloak provider, exact ID, metrics kind, OpenMetrics protocol, and `/metrics` path. The negative test disables metrics and asserts the source is absent. The current 078 branch contains a positive witness regression using a registered `keycloak-metrics` source plus a valid resolved Keycloak placement; it derives a non-forgeable available witness. This corroborates that 097's registry identity and 078's reader match. No claim is made here about accepting or reviewing PR #1650.

The #1660 diff does not modify the 080 selection code or its non-forgeability tests. PR #1590 remains at r3 head `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`.

**Verdict: APPROVE CONTENT** for PR #1660 at `f709e14b58f55be9e6ef93323e31bb9166aa04e8`. This is a content verdict only; it does not accept the task or satisfy the skipped merge gates.

## Binding confirmation for 078

**Confirmed: 078 may build on the 0428-097 branch content at `f709e14b58f55be9e6ef93323e31bb9166aa04e8`.** The registered provider and source ID match the 078 witness lookup, and the registration stays gated by metrics policy. This confirmation is limited to the 097 registry-content interface; it is not a verdict on #1650. Per the mission, #1650 @ `d94d477d92f16c9fba5f76b681a332ee03f8456e` remains blocked pending 097 approval and rebase onto the closed ring; no review verdict is issued for it.

## repo-rule compliance and turn-start flags

- Read-only product review; no product code, PR state, CI, task state, or release state changed. No merge, approval, or GitHub review mutation.
- Turn-start flags forwarded to the coordinator: worker pool 0/4; `NO_ELIGIBLE_WORK` holds on ornith:1, ornith:2, laptop:1, laptop:2; 41 open PRs.
