---
id: t-20261120-r28-pr-inventory-audit
kanban_title: 0428-160 · pr inventory audit
card_number: "0428-160"
card_short_title: "pr inventory audit"
type: task
areas: [cli, application, security]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w160-pr0428-160-prinv
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---
- [x] t-20261120-r28-pr-inventory-audit · offene pull-requests des fensters inventurieren #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/application #area/cli #area/security #kind/task
    <!-- generated:card -->
    **Owner:** w160-pr0428-160-prinv  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w160-pr0428-160-prinv  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
## Ziel

Inventur aller offenen Pull-Requests des 0.4.28-Fensters ( basics-check meldet 25 gegen sollwert 12): je PR zustand,
kopf-alter, basis-abstand, schreib-konflikt und ein urteil in genau drei kategorien. Reine verifikation, KEINE
produktaenderung, KEIN schliessen von PRs (das ist meine aktion).

## Pruefschnitte

1. Symlink-Enthaltung an jedem Ort, der einen Component-Pfad aufloest (S1).
2. 'unique components' gegen registry und footprint (S2).
3. maschinelle CLI-Registrierung (machine_coverage.go, handschriftlich) gegen den echten Kommando-Baum (S3).
4. wizard- und mcp-Pfade gegen denselben Validierungshelfer wie der source-model-Zweig (S4).

## Akte

evidence/r28-welle4-2026-11-19/pr-inventory-audit/round-1.md

inventur geliefert und von mir akzeptiert: 25 offene PRs gegen die gh-api verifiziert, urteil in den drei erlaubten kategorien — 7 AMEN (#1704 #1702 #1693 #1690 #1615 #1596 #1580), 7 HOPF-FREI (#1684 #1695 #1650 #1614 #1625 #1623 #1606), 11 SUPERSEDED/TODC (#1627 #1620 #1597 #1594 #1665 #1645 #1591 #1588 #1587 #1585 #1582). akte 14768 bytes auf main 7b687538, checkboxen null. FOLGE, die ich selbst ziehe: die 11 superseded-kandidaten schliesse ich NICHT unprueft — §3.8 verlangt ancestry-/blob-nachweis pro einzelfall, und ein fehlgeschlossener nachweis ist ein verlust. dafuer laeuft karte 0428-164 (blob-identitaet + brett-wahrheit). NEBENBEFUND von mir gemessen: #1645 liegt in der TODC-menge, damit ist die write-set-kollision mit #1614 (cmd/baha/app_status_result.go) fuer den ownerentscheid 062 entschaerft, aber nicht geloest
