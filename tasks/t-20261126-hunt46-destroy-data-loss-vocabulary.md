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

## Owner decision — 2026-11-25

A full application destroy deletes every resource and volume within the selected application's destruction scope, including recovery- or backup-labelled volumes. Otherwise the operation is app deletion. The selected-Core `control-plane destroy --delete-data` remains a narrower operation that deletes only its canonical Core resources and explicitly selected Core volumes. Warnings must state each scope's actual data-loss consequence clearly; use distinct wording where the scopes differ.

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

## Current-source recheck — 2026-11-25

At `mcpdev80/baseharbor/develop`, commit `7bdeae95ccf0ce0d2fe39ae6d4c884402268995d`, `cmd/baha/runtime_destroy_impact.go` distinguishes installation-wide destruction from selected-Core destruction, and `cmd/baha/control_plane_destroy.go` describes permanent loss for explicitly selected canonical Core volumes. The installation destroy report also lists preserved external recovery locations separately. Align warnings with these scopes and the owner decision for application-owned volumes; do not imply that an in-scope application volume is retained.

## Task

- Review the full-application and selected-Core destroy consequence/consent surfaces, including CLI and JSON/MCP output.
- State that full application destroy permanently deletes all resources and volumes inside the selected application's scope, including recovery/backup-labelled volumes.
- State that selected-Core `--delete-data` deletes only canonical Core resources and explicitly selected Core volumes; preserve the rest of its narrower scope.
- Keep external recovery files, source repositories, foreign resources, and out-of-scope data clearly separate from the selected application volume scope.
- Add focused wording/contract regression coverage for both commands and their structured output.
- Run existing mapped checks and record the exact candidate SHA, test IDs, mapped gates, triggers, and results.

