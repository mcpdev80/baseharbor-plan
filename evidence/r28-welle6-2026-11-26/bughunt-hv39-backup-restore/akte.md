# BUG-HUNT slice H-V39 - backup/restore & data-safety surface

Sitz `w172-0428-224-hunt-v39`. H-V39 (pure FINDING, no product changes). READ-ONLY audit of the `app backup` / `app restore` fail-closed behavior, restore idempotency, and per-class artifact retention, cross-checked against the shipped code paths in `cmd/baha/app_backup*.go` + `application_restore*.go`, `internal/applicationbackup/*`, and the docs claims in `docs/reference/backup-and-restore.md`.

## PLAN

- anchor rule: fetch develop via `git ls-remote` exact tip, cut fresh worktree at EXACT tip
- locate backup/restore & data-safety surface: cmd/baha + internal/, per-row file:line
- verify fail-closed on partial backups (ValidateForCapture, manifest count, digest)
- verify restore idempotency (archive-revision bind, manifest YAML match, OpenBao non-empty guard)
- cross-check cmd/baha vs internal/ vs docs claims
- findings + proposed card lines in this akte; no product edits
- cleanliness (no containers/volumes left; docker ps -a witness); END_DONE with fund count
- NO subagents, NO product edits, NO workflow edits, NO VM/compose launches

## Anchor

