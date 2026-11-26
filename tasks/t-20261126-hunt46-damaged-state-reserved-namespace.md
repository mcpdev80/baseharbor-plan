---
id: t-20261126-hunt46-damaged-state-reserved-namespace
card_number: "0428-328"
card_short_title: "skip reserved damaged scan"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "DamagedDeploymentNamespace (internal/deployment/damagedstate.go:266) iterates deployments/ children and calls…"
kanban_title: 0428-328 · skip reserved damaged scan
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1869"]
sources: []
blocker: "blocked-BASELINE as STATE: family catalog PR #1869 open, develop row pending freeze-lift per w267 7199390854; candidate heads recorded"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261126-hunt46-damaged-state-reserved-namespace · 0428 hunt H-V46: DamagedDeploymentNamespace flags the reserved never-delivered namespace as damaged (low) #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **PR:** [baseharbor#1869](https://github.com/mcpdev80/baseharbor/pull/1869)  
    **Blocker:** blocked-BASELINE as STATE: family catalog PR \#1869 open, develop row pending freeze-lift per w267 7199390854; candidate heads recorded  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** [baseharbor#1869](https://github.com/mcpdev80/baseharbor/pull/1869)  
**Source:** 
<!-- /generated:links -->

## Goal

`DamagedDeploymentNamespace` (internal/deployment/damaged_state.go:266) iterates `deployments/` children and calls `DamagedDirectoryState` on each. The reserved `never-delivered/` directory is a child of `deployments/` and is reached by the scan. It only avoids flagging while it holds only `.json` proof files; the current proof-exclusion guard excludes a damaged directory only when a proof for THIS repository app exists, not when the namespace itself is the reserved one. This card adds an explicit reservation skip.

## Scope

- In scope:
  - `internal/deployment/damaged_state.go` `DamagedDeploymentNamespace`: skip the reserved `never-delivered` subdirectory explicitly at the enumeration loop.
  - Positive regression: placing a protected-state file (e.g. `runtime.env`) directly under `never-delivered/` no longer flags the Target as having damaged deployment state.
- Out of scope:
  - The `CollectableOrphans` reserved-namespace guard: same root cause, different seam — separate card 0428-327.

## Acceptance

- `DamagedDeploymentNamespace` explicitly skips the reserved `never-delivered` subdirectory.
- A protected-state file placed directly under the reserved namespace does not flag the Target as damaged.
- Positive regression via the existing damaged-state harness proving the reserved namespace is excluded.
- Every required test is reachable by a real CI check in the same PR; test registered and mapped in the same PR (Gate Rule). Docker/Podman: n/a (pure state-file seam).
- Exact source SHA -> test ID -> mapped CI gate -> trigger -> actual run recorded in handoff.

## Dependencies and file ownership

- Owned files or areas: `internal/deployment/damaged_state.go`.
- Shared files: n/a.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V46 (akte evidence/r28-welle6-2026-11-27/bughunt-hv46-state-lifecycle/ on origin/main 62de9bb74, anchor develop 2a141387d; re-verified against develop 384d857b5 at intake). BF-46-4 LIVE (proven by repro at intake). `DamagedDeploymentNamespace` iterates `deployments/` entries and calls `DamagedDirectoryState` on each child dir (line 270). `DamagedDirectoryState` (177-204) returns true when a child dir has no `deployment.json` but retains protected state files. The `never-delivered/` directory is a child of `deployments/` and the current proof-exclusion guard (lines 277-287) only skips a damaged directory when a proof for THIS repository app exists, not when the namespace itself is reserved. Reproduced at intake: placing `runtime.env` directly under `never-delivered/` flags the Target as having damaged deployment state. Fix: explicitly skip the reserved `never-delivered` subdirectory (matching the reservation the adoption writer creates).
