# CODEX-REVIEW 0427-134 R7 — PR #1457

## PLAN

1. Verify the exact PR head, target base, ancestry, and R7-only diff.
2. Review the browser-observer placement and the CLI counterfactual against the R6 stop criterion.
3. Map CA/PKCE coverage and the card's runtime acceptance to current evidence.
4. Verify exact-head hosted results, identify the failing job and compare its failure with the cited develop runs.
5. Publish the verdict and stop criteria in this planning evidence file.

## Candidate and provenance

Role: CODEX-REVIEW.

Repository: `mcpdev80/baseharbor`; PR [#1457](https://github.com/mcpdev80/baseharbor/pull/1457), task 0427-134.

Reviewed head: `1770873042cfcd23a49e793664715afb11516290`.

The PR targets `develop` at `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c`. The R7 delta parent is `b4b027de593f306ec7cf2d3465bcb735e69628f2`. Both `git merge-base --is-ancestor <sha> 1770873042cfcd23a49e793664715afb11516290` checks returned 0. GitHub reports the PR open and mergeable.

The delta from `b4b027de` is limited to `cmd/baha/operator_tenant_bootstrap_test.go` (25 insertions and 25 deletions). No production or workflow file changed in R7.

## Review findings

### 1. Browser observer and CLI counterfactual: PASS

In `cmd/baha/operator_tenant_bootstrap_test.go`, `clearInheritedNoBrowser` and `installFakeXdgOpen` run at lines 164-166, before `operatorLoginCommand().Run` at line 168. The post-command marker assertion at lines 175-180 fails if the command attempts to launch a browser. The observer therefore covers the command's own invocation, not a subsequent direct lower-level login.

The check is counterfactually meaningful. In `internal/operatorauth/login.go:135-143`, `--auth-code-file` queues the callback before `internal/operatorauth/login.go:151-153` conditionally calls `openBrowser`. If the CLI drops `NoBrowser` at `cmd/baha/operator_auth.go:64`, the queued code can still complete exchange and persistence, but `openBrowser` runs before the callback is consumed and the preinstalled marker records it. The assertion at test line 178 then fails. The test also proves the managed path did not take the trusted-local early return and that token exchange/session persistence completed (`operator_tenant_bootstrap_test.go:172-195`). Round 7 records the forced-`NoBrowser:false` mutation failing and restored production passing.

### 2. CA/PKCE integration coverage: test-level pass; card runtime acceptance remains unproven

`TestOperatorLoginCommandNoBrowserReachesHeadlessPath` drives the production `operatorLoginCommand().Run` path. `startManagedOperatorOIDCServer` creates a fresh CA and a TLS endpoint (`operator_tenant_bootstrap_test.go:319-327, 332-350, 408-425`); the test points the production trust-file configuration at that CA. Its token endpoint requires an authorization-code exchange and a nonempty PKCE verifier (`operator_tenant_bootstrap_test.go:373-388`). This is durable CA-trust and headless-PKCE regression coverage for the OIDC client path.

This fixture is an in-process OIDC test server, not a managed Keycloak instance. It does not perform `baha login -e dev --init-tenant` against native Core/Keycloak and does not execute `baha node add` on both Docker and Podman. The card's outcome expressly requires those native-host journeys without manual trust changes. The existing E2E dossier records the earlier login/node-add cells as blocked, and no successful replacement of those two real runtime outcomes is present in the R7 evidence. Thus the test-level CA/PKCE regression is present, but the card's full native-runtime outcome is not yet established.

### 3. CI capture and exact-head hosted state: test captured; required native gate red

The exact-head GitHub Actions run [42497243794](https://github.com/mcpdev80/baseharbor/actions/runs/42497243794) completed with **failure** on the reviewed SHA. `PR · Validation · go-unit-tests` passed; its `scripts/pr-unit-database.sh` step runs `go test ./... -count=1`, which includes `TestOperatorLoginCommandNoBrowserReachesHeadlessPath`. Build, vet, formatting, documentation, wizard-registration, and both native destroy-retry jobs also passed.

Both `PR · Native Keycloak/Core · docker` and `PR · Native Keycloak/Core · podman` failed. `PR Selected Checks` is also **failure**; its log reports `BLOCKED: workflow job did not succeed: pr_owner_node_native`. This is not a skippable result.

The native failure is in the separate `TestControlPlaneSingleDefaultNativeRuntimeInCI` fixture: the R7 run evidence records `bootstrap leftover marker missing (teardown not guaranteed)` at `cmd/baha/control_plane_single_native_ci_test.go:31`. The same test and error occurred on develop in runs [42485190712](https://github.com/mcpdev80/baseharbor/actions/runs/42485190712) (Docker) and [42485190770](https://github.com/mcpdev80/baseharbor/actions/runs/42485190770) (Podman), consistent with the separate 0427-156 failure domain and unrelated to this test-only R7 delta. The 0427-156 diagnosis traces it to the native single-default CI job not setting `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`; the shared TestMain then does not create the marker that the test unconditionally requires. This needs the workflow owner, not a code change in this R7 delta.

There is an important gate distinction: the failing test's root cause is external to 0427-134, but the **job is selected and required for this PR**. The trusted path selector in `.github/workflows/ci.yml:557-565` matches `cmd/baha/operator_`; this R7 change is `cmd/baha/operator_tenant_bootstrap_test.go`. The `pr_owner_node_native` matrix is conditioned on `owner_node_required` at `.github/workflows/ci.yml:1042-1074`, and `PR Selected Checks` includes that job at lines 1079-1082. So it is accurate to attribute the particular single-default failure to the 0427-156/shared fixture, but inaccurate to say no required check is underneath it. I did not edit workflow files or rerun CI.

## VERDICT: KORREKTUR — external acceptance blocker

The R7 source delta closes the R6 browser-observer gap and the command-entry CA/PKCE regression is covered by the passing unit job. I found no new R7 source defect. However, the task is not acceptance-ready: the exact-head `PR Selected Checks` is red on a selected native job, and the card's real Docker/Podman `--init-tenant` plus `node add` outcome is not established by the in-process OIDC fixture. The native red has a matching develop failure and should be handled in its owning 0427-156 scope, not patched in this 0427-134 test-only delta.

## Actionable recipe and stop criterion

1. Keep the R7 observer-before-Run arrangement and the command-entry assertion. No additional R7 source edit is requested for this review point.
2. The owner of the shared native fixture must resolve the missing-marker failure or provide an explicit waiver. Because `PR Selected Checks` includes `pr_owner_node_native`, do not mark the PR accepted or merge-ready while run 42497243794 remains terminal failure. Observe a new exact-head hosted run after the authorized resolution; do not rerun it from this review.
3. Supply successful evidence that `baha login -e dev --init-tenant` and `baha node add` complete on both native Docker and Podman hosts using the managed CA path without OS trust surgery. Ensure the evidence identifies each host, exact candidate, command output, and cleanup result.

Stop criterion: approval/acceptance requires the selected native job and `PR Selected Checks` to pass on the exact reviewed head (or a reviewed successor), plus the card's successful native Docker and Podman login/node journeys. The unit-test pass and matching develop failure establish neither a green required check nor those real-runtime outcomes.

## Review integrity and planning provenance

Read-only product review; no product changes, tests, workflows, VM stacks, or CI reruns were made by this reviewer.

Planning repository: `https://github.com/mcpdev80/baseharbor-plan.git` (`origin` verified). Before publication, the exact `git ls-remote origin refs/heads/main` output was:

```text
642cef5d692ddbbb81e37d354d46008626462f4a	refs/heads/main
```

The round-7 source evidence exists at that planning head; its introducing commit is `b057e59aed4f0b8ef07d2876fc311e582885b924`.

Planning validation: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 4 dependency-state warnings in unrelated task notes; rendering produced no additional changed files.

END_BLOCKED 0427-134-review-r7 — source delta passes the observer criterion, but selected native CI is red and card-level Docker/Podman login plus node-add acceptance remains unproven.
