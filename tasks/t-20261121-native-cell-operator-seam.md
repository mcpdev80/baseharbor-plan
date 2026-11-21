---
id: t-20261121-native-cell-operator-seam
card_number: "0428-209"
card_short_title: "0428-209 native cell seam"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: Codex team (current thread)
kanban_status: active
kanban_lane: active
kanban_summary: "controlplanesinglenativecitest.go stops failing with prepare BaseHarbor integration trust plane: because the native-cell test…"
kanban_title: 0428-209 · 0428-209 native cell seam
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1740]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-native-cell-operator-seam · 0428-209 stamp the native Keycloak/Core cell through the runWithIO seam #task #release/v0-4-28 #status/active #view/active #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** Codex team (current thread) · **Priority:** high  
    **PR:** [baseharbor#1740](https://github.com/mcpdev80/baseharbor/pull/1740)  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** Codex team (current thread)  
**Priority:** high  
**PRs:** [baseharbor#1740](https://github.com/mcpdev80/baseharbor/pull/1740)  
**Source:** 
<!-- /generated:links -->

## Goal

`control_plane_single_native_ci_test.go` stops failing with `prepare BaseHarbor integration trust plane:` because the
native-cell test support authenticates its `runWithIO` call through the same operator seam that 0428-204 introduces,
without changing production enforcement.

## Why

w218 diagnosed the third red cell (akte `evidence/r28-welle4-2026-11-20/native-keycloak-core-cell/round-1.md`):
`#1594` (develop `40cb28c758`) removed the dev-to-trusted-local auto-admit, so the native cell reaches
`cmd/baha/runtime_integration_test_support_test.go:722` (helper at `:1048`, routed through `runtime_withIO`,
`cmd/baha/main.go:147`) without a `VerifiedPrincipal` and fails with the verbatim 0428-204 gate message
(`internal/operatorauth/authorization.go:285`). w218 measured and stated the consequence explicitly: **0428-204 does not
cover this cell**, because that card stamps only contexts that pass through `runWithIO` in the CLI command tests, while
the native cell builds its contexts in the integration test-support helper.

## Scope

Allowed write-set:

- `cmd/baha/runtime_integration_test_support_test.go`
- `cmd/baha/control_plane_single_native_ci_test.go`

Forbidden:

- `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**` (Owner rails)
- every other file in `cmd/baha/` — 0428-204 owns those edits while it runs; this card is stacked behind it

## Acceptance criteria

1. The native cell test passes at the exact candidate head.
2. The helper authenticates through the shared seam helper introduced by 0428-204; a second private stamping path in this
   card is rejected in review.
3. Negative cases stay unauthenticated: any fail-closed assertion in these two files needs its own explicitly unstamped
   server or context (coordinator rule 2026-11-21).

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | native Keycloak/Core cell of PR Selected Checks |
| Test identifier | `0428-209` |
| Route | `auto-discovery` |

## Dependencies

Needs 0428-204's seam helper content (branch-level stacking, not a merge wait). Do not commission while 0428-204 still
writes in `cmd/baha/`.

## Stop and report

If the cell only goes green by changing enforcement or the auto-admit behaviour, stop and report file:line: that is an
Owner decision, not a test fix.

## Handoff

Current branch `lane-0428-209-native-cell-operator-seam`, PR [#1740](https://github.com/mcpdev80/baseharbor/pull/1740), exact head `8082766293bd807b1a5cd4f3dc34fd6723ab9ed5`. Added a regression assertion in `TestControlPlaneSingleDefaultNativeRuntimeInCI` that the trust-plane bootstrap Target is registered and resolves to the selected Docker/Podman runtime. The focused package command passes locally. Exact PR run [44868123470](https://github.com/mcpdev80/baseharbor/actions/runs/44868123470) is queued; it has not produced a terminal native-cell result. The previous run at `6f0fe16f` skipped the native matrix and does not satisfy acceptance. Final evidence will be recorded at `evidence/r28-welle4-2026-11-21/native-cell-operator-seam/round-1.md` after the exact native cell runs.
