---
id: t-20261120-r28-valkey-dashboard-unavailable-only
card_number: "0428-183"
card_short_title: "valkey dashboards gate"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-183 · valkey dashboards gate
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

- [ ] t-20261120-r28-valkey-dashboard-unavailable-only · Perses: new DB/Valkey dashboards reachable only as DashboardUnavailable #task #release/v0-4-28 #status/planned #view/ready #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

F2 of hunt round-1, measured at develop 96f2ae11a25a: internal/metrics/valkey.go:187, :195, :226, :265 return DashboardUnavailable on every path the hunt could reach, so availability is never true even when the backend is configured and verified.

## Acceptance

1. An availability path that returns a real dashboard (not DashboardUnavailable) when the backend signal is configured AND verified, mirroring the identity-dashboard predicate that 0428-078 hardened.
2. Tests for all three states (not_configured, configured_unverified, verified) on the DB and Valkey faces; configured_unverified must be false.
3. Mutation both directions (predicate reverted, availability branch forced) with separate isolated tests, and the CI job name in the evidence.

## Boundaries

internal/metrics/** plus the dashboard catalog. No .github/**, no gate changes. Coordinate with 0428-078 (identity dashboard) so the same availability semantics are not implemented twice differently.
