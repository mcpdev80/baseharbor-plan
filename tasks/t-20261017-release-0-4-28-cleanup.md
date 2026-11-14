---
id: t-20261017-release-0-4-28-cleanup
card_number: "0428-002"
card_short_title: "reconcile old PRs, tasks and"
type: maintenance
areas: [release]
release: v0.4.28
version: v0.4.28
release_stage: cleanup
parent: v0.4.28
owner: lane-0428-002-r28
kanban_lane: closed
kanban_summary: Reconcile previous-release leftovers before new development.
kanban_status: closed
kanban_title: "0428-002 · reconcile old PRs, tasks and"
priority: high
depends_on: [t-20261017-release-0-4-27-verify]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/commit/2ab26e5f"]
early: true
---

- [x] t-20261017-release-0-4-28-cleanup · v0.4.28 · Release start: reconcile old PRs, tasks and branches #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/release #kind/maintenance
    <!-- generated:card -->
    **Owner:** lane-0428-002-r28 · **Priority:** high  
    **Needs:** [t-20261017-release-0-4-27-verify](t-20261017-release-0-4-27-verify.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/commit/2ab26e5f)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md) (v0.4.28)  
**Depends on:** [t-20261017-release-0-4-27-verify](t-20261017-release-0-4-27-verify.md)  
**Required by:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
**Owner:** lane-0428-002-r28  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reconcile previous-release leftovers before new development.

## Scope and acceptance

- Read current remote PRs, task claims, branches, release evidence and running CI across BaseHarbor, Demo and this plan repository; archived Console and Node Connector are excluded.
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

## Owner sequencing decision — 2026-11-14

v0.4.27 remains unreleased, so previous-release cleanup waits for its actual verification. The specifically authorized read-only 0.4.28 audits and coordination may proceed in parallel without treating v0.4.27 work as leftovers.
