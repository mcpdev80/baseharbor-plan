# Independent exact-head review: PR #1752

Verdict: APPROVE — implementation review against card 0428-061. No code findings at the reviewed head. This is not merge clearance: the PR remains Draft, the card remains blocked on the owner authorship decision recorded in its frontmatter, and the run's `PR Selected Checks` aggregate was skipped.

## PLAN

1. Read the corrected mission, card 0428-061, owner CLI brief, and command mapping.
2. Refresh the exact PR head, develop base, and hosted run through the verified GitHub remote.
3. Inspect the source-pull, CLI/MCP, generated contract, and regression evidence without changing product files or running local tests.
4. Record the verdict and remaining non-code blockers in Planning evidence.
5. Validate and publish the evidence, update the live board, and post the terminal handoff.

## Scope and provenance

- Corrected contract: `t-20261114-r28-cli2-source-pull`, card 0428-061. Its frontmatter names PR `mcpdev80/baseharbor#1752`, with dependencies on `t-20261114-r28-cli2-app-lifecycle` and `t-20261114-r28-cli2-source-model`.
- Exact PR: https://github.com/mcpdev80/baseharbor/pull/1752, OPEN and Draft. Head `34feb493480ec3b2703681bf576ce41e3904995b`; base `develop` at `1ff16925c4e141d732459a34ddf0b7f49128a214`. Fresh `git ls-remote` returned those exact OIDs for `refs/pull/1752/head` and `refs/heads/develop`; GitHub compare reports 15 commits ahead, 0 behind, 19 changed files.
- Planning remote identity, checked before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- The previous finding that workload-port behavior was missing is retracted: 0428-199 is not this PR's contract. The corrected contract is 0428-061.

## Contract review

Card acceptance is met by the reviewed implementation:

- Safe whole-repository pull, component selection, strict fast-forward only, dirty/ahead/diverged/no-Git blockers, preview, and actionable noninteractive failures are described in `cmd/baha/app_pull.go:24-35` and implemented in `cmd/baha/app_pull.go:46-119,122-151`. The owner brief defines `app pull` as the Git-source update, whole-repository pull semantics, `-c`, and shared-impact preview in `evidence/cli-redesign-20261114/brief.md:8-9`; the command map maps prior workspace/app update operations to `baha app pull` at `evidence/cli-redesign-20261114/command-map.md:66,118,151`.
- The source planner's apply path uses `git merge --ff-only`, records per-repository failures, marks aggregate success false if any repository is not current, and explicitly documents that there is no cross-repository rollback at `internal/development/source_pull.go:136-193`. The implementation fails before `--up` unless the aggregate pull succeeds at `cmd/baha/app_pull.go:153-183`.
- Runtime partial failure is explicitly tested: `TestSourcePullApplyTimePartialFailureRunsOnce` introduces a later-source divergence after an earlier source advances and verifies unsuccessful aggregate status and retained per-repository state at `internal/development/source_pull_test.go:206-321`. This is a deliberate partial-application contract, not an all-or-nothing transaction. Preflight-blocked partial selection has its separate test at `internal/development/source_pull_test.go:146-204`.
- Relevant regression coverage also includes dirty-tree refusal (`internal/development/source_pull_test.go:54-83`), diverged history (`:85-116`), no Git repository (`:118-144`), same repository mapped across components only once (`:324-353`), component filtering (`:355-394`), unknown component fail-closed (`:396-405`), and non-mutating preview (`:407-439`).
- For `--up --output json`, `cmd/baha/app_pull.go:160-183,186-201` emits one JSON object containing `pull` and `up`; it buffers the lifecycle output rather than concatenating two JSON documents. `cmd/baha/app_pull_options_test.go` covers the single-document composite output. The exact head's generated CLI command index and machine-control fixture include the new command/tool surfaces; the golden declares `app.pull` mutating, confirmation-required, policy-required, and `baseharbor.app.pull` at `contracts/machine/v1/control.golden.json:723-730`.
- MCP matches the owner brief's requirement to preserve the underlying domain/MCP operation. The typed `machineApplicationPullInput` exposes target/name/environment, components, `up`, and explicit `approval` at `cmd/baha/mcp.go:95-107`. The registered `app.pull` handler authorizes the current MCP context, calls `applicationlifecycle.RequireApproval("app.pull", input.Approval)`, reuses `runAppPull`, and returns the structured result at `cmd/baha/mcp_lifecycle_extra.go:84-113`. This resolves the prior F4 approval gap. `TestAppPullMCPApprovalRegression` drives the production MCP registration and checks refusal without approval plus passage through the approval gate with approval at `cmd/baha/app_pull_mcp_approval_regression_test.go:14-77`.

## Card relationship and authorship note

- 0428-061 frontmatter has `depends_on: [t-20261114-r28-cli2-app-lifecycle, t-20261114-r28-cli2-source-model]` and `prs: [mcpdev80/baseharbor#1752]`.
- 0428-225 frontmatter has `depends_on: []` and `prs: [mcpdev80/baseharbor#1751]`. It is the Perses release-gate drift task, not a source-pull dependency. These fields establish that source pull belongs to 0428-061, not 0428-225.
- Per mission, authorship only: commits `b010dabcb`, `e7df5ab4a6c`, and `7b3c65880` have author `BaseHarbor Worker <worker@example.invalid>`. This remains the owner's decision; I make no authorship verdict.

## Hosted evidence and limits

Run `44987053069` completed SUCCESS at exact head `34feb493480ec3b2703681bf576ce41e3904995b`. Draft source-and-routing job `137099809829`, Draft Go packages `137099809947`, cli-0 `137099809960`, cli-1 `137099810267`, cli-2 `137099810028`, and cli-3 `137099810021` succeeded. In cli-3, both “Install interactive shells for the shell-wrapper path” and “Run installed zsh and fish wrapper regression” succeeded. The packages and other CLI shards skipped those shell steps; cli-3 is the executed shell evidence. `PR Selected Checks` job `137099812604` was SKIPPED, as were the native/HA and other non-Draft paths. Therefore this review confirms the requested Draft Go evidence but does not claim all required CI gates passed.

No local tests were run. No product branch, PR state, review, or GitHub comment was changed.

## repo-rule compliance

Read-only review used GitHub API content at the exact head and Planning task/brief sources. Evidence is stored only in the `baseharbor-plan` repository. No product files were modified and no local product tests were run.

## cleanliness

Before review, `docker ps -a --no-trunc` returned no containers. After review, `docker ps -a --no-trunc` returned no containers. Session PID: 2435850.

## END codex-rev-1747 DONE

Exact-head verdict: APPROVE for implementation at `34feb493480ec3b2703681bf576ce41e3904995b`; card 0428-061 acceptance is met in the reviewed code, with no code findings. MCP difference: none; typed arguments and explicit approval enforcement are present. Card 0428-199 is not this PR's contract. Merge remains held by the Draft state, skipped `PR Selected Checks`, and owner authorship decision.
