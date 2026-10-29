---
id: t-20261029-r27-ci-producer
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: Flash-Coordinator (41e61806) via worker lanes
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

- [ ] t-20261029-r27-ci-producer · CI: qualify a real public-contracts producer #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Flash-Coordinator (41e61806) via worker lanes · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** Flash-Coordinator (41e61806) via worker lanes  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Qualify a genuine public-contracts pilot producer

## Scope

Select a small real profile-contract slice under contracts/ with .go or .json changes, after checking startup and existing work. Run the actual planner and targeted tests, establish deterministic task linkage and document candidate. Do not fabricate a no-op change.

## Acceptance

Planner selects integration/static/public-contracts, relevant real checks execute, and the exact PR/candidate is available for the automatic chain. Product task itself is accepted only against its full criteria.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Reserve only the concrete profile files and tests agreed by coordinator; no shared CI workflow edits.

## Handoff

Unassigned. Coordinator checks current claims and source heads before assignment.

