# envgrand-trigger round 1 — PR #1620 and #1627 empty rollups

**Role:** WORKER · 2026-11-16 · diagnosis + qualifying-trigger attempt. No product files, no PR metadata, no CI state changed. No `.github/**` edit. No merge, no force-push, no retarget, no `ready_for_review`. No subagent (§4.8): every step executed in this session.

**Base attestation:** planning repo `origin/main` = `2834189213cbab6f23c6462e2e02354aff36326b` (short `28341892`), witnessed via `git ls-remote origin main` from `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. Evidence committed on that branch.

**Exact heads (reality witnesses, `git ls-remote origin` from fresh clone):**
- PR #1620 branch `w067-cli2-wizard-platform` @ `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d` (matches mission name)
- PR #1627 branch `cli2-env-delete` @ `49e164ccbd6552a98854ceceaabfafa748775ed1` (matches mission name)

Both PRs: `state=OPEN, isDraft=true, mergedAt=never`. Base of both = `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3` (a CLI-env-policy merge commit `origin/lane-0428-env-registry` rebase base); not a foreign-candidate cut, branches are the mission-named candidates, not branches I authored.

## PLAN

1. Fresh clone in own zone (`/home/.../workers/.models/laptop/envgrand-clone.git`); `rev-parse` named heads as first action.
2. Confirm empty `statusCheckRollup` and zero CI runs at exact heads for both PRs.
3. `.go-root-check` (batch9 #1610 recipe): any embedded `.go` under `testdata/` in the PR diff?
4. Diagnose trigger matrix across all workflows.
5. NOT-log structural finding with file:line; no further pitchen, no `.github/**` edit.
6. Commit akte to planning `origin/main`; verify presence via `ls-remote` before END.

## Findings

### 1. Empty rollup is real and structural, not a missing qualifying run

- `gh run list --repo ... --head_sha <exact>` returns **0 runs** for both `e7eeeb580...` and `49e164ccb...`.
- `gh api .../commits/<exact>/check-runs` returns `total_count=0` for both exact heads.
- `gh pr view <n> --json statusCheckRollup` returns `[]` for both.
- Neither PR diff contains any `.go` file under `testdata/`, so the batch9 #1610 recipe (rename embedded witness `.go` to non-package suffix) does **not** apply:
  - #1620 diff: `cmd/baha/app_access.go` (+53), `cmd/baha/app_access_test.go` (+103).
  - #1627 diff: `cmd/baha/commands.go`, `cmd/baha/env_destroy.go` (+323), `cmd/baha/env_destroy_integration_test.go` (+172), `cmd/baha/machine_coverage.go`, `docs/cli/command-index.md`, `docs/de/cli/command-index.md`, `docs/reference/cli-machine-coverage.md`, `internal/deployment/environment_destroy_scope.go` (+324), `internal/deployment/environment_destroy_scope_test.go` (+280). No `testdata/` path, no Go package-selection failure possible.

### 2. Root cause — no `pull_request` trigger matches the feature branches

Every workflow in `mcpdev80/baseharbor` and its `pull_request` branch filters:

| Workflow file | `pull_request` branches |
| --- | --- |
| `.github/workflows/ci.yml` (the CI · Source & Quality gate) | `develop`, `main` only |
| `.github/workflows/host-trust-owned-e2e.yml` | `release/v0.4.24` only (plus `paths:` filter) |
| `.github/workflows/docker-runtime-acceptance.yml` | `workflow_call` / `workflow_dispatch` only (no `pull_request`) |
| `.github/workflows/mcp-lifecycle-acceptance.yml` | `workflow_call` / `workflow_dispatch` only (no `pull_request`) |
| `.github/workflows/nextjs-greenfield-e2e.yml` | `workflow_dispatch` only |

`ci.yml` trigger surface (absolute lines, witnessed in cloned file):

- `ci.yml:7` `push:` → `develop` and `runtime-validation/**` only.
- `ci.yml:13` `pull_request:` → `ci.yml:15` `develop`, `ci.yml:16` `main`.

Neither `w067-cli2-wizard-platform` nor `cli2-env-delete` is in any `pull_request` branch filter, and neither is a `push` target branch. GitHub therefore emits no `pull_request` event for either PR head → zero check-runs → empty rollups. The heals landed (branch HEADs are the mission-named SHAs) but the `pull_request` event never fires for feature branches.

### 3. NOT-log / structural finding (per mission, no further pitchen)

`event=pull_request` never fires for these PRs because the feature branch is absent from every workflow's `pull_request.branches` allow-list. The qualifying CI gate lives at `.github/workflows/ci.yml`, trigger `pull_request:branches:[develop, main]` (`ci.yml:13-16`). The fix is an **owner action**: add the feature branches (or the intended lane prefix) to `ci.yml`'s `pull_request.branches` — this is a `.github/**` change and is Owner scope. Reporting the exact needed change here; not editing it. No `.github/**` workflow fires `pull_request` on arbitrary feature branches by design, so an empty trigger-commit would not produce a qualifying run and is intentionally not attempted.

## Evidence / witnesses

- Fresh clone (bare) at `/home/marcel/dev/baseharbor-ecosystem/workers/.models/laptop/envgrand-clone.git`; `git ls-remote origin` output:
  - `49e164ccbd6552a98854ceceaabfafa748775ed1 refs/heads/cli2-env-delete`
  - `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d refs/heads/w067-cli2-wizard-platform`
- `gh api .../actions/runs?head_sha=<exact>` → 0 runs each.
- `gh api .../commits/<exact>/check-runs` → `total_count=0` each.
- CI trigger file: `.github/workflows/ci.yml` (lines 7, 13-16); host-trust: lines 3-5.

## END

DONE — diagnosis complete; structural finding (missing `pull_request` trigger for feature branches) logged with `ci.yml:13-16`; owner fix (add branch to `pull_request.branches`) reported, not edited. No product or PR state changed.
