---
id: t-20261022-r27-evidence-acceptance
card_number: "0427-066"
card_short_title: "Accept the automatic receipt"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: flash-coordinator + o145 (W5 independent)
kanban_lane: closed
kanban_summary: ""
kanban_status: closed
kanban_title: "0427-066 · Accept the automatic receipt"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1151]
sha: 4f0ce579
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261103-ci-plain-checks
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1151", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/public-contracts/41021394575-1.json"]
---

- [x] t-20261022-r27-evidence-acceptance · Historical: Accept the automatic receipt chain, not partial jobs #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** flash-coordinator + o145 (W5 independent) · **Priority:** critical  
    **PR:** [baseharbor#1151](https://github.com/mcpdev80/baseharbor/pull/1151)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1151), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/public-contracts/41021394575-1.json)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** flash-coordinator + o145 (W5 independent)  
**Priority:** critical  
**PRs:** [baseharbor#1151](https://github.com/mcpdev80/baseharbor/pull/1151)  
**Source:** 
<!-- /generated:links -->

## Superseded by Owner instruction — 2026-11-03

This task describes the retired receipt/evidence implementation. It is closed as **superseded**, not accepted as a current prerequisite. The Owner requires ordinary CI, Pre-Release and Release jobs without gate manifests, completed-run/job re-verification, evidence reuse, separate receipt approval or shadow consumption. The sole CI record contains merge commit SHA and PR number.

Current implementation and acceptance are tracked in [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md). No historical PASS, pilot or approval satisfies its remaining checks. Existing receipts and release records remain historical data; no release or tag is authorized.

## Historical scope and results

The [original task at the pre-simplification Planning revision](https://github.com/mcpdev80/baseharbor-plan/blob/6a687317d2540106a0ff790d78e5ea05ab84a178/tasks/t-20261022-r27-evidence-acceptance.md) preserves the former criteria, owners, PRs and results. Do not resume that workflow or reinstate its dependencies.
