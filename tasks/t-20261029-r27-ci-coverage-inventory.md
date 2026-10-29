---
id: t-20261029-r27-ci-coverage-inventory
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

- [ ] t-20261029-r27-ci-coverage-inventory · CI: map current required checks and replacement coverage #task #release/v0-4-27 #status/planned #view/ready #area/ci #kind/task
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

Map all current required checks and replacement coverage

## Scope

Read current protected branch/rulesets, workflows, planner, required check names, executor capacity and existing test discovery. Produce an exact check-to-new-path mapping with gaps and source links. Read-only: do not change workflows or rulesets.

## Acceptance

Evidence identifies each required check, actual test invocation, source and candidate binding, runner and replacement or explicit unresolved gap. No unverified parity claim.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Planning handoff under evidence/r27-ci-replacement-2026-10-29/coverage-inventory.md; no product writes.

## Handoff

Unassigned. Coordinator checks current claims and source heads before assignment.

