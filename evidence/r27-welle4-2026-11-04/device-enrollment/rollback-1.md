## w132-enroll-rollback — migration rollback test failure: ROOT CAUSE + OWNER SCOPE DECISION

Lane: w132-enroll-rollback (Worker). Coordinator: f49a3303. Card: t-20261018-r27-device-enrollment.
Repo: baseharbor. Branch: work/w96-production-wiring-f8ef4255.

### PROVENANCE (branch proof = proof)
- Branch head (pushed): dcbdd5c2c8ba3593437a140b1e947585ea6ae5f8
- ls-remote before push: 9ac4e2c4af68f7523aa4ee6a66ada8788337cb60
- ls-remote after push:  dcbdd5c2c8ba3593437a140b1e947585ea6ae5f8  refs/heads/work/w96-production-wiring-f8ef4255
- merge-base --is-ancestor origin/develop HEAD: YES (develop 2ea2c6f1 is ancestor of HEAD)
- 2ea2c6f1 (develop/#1377) IS an ancestor of HEAD: confirmed
- git diff origin/develop...HEAD --name-only (own write-set only, now reverted): internal/database/migrations.go, internal/database/migration_rollback_integration_test.go (instrumentation only)

### TASK-1 (environment): TWO DB TESTS FIXED VIA DEVELOP MERGE
- The two DB tests failed because they read the DSN from a hardcoded 127.0.0.1:5432 instead of BASEHARBOR_TEST_DATABASE_URL; develop's 2ea2c6f1 (PR #1377) fixes this.
- I merged develop into my branch (no force-push, no rewrite of history): 9ac4e2c4..dcbdd5c2.
- Verified after merge: TestIdentityTenantResolverUsesIdentityScopedRLs PASS, TestTenantRLSIsolation PASS.

### TASK-2 (product): MIGRATION ROLLBACK TEST RED — REPRODUCED
Fresh Docker postgres:18 fixture, BASEHARBOR_TEST_DATABASE_URL set, single test:
```
=== RUN   TestMigrationRollbackOwnsOnlyLatestChange
    migration_rollback_integration_test.go:31: verifyMembershipContextRollback FAILED: membership context rollback changed earlier security ownership
--- FAIL: TestMigrationRollbackOwnsOnlyLatestChange (0.34s)
FAIL
```
Reproduces in a clean isolated run (not a shared-environment artifact). Same run PASSES on develop (only 0001-0008).

### ROOT CAUSE (confirmed, NOT a RollbackLast defect)
- RollbackLast is correct: migration table applied_at DESC returns 0009_workstation_enrollment.sql as most recent (epoch .289054 vs 0008 .280035).
- verifyMembershipContextRollback (test line 30) assumes the FIRST RollbackLast reverts 0008 (the membership NULLIF fix), leaving the memberships policy as plain current_setting.
- My lane added migration 0009_workstation_enrollment (new tables only, no membership-policy change) with a HIGHER number than 0008, so it now sits ABOVE 0008 in applied_at order.
- First RollbackLast reverts 0009 instead of 0008 -> NULLIF stays -> safeContext=true -> FAIL condition `safeContext || !forcedRLS || !identityResolution` triggers.
- This offsets the ENTIRE rollback chain by one (line 34 reverts 0008 instead of 0007, so connector_certificate_overlap survives -> overlapExists=true -> would also fail at line 48).
- Down.sql files 0006/0007/0008 are correct. The defect is the migration NUMBER of 0009 relative to 0008.

Migration order (applied_at DESC): 0009 (.289054) > 0008 (.280035) > 0007 > 0006 > 0005 > 0004 > 0003 > 0002 > 0001 (.151520).

### BLOCKER: OWNER SCOPE DECISION REQUIRED (posted as QUESTION to f49a3303)
Two mutually-exclusive fixes; neither safe to choose unilaterally:
- (A) Rename migration 0009 to a LOWER number than 0008 so the membership NULLIF fix (0008) becomes the latest applied migration again. Down.sql must exist for the renumbered file; changes migration file names and rollback order.
- (B) Accept 0009 as correctly the newest migration and update the test's rollback-chain expectation — but the mission forbids rewriting the DB tests, so (B) is out under current constraints.

Per mission constraints (tests unchanged, no rollback-logic rewrite without a reproduced bug, no second PR) I have NOT modified the test or reordered migrations. The bug is reproduced and root-caused; the FIX requires an Owner ordering decision.

### STATUS
- RollbackLast: correct, no change.
- Two DB connection bug: fixed via develop merge.
- Migration rollback test: red, root-caused to 0009 vs 0008 migration-number ordering. BLOCKED pending Owner decision.

END_BLOCKED w132-enroll-rollback: head=dcbdd5c2 before=red after=red(root-caused=migration-ordering 0009 above 0008) | blocker=owner decision: rename 0009 below 0008 (A) vs accept 0009 newest (B, conflicts with tests-unchanged) | ls-remote=dcbdd5c2
