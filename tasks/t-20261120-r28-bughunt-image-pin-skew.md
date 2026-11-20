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
owner: w172-pr0428-172-imageskew
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-image-pin-skew/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [x] t-20261120-r28-bughunt-image-pin-skew · audit image pins and version skew #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/release #area/runtime #kind/review
    <!-- generated:card -->
    **Owner:** w172-pr0428-172-imageskew  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-image-pin-skew/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w172-pr0428-172-imageskew  
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


jagd H-V15 BEFUNDLOS: alle vier prüfpfade VERHALTEN KORREKT (fail-closed, deterministischer embedded @sha256 pin, kein ungeprüfter schreibpfad). akte 11489 bytes / 99 zeilen @ 7996f22c, checkboxen null, cleanliness CLEAN. keine folge-karten. QUERBELEG FUER DAS RELEASE-BRETT: das ist der VIERTE befuendlose abschluss in folge (H-V13 install/destroy/retry, H-V14 secret reveal, H-V15 image pins, H-V16 connector handshake); nur H-V12 (keycloak signal scope) hatte funde -> karten 0428-166/167/168. die releasedesse von develop ist damit in fünf geschnitten an vier stellen sauber, und 168r2/078r2 sind genau die korrekturen aus dem einen treffer
