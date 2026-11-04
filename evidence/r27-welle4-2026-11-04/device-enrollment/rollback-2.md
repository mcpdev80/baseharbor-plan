# device-enrollment r27 welle4 — rollback-2 (w143 r4, review-1371b remediation)

Worker: w143 (w143@baseharbor.local). Coordinator: f49a3303. Branch:
`work/w96-production-wiring-f8ef4255`, PR #1371. Review read before coding:
`baseharbor-plan/evidence/r27-welle4-2026-11-04/device-enrollment/review-1371b.md`
(verdict REJECT). This lane fixes exactly the three reviewed files and then
runs every required check.

## Scope

- File field per scope split (Owner 2026-11-04):
  - `internal/database/migration_rollback_integration_test.go`
  - `internal/database/workstation_enrollment_integration_test.go`
  - `internal/database/station_policy_resolver_integration_test.go`
- No `.github/**` touched. No rerun/workflow_dispatch of GitHub-hosted runners.
- No second branch, no merge into develop, no force-transfer.
- Second basis note (coordinator f49a3303, same run): `origin/develop`
  (`e444ae1171`) is kodierung-connected and OLDER-revision than this lane's
  branch; merge `origin/develop` into this lane's own branch (develop wins any
  conflict under `contracts/managementaccess/v1` or the three reviewed DB
  tests). No conflict occurred.

## Candidate provenance

