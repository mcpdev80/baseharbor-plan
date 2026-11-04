# CODEX REVIEW — PR #1371, Review 1371c

## Verdict

**REJECT** for candidate `f4ec625f801464cdf3128299dee1396b7d8c5dfc` (`work/w96-production-wiring-f8ef4255`). PR #1371 is OPEN/READY, base `develop`; no PR action or merge was performed.

## Candidate identity and scope

- GitHub API head and `git ls-remote origin refs/heads/work/w96-production-wiring-f8ef4255`: `f4ec625f801464cdf3128299dee1396b7d8c5dfc`.
- GitHub API develop and `git ls-remote origin refs/heads/develop`: `e444ae117173dcf84e7aa8b17f73c020d3e2923c`.
- `git merge-base --is-ancestor origin/develop HEAD`: exit 0.
- `git diff --name-only origin/develop...HEAD`: 27 paths, no `.github` paths. `AGENTS.md` is an additional non-enrollment path and is out of this task's bounded enrollment/database/wiring field. The other changed paths are the workstation-enrollment contract, implementation, database, HTTP, and wiring field.
- PR #1371 status: OPEN, not draft, mergeable. Review did not change it.

## Blocking findings

### R1 — a first workstation cannot bootstrap on a clean installation

The production path constructs `database.NewStationPolicyResolver(pool)` in `cmd/baha/workstation_enrollment.go:66-67`. That resolver only authorizes a station when a row already exists in `workstation_enrollment_registry` (`internal/database/station_policy_resolver.go:67-78`). The HTTP bootstrap path resolves/authorizes the station before calling `Enrollment.Create` (`internal/workstationenrollment/http/production_handler.go:93-101`). The only production writer for the registry fact is after successful enrollment (`production_handler.go:137-157`, backed by `internal/database/workstation_enrollment.go:110-132`). Thus a new station on an empty registry cannot reach the first bootstrap; the fact needed to authorize it can only be recorded after the denied operation.

I verified this on a disposable copy of the exact candidate with a fresh PostgreSQL database, a tenant and a valid membership, but zero registry rows. A test sent POST `/api/v1/workstations/bootstrap` through `ProductionHandler` configured with the production `StationPolicyResolver`:

```text
=== RUN   TestReviewInitialStationBootstrapIsDenied
    review_coldstart_test.go:44: registry_rows_before=0 bootstrap_http_status=403 create_calls=0
--- PASS: TestReviewInitialStationBootstrapIsDenied (0.41s)
PASS
ok  github.com/mcpdev80/baseharbor/internal/workstationenrollment/http 0.419s
coldstart_probe_exit=0
```

The API path is routed (403 rather than 404); the request is blocked before bootstrap creation. `internal/database/station_policy_resolver_integration_test.go:63-64` manually inserts the registry row before testing authorization, so it does not cover first enrollment.

**Recipe:** provide an accepted, explicit policy/assignment source that can authorize the initial station before a registry fact exists. Keep tenant membership bound from verified identity policy and retain fail-closed rejection for unassigned/foreign stations. Add a fresh-install regression that proves first bootstrap succeeds only for an explicitly assigned station, that unassigned/foreign bootstrap has zero store/issuer effects, and that successful enrollment records the registry fact for subsequent use. Stop if no authorized initial assignment source exists.

### R2 — stage-order mutation exposes a hard-coded artifact assertion

The candidate selects `latest := names[len(names)-1]` at `internal/database/migration_rollback_integration_test.go:43-55`, but then asserts that `workstation_enrollment_grants` and `workstation_enrollment_registry` are absent at lines 71-79, regardless of which migration is now last. I made a disposable archive of this SHA and swapped the numeric prefixes of both the 0008 and 0009 up/down migration pairs. The test selected `0009_membership_empty_tenant_context.sql`, rolled it back, then failed because the workstation tables correctly remained as artifacts of the earlier `0008_workstation_enrollment.sql` stage:

```text
=== RUN   TestMigrationRollbackOwnsOnlyLatestChange
    migration_rollback_integration_test.go:79: 0009_membership_empty_tenant_context.sql owned schema still exists after rolling back its owning migration
--- FAIL: TestMigrationRollbackOwnsOnlyLatestChange (0.48s)
FAIL
FAIL github.com/mcpdev80/baseharbor/internal/database 0.486s
mutation_exit=1
remaining_migration_versions_and_workstation_tables
0001_core_identity.sql
0002_tenant_rls.sql
0003_application_ownership.sql
0004_identity_membership_resolution.sql
0005_connector_enrollment.sql
0006_connector_certificate_admission.sql
0007_connector_certificate_renewal.sql
0008_workstation_enrollment.sql
workstation_enrollment_grants
workstation_enrollment_registry
```

The dynamic list did choose and rollback the current last stage; the following hard-coded workstation-table assertion wrongly treated an earlier stage as the selected stage. This does not meet the required mutation proof that the chosen stage is reverted while earlier artifacts remain.

The explicit 0007/0008 exception is explained in code: 0008 reverts the in-place tenant-context policy correction introduced by 0004, while 0007 owns the certificate-overlap table (`migration_rollback_integration_test.go:18-20, 96-118`). `strings.HasPrefix(version, stage)` remains only in the helper that walks to the explicitly named 0008 exception, not in selection of the latest migration. No `== "0009..."` latest-stage check was found.

