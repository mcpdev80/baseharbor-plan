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
kanban_summary: "Installation-wide baha destroy --all and selected-Core control-plane destroy --delete-data have different deletion scopes, but…"
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

0428-329 owns `baha app destroy`: delete every resource and volume inside the selected application's scope, including recovery- or backup-labelled volumes; retaining them would be app deletion. This card covers the separate installation-wide `baha destroy --all` scope, which deletes the installation-owned resources and volumes in its selected installation scope, and selected-Core `control-plane destroy --delete-data`, which remains limited to canonical Core resources and explicitly selected Core volumes. Warnings must name each command's actual data-loss scope; do not conflate application, installation, and selected-Core destruction.

## Goal

Installation-wide `baha destroy --all` and selected-Core `control-plane destroy --delete-data` have different deletion scopes, but their data-loss warnings can be conflated across CLI and structured surfaces. Make the consequences clear for both without changing either scope. `baha app destroy` semantics are defined separately by 0428-329.

## Scope

- In scope:
  - Review the "after" consequence text in `cmd/baha/control_plane_destroy.go` (`buildSelectedCoreDestroyPlan`, DeleteData branch) and the installation-wide `full-destroy` discovery/reporting surface (`cmd/baha/runtime_destroy_discovery.go`); clearly state the distinct scope and permanent-loss consequence in each.
  - Low severity: intended behavior; risk is operator conflation. Scope the change to wording/consent surface, not to what either scope deletes.
- Out of scope:
  - The recovery/backup volume provenance heuristic: 0428-329.
  - The never-delivered proof leak: 0428-326.

## Acceptance

- Both commands clearly surface the permanent-loss consequence, with wording appropriate to each scope; no operator can mistake selected-Core deletion for full installation destruction or vice versa.
- The actual deletion scope is unchanged: installation-wide `destroy --all` deletes resources and volumes owned by the selected installation; selected-Core `--delete-data` deletes only canonical Core resources and explicitly selected Core volumes. App-scoped `baha app destroy` remains governed by 0428-329.
- No product behavior delta beyond the consequence/consent wording.
- Every required test is reachable by a real CI check in the same PR where the change warrants a regression (consent-surface/JSON contract path). Docker/Podman: n/a.
- Exact source SHA -> test ID -> mapped CI gate -> trigger -> actual run recorded in handoff.

## Dependencies and file ownership

- Owned files or areas: consequence/consent wording in the destroy surface.
- Shared files: n/a.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Current-source recheck — 2026-11-25

At `mcpdev80/baseharbor/develop`, commit `119d12a5952ef48146dba129a7d1f03f8df36e8e`, `cmd/baha/runtime_destroy_impact.go` distinguishes installation-wide destruction from selected-Core destruction, and `cmd/baha/control_plane_destroy.go` describes permanent loss for explicitly selected canonical Core volumes. The installation destroy report also lists preserved external recovery locations separately. Align warnings with these scopes and the separate application-owned scope in 0428-329; do not imply that in-scope volumes are retained.

## Task

- Review the full-application and selected-Core destroy consequence/consent surfaces, including CLI and JSON/MCP output.
- State that installation-wide `baha destroy --all` permanently deletes every installation-owned resource and volume inside its selected scope; distinguish it from application-scoped `baha app destroy` (0428-329).
- State that selected-Core `--delete-data` deletes only canonical Core resources and explicitly selected Core volumes; preserve the rest of its narrower scope.
- Keep external recovery files, source repositories, foreign resources, and out-of-scope data clearly separate from both selected installation and selected-Core scopes.
- Add focused wording/contract regression coverage for both commands and their structured output.
- Run existing mapped checks and record the exact candidate SHA, test IDs, mapped gates, triggers, and results.

