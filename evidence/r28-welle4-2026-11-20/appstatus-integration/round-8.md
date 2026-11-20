# round-8 · 0428-078 · verified-only gate, catalog removed (single commit)

**Card:** `t-20261114-r28-perses-dashboard-identity` (0428-078)
**Acceptance (r7):** REQUEST CHANGES (the verified-only predicate). The r7 head `0baeaf5550` is the accepted candidate; this round reworks it.
**Owner r8 decision (supersedes r7/P4):** the identity dashboard catalog (`perses_identity_dashboards.go`) has ZERO production consumers — a test-only golden is not a release artifact. Shrink PR #1650: remove the catalog (+test +testdata). Keep the verified-only predicate, its gate test, and the `IdentitySelectionWitnessAt` gate primitive (with P3 target-isolation). Card 0428-181 carries the catalog as a sequenced follow-up (after #1684). `internal/capability/perses_selection.go` stays forbidden for all lanes.
**Candidate head (frozen):** `9add5e8a2122c5555c2403d5ea04073cfb2dc842` (PR #1650, branch `lane-0428-078-perses-identity-on-resolver`, single commit rebased onto develop `96f2ae11a25`)
**Worktree:** `/var/tmp/wt-078-r4`
**Final write-set (r8, one commit):** `cmd/baha/app_status_result.go` (verified-only predicate + `identityDashboardBackendEligible`), `cmd/baha/app_status_perses_gate_test.go` (P1/P2/P5 gate regressions), `internal/metrics/perses_identity_witness.go` (P3 target-isolation) + its test. REMOVED from this PR: `internal/metrics/perses_identity_dashboards.go`, `perses_identity_dashboards_test.go`, `testdata/perses-identity-dashboards/identity-keycloak.json`. NO `perses_selection.go`, NO `.github/**`, NO `scripts/**`. NO subagent (§4.8). NO `git add -A`.
**Local regression:** `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses` (local), `...RemoteTarget` (remote), `...GatesOnKeycloakWitness`; witness `TestIdentityWitnessIsolatedToConcreteTarget` (P3 two-target).

## PLAN

1. Resolve P4 (owner r8): the catalog is a zero-consumer package; remove it from PR #1650 so the candidate carries no dead tree.
2. Keep the verified-only predicate `app_status_result.go:163-167` (both `not_configured` and `configured_unverified` fail closed; `verified` only) and its gate test.
3. Keep the `IdentitySelectionWitnessAt` gate primitive WITH my P3 target-isolation (the blocker the reviewer assigned to `perses_identity_witness.go:37-40`/`:64`).
4. P1: extract the verified-only decision into `identityDashboardBackendEligible`, called by both the local return and the remote-target early return; drive the positive verified+real-witness case through it to `identity_dashboard_eligible=true`.
5. P2: remote fixture serialises the production `applicationStatusResult` through the same json tags the public `baha status --json` face uses and decodes the two gated fields from the real serialisation (no manual struct projection).
6. P5: two isolated mutations with distinct mutants/testnames/verbatim red output (witness `perses_selection.go:110 -> false`; predicate `verified-only -> old configured_unverified form`).
7. Pre-push checks: `go build ./…`, `go vet ./…`, `gofmt -l` (empty), gate + metrics suites.
8. Push via `lane-origin`, single commit rebased onto `96f2ae11a25`, freeze proof (3 lines), one `pull_request` CI run to terminal, run-id + conclusion, then publish this akte on origin/main.

## P4 — catalog removed (owner decision, not a blocker left open)

`git grep` at the r7 head `0baeaf5550` shows `PersesIdentityDashboardAvailability` / `identityDashboardCatalog` are called ONLY within `perses_identity_dashboards.go` itself (`:434` calls `:380`) — zero external callers, no `deploy/` writer, no `perses_runtime.go` route, no `baha perses export` consumer. `FilterEligibleDashboards` / `EligibleCount` in `perses_selection.go` likewise have zero production callers. The identity dashboard was a test-only golden, not a released artifact — exactly the scope violation §4.2 guards against.

Removed from this PR:
- `internal/metrics/perses_identity_dashboards.go` (-503)
- `internal/metrics/perses_identity_dashboards_test.go` (-376)
- `internal/metrics/testdata/perses-identity-dashboards/identity-keycloak.json` (-137)

Consumer of `perses_identity_witness.go` in this PR = `cmd/baha/app_status_result.go:343`.

Proof (`git grep -n IdentitySelectionWitnessAt` at candidate head `9add5e8a2`):
```
cmd/baha/app_status_result.go:327://     Target (fail-closed). This is IdentitySelectionWitnessAt().NonForgeableAvailable(),
cmd/baha/app_status_result.go:343:	identityWitness := metricsprovider.IdentitySelectionWitnessAt(m, keycloakPlacement, targetStateRoot, targetName)
```
A single production consumer (`app_status_result.go`) — the witness is a live gate primitive, not a second dead tree. Card 0428-181 carries the catalog, sequenced after #1684 (both touch `internal/application/perses_runtime.go`); `perses_selection.go` stays locked for all lanes.

## P3 — target-isolation of the witness (blocker, both directions)

`keycloakMetricSignals` previously accepted any native `keycloak-metrics` registry source on the shared sharing boundary, ignoring the signal's `Target`. The fix (`perses_identity_witness.go:134-140`) rejects a signal bound to ANOTHER Target: only a signal resolved to this concrete Target's binding satisfies a positive witness.

New regression `TestIdentityWitnessIsolatedToConcreteTarget` (two targets, same `ScopeShared` + same `SharingBoundary`): only target A has the signal → target A eligible, target B fail-closed (`MetricPresent=false`).

Stop criterion — filter removed makes the regression RED:
```
$ perl -0pi -e 's|...target-isolation guard...||' internal/metrics/perses_identity_witness.go
$ go test ./internal/metrics/ -run 'TestIdentityWitnessIsolatedToConcreteTarget' -v -count=1
    perses_identity_witness_test.go:127: target B witness must fail closed when only target A has the signal: {SelectionConfirmed:true MetricPresent:true MetricCurrent:true TargetAuthorized:true Available:false}
--- FAIL: TestIdentityWitnessIsolatedToConcreteTarget (0.00s)
```
Restored → green.

## REMOTE WITNESSES (P2)

The remote regression `remoteIdentityStatusJSON` (app_status_perses_gate_test.go) now serialises the production `applicationStatusResult` through the same json tags the public `baha status --json` face uses, then decodes the two gated fields from that real serialisation:
```go
encoded, err := json.Marshal(status)
...
var decoded identityStatusJSON
json.Unmarshal(encoded, &decoded)
```
No live mTLS/Core session, no Core stub, no container — the gate fields are computed from the resolved manifest before the remote-target early return (app_status_result.go remote face). Mutating the serialisation/decode away makes the regression RED (the two gated fields no longer survive the real json path). Both negative faces (`configured_unverified => false`, `not_configured => false`) hold.

## MUTATIONSPROOF (per surface, verbatim)

Host: `/var/tmp/wt-078-r4` · `GOCACHE=/var/tmp/gocache-r5 GOMODCACHE=/var/tmp/gomodcache GOTMPDIR=/var/tmp/gotmp-r8 TMPDIR=/var/tmp`.

- **P5 witness mutation** (`internal/capability/perses_selection.go:110 NonForgeableAvailable() -> false`):
  ```
  $ go test ./cmd/baha/ -run 'TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses/perses-verified-real-witness-eligible' -count=1
  --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses
      --- FAIL: .../perses-verified-real-witness-eligible (0.00s)
          app_status_perses_gate_test.go:192: the positive witness must be non-forgeable available
  ```
  Isolated test: `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses/perses-verified-real-witness-eligible`.

- **P5 predicate mutation** (`identityDashboardBackendEligible`: verified-only -> old `configured_unverified`-accepting form):
  ```
  $ go test ./cmd/baha/ -run 'TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses' -count=1
  --- FAIL: .../perses-verified-real-witness-eligible
      app_status_perses_gate_test.go:204: configured_unverified must fail closed on identityDashboardBackendEligible
  ```
  Isolated test: same suite, assertion `:204`. Different mutant (`perses_selection.go:110` vs the predicate), different assertion line — two independent proofs.

- **P3 target-isolation** (filter removed, above): `perses_identity_witness_test.go:127`, test `TestIdentityWitnessIsolatedToConcreteTarget`.

## PRE-PUSH LOCAL CHECKS

```
$ go build ./cmd/baha/ ./internal/metrics/                                   -> BUILD EXIT: 0
$ go vet ./cmd/baha/ ./internal/metrics/                                     -> VET EXIT: 0
$ gofmt -l cmd/baha/app_status_result.go cmd/baha/app_status_perses_gate_test.go internal/metrics/perses_identity_witness.go internal/metrics/perses_identity_witness_test.go  -> (empty = ok)
$ go test ./cmd/baha/ -run 'TestIdentityDashboardEligible'                   -> ok
$ go test ./internal/metrics/ -run 'TestIdentityWitness'                     -> ok (all 5 witness cases PASS)
```

## CI SHARD (exact head)

`scripts/pr-go-unit-shard.py` assigns by `sha256(test_name) % 4`. `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses` → `cli-1`; `...GatesOnKeycloakWitness` → `cli-0`; `...RemoteTarget` → `cli-1`. Corrected tests run in `PR · Go unit · cli-1`.

## FREEZE PROOF (at exact head `9add5e8a2`)

```
$ git ls-remote lane-origin refs/heads/lane-0428-078-perses-identity-on-resolver refs/pull/1650/head
9add5e8a2122c5555c2403d5ea04073cfb2dc842	refs/heads/lane-0428-078-perses-identity-on-resolver
9add5e8a2122c5555c2403d5ea04073cfb2dc842	refs/pull/1650/head

$ git merge-base --is-ancestor 96f2ae11a25a508998c44a9854ef17f8fa15c112 HEAD
-> JA   (develop 96f2ae11a25 is an ancestor of head)
```

Branch head == PR #1650 head == `9add5e8a2122c5555c2403d5ea04073cfb2dc842` (same SHA). develop head `96f2ae11a25` (0428-166 merged). Single commit on top of develop. No second candidate pushed; the r7 head `0baeaf5550` was superseded by this rebase, not merged.

## CI (own terminal run, §4.6)

Run **`44737589479`** (`CI · PR #1650`, event `pull_request`, head `9add5e8a2122c5555c2403d5ea04073cfb2dc842`) → **conclusion success**.

```
PR Selected Checks   completed   success   (composite gate)
PR · Go unit · cli-0   completed success
PR · Go unit · cli-1   completed success   <- corrected gate tests (cli-1)
PR · Go unit · cli-2   completed success
PR · Go unit · cli-3   completed success
PR · Go unit · owner   completed success
PR · Go unit · packages completed success
PR · Validation · go-build  completed success
PR · Validation · go-vet    completed success
PR · Validation · cli-gofmt completed success
PR · Focused Python   completed success
```

No failures. Exact-head CLI shard (`cli-1`) runs the corrected gate tests and passes.

## REPO-RULE COMPLIANCE

- One PR (1650), one frozen commit on the exact head; gate logic in `internal/capability/perses_selection.go` NOT touched (confirmed `git diff --stat` empty). `.github/**` and `scripts/**` NOT touched.
- Write-set respected: only `app_status_result.go` (verified-only predicate + `identityDashboardBackendEligible`) + `app_status_perses_gate_test.go` (P1/P2/P5) + `perses_identity_witness.go` (P3) + its test. Catalog removed from the candidate (owner r8 decision).
- No subagent (§4.8), no `git add -A`. Single commit rebased onto develop, force-push only the unguarded lane branch.
- Own CI run watched to terminal (§4.6); run-id + conclusion at the exact frozen head.
- Freeze proof recorded (same SHA, develop ancestor) before publish; no acceptance on a moving head.
- CI rulesets remain disabled this cycle (see repo CI notes); live Required-Check enforcement is NOT claimed here — this is the `PR Selected Checks` composite success at the frozen head.

## cleanliness:
worktree clean at `9add5e8a2` (committed; single commit on develop). Catalog files deleted from tree; no stray artifacts.
