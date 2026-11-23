---
id: t-20261120-r28-perses-status-never-verified
card_number: "0428-186"
card_short_title: "no verified status source"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w186-0428-186-verified-status-source
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-186 · no verified status source
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-perses-status-never-verified · No source API yields verified: status --json can never report true #task #release/v0-4-28 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** w186-0428-186-verified-status-source  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w186-0428-186-verified-status-source  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by the owner's Codex takeover of 0428-078 (2026-11-20, finding-to-card duty AGENTS 3.3.5)

Measured during the 0428-078 takeover: PersesStatusNow (internal/capability/perses_selection.go) has no code path producing the verified state, so 0428-078's acceptance item P1 (a positive verified case through the public baha status --json output) is not reachable without a probe/source API. Faking 'verified' or letting configured_unverified pass would destroy exactly what the verified-only predicate was introduced to protect (owner ruling r7, reviewer stop-criterion 1).

## Acceptance

1. Name the real probe or source API that can decide 'the Perses backend answers for this selection' and wire it to the status path, or state in the plan why a health probe is the right instrument.
2. Once such a source exists, the positive case in 0428-078 (status --json identity_dashboard_eligible=true) must be reachable by test without touching the predicate.
3. Never a literal true: no hard-coded verified value, no configured_unverified acceptance to make a test green.

## Boundaries

internal/capability/perses_selection.go is owner-closed for the 0428-078 card; this card is the place where a change there may be proposed. It is the sequenced predecessor of 0428-181 (catalog consumer) because a catalog needs a verified signal to emit anything.

dispatched; write-set internal/capability/perses_selection.go confirmed disjoint from w078 (keycloak/metrics/app_status_result)
