---
id: t-20261104-r27-db-skip-sites
card_number: "0427-103"
card_short_title: "four database Integr tests"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w152)
kanban_status: closed
kanban_lane: closed
kanban_summary: The four database-connected integration tests fail with a clear setup error when the test database URL is absent and execute…
kanban_title: "0427-103 · four database Integr tests"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1378]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1378", "https://github.com/mcpdev80/baseharbor/commit/512dcd721ac3fb739bfd4cb0b990fd68d6794762", "https://github.com/mcpdev80/baseharbor/actions/runs/41922518146", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/db-skip-sites/review-1378c.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/db-skip-sites/neutral-1.md"]
---

- [x] t-20261104-r27-db-skip-sites · Tests: four database integration tests fail closed without the test URL #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w152)  
    **PR:** [baseharbor#1378](https://github.com/mcpdev80/baseharbor/pull/1378)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1378), [proof 2](https://github.com/mcpdev80/baseharbor/commit/512dcd721ac3fb739bfd4cb0b990fd68d6794762), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/41922518146), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/db-skip-sites/review-1378c.md), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/db-skip-sites/neutral-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Owner:** coord-welle4 (Lane w152)  
**Priority:** not set  
**PRs:** [baseharbor#1378](https://github.com/mcpdev80/baseharbor/pull/1378)  
**Source:** 
<!-- /generated:links -->

## Goal

The four database-connected integration tests fail with a clear setup error when the test database URL is absent and execute successfully against an isolated PostgreSQL fixture when it is provided.

## Scope

- In scope: fail-closed test-environment checks in the four database-test files listed in the merged PR.
- Out of scope: product-code and workflow changes.

## Acceptance

- The four affected tests fail with a clear error when the database URL is absent; they pass and execute with the isolated fixture.
- PR Selected Checks is terminal-success on the exact reviewed head.
- The change is limited to the four database-test files; no workflow or `AGENTS.md` changes.

## Required checks

- Missing-URL negative cell: all four tests fail closed, exit 1.
- Isolated PostgreSQL positive cell: all four tests pass, exit 0.
- GitHub Actions run 41922518146: terminal success on `760c104a6c499dc2baf6c30ad002bb6141bb7d83`.

## Dependencies and file ownership

- Owned files: `internal/controlplaneruntime/server_integration_test.go`, `internal/database/connector_enrollment_integration_test.go`, `internal/database/migration_rollback_integration_test.go`, and `internal/database/schema_readiness_integration_test.go`.
- Shared files: none.

## Handoff

- Merged into `develop` from PR [#1378](https://github.com/mcpdev80/baseharbor/pull/1378) at [512dcd721ac3fb739bfd4cb0b990fd68d6794762](https://github.com/mcpdev80/baseharbor/commit/512dcd721ac3fb739bfd4cb0b990fd68d6794762). Reviewed head: `760c104a6c499dc2baf6c30ad002bb6141bb7d83`; terminal checks: [run 41922518146](https://github.com/mcpdev80/baseharbor/actions/runs/41922518146). Review and independent cell evidence: [review-1378c](../evidence/r27-welle4-2026-11-04/db-skip-sites/review-1378c.md), [neutral-1](../evidence/r27-welle4-2026-11-04/db-skip-sites/neutral-1.md).

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

## Earlier handoff (superseded by the merged closeout below)
- Kandidat: PR #1378, Zweig work/r27-db-skip-sites, Kopf aca8ff97df8 (ls-remote == Kopf), develop 2ea2c6f1 ist
  Vorfahr; Prüfprotokoll: acht grün, null rot, elf nach Auswahlregel übersprungen; Antrag ist verbindbar.
- Vier echte Stellen umgestellt (Steuerungsschicht, Anmeldungs-Datenbank, Rückbau, Bereitstellungsprüfung):
  ohne gesetzte Verbindung jetzt Fehlschlag mit klarer Meldung, keine Überspringung mehr in diesen Dateien.
- BERICHTIGUNG MEINER EIGENEN LISTE: die fünfte Datei (cmd/baha/bugs_864_871_runtime_test.go:132) war ein
  Suchtreffersyndling — sie prüft Textinhalte, sie überspringt nicht. Die Lane hat das dokumentiert statt
  dort still etwas zu ändern; richtig so.
- Gegenproben mit unerreichbarem Ziel sind für alle vier Stellen rot belegt.

## Temporary blocker after review-1378b (resolved)
Die damalige Abnahme war wegen der belegten Port-5433-Bindung blockiert. Die neutrale Gegenprobe auf Port 55000 und der terminal erfolgreiche Lauf 41922518146 hoben diesen Blocker auf; siehe review-1378c und neutral-1.
