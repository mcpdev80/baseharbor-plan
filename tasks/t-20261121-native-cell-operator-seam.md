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
evidence:
  - "https://github.com/mcpdev80/baseharbor/pull/1740"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44868911131"
---

- [ ] t-20261121-native-cell-operator-seam · 0428-209 stamp the native Keycloak/Core cell through the runWithIO seam #task #release/v0-4-28 #status/active #view/active #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1740](https://github.com/mcpdev80/baseharbor/pull/1740)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1740), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
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

diagnose abgenommen (akte round-2-nativefail.md, plan 8b955447, durchgang 44878727267 an #1743 head 57e7941772ce): (a) DER KORPER LAEUFT — '=== RUN TestControlPlaneSingleDefaultNativeRuntimeInCI' in docker (protokoll-zeile 542) UND podman (zeile 400), kein skip; ihre stellung (c) ist damit N/A, keine auswahl-regel fehlt. (b) scheitert am RUMPF, nicht an der infra: 'cmd/baha/control_plane_single_native_ci_test.go:30' ruft das paket-fixture 'ensureRuntimeIntegrationTrustPlane'; im teardown 'bootstrapTeardownProvider()' (internal/deployment) heisst es 'target \"w169-ci-bootstrap-a755c994\" is not configured' (zeile 543), 'bootstrap trust-plane teardown could not begin' (547), 'teardown left residual resources: no runtime provider available for target' (548). (c) sie weist die korrektur DEM EIGENEN write-set dieser karte zu (test-datei + fixture), also KEIN owner-eingriff. MEINE ZUSATZ-PFLICHT: ihr akte nennt 'operator_core_network_binding_native_test.go' NICHT — ob der #1743-eigene test in denselben zellen laeuft, bleibt fuer mich unbelegt; und der docker-job-log war fuer mich NICHT holbar (job 136769154180, '--log' wie '--log-failed' = 0 bytes, dasselge bekannte abhole-fehler wie bei 44865751734), also sind ihre zeilenangaben vorlaeufig der zeuge und die neue lane muss sie reproduzieren.
