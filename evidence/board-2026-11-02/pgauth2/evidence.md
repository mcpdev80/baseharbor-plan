# pgauth2 — Evidence

## STATUS
DONE — real fix merged-ready, CI green, PR #1269.

## PLAN
1. [done] Read mission pgauth2.txt + baseharbor/AGENTS.md; establish branch `pgauth2-grant-openbao-backend` from develop.
2. [done] Run-Log: which role connects when.
3. [done] Locate init path: postgres-init / role provisioning for OpenBao.
4. [done] Minimal fix: GRANTs + DB ownership for OpenBao backend role (no superuser bypass).
5. [done] Proof: before/after reproduction + go test + regression test.
6. [done] PR #1269; watched PRSC terminal / CI.
7. [done] Card + evidence published.

## Run-Log (role connects when)
- Control-plane init runs as the `postgres` SUPERUSER (via postgres HAProxy) connecting to dbname `postgres`.
- It creates role `openbao` (`BASEHARBOR_OPENBAO_DB_USER`, non-superuser `LOGIN PASSWORD`) and database `openbao`, then grants the role connect on `openbao`.
- OpenBao's PG storage backend (compose.yaml openbao service, user 100, read-only) connects via the HCL `connection_url` `postgres://openbao:…@postgres:5432/openbao?sslmode=verify-ca`.
- The MCP/hosted `gh-hosted-sweep` scans ALL runtime container logs for `permission denied` (cmd/baha/core_installation_runtime_test.go:441). The observed FATAL was `permission denied for database "postgres" / "template1" / "openbao"` — the non-superuser backend role had PUBLIC connect revoked on postgres/template1 and could not connect to any DB the backend probed at startup.

## Root cause
The backend role was a restricted login with `REVOKE ALL ON DATABASE … FROM PUBLIC` applied to `openbao`, and no explicit grant to the `postgres`/`template1` databases it probes on startup → `permission denied`.

## Fix (commit 18c40aee)
In `internal/runtime/openbao_runtime_prepare.go`, `openbao-init.sh` now grants:
- `ALTER DATABASE openbao OWNER TO :openbao_user` (idempotent ownership)
- `GRANT CONNECT ON DATABASE openbao TO :openbao_user`
- `GRANT CONNECT, TEMPORARY ON DATABASE postgres TO :openbao_user`
- `GRANT CONNECT, TEMPORARY ON DATABASE template1 TO :openbao_user`

Role stays a restricted login — no Superuser bypass. App-role isolation is untouched: application roles still cannot connect to postgres/template1 (verified on a live postgres:18 container).

## Evidence / reproduction
- postgres:18 container, simulated stale prior run (openbao DB owned by postgres, PUBLIC revoked): all three `psql -U openbao -d {openbao,postgres,template1}` returned `FATAL: permission denied for database`.
- After applying the grant: all three return `1`. App role `app123` still cannot reach postgres/template1/other DBs.
- `go build ./...` OK, `go vet ./internal/runtime/` OK.
- `go test ./internal/runtime/ ./internal/openbao/ ./internal/application/` all green.
- Added `TestOpenBaoPostgresInitGrantsStorageRoleConnect` (source-level guard on generated openbao-init.sh).

## PR / CI
- PR: https://github.com/mcpdev80/baseharbor/pull/1269 — `fix(secrets): grant OpenBao postgres backend the right privileges`
- Branch: `pgauth2-grant-openbao-backend` (base develop), head SHA `18c40aee`.
- CI run #41392638044: **completed/success** (all gates incl. docker lifecycle acceptance).

## repo-rule compliance
- No `.github/workflows/*` edits, no `scripts/pr-*` edits, no subagent/codeman spawn, no merge (PR open, awaiting owner/Codex-MERGE). No interactive question dialog (QUESTION line used instead).
- Write set limited to `internal/runtime/openbao_runtime_prepare.go` (+ test). Targeted `git add` only.
- No secrets logged.
