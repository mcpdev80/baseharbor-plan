# CODEX-REVIEW — maintenance client r6 — PR #1428

## PLAN

1. Read the r6 review request and inspect its round-6 evidence from planning origin/main.
2. Verify the exact PR/develop refs, ancestry, and terminal hosted run; inspect the r6 delta against the two r5 findings.
3. Record the verdict and source/test witnesses in this planning act, publish it to origin/main, and verify the published evidence and unchanged candidate.

## Verdict: APPROVE

Reviewed candidate: `9548239d85254595054337b17736b3b8941d0133` on PR #1428. The requested base snapshot `0fe53052d00a8d440b499c66a6a65c0d54bae5a0` is an ancestor of the candidate (`git merge-base --is-ancestor` exit 0). At review time the live `develop` ref had advanced to `f7a49e6818efb269cc928ad550038b2bf94d333b`; the requested base remains its ancestor (exit 0), but the current develop tip is not an ancestor of this candidate (exit 1). PR API state was OPEN with mergeability `UNKNOWN`. This verdict covers the requested SHA and r5 code findings only; it does not attest that the candidate contains the latest develop tip or is currently mergeable. Rebase/revalidation against the new base is needed before integration.

Hosted run `42428326653` was independently queried: status `completed`, conclusion `success`, event `pull_request`, head SHA exactly `9548239d85254595054337b17736b3b8941d0133`.

No candidate files were changed and this reviewer did not run tests or CI.

## R5 finding 1 — production tombstone replay reader: resolved

The production package registers the shared tombstone path resolver and ownership predicate during `cmd/baha` initialization (`cmd/baha/maintenance_tombstone.go:38-46`). The production revision lookup calls the tombstone fallback when the deployment state root is gone or has no answer for the requested revision (`internal/application/maintenance_history.go:221-257`). It derives the target and deployment identity, checks installation ownership before resolving a path, then bounds, decodes, validates, and identity-checks the record before returning the requested revision (`internal/application/maintenance_history.go:285-385`; owner predicate in `cmd/baha/maintenance_tombstone.go:59-85`).

The production replay route calls `application.LoadMaintenanceRevision` (`cmd/baha/maintenance_replay.go:20-70`), and `submitApplicationMaintenance` dispatches revision requests to that route before lifecycle mutation (`cmd/baha/app_maintenance_client.go:146-163`). The same lookup is used by commit-time idempotency (`internal/application/maintenance_authority.go:292-308`). This is a production reader path, not just a writer helper.

Regressions exercise the production reader after the faithful destroy owner removes the deployment root. The all-exit matrix checks committed tombstone replay and failed-destroy non-answerability via `application.LoadMaintenanceRevision` (`cmd/baha/app_maintenance_round4_test.go:112-247`). The no-reader mutant test proves the lookup and replay route fail closed without registration (`cmd/baha/app_maintenance_round4_test.go:397-443`); local and remote replay route tests exercise production route responses (`:445-560`). Round-6 evidence records the tombstone-reader mutant as red and the replay route tests as passing. This review did not rerun those tests.

## R5 finding 2 — retry/replay matrix oracle: resolved

The previous duplicate retry block is gone. The exit matrix now has one oracle block (`cmd/baha/app_maintenance_round4_test.go:249-291`): successful teardown replays the committed revision through the production route without a second owner mutation; a history-append failure restores the one-shot hook and retries the same revision, requiring `isNew == true`; failed torn-down owner paths assert the aborted revision is not replayable (`:186-215`).

For the owner-failure history-residue case where the state root remains observable, `TestApplicationMaintenanceHistoryRemovalMutantRedOnOwnerFailure` checks that the fixed path answers nothing and accepts the retry, while a mutant disabling only history removal leaves the revision answerable and refuses the retry (`cmd/baha/app_maintenance_round4_test.go:297-395`). The matrix and isolated mutant test therefore use the correct direction: clean rollback means no aborted replay and a successful retry where the root remains; successful destroy means replay of the committed record. The round-6 evidence reports the no-op history-removal mutation as red.

## Exact candidate delta against requested develop snapshot

The reviewed `0fe53052d00a8d440b499c66a6a65c0d54bae5a0...9548239d85254595054337b17736b3b8941d0133` source delta is 14 files, all maintenance implementation/tests under `cmd/baha/` and `internal/application/maintenance_*`; no `.github/**` or unrelated shared-surface changes are in this PR diff. The r6 correction adds the production reader/route path and fixes the matrix in the existing maintenance test file. Round-6 evidence maps these tests to hosted `PR · Validation · go-unit-tests` on the pull-request trigger, and run `42428326653` passed on the exact candidate head.

## Evidence provenance and terminal record

- Round-6 source evidence was read from planning origin/main. Its tree witness was `100644 blob 48b46718afe5ac6e5aefddc033ac6f4a6bbf9736 evidence/r27-welle5-folge-2026-11-07/maintenance-client/round-6.md`; commit prefix `343391df` is an ancestor of planning origin/main.
- Canonical planning root verification: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned exactly `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. `origin` fetch and push are `https://github.com/mcpdev80/baseharbor-plan.git`.
- Live candidate witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1428/head` returned develop `f7a49e6818efb269cc928ad550038b2bf94d333b` and PR head `9548239d85254595054337b17736b3b8941d0133`.
- No workflow rerun/dispatch, product edit, merge, tag, or release action was performed.

END_DONE integration-1428-review-r6: APPROVE; PR #1428 candidate `9548239d85254595054337b17736b3b8941d0133`; tombstone reader and corrected retry/replay oracles verified; latest develop is `f7a49e6818efb269cc928ad550038b2bf94d333b`.

Planning validation state: `python3 scripts/plan.py render && python3 scripts/plan.py check` rendered derived files; check ended with 2 errors and 2 warnings. Errors were unrelated checked cards missing evidence links: `tasks/t-20261108-bughunt-0427-appnew-contradictory-exit.md` and `tasks/t-20261108-bughunt-0427-multitarget-ambiguity.md` (“a checked card requires evidence links”). Warnings concerned accepted dependency states in two unrelated cards. Rendered derived changes were restored; only this review act is intended for commit. No unrelated card was edited to mask the validator result.

## Merge verification

- Role: CODEX-MERGE. PR #1428 merged with the standard merge strategy; no force push or protection bypass was used.
- PR API reports merged at `2026-11-08T00:37:43Z`; merge commit `419b0211317bab63cb0fa66d07892488685d3ed8`.
- Post-merge `develop` checks on the exact merge commit completed successfully: Runtime · Docker Core run `42430614314` and Runtime · Podman Core run `42430614252`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` returned `419b0211317bab63cb0fa66d07892488685d3ed8`.

END_DONE integration-1428-merge: CODEX-MERGE; PR #1428 merge commit `419b0211317bab63cb0fa66d07892488685d3ed8`; develop head `419b0211317bab63cb0fa66d07892488685d3ed8`.
