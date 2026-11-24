---
id: t-20261120-r28-prune-key-too-coarse
card_number: "0428-194"
card_short_title: "prune key too coarse"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: 0428-194 · prune key too coarse
priority: ""
depends_on: [t-20261114-r28-perses-dashboard-identity]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-prune-key-too-coarse · Pruning is keyed by provider/class/scope only, so it can drop another product signal of the same class. #task #release/v0-4-28 #status/planned #view/waiting #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261114-r28-perses-dashboard-identity](t-20261114-r28-perses-dashboard-identity.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-dashboard-identity](t-20261114-r28-perses-dashboard-identity.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-V17 (2026-11-20, develop f5ce95afce1c)

Hunt akte: `evidence/r28-welle4-2026-11-20/bughunt-hv17-restart-desk/round-1.md`, slice "restart / persistence desk",
base witnessed against develop `f5ce95afce1cfec053dd7717ed05e89bfe153535`.

`internal/observability/registry.go:274-291`: the prune key does not carry the owning boundary tightly enough, so a prune meant for one product can remove a different product signal of the same provider and class. Same failure family the owner stopped twice today (0428-166, 0428-184).

## Acceptance

1. Narrow the prune key so a prune can only ever remove rows written by the same boundary and product, and prove a FOREIGN same-class row survives.
2. Mutation proof: widen the key again and show this specific test turns red, output archived verbatim.
3. Name the CI job that runs the test.

## Boundaries

internal/observability/registry.go (the PruneOwnedPlatformSources site added by #1715) plus tests. #1715 (0428-184) is in review while this card is written: rebase onto develop after it merges.

## Sequel note

This card declares `t-20261114-r28-perses-dashboard-identity` (0428-078) on purpose: the owner's takeover of that card
currently holds `internal/observability/registry.go` for the target / state-root schema. Start this card only after that
write is merged, otherwise the two changes collide in the same file (AGENTS 4.3).


## Cross-reference (bughunt-hv26 F2, by-design, no new card)

Hunt H-V26 F2 records a different spot from this card's consent surface: `--confirm-candidate` is required only
where `record.Source.Kind == "repository" && state == "applying"` (`cmd/baha/deployment_record.go:520-521`,
fail-closed leaf at `:528-573` via `finalizeCandidateConsent`, `cmd/baha/app_candidate_consent.go:180-206`), with
CLI/`up`/remote/MCP all routed through the one context override (`app_candidate_consent.go:50-52`, `:63-67`,
`cmd/baha/mcp_tools.go:486`). Managed-app create uses a non-repository source and is excluded by design.
This card stays the owner of its own consent surface; see dossier
`evidence/r28-welle6-2026-11-24/bughunt-hv26-candidate-consent-gate/round-1.md` (develop 3ebfb90d).
