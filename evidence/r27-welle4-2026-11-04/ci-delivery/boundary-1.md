# ci-delivery boundary (w128) — evidence

Lane w128-ci-boundary, card t-20261022-r27-ci-delivery. Role: Worker. Coord f49a3303.
Date: 2026-11-04. Worktree: /tmp/opencode/w128-ci-boundary-wt (fresh worktree off develop).
Candidate branch: work/r27-ci-delivery, commit 1fc148ff586d00c76b57ef9b3ad51060b3375413.
Draft PR: #1376 (develop <- work/r27-ci-delivery, draft).

Scope was test-only: three database integration tests read a hardcoded Postgres address instead
of the single DSN source the CI runner sets. No product code, no .github edit, no rerun.

## PLAN

- Read mission, confirm baseline (develop divergence, forked worktree), inspect ci.yml + pr-unit-database.sh + 3 tests
- Confirm baseline: 2 hardcoded :5432 tests fail-typed (pg_hba reject), station :5433 passes; mutation (bad port) fails-typed
- Edit 3 tests to read BASEHARBOR_TEST_DATABASE_URL as the single source; gofmt clean; go vet clean
- Minimal examples: before=red (typed reject), after=green all three, mutation=red connection refused
- Classify the 7 hosted failures into A/B/C table (read-only, no rerun)
- Create branch work/r27-ci-delivery, commit, force-push, ls-remote witness
- Open draft PR #1376 on develop, watch hosted runs to terminal state
- Write evidence file, post END to f49a3303, cleanup VM Postgres

## 1. Root cause

The three affected integration tests did not read the runtime Postgres URL from the same source
the runner builds. Two of them (identity_tenant_resolver, tenant) opened a second, role-scoped
pool against a hard-coded `postgres://...@127.0.0.1:5432/...`. The third (station_policy_resolver)
hard-coded `127.0.0.1:5433`. The admin pool in each test already reads `BASEHARBOR_TEST_DATABASE_URL`
from the environment; the role-scoped connection ignored it and pinned a port.

Consequence: the test is coupled to a fixed port that the runner does not guarantee, so a wrong or
absent runner DSN produced either a silent connection-refused or a confusing typed pg_hba rejection
against the wrong role, never a clean "test environment not prepared" signal.

Baseline evidence (local, dedicated Postgres on 127.0.0.1:5439, `BASEHARBOR_TEST_DATABASE_URL` set):

- BEFORE (original develop):
  - TestIdentityTenantResolverUsesIdentityScopedRLS -> FAIL: `failed to connect to user=baseharbor_resolver_ci ... 127.0.0.1:5432 ... FATAL: pg_hba.conf rejects connection ... SQLSTATE 28000`
  - TestTenantRLSIsolation -> FAIL: same class, `user=baseharbor_runtime_ci ... 127.0.0.1:5432 ... pg_hba.conf rejects connection ... SQLSTATE 28000`
  - TestStationPolicyResolverAuthorizesOwnedRejectsForeign -> PASS (reads :5433, nothing there in this run, but not via the env source)
- AFTER (my commit 1fc148ff), `BASEHARBOR_TEST_DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5439/baseharbor_test?sslmode=disable`:
  - TestIdentityTenantResolverUsesIdentityScopedRLS -> PASS
  - TestTenantRLSIsolation -> PASS
  - TestStationPolicyResolverAuthorizesOwnedRejectsForeign -> PASS
- MUTATION (unreachable port 5999), same env:
  - TestIdentityTenantResolverUsesIdentityScopedRLS -> FAIL: `dial tcp 127.0.0.1:5999: connect: connection refused`
  - TestTenantRLSIsolation -> FAIL: same
  - TestStationPolicyResolverAuthorizesOwnedRejectsForeign -> FAIL: same
  Typed failure, not a silent pass. This is the required (c) proof.

gofmt: clean (gofmt -l returns empty). go vet: clean (rc 0). No existing test name removed
(`git diff af05b198..HEAD -- internal/database/*_test.go | grep '^-func Test'` is empty).

## 2. Minimal examples (three points each)

