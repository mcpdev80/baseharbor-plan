# CODEX-REVIEW 0427-134 r3 — PR #1457

## PLAN

1. Resolve the live PR #1457 head, develop base, exact diff, and exact-head run.
2. Check the r2 no-browser correction through the actual CLI argument path.
3. Verify the combined managed-CA and headless-PKCE login regression, documentation, and unit-test result.
4. Compare the reported native-gate STATE with the task acceptance and 0427-137 Owner decision; record exact failed job lines.
5. Publish this act in baseharbor-plan and verify its remote presence and candidate refs.

## Verdict

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1457 head:** `83d175f54ea9aba432d192c87dfe6464e879e0df`  
**PR state:** OPEN, not draft, mergeable; `mergeStateStatus=UNSTABLE`.  
**Run:** `42467172096`, terminal failure on the exact head.

### 1. The `--no-browser` CLI path is still rejected before Login

The r3 code does set `NoBrowser: noBrowser` in `TrustOptions` at `cmd/baha/operator_auth.go:61-65`. But the flag is not removed from the generic argument list: `parseLoginTrustArgs` sets the bool and appends `--no-browser` to `remaining` at `cmd/baha/operator_auth.go:220-222`. `extractApplicationEnvironment` in `cmd/baha/app_context.go:470-499` removes only environment options and returns other arguments unchanged. The command then rejects any remaining argument at `cmd/baha/operator_auth.go:32-34`, before calling `operatorauth.Login`.

The new `TestParseLoginTrustArgsNoBrowserAcceptsHeadlessFlag` (`cmd/baha/operator_tenant_bootstrap_test.go:49-75`) asserts that `--no-browser` is still present in `remaining`; it tests the helper result, not `operatorLoginCommand`. Therefore the documented `baha login ... --no-browser` command still cannot reach the new `TrustOptions.NoBrowser` wiring.

**Correction recipe:** in `cmd/baha/operator_auth.go:220-222`, capture `noBrowser=true` and consume the flag instead of appending it to `remaining` (or explicitly remove it before the generic leftover check). Change the parser test to assert it is absent from `remaining`. Add a command-level regression invoking `operatorLoginCommand` with `-e`, managed `--ca`, `--auth-code-file`, and `--no-browser`; prove it reaches `Login`, completes headlessly, and never calls the browser opener. The stop condition is that the actual command invocation accepts the documented flag and completes the production login path without browser launch.

### 2. Combined managed-CA and PKCE library-path test: PASS

`TestLoginThroughManagedCAProvesCombinedProductionPath` in `internal/operatorauth/login_ca_integration_test.go` calls the real `operatorauth.Login`, with no injected HTTP client, against an OIDC server whose TLS leaf is signed only by the managed test CA. It exercises discovery, JWKS, token exchange, PKCE S256/code-file completion, and persisted session validation. The fixed callback-port behavior is asserted separately by `TestLoginFixedCallbackPortAssertsBoundRedirectURI`. The `--no-browser` part of this test sets `TrustOptions.NoBrowser` directly, so it does not disprove Finding 1 about the CLI parser.

### 3. Documentation and unit checks: PASS on the exact head

Run `42467172096` confirms `PR · Validation · go-unit-tests` passed on `83d175f54ea9aba432d192c87dfe6464e879e0df`; the documentation audit and English/German documentation jobs also passed. The command index and authentication documentation include the headless option. `PR Selected Checks` is not green, as detailed below.

### 4. Native gates are failed, not a passing STATE

The task card `tasks/t-20261108-bughunt-0427-ca-trust-pkce-gap.md:43-53` requires the login/node flows to work without manual trust surgery and requires managed-CA discovery and headless PKCE regression coverage. The 0427-137 Owner decision says qualification tests run on GitHub-hosted Docker/Podman runners, and explicitly says a missing, skipped, or failed required acceptance is not PASS. It does not authorize replacing failed native acceptance with a STATE label or requesting physical-host tests.

On exact-head run `42467172096`, the native jobs actually ran and failed:

