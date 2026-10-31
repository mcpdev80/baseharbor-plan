---
id: t-20261023-appid-repo-workflow-proof
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: ""
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1055"]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1055"]
---

- [ ] t-20261023-appid-repo-workflow-proof · prove native TestRepositoryWorkflowRealLifecycle on final develop head #task #release/v0-4-27 #status/planned #view/queued #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **PR:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
    **Later release** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1055)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** queued  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
**Source:** 
<!-- /generated:links -->

## Goal

Prove `TestRepositoryWorkflowRealLifecycle` passes as an actual native Docker GitHub Actions lifecycle on the final develop head (exact candidate SHA), closing the gap that #1008/#1029 fixture work and #1047's planner lane leave unproven: the named repository lifecycle receipt on develop.

## Scope

- In scope: locate an authentic `TestRepositoryWorkflowRealLifecycle` PASS for a fixed develop SHA in GitHub Actions; if none is retrievable, select the smallest existing Docker acceptance workflow that truly executes that named lifecycle on the fixed candidate through its supported trigger; bind the receipt to exact source SHA, run/attempt, source/image/binary identity and owned cleanup.
- Out of scope: the app.id parser fixture correction (t-20261020), the #1047 CI-planner lane, and the environment-dependency caveat for the provider-registry test.

## Acceptance

- Named `TestRepositoryWorkflowRealLifecycle` PASS receipt on a fixed develop candidate head in GitHub Actions, bound to full candidate SHA, run/attempt and source identity.
- Receipt is an actual native lifecycle run, not a skipped test, an unrelated Selected Check, a static scope regression, or a source SHA other than the fixed candidate.
- Exact source integrity for that SHA (SHA256 of `cmd/baha/app_repository_integration_test.go` and the runtime fixture); no CI-green substitution, no owner/permission waiver.

## Required checks

- GitHub Actions run + check-run receipts for the exact candidate SHA via authenticated API (or the smallest existing Docker acceptance workflow that executes the named lifecycle on that SHA through its supported trigger).
- `git show`/ancestry confirmation that the candidate SHA is the reviewed/frozen develop head; no switch or edit of any unrelated worktree during retrieval.

## Dependencies and file ownership

- Depends on release-start cleanup/updates (t-20261017-release-0-4-27-updates); no product file ownership yet — no implementation, only evidence retrieval or a CI workflow selection.
- Shared: the develop candidate SHA is owned by the integration lane; do not rewrite it to force a receipt.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- 2026-10-24 (o113): state remains waiting; v0.4.27 release-start updates unaccepted. CI-explicit-candidate-trigger #1055 is an unqualified draft PR (head work/ci-explicit-candidate-trigger-20261024) in the develop merge window; no acceptance is recorded. Resolution documented here only because the schema forbids a free-text resolution field on a non-checked card.
- Defect handoff from APPID-R2 recipe point 3 (`evidence/board-2026-10-23/codex-verdict-reviewwave.md`): `TestRepositoryWorkflowRealLifecycle` (fixture `cmd/baha/app_repository_integration_test.go:16`) SKIPS without `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` or a resolvable runtime; the mandatory-native scope check (`cmd/baha/repository_runtime_fixture_test.go:411`) is static YAML/test-name counting, not execution. Historic run IDs 39619782116 / 39627285799 / 39831982468 return HTTP 404 or run only static MCP with runtime skipped, so the required receipt is unverifiable from outside. F27 review on 2026-10-23 (live checks 17:07–17:15 UTC, authenticated `mcpdev80`) confirms develop `1861ed07888a1ec22c218ca491d23ee54f48e261`, Planning `c41cd2cf5d9d2ed7ba18bc346c0cd1ee4f2148e8`; PRs #1008 (`8a40e60a…`) and #1029 (`30e112431b04a7e24e7e7e9ea76a3600e439a988`) are merged and ancestors of develop, but no open APPID native-lifecycle PR exists. Positive owned-path case and negative foreign-owner/unsafe-permission cases are required; do not add skip-if-unverifiable or weaken the production ownership guard. This is a separate task, not a prerequisite for accepting the app.id parser fixture.
- Recipe point 4: after the retrievable receipt and exact-source reviews are attached and all acceptance criteria are mapped, run Planning render/check and publish through the existing owner protocol; no product merge is needed for the already-integrated fixture.
