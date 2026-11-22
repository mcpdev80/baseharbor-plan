# PR #1752 independent review — 9140e0c8224e

## PLAN

1. Verify the product GitHub remote, current PR #1752 head and develop base, then confirm the exact head and run identity.
2. Verify ancestry, full PR diff, commit authorship, and exact base-to-head changed files.
3. Inspect guided source-pull semantics and fail-closed behavior, the MCP `app.pull` contract, and regenerated machine-control golden fixture.
4. Verify run 44968867153 is terminal success for the exact head and determine whether the relevant selected jobs actually executed.
5. Write an independent exact-head verdict with actionable repair findings; publish to Planning origin/main, update the board, and post END. Do not modify the product branch or merge.

## Review scope and witnesses

- Product remote: `https://github.com/mcpdev80/baseharbor.git`; resolved from the product worktree's `origin` URL.
- PR: #1752, branch `lane-0428-061-sourcepull`, OPEN, head `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5`.
- Base: `develop` at `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Remote refs observed: `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop`; `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5 refs/pull/1752/head`.
- `git merge-base --is-ancestor develop-6209874428 pr1752-9140e0c8`: exit 0.
- Diff: 17 files, 1,237 additions, no deletions. Changed paths:
  - cmd/baha/app_pull.go
  - cmd/baha/app_pull_options_test.go
  - cmd/baha/app_pull_render.go
  - cmd/baha/commands.go
  - cmd/baha/machine_coverage.go
  - cmd/baha/mcp_lifecycle_extra.go
  - contracts/machine/v1/control.golden.json
  - docs/cli/command-index.md
  - docs/de/cli/command-index.md
  - docs/de/reference/cli-machine-coverage.md
  - docs/de/reference/mcp.md
  - docs/reference/cli-machine-coverage.md
  - docs/reference/mcp.md
  - internal/development/source.go
  - internal/development/source_pull.go
  - internal/development/source_pull_test.go
  - internal/machine/contract.go
- `git log --oneline develop..HEAD`:
  - 9140e0c8 regenerate control.golden.json for new app.pull discovery
  - 1c8e19f6 gofmt import ordering in mcp_lifecycle_extra.go
  - 73a2f084 register faithful baseharbor.app.pull MCP handler
  - 449c3f58 sync command-index + machine coverage after 0428-065 merge
  - 6b9bb242 classify baha app pull in machine coverage
  - 403d718c restore AGENTS.md deleted from candidate
  - dab943e6 implement guided source pull
- All seven PR-only commits identify `0428-061-sourcepull` as author and committer. No foreign candidate commits were observed.
- `git diff --check develop...HEAD` produced no output.

## Findings

### F1 — REQUEST CHANGES: JSON mode exits before failure handling and skips `--up`

At `cmd/baha/app_pull.go:156-167`, JSON output returns immediately after encoding `SourcePullResult`. The unsuccessful-result check and `opts.Up` lifecycle call are below that return. Therefore `baha app pull --output json` can exit successfully with `successful:false`, and `baha app pull --output json --up` never brings the application up even when every pull succeeded. The JSON flag is accepted alongside `--up`; only `--check` plus `--up` is rejected. This is inconsistent with fail-closed CLI behavior and the advertised `--up` contract.

Repair: preserve JSON output while evaluating the result's success before returning. Ensure failed pulls return a nonzero/actionable error after emitting the structured result (or encode a documented error envelope), and ensure successful `--up` invokes the same lifecycle operation regardless of output format. Add CI-routed regression coverage for both unsuccessful JSON exit status and successful JSON-plus-`--up` lifecycle invocation.

### F2 — REQUEST CHANGES: MCP `app.pull` advertises inputs and behavior its schema/handler do not implement

`cmd/baha/mcp.go:89-93` defines `machineApplicationInput` with only `target`, `name`, and `environment`. `cmd/baha/mcp_lifecycle_extra.go:95-100` builds options with only `OutputFormat: outputJSON`; it never passes component selection or enables `Up`. Yet the registered tool description at `cmd/baha/mcp_lifecycle_extra.go:89` says “selected repository sources” and “with --up converges the application,” and generated `control.golden.json` repeats the `--up` claim. MCP callers cannot select components or request the described up behavior. The registration authorizes `app.pull` in the current context, which is appropriate, but its public contract is not semantically faithful to the CLI/tool description.

Repair: choose and implement the intended MCP contract. Either extend the typed input with explicit component selection and an explicit `up` option, pass both through the shared coordinator and retain app.pull authorization/confirmation policy, or narrow the MCP description/docs/golden to accurately describe a pull-all-sources operation with no `--up`. Add MCP schema/discovery and behavior tests for the chosen contract, including unauthorized invocation rejection.

### F3 — Non-blocking correctness/documentation issue: partial failure test does not exercise runtime partial application

`internal/development/source_pull_test.go:146-200` describes a clean source being updated alongside a dirty source, but `ResolveSourcePullPlan` marks the plan non-applyable when any blocker exists and `ApplySourcePull` returns the original plan at `source_pull.go:145-149`; thus the “clean source was updated” comment is false. The test verifies the known preflight-blocker path only. Runtime application then fast-forwards repositories sequentially (`source_pull.go:151-180`), so a later `merge --ff-only` failure can follow an earlier repository update. The aggregate result correctly remains unsuccessful and `--up` is gated on success in non-JSON mode, but the helper comment at `source_pull.go:136-139` overstates all-or-nothing mutation.

Repair: correct the test comment and document apply-time partial-update behavior accurately; add an injected apply-time failure case that proves the result marks the changed and failed repositories correctly and that `--up` never runs. Do not claim rollback/atomicity across independent repositories unless it is actually implemented.

## Guided source pull and golden fixture

`ResolveSourcePullPlan` filters by requested components, skips OCI/non-Git local sources, inspects repository root, dirty state, branch, upstream and fetched upstream revision, and classifies current/update/ahead/diverged/unavailable states. Known blockers prevent application before any fast-forward. Apply uses only `git merge --ff-only <target revision>`; it does not reset, stash, switch branches, rebase, or merge divergence. `--up` is gated on `result.Successful` in the text-output path. This is appropriately conservative for preflight state, subject to F1 and F3.

The machine golden-fixture diff is additive: exactly one `app.pull` operation record, declared mutating with confirmation and policy required, contract version v1, and MCP tool `baseharbor.app.pull`. Its description reproduces the unsupported `--up` claim, so regenerate/fix it together with F2. The CLI command index and EN/DE machine-coverage/MCP docs are in the 17-file diff; no unrelated delete or fixture churn was observed in the inspected diff.

## CI evidence

- Hosted run `44968867153`: event `pull_request`, head `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5`, completed `success`.
- Terminal aggregate `PR Selected Checks` job `137045215330`: success.
- Executed Go unit shards: `PR · Go unit · packages` job `137044053283` success; its log says `PASS all non-CLI Go package tests`. `PR · Go unit · cli-0` job `137044053261` success; its log says `PASS cli-0: 463 passed / 13 intentionally skipped / 476 discovered; CLI inventory total=1849`. CLI shards 1, 2, 3 and owner shard also completed success: `137044053458`, `137044053311`, `137044053233`, `137044053260`.
- `PR · Source format` job `137043999659` and `PR · Trusted Plan` job `137043999763`: success.
- `Release Source Preflight` and draft/main release-Go jobs were skipped for this PR event; they are not counted as passes. The terminal selected-check aggregate and executed unit shards are the relied-on evidence.
- No workflow files were changed or rerun. No local tests were run for this review.

## repo-rule compliance

- Review-only. No product source, branch, PR state, or merge was changed. No PR comment/review API action was sent.
- Findings concern only this card's implementation and public contract; #1753 remains on its existing hold, unchanged.
- Planning evidence is stored only in the real `baseharbor-plan` repository.

## cleanliness

- Before review, PID 1467884: `docker ps -a` listed seven existing exited `bh-itest-*` containers (one `edit-runtime-integration-dev-api-1`, six `shared-openbao`/`shared-postgres` containers); no running containers. This review started no Docker/Podman containers or compose projects.
- After review, PID 1467884: to be recorded before END.
- Product worktree had pre-existing untracked `0428-183-hopdev-plan/`; it was not modified.

## VERDICT

REQUEST CHANGES for exact head `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5`. Blocking findings: F1 and F2. F3 is a non-blocking but needed accuracy/test-coverage correction. Exact hosted run 44968867153 is green, but green CI does not resolve the interface and output-mode contract defects. No branch modification or merge requested. Preserve #1753 hold.

END codex-rev-1747 DONE — independent review requests changes; candidate 9140e0c8224e2ed346e6971aa0b2f6266d9c88a5
- After review, PID 1467884: `docker ps -a` again listed the same seven exited `bh-itest-*` containers and no running containers; no review-owned container was created.

## Planning publication

- Verified Planning repository remote before commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- First evidence push delivery witness: `96210383bafa3786c6cb61cc804da51937346d5a refs/heads/main`.
- Board step 105 marked done; #1753 step 104 remains done with its existing hold state.

- Exact required origin/main tree witness after fetch: `evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-head9140e0c8.md`.
- Second evidence push delivery witness: `5406131d02fb64ae7ab06c599f9eafc7810b135f refs/heads/main`.

## Follow-up exact-head review — approval contract

Follow-up plan:

1. Reconfirm the live #1752 PR ref and pinned base.
2. Compare the app.pull registry confirmation/policy flags with the MCP input and handler, then verify whether authorization itself enforces confirmation.
3. Append a concise exact-head finding to this evidence, publish it to Planning origin/main, and notify the Coordinator. No product edits.

Live ref witness at follow-up: `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5 refs/pull/1752/head`; base remained `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop`.

### F4 — CONFIRMED: MCP app.pull omits the required explicit approval gate

At exact head `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5`, `internal/machine/contract.go:242` registers `app.pull` as mutating with both `PolicyRequired: true` and `ConfirmationRequired: true`; the regenerated golden fixture publishes the same confirmation requirement. However, `cmd/baha/mcp.go:89-93` uses `machineApplicationInput`, which has no `Approval` field, and `cmd/baha/mcp_lifecycle_extra.go:88-100` calls `authorizeCurrentMCPContext` then directly calls `runAppPull`, with no `applicationlifecycle.RequireApproval` call. `machineMCPTool` at `cmd/baha/mcp.go:266-281` exposes safety annotations but does not enforce confirmation. The authorization path in `internal/operatorauth/authorization.go` copies `ConfirmationRequired` into the decision metadata; it does not reject an allowed operation for missing approval. Thus policy authorization is present, but the declared confirmation is not enforced before this MCP tool fetches and fast-forwards source repositories. This is a real contract/security gap, not only a schema-description mismatch.

Repair: add an explicit `approval` input and call `applicationlifecycle.RequireApproval("app.pull", input.Approval)` before entering `runAppPull`; add an MCP regression proving a missing approval is rejected without invoking Git fetch/pull, and approval allows the authorized operation. Keep the registry/golden confirmation requirement aligned with that enforced gate.

F4 is a blocking REQUEST CHANGES finding alongside F1 and F2. The owner’s request to preserve explicit approval is consistent with this verified gap. Product branch remains untouched.
- F4 publication delivery witness: `725a749fd455ab75ff0abd82c884a0e61d0b6cbd refs/heads/main`.
