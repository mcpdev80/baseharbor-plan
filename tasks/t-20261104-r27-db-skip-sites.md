---
id: t-20261104-r27-db-skip-sites
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w137)
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: "Tests: fehlende Prüfumgebung bleibt in fünf Stellen ein Überspringen"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-db-skip-sites · Tests: fehlende Prüfumgebung bleibt in fünf Stellen ein Überspringen #task #release/v0-4-27 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w137)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Owner:** coord-welle4 (Lane w137)  
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

## Zweck (Koordinator, 2026-11-04)
Die verbundene Hebelkarte t-20261022-r27-ci-delivery hat genau die beiden Datenbankprüfungen umgestellt, die
in den offenen Anträgen rot waren. Auf der Hauptlinie bleiben weitere Stellen, die ohne gesetzte
Verbindung überspringen statt fehlzuschlagen — plattenfest fünf Dateien:
- cmd/baha/bugs_864_871_runtime_test.go
- internal/controlplaneruntime/server_integration_test.go
- internal/database/connector_enrollment_integration_test.go
- internal/database/migration_rollback_integration_test.go
- internal/database/schema_readiness_integration_test.go

## Abgrenzung
Nicht Produktcode, nicht Workflow. Eigene Prüfumgebungs-Annahme: Ohne Verbindung MUSS ein Fehlschlag mit
klarer Meldung stehen, damit ein Lauf nicht scheingrün wird. Wo ein Überspringen fachlich richtig ist
(z. B. optionaler Treiber), bleibt es ausdrücklich mit Begründung im Code, nicht im stillen Schweigen.

## Akzeptanz
1. Jede der fünf Stellen: ohne Verbindung rot mit klarer Meldung, mit Verbindung grün und ausgeführt.
2. Gegenprobe mit absichtlich falschem Ziel: rot (Beweis, dass wirklich geprüft wird).
3. Keine Überspringung bleibt ohne schriftliche Begründung im Code.
4. Prüfprotokoll der gehosteten Läufe bis zum endgültigen Zustand in der Nachweissammlung.

## Claim 2026-11-04
- Auftrag: die fünf verbliebenen Stellen, die ohne Verbindungsangabe überspringen statt fehlzuschlagen,
  auf echtes Fehlschlagen mit klarer Meldung umstellen; wo Überspringen fachlich richtig ist, bleibt es mit
  Begründung im Code. Gegenprobe je Stelle mit unerreichbarem Ziel muss rot bleiben.
