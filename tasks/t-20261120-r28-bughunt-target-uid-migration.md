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
kanban_status: active
kanban_lane: active
blocker: ""
resolution: ""
evidence: []
prs: []
created: 2026-11-20
wait_reason: ""

---

- [ ] t-20261120-r28-bughunt-target-uid-migration · target-uid-migration gegen idempotenz pruefen #task #release/v0-4-28 #status/active #view/active #area/capability #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w161-pr0428-161-tuidhunt  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
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