- `PR · Native Keycloak/Core · docker`, job `128689298771`, step `Execute mandatory native Keycloak/Core acceptance`: `control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-2146291997/baseharbor-bootstrap-cleanup-pending: no such file or directory`.
- `PR · Native Keycloak/Core · podman`, job `128689298704`, same step: `control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-3027939328/baseharbor-bootstrap-cleanup-pending: no such file or directory`.
- `PR · Native destroy retry · docker`, job `128689279892`: `installation_destroy_native_test.go:43: missing deployment state for installation-retry-native/installation-retry/dev [e8cb5b02-1715-4e23-a005-5ff9a09537c6]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable`.
- `PR · Native destroy retry · podman`, job `128689279986`: `installation_destroy_native_test.go:43: missing deployment state for installation-retry-native/installation-retry/dev [1af4ebe7-1f36-4554-87b2-5604a93c00cc]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable`.
- `PR Selected Checks`, job `128691379365` from required app `15368`, failed at `Require selected native acceptance before merge`.

The errors may be in unrelated shared native fixtures; this review does not attribute them to the CA/PKCE diff. The run nevertheless contains terminal failures, not an inability-to-run witness, and it contains no successful native login plus `baha node add` proof. The lane's STATE explanation cannot substitute for the card's acceptance or the executed failed checks.

**Correction recipe:** do not edit `.github/**` or trigger a rerun from this review. Report these exact failures to the workflow/CI owner. The owning lane must correct or obtain owner resolution for the failing acceptance prerequisites, then observe successful required Docker and Podman acceptance and `PR Selected Checks` on the final exact candidate. The native result must include the card's managed-CA login and `baha node add` behavior; passing unit tests alone is not enough.

### 5. Current develop has advanced beyond the PR base

The PR base snapshot is `48d6f10ac8a36ab8289f8981acef153c558dd2d7`, while remote develop is `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`. Compare against current develop reports `ahead_by=3`, `behind_by=5`, merge base `48d6f10ac8a36ab8289f8981acef153c558dd2d7`. Refresh onto current develop after the corrections; the resulting SHA needs new exact-head required checks and review.

The previously reviewed scoped host-cleanup witness in `round-2.md` remains recorded and this r3 delta does not change it. It does not replace the missing native acceptance above.

## Stop criterion

Do not approve until the command-level `--no-browser` invocation reaches Login and succeeds without launching a browser, the required managed-CA/headless behavior passes the selected Docker and Podman acceptance, `PR Selected Checks` succeeds from app `15368`, and the final head is refreshed against current develop. A changed final SHA requires fresh exact-head gates and review. Do not modify workflows or rerun jobs from this review.

## Evidence witnesses

- `gh pr view 1457` reports open, not draft, head `83d175f54ea9aba432d192c87dfe6464e879e0df`, PR base `48d6f10ac8a36ab8289f8981acef153c558dd2d7`, and `mergeStateStatus=UNSTABLE`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1457/head` returned:

```text
d30de3a4a176e073c8c1a9a0fc0b0ef06202b064\trefs/heads/develop
83d175f54ea9aba432d192c87dfe6464e879e0df\trefs/pull/1457/head
```

- GitHub compare of the exact PR base `48d6f10a...` to the head reports `ahead_by=3`, `behind_by=0`, status `ahead`; compare to current develop reports five commits behind.
- `gh run view 42467172096` reports completed failure on the exact candidate SHA. `go-unit-tests` and docs jobs passed; four native jobs failed; `PR Selected Checks` from app `15368` failed.
- Planning repo remote is `https://github.com/mcpdev80/baseharbor-plan.git`; pre-publication `git ls-remote origin refs/heads/main` returned `96b54ce29660797351179ae6db86748328c1fb85`.
- This was a read-only product review: no product files changed, no test was run locally, no workflow edited, and no CI rerun/dispatch or host operation was started.

## END

END_BLOCKED 0427-134-review-r3 — KORREKTUR; `--no-browser` remains in the generic argument list and is rejected before Login; exact-head native Docker/Podman jobs failed and `PR Selected Checks` failed. The combined managed-CA/PKCE library test, unit tests, and docs pass, but they do not clear these blockers.
