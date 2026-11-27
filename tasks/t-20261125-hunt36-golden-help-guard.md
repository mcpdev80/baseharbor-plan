---
id: t-20261125-hunt36-golden-help-guard
card_number: "0428-306"
card_short_title: "add golden --help snapshot CI"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "w396-0428-306-goldenhelp"
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-306 · add golden --help snapshot CI
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1874"]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/pull/220"]
---

- [ ] t-20261125-hunt36-golden-help-guard · 0428 hunt H-V36: add golden --help snapshot CI guard for config/flag surface #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w396-0428-306-goldenhelp  
    **PR:** [baseharbor#1874](https://github.com/mcpdev80/baseharbor/pull/1874)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/pull/220)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w396-0428-306-goldenhelp  
**Priority:** not set  
**PRs:** [baseharbor#1874](https://github.com/mcpdev80/baseharbor/pull/1874)  
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

- 2026-11-27 (w396): Product PR https://github.com/mcpdev80/baseharbor/pull/1874 OPEN at exact head `60d4d4906c686aa867f1c8d5f3d910ddba769999` (branch `lane-0428-306-golden-help-guard`, base develop `ea5218d72e`). Hosted CI runs observed: 45983604940 (cancelled by the draft→ready toggle), 45983691443 and 45987934493 both fail at `PR · Trusted Plan` with the base-catalog abort — `scripts/pr-gate-coverage.json` is loaded from the base/controller, so candidate-only catalog rows for the brand-new guard files cannot resolve fail-loud (`uncataloged source change ... cmd/baha/help_golden_guard_test.go`). Evidence: evidence/2026-11-27/0428-306/akte.md.

- Current state, branch, PR and evidence links. Newest first.

## Claim reconciliation (2026-11-27)

The live session `w396-0428-306-goldenhelp` (Codeman session `7c12281f-8210-4a2f-b612-11227fc271a3`) is busy and working in `/home/marcel/dev/baseharbor-ecosystem/workers/.models/flash`. Its product worktree is on branch `lane-0428-306-golden-help-guard`, one commit ahead of `lane-origin/develop` at `07999fa201`; the modified paths are `cmd/baha/help_golden_guard_test.go`, `cmd/baha/help_golden_invocation_test.go`, `internal/cli/cli.go`, and `internal/cli/help_surface_test.go`, matching this card's golden help surface and invocation scope. The task/branch match is confirmed.

Plan PR #220 published the same card claim and is now redundant with this active owner assignment. It remains open; this reconciliation does not close it. Only an authorized PR owner/coordinator may close it.
