# ROLLE: REVIEW — core PR #1860 content review

- **Reviewed head:** `f5dee5fa525b6825bb5c0dfd72ccf8df92fd7a0c`
- **Base:** `develop` at `ea5218d72e263f21e79853b679af50074dab8c25`
- **PR state:** OPEN; GitHub reports `MERGEABLE`, `mergeStateStatus=BLOCKED`.
- **Verdict:** CHANGES. This is a content verdict only; it does not resolve the recorded Trusted Plan/base-lineage blocker.

## Contract and diff

Card 0428-312 (`tasks/t-20261125-hunt39-volume-recovery-manifest.md`) calls for a test that asserts every owned workload volume appears as a `workload.storage` recovery-manifest contributor and fails closed on omission. The PR diff against the exact `develop` base contains only `internal/applicationbackup/recovery_manifest_workload_test.go` and `scripts/pr-gate-coverage.json`; it adds no product implementation, consent/auth behavior, or workflow change.

`TestWorkloadVolumesAssertedInRecoveryManifest` constructs a selection with `postgres-data` and `cache`, serializes it through `RecoveryManifestPayloadEntry`, reads it with `RecoveryManifestFromPayload`, and checks the two returned contributors and ownership. This is a useful serialization round-trip, but its fixtures are hand-constructed rather than discovered from an application with declared workload volumes.

`TestRecoveryManifestFailsClosedOnMissingOwnedWorkloadVolume` does not exercise a product fail-closed path. It creates a selection and an incomplete manifest, calls `manifest.Validate()` (which succeeds because `RecoveryManifest.Validate` validates only the manifest's own version/contributors and does not compare it with a selection), then performs a test-local nested loop and calls `t.Fatalf` itself when the entry is absent. The test therefore proves its local assertion, not that capture or recovery rejects the missing selected volume. Add a regression that invokes the relevant production capture/recovery validation path and demonstrates that the omitted owned durable volume is rejected there; preserve the passing-manifest case as well.

`TestRecoveryManifestDiscoveryDoesNotInventWorkloadVolumeStateClass` constructs an application with no workload declaration and checks that discovery adds no workload-storage contributor. Retain this negative case, and add a positive discovery fixture if it is the intended proof that declared volumes are collected.

## Trusted catalog and #1861 substitution check

The candidate also adds `source.internal_applicationbackup_recovery_manifest_workload_test_go` for `internal/applicationbackup/recovery_manifest_workload_test.go`, with Docker and Podman `data-capabilities` surfaces and `runtime_specific: true`. That row is absent from the reviewed trusted `develop` catalog at `ea5218d72e263f21e79853b679af50074dab8c25`; adding it in this product PR cannot self-authorize the source for the trusted-base planner. The #1861 row is for `internal/runtime/repository_volume_inventory_test.go` (a different source ID and path), so it cannot substitute for this row. Route this source row through the accepted develop-side 0428-359/#136 baseline family; remove the candidate-side catalog addition from #1860. Do not weaken the trusted planner.

## Carry-forward

The review applies only to head `f5dee5fa525b6825bb5c0dfd72ccf8df92fd7a0c`. A forward hop may carry unchanged test content, but this CHANGES verdict is not acceptance: review the corrected exact head and its required hosted evidence anew. The catalog correction must land on `develop` before the product candidate is requalified against that trusted base.
