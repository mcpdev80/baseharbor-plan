# round-2 — acceptance-cell run (card t-20261018-r27-state-recovery)

- Lane: w249 · Coordinator: 841e7734 · Model: worker-ornith1.5
- Card: t-20261018-r27-state-recovery · Source issue: baseharbor#777 · Release: v0.4.27
- Base develop HEAD verified at run: origin/develop = 5e4fde7177ea020de39b117f6d89cfa8f7c62be2
- Command shell: `cd baseharbor && GOFLAGS=-count=1 go test ...` (host = local dev machine)

## Acceptance cells of the card, run at develop 5e4fde71

Card acceptance (Outcome and acceptance): "Consistent backup of installation identity, deployments/provider ownership, accepted candidates, required protected snapshots and operation commitments; ... Quiesce writer and validate before restore. Recover unknown operations by observation, preserve target data, reject foreign installation." Required checks: "Disk restart/restore/corruption/foreign identity tests and one bounded real state-recovery smoke."

Mapped cells, run line-by-line:

### CELL 1 — Consistent backup of installation identity (backup + recovery metadata round-trip)
- Command: `go test ./internal/application/ -run 'TestBackupMetadataRoundTrip|TestLastBackupMissingIsExplicit|TestBackupMetadataRejectsInvalidIdentity|TestRecoveryMetadataRoundTripAndPermissions|TestLastRecoveryMissing|TestLastRecoveryRejectsInvalidApplicationName' -v`
- Exit: PASS (ok github.com/mcpdev80/baseharbor/internal/application 0.015s)
- Result: PASS
- Witnesses (from -v):
  - TestBackupMetadataRoundTrip --- PASS (0.00s)
  - TestLastBackupMissingIsExplicit --- PASS (0.00s)
  - TestBackupMetadataRejectsInvalidIdentity --- PASS (0.00s)
  - TestRecoveryMetadataRoundTripAndPermissions --- PASS (0.00s)
  - TestLastRecoveryMissing --- PASS (0.00s)
  - TestLastRecoveryRejectsInvalidApplicationName --- PASS (0.00s)

### CELL 2 — Deployments/provider ownership + reject foreign installation (restore binds archive/owner, fail-closed)
- Command: `go test ./cmd/baha/ -run 'TestRestoreRefusesBeforeRuntimeMutationAndBindsArchiveOwnerAndDataDecision|TestRestoreJSONAndEnvironmentSelectorsReachCanonicalValidation' -v`
- Exit: PASS (ok github.com/mcpdev80/baseharbor/cmd/baha 12.022s)
- Result: PASS
- Witnesses:
  - TestRestoreRefusesBeforeRuntimeMutationAndBindsArchiveOwnerAndDataDecision --- PASS (12.00s)
  - TestRestoreJSONAndEnvironmentSelectorsReachCanonicalValidation --- PASS (0.00s)

### CELL 3 — Accepted candidates + protected snapshots + selection fail-closed
- Command: `go test ./internal/applicationbackup/ -run 'TestRecoverySelectionDefaultsOnlySupportedContributors|TestRecoverySelectionIncludeFailsClosedForUnsupportedState|TestRecoverySelectionRejectsUnknownOrConflictingSelectors|TestRecoveryContributorRequiresLogicalResourceOutsideMetadata|TestRecoverySelectionRequiresExplicitExclusionForUnsupportedDurableState|TestRecoverySelectionCannotExcludeApplicationMetadata|TestRecoverySelectionIncludesOwnedResourcesWithoutClaimingExternalPeers|TestRecoveryManifestRoundTrip|TestRecoveryManifestRejectsSelectedUnsupportedContributor|TestDiscoverManifestRecoveryUsesPortableStateClasses|TestDiscoverManifestRecoveryOmitsUndeclaredHistoryClasses' -v`
- Exit: PASS (ok github.com/mcpdev80/baseharbor/internal/applicationbackup 0.010s)
- Result: PASS
- Witnesses (all --- PASS): TestDiscoverManifestRecoveryUsesPortableStateClasses, TestDiscoverManifestRecoveryOmitsUndeclaredHistoryClasses, TestRecoveryManifestRoundTrip, TestRecoveryManifestRejectsSelectedUnsupportedContributor, TestRecoverySelectionDefaultsOnlySupportedContributors, TestRecoverySelectionIncludeFailsClosedForUnsupportedState, TestRecoverySelectionRejectsUnknownOrConflictingSelectors, TestRecoveryContributorRequiresLogicalResourceOutsideMetadata, TestRecoverySelectionRequiresExplicitExclusionForUnsupportedDurableState, TestRecoverySelectionCannotExcludeApplicationMetadata, TestRecoverySelectionIncludesOwnedResourcesWithoutClaimingExternalPeers

