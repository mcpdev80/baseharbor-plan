---
id: t-20261121-native-cell-operator-seam
card_number: "0428-209"
card_short_title: "0428-209 native cell seam"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: b90e4ba1 (candidate delivered) / Coordinator
kanban_status: review
kanban_lane: review
kanban_summary: "controlplanesinglenativecitest.go stops failing with prepare BaseHarbor integration trust plane: because the native-cell test…"
kanban_title: 0428-209 · 0428-209 native cell seam
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1740, mcpdev80/baseharbor#1765, mcpdev80/baseharbor#1766]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1740", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/operator-auth-helper/carrier-census-1737-1738-1740-1741.md", "https://github.com/mcpdev80/baseharbor/pull/1765", "https://github.com/mcpdev80/baseharbor/actions/runs/45021008989"]
  - "https://github.com/mcpdev80/baseharbor/pull/1740"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44868911131"
---

- [ ] t-20261121-native-cell-operator-seam · 0428-209 stamp the native Keycloak/Core cell through the runWithIO seam #task #release/v0-4-28 #status/review #view/review #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** b90e4ba1 (candidate delivered) / Coordinator · **Priority:** high  
    **PR:** [baseharbor#1740](https://github.com/mcpdev80/baseharbor/pull/1740), [baseharbor#1765](https://github.com/mcpdev80/baseharbor/pull/1765), [baseharbor#1766](https://github.com/mcpdev80/baseharbor/pull/1766)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1740), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/operator-auth-helper/carrier-census-1737-1738-1740-1741.md), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1765), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/45021008989), [proof 5](https://github.com/mcpdev80/baseharbor/pull/1740), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44868911131)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** b90e4ba1 (candidate delivered) / Coordinator  
**Priority:** high  
**PRs:** [baseharbor#1740](https://github.com/mcpdev80/baseharbor/pull/1740), [baseharbor#1765](https://github.com/mcpdev80/baseharbor/pull/1765), [baseharbor#1766](https://github.com/mcpdev80/baseharbor/pull/1766)  
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

END_BLOCKED gemeldet, von mir bestaetigt: ihre fix wirkt (der "bootstrap target is not configured"-fall ist behoben), aber der test haelt an cmd/baha/operator_auth_boundary.go:113 an ErrConfigurationRequired, und internal/operatorauth/** ist Tabu. Das ist dieselbe owner-entscheidung wie 0428-214. NEUER VERFAHRENSBEFUND von mir: fuer GRUENE shard-jobs ist der test-detail gar nicht im protokoll - cli-2 (success) liefert 22242 bytes ohne einzige RUN-/PASS-/ok-zeile, cli-0 (failure) 23033 bytes mit FAIL-zeile. "test laeuft remote im shard" ist aus gruenen logs also NICHT beweisbar; die mutation (rot/weiss) bleibt der einzige beleg, plus job-success. Bitte nicht als unterstellung buchen.

ROUTE NEU FESTGELEGT NACH CENSUS (akte operator-auth-helper/carrier-census-1737-1738-1740-1741.md, plan commit da2176f7f40, von 1450c201 gemessen): PR 1726 wird NICHT wieder eroeffnet und es entsteht KEIN neuer traeger - #1750 ist gemergt, also wird der JEWEILIGE eigene delta des kandidaten auf develop 8629450ef3c neu geschnitten. Fernzeugnis der kinder: alle back=275, mergeStateStatus UNSTABLE, base zeigt auf die tote basis lane-0428-198-cli-shard-operator-env (spitze e45430f2f1b). Carrier-abhaengigkeit: ja. Ihr PR-head gemessen: 1740 siehe akte 'Child PR state and diff against the named carrier'. Naechster schritt: mission auf dem ersten freien arbeits-sitz (neu schneiden statt hoepfen; bei 'nein' reicht der additive hop), dann exact gehosteter durchgang + unabhaengige pruefung. Kein merge aus der alten basis heraus.

RE-CUT ROUTE BESTAETIGT (praegenz 1738): PR 1740 haelt, base von der TOten carrier-lane 198 auf develop retargeted + head auf develop-basierten recut (kandidat f4e340eca, 2 files: selection-regression-assertion + bootstrap-target helper). EXAKTE native docker+podman gaetes + unabhaengige review danach. Kein neuer PR. Kein app_broker/controlplaneruntime-zugriff (0428-237).

ROUTE-WECHSEL bestaetigt: statt #1740 base-retarget wurde ein NEUER develop-basierter PR #1765 (head f4e340eca, 2 files: selection-regression-assertion + bootstrap-target helper, BASEHARBOR_TARGET erst nach registration) geoeffnet. #1740 (toter carrier-base) bleibt OFFEN bis #1765 verifiziert+gemerged ist, dann ersetzt/geschlossen. f0f6c8b4 von #1740 abgezogen (kollision). Exakte PR-checks (native docker+podman) starten; unabhaengige review = 1450c201, an terminal-gruen gebunden.

#1765 = GANZE cluster-abhaengig, NICHT sein 2-file delta. Run 45018856573: nativ docker data-capabilities 137197810751 failt secrets broker unhealthy (-> 0428-237, separater PR, laeuft bei Codex Runner), selected docker 137198119508 'app footprint show' confirm-candidate consent + contract (-> #1753 0428-227, EINGEFROREN bis 237-PR), native keycloak/core docker+podman stale network-owner assertion (-> #1766, korrigiert genau das). #1765 own delta ist OK; es kann erst gruen wenn 237-PR + #1766 + #1753-consent auf develop sind. ROUTING an besitzer: broker=0428-237 Codex Runner, candidate-consent=0428-227 (0847d100 triagiert mutation-vs-read, haelt #1753-push), assertion=#1766 (1450c201 review). 0428-232 demo 240e325 (0847d100) = static-mcp behoben.

#1765 = NICHT sein delta. Beide native data-capabilities docker 137197810751 + podman 137197810744 failen TestApplicationCapabilityLifecycleExistingCore/secrets (broker /readyz 503/not_ready, podman FailingStreak 49) = 0428-237. selected docker 137198119508 + podman 137198119493 failen footprint show confirm-candidate = 0428-227 mutation-consent (#1753, eingefroren). native keycloak/core = #1766 assertion. Coreless/guided laufen noch. #1765 haelt an DENSELBEN cluster wie #1753. Wait, nicht review.

Nach #1766 ist die stale assertion KEIN #1765-blocker mehr (beide native keycloak/core green). Was bleibt ist DERSELBE cluster wie #1753: broker 503 (0428-237) + selected confirm-candidate consent (0428-227, braucht Core/owner decision, karte 236 dropped). Delta sauber. PR-ref #1740->#1765 (owner bat darum bei closeout).

TP-fund von b90e: eigene neue source cmd/baha/control_plane_single_native_ci_test.go war nie katalogisiert -> fail-loud guardian. Lane-fix im selben PR (test-to-CI-Aufnahmepflicht, katalog ist Codeman-owned): b90e ergaenzt die source-entry (analog target_runtime_access_provider_test.go: runtime_specific + beide data-capabilities surfaces) + hoppt final auf develop b48ac03ef, ein Push, ein exact-head run.

stand: components-eintrag formgleich platziert (+9, nur eigene zeilen), TP dennoch uncataloged -> inbox-hint gegeben: praezedenz #1786 (978a0f90) dateiuebergreifend replizieren + base-vs-head-lesepfad des guardians belegen. Zweiter identischer failure = eskalation der guardian-diagnose an codex (planned karte 0428-249 grenze beachten: kein .github).

EXAKT-GRUEN: head c8bbb0f52, run 45087109688 SUCCESS (required: TP+selected+native+Go), mergeState CLEAN, dedup-hop korrekt (katalog byteidentisch develop, base-row aus #1790). Uebergeben an CODEX 1450c201 (REVIEW->MERGE, owner-anweisung 02:0x).
