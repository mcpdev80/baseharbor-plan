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
kanban_status: review
kanban_lane: review
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44692628196", "https://github.com/mcpdev80/baseharbor/actions/runs/44699615600", "https://github.com/mcpdev80/baseharbor/actions/runs/44700696085", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1709-0428-168-r2.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1709-0428-168-r3.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md"]
prs: [mcpdev80/baseharbor#1709]
created: 2026-11-20
wait_reason: ""

---

- [ ] t-20261120-r28-keycloak-signal-id-migration-gap · migrate un-prefixed keycloak registrations #task #release/v0-4-28 #status/review #view/review #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** w168-pr0428-168-signal-mig-r3  
    **PR:** [baseharbor#1709](https://github.com/mcpdev80/baseharbor/pull/1709)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44692628196), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44699615600), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44700696085), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1709-0428-168-r2.md), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1709-0428-168-r3.md), [proof 7](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
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

EINFRIEREN VON MIR VERIFIZIERT (unabhaengig von ihrer meldung, 10:0xZ): ls-remote lane-origin zeigt refs/heads/lane-0428-168-signal-id-migration = refs/pull/1709/head = 1fa78df421e5; PR base.sha = 36d075fad77f (develop-spitze), draft=false, 8 dateien; 'git fetch lane-origin refs/pull/1709/head' dann merge-base --is-ancestor = JA; 6 eigene commits ueber develop (log: keine fremden lane-commits). run 44700696085 = in_progress am EINGEFRORENEN head, created 08:12:25Z. neuer inhalt im letzten commit: partielles owner-Scan-Fallthrough, internal/identityprovider/keycloak_realization.go:217-227 und :323-335, mit tests + mutation proof D. KARTE BLEIBT active, NICHT review: die abnahme wird erst bestellt, wenn der run TERMINAL ist und ihre akte auf main liegt - das ist die regel, die ich nach dem unterbrochenen r2-review (candidate changed during review) selbst gesetzt habe. akte bisher: signal-id-migration/fix-2.md @ 38535a8d

## Fresh head after interrupted review — 2026-11-20 08:05 UTC

PR #1709 advanced during CODEX-REVIEW r2 to `380c66c49218a3f8c18d04412536acbc6a2c3a6d`, so the r2 artifact's final verdict is **BLOCKED / stale candidate**, not a verdict on this SHA. Exact run [44699615600](https://github.com/mcpdev80/baseharbor/actions/runs/44699615600) is still in progress; all Go shards/build/vet and package tests have passed, with the selected Docker identity runtime job remaining. Independent exact-head review confirms the stable-sort test is now discoverable in `read_signals_test.go`, but the required migration assertions for source metadata (including Target/Network/Path/Scheme/Descriptor/Enabled) remain absent; `stampLegacyTarget` rewrites Target. Owner-state discovery still swallows `ListKeycloakOwnerProjects`/per-owner `ReadDir` errors instead of failing closed before migration. GitHub reports PR OPEN/non-draft, mergeStateStatus BLOCKED, zero formal reviews. The owner is advancing the candidate; move 0428-168 back to Active while these current-head blockers and the runtime result are resolved. Do not apply run `44696406664` or review r2 as evidence for this newer SHA.

abnahme bestellt, weil alle drei bedingungen der einfrier-regel erfuellt sind: (1) head 1fa78df421e521ab7aeaec05a58d6cf646ddf971 eingefroren, branch = refs/pull/1709/head, kein weiterer push; (2) run 44700696085 am exakten head completed/success, 35/35 checks, 0 failure, auch 'PR · Source format' und 'PR Selected Checks' gruen; (3) akte evidence/r28-welle4-2026-11-20/keycloak-signal-migration/round-3.md auf origin/main (plan head c2e062cf) mit ls-remote-, merge-base- und mutationsbeweis-zeilen. waehrung unabhaengig gemessen: develop 36d075fad77f ist ahne, base.sha = develop-spitze, draft=false, mergeable=clean, 6 eigene commits. CODEX-REVIEW r3 am eingefrorenen head unterwegs (session 95971e0a, rolle REVIEW, akte 1709-0428-168-r3.md), mit bitte, bei APPROVE signatur + rueckgabe des helpers fuer folgekarte 0428-166 anzugeben. reinlichkeit gemeldet: keine container/compose gestartet, /tmp-worktrees entfernt

verdict r3 am eingefrorenen head liegt vor und ist gueltig (akte 1709-0428-168-r3.md: 'PR head before review' = 'PR head after review' = 1fa78df421e5, von mir nachgemessen: branch = refs/pull/1709/head, mergeable=clean). resultat: REQUEST CHANGES, ein blockierender befund (P1-restfall). stelle am eingefrorenen head: internal/identityprovider/keycloak_realization.go, ownerProjectMaps ab :220, :235 ListKeycloakOwnerProjects, :237 'return nil, err', :239-240 nur bei len(recorded)>0. fehlender fall: owner-VERZEICHNIS fehlt (os.ErrNotExist), der abgeleitete scan findet mindestens einen anderen besitzer -> maps werden verworfen. der echte scan-fehler muss weiter abbrechen (ihr r3-pfad, unangetastet). P2 (internal/observability/keycloak_legacy_migration_test.go:138-205) und P4 sind ADRESSED, keine nacharbeit (§5.4). reviewer bestaetigt aus dem log von run 44700696085: packages-shard faehrt TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle ohne filter. korrekturauftrag zugestellt (9d1d1205 busy): not-exist vs echter fehler trennen, abgeleitete besitzer weiterreichen, zwei tests mit mutationsbeweis. 0428-166: nichts genehmigt, RebookLegacySignals nur 'interface planning only', finalsignatur folgt aus der r4-akte

r4 am eingefrorenen head, alle drei bedingungen von mir nachgemessen: (1) head 489e4e66a2b1 = branch = refs/pull/1709/head, kein weiterer push; (2) run 44704834012 completed/success am exakten head, base.sha = develop-spitze 36d075fad77f, draft=false, mergeable=clean, 8 dateien, merge-base --is-ancestor = JA; (3) akte keycloak-signal-migration/round-4.md (228 zeilen) auf main @ 6c6748c74a3b. inhalt der runde: union des abgeleiteten legacy-owner-maps mit dem aufgezeichneten map bei nicht-leerem recorded, ListAll-fehler wird weitergereicht statt umgewandelt, fail-closed abort; der echte scan-error-pfad aus r3 bleibt unangetastet (mutationsbeweis D gilt weiter), neuer beweis E in der akte. CODEX-REVIEW r4 am eingefrorenen head bestellt (session 95971e0a, rolle REVIEW, akte 1709-0428-168-r4.md), auftrag enthaelt die bitte, bei APPROVE die signaturen RebookLegacySignals und MigrateScopedMany woertlich aus dem code zu bestaetigen - damit kann folgekarte 0428-166 ohne raten anfangen
