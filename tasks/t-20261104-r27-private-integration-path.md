---
id: t-20261104-r27-private-integration-path
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w144)
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: "Betrieb: ein privater Prüfstapel muss ohne geteilte Dienste auskommen"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-private-integration-path · Betrieb: ein privater Prüfstapel muss ohne geteilte Dienste auskommen #task #release/v0-4-27 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w144)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle4 (Lane w144)  
**Priority:** not set  
**PRs:** none  
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
