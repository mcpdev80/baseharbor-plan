---
id: t-20261029-r27-develop-main-reconcile
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "o217 (d2ee29b3, ornith; Handoff von q207 nach 2 Fehlschlaegen, Strategy-Change gemaess rv1206C)"
early: true
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261029-r27-develop-main-reconcile · CI: forward-port main-only hardening back to develop #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** q207 (ae27e0da, qwen) · **Priority:** high  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** q207 (ae27e0da, qwen)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make develop a strict superset of main's CI hardening so promotion is lossless

## Scope

Root cause (codex-rv1205 finding 1): CI fixes #1193-#1198 landed main-only and were never forward-ported. Port main's hardening (tasklink GITHUB_TOKEN, GH_WORKFLOW_TOKEN plan_commit env, writer --product wiring abf4d075, pin bump d92c1654, witness GH_TOKEN 7a417d37) onto develop without losing develop's newer chain content (#1200 vars pin, #1201 write-token env, #1202 pins/GH_TOKEN). PR base=develop; merge via Codex path. Afterwards refresh PR #1205 head to the reconciled develop tip.

## Acceptance

Merge-base conflict gone (git merge-tree clean main->develop); every main hardening line present on develop (file:line table); focused receipt suites pass; #1205 promotable without deleting any main defense.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Exclusive: .github/workflows/receipt-post-run.yml, scripts/receipt_writer.py, scripts/receipt_tasklink.py + receipt focused tests (all currently owned by the postrun/verifier lineage - coordinator-sequenced; no overlap with contracts/ producer lanes).

## Handoff

Lane q207 (ae27e0da) dispatched 2026-10-29; PR number/head recorded on delivery.
