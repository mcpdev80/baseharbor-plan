---
id: t-20261119-ci-fast-feedback
card_number: "0428-141"
card_short_title: "fast feedback with safe"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "Codex (CI fast feedback, current chat)"
kanban_status: active
kanban_lane: active
kanban_summary: Make CI failures faster to diagnose and give developers a local fast-feedback path. Let a PR add and exercise its own checks…
kanban_title: 0428-141 · fast feedback with safe
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1698]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261119-ci-fast-feedback · CI: fast feedback with safe PR-owned checks #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** Codex (CI fast feedback, current chat)  
    **PR:** [baseharbor#1698](https://github.com/mcpdev80/baseharbor/pull/1698)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex (CI fast feedback, current chat)  
**Priority:** not set  
**PRs:** [baseharbor#1698](https://github.com/mcpdev80/baseharbor/pull/1698)  
**Source:** 
<!-- /generated:links -->

## Goal

Make CI failures faster to diagnose and give developers a local fast-feedback path. Let a PR add and exercise its own checks while preserving only the base-defined minimum merge contract and backward compatibility with stacked PRs whose base planner is older.

## Scope

- In scope: truthful setup/dispatch/test failure reporting; a documented local fast-check command aligned with the quick PR checks; simplify path selection and reporting only where the acceptance criteria preserve existing proof; exact-head required aggregator behavior; same-PR evolution of optional/additional checks; old-base compatibility for lane stacks.
- Out of scope: broad rewrite, blanket full PR matrix, removing existing required native/runtime proof, stopping Codeman, changing release qualification, or allowing candidate-defined checks to become required for that candidate.

## Acceptance

- **Require — base-owned minimum only:** "Only checks selected by trusted policy from the PR target base (including its predeclared legacy broad fallback) may block this PR. Checks introduced by the PR may run and report, but become merge-required only after they merge into the base." Implement and test this as an explicit invariant.
- Candidate CI changes can run in the same PR and report additional checks, but cannot make those checks a merge requirement for that same PR or remove a base-required check.
- **Require — old-base compatibility:** when a stacked PR targets a base has an older planner that does not understand the candidate's new plan format or check IDs, selection falls back to the conservative relevant suite and succeeds when that suite succeeds; it must not fail merely because the old planner cannot parse the newer plan. Add a regression for new candidate plan vs old base planner.
- Unknown or unclassified paths broaden validation safely; they do not silently skip relevant checks and do not fail solely because the planner vocabulary is stale.
- Setup, checkout, dispatch, test execution, and test assertion failures are reported as distinct causes with the failing step and an actionable local reproduction hint. A missing output artifact must not masquerade as a test failure when the test command never started.
- Provide one documented local fast-check entry point that covers quick formatting, workflow/policy syntax, and focused tests without invoking native or full-release qualification.
- Keep exact-head final aggregation, current required check semantics, and all existing relevant Docker/Podman and cross-repository qualification gates intact.
- Measure the before/after required checks and runner-minutes on comparable PR changes; remove work only where equivalent proof remains. Do not add a full PR matrix.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☑ contract → the existing CI test package (`pr_focused` and `ci-executor-tests`; planner tests stay on `pr-planner-tests`) · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: BaseHarbor CI planner, PR workflow selection/reporting and associated routing/compatibility tests. Owner: Codex (this chat, CI fast feedback).
- Shared files: isolate edits in a dedicated worktree; do not modify a file while another active task owns it. The current Codeman work continues; no restart or interruption is needed.

## Handoff

- **Implementation in progress:** [PR #1698](https://github.com/mcpdev80/baseharbor/pull/1698), branch `ci-fast-feedback`, current source SHA `188016b91b9de7673c3545ef55db3946e2e00fce` (based on `develop` `3b634232`). Local `scripts/ci-fast-check.sh` passes (274 tests); hosted run `44533217111` is running. Earlier hosted attempts caught and fixed: English documentation byte limit, EN/DE technical parity, old trusted final-verifier CLI compatibility (`--plan`), and a truncated large fixture upload. The remote fixture now matches the local 169,505-byte file exactly and has zero NUL bytes.
- **Remaining acceptance work:** complete the exact-head selected checks; then exercise the merged policy through an old `lane-*` base. The currently pinned migration controller `a6756c5cd0f2a8ec43b0b7f777bf215bff2b9248` predates lane-target support, so after PR #1698 is trusted in `develop`, update that pin in a follow-up and verify conservative broad success on a real old-lane PR. Rulesets remain disabled during repair.
- Start with the smallest diagnostic/false-blocker fix, then the local fast-check entry point, then planner/required-check simplification. Do not begin planner changes until both explicit Require invariants above have regression coverage.
- Record exact changed files, SHA, required-check outcomes, old-base fallback proof, and comparable runner cost. Current baseline: CI audit and current PR checks discussed in Codex chat 2026-11-19; refresh live run/PR facts before editing.
