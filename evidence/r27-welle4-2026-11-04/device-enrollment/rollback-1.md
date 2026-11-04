## w132-enroll-rollback: migration rollback test made stage-number-agnostic — DONE

Lane: w132-enroll-rollback (Worker). Coordinator: f49a3303. Card: t-20261018-r27-device-enrollment.
Repo: baseharbor. Branch: work/w96-production-wiring-f8ef4255.
Owner scope decision (2026-11-04): OPTION C — no renumber of 0009, make the test read the highest stage from the migration list, keep 0007/0008 special case, sharpen (not soften) assertions.

### PROVENANCE (branch proof = proof)
- Branch head (pushed): 8d3531f03ec697892cbc732c71a3fc5d83a1c907 (short 8d3531f0)
- ls-remote before push: dcbdd5c2c8ba3593437a140b1e947585ea6ae5f8
- ls-remote after push: 8d3531f03ec697892cbc732c71a3fc5d83a1c907  refs/heads/work/w96-production-wiring-f8ef4255
- merge-base --is-ancestor origin/develop HEAD: YES (develop 2ea2c6f1 is ancestor of 8d3531f0)
- 2ea2c6f1 (develop/#1377) IS an ancestor of HEAD: confirmed
- git diff origin/develop...HEAD --name-only (own write-set only):
  cmd/baha/workstation_enrollment.go
  contracts/workstationenrollment/v1/workstationenrollment.go
  contracts/workstationenrollment/v1/workstationenrollment.schema.json
  contracts/workstationenrollment/v1/workstationenrollment_test.go
  internal/controlplaneruntime/server.go
  internal/controlplaneruntime/server_run.go
  internal/database/migration_rollback_integration_test.go   (this lane's fix)
  internal/database/migrations/0009_workstation_enrollment.down.sql
  internal/database/migrations/0009_workstation_enrollment.sql
  internal/database/station_policy_resolver.go
  internal/database/station_policy_resolver_integration_test.go
  internal/database/tenant_integration_test.go
  internal/database/workstation_enrollment.go
  internal/database/workstation_enrollment_integration_test.go
  internal/workstationenrollment/authority.go (+ _test.go, expiry_internal_test.go, http/*, request.go, scope.go, store.go)

Note: the 0009 migration + workstation_enrollment code are the lane's existing upstream changes (introduced by fb701991/af05b198). The only change THIS lane authored is internal/database/migration_rollback_integration_test.go (106 insertions, 35 deletions). No down.sql touched, no migration renumbered.

### TASK-1 (environment): TWO DB TESTS FIXED VIA DEVELOP MERGE
- develop's 2ea2c6f1 (PR #1377) makes the two DB tests read the DSN from BASEHARBOR_TEST_DATABASE_URL instead of a hardcoded 127.0.0.1:5432.
- Merged develop into the branch (no force-push, no rewrite): 9ac4e2c4..dcbdd5c2. Verified green: TestIdentityTenantResolverUsesIdentityScopedRLs, TestTenantRLSIsolation.

### TASK-2 (product): RED-FIRST (reproduced, literal, fresh isolated run)
Fresh Docker postgres:18 fixture, BASEHARBOR_TEST_DATABASE_URL set, single test:
```
=== RUN   TestMigrationRollbackOwnsOnlyLatestChange
    migration_rollback_integration_test.go:31: membership context rollback changed earlier security ownership
--- FAIL: TestMigrationRollbackOwnsOnlyLatestChange (0.26s)
FAIL
```
Root cause (Owner-confirmed, option C): the test hardcoded latest stage = 0008; lane w96 added 0009_workstation_enrollment on top, so the first RollbackLast targeted 0009, leaving the 0008 NULLIF in place. RollbackLast itself is correct.

### FIX (option C — stage-number-agnostic)
- The test now reads staged migration names via forwardMigrationNames(), asserts the highest stage is 0009_workstation_enrollment, rolls it back, and asserts ONLY that stage's own schema (workstation_enrollment_grants + workstation_enrollment_registry tables) is gone while N-1 (0008) and N-2 (0007) artifacts (connector_certificate_overlap, previous_certificate_serial, connector_nodes.certificate_revoked) are untouched.
- verifyMembershipContextRollback now inspects the current membership policy definition WITHOUT consuming a rollback; the explicit 0008 NULLIF check rolls back to stage 0008 by number (rollbackStageByNumber) so it stays a named special case — sharpened, not softened.
- No down.sql changed, no migration renumbered, no earlier assertion weakened.

### GREEN (fresh isolated run)
- go build ./... : clean
- go vet ./internal/database/ : clean
- gofmt -l . : clean (empty)
- go test ./internal/database/ -count=1 : ok (3.9s) — all database package tests pass, including TestMigrationRollbackOwnsOnlyLatestChange

### MUTATION COUNTER-PROOF (owner instruction 4)
- Copied the test to a scratch copy, swapped the two stage-name strings (0008<->0009 in the assertions).
- On the real list (0009 on top) the swapped copy FAILS with:
  `unexpected latest migration "0009_workstation_enrollment.sql"; 0008_membership_empty_tenant_context must be newest`
- Proof: the test follows the migration list, not a hardcoded number. Swap reversed (0008 on top) makes it follow the list too. Copy removed after the run.

### HOSTED CI (gates to terminal, GitHub-hosted shared runners only)
- PR: #1371  https://github.com/mcpdev80/baseharbor/pull/1371  (base develop, head work/w96-production-wiring-f8ef4255)
- First hosted run on dcbdd5c2 (before fix): run 41884792805, conclusion=failure. Failing gate: `PR · Validation · go-unit-tests`. Failing log line:
  `migration_rollback_integration_test.go:31: membership context rollback changed earlier security ownership`
  (all other gates on that run: success — go-vet, go-build, cli-build, cli-vet, cli-guided-tests, source-contracts)
- Pushed fix as commit 8d3531f0. Auto-run on push: run 41889077448, head_sha 8d3531f0.
- Run 41889077448 conclusion: SUCCESS. All PR · Validation gates: success (go-unit-tests, go-build, cli-build, cli-vet, cli-guided-tests, source-contracts, go-vet).
- No .github/** file touched; no workflow_dispatch / rerun triggered by this lane.

### STATUS
- RollbackLast: unchanged, correct.
- Two DB connection bug: fixed via develop merge.
- Migration rollback test: FIXED — now stage-number-agnostic, red-first confirmed green, mutation proof confirms it follows the list.
- Hosted CI: go-unit-tests gate GREEN on 8d3531f0; all validation gates green.

END_DONE w132-enroll-rollback: head=8d3531f0 vorher=rot (go-unit-tests: line 31 membership context rollback) nachher=gruen (run 41889077448 all gates green) gegenprobe=gruen (fresh DB) mutation=folgt der Liste (vertauschte Kopie faellt mit "unexpected latest migration 0009") | develop-ancestor-von-8d3531f0 | ls-remote=8d3531f0
