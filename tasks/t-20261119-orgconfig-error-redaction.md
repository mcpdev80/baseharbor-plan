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
kanban_status: review
kanban_lane: review
kanban_summary: Reject secret-like organization environment references without copying their contents into validation errors. Keep error…
kanban_title: 0428-149 · Redact secret-like
priority: high
depends_on: [t-20261114-r28-cli2-org-env]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1596]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1596", "https://github.com/mcpdev80/baseharbor/actions/runs/44847161507"]
---

- [ ] t-20261119-orgconfig-error-redaction · Redact secret-like organization references in validation errors #task #release/v0-4-28 #status/review #view/review #area/architecture #area/security #kind/task
    <!-- generated:card -->
    **Owner:** Codex team (current thread) · **Priority:** high  
    **PR:** [baseharbor#1596](https://github.com/mcpdev80/baseharbor/pull/1596)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1596), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44847161507)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-org-env](t-20261114-r28-cli2-org-env.md)  
**Required by:** [t-20261120-redact-invalid-org-environment-key](t-20261120-redact-invalid-org-environment-key.md)  
**Owner:** Codex team (current thread)  
**Priority:** high  
**PRs:** [baseharbor#1596](https://github.com/mcpdev80/baseharbor/pull/1596)  
**Source:** 
<!-- /generated:links -->

## Goal

Reject secret-like organization environment references without copying their contents into validation errors. Keep error messages useful while preventing token/password/credential values from reaching CLI output, logs or audit text.

## Scope

- In scope: redact the reference value from the `validateEnvironmentIdentity` rejection path; add a regression using a distinctive secret sentinel and assert the error remains useful but does not contain the sentinel.
- Out of scope: changing secret-detection rules, authorization policy, unrelated organization config behavior, or editing another worker’s branch. Deliver as a narrow additive commit on the exact 0428-056 PR branch; preserve all existing commits and use fast-forward only.

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

- 2026-11-20: User supplied an adjacent leak in the same validation surface: `Config.Validate` interpolates a secret-like `Environments` map key with `%q` in its invalid-name error (`internal/orgconfig/model.go:149-152` at PR head `c90c3b89`). This is within the card's goal of keeping secret-like organization values out of validation errors and within its owned validation/test files. Added `TestSecretLikeEnvironmentMapKeyIsRedactedFromValidationError`; it fails on `c90c3b89` by printing the sentinel `token=environment-map-key-sentinel-7f3a`. Fix returns a useful generic secret-like environment-name error, while ordinary invalid names retain the previous detailed message. Focused identity/map-key tests, full `go test ./internal/orgconfig -count=1`, `go vet ./internal/orgconfig`, and `git diff --check` pass. Standalone local additive commit `f113baf57aef9e24de5083740decdf84b361f8d8` is in `/var/tmp/baseharbor-sweep-1596` branch `codex/0428-149-map-key-redact`, parent `c90c3b89`; not pushed/integrated because the parent PR is still Draft and its stack hop is pending. Existing prior exact-head CI evidence above covers only `c90c3b89`, not this local commit.

- Fix commit `c90c3b89007e87a4bf277c8c9015fab3ac65728e` is integrated by fast-forward into #1596 branch `cli2-org-env-reconcile`; the PR exact head is this commit, based on `lane-0428-env-registry` `4d14741ee9485b7e0c346fa873ed59f637e71b68`. The card specified a standalone commit for owner cherry-pick; this was integrated directly by fast-forward instead, preserving the exact prior parent and all existing commits. Focused `go test ./internal/orgconfig -run '^TestOrgEnvIdentitySecretMaterialRejected$' -count=1`, full `go test ./internal/orgconfig -count=1`, and `go vet ./internal/orgconfig` all pass at the exact commit. The focused regression is auto-discovered in `PR · Draft Go · packages`; exact run [44592530459](https://github.com/mcpdev80/baseharbor/actions/runs/44592530459) completed SUCCESS on this SHA: source/routing and all five Draft Go shards passed, including the packages shard executing `./internal/orgconfig`; non-draft release/runtime/native jobs were skipped because the PR is Draft and are not claimed as passed. The task is in review for the identity-reference fix; parent #1596 remains Draft and has separate integration/acceptance blockers before Ready/merge.
- ZWEIFEL/follow-up: the separate invalid environment-map-key leak is tracked as planned card [0428-161](t-20261120-redact-invalid-org-environment-key.md). It depends on both #1596's introducing stack and this card; it is unassigned and cannot start until those prerequisites are accepted and the single-writer path is released.

- Exact-head handoff refresh (2026-11-21): #1596 is OPEN/non-draft at `6135e73a6e2c36e09637856412b94133b3743119`, which contains `f113baf57aef9e24de5083740decdf84b361f8d8` (`git merge-base --is-ancestor` verified). Exact run [44847161507](https://github.com/mcpdev80/baseharbor/actions/runs/44847161507) executes `internal/orgconfig` successfully in `PR · Go unit · packages`; the same job is overall red only on the three Loki tests in `internal/logs`, and CLI shards fail on other shared gates. The redaction change is handed off for review; this is not a claim that #1596's full required CI is green or that the PR is mergeable.
