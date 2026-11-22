---
id: t-20261123-catalog-ingress-develop-prereqs
card_number: "0428-252"
card_short_title: "register existing-path sources"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: f0f6c8b4 (branch lane-0428-ingress-catalog, PR folgt) / Coordinator
kanban_status: active
kanban_lane: active
kanban_summary: "One develop-only catalog PR registers the base rows that Trusted Plan needs to admit already-existing product sources in #1753…"
kanban_title: 0428-252 · register existing-path sources
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261123-catalog-ingress-develop-prereqs · Catalog ingress: register existing-path sources in develop base catalog #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** f0f6c8b4 (branch lane-0428-ingress-catalog, PR folgt) / Coordinator  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** f0f6c8b4 (branch lane-0428-ingress-catalog, PR folgt) / Coordinator  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One develop-only catalog PR registers the base rows that Trusted Plan needs to admit already-existing product sources in #1753 and #1765. The resolver reads coverage from the trusted BASE (test-enforced: test_pr_native_gate_plan.py asserts git show :scripts/pr-gate-coverage.json); PR-head rows cannot admit any source, so every touched source must already be cataloged on develop.

## Scope

- In scope: scripts/pr-gate-coverage.json only; three component rows for paths that already exist at the base: internal/operatorauth/local_runtime.go, internal/operatorauth/local_runtime_test.go, cmd/baha/control_plane_single_native_ci_test.go. Row shape mirrors internal.operatorauth.test.operator.go (runtime_specific, both atomic docker+podman data-capabilities surfaces).
- Narrowed by Owner decision 2026-11-23: no packages-root entry. #1725 relocates its regression test into the already-cataloged internal/application/shared_backends_test.go instead (existing gate ownership, no side effects).
- Out of scope: any product code; any PR-branch edit; package-root ingress for not-yet-existing files (#1725 case is a separate policy question raised to Owner).

## Acceptance

- Trusted Plan on this PR is green (catalog-only diff, no product source changed).
- After merge, #1753 and #1765 re-runs pass the uncataloged check without touching their branches' catalog files.

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

abhaengige: #1753 (227) und #1765 (209) blockiert auf diesen base-ingress. Row-form analog internal.operatorauth.test.operator.go.

arbeit beginnt: drei base-rows, lokale validator-pflicht, dann PR + exact-head run. package-root-kapitel gestrichen (owner-schienenroute).
