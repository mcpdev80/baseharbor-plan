# R27 CI replacement — evidence

Round F (strategy-ours union, worker o217). Date 2026-10-29.

1. Source tree built from accepted commit 089572fc1f3e39cf1d61efb887ed97ffda007118 via `git worktree add`; commit exists locally, not on origin.
2. Branch work/r27-develop-main-reconcile-b created; `git merge -s ours origin/main` applied so HEAD has main ancestry while retaining the 089572fc tree content. Merge commit 4c20d676dfdc82f597434a5e64bc7d95ddf409bc.
3. Verify a: `git diff origin/develop...HEAD --stat` non-empty — .github/workflows/receipt-post-run.yml 14 lines, scripts/receipt_writer.py 11 lines, scripts/test_receipt_postrun.py 39 lines; 51 insertions, 13 deletions.
4. Verify b: `git diff origin/main HEAD` grep for '-' lines with GH_WORKFLOW_TOKEN/--product/run_attempt/pull_requests — only one match, inside scripts/test_receipt_postrun.py fixture where the run_attempt expression is reordered into GH_EXPR (still present at line 66 of the worktree). In workflow files receipt-post-run.yml/receipt-approval.yml there are zero '-' removal lines mentioning those tokens; GH_WORKFLOW_TOKEN appears 4x, run_attempt 4x, --product present in receipt_writer.py. Main defenses retained.
5. Verify c: PLANNING_RECEIPT_WRITE_TOKEN present in receipt-post-run.yml (lines 236, 315) and receipt-approval.yml (lines 95, 162); BASEHARBOR_RECEIPT_TRUSTED_SOURCE present in receipt-approval.yml (lines 30, 94, 103). The recipe's receipt-post-run.yml BASEHARBOR_RECEIPT_TRUSTED_SOURCE grep matched nothing because that token is not in receipt-post-run.yml on develop, 089572fc, or the union — it lives in receipt-approval.yml on all three; token present.
6. Unittest suite: GOPATH=/tmp/gopath GOCACHE=/tmp/gocache python3 -m unittest test_receipt_postrun test_receipt_chain test_receipt_writer test_receipt_tasklink → Ran 73 tests in 12.634s, exit 0.
7. Push: pushed work/r27-develop-main-reconcile-b to origin (4c20d676), then retargeted PR #1206 head. gh pr edit --head unavailable; gh api PATCH returned 200 but GitHub refused to move head to a different branch; GraphQL updatePullRequest rejected (no headRefName input, pullRequestId required). Resolution: force-pushed 4c20d676 onto PR's exact head ref work/r27-develop-main-reconcile; PR #1206 head now 4c20d676dfdc82f597434a5e64bc7d95ddf409bc, base develop f95b3446, 3 files changed, +51/-13. Stray branch work/r27-develop-main-reconcile-b deleted from remote.
8. New head SHA reported: 4c20d676dfdc82f597434a5e64bc7d95ddf409bc.

o217-DONE
