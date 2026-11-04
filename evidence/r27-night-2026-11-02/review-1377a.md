# CODEX-REVIEW — PR #1377 CI delivery DSN

- Candidate: `029e3ddd522b63114279d59d5af741ec417ca010` (SHA exact; branch and PR agree)
- Base: `ecbb88545f96473986f8f41394cffce58b97d2df` (`develop`, verified as ancestor and against `ls-remote`)
- PR: OPEN, ready, mergeable. Current hosted state is **not terminal**: `go-unit-tests` is still in progress; `PR Selected Checks` is skipped. Other completed statuses include successful build/vet, policy, plan, source-format and focused Python jobs.
- Verdict: **REJECT**. No approval or merge.

## Seven SHA-exact probes

1. **Write-set — PASS.** `git diff --name-only` shows exactly `internal/database/identity_tenant_resolver_integration_test.go` and `internal/database/tenant_integration_test.go`; no product file, helper, or `.github` path changed.

2. **Hard-coded address/port removed from the two tests — PASS.** Both runtime DSNs now derive host/port/database from `BASEHARBOR_TEST_DATABASE_URL` and append only the test-role credentials and a connect timeout. There is no fixed localhost/port in the changed test bodies.

3. **Missing environment is reported distinctly and does not go green as skipped — FAIL.** Both tests still use `t.Skip("BASEHARBOR_TEST_DATABASE_URL is not set")` at line 18. I ran the two exact tests with the variable unset: both reported `SKIP`, while `go test` returned `PASS`. The message names the missing input, but the integration coverage becomes a green skip, contrary to this mission's explicit requirement.

4. **Own false-port mutation — PASS.** In an archive of the exact SHA, I set `BASEHARBOR_TEST_DATABASE_URL` to a local PostgreSQL DSN using port `59999` and ran `TestIdentityTenantResolverUsesIdentityScopedRLS` and `TestTenantRLSIsolation`. Both executed and failed red at the first database operation with `connect: connection refused`; neither skipped. This confirms the configured endpoint controls the test path. No product workspace was modified.

5. **Single source as `scripts/pr-unit-database.sh` — PASS.** The script exports `BASEHARBOR_TEST_DATABASE_URL` for its ephemeral PostgreSQL fixture at `127.0.0.1:5433`; both tests read that exact variable and derive their runtime DSNs from it. No second host/port setting was introduced.

6. **Package tests, build, gofmt and vet — PARTIAL.** On the exact-SHA archive, `go test ./internal/database -count=1`, `go build -buildvcs=false ./internal/database`, `go vet ./internal/database` and gofmt inspection passed. In the no-DSN package run, the two target tests skipped, so the package PASS does not establish their execution. The false-port mutation run independently confirms they fail when pointed at an unavailable endpoint. Hosted `go-unit-tests` remains in progress, and `PR Selected Checks` is skipped; do not count either as terminal green.

7. **No test deleted or changed into expected failure — PASS.** The diff changes only each runtime DSN from a literal localhost string to the configured environment value plus credentials/timeout. No assertion, setup, or test body was removed or weakened.

## REZEPT

- **Files:** `baseharbor/internal/database/identity_tenant_resolver_integration_test.go` and `baseharbor/internal/database/tenant_integration_test.go`.
- **Change:** make absence of `BASEHARBOR_TEST_DATABASE_URL` a clear test failure (or an explicit typed environment-precondition result that cannot be reported as a successful skipped test under this mission). Keep both DSNs derived from the fixture script's single environment variable.
- **Test requirement:** with the variable unset, both target tests must fail visibly rather than skip; with the valid fixture DSN, both must execute and pass; with a deliberately wrong port, both must execute and fail red. Re-run package tests, build, gofmt and vet, and observe the exact candidate's required hosted checks to terminal status.
- **Stop criterion:** reject if missing database configuration still produces a skipped/green test, if a wrong endpoint does not fail, if either test gains a second connection source, or if required hosted checks remain skipped, red, or nonterminal.

## Review boundary and END

Read-only review of exact candidate `029e3ddd522b63114279d59d5af741ec417ca010`; mutation was only an environment override in a temporary archive. The current PR CI run was re-read and is still nonterminal. No merge performed.

END_DONE codex-r1377a: verdict=REJECT open=missing-dsn-green-skip,hosted-go-unit-nonterminal,pr-selected-checks-skipped | With the DSN unset, both integration tests skip and the package reports PASS.
