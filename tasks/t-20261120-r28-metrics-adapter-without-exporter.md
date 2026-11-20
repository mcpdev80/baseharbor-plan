---
id: t-20261120-r28-metrics-adapter-without-exporter
card_number: "0428-182"
card_short_title: "metrics adapter has no exporter"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "A metrics source is created with RequiresAdapter but no adapter/exporter or compose wiring exists, so its metrics can never be collected."
kanban_title: 0428-182 · metrics adapter has no exporter
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: [evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md]
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-metrics-adapter-without-exporter · Metrics: RequiresAdapter source has no exporter or compose wiring (never collectable) #task #release/v0-4-28 #status/planned
    <!-- generated:card -->
    **Owner:** unassigned  
    <!-- /generated:card -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

F1 of hunt round-1: the source declares RequiresAdapter, but no exporter path and no compose service produces the value. The dashboard/metrics surface therefore shows the signal as structurally unavailable rather than merely unverified.

## Acceptance

1. Either wire the adapter (exporter plus the compose/service entry the contract requires) so the signal becomes collectable, or drop RequiresAdapter from the source with a documented reason.
2. A regression that fails if the source keeps RequiresAdapter while no adapter/compose producer exists (fail-closed at build or startup, not silently zero).
3. The new test is picked up by a named GitHub CI job; name it in the evidence (AGENTS 5.3).

## Boundaries

internal/metrics/** plus the compose/runtime wiring the adapter needs. If the fix must reach internal/application/perses_runtime.go, check first whether 0428-083 (#1684) is still open there and stop with a file:line report if it is.
