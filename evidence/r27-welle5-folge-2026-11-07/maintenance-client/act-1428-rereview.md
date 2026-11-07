# CODEX-REVIEW 0427-maintenance-review — PR #1428

## PLAN

1. Read mission, binding coordinator policies, task contract, prior review, and product rules — in progress.
2. Fetch exact PR/base refs and inspect state transitions, failure states, table-driven regressions, mutation guards, write-set, docs, and hosted CI without rerun — pending.
3. Record SHA-specific verdict and actionable recipe in canonical planning evidence — pending.
4. Publish evidence to origin/main, verify evidence and unchanged candidate witnesses, then post END — pending.

## Candidate and remote witnesses

- Planning repository root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (verified with `git rev-parse --show-toplevel`).
- Planning origin: `https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).
- Product repository: `mcpdev80/baseharbor`; PR #1428 is OPEN and MERGEABLE against `develop`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1428/head` returned develop `8a3f58da905fad52327d33466fde1d9568092519` and PR head `165405832604a01483fb192a7969c6f941dfbb06`.
- GitHub PR API head: `165405832604a01483fb192a7969c6f941dfbb06`; base name `develop`; merge state `CLEAN`, mergeable `MERGEABLE`.
- `git merge-base --is-ancestor 8a3f58da905fad52327d33466fde1d9568092519 165405832604a01483fb192a7969` exited 0.
- Exact delta against develop: 11 files, all under `cmd/baha/*` or `internal/application/*`, all maintenance implementation/tests. No `.github/**`, lifecycle, fixture, or OCI files changed. Diff stat: 3,535 insertions, 0 deletions.
- Hosted checks read via `gh pr checks 1428 --repo mcpdev80/baseharbor`: run `42409911191` terminal success. `PR Selected Checks`, `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `PR · Focused Python`, `PR · Source format`, `PR · Trusted Plan`, and `Workflow policy` passed. Runtime/owner-scoped jobs were skipped; no rerun was requested or triggered.
- The candidate worktree was detached at `165405832604a01483fb192a7969c6f941dfbb06`; review did not modify it and no tests were run locally.

## Findings

1. **REQUEST-CHANGES: successful destroy writes a stale/invalid tombstone.** In `cmd/baha/app_maintenance_client.go:343-360`, the destroy route resolves `authority`, commits the new destroy record through `commitApplicationMaintenanceWindowAuthority`, then calls `stampMaintenanceTombstone(resolved, authority.MaintenanceAuthorityRecord)`. The commit helper at `:445-481` builds and persists a separate updated `record` but returns only `error`; it does not update the passed authority. Therefore the tombstone receives the pre-commit record: for a new window it has empty operation, revision zero, and no valid digest; with prior history it retains the previous operation/revision. The tests at `cmd/baha/app_maintenance_round2_test.go:92-101` and `:150-160` assert only that the tombstone path exists, so they do not detect invalid contents. This violates the required retained, queryable success state.

   Remediation: in `cmd/baha/app_maintenance_client.go`, make the commit path return or otherwise provide the exact committed `MaintenanceAuthorityRecord`, and stamp that record (operation `destroy`, expected next revision, matching digest and deployment identity). Add a regression for both a fresh window and a pre-existing window that reads and validates the tombstone fields after local and remote destroy. The regression must fail if the tombstone is stamped from the pre-commit authority. Stop criterion: every successful destroy leaves a valid tombstone matching the committed destroy revision; owner failure leaves no destroy tombstone and rolls back both current window and history.

2. **REQUEST-CHANGES: requested table-driven all-exit regression is absent.** `cmd/baha/app_maintenance_round3_test.go` has two standalone tests. The history-residue test at `:98-155` directly invokes `application.CommitMaintenanceAuthority`; it does not exercise the client destroy route or its tombstone transitions. The lifecycle rollback test covers owner failure, but no table-driven matrix covers all destroy outcomes and their durable states. This leaves stamp failure, owner failure, and successful local/remote teardown unverified as a single state machine.

   Remediation: extend `cmd/baha/app_maintenance_round3_test.go` with a table-driven client-path matrix for commit/stamp failure, owner failure, and local/remote success, checking current window, history, tombstone content, and retry/read behavior for each outcome. Include the existing failed-destroy history-residue case through the actual client path where feasible, and retain a mutation probe that goes red when the relevant rollback/stamp guard is removed. Stop criterion: each exit has one asserted, valid durable state and the mutation probe demonstrates that the assertions reject the broken behavior.

## Contract checks

- The mission’s maintenance-only write-set is satisfied; no workflow or unrelated lifecycle/fixture/OCI paths are in the delta.
- No gate weakening or CI/workflow changes appear in the delta.
- Existing command-index syntax for `baha app destroy` (`[--yes] [--full-reset]`) and `baha app update` (`[--check] [--backup-password-file FILE | --no-backup]`) is consistent with the routes/options inspected; this candidate does not alter command registration or public flags.
- Hosted CI is green as listed above. No new CI job or local validation was triggered for this read-only review.

## Verdict

REQUEST-CHANGES for PR #1428 at `165405832604a01483fb192a7969c6f941dfbb06`. Do not accept this candidate until the tombstone contains the newly committed destroy record and the requested all-exit client-path regressions pass under the existing hosted Go unit-test and selected-check jobs. No local tests were run and no CI rerun was triggered.

END BLOCKED 0427-maintenance-review: request-changes; candidate `165405832604a01483fb192a7969c6f941dfbb06`.

## Published evidence witness

- `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-rereview.md` returned: `100644 blob 52473487c212d5079b871c0b5c1240302c52dcf8 evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-rereview.md`.
- After publishing this report, `git ls-remote origin refs/heads/main` returned `690253b4b88284508b94d93f3e0f8da4ad301d64 refs/heads/main`.
- Final candidate recheck remained unchanged: develop `8a3f58da905fad52327d33466fde1d9568092519`; PR #1428 head `165405832604a01483fb192a7969c6f941dfbb06`.
- Final pre-publish `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-rereview.md` output: `100644 blob 41150c9a336f167277ddb861f62c9dd180bc4e56 evidence/r27-welle5-folge-2026-11-07/maintenance-client/act-1428-rereview.md`.
