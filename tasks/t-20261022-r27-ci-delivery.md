---
id: t-20261022-r27-ci-delivery
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: coord-welle4 (Lane w128)
kanban_lane: review
kanban_summary: ""
kanban_status: review
kanban_title: "Deferred trusted CI readiness: delivery"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-contract, t-20261103-ci-plain-checks]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1377]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-ci-delivery · Deferred trusted CI readiness: delivery #task #release/v0-4-27 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w128) · **Priority:** critical  
    **PR:** [baseharbor#1377](https://github.com/mcpdev80/baseharbor/pull/1377)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md)  
**Required by:** [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md), [t-20261018-r27-ci-consumption](t-20261018-r27-ci-consumption.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-image-transfer](t-20261018-r27-image-transfer.md), [t-20261018-r27-local-registry](t-20261018-r27-local-registry.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md)  
**Owner:** coord-welle4 (Lane w128)  
**Priority:** critical  
**PRs:** [baseharbor#1377](https://github.com/mcpdev80/baseharbor/pull/1377)  
**Source:** 
<!-- /generated:links -->

# Deferred trusted CI readiness: delivery

## Observable outcome and preconditions
Qualify only missing domain-specific trusted selection, execution and verification for accepted product interfaces. Wait for the accepted normal CI baseline and this card's product/startup dependencies; do not expand gates to keep workers busy during the current repair.

## Covered slices
- delivery-boundary
- candidate-contract
- candidate-pack
- registry-access
- image-transfer
- local-registry
- artifact-resolution
- stage-versions
- version-view
- delegated-handoff
- promote

## Parallel work split when assignable
W1: existing trusted domain mapping and actual test discovery; W2: bounded producer/executor and domain-local fixture; W3: normal required-job result handling and relevant negatives. Coordinator reserves exact files from the actual accepted product interface before assigning writes. Shared central files have one writer; Use a flexible shared worker pool; coordinator reserves non-overlapping files and runner capacity. Independent ready domains may be prepared in disjoint files without a blanket ci-lanes lock.

## Acceptance and exclusions
Actual selected checks execute and fail on missing/invalid required coverage; source/integration/ref and runner isolation stay authenticated. Record available accepted check identity for dependent product slices. Execute the affected checks directly; no full matrix, wildcard allowlist, self-reported green, unqualified new lane or duplicate authority. Run only targeted native checks justified by the actual scope and available isolated runners.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman is resumed by the Owner; the coordinator preserves claims and unpublished work and assigns small non-overlapping iterations under the current order. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261022-r27-ci-delivery.md) remain immutable history, not competing operational instructions.

## Owner update 2026-10-29

Separate current CI baseline readiness from later tests of product interfaces that do not yet exist. Coordinator records the real dependency graph and coverage mapping; no fabricated readiness or blanket product development before the new CI cutover. Assign only bounded independent slices with exclusive files.

## Current CI contract — 2026-11-03

The Owner retires the evidence and receipt approval chain. This task supplies only the missing ordinary test selection/execution for its domain. Job results flow through normal dependencies; no gate manifests, archived-run verification or evidence reuse. The only CI receipt is merge SHA plus PR number. The replacement baseline task remains open until its actual checks pass.

## Vorbehalt 2026-11-04 (Owner-Maßnahme)
- Diese Readiness-Karte ist der Hebel für zwölf nachfolgende Aufgaben und läuft parallel zu den PR-Korrekturen;
  sie wartet nicht auf die übrigen offenen CI-Läufe.
- Dazu wird die gemeinsame Go-/Docker-/Datenbank-Testursache als eigenständiges Arbeitspaket abgegrenzt:
  Ursache, betroffene Gates, Minimalbeispiel und die saubere Trennung von Produktfehler gegen Umgebungsfehler.

## Handoff 2026-11-04 (Lane w128, Korrekturrunde nach Provenanz-Befund)
- Kandidat: PR #1377, Zweig work/r27-ci-delivery-dsn, Kopf 029e3ddd522, develop ecbb8854 ist Vorfahr.
- Geänderte Dateien exakt zwei Integrationstests (internal/database/identity_tenant_resolver_integration_test.go,
  internal/database/tenant_integration_test.go): sie lesen die Verbindung jetzt aus BASEHARBOR_TEST_DATABASE_URL
  statt einer fest kodierten Adresse; ohne gesetzte Variable gibt es einen klaren Hinweis auf die fehlende
  Testumgebung statt eines stillen Verbindungverweigerungsfehlers.
- Mutationsgegenprobe belegt: absichtlich falscher Port im Wert => Prüfung bleibt ROT.
- Der erste Versuch (PR #1376) war aus dem Anmelungskandidaten geschnitten (26 Dateien, fremdes Schreibgut);
  er ist mit Beleg geschlossen und der Zweig gelöscht — die Trennung ist damit sauber.
- Klassifikation über die offenen Kandidaten: 0 Produktfehler, 5 Umgebung, 2 Reihenfolge/Basis in dieser Familie.
