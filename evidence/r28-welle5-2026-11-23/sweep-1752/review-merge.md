# PR #1752 post-merge review

ROLE: REVIEW

VERDICT: APPROVE

## PLAN

1. Read the #1752 mission and task contract; record the exact candidate, base, acceptance checks, and evidence path.
2. Refresh the product and Planning remote witnesses and inspect the exact PR diff and merge state.
3. Inspect source-pull behavior, consent handling, catalog coverage, and hosted test receipts.
4. Compare all acceptance criteria with the exact-head candidate and terminal CI results.
5. Publish this review evidence only in the actual baseharbor-plan repository.
6. Confirm the evidence path on origin/main, update the live board, and post the required END.

## Review scope and result

Card 0428-061, “Implement guided source pull.” PR #1752 (`lane-0428-061-sourcepull`) had exact base `7b45db92deed6c4dbc4b81f355422a8276e2740e` and exact tested head `9e7c74409916ac7118e3f4765a9553a427fb218d`. GitHub reports the PR merged at 2026-11-23 16:37:47Z as `dc8626e9c52be07a8ea5b87b468c5991b7540c4f`.

The 19 changed paths are within the guided app/source-pull implementation, its CLI/MCP/contract surfaces, generated command and machine reference documentation, and focused tests:

- `cmd/baha/app_pull.go`
- `cmd/baha/app_pull_mcp_approval_regression_test.go`
- `cmd/baha/app_pull_options_test.go`
- `cmd/baha/app_pull_render.go`
- `cmd/baha/commands.go`
- `cmd/baha/machine_coverage.go`
- `cmd/baha/mcp.go`
- `cmd/baha/mcp_lifecycle_extra.go`
- `contracts/machine/v1/control.golden.json`
- `docs/cli/command-index.md`
- `docs/de/cli/command-index.md`
- `docs/de/reference/cli-machine-coverage.md`
- `docs/de/reference/mcp.md`
- `docs/reference/cli-machine-coverage.md`
- `docs/reference/mcp.md`
- `internal/development/source.go`
- `internal/development/source_pull.go`
- `internal/development/source_pull_test.go`
- `internal/machine/contract.go`

The machine operation/coverage and generated-reference integration is the documented coordinator exception in the card history. No `.github/**` or `scripts/**` path changed. The PR does not modify the workflow surface.

## Acceptance findings

- Dirty, ahead, detached, missing-upstream, divergent, and non-repository paths become blocked/non-applyable states. Source pull uses strict `git merge --ff-only` against the preflight target revision; it does not stash, reset, switch, rebase, or merge divergent history.
- A selected source is represented once when multiple components map to it. `TestSourcePullSameRepoAcrossComponentsStaysOnce` asserts one repository result for the shared source.
- Preflight partial failure stays unsuccessful without applying a blocked selection. The separate apply-time partial-failure test proves the aggregate remains unsuccessful after one repository advances and another fails; the failed repository is left as-is, and the CLI returns before the `--up` lifecycle.
- `--up` is invoked only after a successful pull result. `--check` and `--up` are mutually exclusive, check mode only renders the plan, and JSON `--up` emits one composite document.
- The MCP surface calls `RequireApproval("app.pull", input.Approval)` before the shared pull path. `TestAppPullMCPApprovalRegression` verifies approval=false is refused by the approval gate and approval=true is not refused by that gate.
- The command is noninteractive, returns actionable blockers, and documents that secret values are not printed. The reviewed result and plan structures contain source/revision/state/blocker metadata and no application secret fields.
- Repository/local sources are handled; unsupported source types are skipped explicitly by the source-pull planner rather than being reported as pulled.

Catalog bytes are unchanged from exact base through candidate and current develop. The Git blob SHAs match at all three refs:

- `scripts/pr-gate-coverage.json`: `905742ae83257b0c38148cc3fb83de722184839a`
- `scripts/pr-native-gate-plan.py`: `4259fbf665f80f6e6cb43bb0995f7a120aa2042b`
- `scripts/release-requirements.json`: `b58cbe10ad49ed2e909095934c4a0b469eefa0ab`
- `scripts/pr-selected-runtime-matrix.py`: `e1f39d82d4b5a8814997fd79e62a3afb256b8ca9`

The exact-base coverage catalog already maps the app-pull implementation and tests to Docker/Podman data-capabilities gates and `internal/development/source_pull.go` plus its tests to Docker/Podman observability gates. No new ingress PR or catalog change was needed for these paths.

