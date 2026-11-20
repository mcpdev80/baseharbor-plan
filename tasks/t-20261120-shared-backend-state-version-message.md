---
id: t-20261120-shared-backend-state-version-message
card_number: "0428-201"
card_short_title: "shared state version message"
type: bug
areas: [lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-201 · shared state version message
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-shared-backend-state-version-message · shared state version message #task #release/v0-4-28 #status/planned #view/ready #area/lifecycle #kind/bug
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

## Found by bug hunt H-V21 (2026-11-20, develop `40cb28c758b0`)

Hunt akte: `evidence/r28-welle4-2026-11-20/bughunt-hv21-shipped-surface/round-1.md`, slice "upgrade from outside".

`internal/application/shared_backends.go:17` sets `sharedBackendStateVersion = 3`; `decodeSharedBackendState`
(`internal/application/shared_backends_state.go:31-32`) rejects any other version with
`unsupported shared backend state version N`. No migration from v1/v2, no discard: pure fail-closed. That is the
intended decision of the shared-backend cards, so the gate itself is right.

What is missing is the surface: two different state files (`deployment.json` and the shared-backends state) both
carry a version field that fails closed, but neither human message tells the operator that this is an
upgrade-from-outside situation. See the sibling finding `0428-200`, which shows the same class on the deployment
record where the message is not just generic but actively false.

## Acceptance

1. The shared-backends version failure names the version found, the version expected, and the supported next
   step, and is distinguishable from a corrupt or unreadable file.
2. Fail-closed behavior stays byte-identical: no migration, no discard, no rewrite.
3. A regression writes a v2 state file, runs the real command surface that loads it, and asserts the version
   reason (not a generic error) reaches the user.
4. One hosted run at the exact head shows the owning shard executed, 0 failure. Gate failures from `0428-198` are
   recorded and reported, not fought.

## Boundaries and stops

- Allowed to write: `internal/application/shared_backends_state.go` (message plus error kind) and its test files;
  `internal/application/shared_backends.go` only for the error type it exposes.
- Locked (other owners): `internal/observability/registry.go` (0428-078 plus 0428-189..194),
  `internal/application/perses_runtime.go` and `internal/serviceaccess/**` (#1684),
  `internal/machine/**`, `internal/operatorauth/**`, `internal/identityprovider/**` (#1594/#1615/#1650 owner),
  `internal/metrics/**` (#1714), `cmd/baha/context_terminal*.go` (#1718).
- Do not add a migration path without a card and an owner decision.
- No subagents (AGENTS 4.8), no `git add -A`, no merge, no force-push on develop/main.