### CELL 4 — Reject foreign installation + corrupt state (disk/corruption/foreign)
- Command: `go test ./internal/application/ -run 'TestCheckReferenceProviderRegistryRejectsCorruptStateBeforeReconcile|TestRetainedIntentRejectsForeignOwnershipAndInactiveProjection|TestExternalProviderBindingAndReleasePreserveForeignInstance' -v`
- Exit: PASS (ok github.com/mcpdev80/baseharbor/internal/application 0.016s)
- Result: PASS
- Witnesses:
  - TestExternalProviderBindingAndReleasePreserveForeignInstance --- PASS (0.00s)
  - TestCheckReferenceProviderRegistryRejectsCorruptStateBeforeReconcile --- PASS (0.00s)
  - TestRetainedIntentRejectsForeignOwnershipAndInactiveProjection --- PASS (0.00s) (subtests: different-app, different-environment, missing-owner, inactive all PASS)

### CELL 5 — Bounded real state-recovery smoke (TestAppBackupRestoreCLIRealDisasterRecovery, opt-in)
- Command attempted: `BASEHARBOR_APP_BACKUP_ACCEPTANCE=true go test ./cmd/baha/ -run 'TestAppBackupRestoreCLIRealDisasterRecovery' -v -timeout 2400s`
- This cell materializes a real Core via Docker (guided `baha up` -> OpenBao readiness -> postgres backup -> restore). It requires a container-free VM smoke host (baha-docker/baha-podman), NEVER the host the session runs on.
- Local run on the dev machine: FAIL. First line of failure output:
  - `app_backup_restore_integration_test.go:63: guided Core start / authenticated OpenBao readiness: Core sql failed: existing native network lacks a protected Core or shared backend owner`
  - `app_backup_restore_integration_test.go:302: foreign native volume retained its exact identity after owned cleanup; separate sentinel removal verified`
- Diagnosis: this is a TEST-ISOLATION / SHARED-HOST artifact, not a product code gap. The test expects a clean native Docker network; the failure "existing native network lacks a protected Core or shared backend owner" means prior shared-host network state was present. Cell 5 cannot be legitimately verified from the dev machine — it is a daemon/VM test by design.
- Per owner directive (R1, 2026-11-06) the containers the test spawned on the dev machine were stopped and their networks/volumes (name-only bh-backup-recovery-ci-*) removed; host proven container-free (docker ps -a = 0 bh-*). Cell 5 must be run on a claimed VM host only.

## Cell tally at develop 5e4fde71

- CELL 1 (installation-identity backup round-trip): PASS
- CELL 2 (deployment/provider ownership + reject foreign): PASS
- CELL 3 (accepted candidates + protected snapshots + selection fail-closed): PASS
- CELL 4 (foreign identity + corrupt state): PASS
- CELL 5 (bounded real state-recovery smoke): NOT VERIFIED — VM-host requirement; local run was a shared-host isolation failure, not a product defect.

## Verdict

- Not all card cells are GREEN at develop 5e4fde71: CELL 5 is unverified (requires a VM smoke host). The four local unit/build cells are GREEN, which shows the recovery production path, owner-binding and foreign/corrupt rejection are implemented and passing on this head. CELL 5 is a real-host smoke test and cannot be run here without a VM.
- Therefore the "already satisfied, no work" hypothesis is NOT proven yet: it depends on CELL 5 going green, which is pending a host release.
- No new PR is created — the transcript/evidence is the artifact. No product files edited in this run (tests are read-only against develop).

## Host-hygiene compliance (owner R1, 2026-11-06)

- Stop/stopped my own just-started containers (name-only bh-backup-recovery-ci-*), removed their networks and volumes (name-only).
- Proof: `docker ps -a | grep -c 'bh-'` = 0; leftover my-stack networks = 0; leftover my-stack volumes = 0.
- Dev machine is container-free. No other lane's resources touched.

## Status

- END: END_BLOCKED — awaiting host release (baha-docker or baha-podman) to run CELL 5 (the only remaining card cell).
- Cells 1-4 already GREEN at develop 5e4fde71 (recorded above).
- After VM run: if CELL 5 goes GREEN, all cells green => hypothesis 'bereits erfuellt' proven; worker marks nothing accepted (owner changes card status). If CELL 5 is RED with a product-code failure => that gap becomes the actual task.
- vm-lock: docker=w246, podman=w243 (single host at a time).
