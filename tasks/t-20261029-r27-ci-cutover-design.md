---
id: t-20261029-r27-ci-cutover-design
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "q201 (38460858, qwen)"
early: true
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-29/scripts/ruleset-activation/README-activation.md"]
---

- [x] t-20261029-r27-ci-cutover-design · CI: specify candidate-bound completion and ruleset #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** q201 (38460858, qwen) · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-29/scripts/ruleset-activation/README-activation.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** q201 (38460858, qwen)  
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

Lane q201 delivered cutover-design.md (END q201-DONE, disk-verified). Read-only deliverable: card stays active per schema (review needs PR); coordinator integrates design findings with coverage-inventory when cutting over. Evidence: https://github.com/mcpdev80/baseharbor-plan/blob/HEAD/evidence/r27-ci-replacement-2026-10-29/cutover-design.md

