# CODEX-REVIEW 0427-134 r5 — PR #1457 candidate delta

## PLAN

1. Verify the candidate branch, PR head, develop head, and commit ancestry from remote refs.
2. Compare only `7da148a3..48a3e36f` and inspect the test plus the production branch mechanisms it claims to exercise.
3. Evaluate each requested counterfactual: trusted-local early return, lost `--no-browser` forwarding, and browser launch.
4. Check which hosted runs apply to the candidate SHA and record exact current PR checks.
5. Publish the review evidence to baseharbor-plan origin/main.

## Candidate and ancestry witnesses

- Repository: `mcpdev80/baseharbor`; base: `develop` at `618d23bde0870391541a8bbdf3ee103f22d70560`.
- Candidate branch `134-r3-ca-pkce`: `48a3e36fb627141c0434bdcd8b7249887faef9f5`.
- Current PR #1457 head: `83d175f54ea9aba432d192c87dfe6464e879e0df`; PR is open, non-draft, merge state `UNSTABLE`.
- GitHub compare confirms `83d175f5..48a3e36f` is linear and ahead by two commits: `7da148a36131b339a84b26942093e09be1e521bb`, then `48a3e36fb627141c0434bdcd8b7249887faef9f5`.
- The requested delta `7da148a3..48a3e36f` is exactly one commit and changes only `cmd/baha/operator_tenant_bootstrap_test.go` (228 additions, 14 deletions). No unrelated files or content are in this delta. The cumulative `83d175f5..48a3e36f` file set is `cmd/baha/operator_auth.go` plus that test file; the production parser/forwarding change is R4 context, not part of this R5 delta.

## Delta review

The rewritten `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` now uses `-e managed`, configures an in-process HTTPS OIDC server with a managed test CA, supplies an authorization-code file, and retains an unknown-leftover negative control (`cmd/baha/operator_tenant_bootstrap_test.go:105-163`). This is a meaningful improvement over R4's `dev` trusted-local path.

### Counterfactual results

- Trusted-local early return: the test checks that output does not contain `trusted local operator mode` (`cmd/baha/operator_tenant_bootstrap_test.go:152-154`), and the current early return emits that exact text before Login (`cmd/baha/operator_auth.go:44-50`). It therefore fails for the current known trusted-local early-return behavior. It does not assert a token exchange or other server-side proof that `operatorauth.Login` was reached, so an alternate silent early return is not excluded.
- `--no-browser` not forwarded: **not proven red**. The test supplies an auth-code file, so the headless code exchange can still complete if `NoBrowser` is false. The command passes the parsed flag to `TrustOptions.NoBrowser` at `cmd/baha/operator_auth.go:61-65`, but the test does not assert this value or observe browser launch.
- Browser launched: **not proven red**. `operatorauth.Login` calls `openBrowser` when `suppressBrowser(opts.NoBrowser)` is false (`internal/operatorauth/login.go:151-152`); `openBrowser` starts the platform launcher (`:294-309`). The launch error is ignored by Login, and the test has no launcher spy, fake executable, invocation marker, or equivalent assertion. It can complete its auth-code-file exchange while a browser launcher was attempted.

## Hosted run truth

- `gh run list --commit 48a3e36f` returned no hosted runs for the candidate branch SHA.
- The existing PR run 42467172096 is on old PR head `83d175f54ea9aba432d192c87dfe6464e879e0df`, so it does not validate the R5 delta. It is terminal failure: `PR Selected Checks`, Native Keycloak/Core Docker and Podman, and Native destroy retry Docker and Podman failed. Its Go unit, build, vet, gofmt, and documentation jobs passed, but those results belong to 83d175f5 only.
- Therefore no hosted result presently qualifies for 48a3e36f. After the fast-forward reaches PR #1457, a new run must report `headSha=48a3e36f` and terminal success for `PR Selected Checks`, `PR · Validation · go-unit-tests`, other required validation checks, and the card-required native Docker and Podman login/managed-CA acceptance cells. A candidate-branch local result or the earlier PR-head run cannot substitute. `.github/**` is Owner-owned; no workflow rerun or dispatch was made by this review.

## Verdict and correction recipe

**ROLLE: REVIEW — URTEIL: korrektur.** The R5 commit is scoped to one test file and enters the managed branch; it catches the current trusted-local message path. It does not distinguish the flag-forwarding regression from a browser-launch attempt, and no hosted run exists on this candidate SHA. The old PR-head run is red and stale for this delta.

- `cmd/baha/operator_tenant_bootstrap_test.go:142-154`: make the test prove Login was reached by asserting a token-exchange/server request or persisted authenticated principal, not only absence of the early-return string.
- In the same test, isolate and observe browser launching. Clear any `BASEHARBOR_NO_BROWSER` environment override, replace the Linux CI `xdg-open` executable with a temporary marker script (or use an equivalent explicit browser-launch seam), and assert no marker is created. The mutation that drops `NoBrowser: noBrowser` at `cmd/baha/operator_auth.go:64` must fail; the mutation that permits `openBrowser` at `internal/operatorauth/login.go:151-152` must fail.
- Recheck the unknown-leftover flag control after strengthening the main assertion.
- Stop criterion: no approve until those counterfactuals are demonstrated by the regression, the candidate is fast-forwarded to the PR, and the new exact-PR-head run is terminal green for `PR Selected Checks`, Go unit validation, and required native Docker/Podman acceptance. Preserve Owner ownership of workflow files.

## Review integrity

Read-only review; candidate and PR refs were checked after the source inspection and remained `48a3e36fb627141c0434bdcd8b7249887faef9f5` and `83d175f54ea9aba432d192c87dfe6464e879e0df`. Planning repository remote: `https://github.com/mcpdev80/baseharbor-plan.git`. Pre-publication witness: `64816a2d12aed82b86b3bb564fb1548069f38284 refs/heads/main`.

END_DONE 0427-134-review-r5 — KORREKTUR; reviewed delta 48a3e36f is test-only, but browser suppression counterfactual and hosted exact-head evidence remain outstanding.
