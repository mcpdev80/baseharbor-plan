# PR #1835 redundancy ruling — current develop addendum

## PLAN

1. Verify the current develop and PR exact heads, tree IDs, catalog blob IDs, and compare file list.
2. Verify card 0428-287 acceptance against current implementation and relevant tests at file and line level.
3. Check whether the original recovery payload is an ancestor of current develop and whether its full-reset regressions survive in either tree.
4. Decide whether the owner’s conditional close-as-redundant rule is satisfied; record the stale-catalog non-merge finding and the smallest delta-restoring route.
5. Publish this akte and the authorized #1853 admission line through the plan PR flow; post the final lane disposition.

## Evidence identity and base attestation

- Card owner VERBATIM as read from plan main `68cff4551f6052f1e99797ff1009275fcef8cae1` before that branch moved: `w185-0428-287-pr1835-podman`.
- Evidence author identity: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): record #1835 redundancy ruling'`.
- Pre-push gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.
- Verified plan remote before evidence worktree: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` returned `46f7fcb0ab7c417a2f8fbebe518caf1cd6b5421a refs/heads/main`.
- This evidence worktree was created detached at that exact SHA; `git merge-base --is-ancestor 46f7fcb0ab7c417a2f8fbebe518caf1cd6b5421a HEAD` succeeds before creating the evidence branch. The latest origin/main snapshot no longer contains the task files or prior w136 akte paths; the owner strings above are preserved from the immediately preceding verified plan-main snapshot, not claimed to exist in the latest tree.

## Exact candidate and catalog finding

- PR #1835 is OPEN at head `41cda5f9ff428eed147b19b0f40668060e0db8a9`, base `develop`; current develop is `fcd449117e189c555c7530b9527cd22d3f6f25ff`.
- Current develop tree is `62498eaa3adc6d4c66cfb091b1d0d143dc894973`; PR head tree is `ddf34fc5e9f482f7f9273f2acdafe86242b627d5`.
- `gh api repos/mcpdev80/baseharbor/compare/41cda5f9ff428eed147b19b0f40668060e0db8a9...fcd449117e189c555c7530b9527cd22d3f6f25ff` returns the sole tree difference as `scripts/pr-gate-coverage.json` (`ahead_by=4`, `behind_by=10`, status `diverged`).
- The PR head catalog blob is `68ad2b451f0c2c7467d3f1c989a3bf67e0d25e32`; current develop blob is `293dc02ffc999cbfeae5c87bec661898ca30acba`. The former is pre-#1852 catalog content. Merging #1835 would replace the current catalog blob with the stale blob and remove the three #1852 rows. Do not merge #1835 in its current form.
- The earlier `files=[]` comparison against the old base and the earlier equal tree ID applied before #1852; they are superseded by the current-tree comparison above.

## 0428-287 acceptance check

Card acceptance requires authorized full installation destroy/reset after an unmaterialized or broken app record, verified owned cleanup, idempotent rerun, and preservation of ambiguous, foreign, and shared resources. It also requires positive/negative regressions and independent native Docker and rootless Podman verification.

- Current develop `cmd/baha/application_destroy_authorization.go:53-58` builds the runtime retirement plan; on any reset-time `isProviderConsumerInventoryError`, it falls back to `buildIncompleteInventoryDestructionPlan`. This source has no `isStuckUnmaterializedApply` predicate checking `record.Observed.State`, readiness, and missing runtime evidence before fallback.
- The candidate tip has the same broad fallback and no stuck-state predicate. Commit `f2247a689711c1c9200b25cbb729f19cb858587d` contains the intended narrower predicate, but the final #1835 tree does not contain that change: the raw source at both `fcd449117...` and `41cda5f9...` has the broad fallback at lines 53-58.
- `cmd/baha/w287_destroy_after_failed_apply_test.go` is absent from current develop (GitHub Contents API returns 404). `cmd/baha/installation_reset_preservation_test.go` is also absent (404), so `TestInstallationResetPreservesSharedForeignProvider` is not present.
- Current develop has `cmd/baha/w154_destroy_aborted_apply_test.go:44-109`, which reconstructs an unmaterialized applying record and tests application stop (`stopSelectiveApplicationWithConsent`); it does not run installation full-reset destruction or assert that a shared/foreign provider instance and binding survive reset. It is related coverage, not the required 0428-287 regression.
- The original recovery commit `34b998e397d8d0b6931a86509c9421eb9b6165ee` is not an ancestor of current develop: GitHub compare `fcd449117...34b998e...` reports `status=diverged`, `ahead_by=1`, `behind_by=19`. Its full-reset regression test commit `e3908a4ca85855fbbc663ce640290584543be1da` likewise is not represented in either final tree; the file is absent at both tips.

## CI state

- Exact-head run `45698449498` on #1835 was a pull_request run and completed FAILURE at the PR stage boundary. The failing log line is `ValueError: no independently executable PR validation checks`; `UNIT_SCOPE` was blank and `UNIT_RESULT: skipped`. It did not execute the acceptance tests and is not a product-red/product-green result.
- No CI routing workaround or workflow edit is proposed.

## Decision and minimum route

The owner’s conditional close-as-redundant premise fails: current develop does not contain the complete accepted behavior and its full-reset shared/foreign preservation regression. Therefore keep card 0428-287 active and do not close #1835 as redundant. Keep #1835 unmerged because its tree has no useful code/test delta and carries a stale catalog blob that regresses #1852.

Minimum fix-forward on the existing card/candidate chain: hop from current develop without rewriting history; preserve the current catalog rows; restore the `isStuckUnmaterializedApply` gate from the intended f224 change in `cmd/baha/application_destroy_authorization.go`; restore the deterministic W287 failed-apply/idempotence tests and `TestInstallationResetPreservesSharedForeignProvider` in their original Go test files; prove red-first baseline and candidate pass; retain authorization/consent checks and shared/foreign preservation; then run the existing Docker and rootless Podman native data-capabilities gates as actually executed evidence. Do not alter `.github/**`, add routing hacks, or create a new card.

## Publication

Plan evidence branch and PR publication are pending. The latest fetched plan main is a new snapshot (`46f7fcb0a`) that lacks the prior task and akte paths; this is recorded above so publication will be based on current remote main rather than the old shared checkout.

- Posted the exact-head HOLD finding to PR #1835 as issue comment `https://github.com/mcpdev80/baseharbor/pull/1835#issuecomment-7175686383`; no merge or close action was taken.

## Current plan-main refresh

- Before publication, the plan remote advanced from `46f7fcb0ab7c417a2f8fbebe518caf1cd6b5421a` to `6b61a0e8c92bed0e00b075811cd214f2e4e1e9c0`. The two unpushed w136 evidence commits alone were rebased onto that fresh origin/main; no shared checkout was rebased or modified.
- Current branch `w136-1835-redundancy-ruling` is based on `6b61a0e8c92bed0e00b075811cd214f2e4e1e9c0`. `git merge-base --is-ancestor origin/main HEAD` succeeds. `git log --oneline origin/main..HEAD` lists only w136 evidence commits `2da99a861` and `930bf1e1a`; `git diff --name-only origin/main...HEAD` lists only the four evidence files above.
- Latest evidence commit author gate: `git show -s --format=%an HEAD` prints `w136-pr1836-rowsreview`.

## Publication blocker

- The mandated local `bash scripts/ci-fast-check.sh` completed with one failure at `scripts/test_ci_check_routes.py:216`, test `test_planner_validation_route_includes_planner_and_coverage_suites`: the expected planner command includes four suites but `ci.yml:1363` currently contains only two. This is an owner-scope workflow finding, so I did not push or edit `.github/**`.
- END w136-pr1836-rowsreview BLOCKED — PR #1835 remains held at `41cda5f9ff428eed147b19b0f40668060e0db8a9`; develop has incomplete 0428-287 acceptance and the candidate catalog blob is stale; local evidence is unpushed because the pre-push check failed at `scripts/test_ci_check_routes.py:216`.

- Final local evidence branch verification before END: `git log origin/main..HEAD` lists only this lane’s evidence commits, and `git diff --name-only origin/main...HEAD` lists only the four akte files. Delivery was held before any push because the pre-push check failed at the owner-only workflow scope assertion. Evidence path is therefore not yet present on origin/main.

- Final plan-publication guard: fresh `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` returned `c5b6b1faecb157a3b0d1bf856b5e2781ccd8391f`. The isolated branch was based on the preceding `6b61a0e8c` snapshot and includes that intervening owner claim commit; the coordinator’s earlier no-push notice says not to expose such unpublished owner work. Together with the failed fast-check, this leaves the akte local/unpushed pending owner lift.
