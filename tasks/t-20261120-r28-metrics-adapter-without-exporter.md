---
id: t-20261120-r28-metrics-adapter-without-exporter
card_number: "0428-182"
card_short_title: "adapter without exporter"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w182-0428-182-metricsadapter
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-182 · adapter without exporter
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md"]
---

- [ ] t-20261120-r28-metrics-adapter-without-exporter · Metrics: RequiresAdapter source has no exporter or compose wiring (never collectable) #task #release/v0-4-28 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** w182-0428-182-metricsadapter  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w182-0428-182-metricsadapter  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

F1 of hunt round-1: the source declares RequiresAdapter, but no exporter path and no compose service produces the value. The dashboard/metrics surface therefore shows the signal as structurally unavailable rather than merely unverified.

## Acceptance

1. Either wire the adapter (exporter plus the compose/service entry the contract requires) so the signal becomes collectable, or drop RequiresAdapter from the source with a documented reason.
2. A regression that fails if the source keeps RequiresAdapter while no adapter/compose producer exists (fail-closed at build or startup, not silently zero).
3. The new test is picked up by a named GitHub CI job; name it in the evidence (AGENTS 5.3).

## Boundaries

internal/metrics/** plus the compose/runtime wiring the adapter needs. If the fix must reach internal/application/perses_runtime.go, check first whether 0428-083 (#1684) is still open there and stop with a file:line report if it is.

hunt-fund F1 (hunt-signals-103/round-1.md) auf dem freigabenen sitz von 078: quelle erklaert RequiresAdapter, aber exporter/producer fehlt, metrik ist strukturell nicht sammelbar. akzeptanz: verdrahten ODER RequiresAdapter entfernen (begruendet), regression fail-closed, CI-jobname in der akte. SCHREIBFELDER disjunkt gewaehlt: die dateien von #1684, #1645, 0428-183 (valkey.go) und internal/observability/** (0428-184) sind in der mission ausdruecklich verschlossen, meldung statt doppelschreiber (§4.3).
