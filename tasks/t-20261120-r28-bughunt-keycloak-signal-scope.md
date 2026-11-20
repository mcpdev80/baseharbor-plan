---
id: t-20261120-r28-bughunt-keycloak-signal-scope
kanban_title: 0428-165 · bughunt keycloak signal scope
card_number: "0428-165"
card_short_title: "bughunt keycloak signal scope"
type: task
areas: [capability, cli]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: ""
kanban_status: planned
kanban_lane: ready
blocker: ""
resolution: ""
evidence: []
prs: []
created: 2026-11-20
wait_reason: ""

---
- [ ] t-20261120-r28-bughunt-keycloak-signal-scope · projekt-enthalzung der signal-ids befunden #task #release/v0-4-28 #status/planned #view/ready #area/capability #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Hunt-Schnitt H-V12 auf der soeben gemergten projekt-weiten Signal-ID-Enthaltung
(PR #1707, merge b7cbc00f0adf, 'scope Keycloak signal IDs by project'). Reine Befundung,
keine Produktaenderung, kein PR, keine VM. Funde gehen als eigene Karten zurueck.

## Pruefschnitte

1. K1: wie die Projekt-ID in die Signal-ID eingeht (Trenner, Kollisionsmoeglichkeit).
2. K2: alle anderen Stellen, die Signal-/Trace-Identitaeten fuer Perses bauen — gleiche Regel, zwei Stellen?
3. K3: Ablleseverhalten bestehender Registrationen ohne Praefix (verschwinden oder Leichen?).
4. K4: testet der Merge-Test Kollision oder nur Unterscheidung.

## Akte

evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md
