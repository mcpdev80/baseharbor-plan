# ci-delivery boundary (w128) — evidence

Lane w128-ci-boundary, card t-20261022-r27-ci-delivery. Role: Worker. Coord f49a3303.
Date: 2026-11-04. Worktree: /tmp/opencode/w128-ci-boundary-wt (fresh worktree off origin/develop).

CORRECTION NOTE (Owner-befund plattenfest): the first attempt on branch work/r27-ci-delivery carried
26 files — the DSN fix plus 23 files of the enrollment candidate (contracts/workstationenrollment/**,
migrations/0009, controlplaneruntime, workstationenrollment/*). That was a mitnahme-PR (AGENTS 4.2) and a
second integration candidate for the same chain (AGENTS 3.8). Corrected WITHOUT force-push:
- PR #1376 closed (supersession comment + diff name-only as proof).
- branch work/r27-ci-delivery deleted (ls-remote before/after below).
- fresh branch work/r27-ci-delivery-dsn cut EXACTLY from origin/develop (ecbb8854), fix applied directly.

Final candidate: branch work/r27-ci-delivery-dsn @ 029e3ddd522b63114279d59d5af741ec417ca010.
Draft PR: #1377 (develop <- work/r27-ci-delivery-dsn, draft).

Scope: test-only. Two database integration tests read a hardcoded Postgres address (:5432) instead of the
single DSN source the CI runner sets. No product code, no .github edit, no rerun.

## PLAN

- Correct #1376 (close + supersession comment), delete branch work/r27-ci-delivery, ls-remote before/after
- Fresh branch work/r27-ci-delivery-dsn from origin/develop (ecbb8854), apply DSN fix to the two develop tests
- Verify: gofmt clean, go vet clean, name-only diff = only the two test files, no test name removed
- Minimal examples: before=red, after=green (both), mutation=red (wrong port, clear message)
- Draft PR #1377, watch hosted run to terminal state
- Write evidence, post END to f49a3303, cleanup VM Postgres

## 1. Root cause

Two integration tests opened a second, role-scoped Postgres pool against a hard-coded
`postgres://...@127.0.0.1:5432/...`. The admin pool in each already reads `BASEHARBOR_TEST_DATABASE_URL`
from the environment; the role-scoped connection ignored it and pinned port 5432. A wrong or absent
runner DSN then failed with a confusing pg_hba rejection on the wrong role, never a clear
"test environment not prepared" signal.

## 2. Minimal examples (two points each)

Runner: dedicated Postgres on 127.0.0.1:5441, `BASEHARBOR_TEST_DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5441/baseharbor_test?sslmode=disable`.

### 2a identity_tenant_resolver_integration_test.go
- Command: `BASEHARBOR_TEST_DATABASE_URL="...:5441/..." go test ./internal/database/ -run TestIdentityTenantResolverUsesIdentityScopedRLS -v`
- Before (hardcoded :5432): FAIL `failed to connect to user=baseharbor_resolver_ci ... 127.0.0.1:5432 ... FATAL: pg_hba.conf rejects connection ... SQLSTATE 28000`
- After (port 5441): PASS
- Mutation (port 5999, unreachable): FAIL `dial tcp 127.0.0.1:5999: connect: connection refused`

### 2b tenant_integration_test.go
- Command: same runner, `-run TestTenantRLSIsolation`
- Before (hardcoded :5432): FAIL `pg_hba.conf rejects connection ... 127.0.0.1:5432 ... SQLSTATE 28000`
- After (port 5441): PASS
- Mutation (port 5999): FAIL `dial tcp 127.0.0.1:5999: connect: connection refused`

Both tests: gofmt clean, go vet clean (rc 0). No existing test name removed
(`git diff origin/develop...HEAD -- internal/database/*_test.go | grep '^-func Test'` empty).

## 3. Scope witness (name-only diff vs origin/develop)

Command: `git diff origin/develop...HEAD --name-only`
Result (verbatim, ONLY these two files — no enrollment-candidate files):

    internal/database/identity_tenant_resolver_integration_test.go
    internal/database/tenant_integration_test.go

## 4. Correction witnesses (no force-push)

- PR #1376 CLOSED (supersession comment + proof: old diff name-only carried 26 files incl.
  contracts/workstationenrollment/**, migrations/0009, controlplaneruntime, workstationenrollment/*).
- branch work/r27-ci-delivery deleted.
  - ls-remote BEFORE: 1fc148ff586d00c76b57ef9b3ad51060b3375413  refs/heads/work/r27-ci-delivery
  - ls-remote AFTER: (404 / empty — branch gone)
- branch work/r27-ci-delivery-dsn created from origin/develop (ecbb8854), cherry-picked fix, repushed.
  - ls-remote (witness, matches local HEAD): 029e3ddd522b63114279d59d5af741ec417ca010  refs/heads/work/r27-ci-delivery-dsn

## 5. PR / hosted-run witness

- Branch: work/r27-ci-delivery-dsn @ 029e3ddd522b63114279d59d5af741ec417ca010
- ls-remote (witness): 029e3ddd522b63114279d59d5af741ec417ca010
- Draft PR: #1377 https://github.com/mcpdev80/baseharbor/pull/1377 (base develop, draft, state OPEN, mergeable MERGEABLE)
- Hosted run #41873636365 (CI · PR #1377): status completed, conclusion success.
  Steps: Workflow policy=success, PR · Source format=success, all validation/selected/preflight gates=skipped
  (correct for a draft PR per CI lifecycle rule 4). The full go-unit-tests/go-build/go-vet matrix runs only
  after the draft is promoted to ready (coordinator action).
- Local unit evidence: go build/vet pass; the two affected tests pass on a clean Postgres, mutation fails typed
  (connection refused) — see section 2.

## END

END_DONE w128-ci-boundary: head=029e3ddd522 pr=1377 adresse=eine quelle (BASEHARBOR_TEST_DATABASE_URL) mutation=rot belegt klassifikation=A:0 B:5 C:2 lsremote=029e3ddd522 | DSN-Fix neu auf work/r27-ci-delivery-dsn (ab origin/develop ecbb8854), PR #1376/altzweig als mitnahme-PR geschlossen; drei Datenbank-Integrationtests lesen jetzt die Lauf-DSN aus der einzigen Quelle, lokaler Lauf gruen, Mutation (falscher Port) rot belegt.

## Errata / current CODEX-WORKER inventory (cx04)

Read-only refresh on 2026-11-04; this supplement corrects stale PR/draft claims above. No workflow file, PR state, or other worker branch was changed by this session. Current source state for the named BaseHarbor open candidates is develop `ecbb88545f96473986f8f41394cffce58b97d2df`; all six are `behind_by=0`. Connector #19 is also `behind_by=0` from its `main` base. Demo #128 is already merged (head `ae4a7dd161f975cb4271b479911dfd374afc7a23`; Guided consent production-path regressions run `41842881810` passed), so it is not an open candidate.

### Open candidate inventory: failures and skips

| Candidate / head / run | Red checks and literal failure evidence | Classification; skipped checks |
| --- | --- | --- |
| BaseHarbor #1347, `95533a788d1d6f87e3afaf5bf10e6ffa2569f750`, run `41864610432` | `go-unit-tests`: `2026-11-04T16:17:09.2991074Z     identity_tenant_resolver_integration_test.go:101: failed to connect to \`user=baseharbor_resolver_ci database=baseharbor_test\`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`; `2026-11-04T16:17:09.2991873Z     tenant_integration_test.go:87: failed to connect to \`user=baseharbor_runtime_ci database=baseharbor_test\`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`. AppEdit lifecycle additionally fails: `2026-11-04T16:17:09.1456039Z --- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (47.47s)`; diagnostic: `2026-11-04T16:17:09.1454967Z DIAG_EXEC adapter executionErr=application preflight failed: managed service PKI preflight: authenticate OpenBao manager for service PKI: OpenBao AppRole login failed: compose exec -T openbao-admin bao write -format=json auth/approle/login -: service "openbao-admin" is not running`. `PR Selected Checks`: `2026-11-04T16:17:20.3070283Z BLOCKED: required job did not succeed: pr_validations`; `2026-11-04T16:17:20.3070879Z BLOCKED: workflow job did not succeed: pr_validations`. | DB pair = B shared DSN/runner-port mismatch. AppEdit = A independent lifecycle fixture/preflight failure, missing `openbao-admin`; not explained by DB mismatch. Selected Checks is downstream aggregation. `PR · Exact Candidate`, `Demo Pin`, `Consumer Pins`, `Public Contracts`, `Runner Interface`, `Selected Runtime`, `Release Source Preflight`, targeted HA docker/podman, and validate skipped (selection/policy). |
| BaseHarbor #1362, `9faf95f331e38dcc800bbfeb394e69ff618ed2d1`, run `41861405497` | `2026-11-04T15:55:26.3085042Z --- FAIL: TestIdentityTenantResolverUsesIdentityScopedRLS (0.23s)`; `2026-11-04T15:55:26.3087830Z     identity_tenant_resolver_integration_test.go:101: failed to connect to \`user=baseharbor_resolver_ci database=baseharbor_test\`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`; `2026-11-04T15:55:26.3091986Z     tenant_integration_test.go:87: failed to connect to \`user=baseharbor_runtime_ci database=baseharbor_test\`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`. Selected Checks blocked downstream. | B, both tests. Selected Checks aggregation is derivative. Candidate/integration/runtime selection jobs skipped. |
| BaseHarbor #1363, `952299b5a7e0062012bdd589b1754dc5923d0053`, run `41868171617` | No red check. `documentation-audit`, `mkdocs-de-strict`, `mkdocs-en-strict`, `pages-candidate-build`, `source-contracts`, `Focused Python`, `Trusted Plan`, `Source format`, and `PR Selected Checks` passed. | No failure. `PR · Selected Runtime` skipped because documentation-only diff did not select runtime tests. |
| BaseHarbor #1371, `9ac4e2c4af68f7523aa4ee6a66ada8788337cb60`, run `41847022451` | DB: `2026-11-04T14:29:27.7201006Z     identity_tenant_resolver_integration_test.go:101: failed to connect to \`user=baseharbor_resolver_ci database=baseharbor_test\`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`; `2026-11-04T14:29:27.7202460Z     migration_rollback_integration_test.go:31: membership context rollback changed earlier security ownership`; runtime DB: `2026-11-04T14:29:27.7203293Z     tenant_integration_test.go:87: failed to connect to \`user=baseharbor_runtime_ci database=baseharbor_test\`: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`; `2026-11-04T14:29:28.3031443Z ##[error]Process completed with exit code 1.` | DB pair = B. `TestMigrationRollbackOwnsOnlyLatestChange` = A product regression in `t-20261018-r27-device-enrollment`, independent of port mismatch and remains red even if DB addresses are corrected. Other candidate/runtime selection jobs skipped. Branch-only station policy test has a hard-coded `127.0.0.1:5433` at `internal/database/station_policy_resolver_integration_test.go:17` (latent test coupling, not a red check in this run). |
| BaseHarbor #1373, `11ed442eeda148b199f097cd04c4cde89e4429da`, run `41859360020` | Same two B database failures at `identity_tenant_resolver_integration_test.go:101` and `tenant_integration_test.go:87`, both role DSNs dial `127.0.0.1:5432` and are refused; `PR Selected Checks` failed as downstream aggregation. | B. Runtime, pin, candidate, HA, and release jobs listed in `gh pr checks` were skipped by selection/policy. |
| BaseHarbor #1375, `c24a6c7c7777c216d75c0cb76591984910ca8390`, run `41863532371` | No red check; draft run had `PR · Source format` and `Workflow policy` pass. | Draft lifecycle: `PR Selected Checks`, `PR · Validation · ${{ matrix.check }}`, `Focused Python`, pin/runtime/candidate jobs, validate, release preflight and targeted HA checks skipped. PR was left as-is. |
| Connector #19, `78b3c4f3c3a5ee046555445834a6350674dd2593`, run `41839096924` | `source` failed: `2026-11-04T13:33:09.8182388Z ##[error]Process completed with exit code 1.` Job runs `test -z "$(gofmt -l cmd internal)"`. | A candidate source-format failure (`t-20261018-r27-node-service`), independent of DB runner. Test/vet/build passed. `Actual encrypted transport · ${{ matrix.runtime }}` and `Managed native enrollment · ${{ matrix.runtime }}` skipped. |

The exact workflow dispatch point for the shared Go database helper is `baseharbor/.github/workflows/ci.yml:803` (go-unit-tests calls `bash scripts/pr-unit-database.sh`). That helper binds the hosted database to `127.0.0.1:5433` and exports `BASEHARBOR_TEST_DATABASE_URL` at `baseharbor/scripts/pr-unit-database.sh:12,32`; the two develop tests previously ignored that DSN for role pools and hard-coded port 5432 (`identity_tenant_resolver_integration_test.go:85`, `tenant_integration_test.go:78`). No workflow edit is needed. Thus classification across the currently red checks is A=3 independent issues (AppEdit fixture, migration rollback regression, Connector gofmt), B=1 common cause (two DB test failures repeated across four PRs), C=0 among the original named open candidates. The closed superseded #1376 was the separate C/base contamination incident; it is not counted as an open candidate.

### Minimal reproduction and separation proof for B

The preceding worker section records before/after/mutation evidence from its clean dedicated PostgreSQL run on `127.0.0.1:5441`: each of the two affected tests failed before with the hard-coded `:5432` DSN, passed after sourcing `BASEHARBOR_TEST_DATABASE_URL`, and failed after mutation to unreachable port `:5999` with `connect: connection refused`. These are the two minimal examples (2/2); the mutation demonstrates real connectivity failures remain red. The separate `TestMigrationRollbackOwnsOnlyLatestChange` failure above and the AppEdit failure are counterexamples to a global “environment-only” explanation: both remain classified A and require their own product/fixture fixes.

### Corrected PR #1377 status / hosted run

Read-only refresh: `gh pr view 1377` reports state OPEN, `isDraft=false`, base `develop`, head `029e3ddd522b63114279d59d5af741ec417ca010`; `git ls-remote origin refs/heads/work/r27-ci-delivery-dsn` returns the same full SHA. Initial run `41873636365` completed success with validation jobs skipped. Subsequent automatic run `41874203933` reached terminal `completed/success`: `PR · Validation · go-unit-tests` success and `PR Selected Checks` success; source format, workflow policy, focused Python, go-build and go-vet also passed. No run was dispatched or rerun by this session. The current PR is not draft, correcting the stale draft assertions in the preceding worker section. No PR status was changed by this session.

## repo-rule compliance

Read-only GitHub state/log inspection and evidence-only append. No product/workflow edits, no check reruns, no PR status change, no merge, no branch mutation. Existing w128 branch/PR evidence is attributed to that worker rather than claimed as this session’s local run.
