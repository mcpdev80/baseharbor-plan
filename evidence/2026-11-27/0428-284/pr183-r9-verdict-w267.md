# Independent exact-head review: BaseHarbor Demo PR #183, 0428-284

## PLAN

1. Read `codex-pr183-r9-verdict.txt` and record the numbered plan in the live todo and this akte.
2. Verify the GitHub remote, exact PR head, develop base, and ancestry before reviewing.
3. Inspect the exact diff and published r9 akte for the log-only source, final-drain digest binding, positive and negative assertions, consent/auth scope, and workflow scope.
4. Record a PASS or CHANGES verdict with precise file:line findings and exact run receipts.
5. Merge PR #183 normally only if every mission criterion passes; otherwise leave it open and report the correction recipe.
6. Publish this review akte through an isolated Plan PR, validate the exact Plan head, and verify the akte path on Plan main.
7. Record the terminal outcome in the akte and post the coordinator END status.

## Visible commit identity block

- Exact task-card owner fetched from Plan `origin/main` `b0965fcc34a7209b2218d099f7421043215753fc`: `owner: w267-0428-284-pridentity`.
- Git user.name: `w267-0428-284-pridentity`.
- Git user.email: `w267-0428-284-pridentity@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push author gate: `git show -s --format=%an HEAD` must equal `w267-0428-284-pridentity` exactly.

## Provenance and receipts

- Plan remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push). The isolated Plan branch was first cut from `origin/main` `edfa742ea8ca9d3a6d4e14ad689620f507f2655d`, then fast-forwarded before its first commit to current `origin/main` `b0965fcc34a7209b2218d099f7421043215753fc`. The original cut SHA is an ancestor of the branch and first commit.
- Product remote: `https://github.com/mcpdev80/baseharbor-demo.git`.
- Fresh remote witness: `58ac70679efe5f7e95bd47d602841704fb9ffa67 refs/heads/develop`; `ee3d4c0835cdd8101f8d5cc5fdcde0f1247bb02b refs/pull/183/head`.
- Fetched review refs: `refs/review/w267-pr183-r9-develop-20261127` at `58ac70679efe5f7e95bd47d602841704fb9ffa67` and `refs/review/w267-pr183-r9-head-20261127` at `ee3d4c0835cdd8101f8d5cc5fdcde0f1247bb02b`.
- `git merge-base --is-ancestor <develop-ref> <PR-head-ref>` succeeded. `git diff <develop-ref>...<PR-head-ref> --name-only` lists only `tests/guided/drive.py` and `tests/guided/test_consent_capture.py`; there is no `.github/**` or `ci.yml` change. `git diff --check` reports one trailing blank line at EOF in `tests/guided/drive.py:798`.
- PR [#183](https://github.com/mcpdev80/baseharbor-demo/pull/183) remains OPEN, base `develop`, head `ee3d4c0835cdd8101f8d5cc5fdcde0f1247bb02b`, merge state CLEAN.
- Hosted run [46027631368](https://github.com/mcpdev80/baseharbor-demo/actions/runs/46027631368) is terminal SUCCESS on that exact head, event `workflow_dispatch`, with the executed job `Guided consent · production-path regressions` successful.
- Run [46025594967](https://github.com/mcpdev80/baseharbor-demo/actions/runs/46025594967) is terminal FAILURE on the same head, event `push`, with zero jobs. It is diagnostic only and supplies no test receipt. No rerun or dispatch was triggered by this review.
- Published implementer akte is `evidence/2026-11-27/0428-284/r9-w392-akte.md`, blob `27f133e5d4757a00286a16c9a71d4a9ddbcba49f` on Plan main. The file records the cited prior review corrections and run outcomes.

## Verdict: CHANGES

### Finding 1: production does not establish an independent log-only source

In `tests/guided/drive.py:371-385`, each PTY chunk is read with `os.read`, written to the log, appended to `capture_buffer` when `capture=True`, and counted in `bytes_read`. The final-drain loop does the same at `:433-459`. The helper at `:298-306` can append `log[already_read:]`, but the production writer advances the log and capture from the same chunks. No reachable production path in this diff demonstrates bytes present only in the log and absent from capture. `test_consent_capture.py:744-784` tests the helper with a synthetic log suffix; it does not demonstrate that divergence through `run_tty`.

Correction recipe: either provide a deterministic production-path seam that creates a real log/capture divergence and assert reconciliation repairs it, or remove the unsupported log-only-source claim and retain only a separately proven final-drain fix. Keep the regression tied to the actual `run_tty` writer path.

### Finding 2: test_25 does not bind the digest to the final-drain branch

`test_consent_capture.py:860-865` performs both `run_capture` calls before the test installs a hook at `:936-937`. The test sets `drive._test_final_drain_hook`, but `drive.py:37` defines `_run_tty_final_drain_hook`; `run_tty` reads that different module global at `:468` (and assigns it to `run_tty._final_drain_hook` at `:353`). Thus the test-supplied hook cannot observe either run. `drained["chunks"]` is only initialized and appended to in the lambda; no assertion checks its contents. The exact-once assertions at test lines `939-943` and `993-1003` prove the digest occurs once in the returned transcript, while `_final_drain_increment_static_check` proves a structural loop property; neither proves the digest was read by that branch.

Correction recipe: make the test hook a single shared seam that `run_tty` actually reads, install it before the invocation under test, and assert the digest occurs in a chunk observed from the final-drain branch. Retain the positive exactly-once transcript/log assertion and add a negative control that fails if the branch drops the digest or reconciliation duplicates it. Avoid timing-based claims.

### Scope and consent/auth review

The diff is confined to the guided test harness and its tests. It does not edit `.github/**`, `ci.yml`, product auth, authorization, or consent decision rules. The `drive.py` behavior change is test-harness capture instrumentation; no product behavior delta was found. The observed hosted success does not resolve the two static-review findings above.

No product merge was performed because the verdict is CHANGES. Card 0428-284 remains in its existing review state pending coordinator handoff of the correction recipe.

## Repo-rule compliance

- No product files were changed, no local tests were run, and no PR run was triggered.
- Review used the exact remote head and exact develop base; only the two listed candidate paths were compared.
- Evidence is isolated to this akte; generated views and other cards are not part of the planned change.

## END

END_DONE w267-0428-284-pridentity: exact-head review complete; CHANGES on PR #183, no product merge; correction recipes recorded above.

## Commit identity witness

- First review-evidence commit: `04fe029 an=w267-0428-284-pridentity cn=w267-0428-284-pridentity`.
- The canonical author and committer fields are set per-command for this branch; the pre-push gate is `git show -s --format=%an HEAD` and must print `w267-0428-284-pridentity`.
