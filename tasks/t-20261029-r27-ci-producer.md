---
id: t-20261029-r27-ci-producer
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "q202 (a71d5cd0, qwen)"
early: true
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1199", "mcpdev80/baseharbor#1203", "mcpdev80/baseharbor#1207"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261029-r27-ci-producer · CI: qualify a real public-contracts producer #task #release/v0-4-27 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** q202 (a71d5cd0, qwen) · **Priority:** high  
    **PR:** [baseharbor#1199](https://github.com/mcpdev80/baseharbor/pull/1199), [baseharbor#1203](https://github.com/mcpdev80/baseharbor/pull/1203), [baseharbor#1207](https://github.com/mcpdev80/baseharbor/pull/1207)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** q202 (a71d5cd0, qwen)  
**Priority:** high  
**PRs:** [baseharbor#1199](https://github.com/mcpdev80/baseharbor/pull/1199), [baseharbor#1203](https://github.com/mcpdev80/baseharbor/pull/1203), [baseharbor#1207](https://github.com/mcpdev80/baseharbor/pull/1207)  
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

Lane q202 delivered producer-diagnostics.md (END q202-DONE, disk-verified, sanitized). Verified: #1199 (head 96a96362, merge 7a4debcc, run 40833893562) executed integration/static/public-contracts on integration_sha 8515e627 with trusted-pr-plan artifact and tree parity; post-run writer fired automatically but failed closed at publication because the token was absent in that run context (repo secret now verified present via gh api — requalification of a NEW producer run required to prove automatic publication). Evidence: https://github.com/mcpdev80/baseharbor-plan/blob/HEAD/evidence/r27-ci-replacement-2026-10-29/producer-diagnostics.md

