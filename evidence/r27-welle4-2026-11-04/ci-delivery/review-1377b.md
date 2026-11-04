# CODEX-REVIEW — PR #1377 ci-delivery DSN, round 2

- Candidate: `5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9` (`work/r27-ci-delivery-dsn`; live PR #1377 head matches).
- Base: `develop` `ecbb88545f96473986f8f41394cffce58b97d2df` (live PR base; candidate has it as ancestor).
- Task: `t-20261022-r27-ci-delivery`.
- Verdict: **ACCEPT** (technical review only; no merge).

## Seven SHA-exact review points

1. **Write set — PASS.** `git diff ecbb88545f96473986f8f41394cffce58b97d2df...HEAD --name-only` returns exactly:
   - `internal/database/identity_tenant_resolver_integration_test.go`
   - `internal/database/tenant_integration_test.go`

2. **Missing test environment fails clearly — PASS.** Neither changed test contains `t.Skip`. Both fail at line 18 with `t.Fatal("testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt")`. My own run, with the variable explicitly unset:

   ```text
   env -u BASEHARBOR_TEST_DATABASE_URL go test ./internal/database -run '^(TestIdentityTenantResolverUsesIdentityScopedRLS|TestTenantRLSIsolation)$' -count=1 -v
   ```

   exited 1 and reported, for each test:

   ```text
   testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
   --- FAIL: TestIdentityTenantResolverUsesIdentityScopedRLS
   testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt
   --- FAIL: TestTenantRLSIsolation
   ```

   This is an explicit missing-fixture diagnosis, not a simulated connection refusal.

3. **Correct DSN runs both tests — PASS.** My own isolated PostgreSQL 18 instance and DSN `postgres://postgres:postgres@127.0.0.1:35433/baseharbor_test?sslmode=disable` ran both exact tests. Output:

   ```text
   --- PASS: TestIdentityTenantResolverUsesIdentityScopedRLS
   --- PASS: TestTenantRLSIsolation
   PASS
   ok github.com/mcpdev80/baseharbor/internal/database 0.468s
   ```

   The local fixture used a free private port because 5433 was already occupied by another container; the candidate's integration tests take the host/port solely from `BASEHARBOR_TEST_DATABASE_URL`. The hosted exact-SHA `go-unit-tests` job also succeeded (run `41878182617`).

4. **Wrong-port mutation — PASS.** My own mutation run used `postgres://postgres:postgres@127.0.0.1:1/baseharbor_test?sslmode=disable&connect_timeout=1`. Both tests failed at their first DB connection with the literal `dial tcp 127.0.0.1:1: connect: connection refused`; neither skipped or passed. Exit status was 1.

5. **Single DSN source — PASS.** `scripts/pr-unit-database.sh:11-16` starts Postgres and publishes the runner's port; `:32` exports the single `BASEHARBOR_TEST_DATABASE_URL` consumed by `go test ./...` at `:33`. Both integration tests use that same variable for the admin pool and derive their restricted-role DSNs by appending only `user`, `password`, and `connect_timeout` query parameters. Neither retains a hardcoded second port or second host.

6. **No test deleted or weakened into expected failure — PASS.** Comparing both test bodies against develop shows only two intended changes per test: missing DSN changes from `t.Skip` to clear `t.Fatal`, and the restricted-role connection changes from hardcoded `127.0.0.1:5432` to the shared DSN plus role credentials. Test assertions and behavior remain present; no tests were deleted or rewritten to expect an error.

7. **Package checks — PASS.** On the exact candidate worktree I ran:

   - `go test ./internal/database -count=1` with an isolated PostgreSQL database: PASS (`2.054s`).
   - `go build ./internal/database`: PASS.
   - `go vet ./internal/database`: PASS.
   - `gofmt -l` on both changed files: empty output (`gofmt clean`).

## Hosted gates

Live PR #1377 is OPEN, ready (not draft), and mergeable. Run `41878182617` completed successfully for exact head `5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9`. `PR Selected Checks` is terminal SUCCESS. Rollup: **8 SUCCESS / 0 FAILURE / 10 SKIPPED**. Skipped gates remain skipped, not claimed as passes. Required ordinary source, focused Python, go-build, go-unit-tests, go-vet, Trusted Plan, workflow policy, and selected-check aggregation all succeeded.

## Review boundary and END

Read-only review of exact candidate `5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9`; no product/workflow files changed, no hosted run triggered, and no merge performed. Local Postgres container and temporary Go caches were reviewer-owned and removed after the checks.

`END_DONE codex-r1377b: verdict=ACCEPT open=none | Beide Tests scheitern ohne DSN und am falschen Port reproduzierbar; mit isolierter Datenbank sind sie gruen, und der terminale Hosted-Run ist 8/0/10.`
