---
id: t-20261124-gate-catalog-baseline-1816
card_number: "0428-261"
card_short_title: "add 3 Trusted Plan rows to"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w51-0428-261-catalog
kanban_status: review
kanban_lane: review
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-261 · add 3 Trusted Plan rows to
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1817]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/2026-11-24/0428-261-gate-catalog-baseline-1816/round-1.md"]
---

- [ ] t-20261124-gate-catalog-baseline-1816 · CI/catalog: add 3 Trusted Plan rows to develop pr-gate-coverage.json #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** w51-0428-261-catalog  
    **PR:** [baseharbor#1817](https://github.com/mcpdev80/baseharbor/pull/1817)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/2026-11-24/0428-261-gate-catalog-baseline-1816/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w51-0428-261-catalog  
**Priority:** not set  
**PRs:** [baseharbor#1817](https://github.com/mcpdev80/baseharbor/pull/1817)  
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

Candidate green: #1817 draft, head 3bae61a7 on develop d4fa8c589, run 45290693530 terminal success; diff = ONLY scripts/pr-gate-coverage.json adding EXACTLY the 3 data.capabilities rows (verified). Trusted Plan aggregate SKIPPED while draft. MERGE-FROST: Owner advances #1817 to ready + merges when green -> then rebase #1816 -> exact-head Hosted green. No lane merge; no Codex.

Expanded: #1817 now carries 6 develop-baseline rows — 3 for #1816 (cmd/baha app_status_collect/_perses_alert_evaluator_0428_152_test/perses_lifecycle) + 3 for #1810 (internal/application/perses_lifecycle_go, internal/metrics/perses_backend_status_go + _test_go). ALL surfaces docker+podman data.capabilities (validator-exact). Draft to develop d4fa8c589. Owner advance+merge once -> unblocks #1816 (rebase) AND #1810 (Trusted Plan). No lane merge; no Codex.

#1817 = 7 develop-baseline rows total: 3 for #1816 (cmd/baha app_status_collect/_perses_alert_evaluator_0428_152_test/perses_lifecycle) + 3 for #1810 (internal/application/perses_lifecycle, internal/metrics/perses_backend_status + _test) + 1 for #1809 (cmd/baha/environment_operations). ALL docker+podman data.capabilities; scripts file only; draft to develop d4fa8c589. Owner advance+merge unblocks #1816+#1810+#1809 rebases. No lane merge; no Codex.

NOT owner-ready yet: head a54df7cf has 6 rows but MISSING source.cmd_baha_environment_operations_go (required by #1809 exact Trusted Plan run 45292500773, docker+podman data.capabilities). w51 re-nudged to push a 7-row head. OWNER: do NOT advance/merge #1817 until all 7 rows present + exact-head CI green. Draft CI now: 5 success/27 skipped/1 active. scripts file only; no lane merge; no Codex.

7 rows now present at head d76aea570 (env_operations 7th landed): 3 for #1816, 3 for #1810, 1 for #1809, all docker+podman data.capabilities, scripts file only, draft to develop d4fa8c589. Owner advance+merge once exact-head Hosted draft/ready checks green -> rebase #1816+#1810+#1809. No lane merge (frost); no Codex.
