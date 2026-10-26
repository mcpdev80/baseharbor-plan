---
id: t-20261024-r27-ci-impact-prototype
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "ChatGPT (isolated v0.4.27 prototype)"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1051]
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261024-r27-ci-impact-prototype · CI: trusted impact qualification prototype #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (isolated v0.4.27 prototype) · **Priority:** high  
    **PR:** [baseharbor#1051](https://github.com/mcpdev80/baseharbor/pull/1051)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** ChatGPT (isolated v0.4.27 prototype)  
**Priority:** high  
**PRs:** [baseharbor#1051](https://github.com/mcpdev80/baseharbor/pull/1051)  
**Source:** 
<!-- /generated:links -->

## Binding three-worker execution — Owner instruction, 2026-10-26

Routing: **W1**. Use the [coordinator handoff](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md); it supersedes earlier five-worker or serialized implementation scheduling.

W1: exact impact mapping and trusted discovery. W2: compatibility of selected producer inputs and bounded fixtures. W3: changed-input/missing-coverage/false-green negatives. Preserve draft #1051 as historical preparation; do not silently accept or expand its old mapping.

Exactly three concurrent worker slots for all v0.4.27 CI work, plus the coordinator; never three additional workers on top of active claims. Existing owners/claims and completed commits are preserved. Coordinator hands over reservations explicitly and balances remaining effort, moving a bounded unfinished subtask or cross-review to a free worker rather than inventing work. No worker edits another worker's scripts, test file or workflow; common-branch pushes, Planning metadata and final integration have one coordinator writer.

Dependencies in frontmatter remain acceptance/readiness requirements, not blanket locks on the explicitly authorized isolated receipt preparation against frozen #1090 interfaces. Parallel preparation does not accept an unmerged dependency, change a shared interface unilaterally, or qualify a new domain. The first one-gate receipt skeleton must be accepted before live domain-gate expansion. Later domain implementation still requires its accepted product contracts, fixtures and release-start inputs; choose another actually ready task or report the concrete blocker if three safe work slices do not exist.

Do not alter active producer behavior or required-check enforcement before the accepted cutover. Preserve the legacy qualification route, use the smallest sufficient checks and batch candidates; no full matrix or duplicate green runs. Cross-review must be by another worker/coordinator and applies to the final integrated SHA.


# CI: trusted impact qualification prototype

## Goal
Review and test exact-path CI impact mapping without changing active v0.4.26 trusted CI.

## Scope
- Isolated design, review and regression preparation only on the existing draft PR.
- No merge to develop, no Ruleset or production workflow changes, no v0.4.26 interference.
- Do not treat prototype output as accepted trusted evidence.

## Acceptance
- Review rename/delete and out-of-scope path regressions; verify that no prototype test self-qualifies or bypasses conservative coverage.
- Final independent check and Owner-authorized rollout must follow v0.4.26 completion.

## Dependencies and file ownership
The v0.4.27 release-start updates remain unaccepted; this active status documents isolated work only, not production readiness. Existing PR #1051 remains draft. No ownership of other tasks or PRs is implied.

## Handoff
- 2026-10-24: isolated preparation in [PR #1051](https://github.com/mcpdev80/baseharbor/pull/1051); current status active, not qualified or mergeable by this card.

- Hugging Face independent execution on draft PR #1051 commit `c7352556e39d3c09a70609985382d00c4b7e4304`: [R27 exact-path planner 4/4 PASS](https://huggingface.co/jobs/ThunderHawk1080/6adbf710046eb82b1ecd8a4b). Other acceptance gates pending.

- 2026-10-24: full independent planner suite executed with git, Go and pinned PyYAML on isolated PR #1051 head `c7352556e39d3c09a70609985382d00c4b7e4304`: [99/99 tests PASS on Hugging Face](https://huggingface.co/jobs/ThunderHawk1080/6adc5167046eb82b1ecdaf58). Includes the exact-path prototype impact tests. No promotion or GitHub required-check qualification inferred from this offline run.
