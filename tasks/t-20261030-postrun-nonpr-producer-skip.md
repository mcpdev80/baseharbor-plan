---
id: t-20261030-postrun-nonpr-producer-skip
card_number: "0427-090"
card_short_title: "Receipt Post-Run fails on"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: q260
kanban_lane: closed
kanban_summary: ""
kanban_status: closed
kanban_title: "0427-090 · Receipt Post-Run fails on"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1230]
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261103-ci-plain-checks
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-30/q260.md]
---

- [x] t-20261030-postrun-nonpr-producer-skip · Historical: Receipt Post-Run fails on non-PR producer runs (runtime-validation pushes) instead of clean skip #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** q260  
    **PR:** [baseharbor#1230](https://github.com/mcpdev80/baseharbor/pull/1230)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-30/q260.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** q260  
**Priority:** not set  
**PRs:** [baseharbor#1230](https://github.com/mcpdev80/baseharbor/pull/1230)  
**Source:** 
<!-- /generated:links -->

## Superseded by Owner instruction — 2026-11-03

The old post-run artifact/extractor/verifier path is retired. CI, Pre-Release and Release use normal required jobs without gate manifests, evidence verification/reuse or extra receipt approval. The only CI record contains merge SHA and PR number. No new implementation is required under this historical card.

Replacement and its still-pending acceptance: [CI simplification](t-20261103-ci-plain-checks.md). Actual safe-publication tests for the minimal writer remain part of that implementation; this does not remove error handling for rejected pushes or conflicting records.

## Historical scope and results

[Original task](https://github.com/mcpdev80/baseharbor-plan/blob/6a687317d2540106a0ff790d78e5ea05ab84a178/tasks/t-20261030-postrun-nonpr-producer-skip.md). Existing historical data is preserved; no release or tag is authorized.
