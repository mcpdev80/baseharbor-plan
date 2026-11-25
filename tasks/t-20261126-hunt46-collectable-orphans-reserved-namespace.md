---
id: t-20261126-hunt46-collectable-orphans-reserved-namespace
card_number: "0428-327"
card_short_title: "collectable orphan skip dir"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "CollectableOrphans (internal/deployment/deploymentlist.go:185) enumerates each direct child directory of deployments/ as a…"
kanban_title: 0428-327 · collectable orphan skip dir
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

- [ ] t-20261126-hunt46-collectable-orphans-reserved-namespace · 0428 hunt H-V46: CollectableOrphans lists the reserved never-delivered dir as a collectable orphan UUID (medium) #task #release/v0-4-28 #status/planned #view/ready #kind/task
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

## Goal

`CollectableOrphans` (internal/deployment/deployment_list.go:185) enumerates each direct child directory of `deployments/` as a would-be deployment UUID. The reserved `never-delivered/` directory is a direct child of `deployments/`, so it is enumerated; it is only not listed as an orphan by accident (a missing `never-delivered/deployment.json` read bails early). This card adds an explicit reservation skip so the reader (orphan/damage scan) excludes the namespace the writer (adoption) creates at `never-delivered/<applicationID>/<environment>.json`.

## Scope

- In scope:
  - `internal/deployment/deployment_list.go` `CollectableOrphans`: skip the reserved `never-delivered` subdirectory explicitly at the enumeration loop (before `deploymentOwnerMissingForDetach`), not by relying on a missing-record read.
  - Positive regression: a crafted `never-delivered/deployment.json` whose `DeploymentID=="never-delivered"` and `Target==target` is NOT returned as a collectable orphan (reproducible with the existing deployment harness).
- Out of scope:
  - The `DamagedDeploymentNamespace` reserved-namespace guard: same root cause, different seam — separate card 0428-328.

## Acceptance

- `CollectableOrphans` explicitly skips the reserved `never-delivered` subdirectory regardless of its contents.
- The crafted reserved-dir record (DeploymentID/Target match) is no longer advertised as a collectable orphan.
- Positive regression via the existing deployment harness proving the reserved dir is excluded.
- Every required test is reachable by a real CI check in the same PR; test registered and mapped in the same PR (Gate Rule). Docker/Podman: n/a (pure state-file seam).
- Exact source SHA -> test ID -> mapped CI gate -> trigger -> actual run recorded in handoff.

## Dependencies and file ownership

- Owned files or areas: `internal/deployment/deployment_list.go`.
- Shared files: n/a.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V46 (akte evidence/r28-welle6-2026-11-27/bughunt-hv46-state-lifecycle/ on origin/main 62de9bb74, anchor develop 2a141387d; re-verified against develop 384d857b5 at intake). BF-46-3 LIVE (proven by repro at intake). `CollectableOrphans` iterates `os.ReadDir(root/deployments)` and treats each `IsDir()` child name as a `deploymentID`. The `never-delivered/` directory is a direct child of `deployments/`, so it is enumerated at line 189 (`deploymentID := entry.Name()` => "never-delivered"); current code only avoids listing it by relying on the read of a nonexistent `never-delivered/deployment.json` to bail. If the subtree ever contains a `deployment.json` whose embedded `DeploymentID=="never-delivered"` and `Target==target` (which the current code now admits), the guard attributes the reserved dir as a collectable orphan UUID. Reproduced at intake with a crafted record: `CollectableOrphans` returned the reserved dir. Fix: make `CollectableOrphans` explicitly skip the reserved `never-delivered` subdirectory (matching the reservation the adoption writer creates at `never-delivered/<applicationID>/<environment>.json`, never_deliveredProofPath:21).
