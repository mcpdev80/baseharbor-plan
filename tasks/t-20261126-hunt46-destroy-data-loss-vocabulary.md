---
id: t-20261126-hunt46-destroy-data-loss-vocabulary
card_number: "0428-330"
card_short_title: "unify destroy data-loss words"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Two differently-named destructive scopes both delete owned volumes, but the data-loss severity wording is split across…"
kanban_title: 0428-330 · unify destroy data-loss words
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

- [ ] t-20261126-hunt46-destroy-data-loss-vocabulary · 0428 hunt H-V46: destroy --all and control-plane destroy --delete-data use split data-loss consequence vocabulary (low) #task #release/v0-4-28 #status/planned #view/ready #kind/task
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

Two differently-named destructive scopes both delete owned volumes, but the data-loss severity wording is split across `full-destroy` (installation) and `delete-data` (Core), so an operator (and the MCP/JSON surfaces) can conflate them. This card unifies the "delete owned volumes permanently" warning so it is surfaced identically for both scopes, or explicitly documents that they are distinct scopes.

## Scope

- In scope:
  - Review the "after" consequence text in `cmd/baha/control_plane_destroy.go` (`buildSelectedCoreDestroyPlan`, DeleteData branch) and the `full-destroy` discovery/reporting surface (`cmd/baha/runtime_destroy_discovery.go`), and surface the "owned volumes permanently lost" consequence identically, or add an explicit shared "DESTRUCTIVE DATA LOSS" tag in one place.
  - Low severity: intended behavior; risk is operator conflation. Scope the change to wording/consent surface, not to what either scope deletes.
- Out of scope:
  - The recovery/backup volume provenance heuristic: 0428-329.
  - The never-delivered proof leak: 0428-326.

## Acceptance

- Both destructive scopes surface the owned-volumes-permanently-lost consequence with identical wording (or an explicit shared tag), with no silent divergence.
- The actual deletion scope of each command is unchanged (full-destroy deletes all owned; selected-core --delete-data deletes only canonical Core volumes).
- No product behavior delta beyond the consequence/consent wording.
- Every required test is reachable by a real CI check in the same PR where the change warrants a regression (consent-surface/JSON contract path). Docker/Podman: n/a.
- Exact source SHA -> test ID -> mapped CI gate -> trigger -> actual run recorded in handoff.

## Dependencies and file ownership

- Owned files or areas: consequence/consent wording in the destroy surface.
- Shared files: n/a.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V46 (akte evidence/r28-welle6-2026-11-27/bughunt-hv46-state-lifecycle/ on origin/main 62de9bb74, anchor develop 2a141387d; re-verified against develop 384d857b5 at intake). BF-46-1 LIVE. The whole-installation `destroy --all` path is discovered/reported as `full-destroy` (runtime_destroy_discovery.go: discoverFullDestroyTargets, discoverFullDestroyDeployments, fullDestroyResult). The single Core module path, `control-plane destroy`, is gated by a different context key `selectedCoreDataDeletionKey` / `DeleteData` flag, not by `full-destroy` (control_plane_destroy.go:19, 39, 70-72). Vocabulary gap: the "after" consequence text is built conditionally on `p.DeleteData`; full-destroy names "continuing to preserve application-owned workload data volumes" (CHANGELOG.md:473) while the selected-core `--delete-data` path (line 71) says "Volume contents are permanently lost". Neither surfaces a shared "DESTRUCTIVE DATA LOSS" tag in one place. Fix: unify the data-loss consequence vocabulary, or explicitly document that they are distinct scopes.
