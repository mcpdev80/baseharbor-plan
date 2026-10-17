---
id: core-900
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: mcpdev80 (session 2)
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#931"]
sources: ["mcpdev80/baseharbor#900"]
source_updated: "2026-10-15T19:49:39Z"
labels: [area/evidence]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/931", "https://github.com/mcpdev80/baseharbor/actions/runs/38800898245"]
---

- [x] core-900 · GC: preserve active PRs, candidates and evidence origins #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (session 2)  
    **PR:** [baseharbor#931](https://github.com/mcpdev80/baseharbor/pull/931)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/931), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/38800898245)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** none  
**Required by:** [core-901](core-901-pilot-verify-parallel-task-prs-ci-costs.md), [core-922](core-922-docs-new-edit-provider-selection.md), [core-923](core-923-acceptance-new-edit-journeys-consumers.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (session 2)  
**Priority:** not set  
**PRs:** [baseharbor#931](https://github.com/mcpdev80/baseharbor/pull/931)  
**Source:** [baseharbor#900](https://github.com/mcpdev80/baseharbor/issues/900)
<!-- /generated:links -->

## Goal

Cleanup removes no reference or evidence the new workflow still needs.

## Scope

- In scope: the existing artifact/branch GC authority and focused dry-run tests.
- Out of scope: PR #930, CI/runner execution, the evidence verifier, production deletion.

## Acceptance

- Open task PRs, active candidate lines and approved source refs are protected.
- Original evidence stays authenticatable until the end of its use/retention; expired evidence is not treated as valid.
- Closed/inactive data is still cleaned under the existing explicit policy; no blanket unlimited retention.
- Failed discovery fails closed.

## Required checks

- GC dry-run/fixtures for open, closed, active candidate and evidence origin; no real deletions for qualification.

## Dependencies and file ownership

- Satisfied: #899 (closed as completed 2026-10-15).

## Handoff

- 2026-10-16 Maintainer-authorized closeout: Accepted integrated GC protection PR #931 (`bf69ad0a37fcec12958992d4826e4f8d14c13ba6`). Rechecked [Actions 38800898245](https://github.com/mcpdev80/baseharbor/actions/runs/38800898245): GC tests SUCCESS; productive deletion jobs SKIPPED. Acceptance covers tested SHA-aware retention, pagination and fail-closed behavior; no productive deletion was performed.

- 2026-10-15T20:32Z: PR #931 merged into develop (merge commit `bf69ad0a37fcec12958992d4826e4f8d14c13ba6`). The issue is still open; a merged PR is not acceptance — awaiting Maintainer acceptance with evidence.
- 2026-10-15: session 2 owns #900 only, on a dedicated branch against develop. Draft PR #931 ("retain active sources and evidence origins"), head `0459ae9411` at snapshot time.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
