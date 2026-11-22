# PR 1769 independent review

## PLAN

1. Resolve the PR 1769 head ambiguity and fetch exact develop ancestry and one-file diff.
2. Inspect the test for real operatorauth.WithEnforcement usage, self-contained opt-out, and reachable authentication_failed denial.
3. Verify terminal exact-head PR CI, compile, vet, and native matrix status without treating skipped checks as green.
4. Confirm PR 1741 remains open pending PR 1769 verification and merge; record read-only verdict and evidence.
5. Publish evidence on baseharbor-plan origin/main, verify path, and post END.

## Exact candidate and provenance

- Role: CODEX-REVIEW, read-only and independent.
- PR #1769: https://github.com/mcpdev80/baseharbor/pull/1769; base `develop`; branch `codex/0428-218-mcp-seam-recut`; state OPEN, merge state BLOCKED.
- Exact current PR head: `2f06b52a25a58fdddcaaab18b0eae27514a76569`; `refs/pull/1769/head` matched. The mission's `8f5f4b0` is an intermediate commit, not the current PR head or the exact-head CI target.
- Product `git remote -v` resolved `origin` and `lane-origin` to `https://github.com/mcpdev80/baseharbor.git`; only the resolved GitHub URL was used.
- Exact fetched remote develop SHA: `64eab13e23fba8bca07a1d68c687fa36afedb64e` from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`.
- `git merge-base --is-ancestor 64eab13e23fba8bca07a1d68c687fa36afedb64e 2f06b52a25a58fdddcaaab18b0eae27514a76569` exited 0.
- `git diff --name-only 64eab13e23fba8bca07a1d68c687fa36afedb64e...2f06b52a25a58fdddcaaab18b0eae27514a76569` output: `cmd/baha/mcp_operator_seam_test.go`.
- `git log --oneline 64eab13e23fba8bca07a1d68c687fa36afedb64e..2f06b52a25a58fdddcaaab18b0eae27514a76569` output, all on the PR branch: `2f06b52a2 test(0428-218): wrap fixture documentation`; `dc330f741 test(0428-218): clarify anonymous MCP fixture`; `8f5f4b0fc test(0428-218): use current operator auth fixture`; `acfee600b test(0428-218): cover MCP operator seam on current develop`.
- The exact PR diff changes no product implementation, `cmd/baha/app_broker.go`, `cmd/baha/operator_test_fixture_test.go`, `.github/**`, or `scripts/**`.

## Self-contained fixture and semantics review

- The anonymous context is created inline at `cmd/baha/mcp_operator_seam_test.go:56` using the real product symbol `operatorauth.WithEnforcement(context.Background())`. The test does not call a `withoutOperatorAuthTestContext` or other new shared helper; no 231 change is needed.
- The positive path uses existing `testOperatorContext` at line 45. The test calls the same MCP `target.create` through the workspace mutation client for both contexts.
- The negative path asserts MCP tool error at lines 61-63, `authentication_failed` at lines 67-68 and 88-90, the exact production message at lines 95-96, and absence of an authenticated principal at lines 101-103. The denial path is reachable and the gate is not weakened by the recut.
- The change from intermediate `8f5f4b0fcf31afac347aabc532691dba9da1c9f2` to current head `2f06b52a25a58fdddcaaab18b0eae27514a76569` changes only fixture documentation comments (2 lines changed); no executable code changed.
- Static content review passes.

## Exact-head hosted CI

- Exact-head run 45024804281 (`CI · Source & Quality`, `pull_request`) targets `2f06b52a25a58fdddcaaab18b0eae27514a76569`. At the final observation its status was `in_progress`, with no terminal conclusion.
- Exact run jobs `PR · Validation · go-vet` 137215487876 and `PR · Validation · go-build` 137215487890 completed `success`; `PR · Go unit · owner` 137215487912 and `PR · Go unit · packages` 137215487946 completed `success`.
- Go unit CLI shards 137215487908 (`cli-1`), 137215487934 (`cli-0`), and 137215487989 (`cli-3`) completed `success`; job 137215487942 (`cli-2`) remained `in_progress`. No terminal `PR Selected Checks` aggregate was present at final observation.
- `PR · Native · ${{ matrix.id }}` job 137215483179 was skipped. The mission allows the native matrix to be skipped for this test-only port; it is not counted as a green result.
- Run 45024804281 is not terminal green yet. Verdict: PENDING; no approval is issued while required PR-CI jobs remain in progress.

## Replacement sequence

- PR #1741 remains OPEN, unmerged, at head `fb5a5deaf36ba160b527019a3ef4eea85060905d`.
- Required order remains #1769 verified and merged before #1741 is rerun and merged. This review performed no merge, close, comment, rerun, or workflow_dispatch.

## Repo-rule compliance

- Read-only review; no product edits or local tests. No workflow files were changed and no workflows were triggered by this review.
- Planning remote first line observed: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- `python3 scripts/plan.py check`: 684 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 11 warnings.

## cleanliness

- Before review, `docker ps -a` under shell PID 83666 showed only the header and no containers.
- After review, `docker ps -a` under shell PID 87620 showed only the header and no containers. No containers were started.

## Verdict

PENDING — the exact head's implementation review passes, but exact-head run 45024804281 remains in progress and required PR-CI shards lack terminal results.

END codex-rev2-1736 DONE: PENDING for exact head 2f06b52a25a58fdddcaaab18b0eae27514a76569; wait for terminal exact-head PR-CI before approval.

## Publication witness

- Exact `git ls-tree -r --name-only origin/main | grep` output after fetching origin/main: `evidence/r28-welle5-2026-11-22/mcp-operator-seam-0428-218/review-1769-head8f5f4b0.md`
