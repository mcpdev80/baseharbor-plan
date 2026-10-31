---
id: t-20261024-r27-candidate-trigger-prototype
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "ChatGPT (isolated v0.4.27 prototype)"
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-acceptance]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1055]
sources: []
early: false
blocker: ""
resolution: superseded
superseded_by: t-20261029-r27-ci-producer
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1055"]
---

- [x] t-20261024-r27-candidate-trigger-prototype · Deferred explicit candidate-trigger policy (after skeleton) #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (isolated v0.4.27 prototype) · **Priority:** high  
    **PR:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1055)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** ChatGPT (isolated v0.4.27 prototype)  
**Priority:** high  
**PRs:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
**Source:** 
<!-- /generated:links -->

# Deferred explicit candidate-trigger policy (after skeleton)

## Outcome and timing
Preserve the original requirement for explicit candidate submission instead of indiscriminate CI churn. This is a later bounded trigger-policy task, not permission to alter active legacy triggers while fixing receipt publication. Do not blindly merge old #1055 or its skip-as-success behavior.

## Three-slot routing after prerequisites
Coordinator reserves a concrete ready slice: W1 trusted mapping/request binding, W2 explicit dispatch wiring, W3 stale/pending/skipped-result negatives. Three total slots across all CI work; current W1/W2/W3 receipt work has priority. Preserve existing branch/source and hand off rather than starting duplicate work.

## Preconditions and acceptance
Accepted automatic skeleton and required-check semantics; source/ref/actor and exact candidate binding reviewed. Missing/skip/fail must not become PASS. Same ordinary path for human and agent; smallest positive/negative trigger checks, no generic flag framework, full runtime matrix or new evidence authority. Coordinator fixes exact files and interfaces before later assignment.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman is resumed by the Owner; the coordinator preserves claims and unpublished work and assigns small non-overlapping iterations under the current order. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261024-r27-candidate-trigger-prototype.md) remain immutable history, not competing operational instructions.
