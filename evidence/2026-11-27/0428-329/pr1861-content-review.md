# PR #1861 content review — card 0428-329

**Role:** Codex REVIEW; content-only, no product or PR writes.

## Reviewed refs and diff

At review, `refs/pull/1861/head` and GitHub PR #1861 both point to `ad368f5424a2073e20fc07440f8715fd45daedf8`. PR base is `develop`; live develop is `ea5218d72e263f21e79853b679af50074dab8c25`. The PR is OPEN, mergeable=true, merge state BEHIND. GitHub's compare of live develop to the candidate reports `ahead_by=1`, `behind_by=1`, `status=diverged`; the PR's stored base SHA is older (`6d237ccdf3a5db19c5814ad5b76d01be6c38c35c`). The SHA-specific candidate diff has three files:

- `internal/runtime/repository_volume_inventory.go`: removes the heuristic that marks a volume shared/preserved because a label key/value contains “recovery” or “backup”. Existing ownership checks still mark foreign/conflicting Compose projects as shared.
- `internal/runtime/repository_volume_inventory_test.go`: changes the recovery-volume expectation and adds Docker/Podman inventory cases for owned-backup and foreign-backup labels.
- `scripts/pr-gate-coverage.json`: adds `source.internal_runtime_repository_volume_inventory_go` and `source.internal_runtime_repository_volume_inventory_test_go`, while deleting unrelated source rows and removing `runtime_specific` markers from other rows.

Blob witnesses at this review snapshot (candidate / live develop): `repository_volume_inventory.go` = `4e0ca27e24d149510784898bbc9d26fad115f0b3` / `4da5cb5f2da3bf51c6bc7675644c1d614cf8d147`; `repository_volume_inventory_test.go` = `037056d750626ff5d3ee2987da68a8ba8641849c` / `9017b83675b986b9d7c1bf4809642a3d15cbf2ff`; `pr-gate-coverage.json` = `04cc8869103ec96dba2871e09649815d538207f9` / `792a767aaceb600f5f0da228264413333014d1a8`.

There is no consent/auth path in the diff. The code direction matches card 0428-329's contract: ownership/scope metadata, not backup/recovery substrings, determines whether a volume is inside the selected installation's destroy scope. This preserves foreign/conflicting volumes while allowing an owned recovery/backup volume to be treated as owned.

## CHANGES — not accepted

Two content issues prevent acceptance:

1. The new `TestRepositoryVolumeInventoryRecoveryBackupFullDestroy` calls only `InventoryRepositoryVolumes` and asserts `Shared` flags. It does not exercise the destroy-plan output that consumes those flags, so it does not prove the card's required behavior (“owned recovery/backup volume is deleted; foreign volume remains untouched”). Add a focused regression through the real destroy-plan rendering path (`cmd/baha/app_destroy_volumes.go` / `renderRepositoryDestroyVolumes`): assert that an owned recovery/backup volume receives the explicit cleanup command, while a foreign/conflicting volume receives no destructive command and remains manual-inspection-only. Test the existing explicit confirmation path; do not add automatic consent or automatic deletion.
2. The catalog edit is not an acceptable candidate-side substitute for trusted-base admission. At live develop `ea5218d72e263f21e79853b679af50074dab8c25`, neither affected source ID is present; both are only added by this PR. The same file diff removes existing source rows and `runtime_specific` declarations unrelated to 0428-329. Remove the catalog-file edits from this product PR and preserve all existing develop rows. Route the two source IDs through the existing trusted-baseline family 0428-359/#136 (or wait for its already-authorized baseline landing); qualification requires the rows to exist on trusted develop before the refreshed product PR run. A candidate-side row cannot authorize its own Trusted Plan run.

After those corrections, w367 must absorb current develop by an ordinary forward merge and publish a final head. A carry-forward ACCEPT is possible only after an exact-head review confirms the corrected payload and that the reviewed product/test blobs are unchanged from that corrected candidate; the current head cannot be accepted by its mergeable state or by a future hop alone. The affected source files are not present in the trusted develop catalog at this review snapshot, so no qualification is claimed here.

## Scope and contract

Card 0428-329 is `tasks/t-20261126-hunt46-recovery-backup-volume-heuristic.md`. Its acceptance requires authoritative ownership rather than substring matching, an owned recovery/backup volume in the destroy scope, a foreign volume outside that scope, and regressions that prove both outcomes. This review does not broaden the card, change consent/auth, or qualify Hosted CI. The branch hop is transport work and does not cure the content findings.
