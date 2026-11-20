---
id: t-20261120-r28-signal-id-normalization-collision
kanban_title: 0428-166 · signal id token collision
card_number: "0428-166"
card_short_title: "signal id token collision"
type: bug
areas: [observability, capability]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: [t-20261120-r28-keycloak-signal-id-migration-gap]
blocked_by: []
superseded_by: []
owner: ""
kanban_status: planned
kanban_lane: planned
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md"]
prs: []
created: 2026-11-20
---

- [ ] t-20261120-r28-signal-id-normalization-collision · collide project names by token fold #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261120-r28-keycloak-signal-id-migration-gap](t-20261120-r28-keycloak-signal-id-migration-gap.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-keycloak-signal-id-migration-gap](t-20261120-r28-keycloak-signal-id-migration-gap.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Karte aus Bug-Hunt H-V12 (FUND 1, K1). Die Keycloak-Signal-ID wird als
`"keycloak:" + r.files.Project` gebaut; `projectToken` faltet jedes `.` zu `-`.
Damit sind `my.identity` und `my-identity` im selben Registry-Raum nicht unterscheidbar.

## Befund (Quelle: Akte, vom Coordinator am Quelltext bestaetigt)

- `internal/identityprovider/keycloak_realization.go:134` (`registrationID := "keycloak:" + r.files.Project`)
- `internal/runtime/project.go` (`projectToken`: lowercase, trim `-`, `.` -> `-`)
- Der Praefix ist konstant, die Faltung ist uralt — das Loch ist die ungesicherte
  Normalisierungs-Grenze, nicht die neue ID-Formel.

## Erwartung vs. Ist

Erwartet: zwei verschiedene Projekte ergeben zwei verschiedene Signal-IDs.
Ist: zwei verschiedene Projekte mit `.` statt `-` ergeben dieselbe ID.

## Stop-Kriterium

Wer die ID-Formel aendert, aendert die Rueckwaertskompatibilitaet (Karte 0428-168).
Diese Karte ist NACH 0428-168 zu nehmen, nicht davor.

## Akte

https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md
