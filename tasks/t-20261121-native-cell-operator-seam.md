---
id: t-20261121-native-cell-operator-seam
card_number: "0428-209"
card_short_title: "0428-209 native cell seam"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: wait
kanban_lane: wait
kanban_summary: "controlplanesinglenativecitest.go stops failing with prepare BaseHarbor integration trust plane: because the native-cell test…"
kanban_title: 0428-209 · 0428-209 native cell seam
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1740]
sources: []
blocker: ""
wait_reason: "NEUER STAND, gemessen 08:0xZ: der owner hat #1743 weiter gepusht (head jetzt 57e7941772ce, base develop, mergeStateStatus BLOCKED) und meine native-frage ist damit NICHT erledigt, sondern verschaerft: 'PR · Native gate plan' = success, 'PR · Trusted Plan' = success, ABER 'PR · Native Keycloak/Core · docker' UND '· podman' = FAILURE, 'PR · Native · matrix' = skipped, 'PR Selected Checks' = failure. Die zwei zellen, die meinen fall ausfuehren sollen, sind also ROT — ich weiss noch nicht, ob sie den fall ausfuehren und er scheitert, oder ob die zelle an eigener infraektion scheitert. Diagnose-lane laeuft (0428-215-nativefaildiag)."
resolution: ""
evidence:
  - "https://github.com/mcpdev80/baseharbor/pull/1740"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44868911131"
---

- [ ] t-20261121-native-cell-operator-seam · 0428-209 stamp the native Keycloak/Core cell through the runWithIO seam #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1740](https://github.com/mcpdev80/baseharbor/pull/1740)  
    **Waiting:** NEUER STAND, gemessen 08:0xZ: der owner hat \#1743 weiter gepusht (head jetzt 57e7941772ce, base develop, mergeStateStatus BLOCKED) und meine native-frage ist damit NICHT erledigt, sondern verschaerft: 'PR · Native gate plan' = success, 'PR…  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1740), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
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

Current branch `lane-0428-209-native-cell-operator-seam`, PR [#1740](https://github.com/mcpdev80/baseharbor/pull/1740), exact head `0ffe093357d9f7fb52f5e7542f4ade41e48fab1b`. The exact test `cmd/baha::TestControlPlaneSingleDefaultNativeRuntimeInCI` passed in both `PR · Native Keycloak/Core · docker` (job 136738825463) and `PR · Native Keycloak/Core · podman` (job 136738825465), run [44868911131](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131), triggered by the `pull_request` update to #1740. Focused local package invocation also passes (skips without native runtime opt-in). The full stacked PR run is not green: `PR · Go unit · cli-0` fails only on `TestAppListAllTargetsWorksAfterInstallationDestroy`, owned by 0428-210; `PR Selected Checks` consequently fails. This is handed off for independent review; do not mark accepted or merge #1740 until the stack's required checks are resolved.

Ein 'skipped' waere kein beweis gewesen (AGENTS 5.3); jetzt ist es rot statt skipped - beide faelle verlangen dieselbe antwort: datei:zeile der auswahl + ob der testkörper laeuft.
