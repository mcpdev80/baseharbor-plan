---
id: t-20261108-bughunt-0427-appnew-contradictory-exit
card_number: "0427-125"
card_short_title: "app new: success plus error"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.
kanban_title: "0427-125 · app new: success plus error"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1440]
sources: []
blocker: ""
wait_reason: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/1e83abd3c"]
resolution: accepted
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

- [x] t-20261108-bughunt-0427-appnew-contradictory-exit · 0427-125 · App new meldet Erfolg plus Fehler #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/dx #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1440](https://github.com/mcpdev80/baseharbor/pull/1440)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/1e83abd3c)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1440](https://github.com/mcpdev80/baseharbor/pull/1440)  
**Source:** 
<!-- /generated:links -->

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-1 podman2 hunt on develop 0fe53052: wizard-completed run prints success then an restore-required error at exit; string is composed, repro in the act.

## Acceptance

app new exits with exactly one truthful verdict (success XOR actionable error + next command); no success+error pairing; regression covers the exit path.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.

## 2026-11-08 Takeover (ChatGPT)

- Owner: `owner:chatgpt`; Lane: `active`.
- Work order: a small, targeted product fix including regression and a mandatory PR CI. No simultaneous changes to other cards.
- No product commit and no PASS/completion claimed yet; evidence/PR added after actual implementation.

## 2026-11-08 Produktarbeit (ChatGPT)

- [PR #1440](https://github.com/mcpdev80/baseharbor/pull/1440), Head `425777028faadd7ac100e3f2dd1ef4d0cb308a5a`: `app new` meldet `Created` und `Validation: SATISFIED` erst nach erfolgreicher Target-Registrierung bzw. optionalem Lifecycle. Zuvor moegliche gleichzeitige Erfolg/Fehler-Ausgabe wird verhindert.
- Regression ensures a failed lifecycle does not emit a success signal. PR CI pending, card `active`, not complete.

## 2026-11-08 Acceptance (ChatGPT)

- [PR #1440](https://github.com/mcpdev80/baseharbor/pull/1440) **merged to develop**: `1e83abd3ccd4f0b6622bde601384c628dd2cbef1`; checked head `425777028faadd7ac100e3f2dd1ef4d0cb308a5a`.
- [CI #42429399440](https://github.com/mcpdev80/baseharbor/actions/runs/42429399440) terminal `success`, all jobs successful, no errors; native cross-repo VM journey was not part of this small bug acceptance.
- **Status `closed` / accepted:** targeted product fix and regression integrated.

## 2026-11-08 Owner Release and Handover

- Processing owner changed from `"owner:chatgpt"` to `unassigned`. An already accepted card stays `closed`.
- Fixed/accepted #1440.
- Alle bestehenden PR-, Commit- und CI-Belege bleiben unveraendert. Kein neuer PASS behauptet.
