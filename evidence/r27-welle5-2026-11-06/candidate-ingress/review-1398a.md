# CODEX-REVIEW — PR #1398 round 1

Date: 2026-11-06
Candidate: `9fc32d4a1f934566cb06864ea36bae448e2b036a`
Task: `t-20261018-r27-candidate-ingress`
Role: CODEX-REVIEW (read-only; no PR action)

## Verdict

**ACCEPT** — the ready-state discriminator protects a completed, consented candidate while allowing retries of an interrupted apply. Authorization, candidate immutability, and exact source selection are covered at the required seams. The diff contains no generic lifecycle-handler edits.

## Checks

- `git ls-remote origin refs/heads/work/r27-candidate-ingress` returned `9fc32d4a1f934566cb06864ea36bae448e2b036a`, equal to the reviewed candidate.
- `git merge-base --is-ancestor origin/develop origin/pr/1398` returned 0.
- Hosted run [42156133078](https://github.com/mcpdev80/baseharbor/actions/runs/42156133078) completed `success` at the exact candidate SHA. PR Selected Checks and the executed Go unit, build, vet, CLI, deployment, source-contract, formatting, focused-Python, workflow-policy, and trusted-plan jobs succeeded; path-inapplicable jobs were skipped.
- Name-only diff from develop:
  - `cmd/baha/app_candidate_consent_test.go`
  - `cmd/baha/deployment_record.go`
  - `internal/development/source_snapshot_test.go`
  No generic lifecycle-handler files are changed.

## Review evidence

- `recordDeploymentBeforeMutation` validates repository candidate consent before writing an applying record. `finalizeCandidateConsent` rejects missing or invalid confirmation; the source path returns the explicit consent error before persisting state. `TestConsentRejectsWrongDigestWriteNothing` and `TestW120RefusedApplyWritesNothingLeavesDestroyableState` cover refusal without state damage; the latter also proves destroy can re-resolve afterward.
- The immutability gate requires a prior consent with the same digest and `Observed.State == "ready"`. The ready-state threshold matches the task note: an interrupted `applying` record is not a finished candidate and must remain retryable.
- Personally ran on the exact candidate in an isolated worktree:
  - `TestInterruptedApplyRetainsOriginalIntentAcrossRetries` and `TestBackendPlacementOwnerPinsOriginalAcrossPolicyChangeAndRetry`: PASS.
  - `TestReapplyingIdenticalCandidateReturnsImmutableError`: PASS.
  - `TestConsentFillForEditSnapshot`, `TestConsentRejectsWrongDigestWriteNothing`, and `TestW120RefusedApplyWritesNothingLeavesDestroyableState`: PASS.
  - `TestSourceSnapshotPinsExactRefAtCapture`: PASS; it confirms a later trunk movement does not alter the captured reference.
- Discriminator mutation (removed `&& prior.Observed.State == "ready"`) made both interrupted-retry tests fail with the immutable-candidate error. Restoring the discriminator made both pass.
- Guard mutation (changed the guard condition to `false && ...`) made `TestReapplyingIdenticalCandidateReturnsImmutableError` fail because the identical re-apply succeeded. The source was restored; the clean worktree is at the candidate SHA with no changes.

## Decision

The exact-head evidence satisfies the mission criteria. No PR action was taken.