**Recipe:** make the dynamic latest-stage assertion track the selected migration's actual schema effect (or isolate fixed migration-specific probes in separately named tests) and prove both the selected stage's rollback and retention of earlier-stage artifacts. Rerun the 0008/0009 number-swap mutation and require it to pass, along with the unmutated rollback test. Stop if the generic assertion still assumes workstation tables are the latest stage.

### R3 — `AGENTS.md` is outside the bounded write-set

The only non-field path in the name-only diff is `AGENTS.md`. It adds lane identity and a branch-specific instruction to merge `develop` into this implementation branch. This operational note does not belong in the workstation-enrollment product PR and is not one of the authorized enrollment/database/wiring paths.

**Recipe:** remove `AGENTS.md` from the PR diff; keep task dispatch and base-refresh directions in the coordinator mission/evidence instead. Stop if any non-field path remains in the exact PR diff.

## Retained 1371a criteria

- The protected operator API registers `/api/v1/workstations/bootstrap` and `/enroll` (`internal/controlplaneruntime/server_run.go:248-281`); the handler dispatches absolute mounted suffixes (`production_handler.go:54-70`). The fresh-registry probe reached the handler and returned 403, not 404.
- The protected API authenticates the bearer, verifies the external principal and resolves tenant membership before adding tenancy context (`internal/controlplaneruntime/server_run.go:213-220, 277-281`; `internal/httpsecurity/middleware.go:41-63`; `internal/database/identity_tenant_resolver.go:27-88`). The enrollment request's `installation_id` is not used to select tenant; the scope resolver uses authenticated tenancy and policy (`internal/workstationenrollment/http/scope_resolver.go:28-54`).
- Registry-fact persistence is fail-closed in the handler: a write error returns HTTP 500 before the success response (`production_handler.go:142-157`). The current unit test covers successful persistence but does not inject a registry-write failure; adding that negative regression is recommended.
- Durable integration coverage uses PostgreSQL, a reopened pool, replay rejection, and registry-fact readback (`internal/database/workstation_enrollment_integration_test.go:22-30, 104-142`).

## Independent checks and CI

- Missing connection variable: the three affected tests failed with their explicit error (no skip):
  - `migration_rollback_integration_test.go:24`: `BASEHARBOR_TEST_DATABASE_URL is not set; the migration rollback test must run against the configured test database`
  - `station_policy_resolver_integration_test.go:20`: `BASEHARBOR_TEST_DATABASE_URL is not set; the station-policy resolver test must run against the configured test database`
  - `workstation_enrollment_integration_test.go:30`: `BASEHARBOR_TEST_DATABASE_URL is not set; the workstation enrollment store test must run against the configured test database`
- With an isolated disposable PostgreSQL 18 database, all three targeted tests passed under `go test ./internal/database -run '^(TestMigrationRollbackOwnsOnlyLatestChange|TestWorkstationEnrollmentDurableStore|TestStationPolicyResolverAuthorizesOwnedRejectsForeign)$' -count=1 -v`; the full `go test ./internal/database -count=1` also passed.
- Same rollback-test command on `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`, `e444ae117173dcf84e7aa8b17f73c020d3e2923c`, and the candidate: each PASS (respectively 0.385s, 0.407s, 0.576s).
- `go test -p 1 ./internal/workstationenrollment/... ./contracts/workstationenrollment/v1 ./internal/controlplaneruntime -count=1`: PASS.
- `go build -p 1 ./cmd/baha ./contracts/workstationenrollment/v1 ./internal/controlplaneruntime ./internal/database ./internal/workstationenrollment/...`: PASS.
- `go vet -p 1` on the same affected packages: PASS. `gofmt -l cmd internal`: empty. `git diff --check origin/develop...HEAD`: PASS.
- A broader local `go test ./... -count=1` was not a valid clean-candidate result: the shared worktree already contained untracked `evidence/scripts/mutation/mutation_swap.go`, which Go discovered as a package with undefined database test helpers; unrelated `cmd/baha` tests also hit read-only `/home/marcel/.local/share` and missing Docker/runtime prerequisites, and the broad parallel build hit the temporary-storage quota. A generated `conformance/provider/v1/testdata/external/go.mod` change and `go.sum` were restored/removed immediately; the pre-existing untracked evidence script was left untouched. The isolated test DB container was removed, and the before/after Docker container name lists matched.
- Exact-candidate hosted run `41903545776`: terminal `completed/success`, head `f4ec625f801464cdf3128299dee1396b7d8c5dfc`, 16 successful jobs, 0 failed, 10 skipped. `go-unit-tests`, `go-build`, `go-vet`, and `PR Selected Checks` passed; skipped checks are not counted as passes.

## repo-rule compliance

- Review was read-only on product source. No product commit, push, PR update, review submission, or merge occurred.
- Candidate worktree status after cleanup contains only the pre-existing untracked `evidence/scripts/` content; no tracked source changes remain.
- No shared Docker stack was modified; only named, disposable reviewer PostgreSQL containers were created and removed.

## Open items

R1 first-station bootstrap policy, R2 stage-order mutation, R3 non-field `AGENTS.md` diff. Required tests: clean-install initial bootstrap positive and negative policy cases; 0008/0009 swap mutation green with earlier-stage retention; exact name-only diff contains only enrollment/database/wiring field. Verdict remains **REJECT** until corrected and reviewed on a new exact SHA.
