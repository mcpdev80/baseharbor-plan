---
id: t-20261108-bughunt-destroy-data-root-residual
card_number: "0427-152"
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
kanban_title: "0427-152 · Destroy-Ziel aus Datenwurzel"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1458]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/act-1455-fate.md"]
---
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Destroy loest eigene Core-ziele aus der datenwurzel (kein wegwerfen fremder ziele, fail-closed nach 127-doktrin); die zwei commits als grundlage nutzen oder bewusst neu schneiden mit begruendung; regression destroy+core im lifecycle-feld.

## Problem (Fund act-1455-fate, datei-/#beleg in der Akte)
Die destroy-änderung aus PR #1455 (owned Core targets aus data root loesen) ist in KEINER ancestry von develop oder #1457 gelandet — gutachten bestaetigt rest-posten a2761413+9a963000. #1455 wird geschlossen, der inhalt bekommt diesen vertrag. Quelle: act-1455-fate.md.

## Acceptance
Destroy loest eigene Core-ziele aus der datenwurzel (kein wegwerfen fremder ziele, fail-closed nach 127-doktrin); die zwei commits als grundlage nutzen oder bewusst neu schneiden mit begruendung; regression destroy+core im lifecycle-feld.

## Dependencies and file ownership
Keine. Write-set: internal destroy + data-root resolution.
