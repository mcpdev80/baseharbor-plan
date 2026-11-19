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
owner: "w154-pr0428-154-covcheck (codeman dbec9d13, ornith:2)"
kanban_status: active
kanban_lane: active
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

- [ ] t-20261119-r28-cli-machine-coverage-regeneration · generierte cli-index-dateien neu erzeugen #task #release/v0-4-28 #status/active #view/active #area/ci #area/cli #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** w154-pr0428-154-covcheck (codeman dbec9d13, ornith:2)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1595)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-source-model](t-20261114-r28-cli2-source-model.md)  
**Owner:** w154-pr0428-154-covcheck (codeman dbec9d13, ornith:2)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Die CLI-Doku-Kette hinterlaeuft VIER generierte markdown-dateien, die niemand bewusst pflegt: docs/cli/command-index.md, docs/de/cli/command-index.md, docs/reference/cli-machine-coverage.md, docs/de/reference/cli-machine-coverage.md. Bei jedem replay eines cli2-commits entstehen konflikte an genau diesen pfaden, weil sie das ERGEBNIS von tests sind, nicht einer entscheidung. Ziel ist ein einziger, nachvollziehbarer regenerationsschritt auf dem stand nach 0428-059, der die dateien aus dem code NEU erzeugt, statt konfliktseiten manuell zusammenzukleben.

PRÄMISSE-KORREKTUR (quelle-inspektion der 0428-059-lane, VON MIR AM develop 4b3a3559 NACHGEMESSEN, queue667): cmd/baha/machine_coverage.go ist KEIN generator-output, sondern die HANDSCHRIFTLICHE classifications-registrierung — 'var cliPresentationCommands = map[string]string' (machine_coverage.go:133), gelesen in :88. Die registry-eintraege fuer die neuen source-/component-/path-kommandos GEHOEREN zum feature-patch von 0428-059 und bleiben dort. Nur die vier markdown-dateien sind generiert; wer sie schreibt, ist gemessen: cmd/baha/human_documentation_test.go:101 (docPath cli/command-index.md, koepfe :78 DE / :80 EN) und cmd/baha/machine_documentation_test.go:57 (checkGeneratedDocumentation fuer cli-machine-coverage.md). Diese karte war mit FUENF dateien angelegt — ein pauschal-fuenf-file-verfahren waere falsch und ist berichtigt.

## Scope

- In scope: GENAU die vier markdown-dateien docs/cli/command-index.md, docs/de/cli/command-index.md, docs/reference/cli-machine-coverage.md, docs/de/reference/cli-machine-coverage.md — und NUR WERKZEUGSEITIG neu erzeugt (ueber die beiden tests oben, nicht mit dem text editor). Nenne den befehl in der akte.
- Out of scope: cmd/baha/machine_coverage.go (handschriftliche registrierung, gehort zu 0428-059, gemessen :133/:88); jede aenderung an .github/**, scripts/pr-gate-plan.py, scripts/test_pr_* (owner-scope; pr-gate-plan.py nennt die vier dateien nur als audit-pfade); jede aenderung an cmd/baha/*.go, die den inhalt der kommandos veraendert; und das manuelle zusammenkleben zweier konfliktseiten (verbotene praxis, §5.6).
- ABHANGIGKEIT gemessen: arbeitet AUF DEM STAND von 0428-059 (#1595) und ist NACH deren merge sinnvoll; vorher ist das ergebnis beim naechsten cli2-commit wieder falsch.

## Acceptance

- Die vier dateien entsprechen dem generator-ausgang auf dem stand nach 0428-059: 'git status --porcelain' ist nach einem frischen generator-lauf LEER fuer diese vier pfade (nichts mehr zu aendern), und der diff gegen develop nennt NUR diese vier dateien — KEINEN treffer in cmd/baha/machine_coverage.go.
- Ein nachweis, dass die vier dateien nicht von hand abweichen, ist VORHANDEN oder fehlt ausdruecklich: pruefe, ob documentation-audit/mkDocs-gates sie treffen (scripts/pr-gate-plan.py nennt alle vier, gemessen) und ob ein lauf sie am PR-head prueft; fehlt der nachweis, ist das ein befund an mich, keine eigene .github-aenderung.
- Kein anderer offener PR der kette enthaelt eine MANUELLE änderung an den vier markdown-pfaden (pruefe #1578/#1580/#1595 per dateiliste; die registry-anteile in machine_coverage.go sind ERWARTET und gehoeren in 059, nicht hierher).

## Required checks

- **Modified features:** bash scripts/ci-fast-check.sh; go build ./cmd/baha; der generator-befehl selbst mit leerem diff als beweis.
- **CI integration:** ein pull_request-lauf am exakten kopf bis terminal (§4.6), SKIPPED ist nicht pass (§5.4). Wenn die karte auf einer lane-* basis arbeitet, eroeffnet ci.yml :17 ('lane-*') den PR-lauf — das habe ich am develop-stand nachgelesen.
