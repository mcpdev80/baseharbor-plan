# CODEX-MERGE verification: PR #1756

## PLAN

1. Confirm develop ref and PR #1756 merged state from GitHub.
2. Verify merge commit parents are the approved head and prior develop.
3. Confirm exact-head review and CI receipts.
4. Publish read-only merge evidence on Planning main.
5. Mark the board complete and post coordinator END.

Session marker: merge1756-witness-20261122
Role: CODEX-MERGE verification, read-only
Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).

## Merge verification

merged: yes (the owner had already merged PR #1756 before this verification; no merge command was issued in this session).

Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1756/head` returned:

    52a3c5446f41a1dd8678d99875e4cb1eee67874c refs/heads/develop
    ebb6c9434a6c1fddacbce487ceb6071f268d4709 refs/pull/1756/head

`GET /repos/mcpdev80/baseharbor/pulls/1756` reports `state=closed`, `merged_at=2026-11-22T06:29:02Z`, `merge_commit_sha=52a3c5446f41a1dd8678d99875e4cb1eee67874c`, head `ebb6c9434a6c1fddacbce487ceb6071f268d4709`, base `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9`, and merged_by `mcpdev80`.

The merge commit has exactly two parents in the normal GitHub merge-commit order: old develop `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9`, then approved candidate `ebb6c9434a6c1fddacbce487ceb6071f268d4709`. This is a merge commit, not a squash commit or rebase-merge. Merge commit SHA: `52a3c5446f41a1dd8678d99875e4cb1eee67874c`.

## Review and CI receipts

The independent exact-head review `evidence/r28-welle5-2026-11-22/gate-admission-census/review-1756-headebb6c9434a6.md` is on Planning `main` and contains `VERDICT: APPROVE` with a merge recommendation for the normal gates.

Exact-head run `44992226702` on `ebb6c9434a6c1fddacbce487ceb6071f268d4709` is terminal SUCCESS with 0 failed jobs. Required aggregate `PR Selected Checks` job `137115951661` passed from Actions integration `15368`. `PR · Validation · pr-planner-tests` job `137115616321` passed; other required validation receipts `ci-executor-tests` `137115616265`, `ci-policy` `137115616294`, `receipt-execution-tests` `137115616351`, `PR · Source format` `137115562365`, `PR · Trusted Plan` `137115562368`, `PR · Native gate plan` `137115562373`, and `PR · Focused Python` `137115616252` all passed. `PR · Selected Runtime` `137115617859` was SKIPPED as documented before the new catalog rows were in develop; it is not treated as runtime evidence.

At the new develop stand `52a3c5446f41a1dd8678d99875e4cb1eee67874c`, `scripts/pr-gate-coverage.json` contains 190 component rows and 15 native-check rows, including all nine newly admitted native rows. The catalog rows are now in the base for subsequent candidate selection. The earlier empty matrix did not exercise those runtime gates.

## Scope and cleanliness

Read-only merge verification. No merge command, product write, GitHub comment, local test, workflow dispatch, force-push, or bypass was performed in this session.

Before publication: PID `2923735`; `docker ps -a` returned only its header and no containers. No containers or compose projects were started.

## Publication

This evidence path was created on Planning `main` at commit `4b51a8911c37053266af3f3e94228028367028bf`. The completed evidence update was published and witnessed by `aab6640655572cd2c67649c3beafe01ae1b823ca refs/heads/main` from `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`.

## END codex-rev2-1736 DONE

merged: yes. New develop SHA `52a3c5446f41a1dd8678d99875e4cb1eee67874c`; normal merge commit parents are `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9` and `ebb6c9434a6c1fddacbce487ceb6071f268d4709`. PR state closed/merged at `2026-11-22T06:29:02Z`. No merge command issued by this session. Planning evidence publication witness: `aab6640655572cd2c67649c3beafe01ae1b823ca refs/heads/main`.