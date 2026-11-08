---
id: t-20261104-r27-private-integration-path
card_number: "0427-106"
card_short_title: "ein privater Prüfstapel muss"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w166, freigegeben)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: "0427-106 · ein privater Prüfstapel muss"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1379]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1379"]
---

- [x] t-20261104-r27-private-integration-path · Betrieb: ein privater Prüfstapel muss ohne geteilte Dienste auskommen #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w166, freigegeben)  
    **PR:** [baseharbor#1379](https://github.com/mcpdev80/baseharbor/pull/1379)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1379)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle4 (Lane w166, freigegeben)  
**Priority:** not set  
**PRs:** [baseharbor#1379](https://github.com/mcpdev80/baseharbor/pull/1379)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- Targeted checks for the changed area; broaden when impact is unknown.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Befund 2026-11-04 (Koordinator, plattenfest, Lane w142 + eigene Gegenmessung)
Der positive Anwendungs-Zyklus als Nachweis ist auf den Prüfrechnern derzeit NICHT herstellbar, ohne den
gemeinsamen Stapel anzufassen. Zwei harte Stellen, beide nachgemessen:
- Die Demo-Auslage verlangt ein Bild, das auf dem Rechner nicht beziehbar ist:
  baseharbor-demo compose.yaml Zeile 48 (minio/minio mit Datumsausgabe) — Rückgabewert "pull access denied,
  repository does not exist or may require docker login". Andere Bilder (Datenbank, Schlüssel-/Value-Dienst)
  sind beziehbar.
- Die Kernseiten-Auflösung zeigt für eine Arbeitslast-Anwendung auf eine GEMEINSAME Bindung (Umgebungsbinde-
  glied nach Rechnername), und es gibt keinen Profilschalter oder eigenständigen Modus, mit dem ein Prüflauf
  eine eigene Instanz bekäme. Ergebnis: Ablehnung mit Fehlerzustand, ohne dass der gemeinsame Stapel
  geschrieben wurde.

## Was diese Karte liefert
Ein dokumentierter, privater Prüfpfad: ein Weg, eine Auslieferung für Nachweise hochzufahren, der ohne
geteilte Dienste und ohne nicht-beziehbare Bilder auskommt (eigene Bindung, eigenes Netz, eigene Datenbank),
plus die Stellungnahme, ob das Vorgabebild durch ein belegbares ersetzt oder der Bezug lokal hergestellt wird.
Bis dahin ist die Kartenlage "Integration auf den Rechnern" für den positiven Nachweis nicht erfüllbar — und
der negative Nachweis (Ablehnung ohne Wirkung, Zerstörbarkeit) bleibt gültig.

## Claim 2026-11-04
- Aus dem Integrationslauf w142 entstanden und von mir auf dem Rechner nachgemessen (Bildabruf mit
  Fehlerausgabe wiederholt). Kein Auftrag an eine laufende Lane: alle fünf Sitze belegt, erste freie Bahn
  erhält diese Arbeit.

## Auftrag 2026-11-04 (aus nachgemessenem Befund)

## Kandidat pruefbar 2026-11-04 (nach dem Neu-Schnitt)
- Kopf 52be57c9893 auf work/r27-private-integration, von mir gegen die ECHTE Adresse gemessen; develop ist
  Vorfahr; die Log-Zeile origin/develop..HEAD traegt NUR deinen eigenen Commit — die anmeldungsdateien, die
  mein verjaerter Spiegel untergeschoben hatte, sind nachgewiesen raus (name-only ohne contracts/).
- Gehosteter Lauf 41913050087 auf genau diesem Kopf: abgeschlossen/erfolgreich (von der Lane beobachtet, von
  mir mit eigener gh-run-Abruf bestaetigt). Draft-PR, basis develop.

## Review-Rueckruf 2026-11-05 (r1379 REJECT, NUR das gate)
Inhalt (Umschaltung + beide Gegenproben) bestanden. Der Lauf am exakten Kopf uebersprang den Job 'Selected
Checks' — vermutlich draft-schalter. Kleinauftrag: PR auf ready, neuen Lauf terminal beobachten, beide
Modus-Zellen am lauf belegen; bleibt der skip: Befund mit Workflow-zeile an den Owner, keine Gewalt.

## Gate-Nachweis geliefert — wieder pruefbar (kopf unveraendert 52be57c9893)
PR ist auf ready gestellt, der ausgewiesene Pflichtlauf 'PR Selected Checks' ist am exakten Kopf terminal
ERFOLGREICH (lauf 41978410480, von mir abgerufen; beide Modus-Zellen in der Akte belegt). Der einzige
Ablehnungspunkt der Prüfung (uebersprungener Gate-Job) ist damit ausgeraeumt — Inhalt war schon vorher
bestanden. Merge-obliegt der Owner-Runde.

## ACCEPT 2026-11-05 (r1379b, Gate-Punkt geschlossen)
Kopf unveraendert 52be57c9893; 'PR Selected Checks' terminal erfolgreich + die zwei modus-zellen belegt —
der einzige ablehnungspunkt der runde 1379 ist ausgeraeumt. MERGE-REIF fuer die Owner-Runde.


## Owner-Abschluss 2026-11-05

- PR [#1379](https://github.com/mcpdev80/baseharbor/pull/1379) nach `develop` gemerged, Squash-Commit `a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3`.
- Pflicht-CI [Run 41978410480](https://github.com/mcpdev80/baseharbor/actions/runs/41978410480) auf dem vor Merge verifizierten PR-Head abgeschlossen: `success`, einschließlich `PR Selected Checks`.
- Historische Review-Rückrufe und Korrekturen bleiben als Nachweis erhalten. Fachliche Abnahme gemäß letzter ACCEPT-Bewertung; separate Release-/Cross-Repo-Qualifizierung dadurch nicht vorweggenommen.
