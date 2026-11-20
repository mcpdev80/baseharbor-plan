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
owner: 0428-166-
kanban_status: active
kanban_lane: active
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [ ] t-20261120-r28-signal-id-normalization-collision · collide project names by token fold #task #release/v0-4-28 #status/active #view/active #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** 0428-166-  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-keycloak-signal-id-migration-gap](t-20261120-r28-keycloak-signal-id-migration-gap.md)  
**Owner:** 0428-166-  
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

sitz frei geworden durch 0428-175s accepted-merge, sofort mit dieser karte besetzt (fuellregel: jagd weicht kartenarbeit). neue frische lane '0428-166-' (sid 29da50cc, laptop-kanal 2/2, model worker-ornith1.5-laptop, readiness von spawn-lane.sh verifiziert, parent-link verified). vorgaenger 0428-168 ist GEMERGT (develop 681700ca66f3), damit ist ihr depends_on-feld erfuellt - karte war 'ready'. grund des ansatzes, am quelltext bestaetigt: registrationID := 'keycloak:' + r.files.Project in internal/identityprovider/keycloak_realization.go:134, und projectToken in internal/runtime/project.go faltet lowercase + '.' -> '-', wodurch 'my.identity' und 'my-identity' im selben registry-raum dieselbe id ergeben. auftrag traegt zwei grenzen: (1) die ID-FORMEL bleibt unveraendert (rueckwirkende kompatibilitaet ist gebiet der gemergten 0428-168), erlaubt ist die absicherung der NORMALISIERUNGS-GRENZE (kollisionsnachweis fail-closed ODER verlustfreie einhebung des trenners, mit goldenem test dass bestehende ids gleich bleiben); (2) der reviewer liefert die zwei signaturen des vorgaengers wörtlich: func RebookLegacySignals(r LegacyReconciliation, sources []SignalSource, registrationID string) []SignalSource und func (l LegacySource) MigrateScopedMany(project string, sourceProjects ...map[string]string) (migrated bool, err error), produktionsstelle internal/observability/migration.go:277-286, beide FREI (nicht aenderbar). einfrier-regel und remote-guard sind auftragsteil
