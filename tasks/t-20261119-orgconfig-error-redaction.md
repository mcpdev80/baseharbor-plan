---
id: t-20261119-orgconfig-error-redaction
card_number: "0428-149"
card_short_title: "Redact secret-like"
type: task
areas: [architecture, security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex team (current thread)
kanban_status: active
kanban_lane: active
kanban_summary: Reject secret-like organization environment references without copying their contents into validation errors. Keep error…
kanban_title: 0428-149 · Redact secret-like
priority: high
depends_on: [t-20261114-r28-cli2-org-env]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261119-orgconfig-error-redaction · Redact secret-like organization references in validation errors #task #release/v0-4-28 #status/active #view/active #area/architecture #area/security #kind/task
    <!-- generated:card -->
    **Owner:** Codex team (current thread) · **Priority:** high  
    **Needs:** [t-20261114-r28-cli2-org-env](t-20261114-r28-cli2-org-env.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-org-env](t-20261114-r28-cli2-org-env.md)  
**Owner:** Codex team (current thread)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reject secret-like organization environment references without copying their contents into validation errors. Keep error messages useful while preventing token/password/credential values from reaching CLI output, logs or audit text.

## Scope

- In scope: redact the reference value from the `validateEnvironmentIdentity` rejection path; add a regression using a distinctive secret sentinel and assert the error remains useful but does not contain the sentinel.
- Out of scope: changing secret-detection rules, authorization policy, unrelated organization config behavior, or editing another worker’s branch. Deliver as an additive fix commit based on the exact 0428-056 candidate and hand it to that owner for integration.

## Acceptance

- A secret-like identity reference is rejected with a safe, actionable error that does not include the supplied reference or any substring of the secret sentinel.
- Existing non-secret reference validation behavior remains unchanged.
- A regression test fails on the current 0428-056 head and passes after the fix.
- Local focused unit tests pass and the commit is integrated into the existing 0428-056 PR before that PR is marked ready or merged.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding:** normal Go package test auto-discovery (`internal/orgconfig`). The regression is a unit test and adds no CI workflow, catalog or package selector changes.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files: only the validation and its dedicated test in `internal/orgconfig/`.
- Dependency: 0428-056 (#1596), whose candidate introduces `EnvironmentIdentity` validation.
- Preserve all commits and worktree state on the 0428-056 branch; deliver a standalone commit for its owner to cherry-pick. No `.github/**` or `security.go` edits.

## Handoff

- Active; exact PR head and owner-accepted integration path are being established. No product edit has been pushed yet.
