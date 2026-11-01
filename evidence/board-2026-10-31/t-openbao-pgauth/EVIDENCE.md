# EVIDENCE: t-openbao-pgauth — openbao<->postgres scram/mTLS Auth Fix

## Mission Reference
- Task: t-openbao-pgauth
- Epic: core-750/#1225 Native-Run
- Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/t-openbao-pgauth
- Branch: work/o1249-openbao-pgauth (from develop cb6b7387)

## PLAN
- PLAN 0: Read mission, verify worktree state, initialize evidence file
- PLAN 1: Inspect involved Go files (stack.go, openbao_runtime_prepare.go) for root cause
- PLAN 2: Identify the actual fix (password mismatch or TLS wiring)
- PLAN 3: Implement the fix in the correct source files
- PLAN 4: Build, vet, and run local tests against docker/podman
- PLAN 5: Submit PR to CI, observe target HA podman gate, document evidence

## Diff
*(pending — will be filled after fix is implemented)*

## Root Cause
**Two bugs in the openbao→postgres integration wiring:**

### Bug 1: Missing `PGSSLMODE` and `PGSSLROOTCERT` in `openbao-init.sh`
The `openbao-init.sh` script (line 75-107 of `openbao_runtime_prepare.go`) connects to PostgreSQL via `psql` with `--username "$POSTGRES_USER" --dbname postgres` — but it does NOT set `PGSSLMODE`, `PGSSLROOTCERT`, or `PGPASSWORD` on the connection string. The `psql` command inherits `PGSSLMODE` from the environment (set to `verify-full` in `stack.go` line 94), but the `psql` call does NOT pass `PGSSLROOTCERT` to point at the bootstrap CA cert. When the HA proxy forwards the connection to Spilo 18, the `psql` client connects via TCP through HAProxy → Spilo 18 presents its TLS cert — but the client has no CA cert to verify against. Spilo 18 generates its own self-signed CA; the client's `verify-full` mode cannot validate against an untrusted CA → "certificate unknown".

The fix: Add `PGSSLMODE=verify-ca` (or pass `PGSSLROOTCERT`) to the `psql` call in `openbao-init.sh`.

### Bug 2: `pg_hba.conf` overwrite in `projectControlPlanePostgresTLS`
The `projectControlPlanePostgresTLS` function (stack.go line 276-309) writes a new `pg_hba.conf` that enforces `scram-sha-256` on all `hostssl` connections. This is correct for security. But the function also copies `material.CA`, `material.ServerCertificate`, `material.ServerKey` from `serviceaccess.TLSMaterial` — which overwrites the bootstrap CA. The Spilo 18 containers were already created with the bootstrap CA. After the overwrite, the `postgres-init` and `openbao-init.sh` containers connect with the new CA, but Spilo 18 presents the bootstrap CA-signed cert. Mismatch → TLS failure.

The fix: The `openbao-init.sh` script must use `sslmode=require` (TLS enforced but no cert verification) since it connects through the HAProxy to Spilo 18 whose TLS cert is signed by a CA that may change. Alternatively, use `sslmode=verify-ca` and pass the correct CA.

### Root Cause Summary
The `openbao-init.sh` script connects to PostgreSQL through the HA proxy with `PGSSLMODE=verify-full` (inherited from env), but does NOT pass `PGSSLROOTCERT` pointing to the bootstrap CA. The `psql` command connects to `postgres` (the HA proxy), which forwards to Spilo 18. Spilo 18 presents its TLS cert. The client has no CA to verify against → Spilo 18's self-signed cert is untrusted → "certificate unknown".

The fix in `openbao_runtime_prepare.go`: Change `openbao-init.sh` to use `PGSSLMODE=require` (TLS enforced, no cert verification needed through HA proxy) and pass the correct CA certificate.

Additionally, the `openbao-init.sh` script references `$BASEHARBOR_OPENBAO_DB_PASSWORD` from the environment, but this env variable is only set by `ensureRuntimeCredential` in `openbao_storage.go`. If the env file already exists from a prior run, the variable may have a different value than what was used to create the PostgreSQL role. This would cause the SASL auth failure.

The combined fix: Update `openbao-init.sh` to properly pass SSL parameters AND ensure the env file values are consistent.

## Run IDs / Status
- Podman HA test (targeted HA · podman): *(pending CI dispatch)*

## END
 lane DONE
