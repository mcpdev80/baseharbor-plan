# cx05-ci-skip-fix evidence

Card: `t-20261022-r27-ci-delivery`; role CODEX-WORKER; continue branch/PR `work/r27-ci-delivery-dsn` / #1377 only.

## PLAN

1. Confirm remote PR/head/base ancestry and that the assigned worktree is clean; keep all unrelated worktrees untouched.
2. Change only the two database integration-test missing-DSN guards from `t.Skip` to the requested clear `t.Fatal`.
3. On one resulting commit, run the database package with the variable unset, run it with a working isolated PostgreSQL DSN, and mutate the DSN to an unreachable port; record exact output and exit status for all three.
4. Run `go build ./...`, `go vet`, and gofmt checks on the same candidate; push once after the local checks, then observe the PR's hosted gates to terminal.
5. Read the three independent A product task cards and record why the DSN fix cannot address them, with relevant source line references.
6. Record the exact candidate SHA, `git ls-remote` witness, hosted run IDs/statuses, and send the required END to f49a3303.

## Candidate before changes

PR #1377 was OPEN and ready, head `029e3ddd522b63114279d59d5af741ec417ca010`; `develop` head `ecbb88545f96473986f8f41394cffce58b97d2df` is an ancestor. Checks/run `41874203933` completed success, including `go-unit-tests` and `PR Selected Checks`. No workflow file is in scope.

## Implementation

Only the missing-DSN guards in `internal/database/identity_tenant_resolver_integration_test.go:18` and `internal/database/tenant_integration_test.go:18` changed from `t.Skip` to `t.Fatal("testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt")`. Commit `5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9`; name-only diff against develop is exactly these two files. No test or assertion was removed. Pushed by fast-forward to the existing PR branch; PR remains OPEN, ready, no status change.

## Three A findings — read-only boundary

- **Migration rollback regression — card `t-20261018-r27-device-enrollment` (“Devices: issue and validate scoped workstation enrollment”).** The independent product failure is `TestMigrationRollbackOwnsOnlyLatestChange`: `migration_rollback_integration_test.go:187` returns `membership context rollback changed earlier security ownership` when rollback has altered earlier schema/security state. This failure happens after the test has obtained a DB and evaluated schema ownership; changing the two other tests' missing-DSN behavior does not change the rollback logic or this assertion.
- **AppEdit/OpenBao fixture failure — card `t-20261018-r27-state-owner` (“State: enforce installation-owned deployment storage”).** The failing journey is `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, `cmd/baha/app_edit_apply_test.go:826`; its observed preflight error is `service "openbao-admin" is not running` (recorded in boundary-1; the task's blocker and causal chain are at `t-20261018-r27-state-owner.md:20,153`). Its cause is an unstarted/missing OpenBao manager service/fixture, not the DSN selection in the two database tests. The card independently records it as an A finding.
- **Connector formatting failure — card `t-20261018-r27-node-service` (“Connector: reconcile enrollment service and restart behavior”).** Connector PR #19's source gate runs `gofmt -l cmd internal` and reports `cmd/baseharbor-node-connector/main.go` and `internal/nodeservice/nodeservice.go` as unformatted (review/handoff on that card). These files are in the separate `baseharbor-node-connector` repository; neither they nor their formatting gate consume `BASEHARBOR_TEST_DATABASE_URL`. The working tree was read-only inspected and left unchanged.

The `ci.yml:803` workflow line already invokes the database helper. No workflow change is needed or made. The shared DSN mismatch fix only changes test DSN sourcing; it cannot correct these three independent A causes.

## Three cases on one head

(a) **Unset variable; full package test; head `5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9`:** `env -u BASEHARBOR_TEST_DATABASE_URL GOCACHE=/tmp/cx05-gocache go test ./internal/database -count=1` → exit 1. Literal output: `identity_tenant_resolver_integration_test.go:18: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt` and `tenant_integration_test.go:18: testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt`; package `FAIL`, no skip and no connection-refused noise.
(b) **Working fixture DSN; full package test; same head:** `BASEHARBOR_TEST_DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5445/baseharbor_test?sslmode=disable GOCACHE=/tmp/cx05-gocache go test ./internal/database -count=1` → exit 0, literal result `ok github.com/mcpdev80/baseharbor/internal/database 2.305s`. This used a dedicated ephemeral PostgreSQL 18 container and a reachable DSN through the same variable populated by `scripts/pr-unit-database.sh`. The script's fixed host port 5433 was already occupied by an unrelated container `sleepy_ganguly`; to avoid touching another lane's DB, the local isolated fixture used free host port 5445. Hosted CI still uses the unchanged helper and its normal 5433 mapping.
(c) **Unreachable-port mutation; both target tests; same head:** set the same variable to `postgres://postgres:postgres@127.0.0.1:59999/baseharbor_test?sslmode=disable` and run `go test ./internal/database -run '^(TestIdentityTenantResolverUsesIdentityScopedRLS|TestTenantRLSIsolation)$' -count=1` → exit 1. Literal failures at each test's DSN open: `127.0.0.1:59999 ... dial tcp 127.0.0.1:59999: connect: connection refused`. This proves configured endpoints are actually attempted and remain red when unreachable.

## Required checks and hosted runs

On the same committed head: `go vet ./...` exit 0; `gofmt -d` for both changed test files empty; `go build -buildvcs=false ./...` exit 0. Plain `go build ./...` initially failed with Go's `error obtaining VCS status: exit status 128` in this temporary worktree; disabling only build VCS stamping allowed the full build. No test input was hidden or skipped in the package run with a valid DSN.

Hosted run `41878182617` for head `5b2fbb65c356fb977baa5dcb6d8e6804a90f4fe9` was queued when first observed; terminal status pending. Prior head's completed run `41874203933` is historical only and not used for this new SHA.

## repo-rule compliance

Only the two assigned test files may change. No `.github` edits, no tests removed, no merge, no PR status change, no second branch/PR, no subagents. Do not touch the other shared worktrees or their untracked files.
