---
id: t-20261117-hunt-signals-105
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-105"
title: "Alert-Ebene develop-weit leer"
kanban_status: closed
kanban_lane: closed
kanban_title: 0428-105 · Alert-Ebene develop-weit leer
kanban_summary: ""
sources: []
source_note: "hunt hunt-signals befund-1 (akte: evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)"
depends_on: [t-20261114-r28-perses-alerts]
owner: Codex (Marcel Wait sweep 2026-11-21)
blocker: ""
wait_reason: ""
resolution: superseded
superseded_by: t-20261114-r28-perses-alerts
prs: ["mcpdev80/baseharbor#1704"]
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md"
  - "https://github.com/mcpdev80/baseharbor/pull/1704"
  - "https://github.com/mcpdev80/baseharbor/commit/dea88c8f2caa2db93c1216c619993e444080a9d2"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44908265726"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44908259476"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44908259346"
card_short_title: Alert-Ebene develop-weit leer
---

- [x] t-20261117-hunt-signals-105 · Alert-Ebene develop-weit leer #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Marcel Wait sweep 2026-11-21)  
    **PR:** [baseharbor#1704](https://github.com/mcpdev80/baseharbor/pull/1704)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1704), [proof 3](https://github.com/mcpdev80/baseharbor/commit/dea88c8f2caa2db93c1216c619993e444080a9d2), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44908265726), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44908259476), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44908259346)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md)  
**Owner:** Codex (Marcel Wait sweep 2026-11-21)  
**Priority:** not set  
**PRs:** [baseharbor#1704](https://github.com/mcpdev80/baseharbor/pull/1704)  
**Source:** 
<!-- /generated:links -->

Einzelschritte in der referenzierten hunt-akte (befund-1.md); Umsetzung als normale task-kette (claim -> branch -> CI -> evidence -> review).


## Handoff - 2026-11-17

**ZWEIFEL — returned to the queue without product changes.** The develop-wide absence of alert-rule registration is confirmed by the hunt evidence and current develop source, but the overlapping implementation is already owned by 0428-073 / PR #1613, which is still a draft and has not merged. Avoid a second alert-evaluator write set. This card now depends on 0428-073 and can be reassessed after that task is accepted. No product branch, commit or PR was created. Codex hands this lane to the next release-blocking Ready card 0428-113, the repeated Docker Loki log-ingestion timeout.


## Resolution — 2026-11-21

Superseded by accepted task [0428-073](t-20261114-r28-perses-alerts.md). This hunt recorded that develop lacked an alert evaluation level. PR [#1704](https://github.com/mcpdev80/baseharbor/pull/1704) now provisions the owned Prometheus rule and proves real evaluation plus persisted TSDB history; it merged as `dea88c8f2caa2db93c1216c619993e444080a9d2`. Exact PR checks passed in [44908265726](https://github.com/mcpdev80/baseharbor/actions/runs/44908265726), with native Docker and Podman acceptance in [44908259476](https://github.com/mcpdev80/baseharbor/actions/runs/44908259476) and [44908259346](https://github.com/mcpdev80/baseharbor/actions/runs/44908259346). No separate implementation remains for this duplicate finding.
