---
id: t-20261024-v0426-ci-integration-closeout
type: task
areas: [ci]
release: v0.4.26
version: ""
parent: v0.4.26
owner: Codex (session 1 CI implementation and integration)
priority: critical
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1064", "mcpdev80/baseharbor#1060", "mcpdev80/baseharbor#1056", "mcpdev80/baseharbor#1052", "mcpdev80/baseharbor#1046"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261024-v0426-ci-integration-closeout · CI: finish serialized v0.4.26 qualification and integration #task #release/v0-4-26 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (session 1 CI implementation and integration) · **Priority:** critical  
    **PR:** [baseharbor#1064](https://github.com/mcpdev80/baseharbor/pull/1064), [baseharbor#1060](https://github.com/mcpdev80/baseharbor/pull/1060), [baseharbor#1056](https://github.com/mcpdev80/baseharbor/pull/1056), [baseharbor#1052](https://github.com/mcpdev80/baseharbor/pull/1052), [baseharbor#1046](https://github.com/mcpdev80/baseharbor/pull/1046)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (session 1 CI implementation and integration)  
**Priority:** critical  
**PRs:** [baseharbor#1064](https://github.com/mcpdev80/baseharbor/pull/1064), [baseharbor#1060](https://github.com/mcpdev80/baseharbor/pull/1060), [baseharbor#1056](https://github.com/mcpdev80/baseharbor/pull/1056), [baseharbor#1052](https://github.com/mcpdev80/baseharbor/pull/1052), [baseharbor#1046](https://github.com/mcpdev80/baseharbor/pull/1046)  
**Source:** 
<!-- /generated:links -->

## Goal

Complete the serialized v0.4.26 CI qualification chain and integrate verified candidates without changing v0.4.27 or publishing a release. Marcel assigned this session the implementation/integration role after the Codeman stop; two other sessions own native consumer acceptance and independent review.

## Scope

- In scope: #1064 prerequisite, #1060 qualification, #1052 integration, #1056 bootstrap/pins-data review corrections and #1046 qualification. Continue existing PRs and preserve saved work.
- Out of scope: native consumer fixtures/receipts (session 2), independent reviews and shared release-dossier reconciliation (session 3), v0.4.27 activation, tags, deployment and full pre-release.

## Acceptance

- Current exact candidates have source review, mandatory CI and recorded integration outcomes; known defects remain blocking until corrected.
- All planner writes are serialized. No fabricated native success, self-qualification or Required Check bypass.

## Required checks

- Focused planner/runner/resolver and existing executor/verifier regressions, workflow policy/syntax where affected, followed by the actual candidate's mandatory CI.

## Dependencies and file ownership

- Owned implementation: scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py, scripts/pr-check-runner.py and directly affected CI tests/bindings within the named chain; no concurrent writer.
- Shared Planning views are rendered from current main and published with concurrent work preserved. Native and independent-review evidence remain with their separate sessions.

## Handoff

- 2026-10-24: takeover from HANDOFF at planning 78dc7b5. #1064 head 54dfa458528e958be0ea3d8157a46bd501e76eb1 has green mandatory CI run 40108385755; independent review pending in session 3. develop is 65aa063e90767c85af976081c100be1817370e67. #1056 green CI does not resolve its reported bootstrap/DAG-origin review findings. Local checkout: /workspace/scratch/754a78dce362/baseharbor-ci. No merge or runtime execution yet.
