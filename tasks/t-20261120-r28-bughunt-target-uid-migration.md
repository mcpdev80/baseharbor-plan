---
id: t-20261120-r28-bughunt-target-uid-migration
kanban_title: 0428-163 · bughunt target uid migration
card_number: "0428-163"
card_short_title: "bughunt target uid migration"
type: task
areas: [capability, cli]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w161-pr0428-161-tuidhunt
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-target-uid-migration/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [x] t-20261120-r28-bughunt-target-uid-migration · target-uid-migration gegen idempotenz pruefen #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/capability #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w161-pr0428-161-tuidhunt  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-target-uid-migration/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w161-pr0428-161-tuidhunt  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Hunt-Schnitt H-V11 auf dem frisch gemergten uid-target-pfad: PR #1580, merge bbc937c8f1,
darin "fix: serialize legacy target UID migration writes" und "no-mutation in MigrateLegacyTargetUIDs".
Reine Befundung, keine Produktaenderung, kein PR, keine VM. Funde gehen als eigene Karten zurueck.

## Pruefschnitte

1. V1 Idempotenz: zwei Laeufe der Migration auf demselben Bestand, zweiter muss inhaltlich leer ausgehen.
2. V2 Serialisierung: zwei schreibende Zugariffe gleichzeitig, kein verlorener und kein doppelter Eintrag.
3. V3 No-Mutation-Regel: MigrateLegacyTargetUIDs darf eine bestehende uid nicht veraendern.
4. V4 Beobachterfrage: was sehen status- und desk-pfad vor und nach der Migration.

## Akte

evidence/r28-welle4-2026-11-19/bughunt-target-uid-migration/round-1.md

jagd H-V11 BEFUNDBLOS, vier szenen je mit zeuge (akte 8643 bytes, 15 datei:zeile-belege, main 6b1a2b9e): V1 idempotenz zweiter lauf laedt dieselbe uid, config-bytes unveraendert (TestV1Sec...); V2 serialisierung ueber AcquireStateFileLock (config_mutation.go:77) auf .installation.lock (lock_unix.go); V3 no-mutation bestehende gemappte uid bleibt, aufrufer-map unangetastet (target_id.go:88); V4 beobachter status/desk lesen identitaet aus .baseharbor/.apps (app.go:118), entkoppelt von der migration. cleanliness: clean. Fund→Karte-pflicht: kein fund, keine karte. WERT FUER DAS DOSSIER: der merge bbc937c8f1 (#1580) ist damit von der QUELLEN seite befunden; die blob-seite prueft karte 0428-164
