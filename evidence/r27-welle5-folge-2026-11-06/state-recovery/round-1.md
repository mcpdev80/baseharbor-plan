# round-1 — state recovery (card t-20261018-r27-state-recovery)

- Lane: w249 · Coordinator: 841e7734 · Model: worker-ornith1.5
- Card: t-20261018-r27-state-recovery (state: ready, all prerequisites accepted)
- Source issue: baseharbor#777 · Release: v0.4.27

## PLAN

- Read mission, card, release note, baseharbor/AGENTS.md; discover current recovery implementation state
- Claim the card via scripts/plan.py claim (commit + push)
- Cut isolated branch work/r27-state-recovery from develop HEAD; record base SHA in evidence and show it is an ancestor of first commit
- Identify and implement the actual remaining state-recovery gap (bounded, within card scope only)
- Run the smallest matching local tests; diagnose and fix real failures
- Push candidate + open PR against develop; observe the hosted checks to TERMINAL state myself (Eigenes-Run-Pflicht)
- Update planning evidence; publish evidence to origin/main; post END to coordinator 841e7734

## Discovery / current implementation state

- Card scope: restore installation identity, deployment/provider ownership, accepted candidates, protected snapshots and operation commitments; quiesce writer, validate before restore, recover unknowns by observation, preserve target data, reject foreign installation.
- Recovery feature already mature on develop: internal/application/{backup_metadata, recovery_metadata}.go, internal/applicationbackup/*, cmd/baha/app_backup_*.go, app_recovery_*.go, application_restore_*.go, target_recovery.go, update_*_recovery*.go.
- Real disaster-recovery smoke test present (opt-in via BASEHARBOR_APP_BACKUP_ACCEPTANCE=true): TestAppBackupRestoreCLIRealDisasterRecovery in cmd/baha/app_backup_restore_integration_test.go.
- Baseline: go build ./internal/application/... OK; go test ./internal/application/... OK at develop head.

## Base attestation

- develop HEAD (base ref I will cut from): <sha10 develop>
- Show this SHA is an ancestor of my first commit and list my own commits only.

## Repo-rule compliance

- Implementation confined to card scope (zustand/wiederherstellung); no other slice's files.
- No .github edits; no runner infra; no second branch/PR; no subagents; no subagents.
- Evidence lives only in baseharbor-plan; never in a product repo.

## Honest discovery result (before END)

- The recovery feature required by the card is ALREADY fully implemented and tested on develop head 5e4fde71:
  - Installation identity + deployment/provider ownership binding on restore: internal/application/{backup_metadata,recovery_metadata}.go, cmd/baha/application_restore_authorization.go (binds restore to resolved.DeploymentIdentity, 64-char archive revision, revalidate provider intent, reject foreign/missing), cmd/baha/target_recovery.go (operator-owned recovery material, never overwrites).
  - Accepted candidates + protected snapshots + operation commitments: cmd/baha/app_backup_restore.go (full restore lifecycle, quiesce writer, validate before restore, verify health, record applied deployment), cmd/baha/app_recovery_selection.go, internal/applicationbackup/*.
  - Reject foreign installation + corrupt-state: TestCheckReferenceProviderRegistryRejectsCorruptStateBeforeReconcile, TestRetainedIntentRejectsForeignOwnership, TestExternalProviderBindingAndReleasePreserveForeignInstance.
  - Bounded real state-recovery smoke: TestAppBackupRestoreCLIRealDisasterRecovery (opt-in BASEHARBOR_APP_BACKUP_ACCEPTANCE=true), cmd/baha/app_backup_restore_integration_test.go (440 lines).
  - Recent r27 recovery surface improvements already merged: #1027 (isolated backup recovery + shared resource preserve), #1396 (r27-secure-export credential adapter).
- Baseline: go build ./internal/application/... OK; go test ./internal/application/... OK.
- NO code gap, TODO, stub or failing requirement found that is in this card's scope.

## Question to coordinator (scope decision)

- The card note (planning only, unassigned) plus the card being in ready/planned suggests work was expected. But the product implementation satisfies every acceptance bullet. This is an Owner/scope decision: (A) the card is already satisfied by develop and the coordinator reassigns/closes the planning act, or (B) there is a specific bounded r27 refinement not yet on develop that the coordinator points to. A worker must not mark the card accepted/closed (Maintainer duty) nor invent new work.
- Also flagged: state-owner (card dependency) was BLOCKED on CI-environment root cause in an older shift; the current card note marks all deps accepted. Confirm the acceptance is real before any further work.

## Status

- END: QUESTION posted 2026-11-06 awaiting coordinator 841e7734 scope decision
- Lane state: BLOCKED awaiting Owner/scope decision — the recovery feature required by the card is already fully implemented and tested on develop 5e4fde71; no work may proceed without an explicit Owner directive (A) reassign/close planning, or (B) the specific bounded refinement. Worker did not mark the card accepted nor invent work (Maintainer/Owner duty).
- Evidence on disk: evidence/r27-welle5-folge-2026-11-06/state-recovery/round-1.md
