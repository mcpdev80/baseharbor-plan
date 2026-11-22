---
id: t-20261122-env-destroy-native-assertion-contract
card_number: "0428-238"
card_short_title: "native env-destroy assertion"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: f0f6c8b4 (lane, PR #1627 branch cli2-env-delete)
tags: [#task, #release/v0-4-28]
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-238 · native env-destroy assertion
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

- [ ] t-20261122-env-destroy-native-assertion-contract · test: align native env-destroy assertion with the app stop contract #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** f0f6c8b4 (lane, PR \#1627 branch cli2-env-delete)  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** f0f6c8b4 (lane, PR #1627 branch cli2-env-delete)  
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


- **Test binding (select exactly one):**  normal (auto-discovered) ·  contract  add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR ·  new check  update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
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

## Finding (2026-11-22, exact-head run of PR #1627)

Run `44995034290` at head `bfd01276ff2c1db005063c39390e03bd89cf80cd`: `TestEnvironmentDestroyNativeLifecycle` fails on
BOTH engines - docker job `137124194466`, podman job `137124193912` - at
`cmd/baha/env_destroy_integration_test.go:136`: "KEEP must retain the stopped deployment owner: found=true
state=runtime-retired ready=false err=<nil>". Foundation jobs passed on both engines, so the newly admitted
environment-destroy native coverage itself works.

## Owner disposition (2026-11-22)

TEST expectation mismatch, NOT a proven product defect. `executeEnvironmentScopedDestroy` deliberately invokes the
existing app stop mode; `cmd/baha/app_coreless_runtime_test.go:209` and `cmd/baha/app_capability_runtime_test.go:314`
already require the persisted deployment record `Observed.State=runtime-retired` while the user-facing `app status`
resolves to `stopped`. The new assertion reads `deployment.FindDeployment` and wrongly expects `stopped` there.

Fix: assert BOTH halves of the established invariant - resolved app status reports `stopped` AND the retained record
reports `runtime-retired`. Do NOT change product semantics to force a stored `stopped` state without a broader
contract decision. Rerun hosted CI at the exact head; a green native pair on docker+podman is the evidence.
Parent card: `t-20261114-r28-cli2-env-delete` (0428-055, PRs #1627/#1736).
