# Round 3 — REQUEST CHANGES fix, hop, CI terminal

ROLLE: WORKER
Karte: 0428-076 (perses-dashboard-databases)
PR: #1597, branch perses-dashboard-databases-lane
Plan-sha (evidence authoring): baseharbor-plan origin/main
Datum: 2026-11-21

## PLAN

1. Read review-2.md REQUEST CHANGES and the two owner answers (ans-076.md, ans-076b.md). Done.
2. Fix BEFUND 1 (per-target database-panel builder, gate on the resolved observability-signal status, not the engine name). Done.
3. Fix BEFUND 2 (define Perses dashboard-level variables $application/$env with defaults resolved from the resolved manifest, so no selector carries an undefined placeholder). Done.
4. Regenerate goldens via the production path (no hand-edit). Done.
5. Update the metrics assertion for BEFUND 2 and add a CLI negative test that drives the real resolve path. Done.
6. Run the three required mutations at the fix exact-SHA; confirm all three FAIL red; restore clean. Done.
7. Hop the fix onto measured develop with a clean single fix commit; push ONLY perses-dashboard-databases-lane. Done.
8. Run hosted CI to terminal on the exact fixed head. Done (run 44932093726 success).
9. Publish this file to baseharbor-plan origin/main. In progress.

## BEFUND 1 fix

PersesDashboardAvailability now takes the resolved application.Manifest and derives each backend's
verdict from the RESOLVED observability-signal status, never a caller-supplied boolean and never a
hard-coded per-engine table (owner decision 2026-11-16, decision recorded in the code comment
perses_dashboards.go:688-695).

- persesDashboardBackendAvailable(m application.Manifest, backend capability.ProviderKind): true only
  when manifestPersesSelected(m) (observability management UI selected + Perses pinned + the pinned
  Perses release validates) AND the backend carries a native metrics signal OR is one of the three
  real observability surfaces (Prometheus/Loki/Tempo). PostgreSQL/MongoDB are neither and resolve to
  explicit unavailable.
- PersesDashboardAvailability(m) computes selected := manifestPersesSelected(m) once and answers every
  backend from that single resolved status; a real backend is "available" only when the resolved
  manifest verified observability, otherwise "unavailable" with a concrete reason. An unverified
  target fails closed: every entry unavailable with a concrete reason, never an inferred available
  and never an empty-witness unavailable (0428-142 class).
- Wired cmd/baha/app_status_result.go:150 to pass resolved.Manifest.

PostgreSQL/MongoDB resolve to EXPLICIT UNAVAILABLE with a concrete reason naming the missing verified
signal in the pinned reference catalog (ObservabilityUnsupported). This is intended, not a regression.

## BEFUND 2 fix

Real-backend dashboards DEFINE their dashboard-level Perses variables $application (default m.Name) and
$env (default m.Environment), both sourced from the RESOLVED manifest (BEDINGUNG 1: the default comes
from the resolved manifest path, not a hardcoded code constant). The Prometheus query references the
defined variables, so the selector carries no undefined placeholder.

- persesDashboardVariables(m application.Manifest) builds the two variables from the resolved manifest;
  the variable default is m.Name / m.Environment, never a literal word baked into the code.
- persesDashboardForBackend(m, key) embeds Variables: persesDashboardVariables(m) on each real backend
  dashboard.
- persesDashboardCatalog() resolves the shipped catalog against a deterministic manifest
  (Name:"perses-dashboard-databases", Environment:"dev") so the goldens show the defined-variable shape
  with real defaults, not undefined placeholders.
- cmd/baha/app_perses_cli_test.go: added TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed,
  which drives the genuine baha status --json for a manifest that does NOT select the observability
  management UI and asserts every entry (all three real backends plus PostgreSQL/MongoDB) is
  "unavailable" with a concrete reason. This is the negative path the review required.
