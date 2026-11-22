# PR #1752 provisional findings — exact head 7b3c658800aff87ce8298fe370c5bcd448942f83

## PLAN

1. Refresh exact PR, run, branch head and current develop; compare candidate ancestry and current base.
2. Verify author/committer identity for commits since the accepted base and inspect the updated PR body.
3. Inspect F1 single-document JSON, F2 MCP input and handler, F3 partial-failure/no-up behavior, F4 explicit approval coverage, and the regenerated machine golden fixture.
4. Record findings and keep the verdict held until run 44976906715 is terminal and the Owner hops the candidate to current develop.
5. Publish this read-only review evidence to Planning; no local tests, product/PR mutations or subagents.

## Exact refs and run state

- Product remote: `https://github.com/mcpdev80/baseharbor.git`.
- `git ls-remote` witness: `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 refs/heads/develop`; `7b3c658800aff87ce8298fe370c5bcd448942f83 refs/pull/1752/head`.
- PR #1752 is OPEN and Draft at exact head `7b3c658800aff87ce8298fe370c5bcd448942f83`. Its recorded base SHA is `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Current develop is `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7`. GitHub compare `8b9a8f50645...7b3c658800a` reports diverged, ahead by 12 and behind by 5, with merge base still `6209874428f08dc3e90d6e29a42b30683ce9932a`. The candidate has not yet been hopped to current develop.
- Run [44976906715](https://github.com/mcpdev80/baseharbor/actions/runs/44976906715) is terminal `completed / failure`, event `pull_request`, exact head `7b3c658800aff87ce8298fe370c5bcd448942f83`, base `6209874428f08dc3e90d6e29a42b30683ce9932a`. `PR · Draft Go · cli-3`, job 137068733114, failed `TestEndToEndInstalledZshAndFishWrappers`; the log states `context_terminal_test.go:467: zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh": executable file not found in $PATH`. Draft source/routing (137068733130), packages (137068733199), cli-0 (137068733218), cli-1 (137068732829), and cli-2 (137068733181) succeeded. Ready-mode checks and the `PR Selected Checks` aggregate are absent from this Draft-mode run. This exact run is red and cannot qualify the updated current-base candidate.
- The PR body still describes base `d1acf3f3` and commit `4bae3194`, so that description is stale. It lists acceptance behavior but does not claim that this new head has been accepted or passed the current-base gates.
- The PR diff against its recorded base contains 19 files: `cmd/baha/app_pull.go`, `cmd/baha/app_pull_mcp_approval_regression_test.go`, `cmd/baha/app_pull_options_test.go`, `cmd/baha/app_pull_render.go`, `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go`, `cmd/baha/mcp.go`, `cmd/baha/mcp_lifecycle_extra.go`, `contracts/machine/v1/control.golden.json`, five CLI/MCP documentation files, `internal/development/source.go`, `internal/development/source_pull.go`, `internal/development/source_pull_test.go`, and `internal/machine/contract.go`.

## Findings by prior review item

- F1, single JSON document: `cmd/baha/app_pull.go:160-172` calls `emitSourcePullUpComposite` as the sole JSON write on the successful `--up` path; it no longer writes a standalone pull object first. `cmd/baha/app_pull_options_test.go:73` tests the composite helper, unmarshals one JSON document and checks its `schema_version`, `pull`, and `up` structure. Source and helper regression address the prior double-JSON defect. The helper test is not a full `runAppPull` integration test. The unsuccessful path at `app_pull.go:157-158` returns the classified CLI error before writing the result object; this provisional review does not treat that as the earlier successful-`--up` double-JSON finding.
- F2, MCP arguments: `cmd/baha/mcp.go:100-107` defines typed `components`, `up`, and `approval` fields. `cmd/baha/mcp_lifecycle_extra.go:89-110` passes component selection and `up` to the shared `runAppPull`; `machinePullComponents` removes blank values. The MCP boundary therefore exposes the component and up behavior through the same implementation as the CLI.
- F3, partial failure and no-up: `internal/development/source_pull.go:145-194` fast-forwards sources sequentially and marks the aggregate unsuccessful if any repository did not reach `current`; no cross-repository rollback is attempted. `cmd/baha/app_pull.go:157-160` returns on an unsuccessful aggregate before entering the `opts.Up` branch. `internal/development/source_pull_test.go:213-291` creates a late apply-time divergence, asserts the first source advanced, the second remains at its diverged revision, and the aggregate reports failure. This proves partial state semantics. That test exercises `ApplySourcePull` directly; it does not itself assert the CLI never calls the app-up operation, which is established here by source ordering.
- F4, approval: `internal/machine/contract.go:242` declares `app.pull` mutating with policy and confirmation required. `cmd/baha/mcp_lifecycle_extra.go:96` calls `RequireApproval("app.pull", input.Approval)` after authorizing the current MCP context and before the shared pull handler. `cmd/baha/app_pull_mcp_approval_regression_test.go:26-90` calls the production `baseharbor.app.pull` registration through an in-memory MCP server. The false case requires an MCP error with a classified code and approval-required message, using a committed clean manifest fixture. The granted case only rejects approval-related errors; it does not assert a specific successful downstream result or expected source-resolution outcome, so its positive-side assertion is weaker than the negative gate assertion.
- Machine golden: `contracts/machine/v1/control.golden.json:723-732` adds one `app.pull` record with `safety=mutating`, `confirmation_required=true`, `policy_required=true`, contract v1, and MCP tool `baseharbor.app.pull`, matching the registry metadata.

## Authorship/provenance finding

The exact `7b3c658800aff87ce8298fe370c5bcd448942f83` commit has author and committer `BaseHarbor Worker <worker@example.invalid>`, unsigned, with no GitHub author/committer account association. The immediately preceding commits `b010dabcbbd853d8ee7eaf8d28fb3869b025dec3` and `e7df5ab4a6c3219404de26846198d4f6e1b8fed0` carry the same identity pattern. This matches the previously reported unresolved provenance discrepancy in `identity-followup-e7df5ab4.md`; no attribution evidence was available in this inspection. Coordinator/Owner confirmation is still needed before relying on those commits as task-owner-authored work.

## Review limits and next evidence required

This is a provisional source/diff inspection only. No local tests were run. The exact run is active on the old base, the candidate is five commits behind current develop, and author attribution remains unresolved. Re-review the post-hop exact head and its own terminal hosted run; do not reuse this candidate's result as a verdict for a changed head.

Planning remote verified before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).

## VERDICT: HELD

No APPROVE or REQUEST CHANGES verdict: run 44976906715 is terminal failure on the old base, and the PR remains behind current develop. No GitHub review event, comment, PR-state mutation, merge or close action was made.

## END codex-rev-1747 BLOCKED

Waiting for the shared CI zsh provisioning fix, Owner hop to develop `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7`, a fresh exact-head terminal-green run, and authorship attribution for the worker-identity commits. Current run failure is recorded as STATE: `PR · Draft Go · cli-3` / `zsh: executable file not found in $PATH`.

## Publication witness

Exact output of `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-head7b3c6588.md'`:

`evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-head7b3c6588.md`
