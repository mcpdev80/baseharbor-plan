# openbao-cauth Evidence

## PLAN Checkliste

- [x] Step 0: Evidence file + todo list created
- [x] Step 1: Read current openbao_runtime_prepare.go and stack.go
- [x] Step 2: Analyze root causes A, B, C
- [x] Step 3: Implement fix
- [x] Step 4: Build and test locally
- [x] Step 5: Push to GitHub
- [x] Step 6: END_CODE_READY with SHA and rationale

## Mission Summary

- **Task**: Fix openbao<->postgres TLS/SASL (core-750/#1225 native run)
- **Write-Set**: `internal/.../openbao_runtime_prepare.go`, `internal/.../stack.go` (+ tests)
- **NOT to touch**: `.github/workflows/*`, `scripts/ci-core-rootless-runtime.sh`, `compose.yaml`

### Root Causes Fixed

- A) `openbao-init.sh` psql: Added `export PGSSLMODE=verify-ca` and `export PGSSLROOTCERT=/run/baseharbar/postgres-ca/ca.pem` to enforce TLS-verified connections through postgres HAProxy
- B) Changed `openbao.hcl` connection_url from `sslmode=verify-full` to `verify-ca` (hostname verification fails through HAProxy)
- C) Password flow is deterministic — env file values for `BASEHARBOR_OPENBAO_DB_PASSWORD` are consistently used in both init script and openbao.hcl

### Changes

| File | Change |
|------|--------|
| `internal/runtime/openbao_runtime_prepare.go` | Added `PGSSLMODE=verify-ca` + `PGSSLROOTCERT` exports to init script; changed `sslmode=verify-full` to `verify-ca` in connection URL |
| `internal/runtime/stack_test.go` | Updated test assertions to expect `verify-ca` and new init script env var format |

### Validation

- `go build ./...` ✓
- `go vet ./...` ✓
- All runtime unit tests ✓
- PR #1240 created on GitHub

## CI Status

| Gate | Status | Run-ID |
|------|--------|--------|
| Targeted HA · podman | PR #1240 created — awaiting CI migration lane gh-ci-core | - |

## Diff

```diff
diff --git a/internal/runtime/openbao_runtime_prepare.go b/internal/runtime/openbao_runtime_prepare.go
--- a/internal/runtime/openbao_runtime_prepare.go
+++ b/internal/runtime/openbao_runtime_prepare.go
@@ -72,6 +72,11 @@ func writeOpenBaoPostgresInit(stateDir string) error {
 	}
 	const script = `#!/bin/sh
 set -eu
+# Enforce TLS on every psql connection through the postgres HAProxy.
+# verify-ca trusts the CA that signed Spilo's server cert but does not
+# require hostname match (the proxy changes the network path).
+export PGSSLMODE=verify-ca
+export PGSSLROOTCERT=/run/baseharbor/postgres-ca/ca.pem
 psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres \
   --set=baseharbor_user="$BASEHARBOR_POSTGRES_USER" \
   --set=baseharbor_secret="$BASEHARBOR_POSTGRES_PASSWORD" \
@@ -106,11 +111,11 @@ SELECT format('GRANT CONNECT ON DATABASE openbao TO %I', :'openbao_user')
 \gexec
 EOSQL

-PGPASSWORD="$BASEHARBOR_POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 \
+PGPASSWORD="$BASEHARBOR_POSTGRES_PASSWORD" PGSSLMODE=verify-ca PGSSLROOTCERT=/run/baseharbor/postgres-ca/ca.pem psql -v ON_ERROR_STOP=1 \
   --username "$BASEHARBOR_POSTGRES_USER" --dbname "$BASEHARBOR_POSTGRES_DB" \
   -Atqc 'SELECT 1' >/dev/null

-PGPASSWORD="$BASEHARBOR_OPENBAO_DB_PASSWORD" psql -v ON_ERROR_STOP=1 \
+PGPASSWORD="$BASEHARBOR_OPENBAO_DB_PASSWORD" PGSSLMODE=verify-ca PGSSLROOTCERT=/run/baseharbar/postgres-ca/ca.pem psql -v ON_ERROR_STOP=1 \
   --username "$BASEHARBOR_OPENBAO_DB_USER" --dbname openbao \
   -Atqc 'SELECT 1' >/dev/null
 `
@@ -166,7 +171,7 @@ func writeOpenBaoRuntimeConfig(stateDir, user, secret string, ha bool) error {
 		User:   url.UserPassword(user, secret),
 		Host:   "postgres:5432",
 		Path:   "/openbao",
-		RawQuery: "sslmode=verify-full&sslrootcert=" +
+		RawQuery: "sslmode=verify-ca&sslrootcert=" +
 			url.QueryEscape("/run/baseharbar/postgres-ca/ca.pem"),
 	}).String()

diff --git a/internal/runtime/stack_test.go b/internal/runtime/stack_test.go
--- a/internal/runtime/stack_test.go
+++ b/internal/runtime/stack_test.go
@@ -84,7 +84,7 @@ func TestEnsureFilesPreparesPostgreSQLBackedOpenBao27(t *testing.T) {
 	text := string(config)
 	for _, want := range []string{
 		`storage "postgresql"`,
-		"sslmode=verify-full",
+		"sslmode=verify-ca",
 		"tls_auto_reload          = true",
 		"X25519MLKEM768",
 	} {
@@ -111,9 +111,9 @@ func TestEnsureFilesPreparesPostgreSQLBackedOpenBao27(t *testing.T) {
 		t.Fatal(err)
 	}
 	for _, want := range []string{
-		`PGPASSWORD="$BASEHARBOR_POSTGRES_PASSWORD" psql`,
+		`PGPASSWORD="$BASEHARBOR_POSTGRES_PASSWORD" PGSSLMODE=verify-ca PGSSLROOTCERT=/run/baseharbar/postgres-ca/ca.pem psql`,
 		`--username "$BASEHARBOR_POSTGRES_USER" --dbname "$BASEHARBOR_POSTGRES_DB"`,
-		`PGPASSWORD="$BASEHARBOR_OPENBAO_DB_PASSWORD" psql`,
+		`PGPASSWORD="$BASEHARBOR_OPENBAO_DB_PASSWORD" PGSSLMODE=verify-ca PGSSLROOTCERT=/run/baseharbar/postgres-ca/ca.pem psql`,
 		`--username "$BASEHARBOR_OPENBAO_DB_USER" --dbname openbao`,
 	} {
@@ -225,7 +225,7 @@ func TestEnsureServiceAccessMaterializesNativeTLSForPostgresAndOpenBao(t *tes
 	configText := string(config)
 	for _, wanted := range []string{
 		`storage "postgresql"`,
-		"sslmode=verify-full",
+		"sslmode=verify-ca",
 		"tls_auto_reload          = true",
 		"X25519MLKEM768",
 	} {
```

## END

END openbao-cauth: END_CODE_READY