# 0428-161 r1 — target-uid-migration idempotenz / nebenlauf / no-mutation

- Card/mission: t-20261120-r28-bughunt-target-uid-migration (0428-161), Schnitt H-V11
- Role: pure BUG-HUNT, no product change / PR / merge / VM / container / subagent
- Worker session: `9142ab1f-c464-4f2f-abc8-d6997d8655ae` (this lane)
- Product repo verified via clone at /var/tmp/baseharbor-x161v (https://github.com/mcpdev80/baseharbor.git)
- Merge under review (PR #1580): `bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978`
- Ancestry witnesses (all `git merge-base --is-ancestor <sha> bbc937c8f1` => YES):
  - `522af6f4a` (fix: serialize legacy target UID migration writes)
  - `ae0602e02` (no-mutation in MigrateLegacyTargetUIDs)
  - `3a91e2a83` (fix CLI cmd/baha unit tests for read-triggered UID migration)
- Evidence base = merge head bbc937c8f1 (the #1580 deliverable that develop was carrying today); HEAD c000c5db later reverted LoadConfig to a plain decode, so this is the version under audit.

## PLAN
1. Locate `MigrateLegacyTargetUIDs` in merge bbc937c8f1; inspect migration + no-mutation claim.
2. V1 idempotenz: run the read seam twice on one legacy config; prove the 2nd read actually executes.
3. V2 nebenlauf: locate the serialize lock (file:line); prove it covers the read-triggered write and that a 2nd concurrent caller fails closed.
4. V3 no-mutation: prove an already-mapped Target UID is not rewritten.
5. V4 beobachter: prove the status/desk reader is decoupled from the migration (no feedback loop).
6. Run affected unit tests at exact head; write akte, push to origin/main, post END.

## V1 — idempotenz (DONE, BEGUTACHT)
- Migration seam: `internal/deployment/target.go:223` `migrateAndPersistTargetUIDs(cfg, data)` called from `LoadConfig()`; the read path fills the empty `TargetUID` for legacy Targets and persists exactly once.
- Idempotency contract (`internal/deployment/target.go:226-231`): `MigrateLegacyTargetUIDs` returns `changed` empty when every Target already carries a UID, so `migrateAndPersistTargetUIDs` returns without writing.
- Empirical witness `TestV1SecondLoadActuallyRuns` (local repro, package deployment, PASS): 1st `LoadConfig()` fills `uid1`; 2nd `LoadConfig()` runs and returns the same `uid1`, config bytes byte-identical. The 2nd read is not merely asserted — it is actually executed and reads back the persisted UID, proving no 2nd write.
- Existing witness `TestLoadConfigMigratesLegacyTargetIdempotent` (`internal/deployment/target_migration_test.go:19`): asserts `uid1==uid2` AND that `persisted` equals `persistedAfter` after the 2nd `LoadConfig()` — i.e. it truly runs the 2nd load and checks no churn.

VERHALTEN KORREKT — V1 idempotenz: 2nd LoadConfig runs, returns same UID, config bytes unchanged (witness: TestV1SecondLoadActuallyRuns PASS; TestLoadConfigMigratesLegacyTargetIdempotent PASS).

## V2 — nebenlauf / serialize (DONE, BEGUTACHT)
- Lock location: `internal/deployment/config_mutation.go:77` `coreinstallation.AcquireStateFileLock(root)` inside `saveWithPreparation` (the `SaveExpected` path the current read seam uses via `migrateAndPersistTargetUIDs` -> `migrated.SaveExpected(expected)` at target.go:234).
- `root` = `filepath.Dir(ConfigPath())`; the `.installation.lock` the CAS read (`config_mutation.go:74`) and the flock (`config_mutation.go:77`) both live in that same directory — confirmed for `BASEHARBOR_STATE_DIR` test layout (`<root>/config`).
- Lock is a real advisory `flock` (`internal/stableid/lock_unix.go:270` `unix.Flock(fd, unix.LOCK_EX|unix.LOCK_NB)`) with a cross-process validity probe (`lock_unix.go:283 lockProbeRun`) that fails closed if the FS does not enforce it. A 2nd caller holding a stale read gets `EWOULDBLOCK`.
- The read-triggered branch IS covered: `migrateAndPersistTargetUIDs` persists through `SaveExpected`, so it takes the same `AcquireStateFileLock` as every other config write — not a bypass.
- Empirical witness `TestV2ConcurrentMigration` (local repro, package deployment, PASS): two concurrent `migrateAndPersistTargetUIDs` on one legacy config — caller 0 fails closed with `lock .installation.lock is held ... resource temporarily unavailable`, caller 1 succeeds; exactly 1 successful write; config changed by exactly one writer. Fail-closed, no silent loss.
- The existing `TestLegacyTargetUIDMigrationRespectsConfigurationLock` (`target_migration_test.go:82`) serializes via `coreinstallation.AcquireStateFileLock` then asserts the migration refuses while the lock is held.

VERHALTEN KORREKT — V2 serialize: `AcquireStateFileLock` (config_mutation.go:77) on `.installation.lock` (lock_unix.go:270) covers the read-triggered write; 2nd concurrent caller fails closed on flock EWOULDBLOCK, exactly one writer (witness: TestV2ConcurrentMigration PASS; TestLegacyTargetUIDMigrationRespectsConfigurationLock PASS).

## V3 — no-mutation (DONE, BEGUTACHT)
- Claim (`ae0602e02`, `internal/deployment/target_id.go:80`): `MigrateLegacyTargetUIDs` never mutates an already-mapped UID; the returned config is a fresh map and the caller's `cfg.Targets` is left byte/value-identical.
- Code (`target_id.go:88-104`): the `if strings.TrimSpace(def.TargetUID) != ""` branch copies the untouched definition verbatim into the fresh map and never touches the caller's map; only empty-UID defs get a new cloned UID.
- Empirical witness `TestV3ExistingUIDNotRewritten` (local repro, package deployment, PASS): a config with a pre-existing mapped UID returns `changed` empty and the UID unchanged.
- Existing witnesses `TestMigrateLegacyTargetUIDsNoMutationOnSuccess` (`target_migration_test.go:221`) and `TestMigrateLegacyTargetUIDsNoMutationOnFailure` (`:279`) assert deep-equality of the caller's map before/after both success and validation-failure paths.

VERHALTEN KORREKT — V3 no-mutation: existing mapped UID preserved, caller map untouched (`target_id.go:88`); witnesses NoMutationOnSuccess/NoMutationOnFailure PASS.

## V4 — beobachter (DONE, BEGUTACHT)
- Question: do the status / desk readers observe a Target UID at all, and could a reader re-trigger the migration (feedback loop to V2)?
- Find: the status/desk path resolves app identity from the app Store (`.baseharbor/.apps/<name>` manifest), NOT from `config.yaml` — see `cmd/baha/app.go:118` (`application.Store{Root: filepath.Join(sourceRoot, ".baseharbor", "apps")}`). `rootStatusCommand` (`cmd/baha/commands.go:123`) -> `appStatusCommandWithTLS` -> `app_status_collect`; none read the target UID from config at rest.
- The only production caller of `MigrateLegacyTargetUIDs` is `LoadConfig` (`internal/deployment/target.go:223`); the migration writes only on `LoadConfig` (a config read), never on the status/desk read path. No feedback loop: a status observation neither triggers nor re-reads the migration.

VERHALTEN KORREKT — V4 beobachter: status/desk reads app identity from `.baseharbor/.apps` (app.go:118), decoupled from config migration; migration's sole production caller is `LoadConfig` (target.go:223). No reader re-triggers the write.

## BEWERTUNG
- All four seams (idempotenz, serialize+fail-closed, no-mutation, observer decoupling) verified with witnesses at exact head bbc937c8f1.
- No bug found in the target-uid-migration under this cut. Empirical: `go test ./internal/deployment/` => ok (1.277s); `go test ./cmd/baha/ -run 'UID|Target|Migration'` => ok (25.893s); all four repro/existing witnesses PASS.
- No new test written into the product (mission forbids product changes; CI wiring is Owner scope). The existing witnesses already cover V1-V4.

## repo-rule compliance
- Role honored: pure finding, no product change, no PR/merge, no VM/container/network/volume, no subagent (4.8).
- No writes to `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (bookkeeping dir, never the planning repo).
- Evidence written only from the /var/tmp planning clone against the GitHub remote; single-file write, no `git add -A`.
- Provenance: clone base `bbc937c8f1` (verified ancestors of the merge above); no foreign candidate carried on top.

## cleanliness
- before: `/var/tmp/baseharbor-x161v` = fresh clone (HEAD c000c5db after develop fetch); `/var/tmp/plan-x161` = fresh plan clone (origin/main 2cc718de).
- after: `/var/tmp/baseharbor-x161v` = read-only checkout of bbc937c8f1, no committed product changes (only ephemeral `zz_repro_*_test.go` files created and removed during `go test`, never committed); `/var/tmp/plan-x161` = origin/main at 2cc718de with one added file `evidence/r28-welle4-2026-11-19/bughunt-target-uid-migration/round-1.md`.
- no containers / networks / volumes / state dirs created or left.
- cleanliness: clean.
