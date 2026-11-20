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
owner: w165-pr0428-165-kchunt
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---
- [x] t-20261120-r28-bughunt-keycloak-signal-scope · projekt-enthalzung der signal-ids befunden #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/capability #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w165-pr0428-165-kchunt  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w165-pr0428-165-kchunt  
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

jagd H-V12 mit DREI funden — der erste treffer dieser nacht, und alle drei sind von MIR am quelltext nachgemessen: (1) keycloak_realization.go registrationID := 'keycloak:' + r.files.Project, projectToken faltet '.' zu '-' -> 'my.identity' und 'my-identity' sind ununterscheidbar (karte 0428-166); (2) vier provider bauen die identitaet nach derselben regel, aber internal/logs/realization.go traegt weiterhin das LITERAL 'loki-metrics' ohne projekt,waehrend keycloak/tempo/telemetry das projekt tragen (karte 0428-167); (3) #1707 anderte die ID-regel OHNE bestandsumschreibung — eine bestehende 'keycloak-metrics'-registration ist nach dem deploy weder sichtbar (List, registry.go:383) noch loeschbar (Remove, :367), sie wird zur unreachbaren leiche (karte 0428-168). akte 16978 bytes, checkboxen null. Fund-zu-karte-pflicht ERFUELLT: drei karten, alle mit dieser akte als evidence, 0428-168 blockiert 166 und 167 (reihenfolge steht in den karten)
