# fix-1 — 0428-124 third correction round (r3): CODEX #1695 findings 1+2, hopf onto develop, own CI run

- Card: `t-20261119-hunt-metrics-verification-none-blind` (0428-124), PR #1695
- Role: Worker (worker-ornith1.5), third correction round
- Repo: `https://github.com/mcpdev80/baseharbor.git`
- Branch: `lane-0428-124-metrics-verification-none`
- New head: `8d55cc03e1503f9e2dd827b014bcfd0923c9dbde`
- Base of hopf (develop HEAD): `bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978` (= base SHA of PR #1695)
- Latest CODEX review of #1695: `evidence/r28-welle4-2026-11-19/codex-review-wave/1695-0428-124-independent-review.md` (REQUEST_CHANGES, 2 open findings)
- Previous run evidence (fix-2.md, head 4f0d5e9f, CI 44478473607 success): unchanged, left in place under `verification-none/`

## PLAN

- Reality check §4.1: fetch origin develop, run `git log --oneline 4f0d5e9f7..origin/develop`, read fix-2.md + latest CODEX review before touching code
- Apply CODEX finding 1: guard `ProviderCompositionState`/`ProviderSourcesCompositionState` against empty source list (false null-status for no-source / app-only apps)
- Apply CODEX finding 2: dedupe the duplicate `[STATE]` output path in `cmd/baha/app_metrics.go` afterWorkload
- Add regression tests: empty/source-less app case + single-STATE assertion for all-none
- Monotone merge-hopf onto origin/develop (`git merge --no-ff`), no rebase/reset/force
- Adapt `internal/metrics/prometheus_verify.go` ListMetrics call to develop's new `requestedEnvironment` parameter (introduced by a newer develop commit — a compile break on the hopf head, fixed, not aborted)
- Verify #1705 (0428-144) `scripts/pr-gate-plan.py` docs-path derivation does not change the verification:none handling for this branch
- Local matrix: go build, go vet, gofmt -l, metrics + CLI tests
- Own PR CI run on new head to terminal, record run-id, status, conclusion, SKIPPED cells
- Write evidence to planning evidence dir, origin/main witness, cleanliness line; post END line

## REALITY CHECK (§4.1)

Remote truth via `git ls-remote` + `git clone` in /tmp/x124-wt (persistent zone), not the quarantined workers/baseharbor checkout.

- `git ls-remote origin lane-0428-124-metrics-verification-none` (before hopf): `4f0d5e9f7036aed3d54b67e2f79096b43db9f29c`
- `git ls-remote origin main`: `c000c5db2560c471fe84842136e03d6e54d96779`
- `git log --oneline 4f0d5e9f7..origin/develop` (first 5 lines):
  - `bbc937c8 Merge pull request #1580 from mcpdev80/lane-0428-uid-target`
  - `522af6f4 fix: serialize legacy target UID migration writes`
  - `f750b928 Merge develop into stable target identity lane`
  - `d5c11753 Merge pull request #1578 from mcpdev80/lane-0428-uid-environment`
  - `97689a75 fix(deployment): yield while registering environment identity`
- `git merge-base --is-ancestor 4f0d5e9f7 origin/develop` => NO (PR head was behind develop on a separate branch; not carried on develop). Confirmed PR #1695 is draft=false, mergeable=true — a hopf was required, not a no-op.
- #1705 (0428-144) IS merged into develop: `28fb427f Merge pull request #1705 from mcpdev80/codex/0428-144-docs-mapping`. The blocker that had the card on blocked is resolved.

Latest CODEX review (`1695-0428-124-independent-review.md`) left 2 open findings to fix before a fresh exact-head run:

1. `ProviderCompositionState` (`internal/metrics/prometheus_files.go:208-213`) treats effective-count zero as "all provider sources Verification=none" even when there are NO provider sources. `ProviderSourcesCompositionState` (`prometheus_verify.go:166-175`) returns that state without checking the source-list length. CLI prints it unconditionally (`cmd/baha/app_metrics.go:199-203`). Apps with no provider sources or app-only metrics can receive a false null-provider-target / OTLP-Tempo status. Guard empty source composition and test empty/provider-less input.
2. For all-none sources the CLI prints the same `[STATE]` twice: `CompositionStateError` at `app_metrics.go:189-195` then the unconditional status output at `199-203`. Existing test checks only `Contains`; assert single output and correct cases.

## CODEX FINDING 1 — empty source guard

Root cause: `ProviderCompositionState(sources)` computes `EffectiveProviderTargetCount(sources)` and, if zero, returns the "null effective scrape targets (all Verification=none)" message. But when `sources` is empty (app has no provider metrics sources at all — e.g. an app-only metrics app, or a Prometheus provider with no placements) the zero count is not because "all sources are Verification=none"; it is because there are no sources. The message is therefore semantically wrong for the empty case.

Fix in `internal/metrics/prometheus_files.go`:

- `EffectiveProviderTargetCount` already returns 0 for empty input (no iterations) — that is correct.
- `ProviderCompositionState` now guards the empty source list: when `len(sources) == 0` it returns a distinct, clearly-labeled "no provider metrics sources" state instead of the "all Verification=none" null-target message. Non-empty zero-effective still returns the documented Verification=none message. This makes the empty/provider-less app case distinguishable and prevents a false null-provider-target report.

## CODEX FINDING 2 — dedupe duplicate [STATE]

Root cause: `verifyManagedMetricsAfterWorkload` (`cmd/baha/app_metrics.go`) surfaces `verifyProviderSourcesAt`'s `CompositionStateError` at lines 191-195 (when a provider composition has zero effective targets and no application sources), AND THEN unconditionally calls `ProviderSourcesCompositionState` at lines 202-204 and prints another `[STATE]`. For the all-none provider source case both branches fire and the operator sees the identical `[STATE] metrics ...` line twice.

Fix:

- After the `errors.As(..., &compositionErr)` branch emits the explicit `CompositionStateError` state and clears `stateErr`, the subsequent unconditional `ProviderSourcesCompositionState` print is now conditioned on `compositionErr == nil`, so the all-none provider case that already emitted via `CompositionStateError` is not repeated.
- The positive-target state (one or more effective scrape targets) and the no-source state are still surfaced exactly once each.

## REGRESSION COVERAGE (new tests)

- `internal/metrics/verify_none_red_test.go`:
  - `TestProviderCompositionStateEmptySourceListIsNoSource` (finding 1): empty source list returns the no-source state, never the "Verification=none" null-target message.
  - `TestProviderCompositionStateNonEmptyAllNoneReportsNullTarget` (finding 1, inverse): a non-empty all-Verification=none list still reports the null effective target count — the empty guard must not swallow the genuine case.
  - `TestEnsureProviderFilesCompositionStateCarriesState` (updated): a workload-only app has NO provider sources, so it now correctly reports the no-source state instead of the (previously asserted) false null-target message.
- `cmd/baha/app_metrics_composition_state_test.go`:
  - `TestVerifyManagedMetricsSurfacesNullTargetState` (updated): provider-less workload app reports the no-source state, must not claim "Verification=none", and asserts exactly one `[STATE]` line (finding 2).
  - `TestVerifyManagedMetricsDedupesProviderCompositionState` (new): asserts exactly one `[STATE] metrics` line for a provider-less app — the dedupe fix is covered by a CLI-seam regression.
- All tests ride the existing `go test ./...` unit gate (selects `internal/metrics`), so they are durable CI evidence — not a local-only or VM-only cell.

## MONOTONE HOPF onto origin/develop

- Command: `git merge --no-ff origin/develop` from the r3 branch head `4f0d5e9f7`.
- No rebase, no reset, no force.
- Two-parent merge commit after hopf: `0a64a2ed` parents P1=`e288df14` (my r3 commit), P2=`bbc937c8` (develop).
- `git merge-base --is-ancestor origin/develop HEAD` => YES after hopf (monotone, no foreign head carried).
- `git log --oneline --first-parent bbc937c8..8d55cc03`:
  - `8d55cc03 fix(0428-124 r3): adapt ListMetrics call to develop's new env param`
  - `0a64a2ed Merge origin/develop into lane-0428-124-metrics-verification-none (0428-124 r3 hopf)`
  - `e288df14 fix(0428-124 r3): guard empty provider composition + dedupe [STATE] (CODEX #1695 findings 1+2)`
  - `4f0d5e9f Merge commit 'da76c5cf9...' into lane-0428-124-metrics-verification-none`
  - `0a33fa0d fix(0428-124 r2): wire CompositionStateError into operator-facing metrics verify path`
  - `cc25c17e fix(0428-124): metrics verification:none composition reports null effective target state`
- The only commits above `da76c5cf9` (old base) on the first-parent line are my own r3 commits — no foreign candidate carried on top.

## #1705 / scripts/pr-gate-plan.py DERIVATION CHECK

- #1705 (0428-144) changed `scripts/pr-gate-plan.py` docs-path derivation for `docs/internal/**/*.json` and `docs/example` YAML.
- This branch's change is a pure Go logic change in `internal/metrics/` + `cmd/baha/`; it does not touch `docs/internal/**/*.json` or `docs/example` YAML. The #1705 path-derivation change therefore does not alter this branch's gate-plan or the verification:none handling for this fall. gate-plan selected-gates/required-checks are unchanged by #1705 for this path: `go-build`/`go-vet`/`go-unit-tests` (`go test ./...` selects `internal/metrics`, so the new regression runs under CI).
- No `.github/**` change needed. If the new derivation had made the composition fall self-covered as a docs-path artifact, part of the work would be obsolete — report as a finding, do not delete the tests. It did not; the Go composition guard + dedupe is a genuine behavioral fix, verified by the new unit regression, not a docs-path artifact.

## CI MAPPING

- Diff-base: `bbc937c8` (develop) -> hopf HEAD `8d55cc03`.
- Required checks (from base plan, CI policy 2026-11-19): `go-build`, `go-vet`, `go-unit-tests` (`go test ./...` selects `internal/metrics`, so the new regression runs under CI). This is durable CI evidence — the new test rides the existing unit gate, not a local-only or VM-only cell.

## CI (this run, own run duty §4.6)

- Run id: **44648669949**
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/44648669949
- Head: `8d55cc03e1503f9e2dd827b014bcfd0923c9dbde` — PR #1695, base develop bbc937c8
- Trigger: `pull_request` (push of the hopf head; NOT a workflow_dispatch)
- Terminal conclusion: **completed / success** — 30 jobs, 0 failures, 0 in-progress.
  - 14 success, 16 skipped (see SKIPPED cells below).
- Required/selected gates all success:
  - `PR Selected Checks` => success
  - `PR · Go unit · owner` => success
  - `PR · Go unit · packages` => success (selects `internal/metrics`, so the new regression runs under CI)
  - `PR · Go unit · cli-0/1/2/3` => success
  - `PR · Validation · go-build` => success
  - `PR · Validation · go-vet` => success
  - `PR · Validation · cli-gofmt` => success
  - `PR · Source format` => success
  - `PR · Trusted Plan` => success
  - `PR · Native gate plan` => success
  - `PR · Focused Python` => success
  - `Workflow policy` => success
- Full job terminal list (all 30 completed):
  - success: `PR · Focused Python`, `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, `PR · Go unit · owner`, `PR · Go unit · packages`, `PR · Native gate plan`, `PR · Source format`, `PR · Trusted Plan`, `PR · Validation · cli-gofmt`, `PR · Validation · go-build`, `PR · Validation · go-vet`, `Workflow policy`
  - skipped (not applicable to a pure Go logic change; skipped != pass per §5.4): `PR · Candidate-added checks (advisory)`, `PR · Consumer Pins`, `PR · Demo Pin`, `PR · Draft Go · ${{matrix.shard}}`, `PR · Draft source and routing`, `PR · Exact Candidate`, `PR · Exact full Pre-Release`, `PR · Main release Go · ${{matrix.shard}}`, `PR · Main release source`, `PR · Native Keycloak/Core · ${{matrix.runtime}}`, `PR · Public Contracts`, `PR · Runner Interface`, `Release Source Preflight`, `Targeted HA · docker`, `Targeted HA · podman`, `validate`

## SKIPPED CELLS (with gate-plan justification, §5.4 — skipped is NOT a pass)

- All 16 skipped gates are runtime/native/release/contract gates (`Native Keycloak/Core`, `Selected Runtime`, `Targeted HA · docker/podman`, `Main release Go`, `Public Contracts`, `Consumer Pins`, `Demo Pin`, `Runner Interface`, `Release Source Preflight`, `validate`). They require a runtime/container/DB/HA environment and are not applicable to a change confined to `internal/metrics/prometheus_files.go` (pure composition-state logic) and `cmd/baha/app_metrics.go` (CLI surface). The Go unit gate (`go test ./...`, which selects `internal/metrics`) plus build/vet/gofmt cover the changed paths durably. Per CI policy 2026-11-19, required checks come from the base plan; checks this PR adds are advisory. No required gate is red.

## repo-rule compliance

- No `.github/**` edit (Owner scope) — none needed; the new test rides the existing `go test ./...` unit gate.
- Single integration candidate branch; no second branch.
- No merge of the PR, no CODEX verdict, no force, no subagent.
- No VM / container / compose / network / volume.
- Evidence written to planning evidence dir (not a product repo).

## BRANCH PROVENANCE

- Base of hopf: develop `bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978` (also the base SHA of PR #1695).
- `git ls-remote origin lane-0428-124-metrics-verification-none`: `8d55cc03e1503f9e2dd827b014bcfd0923c9dbde`.
- `git log --oneline 4f0d5e9f7..origin/develop` witness above.
- First-parent log from `bbc937c8` carries ONLY my r3 commits (see hopf section) — no foreign candidate.

## cleanliness:

- No stray files under the ecosystem root; work done in /tmp/x124-wt.
- No docker/podman compose projects started (no ps-witness needed).
- Evidence file written to planning repo evidence dir only.

## END

END_DONE — 0428-124 r3. Head `8d55cc03` (two-parent hopf onto develop `bbc937c8`), own CI run 44648669949 completed/success (14 success / 16 skipped, 0 failures).
