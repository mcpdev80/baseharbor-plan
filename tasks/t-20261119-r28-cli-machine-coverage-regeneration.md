---
id: t-20261119-r28-cli-machine-coverage-regeneration
kanban_title: 0428-154 · cli coverage regeneration
card_number: "0428-154"
card_short_title: "cli coverage regeneration"
type: task
areas: [cli, docs, ci]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
blocker: ""
wait_reason: ""
depends_on: [t-20261114-r28-cli2-source-model]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
source_note: "ubertrag aus dem transfer-ersuchen der 0428-059-lane (handoff e426cb5b): der replay von eda0cd61 laeuft auf konflikte in cmd/baha/machine_coverage.go und den vier generierten CLI-index-/coverage-dokumenten. VON MIR GEMESSEN: keine lebende karte reserviert diese pfade — die karten, die sie nennen (0427-013, 0428-047, 0427-131, 0428-084, 0427-023), sind ALLE closed; der einzige offene PR, der sie anfasst, ist #1595."
evidence:
  - "https://github.com/mcpdev80/baseharbor/pull/1595"
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-r28-cli-machine-coverage-regeneration · generierte cli-index-dateien neu erzeugen #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/ci #area/cli #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1595)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Die CLI-Kette hinterlaeuft generierte dateien, die niemand bewusst pflegt: cmd/baha/machine_coverage.go und die vier dokument-ausgaben docs/cli/command-index.md, docs/de/cli/command-index.md, docs/reference/cli-machine-coverage.md, docs/de/reference/cli-machine-coverage.md. Bei jedem replay eines cli2-commits entstehen konflikte an genau diesen pfaden, weil sie das ERGEBNIS eines generators sind, nicht einer entscheidung. Ziel ist ein einziger, nachvollziehbarer regenerationsschritt auf dem aktuellen develop-stand, der die dateien aus dem code NEU erzeugt, statt konfliktseiten manuell zusammenzukleben — und eine regel, dass kein anderer PR diese dateien von hand editiert.

## Scope

- In scope: die fünf genannten dateien, NUR WERKZEUGSEITIG NEU ERZEUGT (der generator im repo, nicht manuell geschrieben). Pruefe vorher, WELCHER befehl sie erzeugt (im repository-vertrag oder in scripts/), und schreibe den befehl in die akte.
- Out of scope: jede aenderung an der REGEL, die die dateien abdeckt (.github/**, scripts/test_pr_*, scripts/pr-gate-plan.py — owner-scope), jede aenderung an cmd/baha/*.go, die den inhalt der registrierten kommandos veraendert (das ist sache der jeweiligen cli2-karte), und jeder versuch, konflikte durch manuelles zusammenkleben zweier seiten zu loesen (verbotene Praxis, §5.6 'kein blanket-pick').
- ABHANGIGKEIT gemessen: diese karte arbeitet AUF DEM STAND von 0428-059 (#1595) und ist NACH deren merge sinnvoll; laeuft sie vorher, ist das ergebnis beim naechsten cli2-commit schon wieder falsch.

## Acceptance

- Die fünf dateien entsprechen dem generator-ausgang auf dem stand nach 0428-059, belegt durch 'git status --porcelain' LEER nach einem frischen generator-lauf (also: nichts mehr zu aendern) und durch den diff gegen develop, der NUR diese fünf dateien nennt.
- Ein test ODER ein CI-job haelt fest, dass die generierten dateien nicht von hand abweichen (pruefe, ob dafuer bereits ein audit-exists — 0427-013/0428-047 haben die dateien genannt, aber closed; wenn der nachweis fehlt, ist das ein befund an mich, keine eigene .github-aenderung).
- Kein anderer offener PR der kette enthaelt eine manuelle aenderung an diesen pfaden (pruefe #1578/#1580/#1595 per dateiliste und melde jede manuelle aenderung, die du findest, statt sie zu uebernehmen).

## Required checks

- **Modified features:** bash scripts/ci-fast-check.sh; go build ./cmd/baha; der generator-befehl selbst mit leerem diff als beweis.
- **CI integration:** ein pull_request-lauf am exakten kopf bis terminal (§4.6), SKIPPED ist nicht pass (§5.4). Wenn die karte auf einer lane-* basis arbeitet, eroeffnet ci.yml :17 ('lane-*') den PR-lauf — das habe ich am develop-stand nachgelesen.
