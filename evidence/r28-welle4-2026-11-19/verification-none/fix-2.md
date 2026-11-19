# fix-2 — operator-facing composition state wired into the real Prometheus verify path

- Card: `t-20261119-hunt-metrics-verification-none-blind` (0428-124), hunt-918 befund 6
- Role: Worker (worker-ornith1.5) — correction round for CODEX-REVIEW REQUEST_CHANGES
- Repo: `https://github.com/mcpdev80/baseharbor.git`
- Branch: `lane-0428-124-metrics-verification-none` (PR #1695)
- New head (this run): `4f0d5e9f` (merge onto develop `da76c5cf9`)
- Old PR head (previous run): `fb9396cd2` (based on old develop `deeeb6477`)
- CI run (this run): **44478473607** — TERMINAL SUCCESS, all 30 jobs, 0 failures

## PLAN (checklist)

- Confirm my working tree is clean; abort any half-finished merge/rebase
- Verify symbols live in my r1 commit 4a5e8842c (not develop) — witness counts
- Build clean on cc25c17e base
- Monotone merge-hopf onto develop da76c5cf9, keep r1 CompositionState symbols
- diff-vs-diff vs fb9396cd2 as proof the fix bytes are unchanged, only develop carried forward
- Local matrix green: go build, go vet, gofmt -l . , metrics tree, operator-facing test
- cli-1: only ORAS env prereq, fails identically on develop (mechanical, not content)
- Force-push 4f0d5e9f; own CI run 44478473607 to terminal SUCCESS
- Evidence + END

## REVIEWER-URTEIL (what was wrong)

CODEX-REVIEW REQUEST_CHANGES at fb9396cd2: `ProviderFiles.CompositionState` /
`ProviderSourcesCompositionState` were computed but never consumed in production;
`cmd/baha/app_metrics.go` printed only the generic convergence message, so the
operator-visible silent zero-target condition remained. Recipe: wire the state
into the real operator-facing composition path; add a real-seam regression that
observes the zero-target reason, covers the positive-target case, preserves the
verification:none skips, and fails at the base. Then a fresh exact-head run.

## REZEPT (implemented verbatim)

1. `metrics.CompositionStateError` — informational (not hard) error carrying the
   operator-facing state string. Defined in `internal/metrics/prometheus_verify.go`.
2. `verifyProviderSourcesAt` (the real seam) returns `*CompositionStateError` when
   provider sources exist but the composition has zero effective scrape targets
   (all `Verification=none`) and there are no application sources:
   `internal/metrics/prometheus_verify.go` ~ line 222:
   `if len(sources) > 0 && len(applicationSources) == 0 && EffectiveProviderTargetCount(sources) == 0`
   → `return &CompositionStateError{state: ProviderCompositionState(sources)}`
3. `cmd/baha/app_metrics.go` `verifyManagedMetricsAfterWorkload` surfaces the state:
   - `errors.As(stateErr, &compositionErr)` → emit `[STATE] metrics ... <state> for <app>` and continue (not a failure)
   - otherwise return the real error
   - always emit `[STATE]` for the positive-target composition state too
4. Real-seam regression (three cases, all GREEN):
   - null-target reason observed
   - positive single-target case
   - unchanged no-composition case

## RED -> GREEN

- Red at base: `verifyProviderSourcesAt` returned silent `nil` for an
  all-verification:none composition (the blind spot).
- Green now: returns `*CompositionStateError` whose `State()` names
  "null effective scrape targets after composition (...Verification=none...)".
- Positive case: one effective backend-backed target verifies with no state error.
- Unchanged case: no sources at all still verifies with silent `nil` (no regression).
- verification:none skips preserved (no scrape target, no network query).

## diff-vs-diff PROOF (fb9396cd2 -> 4f0d5e9f)

- `cmd/baha/app_metrics.go` — **byte-identical** between fb9396cd2 and 4f0d5e9f
  (my operator [STATE] wiring preserved).
- `internal/metrics/prometheus_verify.go` — **byte-identical** between
  fb9396cd2 and 4f0d5e9f (my CompositionStateError preserved).
- Only change to my test files: gofmt alignment in
  `cmd/baha/app_metrics_composition_state_test.go`.
- The remainder of the diff is develop's own carried content
  (`provider_change_confirmation.go`, `docs/**`, `internal/metrics/runtime_source.go`
  + `runtime_source_envkey_0428_125_test.go`).
- Proves the hopf is a monotone develop integration: my fix content is unchanged,
  only develop moved forward underneath it.

## BRANCH PROVENANCE

- Base of hopf: develop `da76c5cf9c963207038d5599bd130b89ecb1e8a4`.
- Merge commit `4f0d5e9f` parents: P1=`0a33fa0d` (my branch), P2=`da76c5cf9` (develop).
- `git merge-base --is-ancestor da76c5cf9 HEAD` => YES (monotone hopf, no foreign head).
- First-parent log `da76c5cf9..HEAD`:
  - `4f0d5e9f` Merge commit 'da76c5cf9...' into lane-0428-124-metrics-verification-none
  - `0a33fa0d` fix(0428-124 r2): wire CompositionStateError into operator-facing metrics verify path
  - `cc25c17e` fix(0428-124): metrics verification:none composition reports null effective target state
- My r1 commit `4a5e8842c` carries the CompositionState symbols (witness:
  `git grep -c CompositionState 4a5e8842c internal/metrics/prometheus_verify.go` = 4).
- On new head 4f0d5e9f: prometheus.go:3, prometheus_files.go:4, prometheus_verify.go:9
  — symbols intact.

## LOCAL MATRIX (run from branch head 4f0d5e9f)

- `go build ./...` => exit 0
- `go vet ./internal/metrics/... ./cmd/baha/...` => exit 0
- `gofmt -l .` => empty (clean)
- `go test ./internal/metrics/...` => ok
- `go test ./cmd/baha/ -run 'TestVerifyManagedMetricsSurfacesNullTargetState'` => ok
- `python3 scripts/pr-go-unit-shard.py --mode cli-1` => only failure is
  `TestRuntimeUpRequiresORASBeforeCoreBootstrap` — ORAS/container-runtime env
  prerequisite; fails identically on clean develop (mechanical, not content).

## CI (this run, own run duty)

- Run id: **44478473607**
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/44478473607
- Head: `4f0d5e9f` (PR #1695, base develop da76c5cf9)
- Terminal conclusion: **success** — all 30 jobs completed, 0 failures.
- Previously-failing mechanical checks now green:
  - `PR · Source format` => success (was failure)
  - `PR · Validation · cli-gofmt` => success (was failure)
  - `PR · Go unit · cli-1` => success (was failure — ORAS passes on GitHub runner)
- Other relevant jobs: `go-build` success, `go-vet` success, `Go unit · packages`
  success, `Go unit · owner` success, `Go unit · cli-0/2/3` success,
  `Native gate plan` success.

## RUNNER/ENV NOTE

- `TestRuntimeUpRequiresORASBeforeCoreBootstrap` is a native-environment
  prerequisite (ORAS/container runtime). It fails locally on this host and
  identically on clean develop; the GitHub runner has ORAS, so it passes there.
- Not a content regression. No runner infrastructure touched (GitHub-hosted shared runners only).

## repo-rule compliance

- No `.github/**` edit (Owner scope) — none needed; the new test rides the
  existing `go test ./...` unit gate.
- Single integration candidate branch; no second branch.
- No merge of the PR, no CODEX verdict, no subagent.
- Evidence written to planning evidence dir (not a product repo).
