---
id: t-20261120-bughunt-shipped-surface-desk
card_number: "0428-196"
card_short_title: hunt shipped-surface desk
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: w196-0428-196-huntswt
kanban_status: active
kanban_lane: active
kanban_summary: "Reine Befundung (kein Produktwechsel): was die seit dieser Woche geschlossenen Karten an der ausgelieferten Oberflaeche (baha)…"
kanban_title: 0428-196 · hunt shipped-surface desk
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-bughunt-shipped-surface-desk · hunt shipped-surface desk #task #release/v0-4-28 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w196-0428-196-huntswt  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w196-0428-196-huntswt  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reine Befundung (kein Produktwechsel): was die seit dieser Woche geschlossenen Karten an der ausgelieferten Oberflaeche (`baha`) wirklich zeigen - Kommandoabdeckung, Fehlermeldungen und Verhalten gegenueber einem Zustand einer aelteren ausgelieferten Version. Ausloeser: drei Desk-Rotationen (H-V18/19/20) sind am selben Tag befundlos geblieben, das Muster-Jagen hat kein weiteres Feld; hier wird die Verhaltensseite geprueft.

## Object of audit (nur CLOSED/merged = develop-Stand)

- develop 40cb28c (Spitze zum Schnittzeitpunkt), gebaut aus source, nicht aus einem image-fremden Stand.
- Karten dieser Woche, deren Akzeptanz eine Oberflaechenwirkung behauptet (0428-182, 0428-184, 0428-188, 0428-068).

## Slices

1. Kommando-Flaeche: `baha --help` und die help-Ausgaben der Unterschen gegen die Kartenbehauptungen; Enden an Stellen, die nichts tun; dokumentierte aber ignorierte Flags.
2. Melde-text-vertrag: ein echter Aufruf pro today-Merge in den Fehlerpfad - fuehrt die Meldung zur richtigen Handlung oder verdeckt sie den Grund.
3. Upgrade von aussen: ausgeliefertes binary auf einem Zustand einer aelteren ausgelieferten Version - migrieren, verwerfen oder fail-closed, mit den Dateien, die gelesen wurden.

## Rules

- Keine Produktaenderung, kein Testwechsel, kein `.github/**`, kein PR, kein Board-Wechsel durch die Lane.
- Jeder Fund traegt eine Zeile `FUND-FUER-KARTE: <kurztitel> | <datei:zeile> | <schadensbild>`; Karten legt der
  Coordinator an (§3.3.5 Fund-zu-Karte-Pflicht).
- Doppelungsausschluss: H-V18 (0428-146), H-V19 (0428-147), H-V20 (0428-195, befundlos), H-V17-Funde
  (0428-189..194). Nur ANDERE Stellen melden, mit Zusatz 'wie 0428-1xx, andere Stelle'.

## Evidence

- Akte: `evidence/r28-welle4-2026-11-20/bughunt-hv21-shipped-surface/round-1.md` auf baseharbor-plan main.

## Stop criteria

- Fund ohne `FUND-FUER-KARTE`-Zeile, Akte ohne `cleanliness`-Zeile, oder ein Versuch, Produktcode zu aendern.
- Ausloeser fuer sofortige Stop-with-Meldefrist: eine dep-freie, konfliktfreie Produktkarte wird frei (§3.3.5).

ARBEITET JETZT, kante gegen session gemessen (02aab8d1, ornith, develop-Anker 40cb28c): Hunt-Schnitt H-V21 'ausgelieferte-oberflaechen-desk' - (1) command-abdeckung der heutigen Karten gegen 'baha --help' und die help-Ausgaben der unterschen, (2) Fehler-meldungen auf echten fehlerpfaden (0428-188 grants, 0428-182 unsupported, 0428-184 shared destroy, 0428-068 per-terminal context), (3) verhalten des ausgelieferten binary auf einem zustand einer AELTEREN ausgelieferten version. reine befundung; FUND-FUER-KARTE-zeile pro fund; doppelungsausschluss gegen H-V18/19/20 und 0428-189..194. fuellt den nach H-V20 freigewordenen ornith-sitz (scan: konfliktfreie produktkarten = 0).
