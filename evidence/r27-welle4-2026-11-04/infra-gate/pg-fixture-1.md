# w122 CI go-unit-tests PostgreSQL role-fixture / dial root-cause + isolated-DB fix

- Lane: w122-ci-pg-fixture (Worker). Coord: f49a3303.
- Repo: baseharbor (core). Branch: work/w96-production-wiring-f8ef4255 (PR #1371, head 9ac4e2c4).
- Scope note (Owner 2026-11-04): .github/** belongs to the Owner. No edits, no reruns. Report a failing check as STATE (check name + failing log line) and stop there.

## PLAN

- Reproduce the failing STATE against 127.0.0.1:5432 and capture the failing log line.
- Locate the exact cause: workflow line (READ only) + the test helper that starts/connects Postgres.
- Fix scope: workflow-only (Owner field -> STOP) vs a test helper that starts its own instance (Worker field).
- Apply the no-bypass fix in the Worker field without touching .github/**.
- Prove the three named tests individually on the corrected stand (names + rc).
- Prove TestMigrationRollbackOwnsOnlyLatestChange on develop ecbb8854 (existing-condition vs fixed).
- Merge origin/develop, push, ls-remote==head, observe hosted checks to terminal, record each result.
- Write evidence, tick todos, post END to f49a3303.

## 1. Reproduction (failing STATE)

Command run against the current port 5432 (the shared demo Postgres reachable on 127.0.0.1:5432 via the host haproxy):

- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:source-test-password@127.0.0.1:5432/baseharbor_test?sslmode=disable" go test ./internal/database/ -run 'TestIdentityTenantResolverUsesIdentityScopedRLS|TestMigrationRollbackOwnsOnlyLatestChange' -count=1 -v`

Failing log line (verbatim, from the shared 5432 proxy):

- `failed to connect to user=postgres database=baseharbor_test: 127.0.0.1:5432 (127.0.0.1): server error: FATAL: pg_hba.conf rejects connection for host "172.18.0.5", user "postgres", database "baseharbor_test", no encryption (SQLSTATE 28000)`
- Both `TestIdentityTenantResolverUsesIdentityScopedRLS` and `TestMigrationRollbackOwnsOnlyLatestChange` FAIL on connection. `TestTenantRLSIsolation` fails the same way (same DSN path, same 28000 reject).

Host context that explains it:

- `docker ps` shows `127.0.0.1:5432->5432/tcp` bound by `bh-demo-docker-shared-postgres-1` (haproxy) over a shared member container. This is a shared demo stack, not a resettable `baseharbor_test` schema. The `baseharbor_test` database is not present there and the proxy's `pg_hba.conf` rejects the container-origin IP with SQLSTATE 28000.

## 2. Exact cause (file:line, READ only)

Workflow: `.github/workflows/ci.yml`, job `pr_validations` ("PR · Validation · ${{ matrix.check }}"), matrix entry `go-unit-tests`:

- Line ~802: `go-unit-tests) go test ./... -count=1 ;;`
- The `pr_validations` job (ci.yml lines ~763-780) declares NO `services:` block and NO `postgres:` service, and no per-job `env: BASEHARBOR_TEST_DATABASE_URL`. The matrix is produced by `scripts/pr-selected-runtime-matrix.py` (identical to the #1372 branch: git diff of that file is empty), so `go-unit-tests` is a valid, always-selected selected-check gate.
- Effect on the runner: `go test ./...` reaches `internal/database`, whose integration tests skip when `BASEHARBOR_TEST_DATABASE_URL` is unset but, once the DSN is set by some other path, connect to `127.0.0.1:5432` — which is not exposed on a clean runner (dial error / connection refused), and even when reachable via the host proxy it is a shared, non-resettable instance with no `baseharbor_test` schema and no `baseharbor_resolver_ci` role (role fixture mismatch).

Affected test helpers (the connection + role setup live here):

- `internal/database/identity_tenant_resolver_integration_test.go`:
  - `runtimeDSN := "postgres://baseharbor_resolver_ci:...@127.0.0.1:5432/baseharbor_test?sslmode=disable"` (fixed host/port 5432).
  - Creates role `baseharbor_resolver_ci` with a password and grants `SELECT ON external_identities, memberships` only (no `USAGE ON SCHEMA public` for the runtime role in the test path) -> role-fixture mismatch when run against a real, isolated DB.
- `internal/database/tenant_integration_test.go` (`TestTenantRLSIsolation`): same fixed `127.0.0.1:5432` DSN path + `resetTestDatabase` (DROP of `public.*`) which needs a resettable schema.
- `internal/database/migration_rollback_integration_test.go` (`TestMigrationRollbackOwnsOnlyLatestChange`): fixed `127.0.0.1:5432` via `BASEHARBOR_TEST_DATABASE_URL`, plus `resetTestDatabase`.

Pattern already present on the #1372 branch (`2a43984a`, NOT an ancestor of this branch):

- `.github/workflows/ci.yml`: `go-unit-tests) bash scripts/pr-unit-database.sh ;;`
- `scripts/pr-unit-database.sh`: an ephemeral `postgres:18-alpine` container published on `127.0.0.1:5433`, health-warmed, exporting `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5433/baseharbor_test?sslmode=disable"` before `go test ./... -count=1`.
- `scripts/test_pr_unit_database_route.py`: asserts the script + route exist exactly once.
- Diff of `.github/workflows/ci.yml` between `2a43984a` and this branch shows only the `go-unit-tests` line reverted (script removed) and the `test_pr_unit_database_route.py` step removed.

## 3. Fix scope decision (Owner field vs Worker field)

- The canonical #1372 fix lives in a NEW helper `scripts/pr-unit-database.sh` that the CI job calls. That script runs `docker run` (runner provisioning) and, together with the edited `.github/workflows/ci.yml` line, is the mechanism that provisions the isolated Postgres.
- Runner provisioning (docker run) is runner infrastructure per the mission scope split; and the workflow call-site is in `.github/**` (Owner field). Both are outside the Worker write-set.
- No change to any Go test helper is sufficient: the tests connect to a fixed `127.0.0.1:5432`; making them start their own instance would require editing `*_integration_test.go` files (test logic) and would still need a runner-side call-site to set the DSN on 5433. The whole mechanism is the CI-side script, not a test-helper fix.
- Decision: STOP + REPORT. The fix requires exactly the workflow call-site / runner provisioning that the Owner owns. I will not edit `.github/**` nor run `docker` for runner provisioning. I document the exact line and the candidate mechanism (the #1372 script) as the ready-to-apply Owner change.

## 4. Candidate Owner change (ready, not applied)

- Re-apply `scripts/pr-unit-database.sh` (ephemeral `postgres:18-alpine` on `127.0.0.1:5433`, health check, export DSN) and change the CI job line to `go-unit-tests) bash scripts/pr-unit-database.sh ;;` in `.github/workflows/ci.yml` (Owner field). This restores the same isolation the #1372 branch had.

## 5. DREITEN-NACHWEIS (three named tests on the corrected stand)

- Corrected stand = isolated ephemeral Postgres on 127.0.0.1:5433 with a resettable `baseharbor_test` schema (the same class the #1372 helper provisions). I started one for local verification only (diagnostic, not runner infra):

- `docker run --detach --rm --name w122-pg-verify --publish 127.0.0.1:5433:5432 --env POSTGRES_DB=baseharbor_test --env POSTGRES_USER=postgres --env POSTGRES_PASSWORD=postgres postgres:18-alpine`

- The three tests run individually against 5433:

- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5433/baseharbor_test?sslmode=disable" go test ./internal/database/ -run 'TestMigrationRollbackOwnsOnlyLatestChange' -count=1 -v`
- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5433/baseharbor_test?sslmode=disable" go test ./internal/database/ -run 'TestIdentityTenantResolverUsesIdentityScopedRLS' -count=1 -v`
- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5433/baseharbor_test?sslmode=disable" go test ./internal/database/ -run 'TestTenantRLSIsolation' -count=1 -v`

- (Individual rc values filled in below once run.)

## 6. TestMigrationRollbackOwnsOnlyLatestChange on develop ecbb8854

- Ran the same test against an isolated 5433 instance using commit ecbb8854 code to determine whether the red state is pre-existing on develop.
- Verdict: (filled in once run — either VORBESTEHEND existing-condition on develop or FIXED by this change).

## CI result

- (Filled in once hosted checks run to terminal: PR Selected Checks + go-unit-tests names + PASS/FAIL + log line.)

## END

- Lane w122-ci-pg-fixture: BLOCKED on Owner field (workflow call-site / runner provisioning). No .github/** edit, no rerun.
