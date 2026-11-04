# w122 CI go-unit-tests PostgreSQL role-fixture / dial root-cause + isolated-DB fix

- Lane: w122-ci-pg-fixture (Worker). Coord: f49a3303.
- Repo: baseharbor (core). PR #1371 head: 9ac4e2c4. Branch: work/w96-production-wiring-f8ef4255.
- Scope note (Owner 2026-11-04): .github/** belongs to the Owner. No edits, no reruns. Report a failing check as STATE (check name + failing log line) and stop there. Also handle PR #1363 (head e45e85ed) in the same pass.

## 1. Reproduction (failing STATE)

Command against the current host port 5432 (the shared demo Postgres reached via the host haproxy, `bh-demo-docker-shared-postgres-1`, 127.0.0.1:5432->5432):

- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:source-test-password@127.0.0.1:5432/baseharbor_test?sslmode=disable" go test ./internal/database/ -run 'TestIdentityTenantResolverUsesIdentityScopedRLS|TestMigrationRollbackOwnsOnlyLatestChange' -count=1 -v`

Failing log line (verbatim):

- `failed to connect to user=postgres database=baseharbor_test: 127.0.0.1:5432 (127.0.0.1): server error: FATAL: pg_hba.conf rejects connection for host "172.18.0.5", user "postgres", database "baseharbor_test", no encryption (SQLSTATE 28000)`

Host context: `docker ps` shows 127.0.0.1:5432 bound by the shared demo haproxy over a shared member container. Not a resettable baseharbor_test schema; the proxy rejects the container-origin IP with SQLSTATE 28000. The `baseharbor_resolver_ci` / `baseharbor_runtime_ci` roles do not exist on the shared instance.

## 2. Exact cause (READ-only on .github/workflows/ci.yml)

- Job `pr_validations` ("PR · Validation · ${{ matrix.check }}"), matrix entry `go-unit-tests`, ci.yml ~line 802: `go-unit-tests) go test ./... -count=1 ;;`.
- The `pr_validations` job declares NO `services:` block and NO `postgres:` service and no per-job `env: BASEHARBOR_TEST_DATABASE_URL`. The matrix is produced by `scripts/pr-selected-runtime-matrix.py` (byte-identical to the #1372 branch: git diff empty), so `go-unit-tests` is a valid, always-selected selected-check gate.
- Effect on the runner: `go test ./...` reaches `internal/database`, whose integration tests skip when `BASEHARBOR_TEST_DATABASE_URL` is unset, but once set they connect to a Postgres that the job never exposes (dial error) or reaches via a shared proxy that rejects the connection (SQLSTATE 28000) and has no `baseharbor_test` schema / no `baseharbor_resolver_ci` role (role fixture mismatch).

Affected test helpers (connection + role setup):

- `internal/database/identity_tenant_resolver_integration_test.go` line 85 (was): `runtimeDSN := "postgres://baseharbor_resolver_ci:...@127.0.0.1:5432/baseharbor_test?sslmode=disable"` — host/port 5432 hardcoded; runtime role granted SELECT only.
- `internal/database/tenant_integration_test.go` line 78 (was): `runtimeDSN := "postgres://baseharbor_runtime_ci:...@127.0.0.1:5432/baseharbor_test?sslmode=disable"` — same hardcoded 5432.
- `internal/database/migration_rollback_integration_test.go` line ~21: `dsn := os.Getenv("BASEHARBOR_TEST_DATABASE_URL")` — uses the env DSN (correct), connects to 127.0.0.1:5432 via that env.

Pattern already present on the #1372 branch (`2a43984a`, merged into develop via PR #1372, NOT an ancestor of this branch):

- `.github/workflows/ci.yml`: `go-unit-tests) bash scripts/pr-unit-database.sh ;;`.
- `scripts/pr-unit-database.sh`: ephemeral `postgres:18-alpine` container published on `127.0.0.1:5433`, health-warmed, exporting `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5433/baseharbor_test?sslmode=disable"` before `go test ./... -count=1`.
- `scripts/test_pr_unit_database_route.py`: asserts the script + route exist exactly once.
- Diff of `.github/workflows/ci.yml` between `2a43984a` and this branch shows only the `go-unit-tests` line reverted (script removed) and the regression-test step removed.

## 3. Scope decision: worker field vs owner field

- The canonical #1372 fix lives in a NEW helper `scripts/pr-unit-database.sh` (runner provisioning via `docker run`) that the CI job calls. That script + the edited `.github/workflows/ci.yml` line = runner provisioning + the Owner-owned workflow file. Both are OUTSIDE the Worker write-set (mission scope split).
- The remaining failure for the two hardcoded-5432 tests (resolver, tenant) CAN be fixed in the worker field: derive the runtime DSN host/port/password from `BASEHARBOR_TEST_DATABASE_URL` (already available in the ephemeral fixture) instead of hard-coding 127.0.0.1:5432. No .github edit, no t.Skip, no env trick that silences the case: the dedicated-role RLS/custom-setting assertions still run over the role connection.

## 4. Fix applied in the worker field (NO .github/** change)

- New file `internal/database/test_runtime_dsn_test.go`: helper `runtimeDSNFromEnv(t, role, password)` parses `BASEHARBOR_TEST_DATABASE_URL`, rewrites only user/host/port/password to the given role+password, returns the resulting DSN. The roles the tests create via the admin pool live on that same fixture, so no fixture change and no silencing.
- `internal/database/identity_tenant_resolver_integration_test.go`: `runtimeDSN := runtimeDSNFromEnv(t, "baseharbor_resolver_ci", runtimePassword)` (replaced hardcoded 5432).
- `internal/database/tenant_integration_test.go`: `runtimeDSN := runtimeDSNFromEnv(t, "baseharbor_runtime_ci", runtimePassword)` (replaced hardcoded 5432).

## 5. DREITEN-NACHWEIS (three named tests, corrected stand = isolated ephemeral postgres on 127.0.0.1:5434, baseharbor_test)

Isolated fixture started for local verification only (diagnostic; not runner infra):

- `docker run --detach --rm --name w122-pg-fresh5434 --publish 127.0.0.1:5434:5432 --env POSTGRES_DB=baseharbor_test --env POSTGRES_USER=postgres --env POSTGRES_PASSWORD=postgres postgres:18-alpine`

Individual runs:

- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5434/baseharbor_test?sslmode=disable" go test ./internal/database/ -run '^TestIdentityTenantResolverUsesIdentityScopedRLS$' -count=1` => **RED before fix**: `SQLSTATE 28000 ... 127.0.0.1:5432`; **GREEN after fix**: `ok ... 0.34s`.
- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5434/baseharbor_test?sslmode=disable" go test ./internal/database/ -run '^TestTenantRLSIsolation$' -count=1` => **RED before fix**: `SQLSTATE 28000 ... 127.0.0.1:5432`; **GREEN after fix**: `ok ... 0.33s`.
- `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5434/baseharbor_test?sslmode=disable" go test ./internal/database/ -run '^TestMigrationRollbackOwnsOnlyLatestChange$' -count=1` => FAIL (see section 6 — genuine w96 migration 0009 regression; production-migration Owner field).

Full package after the DSN fix: `go test ./internal/database/ -count=1` => 12 PASS, 1 FAIL (`TestMigrationRollbackOwnsOnlyLatestChange` only). `go test ./contracts/...` => ok. `go test ./cmd/baha -run '^TestDoctor'` => ok. Red->green verified: same tests RED on host 5432 (SQLSTATE 28000), GREEN after the DSN change, no skip, no t.Setenv trick.

## 6. TestMigrationRollbackOwnsOnlyLatestChange — NEBENEINANDER on develop ecbb8854 vs PR #1371 9ac4e2c4

- develop (ecbb8854, 8 migrations, 0008 is latest): `go test ./internal/database/ -run '^TestMigrationRollbackOwnsOnlyLatestChange$'` => **PASS** (0.34s).
- PR #1371 (9ac4e2c4, 9 migrations; w96 adds 0009_workstation_enrollment on top of 0008): same test => **FAIL** at migration_rollback_integration_test.go:31 (`membership context rollback changed earlier security ownership`).
- Verdict: NOT a pre-existing develop condition. It is a genuine regression introduced by the w96 migration 0009. Mechanism (instrumented): the test's first phase `verifyMembershipContextRollback` asserts that the FIRST `RollbackLast` removes 0008's `NULLIF` tenant-isolation correction. With 0009 on top, the first rollback removes 0009 (workstation_enrollment), leaving 0008's NULLIF correction in place -> `safeContext=true` -> assertion fires. Before 0009, the first rollback removed 0008 directly -> `safeContext=false` -> test passed.
- Evidence for the anmeldungs-kette (production-migration decision, Owner field; Worker edits NO migration files):
  - Test: `TestMigrationRollbackOwnsOnlyLatestChange`, file `internal/database/migration_rollback_integration_test.go`, assertion at **line 31** (`membership context rollback changed earlier security ownership`, inside `verifyMembershipContextRollback`).
  - Both SHAs: **develop = ecbb8854** (8 migrations, 0008 latest) => **PASS**; **PR #1371 head = 9ac4e2c4** (9 migrations) => **FAIL** at line 31.
  - Exact first-rollback target that breaks it: `RollbackLast` on 9ac4e2c4 removes **`0009_workstation_enrollment.sql`** (its down-file `0009_workstation_enrollment.down.sql` = `DROP TABLE ... workstation_enrollment_registry; DROP TABLE ... workstation_enrollment_grants;`), which does NOT touch 0008 -> 0008's `NULLIF` tenant-isolation correction remains -> the line-31 assertion fires. On ecbb8854 the same first `RollbackLast` removes **`0008_membership_empty_tenant_context.sql`** and clears the NULLIF -> test passes.
  - This is a production migration-ordering/ownership question (fold 0009 into 0008, or otherwise make 0008 the latest-rollback layer, or add a 0009 rollback phase to the test) — Owner/migration-design decision. No test-environment fix can resolve it.
- This is a production-migration ordering/ownership question (fold 0009 into 0008, or otherwise restore 0008 as the latest-rollback layer), not a test-environment question. It cannot be fixed by the ephemeral-DB mechanism (#1372) and cannot be fixed by the DSN helper. It sits in the production migration chain I authored.

## 7. PR #1363 (head e45e85ed, base develop, open, non-draft)

- PR #1363 is already built on top of the merged #1372 fix: `.github/workflows/ci.yml` line 803 = `go-unit-tests) bash scripts/pr-unit-database.sh ;;`, and `scripts/pr-unit-database.sh` exists. So its two red checks are NOT the missing-script issue that #1371 has.
- Same failing-family diagnosis applies to #1363's `go-unit-tests`: on a clean runner the ephemeral 5433 fixture is provided, but the resolver/tenant tests hardcode 127.0.0.1:5432 for their runtime role connection, so they would still hit SQLSTATE 28000 there. My DSN fix (worker field) covers that same class for any branch that carries it.
- #1363's head also carries the w96 migration 0009 (it descends from the same develop merge), so `TestMigrationRollbackOwnsOnlyLatestChange` fails on #1363 for the same migration-ordering regression as #1371 (section 6).
- State recorded for both PRs; no rerun triggered; .github/** untouched.

## 8. CI result

- Not reached: STOP + escalate on the migration-ordering regression (section 6), which is a production-migration decision (Owner field). No .github/** edit, no rerun, no push. Hosted checks not observed.

## 9. Partial success summary

- Worker-field fix applied and proven red->green for the two hardcoded-5432 tests (resolver + tenant) against an isolated ephemeral Postgres: no skip, no env trick, dedicated-role assertions still run.
- Root cause of the dial/role-fixture (ci.yml:802, no isolated DB) documented with file:line for the Owner to raise against ci.yml:802.
- Genuine production regression (w96 migration 0009 breaking `TestMigrationRollbackOwnsOnlyLatestChange`, develop=PASS vs 9ac4e2c4=FAIL) documented with exact first-rollback target and both SHAs for the anmeldungs-kette.
- .github/** untouched, no rerun, no push.

## END

- Lane w122-ci-pg-fixture: END_DONE (partial success). DSN fix applied + proven red->green for the 2/3 tests (no skip, no env trick). Root cause (ci.yml:802) and genuine w96 migration 0009 regression documented with evidence for the Owner/anmeldungs-kette. No .github/** edit, no rerun, no push.
