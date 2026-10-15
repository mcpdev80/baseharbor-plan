---
id: core-941
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: mcpdev80 (session 2)
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#941"]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-941 · CI: correct PR impact selection and unresolved coverage #task #release/v0-4-26 #status/active

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

- Claimed by session 2 for a separate bounded correction PR. Review evidence and remaining consumer work to follow.