## Hosted CI evidence

GitHub Actions run `45213925226` (`CI · PR #1752`, event `pull_request`) ran against exact head `9e7c74409916ac7118e3f4765a9553a427fb218d`. `PR · Trusted Plan` completed successfully and its log records `BASE_SHA=7b45db92deed6c4dbc4b81f355422a8276e2740e`, `HEAD_SHA=9e7c74409916ac7118e3f4765a9553a427fb218d`, and integration SHA `e97a32d1977302404a36f16437953d6323f50adf`. The planner log selected the conservative fallback (“No narrow mapping: conservative checks selected.”); the selected plan and its executed jobs, not skipped jobs, are the CI evidence.

The terminal aggregate `PR Selected Checks` (check run `137845483307`, integration app `15368`) completed with conclusion `success` at 2026-11-23 16:36:21Z on the exact candidate head. Relevant selected jobs completed successfully:

- `PR · Native gate plan` (`137829814860`), `PR · Trusted Plan` (`137829815199`), `PR · Source format` (`137829815048`), and `Workflow policy` (`137829814854`).
- `PR · Go unit · cli-0` through `cli-3` (`137829991809`, `137829991798`, `137829991908`, `137829991940`); all passed. The CLI shard summaries report 1,861 passed and 64 intentionally skipped from 1,925 discovered across the four shards.
- `PR · Go unit · packages` (`137829991865`) passed all non-CLI Go package tests, including package `internal/development` (7.196s), which contains the source-pull tests.
- `PR · Go unit · owner` (`137829991852`), `PR · Focused Python` (`137829991564`), `PR · Exact Candidate` (`137829991603`), `PR · Runner Interface` (`137829991612`), and `PR · Demo Pin` (`137829991689`) passed.
- Selected runtime gates passed: Docker data-capabilities (`137830910608`), Docker observability (`137830910729`), Podman observability (`137830910496`), and Docker coreless lifecycle (`137840074677`).
- `PR · Validation · go-build`, documentation audit, English and German strict MkDocs, and wizard-registration tests all passed.

Release, draft-source, draft-Go, and unselected native jobs are recorded as skipped by the PR-event selection. They are not treated as passes. The required selected jobs above actually executed, and the terminal aggregate passed for this exact head. The PR does not change CI planner/workflow files, so no newer-base rerun was required for this review.

## Remote and session witnesses

Resolved product remote: `https://github.com/mcpdev80/baseharbor.git`.

Product `git ls-remote` before the final review pass:

```text
dc8626e9c52be07a8ea5b87b468c5991b7540c4f refs/heads/develop
9e7c74409916ac7118e3f4765a9553a427fb218d refs/pull/1752/head
```

Product `git ls-remote` after the review pass:

```text
dc8626e9c52be07a8ea5b87b468c5991b7540c4f refs/heads/develop
9e7c74409916ac7118e3f4765a9553a427fb218d refs/pull/1752/head
```

Planning repository verification was run in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, the actual planning repository. `git remote -v` returned:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Codeman session identity observed from `codeman agent list --json`: session `fecbada9-9fd8-4df4-9305-d49b53a6e7a7`, name `codex-rev-1747`, mode `codex`; displayed model `GPT-6-Luna` (source `screen`). No backend identity was exposed in that record.

## repo-rule compliance

This was a read-only REVIEW of a merged candidate. No product files, branches, PR state, comments, workflows, or gates were changed or triggered. The review used GitHub API file/PR/check data and the verified GitHub remote; it did not cite the quarantined `workers/baseharbor` checkout. Planning evidence is stored only in the actual baseharbor-plan repository. No local tests were run.

## cleanliness

Coordinator-host `docker ps -a` before review, shell PID `302775`: no containers listed.

Coordinator-host `docker ps -a` after review, shell PID `316778`: no containers listed.

No Docker/Podman compose project was started.

Planning repository validation: `python3 scripts/plan.py render` completed; `python3 scripts/plan.py check` completed with 0 errors and 10 pre-existing dependency warnings across unrelated task notes. `git diff --check` passed. The evidence file contains no Markdown checkbox lines.

## Planning publication

The first evidence push was delivered to the verified Planning GitHub remote:

```text
e14a137c536cc3f01599e243368f6c6654fe4c92 refs/heads/main
```

After fetching `origin main`, `git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1752/review-merge.md$'` returned this exact path:

```text
evidence/r28-welle5-2026-11-23/sweep-1752/review-merge.md
```

END codex-rev-1747 DONE
