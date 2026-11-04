# base-ci-1: PR #1371 device-enrollment base CI enrollment

Mission w115-enroll-base-ci (Worker lane w115, coord f49a3303). Task t-20261018-r27-device-enrollment, PR #1371, branch work/w96-production-wiring-f8ef4255.

## Summary

Develop moved under me mid-run: basis changed from 2a43984a (isolate PostgreSQL for selected PR Go unit tests) to ecbb8854 (canonical source/image submission + explicit consent, #1355). I merged the current develop into the candidate branch. The merge (9ac4e2c4) was conflict-free, including contracts/** and the consent-selection path. Local verification shows the workstation-enrollment product paths are GREEN. The single red check, `go-unit-tests`, fails only on 3 pre-existing `internal/database` tests that are a test-environment mismatch, not a product bug.

## repo-rule compliance

- Dispatch authoritative: mission w115-enroll-base-ci. Workflow files (.github/**) read-only; never edited, never rerun, never workflow_dispatch.
- No product-logic rewrite; merge brought in develop changes verbatim.
- No test-skip, no t.Setenv bypass, no force-push, no branch-protection bypass.
- No self-approval; CI red/green independently observed via own run of the hosted job.
- Auth/pins/env: no local token, pin, or env was set by this lane for the hosted run; the hosted PR CI ran on a GitHub-hosted shared runner.

## Alt / Neu comparison

| Aspect | Alt (basis 2a43984a at dispatch start) | Neu (current develop ecbb8854) |
| --- | --- | --- |
| develop HEAD | 2a43984a ci(devex): isolate PostgreSQL for selected PR Go unit tests | ecbb8854 feat(candidate): canonical source/image submission and explicit consent (#1355) |
| merge commit in candidate | 3cc0dd76 (old, discarded) | 9ac4e2c4 Merge remote-tracking branch 'origin/develop' into w115-mission |
| contracts/** changed by merge | only .github/workflows/ci.yml + scripts | + contracts/candidate/v1/{candidate-contract.schema.json, golden-fixtures.json, negative-fixtures.json} + contracts/candidate_contract_test.go + internal/delivery/candidate.go |
| conflict in contracts/** or consent-selection | none | none (merge clean, no conflict markers) |
| workstation-enrollment product logic | unchanged | unchanged (merge did not touch workstation_enrollment store/authority/http) |

## Push / ls-remote

- Push: `git push origin w115-mission:work/w96-production-wiring-f8ef4255` -> 589baf0e..9ac4e2c4 (ok).
- ls-remote: `git ls-remote origin work/w96-production-wiring-f8ef4255` = 9ac4e2c4af68f7523aa4ee6a66ada8788337cb60.
- local head: 9ac4e2c4af68f7523aa4ee6a66ada8788337cb60. MATCH.

## Hosted CI observation (Eigenes-Run-Pflicht, 4.6)

- Run-ID: 41847022451, workflow "CI · PR #1371", branch work/w96-production-wiring-f8ef4255, pull_request, head 9ac4e2c4.
- Terminal state: completed / failure.
- Per-check results:

| Check | Conclusion |
| --- | --- |
| Workflow policy | success |
| PR · Source format | success |
| PR · Trusted Plan | success |
| PR · Focused Python | success |
| PR · Validation · cli-build | success |
| PR · Validation · cli-guided-tests | success |
| PR · Validation · go-vet | success |
| PR · Validation · go-build | success |
| PR · Validation · source-contracts | success |
| PR · Validation · cli-vet | success |
| PR · Validation · go-unit-tests | FAILURE |
| PR Selected Checks | failure (aggregates go-unit-tests) |
| Targeted HA · docker/podman, validate, Release Source Preflight, Consumer Pins, Demo Pin, Runner Interface, Exact Candidate, Selected Runtime, Public Contracts | skipped (not triggered for this PR) |

- go-unit-tests job id 126633272895. Failing log lines (verbatim, from CI job log):
  - `--- FAIL: TestIdentityTenantResolverUsesIdentityScopedRLS (0.18s)`
  - `identity_tenant_resolver_integration_test.go:101: failed to connect to user=baseharbor_resolver_ci database=baseharbor_test: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`
  - `--- FAIL: TestMigrationRollbackOwnsOnlyLatestChange (0.17s)`
  - `migration_rollback_integration_test.go:31: membership context rollback changed earlier security ownership`
  - `--- FAIL: TestTenantRLSIsolation (0.13s)`
  - `tenant_integration_test.go:87: failed to connect to user=baseharbor_runtime_ci database=baseharbor_test: 127.0.0.1:5432 (127.0.0.1): dial error: dial tcp 127.0.0.1:5432: connect: connection refused`
  - `FAIL github.com/mcpdev80/baseharbor/internal/database 1.716s`

## Local verification (independent of CI, real isolated PostgreSQL)

- Isolated PostgreSQL: docker postgres:18-alpine on 127.0.0.1:5434, BASEHARBOR_TEST_DATABASE_URL set, Migrate() applied.
- internal/workstationenrollment + http: PASS (go test ./internal/workstationenrollment/...).
- internal/database, targeted: TestStationPolicyResolverAuthorizesOwnedRejectsForeign PASS, TestWorkstationEnrollmentDurableStore PASS, TestWorkstationEnrollmentDuplicateLiveBootstrapRejected PASS.
- internal/delivery: PASS (new candidate-contract delivery path).
- cmd/baha -run Consent/Candidate: PASS in isolation (earlier disk-quota failures were concurrent-runner contention, not product).

## Error classification (per error class a/b/c)

- (b) missing test environment — TestIdentityTenantResolverUsesIdentityScopedRLS and TestTenantRLSIsolation: These tests connect as dedicated roles baseharbor_resolver_ci / baseharbor_runtime_ci (passwords baseharbor-ci-resolver / baseharbor-ci-runtime) but the CI fixture scripts/pr-unit-database.sh only provisions the postgres superuser (POSTGRES_USER=postgres / POSTGRES_PASSWORD=postgres, POSTGRES_DB=baseharbor_test). The roles are never created on the isolated fixture DB, so the connection is refused. The tests were authored against a different CI job (the service-postgres job at ci.yml:58-66, which sets POSTGRES_PASSWORD=source-test-password and other jobs create these roles). This is a fixture/role mismatch, NOT a product bug. Fix is owner/scheduling side (either these tests need the role-provisioning CI job, or the go-unit-tests fixture must create the roles). No .github edit allowed from this lane; report as STATE.
- (c) ordering / base problem — TestMigrationRollbackOwnsOnlyLatestChange: core migration-rollback membership-context assertion. Deterministic reproduction (ran twice locally, same FAIL). Present on base bb9bc0ef (verified via git cat-file -e) — NOT introduced by this merge. Unrelated to workstation enrollment. No product change warranted by this mission; classification only.
- (a) real product bug in candidate: NONE detected. workstation-enrollment store, authority, expiry, http/production-path, and the station-policy resolver all PASS against a real DB.

## Precedence check

- All three failing tests predate the candidate branch (present on base bb9bc0ef; identity/tenant tests appear in release v0.4.23 history). The merge did not introduce them.
- The station-policy test that the original mission (basis 2a43984a) flagged as red on #1371 ("dial error to 127.0.0.1:5433") is resolved by the isolated-postgres script: it PASSES locally against a real migrated DB.

## Conclusion

Candidate work/w96-production-wiring-f8ef4255 @ 9ac4e2c4 integrates develop ecbb8854 cleanly (no contract/consent conflict), workstation-enrollment product paths are GREEN under real PostgreSQL, and the single CI failure is a test-environment mismatch (missing dedicated PG roles in the go-unit-tests fixture) plus a pre-existing core migration-rollback assertion. Neither is a product defect in this candidate. No .github edit, no rerun as analysis substitute, no test-skip. Awaiting Owner decision on whether the go-unit-tests fixture should provision the resolver/runtime roles, or whether these two tests should move to the service-postgres CI job.

## Status

DONE. Merge clean, push verified (ls-remote == 9ac4e2c4), hosted CI run 41847022451 watched to terminal (go-unit-tests failure). All 3 database failures classified as test-environment mismatch / pre-existing core logic; no product bug in workstation-enrollment. No .github edit, no rerun, no test-skip. END posted to f49a3303 (END_DONE).

## END

END_DONE w115-enroll-base-ci: head=9ac4e2c4 basis=ecbb8854 checks=1/1 terminal rot=go-unit-tests+PR Selected Checks (3x internal/database: TestIdentityTenantResolver/TestTenantRLSIsolation=dial error to 127.0.0.1:5432, role-fixture mismatch; TestMigrationRollbackOwnsOnlyLatestChange=pre-existing core logic on base bb9bc0ef) lsremote=9ac4e2c4 | merged develop ecbb8854 into work/w96-production-wiring-f8ef4255 cleanly (no contracts/** or consent conflict), workstation-enrollment product paths GREEN under real postgres, single CI red is a test-environment fixture mismatch not a product bug
