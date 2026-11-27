# PR #1881 / card 0428-310 — exact-head content review

ROLE=REVIEW
Reviewer lane: `w267-0428-284-pridentity`
Task owner from current Plan main: `w399-0428-289-providers`.
Plan main reviewed: `2f40ca1630f5919ec7c129a038ff6e2185130966`.
Task: https://github.com/mcpdev80/baseharbor-plan/blob/2f40ca1630f5919ec7c129a038ff6e2185130966/tasks/t-20261125-hunt40-migration-marker-last.md
Evidence on Plan main: https://github.com/mcpdev80/baseharbor-plan/blob/2f40ca1630f5919ec7c129a038ff6e2185130966/evidence/2026-11-27/0428-310/akte.md
Evidence blob: `0912106f7e0803385cc7cb4f65c071616354183b`.

## Exact candidate and diff

Repo `mcpdev80/baseharbor`, PR #1881, branch `lane-0428-310-migration-marker`, exact head `640f53a6e879f094010b5a6690f19193a22f6e91`, current `develop` `6944e8761af6f07b801f55e39bb9a5409226c10b`. PR state OPEN; GitHub reports BEHIND.

The current develop tip is not an ancestor of this head. The exact three-dot comparison uses merge-base `ea5218d72e263f21e79853b679af50074dab8c25` and contains four paths: `internal/orgconfig/migration.go`, `internal/orgconfig/migration_marker_test.go`, `internal/orgconfig/store.go`, `scripts/pr-gate-coverage.json`; diff stat 743 insertions, 46 deletions. `git diff --check` is clean. The candidate moves canonical data through a temp-file fsync and rename, then creates/verifies the completion marker; added tests inject marker-write failure and assert ordering, repair, and marker content.

## Review verdict: CHANGES

Finding — directory durability errors are silently treated as success. `internal/orgconfig/migration.go:167-187` returns `syncDir` after the canonical rename, but `syncDir` returns nil if opening the directory fails and also returns nil for every `Sync` or `Close` error. `ensureFrozenMarker` then proceeds to create the completion marker (`:203-209`). Thus an actual directory I/O failure can allow the code to claim a durable completion marker even though the canonical rename's directory entry was not confirmed durable. This undercuts the crash-window guarantee this task is intended to establish; the code only distinguishes no directory-sync failure from any directory-sync failure by ignoring both.

Correction recipe: propagate directory open/sync/close failures that indicate real I/O failure and do not create or report the completion marker as durable after such a failure. If some supported platforms explicitly lack directory fsync, detect and document only those unsupported-operation cases as a deliberate limitation. Add an injectable directory-sync failure test that proves the marker is not reported complete after a failed data-directory sync, while retry preserves the canonical value.

## Required checks and current state

The task requires exact test-to-gate mapping and actual passing execution. The akte identifies `TestWorldWritableMigrationMarkerWriteFailureFailsClosed`, `TestMigrateToCanonicalKeepsDataBeforeMarkerOrder`, `TestLoadActiveOptionalTwoCallRepairsLostMarkerWithoutManualWrite`, `TestFrozenMarkerContentVerification`, and `TestWriteDurableCanonicalDataFsyncsBeforeRename`; it maps package tests through the existing `PR · Go unit · packages` shard and reports native Docker and rootless Podman package gates passed on this exact head.

Current exact-head pull_request runs are both terminal: `46042082459` cancelled and `46042210279` failure. On `46042210279`, Source format, Native gate plan, Docker onboarding, and Podman workstation onboarding succeeded. `PR · Trusted Plan` failed under the known class-A freeze. The terminal `PR Selected Checks` log says `UNIT_SCOPE` was empty, `UNIT_RESULT` was `skipped`, then `REJECT: Go test selection missing or invalid`. No run is still in progress. Therefore task acceptance is not green even aside from this content finding.

No local tests were run. No PR mutation or merge was performed; Freeze #136 remains active.

END_DONE w267-0428-284-pridentity: #1881 content review completed as CHANGES at 640f53a6e879f094010b5a6690f19193a22f6e91; no merge.
