# PR #1752 read-only review — exact head e7df5ab4a6c3219404de26846198d4f6e1b8fed0

## PLAN

1. Refresh exact PR head/base, diff, and run 44974701796 using GitHub remote evidence.
2. Inspect source and regressions for F1 JSON failure status, F2 MCP schema/approval, F3 apply-time partial failure, F4 explicit app.pull authorization, and generated golden coverage.
3. Record exact run status and any findings; withhold the final verdict until the #1754 CI repair/merge and a fresh green exact #1752 run.
4. Publish this interim review evidence and preserve the separate #1753 hold. No local tests or product changes.

## Exact refs and review state

- Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).
- Product remote verified first: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push).
- PR #1752 is OPEN/Draft, base `develop`, current head `e7df5ab4a6c3219404de26846198d4f6e1b8fed0`; merge state UNSTABLE.
- GitHub compare against supplied base `6209874428f08dc3e90d6e29a42b30683ce9932a`: ahead by 11, behind by 0. The full diff has 19 files, including the pull implementation, source-pull logic/tests, direct MCP regression, and one generated machine-control golden record.
- Compared with prior reviewed head `a4adc29a5844266cf4009bb12b9b68ae26a4a99a`, this hop adds exactly two commits and three changed paths: the direct MCP approval regression test, the JSON composite helper test, and a correction to the apply-time partial-failure test. No production file changed in those two appended commits.
- The prior identity note remains relevant: the two appended commits use unsigned `BaseHarbor Worker` author/committer metadata with no linked GitHub account; see `identity-followup-e7df5ab4.md`. This review does not treat the earlier a4 verdict as covering the new commits.

## Interim source review — provisional findings, no verdict

- F1/F2 JSON result status and composite shape: `cmd/baha/app_pull.go:157-172` writes `result` to `out` when JSON is selected, then for `opts.Up` writes a second composite JSON object to the same writer. Therefore successful `--up --output json` produces concatenated JSON values rather than one document. `cmd/baha/mcp_lifecycle_extra.go:104-110` then unmarshals the combined buffer as one JSON value, so MCP `up=true` fails decoding after the shared lifecycle succeeds. The new `TestEmitSourcePullUpCompositeIsSingleDocument` (`cmd/baha/app_pull_options_test.go:73-107`) tests only the helper in isolation and misses the duplicate first write at the caller.
- F1 failure status: `runAppPull` writes the structured pull result before checking `result.Successful` (`app_pull.go:157-165`) and returns a blocked error for unsuccessful results. The aggregate logic in `internal/development/source_pull.go:182-190` sets `Successful=false` if any repository does not reach `SourcePullCurrent`. The current output ordering on the `--up` success path remains a separate blocking JSON-contract defect.
- F2 MCP contract and F4 production approval: the typed MCP input now includes `Approval` (`cmd/baha/mcp.go:100-107`); the handler first authorizes `app.pull` and then calls `applicationlifecycle.RequireApproval` (`cmd/baha/mcp_lifecycle_extra.go:89-97`). The registry row marks `app.pull` mutating, policy-required, and confirmation-required (`internal/machine/contract.go:242`), and the generated golden adds the corresponding single record. This closes the earlier missing production approval enforcement.
- F4 regression test is a false-positive risk. `appPullMCPRepository` clones the remote at `app_pull_mcp_approval_regression_test.go:102-104`, then writes `baseharbor.yaml` into that clone at `:114-118` without adding/committing it. Source inspection checks `git status --porcelain=v1 --untracked-files=normal` and sets Dirty for any output (`internal/development/source_pull.go:269-277`). Thus the fixture is dirty. With `Approval=false`, if the production approval check were accidentally removed, the call could still return a classified dirty-tree error and satisfy the test's generic non-empty code/message assertions (`app_pull_mcp_approval_regression_test.go:30-45`). With `Approval=true`, the test only rejects messages mentioning approval and accepts unrelated failures (`:48-67`). Fix the fixture to commit the manifest and assert the exact approval-required refusal for false plus successful non-error result for true.
- F3 apply-time partial failure: the corrected test now creates actual divergence only after preflight (`internal/development/source_pull_test.go:263-277`), then asserts an earlier repo advances, the later repo remains at its diverged head, and aggregate success is false (`:279-320`). This covers the documented no-cross-repository-rollback semantics.
- Golden fixture: compare shows a single additive `app.pull` operation record with mutating safety, both policy and confirmation flags true, and `baseharbor.app.pull` binding. No unrelated golden bytes were reported in the patch.

## CI and final-verdict gate

Run [44974701796](https://github.com/mcpdev80/baseharbor/actions/runs/44974701796) is terminal FAILURE on the exact head `e7df5ab4a6c3219404de26846198d4f6e1b8fed0`. Draft Go jobs cli-0 (`137061866370`), packages (`137061866406`), cli-1 (`137061866476`), and cli-2 (`137061866484`) succeeded. Draft Go cli-3 job `137061866445` failed at `context_terminal_test.go:467`: `zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh": executable file not found in $PATH`. `PR Selected Checks` job `137061868091` was SKIPPED, not a pass.

Per the current instruction, wait for #1754's CI repair/merge and a fresh terminal-green #1752 hosted run on its then-current exact head before issuing any final verdict. Revalidate the source findings if that head changes. No local tests were run. #1753 remains on its separate hold.

## repo-rule compliance

Read-only review only. No local tests, product changes, PR comments, draft/ready changes, merges, closes, or subagents.

## END codex-rev-1747 BLOCKED

Final verdict withheld pending #1754 CI repair/merge and a fresh exact-head green run for #1752.

Exact output of `git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-heade7df5ab4.md'` after fetch:

```text
evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-heade7df5ab4.md
```
