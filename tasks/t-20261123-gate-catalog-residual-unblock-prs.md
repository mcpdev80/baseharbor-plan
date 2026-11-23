---
id: t-20261123-gate-catalog-residual-unblock-prs
card_number: "0428-260"
card_short_title: "register residual uncataloged"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: mcpdev80 CI/coverage owner (sweep-assigned apply; owner-scope scripts/**)
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-260 · register residual uncataloged
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

- [ ] t-20261123-gate-catalog-residual-unblock-prs · CI gate catalog: register residual uncataloged cmd/internal paths so the 0428-242 fail-loud guardian stops blocking Trusted Plan for PRs 1810/1809 #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 CI/coverage owner (sweep-assigned apply; owner-scope scripts/\*\*)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** mcpdev80 CI/coverage owner (sweep-assigned apply; owner-scope scripts/**)  
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

H-V38 DELIVERED proven patch (baseharbor-plan origin/main ed1032734, evidence/recovery-2026-11-23/hunt-hv38-catalog-patch/round-1.md): 5-row pr-gate-coverage.json additions clear the 0428-242 guardian rc=1->0 for #1810 (3 gates) and #1809 (2 gates), validate rc=0; 3-row catch-all variant also proven. APPLY=owner/CI scope. Shared unblocker for both PRs' Trusted Plan.

ASSIGNED per sweep routing request: H-V38 proven 5-row scripts/pr-gate-coverage.json patch (origin/main ed1032734) is ready to apply directly to develop. Single owner scripts/** edit; unblocks PR · Trusted Plan for #1810 (3 gates) and #1809 (2 gates), validate rc=0. No worker lane (reserved CI/coverage scope). Owner applies + re-runs both PRs.

H-V39 CENSUS upgraded the ask: NOT just 5 rows. Because develop catalog release=v0.4.27, v0.4.28 plans take catalog-mode and BYPASS all legacy catch-alls -> the current green Trusted Plans are an artifact of the release mismatch. Real fix = ~40 PACKAGE-LEVEL path rows (prefix coverage, so NEW files inherit): decisive = cmd/baha, internal/capability, internal/application, internal/openbao, internal/runtime/resolver + ~20 top internal dirs (88% of 764-path population). Interim unblock for the 3 PRs = H-V38 5-row patch + 1 row for #1650 new file internal/metrics/perses_dashboards_keycloak.go. H-V40 desk is producing the apply-ready patched catalog + offline proof for #1810/#1809/#1650 + new-file inheritance. Landing note: when the rows ship, set catalog release to v0.4.28 deliberately.

DELIVERED via PR #1813 (MERGED, develop d4fa8c589, Hosted run 45265897355 green): 6 PER-FILE component rows clear the immediate guardian aborts for #1810/#1809/#1650. OPEN: (a) develop catalog release field still v0.4.27 while PRs plan v0.4.28 (H-V40 analyzing effect); (b) future NEW files still need a row each (per-file rows do not scale to new files) — H-V40 proving whether package/prefix rows give genuine (non-fallback) coverage in catalog-mode or must be retracted.

SCOPE REVISED per Owner (Hosted evidence): the 87-package-row broad expansion = PR #1814 FAILS 4 pr-planner guard tests (internal/application/provider_union.go no longer unresolved; internal/runtime/new_feature.go no longer raises; runtime/capability + application unowned checks). Broad package rows MASK INTENTIONAL fail-closed sentinels -> secure-by-design VIOLATION. #1814 CLOSED without merge. Correct model = #1813 (MERGED, develop d4fa8c589): EXACT per-file component rows only, for reviewed paths. Rule for this card and all successors: NEVER add broad package rows over explicit unresolved prefixes; future new files get a component row in the PR that introduces them (per-PR admission), not a directory prefix. Current-PR blockers are already resolved by #1813; remaining work = additive hop + exact Headed rerun by each PR owner.
