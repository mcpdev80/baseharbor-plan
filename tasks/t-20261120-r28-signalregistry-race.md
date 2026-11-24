---
id: t-20261120-r28-signalregistry-race
card_number: "0428-192"
card_short_title: "registry has no lock"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: 0428-192 · registry has no lock
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

- [ ] t-20261120-r28-signalregistry-race · The signal registry has no cross-process guard, so two concurrent writers overwrite each other. #task #release/v0-4-28 #status/planned #view/waiting #board/planned #kind/bug
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

`internal/observability/registry.go:472-513,515-530`: read-modify-write without a lock or an atomic rename. Two processes (two baha invocations, or the connector racing the CLI) that register at the same time can lose one registration completely while both report success.

## Acceptance

1. Choose one guard (file lock or rewrite-then-atomic-rename) and state at the site why the other was not needed.
2. A regression that runs two concurrent mutations against the same file and asserts both survive (or the loser fails with a named error): red without the guard.
3. Keep the test deterministic and inside the CI time budget; name the job that runs it.

## Boundaries

internal/observability/registry.go plus test. If a helper file is needed for the lock, keep it inside internal/observability/.

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
