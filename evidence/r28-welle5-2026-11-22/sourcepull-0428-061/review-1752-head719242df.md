# PR #1752 independent exact-head review — 719242df4762

## PLAN

1. Refresh remote PR #1752 and develop refs; verify exact requested head, base, ancestry, full diff paths and commit chain.
2. Inspect F1-F4 corrections: CLI JSON failure exit behavior and JSON-plus-`--up` composite, MCP component/up schema and approval enforcement, and runtime partial failure/reporting plus test.
3. Inspect the machine operation registry, generated golden fixture and relevant documentation; trace changed tests to existing CI selection.
4. Observe hosted run 44971297170 through terminal completion for this exact head; do not count skipped or queued checks as passing.
5. Publish an independent exact-head verdict and evidence after the hosted run is terminal. Do not modify the product branch, run local tests, merge, close or comment.

## Review scope and witnesses

- Product remote: `https://github.com/mcpdev80/baseharbor.git`, resolved from `git remote -v` in the product worktree.
- PR #1752: OPEN and draft; branch `lane-0428-061-sourcepull`; exact head `719242df4762b9cf13be113509291873d35413b3`.
- Base `develop`: `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Live remote refs observed: `719242df4762b9cf13be113509291873d35413b3 refs/pull/1752/head`; `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop`.
- `git merge-base --is-ancestor develop-6209874428 pr1752-719242df`: exit 0.
- Full base-to-head diff: 18 paths, 1,414 insertions, no deletions. Paths:
  - cmd/baha/app_pull.go
  - cmd/baha/app_pull_options_test.go
  - cmd/baha/app_pull_render.go
  - cmd/baha/commands.go
  - cmd/baha/machine_coverage.go
  - cmd/baha/mcp.go
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
- Product commits beyond develop:
  - 719242df fix F1/F2/F3 for app.pull JSON, MCP inputs, partial apply
  - 9140e0c8 regenerate control.golden.json for new app.pull discovery
  - 1c8e19f6 gofmt import ordering in mcp_lifecycle_extra.go
  - 73a2f084 register faithful baseharbor.app.pull MCP handler
  - 449c3f58 sync command-index + machine coverage after 0428-065 merge
  - 6b9bb242 classify baha app pull in machine coverage
  - 403d718c restore AGENTS.md deleted from candidate
  - dab943e6 implement guided source pull
- Commit subjects/identity show the same `0428-061-sourcepull` author for these candidate commits. No foreign commit was observed.
- No product branch, PR state, comment or review API was modified. No tests were run locally.

## Findings and acceptance review

### F1 — REQUEST CHANGES: JSON plus `--up` still emits invalid concatenated JSON

The unsuccessful JSON result is now written before the error is returned, so the caller receives structured failure output and a nonzero result. But `cmd/baha/app_pull.go:157-172` writes the pull-result JSON to `out`, then after successful `--up` writes a second composite JSON document to that same writer. `emitSourcePullUpComposite` creates one valid JSON value, but the first value remains in the stream. Thus `baha app pull --output json --up` produces two top-level JSON documents. The MCP handler then unmarshals the combined buffer at `mcp_lifecycle_extra.go:108-110`, so a successful source pull and app-up can complete and still be returned as an MCP tool failure because the output is not one JSON document. No changed test exercises JSON failure exit status or JSON-plus-`--up` output.

Repair: for JSON plus `--up`, buffer/omit the standalone pull JSON and emit only the composite value; keep the plain text path separate. Add CI-routed command tests that parse exactly one JSON document and verify the pull and `up` fields, plus a failing-pull nonzero exit regression.

### F2 — Addressed in implementation

`machineApplicationPullInput` now exposes `components` and `up`, and the MCP handler passes them into the shared CLI coordinator. `machinePullComponents` filters blank values; source filtering itself trims/deduplicates requests and rejects unknown components. This closes the earlier mismatch between MCP schema and advertised source selection/`--up` behavior.

### F3 — Partial apply behavior now explicit and regression added; execution blocked by CI compile failure

`ApplySourcePull` explicitly documents sequential fast-forwards and no cross-repository rollback. The new `TestSourcePullApplyTimePartialFailureRunsOnce` arranges a post-preflight failure after the first repo advances and asserts the aggregate failure plus per-repository states and final revisions. This accurately characterizes partial runtime failure; `--up` remains guarded on aggregate success in `runAppPull`.

The new test did not compile in the exact hosted run: `internal/development/source_pull_test.go:264:2: declared and not used: webTarget`; `internal/development/source_pull_test.go:271:12: no new variables on left side of :=`. The recorded test behavior therefore has not been executed by this run.

### F4 — Approval enforcement implemented; dedicated regression not present in this diff

The typed MCP input now includes `Approval`, and the handler calls `applicationlifecycle.RequireApproval("app.pull", input.Approval)` before `runAppPull`. The registry continues to declare policy and confirmation required. Static inspection confirms the missing explicit gate from the prior head is now enforced. However, the exact diff adds no MCP app.pull test for rejection without approval or success with approval; the only changed test files are the CLI option parser and source-pull package tests. The relevant hosted package shard failed before tests could establish this behavior. Add explicit positive/negative MCP approval coverage in a CI-selected test file.

### Machine golden and source semantics

The machine-control golden remains an additive single `app.pull` record with safety `mutating`, `confirmation_required: true`, `policy_required: true`, contract v1, and MCP tool `baseharbor.app.pull`. The generated record is aligned with `internal/machine/contract.go`; the implementation now has the explicit approval gate described above.

The guided source pull continues to select repository/local sources, fetch upstream metadata, classify dirty, detached, missing-upstream, unavailable, ahead, diverged, current, and update-available states, and apply only strict `merge --ff-only` targets. Preflight blockers remain non-mutating. Apply-time partial updates are now openly documented and surfaced per repository; there is no cross-repository rollback. No stash, reset, switch, rebase, or divergent merge was introduced.

## Hosted CI state

- Run `44971297170` is terminal `failure`, event `pull_request`, exact head `719242df4762b9cf13be113509291873d35413b3`.
- `PR · Draft Go · packages` job `137051447528` failed to build the new package test. Exact log errors: `internal/development/source_pull_test.go:264:2: declared and not used: webTarget` and `internal/development/source_pull_test.go:271:12: no new variables on left side of :=`; package log then reports `FAIL github.com/mcpdev80/baseharbor/internal/development [build failed]`.
- `PR · Draft Go · cli-3` job `137051447593` failed. Exact test log: `--- FAIL: TestEndToEndInstalledZshAndFishWrappers (0.00s)`; job summary: `CLI shard failed: (package), TestEndToEndInstalledZshAndFishWrappers`.
- `PR · Draft Go · cli-0` `137051447500`, `cli-1` `137051447278`, and `cli-2` `137051447473` completed success.
- `PR · Draft source and routing` `137051447581` completed success.
- `PR Selected Checks` job `137051449439` completed `skipped`; skipped is not a pass. The run is not acceptable as a green required aggregate.
- No workflow files were edited and no rerun/workflow_dispatch was requested or initiated.

## Cleanliness and repository rules

- Docker witness after review, PID 1551701: seven existing exited `bh-itest-*` containers were listed, with no running containers. No local tests or containers were started for this review.
- The product worktree contains pre-existing untracked `0428-183-hopdev-plan/`; it was not modified.
- Planning remote verified as `https://github.com/mcpdev80/baseharbor-plan.git`. Concurrent Planning changes in unrelated tracked files and task files were left untouched; only this evidence file is staged for publication.
- #1753 remains on its separate hold.

## VERDICT

REQUEST CHANGES for exact head `719242df4762b9cf13be113509291873d35413b3`. F1 remains blocking because JSON plus `--up` is not a single valid JSON document. F2 and the F4 implementation gap are addressed in code; F4 still lacks direct MCP approval regression coverage. F3 is represented accurately in implementation and a dedicated runtime partial-failure test, but that test did not compile. The exact hosted run failed in `packages` and `cli-3`, and `PR Selected Checks` was skipped. Do not treat this run as pass evidence. No product branch changes, merge, close, or comment.

END codex-rev-1747 DONE — exact-head review requests changes; candidate 719242df4762b9cf13be113509291873d35413b3
