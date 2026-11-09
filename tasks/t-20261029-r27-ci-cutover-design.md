---
id: t-20261029-r27-ci-cutover-design
card_number: "0427-083"
card_short_title: "CI: specify candidate-bound"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "q201 (38460858, qwen)"
kanban_lane: closed
kanban_summary: ""
kanban_status: closed
kanban_title: "0427-083 · CI: specify candidate-bound"
early: true
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261103-ci-plain-checks
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-29/scripts/ruleset-activation/README-activation.md"]
---

- [x] t-20261029-r27-ci-cutover-design · Historical: CI: specify candidate-bound completion and ruleset #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** q201 (38460858, qwen) · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-29/scripts/ruleset-activation/README-activation.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** q201 (38460858, qwen)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Superseded by Owner instruction — 2026-11-03

This task describes the retired receipt/evidence implementation. It is closed as **superseded**, not accepted as a current prerequisite. The Owner requires ordinary CI, Pre-Release and Release jobs without gate manifests, completed-run/job re-verification, evidence reuse, separate receipt approval or shadow consumption. The sole CI record contains merge commit SHA and PR number.

Current implementation and acceptance are tracked in [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md). No historical PASS, pilot or approval satisfies its remaining checks. Existing receipts and release records remain historical data; no release or tag is authorized.

## Historical scope and results

The [original task at the pre-simplification Planning revision](https://github.com/mcpdev80/baseharbor-plan/blob/6a687317d2540106a0ff790d78e5ea05ab84a178/tasks/t-20261029-r27-ci-cutover-design.md) preserves the former criteria, owners, PRs and results. Do not resume that workflow or reinstate its dependencies.