- internal/metrics/perses_dashboards_test.go: assertValidPromQL now also calls assertDashboardDefinesVariables,
  which unmarshals the shipped dashboard and asserts $application and $env are DEFINED with a non-empty
  default (BEDINGUNG 2: "the variable is DEFINED and the selector is valid", not "the placeholder is
  undefined"). An absent variables block fails this assertion.

## MUTATIONS (exact-SHA, all FAIL red, then restored clean)

Gate is load-bearing and fail-closed. Verified on branch perses-076-rc-fix at e1007ea1 (pre-hop).

- (a) mark a database entry "available": TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases FAILS
  red: database "postgresql-targets" must report unavailable, got "available".
- (b) remove the verify gate (manifestPersesSelected short-circuit): TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed
  FAILS red: database "prometheus-targets" must report unavailable when observability is unverified, got "available".
- (c) pure engine-name table (replace the resolved-manifest observability gate with an engine-name switch):
  TestBahaStatusDatabaseDashboardsUnverifiedTargetFailsClosed FAILS red: database "prometheus-targets"
  must report unavailable when observability is unverified, got "available". This proves the gate is the
  resolved signal status, not the engine name (finding requirement (iii)).

Restored clean; all green before the hop.

## GOLDEN PROVENANCE

All goldens regenerated via the production path (persesPanelJSON on the shipped catalog), no hand-edit.
git log --format=%h|%an|%ad per golden:

- internal/metrics/testdata/perses-dashboards/prometheus-targets.json: 074678d1|0428-076-nativeshape|2026-11-21
- internal/metrics/testdata/perses-dashboards/loki-logs.json: 074678d1|0428-076-nativeshape|2026-11-21
- internal/metrics/testdata/perses-dashboards/tempo-traces.json: 074678d1|0428-076-nativeshape|2026-11-21
- internal/metrics/testdata/perses-dashboards/postgresql-targets.json: 074678d1|0428-076-nativeshape|2026-11-21
- internal/metrics/testdata/perses-dashboards/mongodb-targets.json: 074678d1|0428-076-nativeshape|2026-11-21
- internal/metrics/testdata/perses-native/v0.55.1/prometheus-app-up.json: 074678d1|0428-076-nativeshape|2026-11-21
- internal/metrics/testdata/perses-native/v0.55.1/loki-app-errors.json: 074678d1|0428-076-nativeshape|2026-11-21
- internal/metrics/testdata/perses-native/v0.55.1/tempo-app-traces.json: 074678d1|0428-076-nativeshape|2026-11-21

## BRANCH PROVENANCE (hop)

Measured develop before the hop: git ls-remote refs/heads/develop = e6c199e7b7dd7d076a776d11c3ba16f25e59c254.

The PR branch lineage (37d396000) carried a stray 0428-076-hop2 commit that bumped go.mod/go.sum, which
would have put a foreign author on develop..head. Rebuilt the hop as a single clean fix commit on measured
develop:

- New commit afbcabfc -> amended 074678d1 on develop e6c199e7b7dd, author 0428-076-nativeshape.
- git merge-base --is-ancestor origin/develop HEAD: OK (develop is an ancestor of the fix head).
- git log --format=%an origin/develop..HEAD: ONLY 0428-076-nativeshape.
- git rev-list --count HEAD..origin/develop: 0.
- go.mod/go.sum: NOT in the write-set (verified the build and the metrics + cmd/baha perses tests pass on
  the develop base without the go.mod/go.sum bump).
- Write-set: cmd/baha/app_status_result.go (wiring), cmd/baha/app_perses_cli_test.go (negative test),
  internal/metrics/perses_dashboards.go, internal/metrics/perses_dashboards_test.go,
  internal/metrics/perses_dashboards_helpers.go, internal/metrics/perses_dashboards_0428-076_native_test.go,
  internal/metrics/perses_dashboards_promql_test.go, and 8 goldens. NO tabu files, NO go.mod/go.sum.
- Pushed ONLY perses-dashboard-databases-lane (37d396000 -> 074678d1, forced update). No new branch, no
  merge, no subagents, no git add -A, no git stash.
- Delivery witness (git ls-remote): afbcabfc39fa389229d00762eed85c05b67af0f8 -> perses-dashboard-databases-lane;
  then 074678d149e5b8d0f899c55da92debf52bf0fd46 -> perses-dashboard-databases-lane.
- gh pr view 1597: headRefName perses-dashboard-databases-lane, state OPEN, headSha 074678d1.

## CI

Run 44932093726 (pull_request, branch perses-dashboard-databases-lane, headSha 074678d149e5b8d0f899c55da92debf52bf0fd46),
terminal SUCCESS. No failures; no skipped-required (skips are advisory/release gates).

Per-cell conclusions:
- PR Selected Checks: success
- PR · Source format: success (this was the failure in run 44931477589; resolved by gofmt -w on
  perses_dashboards.go — the struct field tags were over-aligned; the fix is a formatting-only amend)
- PR · Validation · go-build: success
- PR · Validation · go-vet: success
- PR · Validation · cli-gofmt: success
- PR · Go unit · packages: success
- PR · Go unit · owner: success
- PR · Go unit · cli-0/1/2/3: success
- PR · Trusted Plan / Workflow policy / PR · Native gate plan: success

Three byte-counts (counted only from the per-job logs, gh api .../logs | wc -c):
- Go unit packages (job 136930802217): 33409 bytes. Logs contain PASS all non-CLI Go package tests and
  internal/metrics ok 0.450s — the metrics package actually ran in CI, so BEFUND 1 and BEFUND 2 changes
  are durable evidence, not local-only.
- go-build (job 136930802172): 33344 bytes.
- go-vet (job 136930802171): 33344 bytes.

No owner-scope test_real_candidate_go_registration_families run this PR; that failure is a prior-shift
state, not evidence for this candidate.

## repo-rule compliance

- Write-set confined to the card's metrics/status files plus app_status_result.go (wiring) and
  app_perses_cli_test.go (negative test). No tabu files touched: no perses_selection.go, no
  observability/registry.go, no .github/**, no scripts/**, no identityprovider/**, no serviceaccess/**,
  no operatorauth/**, no go.mod/go.sum. git diff --name-only origin/develop..HEAD lists exactly the 15
  files above.
- Exactly one integration candidate per chain: the fix sits directly on measured develop; develop..HEAD
  shows ONLY 0428-076-nativeshape; rev-list head..develop = 0.
- No subagents (Owner directive 2026-11-04): every step ran inside this session's own shell and git.
- No .github/** edits; the format failure was fixed locally with gofmt, which the CI gofmt/vet jobs then
  confirmed.
- Evidence lives only in baseharbor-plan (this file), never in the product repo.

## cleanliness

- No compose/docker/podman projects started this shift; no container/netzwerk/volume witness needed.
- Temp CI logs written to /dev/shm and removed before END; no stray files in /home/marcel/dev/baseharbor-ecosystem
  (git status --short clean). Worktree under /dev/shm/0428-076-fix-wt.
- The stale hop3 worktree /dev/shm/0428-076-hop3-wt was not reused (mission mandates a fresh worktree per
  fix); left for coordinator housekeeping.

## END

END_BLOCKED 0428-076-nativeshape: fix + hop + CI terminal all complete and green, but evidence publish to
baseharbor-plan origin/main is not yet verified via tree witness. This is a blocker on the publish step,
not on the fix. Publish to origin/main, re-verify the tree witness, then post END.
