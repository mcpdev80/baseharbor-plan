---
id: t-20261029-r27-writer-selftest-job
card_number: "0427-088"
card_short_title: "CI: writer selftest job —"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: ""
kanban_lane: closed
kanban_summary: ""
kanban_status: closed
kanban_title: "0427-088 · CI: writer selftest job —"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261103-ci-plain-checks
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261103-ci-plain-checks.md"]
---

- [x] t-20261029-r27-writer-selftest-job · Historical: CI: writer selftest job — validate plan.zip against extract_facts before any publication #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261103-ci-plain-checks.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Superseded by Owner instruction — 2026-11-03

The old post-run artifact/extractor/verifier path is retired. CI, Pre-Release and Release use normal required jobs without gate manifests, evidence verification/reuse or extra receipt approval. The only CI record contains merge SHA and PR number. No new implementation is required under this historical card.

Replacement and its still-pending acceptance: [CI simplification](t-20261103-ci-plain-checks.md). Actual safe-publication tests for the minimal writer remain part of that implementation; this does not remove error handling for rejected pushes or conflicting records.

## Historical scope and results

[Original task](https://github.com/mcpdev80/baseharbor-plan/blob/6a687317d2540106a0ff790d78e5ea05ab84a178/tasks/t-20261029-r27-writer-selftest-job.md). Existing historical data is preserved; no release or tag is authorized.
