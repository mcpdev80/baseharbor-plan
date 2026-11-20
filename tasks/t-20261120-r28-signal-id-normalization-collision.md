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
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44727442216", "https://github.com/mcpdev80/baseharbor/pull/1712", "https://github.com/mcpdev80/baseharbor/commit/96f2ae11a25a508998c44a9854ef17f8fa15c112", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md"]
prs: [mcpdev80/baseharbor#1712]
created: 2026-11-20
wait_reason: ""

---

- [x] t-20261120-r28-signal-id-normalization-collision · collide project names by token fold #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/capability #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** 0428-166-  
    **PR:** [baseharbor#1712](https://github.com/mcpdev80/baseharbor/pull/1712)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44727442216), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1712), [proof 4](https://github.com/mcpdev80/baseharbor/commit/96f2ae11a25a508998c44a9854ef17f8fa15c112), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md)  
    <!-- /generated:card -->

## Accepted — 2026-11-20

PR #1712 was fixed and merged. The collision boundary now preserves an existing owner and legacy signal source, the golden test pins literal legacy IDs, and provider registration was extracted from the over-limit registry source file. Exact final PR head `a83fcc707f814e8d62db2e528d28816196f3e841` passed all required jobs, including Docker identity runtime, in run [44727442216](https://github.com/mcpdev80/baseharbor/actions/runs/44727442216). Independent final review found no blocker. PR #1712 merged at 11:33:24 UTC as `96f2ae11a25a508998c44a9854ef17f8fa15c112`.

<!-- generated:links -->
**State:** accepted  
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

korrekturrunde nach verdict BLOCKED (gueltiger grund, aber nicht ihr fehler): head 5b016319731f bewegte sich WAHREND der abnahme auf 9207a1f08931, und der neue commit ist vom owner selbst (9207a1f08 'test: pin Keycloak signal baseline IDs', author Marcel Pfingstgraef, 11:50:07+01:00, +11/-2 keycloak_signal_golden_test.go) - deshalb wurde das review abgebrochen statt entschieden. ihr inhalt ist NICHT zurueckgewiesen: P1 (guard im normalisierten raum), P3 (mutationssonden loesen verschiedene tests - die unabhaengigkeitsfrage, die mir heute die 068-korrektur eingetragen hat), P4 (golden deckt das gemergte 'keycloak:'-schema ab) und P5 (package-tests executed, nicht skipped) sind BESTAETIGT. BLOCKIEREND bleibt P2, genau das zwei-karten-risiko, das ich dem reviewer mitgegeben hatte: RegisterProviderSignals ruft RebookLegacySignals zuerst (internal/observability/registry.go:257-260) und gibt bei kollision erst danach nil,error (:269-273), und mutateChanged bricht bei callback-fehler sofort ab, bevor die geaenderte slice geschrieben wird (registry.go:752-755) - ein erfolgreiches legacy-rebook wird also verworfen, nur weil die neue registration kollidiert; das geraet in das sicherheitsverhalten der gemergten 0428-168. dazu: TestRegisterKeycloakSignalsPreservesLegacySourceForOwner (internal/identityprovider/keycloak_legacy_migration_integration_test.go:23-145, bravo/alpha :76-88) seedet keine vorhandene kollidierende registration, deckt die kombination also nicht ab. auftrag zugestellt: persistierung des rebooks VOR der rueckgabe des kollisionsfehlers mit einem lock, regression in beide richtungen, einfrieren am neuen head, akte signal-id-collision/round-2.md. nebensaechlich: der owner-commit bleibt stehen und wird in ihrer akte als fremder beitrag genannt; ihr befund zum geteilten plan-checkout (wiederherstellung aus dangling commit, 589cd630) ist angefordert
