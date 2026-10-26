---
id: t-20261022-r27-evidence-contract
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: flash-f71 (worker-1 contract+legacy-bootstrap)
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1090]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-contract · evidence contract #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** flash-f71 (worker-1 contract+legacy-bootstrap) · **Priority:** critical  
    **PR:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-publisher](t-20261022-r27-evidence-publisher.md), [t-20261022-r27-evidence-resolver](t-20261022-r27-evidence-resolver.md)  
**Owner:** flash-f71 (worker-1 contract+legacy-bootstrap)  
**Priority:** critical  
**PRs:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090)  
**Source:** 
<!-- /generated:links -->


# Receipt contract: GitHub live witness, approved Git history

## Goal
One canonical JSON receipt per successful gate/run/attempt, strictly below 500 bytes. Six top-level fields: gate, run (id and attempt), sha (full tested candidate SHA), status (pass), plan (full Planning commit), approved (null or by/at/receipt_commit). No signatures, logs, artifact archive, retention service or second evidence authority.

## Scope and acceptance
- Pin gate details and source/integration inputs in the referenced Planning revision; never infer tested integration SHA from API head_sha alone.
- Receipt path: evidence/receipts/<gate>/<run>-<attempt>.json. Only one transition from approved:null to an authenticated Owner approval is allowed; all other bytes remain fixed.
- The live verifier authenticates repository, workflow, event, attempt, successful run AND named gate job, tested source binding and exact receipt bytes before approval.
- After approval, retained verification uses protected Git history and the applicable plan only; no GitHub API/run/artifact dependency.
- Existing legacy CI qualifies this bootstrap. A real positive receipt plus wrong-SHA, dead-run and edited-receipt rejection defines skeleton acceptance before cutover.
- Product source, tests and paired EN/DE docs ship together in PR 1. No production workflow changes in PR 1.

## Owner decision — 2026-10-26
Marcel explicitly replaced the earlier signed archive design with minimal receipts and authorized task reconciliation and implementation. This supersedes earlier signature/archive requirements for the five evidence stories; it does not accept any implementation or prerequisite.

Source assignment: <https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md> (three concurrent worker packages; coordinator owns integration).
