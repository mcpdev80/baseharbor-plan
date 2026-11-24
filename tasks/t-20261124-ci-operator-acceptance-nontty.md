---
id: t-20261124-ci-operator-acceptance-nontty
card_number: "0428-285"
card_short_title: "CI operator Accept"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Make the test-only CI operator authenticate non-interactively so the Light policy/connectivity/reconciliation/full-destroy gates…
kanban_title: 0428-285 · CI operator Accept
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-ci-operator-acceptance-nontty · CI operator acceptance non-interactive in CI #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make the test-only CI operator authenticate **non-interactively** so the Light policy/connectivity/reconciliation/full-destroy gates stamp the synthetic operator in Hosted CI instead of failing. Residual follow-on to the closed 0428-250 fixture allow-list (which shipped via baseharbor-demo#170 + baseharbor#1815). This is the #1812 unblocker; #1812 itself stays workflow-only.

## Scope

- In scope:
  - baseharbor-demo `scripts/acceptance.sh`: the managed-policy acceptance operator-OIDC step must not require a TTY in CI (seed the test-only `baseharbor_ci_operator_testonly` managed-local operator so no interactive prompt), and must not emit an EMPTY acceptance group when a workload reached READY (the demo-connectivity/reconciliation empty-Acceptance-header symptom on run 45432650561).
  - baseharbor `cmd/baha/ci_integration_operator_enabled.go` (build-tagged test-only fixture): add the missing command forms to the allow-list so `up` with and without `--confirm-candidate` stamp the synthetic operator rather than fail closed.
- Out of scope:
  - baseharbor `.github/**` workflow files (owner-scope; #1825 already added the build tag/binary).
  - The frozen chain PRs #1812/#1819/#1820/#1818 — do NOT touch them.
  - #1826 / 0428-279 / 0428-283 static/mcp operator gap (separate owner decision, runtime=static excluded from this fallback).

## Acceptance

- On this lane's branch, the Light policy/connectivity/reconciliation/full-destroy paths stamp the synthetic CI operator with NO interactive terminal and NO empty acceptance group; consented-up reaches READY and the acceptance step emits a concrete assertion (not a blank group header).
- PR CI green; provide exact SHA -> test ID -> mapped gate -> trigger -> run URL/outcome for the affected operator-acceptance cases.
- The 14 Light RUNTIME gates go green only after this lane merges and #1812 rebases onto it (requalification runs on the #1812 PR, not here).

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
