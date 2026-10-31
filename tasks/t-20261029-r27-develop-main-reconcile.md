---
id: t-20261029-r27-develop-main-reconcile
type: task
areas: [ci]
release: v0.4.27
status: closed
parent: v0.4.27
owner: "o217 (d2ee29b3, ornith; Handoff von q207 nach 2 Fehlschlaegen, Strategy-Change gemaess rv1206C)"
early: true
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1206]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1206","https://github.com/mcpdev80/baseharbor/pull/1214","https://github.com/mcpdev80/baseharbor/pull/1218"]
---

- [x] t-20261029-r27-develop-main-reconcile · CI: forward-port main-only hardening back to develop #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** o217 (d2ee29b3, ornith; Handoff von q207 nach 2 Fehlschlaegen, Strategy-Change gemaess rv1206C) · **Priority:** high  
    **PR:** [baseharbor#1206](https://github.com/mcpdev80/baseharbor/pull/1206)  
    **Needs:** t-20261017-release-0-4-27-updates  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1206), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1214), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1218)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** t-20261017-release-0-4-27-updates  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** o217 (d2ee29b3, ornith; Handoff von q207 nach 2 Fehlschlaegen, Strategy-Change gemaess rv1206C)  
**Priority:** high  
**PRs:** [baseharbor#1206](https://github.com/mcpdev80/baseharbor/pull/1206)  
**Source:** 
<!-- /generated:links -->

## Goal

Make develop a strict superset of main's CI hardening so promotion is lossless

## Scope

Root cause (codex-rv1205 finding 1): CI fixes #1193-#1198 landed main-only and were never forward-ported. Port main's hardening (tasklink GITHUB_TOKEN, GH_WORKFLOW_TOKEN plan_commit env, writer --product wiring abf4d075, pin bump d92c1654, witness GH_TOKEN 7a417d37) onto develop without losing develop's newer chain content (#1200 vars pin, #1201 write-token env, #1202 pins/GH_TOKEN). PR base=develop; merge via Codex path. Afterwards refresh PR #1205 head to the reconciled develop tip.

## Acceptance

PRÜFUNG AM FINALEN MERGE-ERGEBNIS (Owner-Direktive 2026-10-29, ersetzt merge-tree-main->develop-Klausel): #1205 ist nach Synchronisierung mit main konfliktfrei promotierbar (Branch-Sync-Beweis: commit-tree-Simulation S/M2, merge-tree main×M2 exit 0, diff main..M2 ohne Minus-Zeilen der main-Härtungen GH_WORKFLOW_TOKEN/--product/run_attempt/pull_requests); alle main-Härtungen und alle neueren develop-Änderungen bleiben erhalten (file:line table am finalen Kandidaten-Baum); gezielte Tests (unittest-Quartett, 73 Tests) am Kandidaten ausgeführt; geprüfte SHAs (Kandidat, develop-Tip, main-Tip, Simulationen) dokumentiert.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Exclusive: .github/workflows/receipt-post-run.yml, scripts/receipt_writer.py, scripts/receipt_tasklink.py + receipt focused tests (all currently owned by the postrun/verifier lineage - coordinator-sequenced; no overlap with contracts/ producer lanes).

## Handoff

Lane q207 (ae27e0da) dispatched 2026-10-29; PR number/head recorded on delivery.
