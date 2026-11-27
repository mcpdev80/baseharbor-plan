---
id: t-20261125-hunt42-timeout-constant-matrix
card_number: "0428-315"
card_short_title: "unify/align timeout constant"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w400-0428-315-timeoutsfix
kanban_status: wait
kanban_lane: wait
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-315 · unify/align timeout constant
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "content consolidated at d51763d0 (tempo trace-query probe + shared-provider reconcile read central StatusTimeoutMatrix; readiness 90s / existing-provider probe 3s budgets distinct; values unchanged, no tuning) — pushed to PR #1882 head d51763d0 (branch lane-0428-315-timeouts). Two executed pull_request runs on exact head: #7991 + #7992 both FAILED at shared base-catalog coverage gate (uncataloged internal/metrics/perses_tempo_datasource.go + internal/objectstorage/seaweedfs.go). Same Owner-scope shared scripts/pr-gate-coverage.json gate as lanes 307/310/312/316; the two missing catalog rows (surface source.gate.integration.static.public.contracts) are Owner scope, out of lane write-set. After lift: rerun on exact head d51763d0. PR body untouched."
resolution: ""
evidence: []
---

- [ ] t-20261125-hunt42-timeout-constant-matrix · 0428 hunt H-V42: unify/align timeout constant matrix (tempo 10s vs verify; reconcile/readiness values) #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** w400-0428-315-timeoutsfix  
    **Waiting:** content consolidated at d51763d0 (tempo trace-query probe + shared-provider reconcile read central StatusTimeoutMatrix; readiness 90s / existing-provider probe 3s budgets distinct; values unchanged, no tuning) — pushed to PR \#1882 head d51…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w400-0428-315-timeoutsfix  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V42: timeout constants diverge (perses_tempo_datasource.go:66 10s vs perses_tempo_verify.go; objectstorage 120s/90s vs others). Produce single documented timeout matrix constant + align values where semantics identical; behavior-neutral.
