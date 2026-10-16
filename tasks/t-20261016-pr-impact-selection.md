---
id: t-20261016-pr-impact-selection
areas: [ci]
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
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/942", "https://github.com/mcpdev80/baseharbor/commit/14d864dfd38801a56e54901ea520f3b02db134b2", "https://github.com/mcpdev80/baseharbor/actions/runs/38821273254", "https://github.com/mcpdev80/baseharbor/actions/runs/38828055047", "https://github.com/mcpdev80/baseharbor/actions/runs/38882179679"]
---

- [x] t-20261016-pr-impact-selection · CI: correct PR impact selection and unresolved coverage #task #release/v0-4-26 #status/closed #view/closed #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (session 2) · **Priority:** high  
    **PR:** [baseharbor#942](https://github.com/mcpdev80/baseharbor/pull/942)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/942), [proof 2](https://github.com/mcpdev80/baseharbor/commit/14d864dfd38801a56e54901ea520f3b02db134b2), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/38821273254), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/38828055047), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/38882179679)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Owner:** mcpdev80 (session 2)  
**Priority:** high  
**PRs:** [baseharbor#942](https://github.com/mcpdev80/baseharbor/pull/942)  
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

- 2026-10-16 Maintainer-requested independent closeout of **t-20261016-pr-impact-selection — targeted PR impact selection**: rechecked product PR #942 is MERGED at `14d864dfd38801a56e54901ea520f3b02db134b2`, exact reviewed source `4e13aa58a2007fe6c1d847621ced67739f2f0c33`. [Actions 38821273254](https://github.com/mcpdev80/baseharbor/actions/runs/38821273254), job `Exact PR planner tests`, SUCCESS. The former core-893 consumer handoff is complete: PR #930 is integrated and accepted, with real selected-check enforcement qualified in run `38828055047`; current permanent five-check inspection selection was additionally exercised end-to-end in run `38882179679` and product PR #935 is merged. Unknown impact still fails closed and no complete release matrix is selected automatically. ACCEPTED/CLOSED; prior review-only handoffs below are historical, not current blockers.

- 2026-10-16 — **Further bounded review correction:** Draft PR #942 exact source `4e13aa58a2007fe6c1d847621ced67739f2f0c33` limits resolved `internal/capability/` to audited package conformance test files with mandatory `go test ./internal/capability/... -count=1`. All `internal/application/` and non-allowlisted capability implementation, registry/provider and lifecycle paths remain unresolved; all `deploy/docker/**` paths require explicit native qualification rather than merely Docker lifecycle. Negative regression cases cover resolver, registry, lifecycle, backup, security and deployment scripts. Focused immutable-source pilot [Actions 38821273254](https://github.com/mcpdev80/baseharbor/actions/runs/38821273254) verifies the change (**SUCCESS**: 17 planner regressions, actual capability package tests, CLI guided test/vet/build, and 68 evidence/verifier regressions). No core-893-owned source changes, no automatic matrix, no merge.


- 2026-10-16 — **Correction verification follow-up:** PR #942 source `3a56655669b6ec7850c0ef585715399ef0959bd0` now uses `PYTHONPATH=scripts` for actual pre-release/evidence verifier suites. The prior command pilot [38820297125](https://github.com/mcpdev80/baseharbor/actions/runs/38820297125) compiled/vetted/built the CLI but exposed a Python test import error; it is preserved as a failure, not called PASS. Its fixed exact-source pilot is [38820498868](https://github.com/mcpdev80/baseharbor/actions/runs/38820498868); **SUCCESS**: immutable checkout, Python syntax, all 15 planner tests, CLI test/vet/build and **68 actual verifier regressions PASS**. The earlier failure remains preserved, and the isolated pilot remains unmerged. No workflow/final-check edits to core-893.

- 2026-10-16 — **Review correction** for [Draft PR #942](https://github.com/mcpdev80/baseharbor/pull/942): exact source `7aac0149d0cd5bafcc8a2affcf1f9edc5f4fe085`. The planner now resolves only the audited guided read-only CLI adapter with `cmd/baha` targeted test, vet and build checks; backup/restore, mutating CLI and unrecognized CLI paths fail closed as unresolved pending specific native qualification. Only audited planning scripts and Pages documentation workflow resolve without native gates. Runtime execution, GC, release and evidence workflows plus CI executor scripts require the existing policy/planner/verifier checks and are **unresolved** until justified native evidence exists. [GitHub Actions 38820255412](https://github.com/mcpdev80/baseharbor/actions/runs/38820255412) PASS for immutable source, Python syntax and **15 focused regressions**, including adversarial CLI/workflow impact coverage. A separate command-execution pilot is [run 38820297125](https://github.com/mcpdev80/baseharbor/actions/runs/38820297125). core-893 must consume `coverage_status` and enforce any unresolved coverage; do not edit its workflow or mark #893 accepted. No merge.

- 2026-10-16 — **Review handoff (not accepted)**: [BaseHarbor Draft PR #942](https://github.com/mcpdev80/baseharbor/pull/942), exact source `3b6ad3f326f1641d8ce633bec169a8d88944508f`. [Actions 38819610962](https://github.com/mcpdev80/baseharbor/actions/runs/38819610962) `Exact PR planner tests` PASS: Python syntax, 11 focused tests (including actual 65-gate catalog, docs requiring validations with zero release gates, code/CI/native scoped mappings, malformed inputs, rename/delete, immutable revisions and unknown fail-closed). Actual existing executor/verifier test commands are specified, not placeholders. Temporary isolated pilot workflow is not part of PR #942 and is not to be merged. Output `coverage_status` / `unresolved_coverage` is defined in [consumer contract](https://github.com/mcpdev80/baseharbor/blob/3b6ad3f326f1641d8ce633bec169a8d88944508f/docs/internal/pr-impact-selection-contract.md). **Integration remains open**: core-893 must independently adopt and review the explicit fail-closed coverage and zero-native-gates consumer semantics in its owned workflow/final-check code. No #893 workflow edit, runtime matrix, release evidence alteration, merge or release.
- Claimed by session 2 for [BaseHarbor #941](https://github.com/mcpdev80/baseharbor/issues/941) and a separate bounded correction PR. Review evidence and remaining consumer work to follow.
