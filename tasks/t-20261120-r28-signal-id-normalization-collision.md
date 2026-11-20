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
kanban_status: review
kanban_lane: review
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md"]
prs: [mcpdev80/baseharbor#1712]
created: 2026-11-20
wait_reason: ""

---

- [ ] t-20261120-r28-signal-id-normalization-collision · collide project names by token fold #task #release/v0-4-28 #status/review #view/review #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** 0428-166-  
    **PR:** [baseharbor#1712](https://github.com/mcpdev80/baseharbor/pull/1712)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-keycloak-signal-id-migration-gap](t-20261120-r28-keycloak-signal-id-migration-gap.md)  
**Owner:** 0428-166-  
**Priority:** not set  
**PRs:** [baseharbor#1712](https://github.com/mcpdev80/baseharbor/pull/1712)  
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

abnahme bestellt, alle vier punkte gemessen: (1) head 5b016319731f eingefroren, branch = refs/pull/1712/head, EIN eigener commit, draft=false, mergeable=clean, 3 dateien; (2) base = develop-spitze dbe7fbc3905b, merge-base --is-ancestor = JA (zusaetzlich ist 681700ca ahne: die lane hat NICHT gerebasht, ihr branch ist linear - ihre akte attestiert 681700ca als basis, das erklaert die zeitreihendifferenz ohne widerspruch); (3) run 44719507275 completed/success am exakten head; (4) akte signal-id-collision/round-1.md auf main @ 589cd630 mit PLAN, remote witnesses, mutationsbeweisen BEIDER richtungen und '## repo-rule compliance'. gewaehlte bauart: form (a) kollisionsichere fail-closed-guard in RegisterProviderSignals statt verlustfreier ableitung - begruendet in der akte, und genau die richtung, die ihr vorgaenger 0428-168 (gemergt) offen liess. TWO-PUNCH-RISIKO, das ich dem reviewer ausdruecklich aufgegeben habe: die aenderung sitzt in internal/observability/registry.go, also in der datei, ueber die 0428-168 die legacy-umschreibung per RebookLegacySignals innerhalb derselben mutation betreibt - der fail-closed-pfad darf ein bereits registriertes legacy-signal NICHT abbrechen, sonst macht diese karte ein gemergtes sicherheitsverhalten kaputt. dazu: reihenfolge (umschreibung vor der neuen guard?) und ob keycloak_legacy_migration_test.go die kombination abdeckt. zweite nachfrage aus der 068-erfahrung: ob ihre zwei mutationssonden VERSCHIEDENE tests ausloesen
