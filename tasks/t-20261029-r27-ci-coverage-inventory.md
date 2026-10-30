---
id: t-20261029-r27-ci-coverage-inventory
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "o202 (1138dbc9, ornith)"
early: true
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/blob/develop/docs/internal/ci-binding-qualifications.md", "https://github.com/mcpdev80/baseharbor/blob/develop/docs/development/minimal-ci-receipts.md"]
---

- [x] t-20261029-r27-ci-coverage-inventory · CI: map current required checks and replacement coverage #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** o202 (1138dbc9, ornith) · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/docs/internal/ci-binding-qualifications.md), [proof 2](https://github.com/mcpdev80/baseharbor/blob/develop/docs/development/minimal-ci-receipts.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** o202 (1138dbc9, ornith)  
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

Schema note: review status requires a PR; this is a read-only planning deliverable, so the card stays active until the integrated candidate PR carries it. Lane o202 delivered coverage-inventory.md (END o202-DONE, planning commit verified on origin/main, disk-checked by coordinator). Coordinator verification: substantive inventory correct; ONE misdiagnosis — section 1 "rulesets are empty shells" is wrong: GET /rulesets/{id} shows rule 'required_status_checks' (context PR Selected Checks, integration_id 15368) on id 25223521; the lane used a nonexistent /rules sub-endpoint (404). PLANNING_RECEIPT_WRITE_TOKEN exists (names-only check). Awaiting independent review at content level; acceptance per CODEMAN-START proof section.

