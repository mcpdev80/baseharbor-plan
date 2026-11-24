---
id: t-20261120-r28-restart-persist-signal-dump
card_number: "0428-189"
card_short_title: "restart drops signal state"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: 0428-189 · restart drops signal state
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

- [ ] t-20261120-r28-restart-persist-signal-dump · Persisted signal state is written as a dump that a restart does not fully re-establish. #task #release/v0-4-28 #status/planned #view/waiting #board/planned #kind/bug
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

`internal/observability/registry.go:306-312`: persistence writes a dump of the in-memory list, and on a second start not every entry the first run registered is re-established through the same path. After a restart a signal that was live before can be missing or duplicated, with no error anywhere.

## Acceptance

1. State the persistence contract in a comment at the dump site: what survives a restart, in which order, and which fields are reconstructed.
2. A regression that registers sources, persists, reloads the same file in a fresh process state and asserts the SAME set (id, target, class, scope): red when an entry is lost or duplicated.
3. Name the CI job that executes the test in the evidence; a test that only runs in a VM is not evidence (AGENTS 5.3).

## Boundaries

internal/observability/registry.go plus its test. No .github/** unless the gate route of the new test is missing - then the route belongs in this same PR (Owner guidance 2026-11-20, baseharbor-plan 51d95b99).

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
