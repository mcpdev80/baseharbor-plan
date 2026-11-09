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

## 2026-11-08 Takeover (ChatGPT)

- Owner: `owner:chatgpt`; Lane: `active`.
- Work order: a small, targeted product fix including regression and a mandatory PR CI. No simultaneous changes to other cards.
- No product commit and no PASS/completion claimed yet; evidence/PR added after actual implementation.

## 2026-11-08 Product Work (ChatGPT)

- [PR #1441](https://github.com/mcpdev80/baseharbor/pull/1441), head `42f50099e5267dd31093b959828fbd3e21136a65`: with multiple configured targets, the error message now lists alphabetically all selectable names as well as the concrete selection via `baha target activate NAME` or `BASEHARBOR_TARGET=NAME`.
- No implicit target selection (fail-closed remains); new typed-error regression test. PR CI still open, card `active`.

## 2026-11-08 Acceptance (ChatGPT)

- [PR #1441](https://github.com/mcpdev80/baseharbor/pull/1441) **merged to develop**: `f7a49e6818efb269cc928ad550038b2bf94d333b`; checked head `42f50099e5267dd31093b959828fbd3e21136a65`.
- [CI #42429449162](https://github.com/mcpdev80/baseharbor/actions/runs/42429449162) terminal `success`, all jobs successful, no errors; native cross-repo VM journey was not part of this small bug acceptance.
- **Status `closed` / accepted:** targeted product fix and regression integrated.

## 2026-11-08 Owner Release and Handover

- Processing owner changed from `"owner:chatgpt"` to `unassigned`. An already accepted card stays `closed`.
- Fixed/accepted #1441.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.
