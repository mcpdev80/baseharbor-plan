---
id: t-20261120-r28-bughunt-image-pin-skew
kanban_title: 0428-172 · hunt image pin skew
card_number: "0428-172"
card_short_title: "hunt image pin skew"
type: review
areas: [runtime, release]
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
---

- [ ] t-20261120-r28-bughunt-image-pin-skew · audit image pins and version skew #task #release/v0-4-28 #status/planned #view/ready #area/release #area/runtime #kind/review
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

Bug-Hunt H-V15. Prüfschnitt: Welche Bild-Referenzen schreibt BaseHarbor, und was passiert
bei Versionsschiebung (neuer Core, altes Pin; altes Pin, geänderter Registry-Pfad)?

## Anker (develop)

- `internal/deployment/config_mutation.go` und `internal/deployment/target.go`
- `internal/runtime/project.go` (projectToken / Projekt-Normalisierung)
- die Pin-Prüfung in den Workflows (nur lesen; `.github/**` ist owner-scope)

## Schnitte

1. Wo entsteht ein image-pin, und ist er deterministisch reproduzierbar?
2. Was passiert, wenn das Pin auf develop und das Pin im zustand eines bestands-carren
   auseinanderlaufen — fail-closed, stille Übernahme, oder gemischter Lauf?
3. Verliert ein Destroy/Retry zyklus das Pin, und wenn ja, woher kommt es dann neu?
4. Gibt es einen Pfad, der ein Pin ohne Prüfung überschreibt?

## Regel

Reine Befundung: KEINE Produktänderung, KEIN commit, KEIN PR, KEIN merge. Akte mit
`file:line` je Aussage, `git ls-remote origin refs/heads/develop` in der Akte,
`cleanliness:`-Zeile mit Vorher/Nachher-Liste (container/networks/volumes/state dirs).
Nichts gefunden = 'VERHALTEN KORREKT' + Prüfweg. Kartenlose Funde sind verlorene Arbeit —
die Akte nennt für jeden Fund `DATEI:ZEILE`, `ERWARTET (Vertrag)`, `IST (gemessen)`;
Karten gieße ich.

