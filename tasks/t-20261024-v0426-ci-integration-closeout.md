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

## Owner-authorized parallel closeout — 2026-10-24

Marcel explicitly requested parallel completion of v0.4.26. The coordinator delegates disjoint slices within this closeout assignment; existing session-2/session-3 claims and commits remain preserved. Root remains the sole Core CI writer and product merger.

- Native cleanup implementation: Codex /root/native_cleanup, existing Demo #121 only, owns scripts/failure-runtime-diagnostics.sh and its focused tests. Repair the observed Podman cleanup timeout from run 40110974339; no ownership bypass or speculative pins. Coordinate publication through root before changing the remote. This is an explicit bounded assignment alongside the existing native acceptance session, not takeover of its evidence claim.
- Consumer preparation: Codex /root/consumer_freeze, read-only inventory and independently executable preparation; actual D/U/K pins wait for predecessor merges. No concurrent writes to session-2 files.
- Independent source/evidence review: Codex /root/independent_review, read-only product review in separate trees; no implementation changes. Existing session-3 evidence stays authoritative for its exact reviewed sources.

## Dependencies and file ownership

- Owned implementation: scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py, scripts/pr-check-runner.py and directly affected CI tests/bindings within the named chain; no concurrent writer.
- Shared Planning views are rendered from current main and published with concurrent work preserved. Native and independent-review evidence remain with their separate sessions.

## Handoff

- 2026-10-24 current checkpoint: #1064 source e7fe45cc was independently approved in ROUND2 and merged as develop 133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f with green required CI. #1060 integrated that target in manually resolved review anchor 7e08fe920d3f62219a3923669896c601eb43ae96 (tree 3146cab0be56997e527758aa00f038a21b454c59); both full planner matrices preserved, 121 planner tests passed. Fresh independent review and separate trusted-target record precede required CI. Native run 40110974339 completed FAILURE: backup/restore passed, acceptance cleanup preparation timed out (artifact 12567701307 scope-result.json: TimeoutExpired); later workflow cleanup succeeded. No valid fresh Podman receipt or release readiness is claimed.

- 2026-10-24: [Current session-1 evidence](../evidence/ci-integration-2026-10-24/HANDOFF.md). Published replacement #1064 `e7fe45ccb3c2103bb3b57ad3300892b932818934` has green required CI 40110621660; fresh independent review is pending. Corrected #1060 `db79f24a39ccc1a6f8f38a13d20dd18ab151abc2` has green selected component checks in 40110759871 but final coverage remains blocked until reviewed target-side qualification. All 21 actual #1052 bootstrap/retry unit tests passed through the corrected strict helper; no native success is inferred. #1056 preparation is preserved locally at `ad3e4d2f` and is not yet published. Owner started exact Podman receipt run 40110974339; session 2 owns its acceptance. No merges/tags/releases/deployments or v0.4.27 changes.

- 2026-10-24: takeover from HANDOFF at planning 78dc7b5. #1064 head 54dfa458528e958be0ea3d8157a46bd501e76eb1 has green mandatory CI run 40108385755; independent review pending in session 3. develop is 65aa063e90767c85af976081c100be1817370e67. #1056 green CI does not resolve its reported bootstrap/DAG-origin review findings. Local checkout: /workspace/scratch/754a78dce362/baseharbor-ci. No merge or runtime execution yet.
