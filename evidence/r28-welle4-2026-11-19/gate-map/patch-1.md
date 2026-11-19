# Gate-map patch draft (karte 0428-134)

This is a **draft patch** for the Owner. It is NOT applied in any product repo — it stays a reviewable patch in `baseharbor-plan` (Owner scope), and applying it is the Owner's action.

- Mission: `gate-map-patch-draft` (karte 0428-134, Dachkarte 0428-114).
- Fundgrundlage (audit, read-only): `evidence/r28-welle4-2026-11-19/ci-intake-audit/befund-1.md`, audit-commit `74fa2814`.
- Four changes, no fifth, no new gate: go-unit-on-PR, perses smoke cell, demo `branches`, documentation-audit path.
- Delivery: this file (reason per change) AND `gate-map.patch` (git-apply-fähig).
- Every change dry-run verified with `git apply --check` against the target head (witnesses at the foot).
- Base attestation: Planning HEAD `f92a1585bd33808b0a6cb3a0e34ddc1e37e7e922`; baseharbor develop head `907f16713cbf38693d30c9dadaad7fe299759219`; baseharbor-demo main head `adda7599cb5b79689702f6a63a5ca802179df967`.

## CHANGE 1 — go-unit-on-PR (ci.yml:342 + ci.yml:259)

**Hole.** The full Go unit suite `go test ./...` runs only in the `validate` job at `.github/workflows/ci.yml:342`. That job's `if` at `ci.yml:259` is `github.event_name != 'pull_request' && ...`, so it never runs on a Pull Request. On PR, coverage is delegated to `pr_plan` selection: `pr_unit_shards` only runs when `needs.pr_plan.outputs.unit_scope != 'none'` (`ci.yml:1137`), and scope is `'full'` only when `go-unit-tests` is in the trusted `requested` set (`ci.yml:931`) or the sharding executor paths changed. Otherwise scope falls back to `cli` or `none`. `pr_focused` (`ci.yml:1091`) runs a fixed Python suite, not Go. So most changed files route to a narrow check and the affected package's Go tests never run on that PR.

**Proposal.** Route the window-package Go unit tests onto PR by reusing the existing `go-unit-tests` VALIDATION case mechanism. The existing `validate` job already selects a `$VALIDATION` string (ci.yml:1180-1200) that drives which `run` block executes; the `go-unit-tests` case runs `bash scripts/pr-unit-database.sh` at ci.yml:1197. The patch routes the window package paths (`internal/metrics`, `internal/observability`, `internal/logs`, `internal/capability`, `internal/application`, `cmd/baha`) to a Go unit run on PR through that existing selection path, without inventing a new job or a new gate. No new workflow cell, no new CI check id.

**Scope note.** This edits `.github/workflows/ci.yml` (Owner scope, line 259 and the validation-case selection at ci.yml:1180-1200). Report only, not applied.

## CHANGE 2 — perses-smoke cell (TestPersesRuntimeSmokeDockerIsolated)

**Hole.** `TestPersesRuntimeSmokeDockerIsolated` lives only on the perses candidate branch (`internal/application/perses_runtime_test.go`, lane `lane-0428-088-perses-runtime`, head `54fbe47711cd649dac3a55d62c4de532d738299d`) — absent from develop HEAD `internal/` (search returns 0). It is `if os.Getenv("BASEHARBOR_PERSES_RUNTIME_SMOKE") != "1" { t.Skip(...) }` (perses_runtime_test.go:372). No workflow references `BASEHARBOR_PERSES_RUNTIME_SMOKE` (grep `.github/` → 0) and no workflow references `perses` at all. So the smoke test has no CI trigger.

**Proposal.** Add a focused Docker runtime job that runs `BASEHARBOR_PERSES_RUNTIME_SMOKE=1 go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$'` on PR. Choice of cell: `targeted-integration.yml`, NOT `docker-runtime-acceptance.yml`.

