---
id: t-20261117-hunt-signals-101
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-101"
title: "ID-Raum-Heterogenitaet und Keycloak-Kollision in Signal-IDs"
kanban_status: blocked
kanban_lane: blocked
kanban_title: 0428-101 · ID-Raum-Heterogenitaet und
kanban_summary: ""
sources: []
source_note: "hunt hunt-signals befund-1 (akte: evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)"
depends_on: []
owner: ""
blocker: "ZWEIFEL laut handoff: requiredes write-set (internal/id-...) ueberschneidet offenes #1650 (blockiert auf Owner-.github-struktur). naechster trigger: #1650-loesung. Stop-Akte signal-ids/stop-1.md"
wait_reason: ""
resolution: ""
superseded_by: ""
prs: []
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md"]
card_short_title: ID-Raum-Heterogenitaet und
---

- [ ] t-20261117-hunt-signals-101 · ID-Raum-Heterogenitaet und Keycloak-Kollision in Signal-IDs #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Blocker:** ZWEIFEL laut handoff: requiredes write-set (internal/id-...) ueberschneidet offenes \#1650 (blockiert auf Owner-.github-struktur). naechster trigger: \#1650-loesung. Stop-Akte signal-ids/stop-1.md  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** v0.4.28  
**Depends on:** none  
**Required by:** [t-20261117-hunt-signals-103](t-20261117-hunt-signals-103.md), [t-20261117-hunt-signals-104](t-20261117-hunt-signals-104.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Einzelschritte in der referenzierten hunt-akte (befund-1.md); Umsetzung als normale task-kette (claim -> branch -> CI -> evidence -> review).

## Handoff

**ZWEIFEL — returned to the queue without product changes.** The required Keycloak signal ID/registration change overlaps the open #1650 write set: `internal/identityprovider/keycloak_realization.go` is already changed by that lane. Touching it now risks conflicting with its owner and the unresolved #1650 acceptance path. No product branch, commit, push, or PR was created. Keep 0428-101 queued until #1650 resolves; Codeman should dispatch the next independent ready card (currently 0428-102) to the next free lane.
