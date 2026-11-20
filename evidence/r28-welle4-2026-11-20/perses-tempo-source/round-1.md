# t-20261114-r28-perses-tempo-source (0428-091) — Round 1

Owner: `w091-pr0428-091-tempo-source` · Card `0428-091` · Task `t-20261114-r28-perses-tempo-source`

## Remote witnesses

- `git remote -v` on the shared baseharbor checkout (FIRST git action, §4.6):

  ```
  lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch)
  lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
  origin	https://github.com/mcpdev80/baseharbor.git (fetch)
  origin	https://github.com/mcpdev80/baseharbor.git (push)
  upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
  upstream	https://github.com/mcpdev80/baseharbor.git (push)
  ```

  All three remotes resolve to `github.com/mcpdev80`; used `lane-origin` (github URL) only.

- `git ls-remote lane-origin refs/heads/develop` → `36d075fad77fa61ac8c153e979855546589b32c2`
- `git ls-remote lane-origin refs/pull/1645/head` → `c781eb86fc996493bf5e0ee807913e81a51c3ab4`
- GitHub API PR #1645: state `open`, `draft: true`, base `develop`, head `c781eb86`
- GitHub API PR #1610: state `closed` (draft), head `d57ab527` was overwritten, cannot restore
- baseharbor-plan `git remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git`; HEAD `299e8daedf29d79553c5b111078df7cd1bd13986` (main)

## Core finding (recorded before scope decision)

- **#1645** is the sole live carrier of BOTH the accepted #075 Perses seam AND #091's Tempo datasource work.
- **#091's tempo commit chain** (`perses_tempo_contract.go`, `perses_tempo_datasource.go`, `perses_tempo_upstream.go`, `perses_tempo_errors.go`, `perses_tempo_witness_test.go`, `perses_tempo_fixture_test.go`, `perses_tempo_datasource_test.go`, `perses_contract_test.go`, `cmd/baha/app_perses_cli_test.go`, `internal/capability/perses.go`, `internal/capability/perses_test.go`, testdata `perses-pin.json`/`tempo-datasource.json`/`tempo-trace-query.json`) is COMPLETE.
- **All three luna-r1 REQUEST_CHANGES recipes are addressed** in head `c781eb86`:
  1. Health fails closed — `VerifyPersesTempoDatasourceHealth` requires a real TraceQL query and returns `TempoHealthUnverifiedError` on an empty answer (never pin-only pass).
  2. Builder enforces selection/authorization/source — `buildPersesTempoDatasourceWithProbe` returns `TempoSurfaceNotSelectedError`/`TempoNotSelectedError`/`TempoAuthorizationError` before building; no empty-config default datasource.
  3. Native plugin + real trace query verified against the pinned upstream witness model with tamper/drift fail-closed tests.
- **Exact-head CI run `43874313785`** (PR #1645, branch `w091-tempo-r5-fix`, head `c781eb86`): 21 SUCCESS / 0 failure / 9 skipped — required jobs (`PR · Go unit · {cli-0..3,packages,owner}`, `PR · Validation · {go-build,go-vet,cli-gofmt,mkdocs-en-strict,documentation-audit,openbao-package-tests,authority-package-tests}`) actually executed and passed.
- **The blocker**: #1645 is a **draft**. Every required/gated job (`Go unit`, `Validation`, `Native`, `Release`, `PR Selected Checks`) is **SKIPPED** while the PR is draft. Only Draft-scoped jobs ran. An actually-executed required-job run — the acceptance standard (§5.2) — has never happened on a non-draft head for this PR.

## Scope decision (Owner scope — NOT mine to execute)

- The path to acceptance is: un-draft #1645 + hop to current develop `36d075f` + exact-run CI. Per the mission and CI policy, **un-drafting, hopf, and rerun are Owner-scope actions** — forbidden to me (no merge, no PR-state mutation, no `.github/**`, no reruns/workflow_dispatch, no force-push).
- **#083 write-set conflict**: #091's chain is layered on the #075 seam which touches `internal/application/manifest_parse.go`, `manifest_parse_services.go`, `manifest.go`, `manifest_render.go`, `manifest_validation.go`, `management_ui.go`, `cmd/baha/app_status_result.go` — exactly the conflict/blocked files. Rebasing `c781eb86` onto current develop `36d075f` would collide with #083's ongoing work on those files. This collision must be resolved by the owner/#083 lane, not silently.
- **STOP criteria from the mission are all met** (contract-seam allows Tempo as datasource-type = NOT a stop; a pinned Perses plugin IS verifiable = NOT a stop; no .github/scripts change is needed = NOT a stop). The remaining blocker is the draft-state governance, not a technical defect.

## Local verification I could perform myself (exact head `c781eb86`, clean clone)

- `go build ./internal/metrics/` → EXIT 0
- `go test ./internal/metrics/` → `ok ... 0.409s`
- `go test ./internal/metrics/ -run Tempo` → EXIT 0
- `go vet ./internal/metrics/` → EXIT 0
- `gofmt -l internal/metrics/` → clean
- Ancestry: current develop `36d075fa` is NOT an ancestor of head `c781eb86`; merge-base `14d8f17d` — develop has advanced 30+ commits past the PR's base. This is why a hop is required.

## repo-rule compliance

- Evidence only: read-only API witnesses, a clean read-only clone, and local `go build/vet/test`. No product file written. No PR-state mutation. No merge. No `.github/**`. No subagents (§4.8). Evidence published only on baseharbor-plan `origin/main`.

## END status

BLOCKED