Reason for `targeted-integration.yml`:
- It already hosts the focused `workflow_dispatch` gate job (`on.workflow_dispatch` at targeted-integration.yml:30) that builds the BaseHarbor control-plane image with the existing Dockerfile and runs `go test ./cmd/baha -run '^Test...'` under an isolated rootless Docker engine (`bash scripts/ci-core-rootless-runtime.sh`). That is exactly the runtime-docker path and the `go test -run` pattern the perses smoke test expects (it calls `runtimeprovider.Resolve`, `runtime.ConfigProject`, `runtime.UpProject`).
- `docker-runtime-acceptance.yml` is the other runtime-docker path but its jobs are gated to `workflow_dispatch` with a `gate` input keyed to specific named gates; there is no free `go test -run` slot without adding a new input/gate, i.e. a new gate. The focused `workflow_dispatch` job in `targeted-integration.yml` already takes a generic `gate`/`ref` input and a `go test -run` body, so the perses smoke fits that existing body without a new gate.

**Scope note.** This edits `.github/workflows/targeted-integration.yml` (Owner scope). Report only, not applied.

## CHANGE 3 — demo pr-guided-consent branches (baseharbor-demo)

**Hole.** `baseharbor-demo/.github/workflows/pr-guided-consent.yml:4-5` declares `on.pull_request.branches: [main]`. A develop integration PR (base `develop`) never matches, so the guided-consent python regressions never fire on the normal develop PR.

**Proposal.** Change `branches: [main]` to `branches: [main, develop]` at `baseharbor-demo/.github/workflows/pr-guided-consent.yml:5`. One-line change, no new workflow, no new trigger.

## CHANGE 4 — documentation-audit path for docs/internal/*.json (ci.yml:1186 + scripts/pr-gate-plan.py:1189-1192)

**Hole.** `ci.yml:1186` runs `bash scripts/documentation-audit.sh` unconditionally when `VALIDATION == documentation-audit`. But `scripts/pr-gate-plan.py:1189-1192` only emits `DOC_CHECKS` for `docs/*.md`, `docs/*.rst`, the mkdocs/root doc files (`README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `mkdocs.yml`, `mkdocs.de.yml`) and `site/`. `docs/internal/*.json` matches none, so a PR that changes only such a file routes to no `documentation-audit` selection → the audit job does not run. This blocks 0428-131 / #1697.

**Proposal.** Extend the `documentation` area path selection in `scripts/pr-gate-plan.py` so `docs/internal/*.json` also emits `DOC_CHECKS`. Concrete edit: in the `elif` at `scripts/pr-gate-plan.py:1189`, change the `path.startswith('docs/')` clause from `.endswith(('.md', '.rst'))` to include the `docs/internal/*.json` shape, e.g. `path.startswith('docs/internal/') or path.endswith(('.md', '.rst'))`. Reuse the existing `documentation-audit` validation case; no new gate.

**Scope note.** This edits `scripts/pr-gate-plan.py` (Owner scope) and touches the CI selection path. Report only, not applied.

## repo-rule compliance

- Read-only audit artifact. No commit, push, merge, PR, workflow_dispatch, or new test in any product repo.
- No edit to `.github/**`, `scripts/**` (product), or product code — all four findings are file:line patch text only.
- Isolated clones under `/var/tmp/gatemap-wt/` (outside the shared copy). No containers/compose started.
- No subagent (§4.8). Every step run in this session.

## cleanliness

- before: no containers, no compose projects, no /var/tmp state besides existing clones; no running services.
- after: /var/tmp/gatemap-wt/{baseharbor (git clone, origin/develop), demo (git clone, origin/main)} — read-only clones only. No containers, no compose, no running services.
- docker/podman ps witness: (none started)

## dry-run witnesses (git apply --check)

1. `git -C /var/tmp/gatemap-wt/baseharbor apply --check --verbose < patch` against `907f16713cbf38693d30c9dadaad7fe299759219` (ci.yml / pr-gate-plan.py) — witness below.
2. `git -C /var/tmp/gatemap-wt/demo apply --check --verbose < patch` against `adda7599cb5b79689702f6a63a5ca802179df967` (demo pr-guided-consent.yml) — witness below.

(Exact command output pasted in gate-map.patch header witness block.)

## END

END_DONE mission-ci-intake-audit... (see handoff line). Mission `gate-map-patch-draft` (karte 0428-134): draft patch written, four changes, every change dry-run `git apply --check`-verified against the target head; no product write, no workflow/scripts edit, no PR, no merge, no subagent. Evidence on origin/main.
