---
id: t-20261120-post-merge-acceptance-audit-40cb28c
card_number: "0428-197"
card_short_title: post-merge acceptance audit
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: w197-0428-197-postmerge
kanban_status: closed
kanban_lane: closed
kanban_summary: "Reine Befundung (kein Produktwechsel): Abnahme des ERGEBNISSES von fuenf heutigen develop-Merges - hat jede Akzeptanzzeile eine…"
kanban_title: 0428-197 · post-merge acceptance audit
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/post-merge-40cb28c/round-1.md"]
---

- [x] t-20261120-post-merge-acceptance-audit-40cb28c · post-merge acceptance audit #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w197-0428-197-postmerge  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/post-merge-40cb28c/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w197-0428-197-postmerge  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reine Befundung (kein Produktwechsel): Abnahme des ERGEBNISSES von fuenf heutigen develop-Merges - hat jede Akzeptanzzeile eine Stelle im Code und einen Nachlauf? Dieselbe Abnahme hat die Karte 0428-179 erzeugt (post-merge-Befund B2 auf develop 96f2ae11); diese Lane fuehrt sie fuer den heutigen Stand.

## Object of audit (nur CLOSED/merged = develop-Stand)

- #1715 (0428-184), #1716 (0428-182), #1717 (0428-188), #1721 (CI planner base), #1722 (CI serviceaccess routing).
- develop-Anker 40cb28c mit den Vorgaengern 2f81fa2, b98299d2, 63de95e.

## Slices

1. Je Merge: Akzeptanzzeile der Karte, Fundstelle im diff (datei:zeile), ein Gegentest oder echter Aufruf, Verdict ERFUELLET / TEILWEISE / NICHT ERFUELLET.
2. Auswirkung der neuen CI-Auswahlregeln (#1721, #1722) auf die im Feld liegenden PRs #1714, #1718, #1684, #1645 - streckt eine Regel eine Strecke ganz heraus, ist das ein Fund.
3. Querschnitt: ob die Akzeptanztexte selbst noch zum diff passen (formulierte eine Karte etwas anderes als das, was gemergt wurde).

## Rules

- Keine Produktaenderung, kein Testwechsel, kein `.github/**`, kein PR, kein Board-Wechsel durch die Lane.
- Jeder Fund traegt eine Zeile `FUND-FUER-KARTE: <kurztitel> | <datei:zeile> | <schadensbild>`; Karten legt der
  Coordinator an (§3.3.5 Fund-zu-Karte-Pflicht).
- Doppelungsausschluss: H-V18 (0428-146), H-V19 (0428-147), H-V20 (0428-195, befundlos), H-V17-Funde
  (0428-189..194). Nur ANDERE Stellen melden, mit Zusatz 'wie 0428-1xx, andere Stelle'.

## Evidence

- Akte: `evidence/r28-welle4-2026-11-20/post-merge-40cb28c/round-1.md` auf baseharbor-plan main.

## Stop criteria

- Fund ohne `FUND-FUER-KARTE`-Zeile, Akte ohne `cleanliness`-Zeile, oder ein Versuch, Produktcode zu aendern.
- Ausloeser fuer sofortige Stop-with-Meldefrist: eine dep-freie, konfliktfreie Produktkarte wird frei (§3.3.5).

ARBEITET JETZT, kante gegen session gemessen (b5342068, laptop): POST-MERGE-ABNAHME der fuenf heutigen merges (#1715/184, #1716/182, #1717/188, #1721 ci-planner, #1722 ci-routing) auf develop 40cb28c: pro merge akzeptanzzeile -> fundstelle im diff (datei:zeile) -> eigener gegentest oder echter aufruf -> verdict ERFUELLET/TEILWEISE/NICHT. zusatz: treffen die zwei neuen CI-auswahlregeln #1714/#1718/#1684/#1645 noch richtig (eine strecke, die durch die regel ganz herausfaellt, ist ein fund). derselbe abnahme-typ, der heute 0428-179 erzeugt hat (befund B2 auf 96f2ae11).

ABGESCHLOSSEN, befundlos mit zeugen: alle fuenf heutigen merges (1715/184, 1716/182, 1717/188, 1721 ci-planner, 1722 ci-routing) ERFUELLET - akzeptanzzeile -> fundstelle im diff -> gegentest; und der satz, der mir weiterhilft: die neuen CI-auswahlregeln schliessen #1714/#1718/#1684/#1645 NICHT aus. die zwei failures an #1684/#1645 sind damit echtfallender code, kein routing-opfer - beide lanes kriegen das als eine zeile. akte evidence/r28-welle4-2026-11-20/post-merge-40cb28c/round-1.md (86 zeilen, 0 checkboxen, 5 verdict-zeilen, cleanliness-zeile). keine neuen karten, weil es nichts zu giessen gab.
