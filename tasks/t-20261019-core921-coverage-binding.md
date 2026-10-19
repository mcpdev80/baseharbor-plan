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
prs: [mcpdev80/baseharbor#1007]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261019-core921-coverage-binding · CI: bind reviewed core-921 registration coverage #task #release/v0-4-26 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor) · **Priority:** high  
    **PR:** [baseharbor#1007](https://github.com/mcpdev80/baseharbor/pull/1007)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Flash (codeman w1-baseharbor)  
**Priority:** high  
**PRs:** [baseharbor#1007](https://github.com/mcpdev80/baseharbor/pull/1007)  
**Source:** 
<!-- /generated:links -->

## Goal

Trusted PR gate planning resolves coverage for the corrected, independently re-reviewed core-921 registration candidate by an exact complete source/file-status binding, so PR #998 can reach a green mandatory final check without any prefix or directory exemption. The initial source756b22dc8967d0daa7393065cd5bc15f262c7050 now has confirmed MCP source defects and must not be finally qualified as-is.

## Scope

- In scope: preserve the original exact-match implementation and negative tests, then bind the complete corrected independently reviewed source/file-status inventory using the existing trusted Git ancestry/integration proof. Select the actual registration/MCP/consent/CLI/docs/Public Contracts requirements. The original 13-file inventory at756b22dc is historical and must not authorize the source rejected in review5569055023.
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

### 2026-10-19 — Structural blocker found (r4): binding clause unreachable for linear heads; fix + re-pin to a66e5de6 delegated

- r4-planner-mode-analysis.md: pre-merge green was impossible for THIS PR because `core752_reviewed_merge_chain` requires a merge-anchored chain and #1007's head is linear (independent second bug: stale `base.sha` payload belongs to the CI owner, see ci-finding-integration-sha-mismatch.md).
- o12 implements #999-style fix (develop-merge into branch) or r4's option-B chain relaxation (with negative test), re-pins CORE_921 to a66e5de6, reproduces planner resolution locally BEFORE push.


### 2026-10-19 — Self-qualification independently APPROVED; awaiting #998 native SHA for final re-pin

- Independent read-only review of delta `706b5244..48def9e8` by a qwen3.6-laptop session (t20, verified model footer): **APPROVE** - BINDING_PR_1007 clause mirrors #999/#1005, CORE_921 block byte-identical, 84 planner tests pass, planner's pre-merge `unresolved` behavior correctly identified as merge-chain semantics (resolves for later runs once the clause is on develop), not a defect. Evidence: ecosystem `evidence/board-2026-10-19/o17-selfq-review.md`.
- Next: single consolidated Maintainer handoff for #1007 AFTER #998's native proof lands its final SHA (final CORE_921 re-pin included in that same head), avoiding duplicate CI cycles.


### 2026-10-19 — Self-qualification pushed: head `48def9e8`

- Worker o9 added the BINDING_PR_1007 self-qualification clause mirroring the merged #1005/#999 pattern (`core752_reviewed_merge_chain` ancestry, exact path/status pairs, emitted-check subTest); CORE_921 binding head `6931ba9c` and the 16-file #998 set untouched. Planner suite passes locally; pushed to `work/ci-core921-coverage-binding` (PR #1007 head `48def9e85e35db90025b4e354350bac22c9fe806`). Evidence: ecosystem `evidence/board-2026-10-19/o9-binding-repin.md` (## self-qualification).
- Independent local review of the self-qualification delta starts now; CI observation and Maintainer handoff follow per AGENTS.md step 7.


### 2026-10-19 — Independent review of 706b5244: APPROVE

- Worker o13 (session b7ed0ce6, read-only, sha256 before/after equal) independently approved the round-2 head `706b5244`: cli-gofmt plus all four coverage families present in the emitted required list; ancestry negatives run against the temporary repo; stubbed variant deleted; wrong-status-only negative real; all other clauses intact (84+18 tests). Evidence: ecosystem `evidence/board-2026-10-19/o13-1007-review.md`.
- Open: self-qualification clause for the PR's own `scripts/pr-check-runner.py` change (worker o9, cause budget round 1) and final re-pin of CORE_921_PRODUCTION_REVIEWED_HEAD to #998's post-native SHA.


### 2026-10-19 — Codex round 2 gate/negative fixes pushed; self-qualification running

- Head `706b5244`: cli-gofmt + four coverage families required in the emitted checks (reproduced), stubbed ancestry test deleted, real wrong-status-only negative added (84+18 planner/runner tests pass). Codex round-2 findings on these two causes were closed by this commit; independent review of this head running with worker o13.
- New independent cause found via CI: run 39267109503 fails with 'CI execution/evidence impact requires specific qualification: scripts/pr-check-runner.py' - #1007's own runner change needs the established self-qualification clause pattern (mirroring merged #1005/#999, not a new mechanism). Worker o9 implementing (fresh budget round 1). CORE_921_PRODUCTION_REVIEWED_HEAD remains 6931ba9c pending #998 native proof re-pin.

### 2026-10-19 — Binding finalized; PR #1007 open for develop

- Worker o1 (session b70198fc) delivered: develop integrated (bb91fbc3), clause `CORE_921_PRODUCTION_REVIEWED_HEAD = 08d8f498fd82992e762d764967ac892721d9adeb` with complete fifteen path/status pairs from the exact two-dot diff; #991/#1005/#974 and all accepted clauses preserved; positive/negative regressions pin the exact match. Branch head `417b8cbb03d585a2607663f44eb38c1c9e13250d`, PR #1007 non-draft.
- Full planner suites green (see `evidence/board-2026-10-19/o1-binding-final.md`). Independent review and merge are Maintainer actions.


### 2026-10-19 — Existing preparation active; final binding follows corrected source review

- Marcel reconfirmed controlled Codeman continuation. Existing Flash/o1 ownership remains ACTIVE for preserving/checkpointing original work, normal trusted-target integration and generic negative/executor tests. No external worker start is claimed by this remote status update.
- Final exact SHA/status publication waits for corrected independently reviewed #998 source. The source correction is now active and no longer lists this unfinished final binding as a hard implementation predecessor; no task/interface or required final qualification is falsely accepted.
- Preserve all current trusted bindings, including accepted #1005, and actual registration/MCP/CLI/docs/Public Contracts families. No rejected756b22dc source qualification, copied-tree ancestry shortcut or claim takeover.

### 2026-10-19 — Preserve original work; final binding waits for corrected MCP source

- The complete-release audit found source-blocking #998 defects in review5569055023. Existing Flash/core-921 owner must correct the MCP schema and typed-error boundary on its existing source branch and obtain a fresh independent full-source review.
- o1 may preserve/checkpoint its original two-file work and finish generic negative-test preparation, but must update the final exact source/status inventory to that corrected reviewed candidate; the old13-file/SHA scope below is historical, not permission to qualify the rejected source.
- Preserve the actual registration/MCP/consent/CLI/docs/Public Contracts requirements, not only CI_CHECKS+DOC_CHECKS. Integrate accepted #1001/#1002/#1003 and the disjoint #1005 SQL-layout qualification normally before publication; no competing CORE_921 implementation or local worktree mutation was made by the coordinator.

### 2026-10-19 — Controlled owner continuation authorized

- The [controlled resumption decision](../decisions/2026-10-19-ci-stabilization-controlled-resumption.md) supersedes the historical pause below. Flash/o1 retains the existing claim and two unpublished files; no competing CORE_921 binding was created.
- First action: inspect and checkpoint the protected dirty diff, then normally integrate current trusted develop (handoff baseline 7827e6491a7715e0ffffb1e7938764f6788cc30b), preserving accepted #1001/#1002/#1003 changes. No reset, force push or copied-tree ancestry shortcut. The old rebase instruction below is historical; use normal integration without rewriting published history.
- Finish exact source/status and genuine Git negatives, focused planner/runner/diff-base checks, publish on the existing branch and obtain separate independent review plus actual Required CI. Then continue existing #998 after policy acceptance. #995 native testing does not block this disjoint task.
- No worker restart or local coordinator-file edit has been performed by this remote coordinator; the local owner must consume the published handoff and resume its own preserved work.

### 2026-10-19 — PAUSED: BaseHarbor CI stabilization (coordinator hold)

- Controlled development pause ordered by Marcel; infrastructure prerequisite (GC evidence preservation) fixed via merged #999/#1000, but trusted gates still block: `integration_sha_mismatch` (#995/#985 lane) and `coverage-unresolved` needing exact reviewed-bundle qualification (#998/#993/#990/#989). No CI reruns, no correction loops, no merges during the pause.
- State at halt: worker o1 (b70198fc) implemented the CORE_921 exact-match clause + tests UNCOMMITTED on branch work/ci-core921-coverage-binding (base f2bad5ef; develop has advanced to include #999/#1000 — rebase after resumption). No commit, no push, no PR. Snapshot: evidence/board-2026-10-19/o1-binding-pause-note.md.
- Resume point: rebase onto post-#1000 develop, complete `test_pr_gate_plan.py` negatives, commit, push, PR against develop, independent review, then rerun #998 selected checks.

- Created 2026-10-19 from the o1 core-921 review diagnosis (evidence/board-2026-10-19/o1-core921-review.md Round 2): the #974 bootstrap binds only its six test/CI files; the nine registration production paths land in the mixed-unresolved handler or match no handler, so #998 cannot resolve coverage without this develop-side binding clause. No PR yet.
