# CI intake audit — Befund 1 (read-only)

Mission `ci-intake-audit` (Owner, 2026-11-19): find tests in the observability/metrics/logs/enrollment/perses/targets window that no CI job reaches (§5.3 CI intake duty), so the Owner can fill the gate-map once. Read-only; no product edit, no workflow/scripts edit, no PR, no merge, no subagent.

## Base attestation

- Planning HEAD (authoritative): `27b429e7a6143cbf4e596377545290c0523b1da3` kanban: t-20261119-coord-r28-ci-intake-audit -> active
- baseharbor remote develop (ls-remote, never the quarantined checkout): `da76c5cf9c963207038d5599bd130b89ecb1e8a4` feat(cli,docs): print Warning marker in every acknowledging stage; align EN docs with i18n rename (0428-126) (#1696)
- baseharbor remote main (ls-remote): `c000c5db2560c471fe84842136e03d6e54d96779` fix(release): accept exact develop source after squash merge (#1675)
- baseharbor-demo remote main (ls-remote): `adda7599cb5b79689702f6a63a5ca802179df967` tests(guided): track the core Warning-marker rule in every acknowledging stage (0428-129) (#165)
- Isolated clones under /var/tmp/ci-intake-audit-clones/ (outside the shared copy). baseharbor cloned `main` by default (fork default); develop fetched separately to the real remote head.

## Method (and why the counter-check rules out false positives)

1. Window test list: `git grep -l "^func Test" HEAD -- internal cmd`, narrowed to the window themes (observability/metrics/logs/enrollment/perses/targets) → 94 test files, ~600 Test funcs.
2. For each test, decide whether a workflow OR the gate-map (scripts/pr-gate-coverage.json, .github/workflows/*.yml) reaches it, with file:line proof.
3. Counter-check against a known GOOD-mapped test to show the method does not emit false positives.

## CI execution model (findings 1–3 rest on this)

The product repo is a fork whose `develop` is the integration ref. The unit suite is NOT covered uniformly on PR:

- ci.yml `validate` job (line 342): `run: go test ./...` runs the full Go unit suite, but `if` excludes pull_request (line 259). It runs on non-PR pushes only.
- On PR, coverage is delegated to `pr_plan` (line 709) + `pr_unit_shards`/`pr_validations`/`pr_focused`, all gated by `needs.pr_plan` selection. `pr_unit_shards` only runs when `needs.pr_plan.outputs.unit_scope != 'none'` (ci.yml:1137); scope is `'full'` only when `go-unit-tests` is in the trusted `requested` set (ci.yml:931) or the sharding executor paths changed. Otherwise scope falls back to `cli` or `none`.
- `pr_focused` (line 1091) runs a fixed Python regression suite; Go unit is NOT there unless routed.
- Therefore a Go test reaches CI on PR only if the changed file routes to a check that runs `go test <pkg>` (e.g. the `source-contracts` route, capability/log/observability routes, the CLI-package route, runtime-provider route, or `go-unit-tests`). A changed file that routes nowhere leaves its package's tests uncovered on PR.

## The four holes

| test / job | file:line | affected card/PR | gate candidate | begründung |
|---|---|---|---|---|
| Go unit package tests (window: internal/metrics, internal/observability, internal/logs, internal/capability, internal/application, cmd/baha) | .github/workflows/ci.yml:342 (`run: go test ./...`) + ci.yml:259 (`if: github.event_name != 'pull_request' && …`) | all window cards (e.g. 0428-126 perses, 0428-131 docs) | `validate` job; NOT on PR | `go test ./...` is the only runner of the full Go unit suite and its job `if` excludes pull_request. On PR the coverage is delegated to pr_plan selection; the default `pr_unit_shards` runs only when `needs.pr_plan.outputs.unit_scope != 'none'` (ci.yml:1137), and scope is `'full'` only when `go-unit-tests` is in the trusted `requested` set (ci.yml:931). Most changed files route to a narrow check, so the affected package's tests never run on that PR. No workflow or gate-map (scripts/pr-gate-coverage.json) lists individual Go test names or runs `go test ./...` on PR. |
| TestPersesRuntimeSmokeDockerIsolated | mission-known case; NOT present in HEAD `internal/` (search `git grep PersesRuntimeSmoke HEAD` → 0 hits) | perses window (0428-126) | none (no trigger) | The named smoke test is not in current develop HEAD `internal/`. It is a card-scoped known case (env `BASEHARBOR_PERSES_RUNTIME_SMOKE`). No workflow references `BASEHARBOR_PERSES_RUNTIME_SMOKE` (grep `.github/` → 0) and none references `perses` at all. The `internal/metrics` package (perses_contract_test.go, perses_dashboards_valkey_test.go) IS reached on PR only via the source-contracts/capability routes. The smoke test as named has no CI trigger. |
| baseharbor-demo .github/workflows/pr-guided-consent.yml:5 | .github/workflows/pr-guided-consent.yml:4-5 (`pull_request:` → `branches: [main]`) | demo guided-consent regressions (0428-129) | none on PR to develop | The only PR trigger for guided-consent regressions is `pull_request.branches: [main]` (line 5). It never fires on a PR whose base is `develop` (the integration base). The second demo workflow (v0424-targeted.yml:3-4) fires only on `push` to `work/v0.4.2{4,5,6}-ecosystem-release` branches. So guided-consent python regressions are unreachable on the normal develop integration PR. |
| documentation-audit (docs/internal/*.json) | .github/workflows/ci.yml:1186 (`documentation-audit) bash scripts/documentation-audit.sh ;;`) + scripts/pr-gate-plan.py:1189-1192 (`path.startswith('docs/') and path.endswith(('.md', '.rst')) … require(DOC_CHECKS)`) | 0428-131 / #1697 (PR comment 7002848508, head 3448f73e6, run 44478483899 SUCCESS without audit job) | existing `documentation-audit` (ci.yml:1186), no new gate | The `documentation-audit` VALIDATION case runs unconditionally (ci.yml:1186) but `pr-gate-plan.py` only emits `DOC_CHECKS` for `docs/*.md`, `docs/*.rst`, the mkdocs/root doc files (line 1189-1192). `docs/internal/*.json` matches none of these patterns, so a PR that changes only such a file routes to no `documentation-audit` selection → the audit job does not run. Confirmed by the live run: #1697 head 3448f73e6 ran SUCCESS (run 44478483899) with no documentation-audit job despite changed docs/internal/*.json. |

## Counter-check (method falsifies false positives)

GOOD-mapped reference test: `TestObservabilityFullStackAcceptanceInCI`. `observability-acceptance.yml:78` and `:186` run it explicitly (`go test -p 1 ./cmd/baha -run '^TestObservabilityFullStackAcceptanceInCI$' -count=1 -v`) on BOTH docker and podman blocks. Same method that flags the four holes above (search file:line for the exact test/group, then confirm a workflow or gate-map actually runs it) finds a real, present mapping here — so the method does not emit false positives; the four holes above genuinely lack such a mapping.

## Scope / boundaries honored

- No edit to .github/**, scripts/** or product code. All four findings are file:line statements for the Owner.
- No new test, no PR in the product, no merge, no workflow rerun / workflow_dispatch, no subagent (§4.8).
- Isolated clones under /var/tmp/ci-intake-audit-clones/ (never the shared copy). No containers/compose started. Host besenrein — see cleanliness line below.

## cleanliness

before: no containers, no compose projects, no /var/tmp state besides /var/tmp/ci-intake-audit-clones/
after: /var/tmp/ci-intake-audit-clones/ (git clones only); no containers, no compose, no running services
docker/podman ps: (empty witness — none started)
