---
id: t-20261128-hunt48-refresh-public-api-ownership-map
card_number: "0428-345"
card_short_title: "refresh public API surface map"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-345 · refresh public API surface map
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/metrics/perses_prometheus_datasource_runtime.go#L20-L35","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/metrics/perses_prometheus_datasource_runtime.go#L138-L150","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md"]
---

- [x] t-20261128-hunt48-refresh-public-api-ownership-map · 0428 hunt H-V48: stale API ownership map reference #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/metrics/perses_prometheus_datasource_runtime.go#L20-L35), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/metrics/perses_prometheus_datasource_runtime.go#L138-L150), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Disposition

DROP after current-source recheck. The historical `internal/api`/`api-old` package split and the referenced ownership map are absent. The two surviving references are comments in a Prometheus datasource loader; updating those comments is opportunistic cleanup, not a public API ownership-map defect or a necessary v0.4.28 release outcome. BF-48-6 is therefore closed without a dedicated implementation card.
