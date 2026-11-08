# CODEX-REVIEW 0427-134 R6 — PR #1457

## PLAN

1. Verify the live PR head, develop base, ancestry, R6 commit delta, and cumulative PR write-set.
2. Review the three R5 stop criteria against the exact R6 source and round-6 mutation evidence.
3. Compare both failed Keycloak/Core cells with the same native test failure on the post-merge #1474 develop run.
4. Record the verdict, correction recipe, CI state, and stop criterion in this act.
5. Publish this act to baseharbor-plan origin/main and verify its remote tree entry.

## Candidate and provenance

- Repository: `mcpdev80/baseharbor`; PR #1457 is open, based on `develop`, and its live head is `b4b027de593f306ec7cf2d3465bcb735e69628f2`.
- The exact `refs/heads/develop` fetched for this review is `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c`; `refs/pull/1457/head` is `b4b027de593f306ec7cf2d3465bcb735e69628f2`. `git merge-base --is-ancestor cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c b4b027de593f306ec7cf2d3465bcb735e69628f2` exits 0.
- R6 adds the test-only commits `ac78619a`, `d7dbbc37`, and `07be4ac0`, followed by the develop drift merge `2c6ed412` and command-index regeneration `b4b027de`. The cumulative PR diff against develop is the CA/PKCE task's auth files, tests, and English/German auth documentation; it has no `.github/**` changes. The R6 counterfactual test edits are confined to `cmd/baha/operator_tenant_bootstrap_test.go`; the drift-generated documentation changes are `docs/cli/command-index.md` and `docs/de/cli/command-index.md`.
- The prior R5 act required the command-level regression to prove Login completion, detect both a lost `--no-browser` forwarding and an actual browser launch, retain the unknown-flag negative control, and run on the exact PR head with required gates green.

## R5 stop-criterion review

1. **Login reached through the command entry: PASS.** `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` calls `operatorLoginCommand().Run` with the documented flags at `cmd/baha/operator_tenant_bootstrap_test.go:155-157`, then checks a server-side OIDC exchange and a persisted valid session at lines 170-178. The in-process server has no other caller in this test file. The exact-head `PR · Validation · go-unit-tests` job passed in run `42489711156`.
2. **The CLI's `--no-browser` forwarding and browser-launch counterfactual: FAIL.** The browser observer is installed only after the command invocation, at lines 201-203. The observed call at lines 209-212 invokes `operatorauth.Login` directly with `NoBrowser: true`; it does not execute `operatorLoginCommand` or test whether `cmd/baha/operator_auth.go:64` forwards `noBrowser`. The recorded mutation changes `internal/operatorauth/login.go:151` to always call `openBrowser`, so it only proves the direct `Login(...NoBrowser:true)` path is suppressed. The claimed mutation that drops the CLI forwarding was not run: the round-6 note says token exchange would fail, but `AuthCodeFile` delivers the code before browser launch (`internal/operatorauth/login.go:135-143`), and `openBrowser` errors are ignored at lines 151-152. A command-level forwarding mutation can therefore still complete the exchange and session persistence. In addition, `clearInheritedNoBrowser` is called after the command invocation, so an inherited environment override could mask a broken flag path.
3. **Unknown-leftover flag control: PASS.** The command is separately invoked with `--bogus-flag` at lines 223-225 and must return the expected usage error.

The round-6 mutation evidence in `bughunt-ca-pkce/round-6.md` therefore demonstrates the lower-level `operatorauth.Login` browser guard, but it does not close the R5 requirement that the actual CLI entry proves the flag is consumed and forwarded.

## Hosted CI and attribution

- Exact candidate run [42489711156](https://github.com/mcpdev80/baseharbor/actions/runs/42489711156) is terminal failure on head `b4b027de593f306ec7cf2d3465bcb735e69628f2`. `go-unit-tests`, build, vet, formatting, docs, and native destroy-retry Docker/Podman passed. `PR Selected Checks` failed because `PR · Native Keycloak/Core · docker` (job `128759251810`) and `PR · Native Keycloak/Core · podman` (job `128759251840`) failed.
- Both jobs fail immediately at `cmd/baha/control_plane_single_native_ci_test.go:31` with `prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open .../baseharbor-bootstrap-cleanup-pending: no such file or directory`; each test reports `TestControlPlaneSingleDefaultNativeRuntimeInCI (0.00s)`.
- This failure signature matches the independent post-merge develop runs for #1474: Docker run `42485190712` on merge SHA `8ecd1ea5db0f979f971530ab75561fd545cc6c19` and Podman run `42485190770` fail at the same test and line with the same missing-marker error. The marker guard is in shared test support at `cmd/baha/runtime_integration_test_support_test.go:572-589`, introduced by commit `22a3cb8a` for #1454; neither that fixture nor the marker implementation is in the #1457 PR diff. This establishes that the native red is shared and change-independent from R6. The comparison alone does not prove that #156 owns the root cause; the evidence points to the shared bootstrap-marker fixture.
- The external native red is not a finding against the CA/PKCE implementation. It still means the required native cells and `PR Selected Checks` are not green; no rerun or workflow change was made.

## Verdict and correction recipe

**ROLLE: REVIEW — URTEIL: KORREKTUR.** The native Keycloak/Core failure is external to this candidate, but the R5 browser-suppression stop criterion remains unmet in the changed regression itself. This is not an approval-with-external-blocker yet.

- In `cmd/baha/operator_tenant_bootstrap_test.go`, clear `BASEHARBOR_NO_BROWSER` and install the temporary `xdg-open` observer before the `operatorLoginCommand().Run` call at lines 155-157. Immediately after that command returns, assert that no browser-launch marker exists.
- Demonstrate the actual CLI counterfactual by mutating `cmd/baha/operator_auth.go:64` to omit or force false `NoBrowser`; the command-entry test must fail because the marker is written, even though the auth-code exchange and persisted session may otherwise succeed. Restore production code and prove the test passes. Keep the existing token-exchange/session assertions and the unknown-leftover negative control.
- The lower-level direct `operatorauth.Login` browser test may remain as a separate unit check, but it cannot stand in for the command-entry assertion.
- Stop criterion: do not approve until the CLI-level forwarding mutation fails the regression and the corrected candidate has exact-head unit checks green. Before merge, the native Keycloak/Core Docker and Podman failures must be explained/resolved by the owning CI/0427-156 work or covered by an explicit owner waiver; otherwise `PR Selected Checks` remains a blocker. Do not modify `.github/**` or rerun the workflow from this review.

## Review integrity

Read-only product review. No product files, branches, workflows, or test runs were changed or started. Planning repository: `https://github.com/mcpdev80/baseharbor-plan.git`; pre-publication `refs/heads/main` was `762e3585f923927ae487e3917215b2bf676f7610`.

END_DONE 0427-134-review-r6 — KORREKTUR; native red is shared with develop run 42485190712, but the browser-launch observer does not cover the CLI command, so the R5 stop criterion remains open.
