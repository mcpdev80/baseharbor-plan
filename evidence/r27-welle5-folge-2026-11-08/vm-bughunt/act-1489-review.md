# CODEX-REVIEW 0427-162 — PR #1489

## PLAN

1. Verify PR #1489's live head, base, and hosted run 42505772259.
2. Review the exact three-file diff, command registration, regression tests, CI coverage, and failed job logs.
3. Publish a SHA-specific verdict and repair recipe in this planning evidence.

## ROLLE: REVIEW

## Verdict: KORREKTUR

### Candidate and remote state

- PR #1489 is OPEN, base `develop`, exact head `6d96bf5cad206327c895becf77a785c7186e6b76`; GitHub reports `MERGEABLE`, state `UNSTABLE`.
- `git ls-remote` reported `develop` at `3187cea15728143146905c7238ad6e280ca11b3e` and `refs/pull/1489/head` at `6d96bf5cad206327c895becf77a785c7186e6b76`.
- Run `42505772259` is terminal `failure` on that exact head. `go-unit-tests`, `go-vet`, `go-build`, `cli-gofmt`, Source format, Focused Python, and both Native destroy retry jobs passed. Both Native Keycloak/Core jobs failed, and `PR Selected Checks` failed.

### Review findings

1. **The replacement command exists.** The five changed operator-facing strings say `baha up`. In the exact candidate source, `cmd/baha/commands.go:76-80` registers top-level `up` with `runtimeUpCommandWithInputResolver`; its usage/help text describes the management-Core setup path. `cmd/baha/app_up.go:41-45` also registers `baha app up`. Thus the replacement does not point at a nonexistent `baha core install` command.
2. **No selection-logic change is present.** The product diff is exactly three files: four `core install` to `up` string replacements in `cmd/baha/use_target.go`, one recovery-string replacement in `cmd/baha/onboarding.go`, and two tests in `cmd/baha/use_target_connection_test.go`. The production selection/binding control flow is unchanged.
3. **The regressions are CI-covered.** `TestBindExplicitSelectionBindsWithoutLocalIssuerDir` removes only the local issuer directory while retaining a verified Core and Keycloak issuer, then calls the production `bindExplicitSelectionToConnection` path. `TestBindExplicitSelectionFailsClosedOnAbsentCore` checks that a target without a verified Core still errors. Both are in the `cmd/baha` package covered by the passing hosted `PR · Validation · go-unit-tests` job on this exact SHA. The run also passed build, vet, and CLI formatting.
4. **The hosted run is not green, and the red check is not waived by labeling it STATE.** `PR · Native Keycloak/Core · docker` (job `128807996962`) and `PR · Native Keycloak/Core · podman` (job `128807996957`) both failed `TestControlPlaneSingleDefaultNativeRuntimeInCI` at `cmd/baha/control_plane_single_native_ci_test.go:31`: `prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-1871000762/baseharbor-bootstrap-cleanup-pending: no such file or directory` (Docker); Podman reported the same error with its run-specific `/tmp/baseharbor-ci-data-65326115/...` path. `PR Selected Checks` (job `128810460846`) then failed with `BLOCKED: workflow job did not succeed: pr_owner_node_native`; its log shows `NATIVE_REQUIRED: true`. This is a required selected check failure on the reviewed head, even if the failing test belongs to the separate 156-domain investigation. No rerun or workflow change was made.

### Umsetzbares Lösungsrezept

- **Dateien:** `cmd/baha/control_plane_single_native_ci_test.go` / its bootstrap fixture ownership. Resolve the missing `baseharbor-bootstrap-cleanup-pending` marker failure in the responsible 156-domain lane; preserve fail-closed cleanup semantics. This is an external test-fixture finding, not a reason for this PR to alter unrelated application logic.
- **Files:** retain the text-only updates in `cmd/baha/use_target.go` and `cmd/baha/onboarding.go`; retain both BF-02 regressions in `cmd/baha/use_target_connection_test.go`.
- **Test requirement:** obtain a terminal green native Keycloak/Core result and a passing `PR Selected Checks` on the exact current PR head after the shared fixture issue is corrected. Do not treat the successful unit/build jobs or a STATE note as a substitute for the failed required check.
- **Stop criterion:** approval waits until the exact-head `PR Selected Checks` is successful and both required native Keycloak/Core jobs pass. If the independent 156-domain lane confirms the failure is external, record that attribution, but still require the final selected check to pass.

## repo-rule compliance

Read-only review of the product PR. No product code or `.github/**` files were changed; no checks were rerun or dispatched.

## END 0427-162 REVIEW

KORREKTUR — `6d96bf5cad206327c895becf77a785c7186e6b76`; wording and unit coverage look sound, but run `42505772259` failed the two required native jobs and `PR Selected Checks`.
