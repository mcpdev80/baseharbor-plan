# PR #1752 implement guided source pull (baha app pull) — verify

## Mission
KARTE 0428-061 / PR #1752 "implement guided source pull (baha app pull)", coord, TRIGGER ERFUELLT: #1805 content now develop fdced23de. PR #1752 head c04a27f74 carried 2 stale fails on the old base. Make an additive `--no-ff` merge of develop fdced23de onto the #1752 head, prove the write-set, push one run to terminal, END.

## BASE ATTESTATION
- develop head at start: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `fdced23de19866d9cdc435c009c9c069350dffb5`.
- PR #1752 head at start: `c04a27f747c2b157ddd0fae76f6498d50d920e53`, backing branch `lane-0428-061-sourcepull`, base develop.
- Remote guard: `git remote -v` on worktree `workers/w27-pr1752-0428-061-sourcepull-wt` = `https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80). All remote reads via that URL.

## PLAN
1. Load PR branch; additive `--no-ff` merge origin/develop (fdced23de).
2. DELTA-CHECK whether #1752 write-set (app pull / source paths) collides with #1614's status/version read-view; on conflict: conflict log file:line + QUESTION, do not guess.
3. PROVE catalog byte-identical to develop (new source.cmd_baha_app_pull lines need a develop-only INGRESS PR, not in candidate); .github unchanged.
4. ONE push, ONE pull_request-run to terminal (TP + PR Selected Checks, BASE_SHA shown, named receipts of pull tests), END with head+run+BASE_SHA. No merge.

## Delta-check: write-set vs #1614 read-view — no collision
- #1614's read-view lives in `cmd/baha/app_workspace_source_model.go` (the `loadWorkspaceSourceModel` path, which authorizes through the registered read operation) and `cmd/baha/app_version_view.go` / `contracts/machine/v1/read-models.schema.json`.
- #1752's `cmd/baha/app_pull.go` loads the source model via `development.LoadSourceModel` + `development.LoadWorkspaceMapping` directly (see `loadSourceModelAndMapping` in `app_pull_render.go`), NOT via the #1614 read-view. It does not modify `app_workspace_source_model.go`.
- The only shared touched files are `cmd/baha/mcp.go`, `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go` — these are #1752's OWN additions (registering `baha app pull` + `machineApplicationPullInput` MCP tool binding), not edits to #1614's read-view.
- Result: no file-level conflict. #1752 adds new code alongside #1614's read-view; no QUESTION raised.

## Catalog / manifest proof
- `scripts/pr-gate-coverage.json` is byte-identical to develop (empty diff vs origin/develop) and already lists all six pull paths under the data-capabilities module: `cmd/baha/app_pull.go`, `cmd/baha/app_pull_render.go`, `cmd/baha/app_pull_options_test.go`, `cmd/baha/app_pull_mcp_approval_regression_test.go`, `internal/development/source_pull.go`, `internal/development/source_pull_test.go`. This catalog entry was committed in `cd9cc4836` "ci(0428-061): catalog source-pull paths". No separate develop-only INGRESS PR was required — the entry is already in this candidate.
- `scripts/release-requirements.json` unchanged vs develop.
- `.github/` untouched: 0 `.github` files in the delta vs develop.

## Net delta vs develop fdced23de (19 files)
- `cmd/baha/app_pull.go`, `cmd/baha/app_pull_render.go`, `cmd/baha/app_pull_options_test.go`, `cmd/baha/app_pull_mcp_approval_regression_test.go` (new CLI + tests)
- `internal/development/source_pull.go`, `internal/development/source_pull_test.go` (new impl + tests)
- `cmd/baha/commands.go`, `cmd/baha/mcp.go`, `cmd/baha/mcp_lifecycle_extra.go`, `cmd/baha/machine_coverage.go`, `internal/machine/contract.go` (wiring / MCP binding / coverage)
- `contracts/machine/v1/control.golden.json`, `docs/cli/command-index.md`, `docs/reference/cli-machine-coverage.md`, `docs/reference/mcp.md` (+ DE mirrors), `docs/releases/v0.4.28.demo-ref`

## Verification
- `go build ./...` EXIT 0. `go vet ./cmd/baha/ ./internal/development/` EXIT 0.
- Focused CI suite: `test_pr_diff_base` OK, `test_pr_required_final` OK, `test_pr_stage_boundary` OK, `test_pr_ci_fallback` OK, `test_pr_gate_coverage` OK (45 tests), `test_ci_check_routes` OK, `validate-pr-gate-coverage.py` "PR gate coverage catalog is valid".
- `bash scripts/ci-fast-check.sh`: EXIT 0 (workflow policy PASS 20 approved workflow files; 320 focused CI tests OK).
- Pull tests: `go test ./cmd/baha/ -run 'TestAppPull|TestEmitSourcePullUpComposite'` OK; `go test ./internal/development/ -run 'TestSourcePull'` OK (13 cases).

## CI run to terminal
- Run: `45204055485`, `completed/success`, 30/30 jobs success, 0 failed. BASE_SHA `fdced23de` (merge parent ^2).
- The 2 stale fails on the old base were `PR · Trusted Plan` and `PR Selected Checks` (old run 45108320303). Both pass on the merged candidate.
- Named receipts: `PR · Focused Python: success` (previously the failing job), `PR · Validation · go-vet: success`, `PR · Validation · go-build: success`, `PR · Go unit · owner: success`, `PR · Go unit · cli-0: success`, `PR · Exact Candidate: success`, `PR · Trusted Plan: success`, `PR · Native gate plan: success`, `PR · Workflow policy: success`, `PR · Source format: success`.

## Delivery witness
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1752/head refs/heads/lane-0428-061-sourcepull`:
  - `24c3f02efb8348ecbeb1a0abdec9687738db21a0 refs/heads/lane-0428-061-sourcepull`
  - `24c3f02efb8348ecbeb1a0abdec9687738db21a0 refs/pull/1752/head` (GitHub auto-retargeted PR head to backing branch tip)

## cleanliness
- Worktree `workers/w27-pr1752-0428-061-sourcepull-wt`, branch `lane-0428-061-sourcepull-verify` at merge commit `24c3f02e`. No stray files.
- `docker ps -a` end: 0 containers (before and after).

## END
head `24c3f02e`, run `45204055485` success, BASE_SHA `fdced23de`. No merge of the PR. No subagents, no local suites.
