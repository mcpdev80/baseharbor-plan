---
id: t-20261120-r28-keycloak-producer-target-mismatch
card_number: "0428-185"
card_short_title: "producer target mismatch"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-185 · producer target mismatch
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

- [ ] t-20261120-r28-keycloak-producer-target-mismatch · Keycloak producer registers ID/target the identity witness can never match #task #release/v0-4-28 #status/planned #view/ready #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
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

## Found by the owner's Codex takeover of 0428-078 (2026-11-20, finding-to-card duty AGENTS 3.3.5)

Measured while the owner completed 0428-078: internal/identityprovider/keycloak_realization.go registers the signal with id 'keycloak:<files.Project>' and target 'keycloak:9000', while internal/metrics/perses_identity_witness.go looks for the name 'keycloak-metrics' with target = m.Name. The two spellings never coincide, so the witness rejects a genuine production record. This is the root cause behind the P3 blocker of review 1650-0428-078-r8.md: target isolation cannot be proven while the producer and the witness disagree about what a target is.

## Acceptance

1. One canonical identity for the produced signal (name and target) chosen in the producer or in the witness, not both patched independently; write the chosen form into a comment where it is read.
2. A regression that registers the REAL producer record and asserts the witness accepts it (positive direction) and that a foreign target still fails (negative direction).
3. If target-uid/state-root scoping needs a schema change in internal/observability/registry.go or provider_registration.go (today the registryPath is global, without target uid/root): that change belongs to the card that owns those files for this release - coordinate before editing, see AGENTS 4.3.

## Boundaries

internal/identityprovider/keycloak_realization.go plus internal/metrics/perses_identity_witness.go. internal/observability/registry.go and provider_registration.go are released to the 0428-078 takeover work for the target-root change; 0428-184 is confined to its destroy-side cleanup. No .github/**.
