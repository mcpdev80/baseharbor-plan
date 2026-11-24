---
id: t-20261120-r28-runtimetarget-failclosed
card_number: "0428-190"
card_short_title: "empty target accepted"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: 0428-190 · empty target accepted
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

- [ ] t-20261120-r28-runtimetarget-failclosed · An empty or foreign runtime target is accepted instead of failing closed. #task #release/v0-4-28 #status/planned #view/waiting #board/planned #kind/bug
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

`internal/observability/registry.go:257-272`: empty targets and targets owned by someone else go through the same branch as valid ones. A registration can therefore bind a signal to nothing, or to another tenant target, and still report success.

## Acceptance

1. Fail closed on an empty target and on a target the registering scope does not own, with an error string that says which of the two it is.
2. Regression in both directions: valid target registers; empty target and foreign target each produce the named error.
3. Name the CI job that runs the test.

## Boundaries

internal/observability/registry.go plus its test. Do NOT restructure registryPath and do NOT add target-uid/root fields - that schema work is the owner 0428-078 card (see sequel note).

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
