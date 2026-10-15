---
id: t-20261016-pr-impact-selection
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: mcpdev80 (session 2)
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#942"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261016-pr-impact-selection · CI: correct PR impact selection and unresolved coverage #task #release/v0-4-26 #status/review #view/active
    <!-- generated:card -->
    **Owner:** mcpdev80 (session 2) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Owner:** mcpdev80 (session 2)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Correct the existing #892 trusted diff-to-check planner without changing the #893 executor and final-check owners. This is a bounded prerequisite of [core-893](core-893-ci-enforce-selected-pr-checks.md).

## Scope

- In scope: `scripts/pr-gate-plan.py` and focused planner tests, an explicit non-broad unresolved output contract.
- Out of scope: #893 workflow, executor, verifier or release evidence semantics.

## Acceptance

- Docs-only changes select existing documentation validation checks with zero unrelated release gates.
- Known code and CI/evidence areas select justified checks and gates.
- Unknown, unverified, invalid or empty inputs fail closed through explicit unresolved coverage; never quietly select all release gates or exempt validation.
- Preserve exact diff commit identities, deleted/renamed path handling, trusted-base planning authority.
- Describe minimal #893 consumer adaptations; no self-exempting required checks.

## Required checks

- Focused planner tests including actual repo catalog, path/status adversarial fixtures; Python syntax; targeted unprivileged Actions execution on immutable source.

## Dependencies and file ownership

- Existing #892 planner only; coordinate interface with core-893 owner.
- No edits to core-893-owned CI workflow or final-check files.

## Handoff

- 2026-10-16 — **Review handoff (not accepted)**: [BaseHarbor Draft PR #942](https://github.com/mcpdev80/baseharbor/pull/942), exact source `4394edd2dc16805bf5c2663d141f3303c460ab21`. [Actions 38819462167](https://github.com/mcpdev80/baseharbor/actions/runs/38819462167) `Exact PR planner tests` PASS: Python syntax, 11 focused tests (including actual 65-gate catalog, docs requiring validations with zero release gates, code/CI/native scoped mappings, malformed inputs, rename/delete, immutable revisions and unknown fail-closed). Temporary isolated pilot workflow is not part of PR #942 and is not to be merged. Output `coverage_status` / `unresolved_coverage` is defined in [consumer contract](https://github.com/mcpdev80/baseharbor/blob/4394edd2dc16805bf5c2663d141f3303c460ab21/docs/internal/pr-impact-selection-contract.md). **Integration remains open**: core-893 must independently adopt and review the explicit fail-closed coverage and zero-native-gates consumer semantics in its owned workflow/final-check code. No #893 workflow edit, runtime matrix, release evidence alteration, merge or release.\n- Claimed by session 2 for [BaseHarbor #941](https://github.com/mcpdev80/baseharbor/issues/941) and a separate bounded correction PR. Review evidence and remaining consumer work to follow.
