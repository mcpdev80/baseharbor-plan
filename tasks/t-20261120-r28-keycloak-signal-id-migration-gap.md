---
id: t-20261120-r28-keycloak-signal-id-migration-gap
kanban_title: 0428-168 · signal id migration gap
card_number: "0428-168"
card_short_title: "signal id migration gap"
type: bug
areas: [observability, capability]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w168-pr0428-168-signal-mig-r3
kanban_status: active
kanban_lane: active
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44692628196", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md"]
prs: [mcpdev80/baseharbor#1709]
created: 2026-11-20
wait_reason: ""

---

- [ ] t-20261120-r28-keycloak-signal-id-migration-gap · migrate un-prefixed keycloak registrations #task #release/v0-4-28 #status/active #view/active #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w168-pr0428-168-signal-mig-r3  
    **PR:** [baseharbor#1709](https://github.com/mcpdev80/baseharbor/pull/1709)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44692628196), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261120-r28-provider-signal-id-scope-inconsistency](t-20261120-r28-provider-signal-id-scope-inconsistency.md), [t-20261120-r28-signal-id-normalization-collision](t-20261120-r28-signal-id-normalization-collision.md)  
**Owner:** w168-pr0428-168-signal-mig-r3  
**Priority:** not set  
**PRs:** [baseharbor#1709](https://github.com/mcpdev80/baseharbor/pull/1709)  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Karte aus Bug-Hunt H-V12 (FUND 3, K3). PR #1707 hat die Keycloak-Signal-ID von
`"keycloak-metrics"` auf `"keycloak:<project>"` umgestellt, ohne Bestandsumschreibung.

## Befund (Quelle: Akte)

- Vor #1707: `ID: "keycloak-metrics"` (wörtlich, aus dem Merge-Diff gestrichen).
- Nach #1707: `ID: "keycloak:" + r.files.Project` = z. B. `keycloak:bh-<target>-<app>-identity-<env>`.
- `List` (`internal/observability/registry.go:383`) und `Remove` (`:367`) arbeiten auf exakter ID.
- Eine bestehende Registration ohne Präfix wird damit nach dem Deploy **nicht mehr gefunden** —
  sie ist weder sichtbar noch löschbar.

## Erwartung vs. Ist

Erwartet: Ein Deploy der ID-Regel behält bestehende Registrationen beobachtbar oder stellt sie um.
Ist: bestehende Registrationen werden zu unreachbaren Leichen.

## Reihenfolge

Diese Karte blockiert 0428-166 und 0428-167 (jede weitere ID-Änderung vertieft das Loch).

## Akte

https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md

loop-abbruch angeordnet (§3.6): gemessen 861 FAIL-zeilen, 234 paketlaeufe, ein test 177x rot. der wichtige unterschied: ihr NEUER test und ReconcileLegacySignals existieren NICHT auf develop (git grep leer), aber TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle EXISTIERT dort (internal/application/shared_postgres_runtime_owner_test.go) und laeuft dort gruen (develop-push 44669117744/44669117784 success, packages-shard ohne namenfilter) — bei ihnen rot. das ist inhalt, nicht umfeld. befehl: zuerst WIP-stand ausliefern (vier stunden arbeit existieren nur auf diesemrechner = derselbe risikotyp wie bei karte 078), dann nur noch isolierte -run-laeufe mit den beiden FAIL-Blocken woertlich in die akte. DECKEL: scheitert ein weiterer anlauf an demselben existierenden test, rotation auf frische Lane


## PR #1709 exact-head refresh — 2026-11-20 ~07:12 UTC

The owner advanced #1709 to head `4d3494ea7a145e2a92c8008eb510d3c5b49ad06c`; exact run [44692628196](https://github.com/mcpdev80/baseharbor/actions/runs/44692628196) is still in progress. At the latest live read, 34 jobs were present: 15 successful, 16 skipped, `PR · Source format` failed, and Go/runtime jobs were still running. The maintainer findings in comment [7029213393](https://github.com/mcpdev80/baseharbor/pull/1709#issuecomment-7029213393) remain the acceptance reference: preserve legacy owner/source fields through the complete registration path, and ensure the stable-sort regression is in a Go-discoverable `_test.go` file. Keep this task Active while the owner works; do not infer acceptance from the partial run. See the [sweep snapshot](../evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md).

## Exact-run terminal result — 2026-11-20 ~07:20 UTC

Run [44692628196](https://github.com/mcpdev80/baseharbor/actions/runs/44692628196) completed FAILURE on exact head `4d3494ea7a145e2a92c8008eb510d3c5b49ad06c`: 35 jobs, 17 success, 16 skipped, 2 failures (`PR · Source format`, `PR Selected Checks`). The source-format log reports `internal/observability/registry.go has 930 lines (limit: 800; baseline ratchet: 0)`; Selected Checks is blocked by `source_format`. The Docker identity runtime job completed, but the test `TestReadSignalsForTestSortsStably` remains in `read_signals_test_helper.go`, which Go does not discover as a test file. Independent current-diff review finds partial progress on the legacy-owner defect: migration is now in the same `RegisterProviderSignals` mutation, with appA/appB coverage for owner ID/list/remove. It still does not assert all preserved metadata fields (network, target, descriptor, enabled state). The maintainer acceptance in comment [7029213393](https://github.com/mcpdev80/baseharbor/pull/1709#issuecomment-7029213393) remains outstanding, and `TestReadSignalsForTestSortsStably` is still in a non-`_test.go` filename so Go will not discover it. PR remains OPEN at this head with no formal review; keep 0428-168 Active while the owner fixes the candidate. See the [sweep snapshot](../evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md).

uebergabe dokumentiert (§3.6): die vorige session ist entlassen, ihr END_BLOCKED-grund war 'Der Kontext meiner Session erreichte sein Limit' — kein inhaltliches problem, aber eine frische session war faellig. ihr stand ist NICHT verloren: PR #1709 head 4d3494ea7a14 liegt bei github (35/35 checks fertig, 2 failure = 'PR · Source format' + 'PR Selected Checks'). die neue lane uebernimmt mit dem ausdrücklichen hinweis, den die vorige nicht genutzt hat: der EXISTIERENDE develop-test TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle (internal/application/shared_postgres_runtime_owner_test.go) war bei ihr rot, ihr neuer test 234x — ein auf develop grüner, am zweig roher test ist inhalt (§5.3), keine umgebungsfrage. akte round-3.md mit uebernahme-protokoll

uebernahme hat in 30 minuten geliefert, wofuer die vorige session 4 stunden brauchte und dabei nur lokal arbeitete: head 85bb4b4a4cb8, base.sha = develop-spitze 36d075fad77f, draft=false, 7 dateien, 35/35 checks completed, 0 failure, mergeable=clean. waehrung gemessen: fetch refs/pull/1709/head, merge-base --is-ancestor = JA. CODEX-REVIEW r2 bestellt (session 95971e0a, rolle REVIEW, akte 1709-0428-168-r2.md) mit zusatzauftrag: die rezept-tests muessen den ECHTEN register-/change-strom aufrufen, und der EXISTIERENDE shared-postgres-test muss gruen bleiben. ihre akte fix-2.md raeumt ein, dass meine messung 'head stuck at 0d1568ec4dc8 seit 03:13Z' wahr war: der zustand war nie bei github

CODEX-REVIEW r2 = BLOCKED, nicht inhaltlich: 'Review stopped: candidate changed during review' (akze 1709-0428-168-r2.md). angefragt war 85bb4b4a4cb8, der reviewer traf 380c66c49218 vor (branch + refs/pull/1709/head identisch, mergeable=blocked). URSACHE IST MEIN VERFAHREN: ich habe die abnahme bestellt, waehrend die lane noch gearbeitet und gepusht hat. inhalteilich haelt der reviewer in diesem unterbrochenen protokoll fest: P1 largely addressed, P2 addressed (registry.go:708-710 fuehrt mutation ueber mutateChanged), P4 addressed, und der packages-shard die neuen tests ausfuehrt. karte zurueck auf active; einfrier-befehl hinaus (kein push bis abnahme-bestellung), dann review am EINFRIERTEN head
