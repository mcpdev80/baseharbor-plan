---
id: t-20261017-release-0-4-30-cleanup
type: maintenance
areas: [release]
release: v0.4.30
version: v0.4.30
release_stage: cleanup
parent: v0.4.30
owner: ""
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-4-30-cleanup · v0.4.30 · Release start: reconcile old PRs, tasks and branches #task #release/v0-4-30 #status/planned #view/queued #area/release #kind/maintenance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Later release** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** queued  
**Release:** [v0.4.30](../releases/v0.4.30.md) (v0.4.30)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-30-updates](t-20261017-release-0-4-30-updates.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reconcile previous-release leftovers before new development.

## Scope and acceptance

- Read current remote PRs, task claims, branches, release evidence and running CI across BaseHarbor, Demo, Console, Connector and this plan repository.
- Close or supersede obsolete PRs/tasks only with an integration or explicit-obsolescence reference. Preserve genuinely active/future work and owner claims; no blanket deletion of unmerged code.
- Delete incorporated temporary branches. Preserve maintained tracks, immutable tags, approval/candidate refs and evidence still needed by release verifiers; apply existing artifact-GC retention rules.
- Publish a concise kept/removed/deferred inventory with reasons on planning main. No product changes, release or task acceptance is implied by cleanup.

## Required checks

Inspect actual remote state; verify required changes are incorporated before deletion. No runtime journey or full matrix for housekeeping.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#cleanup). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
