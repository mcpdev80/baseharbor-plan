# 0427-access-wizard — round 4 evidence (finding #4: fail-closed offboarding kinds)

Card: `t-20261018-r27-access-wizard` (0427-013). Mission `0427-access-r4.txt`, lane `496759eb` (ornith, FRISCH).
Self-run. No subagents (directive 4.8).

## ## PLAN (checklist — AGENTS 4.4)

- Read mission + binding `act-1430-review.md` (commit `20810abd` on origin/main) and confirm remote truth via `git ls-remote` (PR#1430 head `5ccb81472`, develop `8a3f58da9`).
- Reconcile candidate #1430 head `5ccb81472` against the 4 findings; run existing Go wizard suite.
- Implement finding #4 only (findings #1-3 already merged in #1430): fail-closed routing for unimplemented offboarding kinds; no cross-card write.
- Add a regression proving each unimplemented `RemoveKind` fails closed and leaves the store byte-identical.
- gofmt/build/vet clean; full accesswizard + cmd/baha wizard suites PASS.
- Push named candidate branch `work/r27-access-wizard`, ls-remote witness, base-ancestor proof, own-commits-only log.
- Evidence to baseharbor-plan origin/main (ls-remote witness before END); publish handoff, card -> review, END.

## Base attestation

- Product repository: `mcpdev80/baseharbor`, fresh clone at `/tmp/opencode/0427-access-r4-wt` (NOT the quarantined ecosystem checkout `baseharbor`, which is on branch `work/r27-client-commands`).
- Base SHA I cut from (PR#1430 head, the named candidate head in the mission): `5ccb81472ef1a9ca53e065c94ccd89987fa05211`.
- `5ccb81472` IS an ancestor of my branch head — `git merge-base --is-ancestor 5ccb81472 HEAD` returns 0; confirmed via `git merge-base --is-ancestor 5ccb81472 be65de6d`.
- My branch base (`git rev-parse work/r27-access-wizard-r4^`) == `5ccb81472` == remote `work/r27-access-wizard` tip, so the push was a clean fast-forward onto the named candidate branch. No branch cut from another PR head.

## Finding reconciliation (against act-1430-review.md, verbatim recipe)

Finding #1 (PERSISTENZ), #2 (CANCEL), #3 (MULTIPLE TARGETS) are ALREADY IMPLEMENTED in candidate #1430 at head `5ccb81472`:

- #1 persistence: `internal/accesswizard/authority.go` `ResolveAssignment`/`RevokeAssignment` fold the Manager's owned profile set back into the loaded active state via the new `internal/orgconfig/profiles.go` seam `PersistActive(manager, state)` -> `SaveActive`. A persistence failure returns Deny and leaves no success (finding #1 recipe). CLI regression `TestAccessAssignPersistsThroughCLI` / `TestAccessOffboardPersistsThroughCLI` reload active state and assert the durable owned profile set.
- #2 cancel: `internal/accesswizard/controller.go` `pageSelect` maps `cancel` to a sentinel `Selection{isCancel:true}`; `Run` returns before ever invoking the `decide` write-callback, and the review screen requires explicit `yes`. `TestAccessAssignCancelAfterSelectionLeavesStateUnchanged` proves the store is byte-identical after cancel-after-selection (finding #2 recipe).
- #3 multiple targets: both command callbacks in `cmd/baha/access_wizard_command.go` loop over `review.Selected` (assign via `ResolveAssignment(..., replace=true)`; offboard via `RevokeAssignment`), never truncating to `Selected[0]` (finding #3 recipe).

Finding #4 (OFFBOARDING KINDS) was the only unmet item and is what this round implements.

## Terminal CI receipt (hosted, run on `be65de6d` — the final candidate SHA)

- Run: **CI · PR #1430**, run_id **42421669238**, run_number 5111, event `pull_request`, head_sha `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd`, branch `work/r27-access-wizard`.
- Status: **completed** / conclusion **success** (terminal; started 2026-11-07T22:40:01Z, updated 2026-11-07T22:48:21Z).
- Passed jobs (14): Workflow policy, PR · Source format, PR · Trusted Plan, PR · Focused Python, PR · Validation · cli-gofmt (job 128551266489), go-vet (128551266490), go-unit-tests (128551266500), pages-candidate-build, documentation-audit (128551266508), go-build (128551266525), mkdocs-en-strict, mkdocs-de-strict, wizard-registration-tests (128551266589), PR Selected Checks.
- Failed: **0**. Skipped (legitimate for a Go-only change; not a covered path): validate, Targeted HA · docker, Targeted HA · podman, Release Source Preflight, PR · Consumer Pins, PR · Selected Runtime, PR · Demo Pin, PR · Exact Candidate, PR · Runner Interface, PR · Public Contracts.
- No rerun or workflow_dispatch by me: the run was the normal GitHub pull_request trigger on the named candidate branch push.

## Finding place-witnesses (file:line counter-objects for the recheck)

Reviewer recheck objects — the three already-merged functional fixes in candidate head `5ccb81472`:

- **#1 Persistence** (recipe: durable write via additive seam, persistence-regression reloads store and compares): durable write seam `internal/orgconfig/profiles.go:585` `func PersistActive(manager *Manager, state ActiveState) error`; wired into both production callers `internal/accesswizard/authority.go:93` (`ResolveAssignment`) and `:148` (`RevokeAssignment`). CLI regression reloads the store and asserts the durable owned profile set: `cmd/baha/access_wizard_persistence_test.go` `ownedProfileCount`/`ownedProfile` (asserts at :118,:132,:153,:174).
- **#2 Cancel** (recipe: `cancel` after selection must NOT invoke the write-callback; review needs explicit confirmation): `pageSelect` returns the isCancel sentinel at `internal/accesswizard/controller.go:280`; `Run` returns on the sentinel BEFORE `decide(review)` at `:206` (guard at `:163`) — no write on cancel.
- **#3 Multiple targets** (recipe: loop/batch over ALL accumulated selections per route, assign+revoke, table-driven last-bearing): both command callbacks iterate `review.Selected` — assign `cmd/baha/access_wizard_command.go:64`, offboard `:129` (no `Selected[0]` truncation).

Finding **#4** (this round) implemented + witnessed above (fail-closed guard in `RevokeAssignment`, `RemoveManagedUser` only, regression `TestOffboardUnimplementedKindFailsClosedNoSilentMutation`).

Per the binding recipe: "Standalone `RemoveConnection`, `RemoveDevice`, `RemoveGrant`, `RemoveManagedUser`, `OffboardRequest`, and `ValidateOffboard` are currently declarations/helpers used only in tests ... Stop if any route requires another task's owned lifecycle/API paths; record the dependency instead of widening this PR." Mission point 4 (Owner clarification): "die vollen routes gehoeren auf t-20261018-r27-managed-users — HIER nur fail-closed, querverweis in evidence."

I did NOT implement the full production routes (they need device-lifecycle / managed-users production authorities — other cards' owned write-sets). I added a fail-closed guard at the single durable offboard route (`RevokeAssignment`):

- `internal/accesswizard/authority.go` `RevokeAssignment` now takes a `RemoveKind` argument and serves ONLY `RemoveManagedUser` (the one kind this wizard implements). Any other kind (`RemoveConnection`, `RemoveDevice`, `RemoveGrant`) returns a wrapped `ErrDenied` with a clear rejection message and mutates nothing:
  - `return &wizardError{message: fmt.Errorf("%w: %q removal is not implemented by this wizard; it is served on its own card", ErrDenied, kind).Error(), wrap: ErrDenied}`.
  - `wizardError` now carries a `wrap error` and implements `Unwrap()` so the sentinel stays on the chain (existing `errors.Is` regressions keep working).
- `cmd/baha/access_wizard_command.go` offboard callback passes `RemoveManagedUser` (existing managed-user revoke path preserved).
- Existing regressions updated to pass `RemoveManagedUser`: `internal/accesswizard/persistence_cancel_test.go` (`TestRevokePersistsThroughResolveLoad`, `TestRevokePersistenceFailureFailsClosed`) and `internal/accesswizard/offboard_scope_regression_test.go` (`TestOffboardRemovesOnlyRequestedPersonOnReviewedTarget`, `TestOffboardWrongTargetCannotRevokeAnotherProfile`, `TestOffboardNilAuthorityAlwaysDenies`).

No `.github/**` file touched. No lifecycle/fixture/OCI/node/maintenance files touched. No other card's files touched. Write-set is exactly: `cmd/baha/access_wizard_command.go`, `internal/accesswizard/authority.go`, `internal/accesswizard/offboard_scope_regression_test.go`, `internal/accesswizard/persistence_cancel_test.go`.

New regression `internal/accesswizard/offboard_scope_regression_test.go` `TestOffboardUnimplementedKindFailsClosedNoSilentMutation`: table-driven over all three unimplemented kinds (`RemoveConnection`, `RemoveDevice`, `RemoveGrant`), asserts `errors.Is(err, ErrDenied)` and that `manager.SnapshotProfiles()` is unchanged after the call (no silent first-kind mutation of the managed-user profile).

## Verification (local, SHA `be65de6d`)

- `go build ./...` -> OK (exit 0).
- `go vet ./internal/accesswizard/... ./cmd/baha/...` -> clean.
- `gofmt -l` on all four changed files -> clean (empty).
- `go test ./internal/accesswizard/...` -> ok (includes `TestOffboardUnimplementedKindFailsClosedNoSilentMutation` /1/2/3 kinds, all PASS, plus all existing offboard/revoke/snapshot regressions).
- `go test ./cmd/baha/... -run 'Access|Wizard'` -> ok (64.5s; the CLI command-level wizard suite).
- No hosted CI rerun, no workflow_dispatch, no `.github` edit. The named candidate branch push is the normal GitHub push; CI runs per repository rules.

## Branch provenance / one candidate per chain

- Named candidate branch pushed: `work/r27-access-wizard`.
- `git ls-remote origin work/r27-access-wizard` -> `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd` (my commit at tip).
- `git ls-remote origin refs/pull/1430/head` -> `be65de6d...` (PR points at the candidate branch; head advanced to my commit).
- Candidate-only log `git log 5ccb81472..be65de6d` lists ONLY my own commit:
  ```
  be65de6d fix(access-wizard): r4 fail-closed unimplemented offboarding removal kinds
  ```
- No foreign commit carried on top. The stray local branch `work/r27-access-wizard-r4` (temporary) was deleted from origin with a `ls-remote` before/after witness; it does not exist at origin.

## Evidence provenance

- Planning repository verified before the evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- Evidence path: `evidence/r27-welle5-folge-2026-11-07/access-wizard/round-4.md`.

## REPO-RULE COMPLIANCE

- No `.github/**` edits; no runner infrastructure; no VM compose.
- No other card's product files touched (no lifecycle/fixture/OCI/node/maintenance).
- No production-evidence written into the product repo (RUNBOOK 3.11 / AGENTS 3.11); evidence stays in baseharbor-plan.
- Branch cut from the named candidate head `5ccb81472` (ancestor proven); own-commits-only log.
- One integration candidate per chain; stray branch deleted.

## END

END_DONE 0427-access-r4: r4 complete. Findings #1-3 already merged in PR#1430 head `5ccb81472` (place-witnesses in this file); finding #4 now fail-closed: `RevokeAssignment` serves only `RemoveManagedUser`, unimplemented kinds (connection/device/grant) fail closed on `ErrDenied` with a clear rejection and never mutate the managed-user profile set. Commit `be65de6d` at named candidate branch `work/r27-access-wizard` tip; gofmt/build/vet clean; accesswizard + cmd/baha wizard suites PASS. Hosted CI · PR #1430 run_id 42421669238 TERMINAL success (14 passed, 0 failed, remaining skipped for Go-only change). Evidence committed to origin/main; card -> review. Cross-reference for full offboarding kind routes: t-20261018-r27-managed-users / t-20261018-r27-device-lifecycle.