- develop HEAD (git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop): `a87da7d179e08d43e8987885c38ab459ff1d887d`
- planning repo remote: `origin	https://github.com/mcpdev80/baseharbor-plan.git` (fetch)
- fresh worktree cut at EXACT tip: `/tmp/opencode/w172-hunt-v39-wt` @ a87da7d179; `git merge-base --is-ancestor origin/develop HEAD` passes; `git diff origin/develop..HEAD --name-only` empty (worktree is develop, no edits)
- real product remote verified: `git -C baseharbor remote -v` -> `origin	https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80), never pushed through a local path
- base attestation: this hunt's worktree is cut from develop tip a87da7d179e08d43e8987885c38ab459ff1d887d, an ancestor of every commit this lane could make; no foreign candidate carried (empty `git log --oneline origin/develop..HEAD`)

## Scope read (code inventory)

Backup/restore surface (production, non-test):
- `cmd/baha/app_backup_restore.go` - CLI lifecycle `appBackupCommand`/`appRestoreCommand`, `executeApplicationBackupLifecycle`, `executeApplicationRestoreLifecycle`, `restoreApplicationState`, fail-closed helpers (`readBackupPasswordFile`, `writeBackupArchive` with O_EXCL).
- `cmd/baha/app_backup_restore_data.go` - `captureApplicationBackup`, `loadApplicationRestoreData`, per-class validation + `validateRecoveredLogicalResources`.
- `cmd/baha/app_backup_restore_guided.go` - guided interactive backup/restore, terminal echo disable, in-memory memfd password file, `requireVerifiedRestoreScope`.
- `cmd/baha/app_backup_restore_discovery.go` - guided backup discovery, owner-only `.bhbackup` scan.
- `cmd/baha/app_backup_paths.go` - git-worktree-risk guard, non-interactive default destination.
- `cmd/baha/app_backup_recovery.go` - bounded post-backup recovery of stopped workload/broker/exposure.
- `cmd/baha/app_recovery_selection.go` - `discoverApplicationRecoverySelection`, workload-volume ownership classification.
- `cmd/baha/app_recovery_metadata.go` - restore JSON output + recovery-metadata recording.
- `cmd/baha/application_restore_authorization.go` - restore plan build + consent (two acks + destructive data-deletion), `requireVerifiedRestoreScope`.
- `cmd/baha/application_restore_source.go` - restore source/deployment owner reconciliation + manifest-match guard.
- `internal/applicationbackup/recovery.go` - `RecoverySelection`, `Apply` (include/exclude rules), `ValidateForCapture`.
- `internal/applicationbackup/recovery_manifest.go` - manifest version + contributor validation.
- `internal/applicationbackup/recovery_discovery.go` - `DiscoverManifestRecovery` contributors + support/ownership.
- `internal/applicationbackup/archive.go` - `Build`/`Open`, manifest entry count + digest + size, payload validation.
- `internal/applicationbackup/crypto.go` - argon2id KDF + AES-256-GCM authenticated envelope.
- `internal/applicationbackup/postgres.go` - `ValidatePostgresBackupSet`, `PostgresBackupsFromPayload`.
- `internal/applicationbackup/secrets.go` - OpenBao backup identity binding.
- `internal/application/application_restore_source.go`, `internal/application/postgres_backup.go`, `internal/application/shared_backends*.go` - runtime reconcile/verify/release.

Docs claims: `docs/reference/backup-and-restore.md`, `docs/how-to/backup-restore.md`, `docs/tutorials/getting-started.md`.

## Findings (per-row)

### F1 - Fail-closed on partial backup: VALIDATED (no finding)
- `internal/applicationbackup/recovery.go:160-165` `ValidateForCapture`: a durable contributor that is `RecoveryUnsupported`/`RecoveryExternal` and NOT `ExplicitlyExcluded` fails the capture. This is the exact "durable unsupported blocks backup unless explicitly excluded" rule documented at `docs/reference/backup-and-restore.md:98`.
- `internal/applicationbackup/recovery.go:126-131`: `application.metadata` cannot be excluded (`"application.metadata is required in every recovery unit"`).
- `internal/applicationbackup/recovery.go:139-145`: an `--include-state` class not present for the application fails, and a supported class with no supported contributor fails.
- `internal/applicationbackup/archive.go:22-49`: `Build` rejects >MaxEntries (128), per-entry >MaxEntryBytes (512 MiB), and payload >MaxPayloadBytes (2 GiB).
- Verdict: partial backup is fail-closed by contract; docs and code agree. No finding.

### F2 - Restore idempotency / re-authentication: VALIDATED (no finding)
- `cmd/baha/application_restore_authorization.go:182-189` `authorizeApplicationRestore` rebuilds the plan a second time and compares `current.Scope.PlanID != p.Scope.PlanID`; a stale plan returns `stale-impact-consent`. The archive is re-hashed into `data.archiveRevision` (`RestorePostgresInstancesAt` path re-binds via `data.archiveRevision`).
- `internal/applicationbackup/archive.go:112-139` `Payload.Validate`: manifest entry count, per-entry size + SHA256 digest + kind must all match; `Open` returns on any mismatch (fail closed).
- `cmd/baha/application_restore_source.go:94,118`: restored source manifest YAML must equal backup desired state (`errors.New("... does not match backup desired state")` / `"selected repository environment manifest does not match backup desired state"`).
- `cmd/baha/app_backup_restore.go:292-295`: restore refuses a non-empty target OpenBao scope (`"restore target OpenBao scope is not empty; refusing PostgreSQL mutation"`).
- Verdict: restore is not silently idempotent - each mutation re-validates the archive, re-consents, and re-checks the target is empty. No finding.

### F3 - OpenBao secret scope round-trip + manifest binding: VALIDATED (no finding)
- `internal/applicationbackup/secrets.go:21-45` `OpenBaoBackupFromPayload`: `payload.Manifest.Application/Environment` and `backup.Identity.Name/Environment` must match the restore target, else `"backup archive identity does not match restore target"`.
- `internal/applicationbackup/postgres.go:213-244` `ValidatePostgresBackupSet`: exact instance-count match, no unexpected/duplicate/empty instance; restore uses `ON_ERROR_STOP=1` + verifies `SELECT 1 == "1"` (`postgres_backup.go:199`).
- Verdict: secret + SQL payloads are identity-bound and verified after restore. No finding.

### F4 - Workload-volume ownership classification (find: bind-mount exclusion is silent-by-default, not fail-closed)
- Location: `cmd/baha/app_recovery_selection.go:188-234` `resolveRecoveryWorkloadStorage`.
- Behavior: compose volumes are classified `volume` vs `bind`. Owned `volume:` contributors get `RecoverySupported` + `DefaultSelected: true` and are captured. `bind:` mounts and external named volumes are recorded as `RecoveryExternal` + `ExplicitlyExcluded: true` (lines 195-218), so they are neither captured nor reported as a blocker.
- Observation: this matches the documented rule at `docs/reference/backup-and-restore.md:96` ("External named volumes, bind mounts ... are represented explicitly as external/excluded contributors rather than copied silently") and `recovery_discovery.go:118-119` (external identity) / `:136-141` (external logs). The classification is a discovery-time decision, not a per-archive fail-closed guard.
- Proposed card: "Make bind-mount / external-volume exclusion in `cmd/baha/app_recovery_selection.go:188-234` a recorded recovery-contributor assertion in the per-archive recovery manifest (currently external/excluded is only emitted on the discover path; a hand-edited manifest could claim a workload-storage entry without an owned backing volume). Scope: internal/applicationbackup + cmd/baha, read-only manifest assertion; no runtime change."
- Severity: low (documentation already discloses the boundary; this hardens the manifest, not the runtime).

### F5 - `writeBackupArchive` O_EXCL + atomicity: VALIDATED (no finding)
- `cmd/baha/app_backup_restore.go:687-712` `writeBackupArchive`: `os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0o600)` refuses to overwrite an existing archive; on write or close error the file is removed before returning the error. Directory created `0o700`.
- `cmd/baha/app_backup_paths.go:111-116` `ensureDefaultBackupOutsideGit`: default destination refuses to resolve inside the Git worktree.
- Verdict: backup cannot clobber an existing archive and cannot land inside the repo by default. No finding.

### F6 - Restore manifest-mismatch guard exists but is only checked on the repository-source path (find: non-registered restore relies on the archived identity, not a re-read desired manifest)
- Location: `cmd/baha/application_restore_source.go:94,118` checks `selection.Manifest.YAML() != backupManifest.YAML()` ONLY when `resolved.SourceAvailable` (a registered source repo). For a restore from a bare archive path with no source repo, the manifest identity comes from the decrypted archive (`restore_data.manifest`) and is bound through `data.archiveRevision`, not re-validated against a local desired manifest.
- Observation: this is acceptable - the encrypted archive IS the source of truth and is authenticated by the password (GCM). But the two-code-path split (`application_restore_source.go`) means the manifest-match guard is conditional on a registered source. If a restore is run against a different application repo (no matching deployment record), `resolveRestoreTarget` falls through to the `errors.New("restore preflight source repository is unavailable")` path (line 108).
- Proposed card: "Document / assert that restore identity is authoritative ONLY from the archived manifest when no registered source repo exists (`cmd/baha/application_restore_source.go:104-109`), and add a regression test that a restore of an archive whose `application_id` no longer matches any local deployment fails before the first mutation. Scope: cmd/baha test only."
- Severity: low (fail-closed on the unregistered path already; a test would pin the boundary).

### F7 - Shared-backend reconcile is idempotent (no finding)
- `internal/application/shared_backends_resources_runtime.go:406-410`: destroy-all shared backends prunes providers first and removes the env directory only AFTER both PostgreSQL and Valkey prunes succeed, so "Pruning is idempotent, so a failure between providers can be retried" (line 408). This is the data-safety idempotency contract for the shared-backend restore path.
- Verdict: shared-backend teardown is idempotent and ordered. No finding.

## Cross-check vs 0428-249 / hv38

- 0428-249 (card `t-20261122-runtime-image-registry-artifact-unknown`, blocked) is a separate active task: the 'light-runtime blob/manifest unknown' root cause is a `.github` pre-release workflow ordering + `scripts/acceptance.sh` missing-file decision, Owner `.github/**` scope. This hunt's "registry artifact retention" surface is the per-archive recovery-manifest retention (F1/F3/F4), NOT the pre-release image publication. No overlap.
- H-V38 (`evidence/r28-welle6-2026-11-26/bughunt-hv38-artifact-pins/akte.md`) covered release-image artifact pins + ORAS digest verification; it confirmed `ci-local-oci-registry.sh:61-65` rejects a non-sha256 digest. H-V39 does not touch release/image publication; its artifact retention is application-scoped recovery data, a distinct surface.

## Proposed cards

1. F4: harden bind-mount / external-volume exclusion in `cmd/baha/app_recovery_selection.go:188-234` to a per-archive recovery-manifest assertion (owned backing volume must be present when a workload-storage entry is claimed). internal/applicationbackup + cmd/baha, read-only manifest assertion. Low severity.
2. F6: add a cmd/baha regression test pinning that a restore of an archive with no matching local deployment fails before the first mutation (`cmd/baha/application_restore_source.go:104-109`). Test only. Low severity.

## Fund count

- Real (buildable card): F4, F6 (2).
- INFO / boundary hardening, optional: none separate.
- Confirmed OK (no card): F1, F2, F3, F5, F7.

Total proposed cards: 2. No product edits made. No workflow edits made. No VM/compose launched.

## Cleanliness

- docker ps -a before: `CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES` (none).
- docker ps -a after: `CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES` (none).
- No volumes, networks, state directories, or compose projects created. ambient-core/ images untouched.
- freshness: clean.
- host is the coordinator/codeman server (not a test host); no containers were started here per the Owner directive.

## Evidence witnesses

- planning remote: `origin	https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push)
- evidence commit author verified: `git show -s --format=%an HEAD` == `w172-0428-224-hunt-v39`
- push: `<range>  main -> main`
- origin/main existence witness: `git ls-tree -r --name-only origin/main | grep bughunt-hv39-backup-restore` -> `evidence/r28-welle6-2026-11-26/bughunt-hv39-backup-restore/akte.md`

## END

END_DONE w172-0428-224-hunt-v39: H-V39 backup/restore & data-safety audit complete; 2 proposed cards (F4 recovery-manifest workload-volume assertion, F6 restore-identity regression test), 5 surfaces confirmed fail-closed/idempotent (F1/F2/F3/F5/F7); no product/workflow edits, no containers.