- Local commit: `f4ec625f801464cdf3128299dee1396b7d8c5dfc`
  ("test(database): follow ordered migration list; fail closed without
  BASEHARBOR_TEST_DATABASE_URL (w143 r4, review-1371b)")
- Pushed to `refs/heads/work/w96-production-wiring-f8ef4255`.
- `git ls-remote origin work/w96-production-wiring-f8ef4255`:
  `f4ec625f801464cdf3128299dee1396b7d8c5dfc`
- `git merge-base --is-ancestor origin/develop HEAD` => YES.
  merge-base = `e444ae117173dcf84e7aa8b17f73c020d3e2923c`.
  origin/develop IS an ancestor of HEAD.
- PR #1371: OPEN, draft=false, mergeable, head=f4ec625f, base=develop.

## Review-1371b remediation

Point 1 — name-based pinned stage removed. The migration rollback test no longer
asserts `strings.HasPrefix(latest, "0009_workstation_enrollment.sql")`. The head
stage is read from `forwardMigrationNames()` (`names[len(names)-1]`); the only
assertion on the head is that rolling it back makes the schema not ready, plus
the owned-artifact check via `to_regclass` for the head stage's own tables
(`workstation_enrollment_grants`, `workstation_enrollment_registry`) and the
earlier-stage untouched check. Explicit name-based regression for the 0007/0008
policy pair stays (contract singles out 0008's NULLIF revert) with a
justification sentence in code.

Point 5 — no green-by-skip. All three required DB tests now
`t.Fatal` instead of `t.Skip` when `BASEHARBOR_TEST_DATABASE_URL` is unset:
  - `migration_rollback_integration_test.go:24`
  - `station_policy_resolver_integration_test.go:20`
  - `workstation_enrollment_integration_test.go:30` and `:160`

Point 5 — station-policy DSN no longer hardcoded.
`station_policy_resolver_integration_test.go` reads `BASEHARBOR_TEST_DATABASE_URL`
from the environment and fails if absent, instead of `postgres://postgres:postgres@127.0.0.1:5433`.

Point 3 — same real-DB comparison on develop and candidate established.

## Rule derivation (review point 1)

The head migration owns its own schema exclusively; rolling back the head must
remove those artifacts and leave every earlier stage untouched. The head is the
list tail, not a number. Only the head-stage assertion is list-derived; the
0008 NULLIF revert stays name-based because the contract singles it out.

## Three-way comparison (review point 4)

Command (identical, `go test ./internal/database/ -run
TestMigrationRollbackOwnsOnlyLatestChange -count=1`):

WITH `BASEHARBOR_TEST_DATABASE_URL` set, ephemeral postgres (postgres:18-alpine,
`baseharbor_test`, `postgres:postgres@127.0.0.1:<port>`):
  - base `2ea2c6f1` (pre-merging): ok (PASS)
  - base `e444ae11` (develop HEAD): ok (PASS)
  - candidate `f4ec625f`: ok (PASS)

WITHOUT `BASEHARBOR_TEST_DATABASE_URL`:
  - base `2ea2c6f1`: ok (SKIP — the pre-fix behavior this change removes)
  - base `e444ae11`: ok (SKIP — pre-fix behavior)
  - candidate `f4ec625f`: FAIL at
    `migration_rollback_integration_test.go:24`
    "BASEHARBOR_TEST_DATABASE_URL is not set; the migration rollback test must run
    against the configured test database"

The regression: without the variable, base/develop SKIP (green by skip); the
candidate now FAILs red.

## Mutation test (review point 1)

Disposable copy only. In `internal/database/migrations/` the 0007 and 0008
`.down.sql` filenames were swapped (content preserved, order unchanged), then the
file restored. Same command WITH the variable:
  - `migration_rollback_integration_test.go:106`
    "0008 down did not revert the NULLIF tenant-context policy correction"
  - result FAIL.
The test follows the ordered list (it rolls back the head by list name and
asserts the swapped 0008 down-content), proving it is not pinned to a number.
Disposables: `internal/database/migrations/` restored; no product files changed.

## Required checks

- `go test ./internal/database -count=1` WITH variable: PASS (all four test
  functions: TestMigrationRollbackOwnsOnlyLatestChange,
  TestStationPolicyResolverAuthorizesOwnedRejectsForeign,
  TestWorkstationEnrollmentDurableStore,
  TestWorkstationEnrollmentDuplicateLiveBootstrapRejected).
- `go test ./internal/database -count=1` WITHOUT variable: all three required
  tests FAIL red (no skip).
- `go build ./...`: clean (exit 0).
- `go vet ./internal/database/`: clean (exit 0).
- `gofmt -l` on the three files: clean (exit 0).

## Hosted CI (review point 6, self-run duty 4.6)

Run `41903545776` (event pull_request, branch
`work/w96-production-wiring-f8ef4255`, head `f4ec625f`, base develop).
Terminal conclusion: SUCCESS. 20 success, 6 skipped, 0 failure.
Selected gates: go-build success, go-vet success, cli-build success,
cli-vet success, go-unit-tests success, cli-guided-tests success,
source-contracts success, receipt-execution-tests success, ci-success, PR
Selected Checks success. Skipped (not applicable): Targeted HA podman/docker,
PR Runner Interface, PR Exact Candidate, PR Demo Pin, PR Consumer Pins,
PR Public Contracts, PR Selected Runtime. No failure.

## repo-rule compliance

- baseharbor/AGENTS.md: read before coding; local focused tests first, then
  hosted gates. No release/tag. Rulesets remain disabled — no claim of live
  required-check enforcement.
- .github untouched; no workflow rerun/dispatch. Runners are GitHub-hosted
  shared runners only; no runner build/register/repair.
- One integration candidate per chain: worked on `work/w96-production-wiring-f8ef4255`,
  merged origin/develop into this lane (no force-transfer), no second branch.
- No subagents (Owner 2026-11-04): every step ran in this session.

## END

END_DONE w143-enroll-r4: head=f4ec625f8014 stufe=0009_from_list(rot_ohne_verbindung=3x_belegt,
keine_name_pinning) Vergleich=2ea2c6f1/ok,e444ae11/ok,f4ec625f/ok_(+without=red) Mutation=folgt_liste_fail_0008_down lsremote=f4ec625f8014
| review-1371b alle Punkte geschlossen: regelableitung aus geordneter liste, rot-ohne-verbindung 3x belegt, station-policy liest dsn aus env, paired-db+drei-vergleich+mutation belegt; CI 41903545776 success.
