# 0428-082 · native Perses infrastructure dashboards — round-6 (Luna batch19 correction)

Lane: flash worker (mission `/var/tmp/missions/mission-082-perses-dashboards-r6-pinfix.md`).
Candidate base: `dda073da4` (PR #1665, DRAFT, base `w083-perses-datasources`).
New commit this round: `e580d32414565442376f23ace9a4a2dd7ed03838` (pinfix only).
Remote witness: `git ls-remote origin refs/heads/lane-0428-082-perses-dashboards`
before push = `dda073da4a495f61d2f754ae37a0262225f68df8`, after push =
`e580d32414565442376f23ace9a4a2dd7ed03838` (fast-forward). PR head refreshed and
verified: OPEN draft=true base=w083-perses-datasources head=e580d3241.

## PLAN checklist

1. [x] Reality check: ls-remote, fresh worktree at `dda073da4`, batch19 akte read
   (`batch19/act-luna-batch19.md` @ c9967d18).
2. [x] Release argument threaded (no default-substitute when a release is supplied);
   unpinned stays fail-closed.
3. [x] `TestPersesPrometheusDatasourceFailClosedWhenUnpinned` + whole `internal/metrics`
   group GREEN in the lane's own go-test run; 080 files byte-identical.
4. [x] Commit on `dda073da4`, refspec push + ls-remote before/after; PR stays DRAFT.
5. [x] New exact-head `workflow_dispatch` run to terminal (43999100666): the batch19
   blocker (`Run unit and package tests`, incl. `internal/metrics`) is GREEN; the run
   still falls at the documented, base-owned runtime-integration set (below).
6. [x] Target-root fix (`dda073da4`) retained unchanged (Luna: begruendet + separat belegt).
7. [x] Akte + board todo + END post.

## The fix (batch19 Object 2 recipe point 1)

Finding (Luna, confirmed): at `dda073da4`, `internal/metrics/perses_prometheus_datasource.go`
:185-186 — `buildPersesPrometheusDatasourceWithProbe` received an explicit `release` but
called `buildPersesPrometheusDatasourceAt(m, probe, "", "")` **without it**, and that helper
unconditionally substituted `capability.PersesDefaultRelease` (line :193 `release :=
capability.PersesDefaultRelease`). An invalid/unpinned release was therefore silently replaced
by the supported default, and `TestPersesPrometheusDatasourceFailClosedWhenUnpinned`
(`perses_prometheus_datasource_test.go:280-288`) went red — exact-head witness: dispatch run
`43997001011` on `dda073da4`, `Run unit and package tests` FAILED
("unpinned perses must fail closed, not fabricate a datasource").

Fix shape, exactly per recipe: the Target-bound core is now
`buildPersesPrometheusDatasourceAtWithRelease(m, release, probe, dataDir, namespace)`
(datasource.go :199). Two delegates, each passing the release it INTENDS:

- `buildPersesPrometheusDatasourceWithProbe` (:185) passes the caller's explicit release —
  no default-substitute when a release was supplied; unpinned fails closed again.
- `buildPersesPrometheusDatasourceAt` (:196) passes `capability.PersesDefaultRelease` — the
  production default-pin entry point (the infra-dashboard face,
  `perses_infra_dashboards.go:615`), behavior unchanged.

`git diff dda073da4..e580d3241 --name-only` = `internal/metrics/perses_prometheus_datasource.go`
only (1 file, +10/−3). The 0428-080 selection files are byte-identical (`diff -q` against
`dda073da4` blobs: PASS). The Target-root binding commit `dda073da4` is untouched.

## Local verification (candidate e580d3241)

- `go test -count=1 -v -run TestPersesPrometheusDatasourceFailClosedWhenUnpinned ./internal/metrics`
  → `--- PASS` (red-before reproduced only at `dda073da4`; host run this round, TMPDIR under /var/tmp).
- `go test -count=1 ./internal/metrics ./internal/capability` → both `ok`.
- `go test -count=1 -run 'TestPersesInfra|TestBahaStatusInfrastructure' ./cmd/baha` → `ok`.
- `go build ./cmd/baha` PASS; `go vet ./...` PASS; `gofmt -l cmd internal contracts` empty;
  `bash scripts/source-readability-audit.sh` PASS (size/span/ratchet).

## Exact-head dispatch qualification (recipe point 2)

`workflow_dispatch` run **43999100666** on `e580d3241` (CI · Source & Quality,
watched to terminal per Eigenes-Run-Pflicht):

- `Run unit and package tests` — the step that failed red at `43997001011` — **SUCCESS**.
  Log witness: `ok github.com/mcpdev80/baseharbor/internal/metrics 0.249s` (the
  package-job run is not `-v`, so individual tests emit no lines; the witness is
  (1) the package PASS line — impossible while any test in it fails, which is exactly
  how `43997001011` went red with `--- FAIL: TestPersesPrometheusDatasourceFailClosedWhenUnpinned`
  / `FAIL github.com/mcpdev80/baseharbor/internal/metrics 0.349s`, and (2) the lane's
  own verbose local run above, which executes the test at the same commit.
- The run as a whole is FAILURE at a LATER, base-owned step: `Run runtime integration
  tests serially`. Its failures are the documented runtime set — `ORAS is required by
  BaseHarbor integration tests, but it is not installed` on the hosted runner
  (`app_repository_integration_test.go:27` trust-plane prepare):
  `TestRepositoryWorkflowRealLifecycle`, four `TestRepositoryCompose*…InCI`/
  `TestRepositoryBuildWorkload…InCI` in `cmd/baha`, and
  `TestMultiInstanceComposeLifecycleInCI` in `internal/application`.
  This same step fails identically on unrelated heads of this base — e.g. dispatch run
  `43968469748` on `d2a9cd11d` fails `Run runtime integration tests serially` too — and
  none of the failing tests exist in this PR's diff (this PR changes only
  `internal/metrics/*` and `cmd/baha/app_status_result.go` + its test files). Round-4
  classified this set as a dispatch-context/runner-property gap (triage); it is not a
  product fail of candidate `e580d3241` and no lane-side fix is in scope.
- Conclusion per recipe: the exact-head witness that BLOCKED approval (`43997001011`) is
  superseded; `internal/metrics` (incl. the unpinned fail-closed pin) is GREEN in a
  hosted exact-head run at `e580d3241`. `pull_request` runs for #1665 remain gated by the
  PR-run allowlist doorstop (rounds 3/4 finding) — dispatch is this lane's qualification
  path, as in prior rounds.

## Live-witness pending on 0428-100 content

Per Luna batch19: the `httptest` round trips in
`TestPersesInfraDashboardVerifiesOverRealHTTPPath` validate the production HTTP/query path
but are scripted, and the round-5 cell fell before any real query because the deploy path
materialized `runtime-sources.json sources: []` for the workload-only app. That registration
gap is card **0428-100** ("Workload-only metrics source registration",
`tasks/t-20261117-workload-only-metrics-source-unregistered.md`, lane
`lane-0428-100-workload-only-registration` per its round-1 evidence at
`evidence/r28-welle3-2026-11-16/workload-only-registration/round-1.md`). Its PR reference:
the card's `prs: []` is still EMPTY at the current planning remote (`origin/main` fetched
this turn) — no hosted PR exists to cite yet. Once 0428-100 lands its registration fix,
this lane's self-contained `scripts/cell-witness.sh` (round-5 akte) re-runs the deploy →
product-path verify to a real per-panel `/api/v1/query` over materialized sources; the
dashboard side (verifier, face, Target-root binding) needs no change for that witness.

## CI capture note

All new/changed tests live in `internal/metrics` and `cmd/baha` packages, executed by the
existing package job (`Run unit and package tests`) — proven by this round's hosted run.
No test is cell-only; no `.github/**` change was needed or made.

## Cell hygiene

No cell was run this round (the deploy-path fall is 0428-100's content, not this pinfix);
`baha-docker` zone `w082r5` remains as left by round-5: containers 0, no zone resources.

## Handoff

- Candidate: `e580d3241` on `lane-0428-082-perses-dashboards` (chain
  `47d4ff298 → d2a9cd11d → 081dc926d → dda073da4 → e580d3241`), PR #1665 DRAFT base `w083-perses-datasources`.
- batch19 recipe: point 1 fixed, point 2 qualified (metrics green exact-head; the residual
  dispatch failure is the documented runner-tooling set with run IDs above), point 3
  pending 0428-100 content (paragraph above).
