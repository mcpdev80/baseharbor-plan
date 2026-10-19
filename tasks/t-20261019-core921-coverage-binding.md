---
id: t-20261019-core921-coverage-binding
type: task
areas: [ci]
release: v0.4.26
version: ""
parent: ""
owner: Flash (codeman w1-baseharbor)
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261019-core921-coverage-binding · CI: bind reviewed core-921 registration coverage #task #release/v0-4-26 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Flash (codeman w1-baseharbor)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Trusted PR gate planning resolves coverage for the independently reviewed core-921 registration candidate `756b22dc8967d0daa7393065cd5bc15f262c7050` by an exact reviewed-bundle binding, so PR #998 can reach a green mandatory final check without any prefix or directory exemption.

## Scope

- In scope: one exact-match clause in `scripts/pr-gate-plan.py` binding the complete 13-file changed-status set of `origin/develop...756b22dc8967d0daa7393065cd5bc15f262c7050` to reviewed head `756b22dc8967d0daa7393065cd5bc15f262c7050` with the same `core752_reviewed_merge_chain` guard used by the merged #974/#991 clauses, requiring `CI_CHECKS` plus `DOC_CHECKS` for the six reference docs; matching test additions in `scripts/test_pr_gate_plan.py`.
- Out of scope: any change to #998's product code, parser behavior, enforcement pin handling, or other reviewed bundles.

## Acceptance

- The new clause fires only on the exact path set, exact per-path statuses, exact reviewed head, and a clean trusted-base merge chain; every other combination still reports unresolved.
- `python3 scripts/test_pr_gate_plan.py` and `scripts/test_pr_check_runner.py` pass; negative regression proves a mutated path/status/head does not resolve coverage.
- Independent review of this CI-owner change precedes merge; after merge, #998's rerun selected checks resolve coverage.

## Required checks

- `python3 -m py_compile scripts/pr-gate-plan.py scripts/test_pr_gate_plan.py`
- `python3 scripts/test_pr_gate_plan.py`
- `python3 scripts/test_pr_check_runner.py`

## Dependencies and file ownership

- Owned files or areas: `scripts/pr-gate-plan.py`, `scripts/test_pr_gate_plan.py`
- Shared files: coordinate through the owning task.

## Handoff

### 2026-10-19 — PAUSED: BaseHarbor CI stabilization (coordinator hold)

- Controlled development pause ordered by Marcel; infrastructure prerequisite (GC evidence preservation) fixed via merged #999/#1000, but trusted gates still block: `integration_sha_mismatch` (#995/#985 lane) and `coverage-unresolved` needing exact reviewed-bundle qualification (#998/#993/#990/#989). No CI reruns, no correction loops, no merges during the pause.
- State at halt: worker o1 (b70198fc) implemented the CORE_921 exact-match clause + tests UNCOMMITTED on branch work/ci-core921-coverage-binding (base f2bad5ef; develop has advanced to include #999/#1000 — rebase after resumption). No commit, no push, no PR. Snapshot: evidence/board-2026-10-19/o1-binding-pause-note.md.
- Resume point: rebase onto post-#1000 develop, complete `test_pr_gate_plan.py` negatives, commit, push, PR against develop, independent review, then rerun #998 selected checks.

- Created 2026-10-19 from the o1 core-921 review diagnosis (evidence/board-2026-10-19/o1-core921-review.md Round 2): the #974 bootstrap binds only its six test/CI files; the nine registration production paths land in the mixed-unresolved handler or match no handler, so #998 cannot resolve coverage without this develop-side binding clause. No PR yet.
