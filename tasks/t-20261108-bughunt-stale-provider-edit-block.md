---
id: t-20261108-bughunt-stale-provider-edit-block
card_number: "0427-150"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: baha target create --reference local + baha app init --quick completes the native acceptance bootstrap path (documented flow…
kanban_title: "0427-150 · Veraltete Instanz sperrt Edit"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1458]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md"]
---
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Provider-instanz-pruefung beim edit-refresh (veraltet = neu losen oder klar melden); regression mit state-only app im selben target in der lifecycle gruppe.

## Problem (Fund H-P3, datei-/#beleg in der Akte)
app edit kann ein need nicht aendern wenn eine unapplied state-only app existiert: veraltete provider-instance im target-registry fuehrt zu fehlerhaften referenzen. Quelle Hunt H-P3 BF-03 (blocker-kandidat).

## Acceptance
Provider-instanz-pruefung beim edit-refresh (veraltet = neu losen oder klar melden); regression mit state-only app im selben target in der lifecycle gruppe.

## Dependencies and file ownership
Keine. Write-set: target registry provider-instance refresh im edit-pfad.
