---
id: t-20261122-footprint-show-not-admitted-in-data-capabilities-gate
card_number: "0428-227"
card_short_title: "footprint show gate admission"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w21-pr1702-0428-142-compat
kanban_status: review
kanban_lane: review
kanban_summary: "The disposable acceptance gates that legitimately call baha app footprint show are admitted by the CI operator boundary, so the…"
kanban_title: 0428-227 · footprint show gate admission
priority: ""
depends_on: [t-20261121-develop-full-suite-red, t-20261122-ci-integration-operator-seams-without-gate-admission]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1753]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-footprint-show-not-admitted-in-data-capabilities-gate · Acceptance contract: baha app footprint show is admitted only for the guided gate #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** w21-pr1702-0428-142-compat  
    **PR:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-develop-full-suite-red](t-20261121-develop-full-suite-red.md), [t-20261122-ci-integration-operator-seams-without-gate-admission](t-20261122-ci-integration-operator-seams-without-gate-admission.md)  
**Required by:** [t-20261120-workload-port-flag-ignored-locally](t-20261120-workload-port-flag-ignored-locally.md)  
**Owner:** w21-pr1702-0428-142-compat  
**Priority:** not set  
**PRs:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753)  
**Source:** 
<!-- /generated:links -->

## Goal

The disposable acceptance gates that legitimately call `baha app footprint show` are admitted by the CI operator
boundary, so the gate fails on the contract and not on the command shape. Today the admission exists only for
`gate == "guided"`; on the `data-capabilities` gate the same canonical call is rejected and the job dies with
`command-not-in-managed-workload-set`, which blocks unrelated cards that merely select that gate.

## Scope

- In scope: `cmd/baha/ci_integration_operator_enabled.go` gate-admission branches and their regression tests, plus the
  data-capabilities fixture's use of the footprint read.
- Out of scope: broadening the managed-workload set to arbitrary commands; any change that admits a mutation outside a
  selected disposable target.

## Acceptance

- One documented rule states for which gates `app footprint show` (canonical read-only form) is admitted, and why.
- The chosen shape is implemented either as an additional gate admission or by removing the footprint call from the
  data-capabilities fixture; the reason is recorded in the PR.
- A regression test proves both directions: admitted on the gate that needs it, still rejected as
  `command-not-in-managed-workload-set` on a gate that must not run it.
- The data-capabilities Docker job that previously failed passes on the exact candidate SHA in hosted CI.

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

- Owned files or areas: `cmd/baha/ci_integration_operator_enabled.go` and its `cmd/baha` tests.
- Shared files: coordinate through the owning task. `scripts/pr-check-runner.py` and `scripts/pr-gate-*.py` stay CI-owner
  scope; a change there must be requested as a finding with file:line, not edited by this card.

## Handoff

- Origin of this card, measured by the Coordinator on develop `7d4351c6d645353b6b96c8d320b4c832d55f9047`:
  - `cmd/baha/ci_integration_operator_enabled.go:135` admits the footprint read only under `gate == "guided"`, through
    `ciIntegrationGuidedFootprintShow` (`:232-233`, exact shape `app footprint show -o json`).
  - `:179-180` is the fail-closed branch that produced `command-not-in-managed-workload-set: app footprint show …`.
  - The command itself is registered as read-only elsewhere: `cmd/baha/machine_coverage.go:97` maps
    `baha app footprint show` to `app.footprint.show`, and `cmd/baha/app_registration_921.go:40,43` documents the
    `-o json` form.
- Failure witness: PR #1723 (card 0428-199) exact run `44963676934`, Docker data-capabilities job `137028211165`
  failed with the message above; the same job family also reported that operator authentication wants an interactive
  setup while the input is not a terminal (`cmd/baha/operator_auth_boundary.go:117`), which is the separate
  prerequisite tracked on card 0428-223 (PR #1750).
- Classification: this is a shared acceptance contract in product code, not Owner-scope CI files and not a defect of
  card 0428-199. It is blocked behind nobody; it can be staffed as soon as a seat is free.

hop delivered by 0847d100: refs/pull/1753/head 71deb610a03, back=0 against develop 6209874428f, PR draft=false, exact run 44972857723 in_progress. a second re-hop branch lane-0428-227-footprint-gate-admission-rh2 (43d85d637a0) exists as surplus, nothing deleted. the data-capabilities gate still depends on the path-to-gate mapping (card 0428-228, Owner-scope)

independent review at exact head 91f4e38795a gives VERDICT APPROVE content, merge blocked by card 0428-228 path to gate entry at scripts/pr-gate-plan.py line 180 (reviewer akte review-1753-head91f4e38795a.md)

Corrected candidate head ce5cf8f3037 (back=0, ahead=1) mit run 44986388874 SUCCESS und 0 failed jobs; der erste versuch e120f0815 war durch eine beschnittene datei ungueltig und CI hat das sofort gezeigt. Selected Runtime ist auch hier SKIPPED (job 137097832863), grund: fehlende components- und native_checks-zeilen, karte 0428-230.
