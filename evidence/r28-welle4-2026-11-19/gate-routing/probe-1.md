# Gate Routing Probe — mission-gate-routing-probe

**Mission tag:** gate-routing-probe
**Date:** 2026-11-19
**Type:** read-only investigation. No `.github/**` / product `scripts/**` edit, no merge, no rerun/dispatch, no PR, no card status change, no subagent (§4.8). Isolated clone under `/var/tmp/ghprobe` only.

**Candidate under probe:** PR #1613, card 0428-073, exact head `d8838f622b551cdc8a7f8e8320c3f122b2ae5783`, run `44491028219`
**Contrast candidate:** PR #1691, head `d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e`, run `44487090323`

## Base attestation

- develop HEAD (origin/develop): `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
- PR #1613 head `d8838f6` is a 3-parent merge commit: `Merge remote-tracking branch 'origin/develop' into w073-perses-alerts`
- PR #1691 head `d1fcfdf6` is a single squash commit
- Both heads reachable in clone at `/var/tmp/ghprobe` (authentic remote, `git ls-remote` verified)

## Fact witnesses

- Run `44491028219` (PR #1613): `gh api repos/mcpdev80/baseharbor/actions/runs/44491028219/jobs`
- Run `44487090323` (PR #1691): `gh api repos/mcpdev80/baseharbor/actions/runs/44487090323/jobs`
- PR metadata: `gh api repos/mcpdev80/baseharbor/pulls/1613` -> `draft: true`; `/1691` -> `draft: false`
- Planner run on #1613 diff: `python3 scripts/pr-gate-plan.py` (env GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop)
- Planner run on #1691 diff: same

## Root cause (the answer to the probe)

The Go-unit / build / vet / policy cells are skipped in run 44491028219 for a reason unrelated to the file-content mapper: **PR #1613 is a DRAFT PR.**

Every normal PR cell carries the guard `github.event.pull_request.draft == false`:

- `PR · Source format` — ci.yml line 514
- `PR · Go unit · ${{ matrix.shard }}` — ci.yml line 1137 (also gated `needs.pr_plan.outputs.unit_scope != 'none'`)
- `PR · Validation · ${{ matrix.check }}` (go-build / go-vet / go-unit-tests / identity-provider-package-tests ...) — ci.yml line 1160
- All other `needs: pr_plan` cells (native, runtime, consumer, pins, exact-candidate, exact-full-pre-release, main-release, etc.) — ci.yml lines 956/980/1012/1055/1094/1137/1160/1282/1313/1332/1349/1386

The two cells that DID run carry the opposite guard:

- `PR · Draft source and routing` — ci.yml line 1481
- `PR · Draft Go · ${{ matrix.shard }}` — ci.yml line 1535

Both use `github.event.pull_request.draft == true`. So a draft PR is contractually routed to the Draft cells only; the normal verification cells are `skipped` by workflow policy, and the run reports `SUCCESS` of those narrow Draft cells while the candidate at its exact head is never Go-unit/vet/build/policy verified.

## The file-content mapper does NOT gate on draft (precise file:line)

`scripts/pr-gate-plan.py` is a pure diff-to-gate mapper. It never reads the draft flag:

- `targeted_plan()` (line 763) has no `draft` reference at all.
- `plan()` (line 1667) — no `draft` reference.
- grep for `draft` in the file: only occurrences are in workflow `if:` strings, not in the planner.

Therefore the skip is 100% the `draft == false` workflow guard, not the planner's file-pattern routing.

## Route-table the probe asked for (file pattern -> group, file:line)

Derived from `scripts/pr-gate-plan.py` `targeted_plan()` path dispatcher (lines ~1240-1560):

| Changed path (subset) | `area` | Checks / gates | file:line |
| --- | --- | --- | --- |
| `internal/capability/perses.go` | `capability-implementation-unresolved` | `require(CODE_CHECKS)` only; fail-closed unresolved | pr-gate-plan.py:1513 |
| `internal/metrics/perses_*.go` (`*_test.go` included) | `unresolved` (catch-all) | no check added; fail-closed unresolved | pr-gate-plan.py:1555 |
| `internal/identityprovider/*.go` | `identity-provider-package` | `identity-provider-package-tests` (+ runtime gates if non-test) | pr-gate-plan.py:1440 |
| `cmd/baha/app_observability_acceptance_test.go` | `observability-acceptance` | CODE_CHECKS + `atomic/docker/observability`, `atomic/podman/observability` | pr-gate-plan.py:1292 |
| `cmd/baha/*.go` (non-test) | `cli-unresolved-runtime-impact` | CODE_CHECKS + CLI_CHECKS; unresolved | pr-gate-plan.py:1307 |
| `internal/application/*.go` (non reviewed-path) | `application-implementation-unresolved` | `require(CODE_CHECKS)` only; unresolved | pr-gate-plan.py:1409 |
| unknown | `unresolved` | -- | pr-gate-plan.py:1555 |

`CONSERVATIVE_CHECKS` (go-unit-tests / go-vet / go-build) are only added in the `conservative_fallback` path at pr-gate-plan.py:1733-1751 when coverage is unresolved AND the diff/integration is valid.

## Planner proof (both candidates, real run)

PR #1613 diff (4 files, base origin/develop `da76c5cf`):
```
internal/capability/perses.go
internal/metrics/perses_contract_test.go
internal/metrics/perses_prometheus_alerts.go
internal/metrics/perses_prometheus_alerts_test.go
```
Planner output:
```
coverage_status: resolved
broad_required: False
selected_gates: []
checks: ['go-build', 'go-unit-tests', 'go-vet']
reasons:
  internal/capability/perses.go: capability-implementation-unresolved
  internal/metrics/perses_contract_test.go: unresolved
  internal/metrics/perses_prometheus_alerts.go: unresolved
  internal/metrics/perses_prometheus_alerts_test.go: unresolved
  No declared runtime gate owner for: <all 4 files>
  Unknown narrow coverage selects normal broad unit/vet/build checks; runtime gates require declared coverage.
```
So the planner DOES select `go-unit-tests` -> the `unit_split` step computes `unit_scope='full'` -> the Go-unit `if` (`unit_scope != 'none'`) would be TRUE. The ONLY remaining false in the Go-unit `if` chain is `draft == false`. Confirmed by PR metadata `draft: true`.

PR #1691 diff (18 files, base origin/develop `da76c5cf`):
```
cmd/baha/app_observability_acceptance_test.go  (-> observability-acceptance -> atomic/docker/observability)
internal/identityprovider/keycloak_signal_registration_test.go (-> identity-provider-package -> atomic/docker/identity)
... plus 16 more (logs/observability/metrics/application/cli-unresolved)
```
Planner output:
```
coverage_status: resolved
selected_gates: ['atomic/docker/identity', 'atomic/docker/observability']
checks: ['go-build', 'go-unit-tests', 'go-vet', 'identity-provider-package-tests']
broad_required: False
```
Draft flag: `false` -> all normal cells run (witnessed in run 44487090323: Go unit cli-0/1/2/3/packages/owner, go-build, go-vet, source format all `success`).

## The one line that makes the difference (mission step 3, item d)

Not a single planner line -- the difference is the PR draft flag evaluated at the workflow `if:` guards. Concretely:

- #1613 `draft == true` -> normal cells `if` short-circuit to skipped; Draft cells `if: ... draft == true` run.
- #1691 `draft == false` -> normal cells proceed.

If the mission intended "one planner line", the operative file is `.github/workflows/ci.yml` line 1137 (`PR · Go unit`), the family of guards at ci.yml 514/1160/956/980/1012/1055/1094/1282/1313/1332/1349/1386 (all `draft == false`), and the Draft-cell guards at ci.yml 1481/1535 (`draft == true`). The planner `scripts/pr-gate-plan.py` is draft-agnostic by design and is NOT the cause.

## Consequences for 0428-073 / #1613

- Per the correct fix (mark non-draft OR otherwise route drafts through the normal cells), the cells that MUST run and pass for #1613 are:
  - `PR · Go unit · cli-0..3, packages, owner`
  - `PR · Validation · go-unit-tests`, `go-vet`, `go-build`, `identity-provider-package-tests`
  - `PR · Source format`
  - plus any `needs: pr_plan` runtime/native cell IF the (correctly routed) planner selects runtime gates for `internal/capability/perses.go` -- currently it does NOT (only `capability-implementation-unresolved`, CODE_CHECKS only), so no runtime gate is expected for this file set.
- Under the current draft state the SUCCESS of the Draft Go cells is a false-verification signal; the candidate at `d8838f6` is NOT covered by the Go-unit/vet/build/policy gates.

## Minimal owner recipe (one line, no new cell)

Two mutually exclusive one-line options in `.github/workflows/ci.yml` (Owner scope -- lane reports, does not edit):

Option A -- stop treating drafts as exempt (one-line change to the guards):
- At ci.yml line 1137 (and the sibling guards 514/1160/956/980/1012/1055/1094/1282/1313/1332/1349/1386) change `github.event.pull_request.draft == false` to drop the draft test (or `draft != true`), so draft PRs run the normal cells; keep the Draft cells (1481/1535) for the draft-only fallback.

Option B -- keep drafts exempt but make the run fail-closed when a draft skips required gates:
- Add an `always()` "PR · Draft required-coverage gate" cell that reads `needs.pr_plan.outputs.unit_scope`/`selected_gates` and fails if a non-draft-intent candidate was routed to Draft (one new always() cell, not a rerun).

The lane's recommendation is Option A: the draft flag is a review-state marker, not a coverage-class marker; drafts that touch real source (`cmd/baha/*.go`, `internal/application/*.go`, `internal/capability/perses*.go`, `internal/metrics/perses*.go`, `docs/spec/*.md`) should run the normal unit/vet/build cells.

## Scope compliance

- No edit to any file under `.github/**` or product `scripts/**`; all script reads are read-only analysis and a local planner run.
- No rerun, no workflow_dispatch, no PR, no merge, no card status change.
- Isolated clone only under `/var/tmp/ghprobe`; the shared `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` quarantine checkout was NOT cited.
- No subagent (§4.8).
- Evidence lives only in baseharbor-plan; none in a product repo.

## Host hygiene

- before docker ps -a: (no containers started this mission)
- after docker ps -a:
- before podman ps -a: (no containers started this mission)
- after podman ps -a:
- cleanliness: clean -- no docker/podman container, network, volume or state directory created by this lane; the isolated git clone lives under /var/tmp/ghprobe, outside the ecosystem root.

## Handoff

END_DONE mission-gate-routing-probe.md: documented that PR #1613 (draft) is routed by the workflow `if:` guards to the Draft-only cells, so Go-unit/vet/build/policy are `skipped` (ci.yml 514/1137/1160 + sibling guards, all `draft == false`; Draft cells 1481/1535 are `draft == true`). The planner `scripts/pr-gate-plan.py` is draft-agnostic (no draft reference in `targeted_plan`/`plan`) and is not the cause. Planner proof attached for both #1613 and #1691; the one-line difference is the draft flag. Minimal owner recipe: Option A -- remove the `draft == false` short-circuit on the normal cells (Owner `.github/**` scope) so drafts touching real source run unit/vet/build. No product change made by the lane.
