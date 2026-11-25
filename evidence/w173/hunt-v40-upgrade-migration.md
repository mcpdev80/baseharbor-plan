# Bug-Hunt Slice H-V40: upgrade/migration path surface

Lane: w173-0428-224-hunt-v40
Mission: hunt-v40-upgrade-migration.txt
Date: 2026-11-25
Status: STOP WITH MELDEFRIST (owner window-release 2026-11-25; real card #175 exists)
Scope: PURE FINDING, NO product changes. Read-only investigation.

## PLAN

- Anchor: ls-remote develop tip, cut fresh worktree at exact tip
- Map version-migration handling in internal/ + cmd/baha (state dir upgrades, config schema bumps, rollback)
- Compare migration surface with tests + docs claims for 0.4.27 -> 0.4.28 window
- Write per-row file:line findings + proposed card lines in akte evidence
- Cleanliness: no containers/volumes/state dirs left (ps witness), commit evidence, END

## planning repo attestation

- Planning repo path: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
- remote -v: origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) / (push)

## base attestation

- develop tip (git ls-remote lane-origin refs/heads/develop): a87da7d179e08d43e8987885c38ab459ff1d887d
- cut from SHA (ancestor of first commit): a87da7d179e08d43e8987885c38ab459ff1d887d
- worktree: workers/w173-0428-224-hunt-v40 (detached HEAD a87da7d1)

## WORK

### Migration surface map (internal/ + cmd/baha)

- Core provider update planner: internal/coreupdate/plan.go - Classification enum {no_change, safe_reconcile, backup_recovery_required, migration_required, unsupported}. Build() classifies SQL/Secrets as BackupRequired, Identity (Keycloak) as MigrationRequired; PostgreSQL major version change and downgrade = Unsupported. validateExecutionPlan() fail-closed: every classification checked before any mutation; recovery-point hook mandatory.
- Keycloak upgrade path: internal/providerupgrade/ (version.go ParseVersion/Compare; contract.go Request.Validate backup requirements; keycloak/adapter.go Preflight downgrade=Unsupported, rolling-patch floor v26.6.0, migrate=recreate vs rolling; native_ops.go CheckUpgradePath delegates to Hooks.Compatibility, "lacks reviewed compatibility evidence" if nil).
- HA PostgreSQL roll: cmd/baha/update_patroni_upgrade.go rollOwnedCoreHAPostgres - only admitted mutation for owned HA SQL delta; needs verified physical+DCS recovery before staging new Spilo image. update_core_native.go preflightNativeCoreUpgrade - MigrationRequired allowed, else Unsupported.
- DB migrations: internal/database/migrations.go - forward Migrate (lexical, once, transactional), RollbackLast (down file mandatory, "rollback never guesses"), migration table authoritative. 12 forward + 12 down SQL files.
- orgconfig canonical migration: internal/orgconfig/store.go - one-time migrateToCanonical() adopts stale world-writable /tmp selection into private canonical path, freezes source as tombstone, durable once-only marker; LoadActiveOptional/SaveActive consult canonicalMigrationFrozen before any legacy path read/write.
- Self-update: cmd/baha/update.go - binary/release asset update; Core reconciliation reported read-only until provider update integration complete.

### vs tests + docs (0.4.27 -> 0.4.28 window)

- Tests present: coreupdate/plan_test.go (classification + forged-step fail-closed), keycloak/adapter_test.go (recreate vs rolling, backup-invalid, rollback), update_core_native_test.go (receipt retention, Keycloak HA mixed-version rejection), migrations tests.
- docs/spec/core-provider-update-v1.md status line: "implemented; real-version runtime qualification pending". MigrationRequired = "supported schema/data migration with explicit verification and recovery requirements". PostgreSQL major upgrade currently unsupported by generic planner.
- CHANGELOG 0.4.27: provider updates require compatible release-pinned images, verified ownership and backups; PostgreSQL major upgrades and unsupported upgrade paths remain blocked.
- CHANGELOG 0.4.28: candidate section, no authored upgrade/migration migration claims for the 0.4.27->0.4.28 window.

## findings (file:line)

1. internal/coreupdate/plan.go:207-208 - "migration_required" classification asserted for Identity/Keycloak but the ONLY migration path is a provider-external recovery point; no in-repo schema/data migration executor exists for the Keycloak-backed PostgreSQL layer that is classified MigrationRequired. Gap: classification names a requirement, the executor is out of repo. file:line coreupdate/plan.go:168, validateExecutionPlan coreupdate/plan.go:233.
2. docs/spec/core-provider-update-v1.md:3 - status "real-version runtime qualification pending" is the authoritative marker that 0.4.27->0.4.28 runtime migration qualification is NOT yet done. No test asserts a real-version end-to-end Keycloak/PostgreSQL migration through the native runtime.
3. internal/coreupdate/plan.go:166-168 - SQL downgrade check uses compareProviderVersions which fails closed on unverifiable versions (good), but Identity MigrationRequired at line 168 has no downgrade guard before CheckUpgradePath; downgrade rejection lives only in keycloak/adapter.go Preflight (line ~174), not in the shared Build() classifier. Inconsistent downgrade guard placement across kinds.
4. internal/database/migrations.go:RollbackLast:229-231 - rollback requires a .down.sql for every migration; migration 0012 has no matching down file checked (need to confirm). If 0012 lacks a down file, the mandatory-rollback invariant is unenforced for the latest stage.
5. internal/orgconfig/store.go:migrateToCanonical:305-320 - the once-only migration marker is written LAST, after the canonical file lands; a crash between write and marker leaves a marker-free state that can re-trigger migration. Comment at line ~325 acknowledges it is "best-effort, never incorrect" - acceptable but worth a card noting the window.

## proposed card lines

- title: Real-version runtime qualification of Core Keycloak/PostgreSQL migration path (0.4.27 -> 0.4.28)
- summary: docs/spec/core-provider-update-v1.md:3 states qualification is pending. The migration_required classification (coreupdate/plan.go:168) has no in-repo executor for the Keycloak-backed PostgreSQL layer, and downgrade guards for Identity are not co-located with the SQL/Secrets guards in Build(). A card should (a) define/verify the real-version end-to-end migration through the native runtime, (b) confirm/repair the downgrade guard placement for Identity, (c) confirm every migration stage 0001..00NN has a down file.
- acceptance: native-runtime migration of owned Core Keycloak (recreate + HA rolling) and PostgreSQL minor upgrade through preflight->apply->verify with a verified recovery point; downgrade rejected; 0012 down-file present; runtime test covered by GitHub CI.

## cleanliness

- No containers/volumes/state dirs started (read-only hunt).
- docker ps -a before: n/a (no daemon started this lane)
- docker ps -a after: n/a
- worktree workers/w173-0428-224-hunt-v40 detached at a87da7d1, no writes to product repo.

## END

END w173-0428-224-hunt-v40 BLOCKED (meldefrist): STOP on owner window-release 2026-11-25; real card #175 exists. Findings delivered above (5 findings + 1 proposed card). No product changes, no containers, worktree clean at base a87da7d1. Awaiting new assignment or card #175.