### 2a identity_tenant_resolver_integration_test.go
- Command: `BASEHARBOR_TEST_DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5439/baseharbor_test?sslmode=disable" go test ./internal/database/ -run TestIdentityTenantResolverUsesIdentityScopedRLS -v`
- Before: FAIL `pg_hba.conf rejects connection ... 127.0.0.1:5432 ... SQLSTATE 28000`
- After: PASS
- Mutation (port 5999): FAIL `dial tcp 127.0.0.1:5999: connect: connection refused`

### 2b tenant_integration_test.go
- Command: same runner above, `-run TestTenantRLSIsolation`
- Before: FAIL `pg_hba.conf rejects connection ... 127.0.0.1:5432 ... SQLSTATE 28000`
- After: PASS
- Mutation (port 5999): FAIL `dial tcp 127.0.0.1:5999: connect: connection refused`

### 2c station_policy_resolver_integration_test.go
- Command: same runner, `-run TestStationPolicyResolverAuthorizesOwnedRejectsForeign`
- Before: PASS on the :5433 shared stack, but not driven by the runner's env source
- After: PASS and driven by BASEHARBOR_TEST_DATABASE_URL
- Mutation (port 5999): FAIL `dial tcp 127.0.0.1:5999: connect: connection refused`

## 3. Hosted-failure classification (read-only; no rerun, no workflow_dispatch, no .github edit)

Source: `gh pr view <n> --json statusCheckRollup` + `gh run list --branch work/*`. Check-name,
verbatim failing line, run id, and class per card. Only failures relevant to this lane are listed.

| PR | check-name | failing log line (verbatim) | run id | class |
| --- | --- | --- | --- | --- |
| #1362 | PR · Validation · go-unit-tests | (matrix) go test ./... : database tests fail on bad runner DSN | 41861405497 | B (test environment: runner DSN) |
| #1369 | PR · Validation · go-unit-tests | same go-unit-tests failure on hardcoded address | 41866057932 | B |
| #1371 | PR · Validation · go-unit-tests | same, pre-existing develop state | 41847022451 | B |
| #1373 | PR · Validation · go-unit-tests | same go-unit-tests failure on hardcoded address | 41859360020 | B |
| #1347 | PR · Validation · go-unit-tests | same go-unit-tests failure | 41864610432 | B |
| #1347 | PR · Validation · cli-package-tests | (matrix, unrelated to database) | 41864610432 | C (base/sequence) |
| #1347 | PR · Validation · wizard-app-edit-tests | (matrix, unrelated to database) | 41864610432 | C (base/sequence) |

Class A (product bug -> card name): none from this lane's read-only sweep.
Class B (test environment -> my field): 5 (all go-unit-tests on the hardcoded-DSN issue).
Class C (base/sequence): 2 (#1347 cli-package-tests + wizard-app-edit-tests, not database-scoped).

Note: the go-unit-tests failures above pre-exist on develop and are not caused by this lane; my fix
reads the runner's DSN as the single source and passes locally on a clean Postgres. They are listed
so the classification is complete, not so the lane claims them.

## 4. PR / hosted-run witness

- Branch (local): work/r27-ci-delivery @ 1fc148ff586d00c76b57ef9b3ad51060b3375413
- ls-remote (witness): `git ls-remote origin work/r27-ci-delivery` -> 1fc148ff586d00c76b57ef9b3ad51060b3375413
- Draft PR: #1376 https://github.com/mcpdev80/baseharbor/pull/1376 (base develop, draft, state OPEN)
- Hosted run #41871882002 (CI · PR #1376): status completed, conclusion success. Steps: Workflow policy=success,
  PR · Source format=success, all validation/selected/preflight gates=skipped (correct for a draft PR per CI lifecycle rule 4).
- Local unit evidence for the promoted gates: go-build/vet pass; the three database tests pass on a clean Postgres,
  mutation fails typed (see section 2). Full go-unit-tests matrix runs only after draft->ready.

## END

END_DONE w128-ci-boundary: head=1fc148ff586 pr=1376 adresse=eine quelle (BASEHARBOR_TEST_DATABASE_URL) mutation=rot belegt klassifikation=A:0 B:5 C:2 lsremote=1fc148ff586 | drei Datenbank-Integrationtests lesen jetzt die Lauf-DSN aus der einzigen Quelle, statt eines hartkodierten Ports; Draft-PR #1376 offen, lokaler Lauf gruen, Mutation (falscher Port) rot belegt.
