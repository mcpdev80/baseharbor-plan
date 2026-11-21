---
id: t-20261117-hunt-signals-105
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-105"
title: "Alert-Ebene develop-weit leer"
kanban_status: active
kanban_lane: active
kanban_title: 0428-105 · Alert-Ebene develop-weit leer
kanban_summary: ""
sources: []
source_note: "hunt hunt-signals befund-1 (akte: evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)"
depends_on: [t-20261114-r28-perses-alerts]
owner: Codex (Marcel Wait sweep 2026-11-21)
blocker: ""
wait_reason: ""
resolution: ""
superseded_by: ""
prs: []
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md", "https://github.com/mcpdev80/baseharbor/pull/1613", "https://github.com/mcpdev80/baseharbor/blob/develop/spec/capabilities/metrics/v1.md"]
card_short_title: Alert-Ebene develop-weit leer
---

- [ ] t-20261117-hunt-signals-105 · Alert-Ebene develop-weit leer #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Marcel Wait sweep 2026-11-21)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1613), [proof 3](https://github.com/mcpdev80/baseharbor/blob/develop/spec/capabilities/metrics/v1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md)  
**Owner:** Codex (Marcel Wait sweep 2026-11-21)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Einzelschritte in der referenzierten hunt-akte (befund-1.md); Umsetzung als normale task-kette (claim -> branch -> CI -> evidence -> review).


## Handoff - 2026-11-17

**ZWEIFEL — returned to the queue without product changes.** The develop-wide absence of alert-rule registration is confirmed by the hunt evidence and current develop source, but the overlapping implementation is already owned by 0428-073 / PR #1613, which is still a draft and has not merged. Avoid a second alert-evaluator write set. This card now depends on 0428-073 and can be reassessed after that task is accepted. No product branch, commit or PR was created. Codex hands this lane to the next release-blocking Ready card 0428-113, the repeated Docker Loki log-ingestion timeout.
