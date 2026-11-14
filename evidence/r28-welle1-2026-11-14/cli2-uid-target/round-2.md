# PR #1580 — Round 2 (R1 correction)

## Role
Worker. Implementation of the R1 correction recipe from
`act-1580-review-r1.md` (CODEX-REVIEW R1 REJECT).

## What the R1 verdict required
1. **Missing persisted legacy-target migration** — `MigrateTargetUID` was called
   only on create. A legacy definition (empty `TargetUID`) never gained a UID on
   read/config-resolution/list. Must generate the missing UID **idempotently and
   persist it**: first read generates, second read is no-churn/no-write.
2. **Tests bypassed the real CLI** — must go through the real
   `baha target create` command via `runWithIO`/tmp-root (precedent 175-r8),
   including the collision case.
3. **GAP** — rename preservation + serialized role separation across
   config/recovery/list round trips.

## Candidate and provenance
- PR #1580 is DRAFT, base `develop`, head branch `lane-0428-uid-target`.
- Exact `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/pull/1580/head`:
  ```
  c769cd107d63134024c4ef70a2f9f19d30c72b67	refs/pull/1580/head
  ```
- Prior candidate: `ebeafa56a2d14d962603cbc649e4764628104417` (R1 head).
- `git merge-base --is-ancestor develop c769cd107`: exit 0.
- CI routed by existing `ci.yml` release-source group. **No `.github/**` change.**

## Changes (c769cd107 vs ebeafa56a2)
- `internal/deployment/target_id.go` — `MigrateLegacyTargetUIDs(cfg Config)
  (Config, []string, error)`: fills only missing UIDs, validates the full
  post-migration config (fails closed on collision), pure + idempotent, sorted
  changed set.
- `internal/deployment/target.go` — `LoadConfig` now decodes →
  `migrateAndPersistTargetUIDs` → `migrateConfigUIDsAt` (CAS read-modify-write on
  the protected config owner, **no installation-lock required**, atomic rename,
  empty-changed-set no-op). `Config.Validate` enforces UID uniqueness via
  `validateTargetUIDUniqueness`.
- `internal/deployment/target_migration_test.go` (new) —
  `TestLoadConfigMigratesLegacyTargetIdempotent`,
  `TestMigrateLegacyTargetUIDsFailsClosedOnCollision`,
  `TestUIDSurvivesConfigRoundTripPreservesRoleSeparation`.
- `cmd/baha/target_uid_cli_test.go` — real-CLI tests via `runWithIO`/tmp-root:
  `TestCLITargetCreateGeneratesStableUID`,
  `TestCLITargetUIDStableAcrossReads`,
  `TestCLITargetUIDCollisionFailsClosedOnRead`.
- `internal/deployment/config_mutation_test.go` — existing fixture
  `TestSaveExpectedPreservesConcurrentConfiguration` was corrected: the copied
  `other` Target now carries a distinct generated UID. It was otherwise valid
  (still tests CAS rejection), but with the now-enforced uniqueness it would have
  collided; the fixture was poisoned by the new constraint, not broken.

## Verification (local)
- `go build ./...` — OK (whole tree builds).
- `go vet ./internal/deployment/... ./cmd/baha/` — OK.
- `go test ./internal/deployment/ -count=1` — **ok** (all pass, including the
  corrected fixture).
- New deployment tests:
  - `TestLoadConfigMigratesLegacyTargetIdempotent` PASS — first `LoadConfig`
    fills the legacy UID and persists it; second `LoadConfig` observes no churn.
  - `TestMigrateLegacyTargetUIDsFailsClosedOnCollision` PASS — two Targets
    sharing one UID return an error.
  - `TestUIDSurvivesConfigRoundTripPreservesRoleSeparation` PASS — UID and
    `TenantID` survive a full save/load round trip and stay distinct.
- New CLI tests (`go test ./cmd/baha/ -run 'TestCLITargetUID|TestCLITargetCreate'`):
  - `TestCLITargetCreateGeneratesStableUID` PASS — real `baha target create`
    auto-generates a valid UID; `TenantID` untouched.
  - `TestCLITargetUIDStableAcrossReads` PASS — create + `baha target list` keep
    one UID.
  - `TestCLITargetUIDCollisionFailsClosedOnRead` PASS — a seeded config with two
    Targets sharing one UID fails closed at `baha target list` (via
    `LoadConfig` → `Validate` uniqueness).

## Design notes
- UID is a Core-side stable identity, auto-generated at create (no manual UUID
  request, no `--target-uid` CLI flag). Only the missing field is filled; names,
  runtime, data dirs and ownership `TenantID` are untouched.
- Migration persistence uses a dedicated CAS seam that does **not** require
  `.installation.lock` (legacy Targets have no Core installation), unlike
  `SaveExpected`. Idempotent: a second read finds no empty UID and writes
  nothing.
- Collision fail-closed flows through the real CLI read path, seeded by writing
  a corrupted config directly (config path precedence: `XDG_CONFIG_HOME` nests
  under `<home>/baseharbor/`, per `ConfigPath()`).

## Repo-rule compliance
- Same branch/PR #1580, head `c769cd107` (was `ebeafa56a2`).
- No `.github/**` change; CI routed by existing `ci.yml` release-source group
  (Owner-scope workflow change not required).
- No merge. Draft only.

## END
POSTED `END_DONE` to `594fd2f5-4e80-43b6-9841-92879146a85e` (welle1 turn).
