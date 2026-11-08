---
id: t-20261108-bughunt-0427-multitarget-ambiguity
card_number: "0427-126"
card_short_title: "multi-target without choice"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.
kanban_title: "0427-126 · multi-target without choice"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1441]
sources: []
blocker: ""
wait_reason: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/f7a49e681"]
resolution: accepted
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

- [x] t-20261108-bughunt-0427-multitarget-ambiguity · 0427-126 · init-status-doctor bei mehreren Targets #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/dx #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1441](https://github.com/mcpdev80/baseharbor/pull/1441)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/f7a49e681)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1441](https://github.com/mcpdev80/baseharbor/pull/1441)  
**Source:** 
<!-- /generated:links -->

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-2 podman2 hunt: brownfield repo; error text verbatim in the act; commands give no --target selection hint.

## Acceptance

the three commands either apply to all targets consistently or present an explicit selectable list with a deterministic default; error text names the remedy.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.

## 2026-11-08 Übernahme (ChatGPT)

- Owner: `owner:chatgpt`; Lane: `active`.
- Arbeitsauftrag: kleiner, gezielter Produktfix inklusive Regression und verpflichtender PR-CI. Keine gleichzeitigen Änderungen an fremden Karten.
- Noch kein Produkt-Commit und kein PASS/Abschluss behauptet; Nachweis/PR werden nach tatsächlicher Umsetzung ergänzt.

## 2026-11-08 Produktarbeit (ChatGPT)

- [PR #1441](https://github.com/mcpdev80/baseharbor/pull/1441), Head `42f50099e5267dd31093b959828fbd3e21136a65`: bei mehreren konfigurierten Targets nennt die Fehlermeldung jetzt alphabetisch alle auswaehlbaren Namen sowie die konkrete Auswahl ueber `baha target activate NAME` oder `BASEHARBOR_TARGET=NAME`.
- Keine implizite Target-Auswahl (Fail-Closed bleibt); neuer Typed-Error-Regressionstest. PR-CI noch offen, Karte `active`.

## 2026-11-08 Abnahme (ChatGPT)

- [PR #1441](https://github.com/mcpdev80/baseharbor/pull/1441) **gemergt nach develop**: `f7a49e6818efb269cc928ad550038b2bf94d333b`; gepruefter Head `42f50099e5267dd31093b959828fbd3e21136a65`.
- [CI #42429449162](https://github.com/mcpdev80/baseharbor/actions/runs/42429449162) terminal `success`, alle Jobs erfolgreich, keine Fehler; native cross-repo VM-Journey war nicht Teil dieser kleinen Bug-Abnahme.
- **Status `closed` / accepted:** gezielter Produktfix und Regression integriert.

## 2026-11-08 Owner-Freigabe und Uebergabe

- Bearbeitungs-Owner gewechselt von `"owner:chatgpt"` auf `unassigned`. Bereits akzeptierte Karte bleibt `closed`.
- Fixed/accepted #1441.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.
