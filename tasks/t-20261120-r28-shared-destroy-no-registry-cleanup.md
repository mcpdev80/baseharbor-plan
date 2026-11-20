---
id: t-20261120-r28-shared-destroy-no-registry-cleanup
card_number: "0428-184"
card_short_title: "shared destroy skips registry"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Destroying a shared resource leaves its observability registry entries behind, so later registrations see stale owners."
kanban_title: 0428-184 · shared destroy skips registry
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

- [ ] t-20261120-r28-shared-destroy-no-registry-cleanup · Shared destroy does not clean the signal registry (stale owners survive) #task #release/v0-4-28 #status/planned
    <!-- generated:card -->
    **Owner:** unassigned  
    <!-- /generated:card -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

F3 of hunt round-1: the destroy path for shared resources removes containers/volumes but does not drop the registry rows that named those signals, so a later RegisterProviderSignals sees an owner that no longer exists. This is the same registry that 0428-166 just hardened with a collision guard, so the interaction is not hypothetical.

## Acceptance

1. Destroy of a shared resource removes (or marks reusable) exactly the registry entries it owns, and a re-registration afterwards succeeds with a fresh owner.
2. A regression that is red if the cleanup line is deleted, and a second case proving a FOREIGN owner entry is NOT deleted (no cross-tenant wipe).
3. CI job name recorded; the test runs in the packages shard.

## Boundaries

internal/observability/** plus the destroy path in internal/runtime/**. Read 0428-166 merged behaviour first (provider_registration.go, migration.go) and stop with a report if the cleanup would change collision semantics.
