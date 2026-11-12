---
id: t-20261109-0427-183-repository-workload-ci-rot
card_number: "0427-183"
card_short_title: "Repository workload CI rot"
type: bug
areas: []
release: v0.4.27
version: ""
parent: v0.4.27
owner: mcpdev80 (Maintainer accepted)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0427-183 · Repository workload CI rot
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/42690054408", "https://github.com/mcpdev80/baseharbor/actions/runs/43288025038"]
---

- [x] t-20261109-0427-183-repository-workload-ci-rot · 0427-183 · Repository lifecycle/compose CI tests fail on develop head #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 (Maintainer accepted)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/42690054408), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/43288025038)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** mcpdev80 (Maintainer accepted)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task Note
Counter-probe (workflow_dispatch on refs/heads/develop d2e225f20, run 42690054408, job "Run runtime integration tests serially", 20:20:2xZ) fails 5 repository lifecycle/compose cells: TestRepositoryBuildWorkloadRebuildsSourceChangesInCI, TestRepositoryComposePinnedWorkloadLifecycleInCI, TestRepositoryComposeWorkloadOnlyLifecycleInCI, TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI, TestRepositoryWorkflowRealLifecycle. Same w169/deployment-state family as 0427-181/182 but on the CURRENT develop head — every PR-side go-test run that executes these serial cells is blocked. Nucleus to find: which of today's landed chains (damaged-state 230221700 / app-list 8a2912c62 / reclaim 82c15567c / isolate d9bf3d94e) changed the repository-workload assumptions.

## Owner closure — 2026-11-13

Owner closure: accepted 2026-11-13. The failing develop counter-probe is retained as historical evidence; later integrated PR CI is green. The exact five serial integration test names were not independently reproduced in the retained current run logs, so this closure records Maintainer acceptance/triage and does not claim a rerun of those exact tests.
