# CODEX-REVIEW 0427-144 — recovered PR #1504

ROLLE: REVIEW  
URTEIL: APPROVE  
Kandidat: `a6bb99bfa1727b2231c3b226a7069c33abe96a51`  
PR: https://github.com/mcpdev80/baseharbor/pull/1504  
Kartenvertrag: `t-20261108-bughunt-wizard-foreign-records`  
Exact-head run: `42530928591` (`pull_request`, completed/success)

## PLAN

1. Verify live PR #1504 head/base, current develop head, ancestry, mergeability, run, and #1501 closure state.
2. Inspect the exact candidate diff and trace foreign-consumer attribution, selection tolerance, and conflict reporting.
3. Check the two-app regression for both unaffected resolution and preservation/actionable handling of the existing foreign record.
4. Map the regression file to its hosted check and pull-request trigger; inspect exact-head results and changed workflow paths.
5. Publish the SHA-specific verdict and drift-aware landing recipe in Planning.

## Live candidate and #1501 incident

The live PR API reports #1504 open and mergeable with head `a6bb99bfa1727b2231c3b226a7069c33abe96a51` and recorded base `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Fetching `refs/pull/1504/head` returned the same SHA. Live `git ls-remote` reports current `develop` at `b3a8042d18ea60f162a32a51df34a499cad6a237`.

The candidate is one commit based on the prior develop head `20902f0a6`; current develop is not an ancestor of it. `merge-base(origin/develop, origin/pr-1504)` is `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Current develop is one commit ahead (`b3a8042d fix(r27): target delete honors --yes on non-TTY (BF-03 / 0427-164) (#1494)`). Its five changed paths are `cmd/baha/bugs_858_860_regression_test.go`, `cmd/baha/human_cli_v0424_test.go`, `cmd/baha/target.go`, `cmd/baha/target_definition_change.go`, and `cmd/baha/target_definition_change_test.go`; none overlap the candidate's changed files. The PR reports mergeable. This is base drift to account for during normal landing, not an unreported ancestry claim.

PR #1501 is closed with `merged_at: null`; GitHub's issue event records closure on 2026-11-08. Its former head was this same `a6bb99bfa1727b2231c3b226a7069c33abe96a51`. The resumed candidate is therefore the same source commit on the open recovery PR #1504, not a new or modified product candidate. The exact-head run checked below is the #1504 pull-request run.

The candidate changes eight files: `cmd/baha/app_core_requirement.go`, `cmd/baha/app_edit.go`, `cmd/baha/app_edit_apply_result.go`, `cmd/baha/app_foreign_records_regression_test.go`, `cmd/baha/app_provider_choice.go`, `cmd/baha/app_wizard_controller.go`, `internal/application/footprint.go`, and `internal/application/provider_union.go`. No `.github/**` path is changed.

## Contract review

The acceptance allows provider resolution either to tolerate unrelated foreign-record residue or to surface a concrete actionable conflict, while retaining the foreign record's own authority. The candidate keeps both outcomes explicit rather than silently dropping a consumer.

- `internal/application/provider_union.go:95-102` sets `ResolutionError.Consumer` to the active consumer key only when the resolver has not already attributed the error.
- `cmd/baha/app_core_requirement.go:162-194` preserves ordinary resolution classes. When an active consumer is identified, the error names `deployment/<ID>`, the missing provider realization, and advises restoring it or releasing the named consumer through its lifecycle owner; it states that no provider was mutated.
- `cmd/baha/app_provider_choice.go:143-165` only converts a `missing` result for the exact currently selected requirement into an unresolved selection-view row. Other errors, including dependency-edge, foreign-instance, and wrong-target failures, still return typed errors. Thus the UI tolerance is limited to the requirement being presented and does not blanket-ignore union-resolution failures.
- `cmd/baha/app_edit.go:80-112` restores preferences from the same choice surface and prints an explicit unavailable-preference message before falling back to automatic selection. The source record is not silently rewritten by opening the edit surface.

The new two-app fixture at `cmd/baha/app_foreign_records_regression_test.go:27-69` writes a foreign SQL app record with a stale provider preference on the same Target as an independent HTTP-only app. The regressions then establish:

- `TestForeignRecordDoesNotBlockHttpAppSelection` (`:86-111`) resolves the HTTP-only app selection and confirms its own exposure proposal remains available.
- `TestForeignRecordUnionReportsConcreteConflictWithNextStep` (`:113-172`) exercises the production union plan, requires a typed `deployment/<ID>` conflict with the stale realization and lifecycle-owner recovery, and verifies the stored foreign preference remains unchanged and its declared projection remains represented.
- `TestForeignRecordStaleReferenceDoesNotPoisonUnrelatedUnionPlan` (`:174-217`) verifies an unrelated HTTP plan succeeds when the foreign realization is registered but unused, and rejects a destructive change to that realization.

This covers tolerance of irrelevant residue, an actionable failure when the retained consumer actually makes the union unresolvable, and preservation of the foreign record rather than overlooking it.

## Hosted CI and trigger

Run `42530928591` is `completed/success` on exactly `a6bb99bfa1727b2231c3b226a7069c33abe96a51` with event `pull_request`. `PR · Validation · go-unit-tests` job `128884763238` passed; `PR Selected Checks` job `128887098202` passed. The run also passed `go-build`, `go-vet`, `cli-gofmt`, `wizard-provider-choice-tests`, `wizard-app-edit-tests`, `wizard-controller-tests`, source format, and the native destroy-retry Docker and Podman jobs. The `Native Keycloak/Core` matrix job was skipped; it is not counted as a pass and no such run is required by this read-only provider-selection acceptance.

The regression source is `cmd/baha/app_foreign_records_regression_test.go`. Its durable CI route is the `go-unit-tests` validation group: trusted develop `scripts/pr-gate-plan.py:1531-1534` defines that group as `go test ./... -count=1`; `.github/workflows/ci.yml:118-124` invokes the selected release-source tests, including `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`, on the `pull_request` event for `develop` (`ci.yml:12-16`). The exact-head `go-unit-tests` job ran and passed. This is test → group → pull-request trigger evidence; no workflow change is needed.

No check rerun was requested or triggered. The existing exact-head run is terminal and successful.

## Verdict and landing recipe

**APPROVE** for source candidate `a6bb99bfa1727b2231c3b226a7069c33abe96a51`. The tolerance path is limited to selection-view missing requirements, union errors retain an actionable consumer owner, and the two-app regression preserves the foreign preference and forbids destructive changes. The exact-head selected checks passed and the implementation introduces no workflow-file requirement.

At landing, account for the one-commit develop drift from `20902f0a6` to `b3a8042d1`. Use the ordinary PR integration path and its current required checks; if synchronizing with current develop changes the candidate SHA, verify checks on that resulting exact SHA. After merge, record the merge commit and fresh develop head. Stop if the integration is not clean or a required check on the integrated candidate is red; do not use a bypass. No post-merge product behavior is claimed by this review.

This was a read-only product review. No product files, PR state, branches, or workflows were changed; no tests or containers were started locally.

END_DONE 0427-144-review-1504: APPROVE — reviewed candidate `a6bb99bfa1727b2231c3b226a7069c33abe96a51`; note base drift to develop `b3a8042d18ea60f162a32a51df34a499cad6a237` at landing.
