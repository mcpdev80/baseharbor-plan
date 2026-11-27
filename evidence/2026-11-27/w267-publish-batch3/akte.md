# Publish remaining lane evidence, batch 3

## PLAN

1. Verify current Plan main and inspect PR #205 for duplicate w385-0428-078-pr1855fix content before copying.
2. Measure source SHA-256 values for the w395 disk evidence and w385 PR-1855 fix akte; compare with canonical main paths and record the nonexistent 9519106b discrepancy.
3. Publish only missing evidence in one isolated Plan PR; reference already-published w385 content instead of duplicating it.
4. Render/check Plan, qualify the exact PR head with Hosted Plan validate, record its run ID in the PR body, merge normally, and verify main commit and blobs.
5. Report PR, main SHA, validate run ID, path-to-blob mappings, and disposition of each requested file.

## Status

Plan recorded before batch-3 repository checks.


## Source and duplicate audit before branch creation

- Exact Plan origin/main before branch creation: `d1b209063daecf05fbd9723a5e0b0a99c83f45a2`; Plan origin URL is `https://github.com/mcpdev80/baseharbor-plan.git`.
- Current w395 source: `workers/evidence/w395-0428-253-deletedsrc/akte.md`, 13026 bytes, SHA-256 `238711cd123f9d5b0352cfa19bbfec1b11bf3cbd1b190f94982f5a46c430ea4d`. The predecessor at `workers/.models/ornith/w395-0428-253-deletedsrc-evidence.md` has SHA-256 `a2e9c58f9bec35be29e5c559b61dfc95fb12fea4b2a2df53fc23d6644f086b4e`; the earlier lane hash `9519106b` was identified as pre-edit and is not the current source hash.
- PR #205 is CLOSED, unmerged (`mergedAt` null); its head file at `evidence/2026-11-27/w385-0428-078-pr1855-checkpoint/akte.md` has the same content SHA-256 `a2dfccd2e098bfbddf0d415c7cd258f2779be9f80441f24457953e05cd7bf9bf` as the current w385 source. It was initially absent from main at `d1b2090`, but a subsequent main update added that exact checkpoint path and identical content. PR #205 remains closed and unmerged; the publication came through commit `d8f88d7ecf13e75dff410ee6f110059e49c6dbf8`. The current main blob is `4c044e50f08635fb5e6972b58d9fdc98469918f4`. The requested canonical path `evidence/w385-0428-078-pr1855fix/akte.md` is absent, so this batch references the published checkpoint instead of creating a duplicate.

## Current-base attestation and commit identity (before first commit)

- Fresh Plan `origin/main` at branch cut: `71812e2b7aad1f2a0cbff85d5f6f8657eaa1ca46`; remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- Exact task owner values fetched from that base: 0428-253 task `tasks/t-20261123-planner-deleted-source-advisory.md` has `owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)`; 0428-078 task `tasks/t-20261114-r28-perses-dashboard-identity.md` has `owner: w385-0428-078-pr1650pre`.
- Commit author and committer: `w267-0428-284-pridentity`; email: `w267-0428-284-pridentity@baseharbor.local`.
- Literal commit invocation: `git -c user.name='w267-0428-284-pridentity' -c user.email='w267-0428-284-pridentity@baseharbor.local' commit -m 'Publish remaining staged lane evidence batch 3'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w267-0428-284-pridentity`; also record `git log --format='%h an=%an cn=%cn' -1`.
- Base ancestry will be checked with `git merge-base --is-ancestor 71812e2b7aad1f2a0cbff85d5f6f8657eaa1ca46 HEAD`; the branch is `w267-0428-284-pridentity/publish-batch3`.

## Additional source findings

- w395 current source is `workers/evidence/w395-0428-253-deletedsrc/akte.md` (13,026 bytes, SHA-256 `238711cd123f9d5b0352cfa19bbfec1b11bf3cbd1b190f94982f5a46c430ea4d`). Its prior-stage file `workers/.models/ornith/w395-0428-253-deletedsrc-evidence.md` hashes to `a2e9c58f9bec35be29e5c559b61dfc95fb12fea4b2a2df53fc23d6644f086b4e`; `9519106b` was the earlier pre-edit hash reported by the lane, not the present file hash.
- w385 PR #205 is CLOSED and unmerged (`mergedAt: null`). It contains the same w385 content (SHA-256 `a2dfccd2e098bfbddf0d415c7cd258f2779be9f80441f24457953e05cd7bf9bf`) at the checkpoint path, now published on main as blob `4c044e50f08635fb5e6972b58d9fdc98469918f4` by commit `d8f88d7ecf13e75dff410ee6f110059e49c6dbf8`. Leave `evidence/w385-0428-078-pr1855fix/akte.md` absent to avoid duplicating this already-published content.
- The #284 round-7 akte says candidate head `dc041ca122d60dfafd09baa882a4872ea4542df0`, while its source filename used ancestor `ba14b0eed`. The requested published filename `round-7-dc041ca12.md` reflects the final candidate head; source bytes remain unchanged (SHA-256 `1ec6716711068375b0c208bbbeddf007beece32e8daeba0685502106173cad2d`).
- Read-only inspection of `tests/guided/drive.py:420-447` and `tests/guided/test_consent_capture.py:788-977` in the w392 worktree shows `_final_drain_hook` is called with the actual chunk read inside `run_tty`'s post-`proc.poll() != None` drain loop, and test_25 asserts that this captured chunk contains the digest. This is a real branch-observation mechanism, not a preconstructed counter value. However, the evidence akte records no Hosted run on final head `dc041ca12`; run `45965565557` is a workflow_dispatch pass on predecessor `ba14b0eed`. Final-head execution remains unproven and requires the Owner-authorized trigger; this publication does not claim otherwise.

## Scope and checks

- Publish exactly these two still-missing files, byte-identically: `evidence/w395-0428-253-deletedsrc/akte.md` and `evidence/2026-11-27/0428-284/round-7-dc041ca12.md`. Reference the w385 checkpoint path already on main instead of duplicating it.
- No product-repository write, no card edit, no local test run, no workflow dispatch, no force push, and no history rewrite.
- Plan render/check is required before the Plan PR; Hosted Plan validation must pass on the exact PR head. Merge is a normal Plan PR merge only after the current-base/head/run checks.
- `python3 scripts/plan.py render && python3 scripts/plan.py check`: completed; 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors and 10 pre-existing v0.4.27 dependency warnings. `git diff --check` passed. The two copied files have the source-matching hashes listed above, and none of the three new evidence files contains a markdown task checkbox.

## END BLOCKED

Batch-3 Plan PR is in progress; final PR number, exact-head validate run, merge SHA, main blob IDs, and END_DONE will be recorded after hosted validation and merge.
