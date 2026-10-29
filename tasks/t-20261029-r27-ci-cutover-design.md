---
id: t-20261029-r27-ci-cutover-design
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
early: true
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261029-r27-ci-cutover-design · CI: specify candidate-bound completion and ruleset #task #release/v0-4-27 #status/planned #view/ready #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Specify candidate-bound asynchronous CI completion

## Scope

Read actual current required checks, app identities, rulesets and workflow events; propose a bounded completion signal after durable receipt approval, exact candidate binding, migration and rollback. Coordinate with coverage inventory without editing its files.

## Acceptance

Design identifies check name, producing app, event, stale/missing/failure behavior, precise rule changes and verification; unresolved rights or coverage are explicit. No activation in this slice.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Planning handoff under evidence/r27-ci-replacement-2026-10-29/cutover-design.md; no shared product writes.

## Handoff

Unassigned. Coordinator checks current claims and source heads before assignment.

