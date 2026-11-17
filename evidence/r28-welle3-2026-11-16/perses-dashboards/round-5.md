# 0428-082 · native Perses infrastructure dashboards — round-5 (Luna batch18 two unprovens)

Lane: flash worker (mission `/var/tmp/missions/mission-082-perses-dashboards-r5-luna2.md`).
Candidate base: `d2a9cd11d` (PR #1665, DRAFT, base `w083-perses-datasources`).
New commits this round: `081dc926d` (product-path hook + witness tests),
`dda073da4` (Target-root binding fix surfaced BY the cell iteration).
Remote witness: `git ls-remote origin refs/heads/lane-0428-082-perses-dashboards`
before push = `081dc926d…` (push #1 after `d2a9cd11d`), after push =
`dda073da4a495f61d2f754ae37a0262225f68df8` (push #2, fast-forward).

## PLAN checklist

1. [x] Mission + Luna batch18 recipe read (`batch18/act-luna-batch18.md` @ ea2ae684).
2. [x] Precedent study: how the Perses lines attach verification paths to the product (file:lines below).
3. [x] Hook builder/verifier into the intended product verification path (no second parallel resolver).
4. [x] Unit-layer real-`/api/v1/query` witness through the production probe path.
5. [~] Cell witness on baha-docker through the deploy path — best-current-state recorded; STOP per two-identical-fall rule, residual diagnosis below (candidate for a correction lane).
6. [x] pos/neg regressions kept; 080 tests byte-identical; build/vet/gofmt/readability green.
7. [x] Commit + refspec push + ls-remote witnesses; PR stays DRAFT (checked: state OPEN, draft true, base w083-perses-datasources).

## Proof (a): product caller — the status-JSON availability face

Precedent study (what the other dashboard lines actually did):

- 0428-077 (`lane-0428-077-r28-perses-dashboard-hosts`, PR #1602): the dashboard
  verdict surfaces on the product status path — `cmd/baha/app_status_result.go`
  :39 (field `host_containers_dashboards`), :152 (remote face) and :255 (local
  face) call `metricsprovider.PersesHostDashboardAvailability(...)`.
- 0428-076 (`perses-dashboard-databases-lane`, PR #1597): same shape —
  `cmd/baha/app_status_result.go` :39 (`database_dashboards`), :251
  `metricsprovider.PersesDashboardAvailability()`.
- 0428-075 seam: `cmd/baha/app_status_result.go` :143 computes
  `capability.PersesStatusNow(...)` before the remote early-return so BOTH faces
  carry it.
- Owner decision (selection akte `r28-welle2-2026-11-16/perses-dashboard-selection/luna-round-2.md`):
  positive Perses availability stays fail-closed/unavailable until the real
  signal path proves it; "Keine Verfuegbarkeit aus einem caller-supplied Status
  ableiten". The 078 resolver fan-in belongs to lane `lane-0428-078-perses-identity-on-resolver`
  (PR #1650) — this round adds NO second parallel resolver.
- Honest note on the #1608 datasources line: its `VerifyPersesPrometheusDatasourceHealth`
  (`internal/metrics/perses_prometheus_datasource.go:329` at base `8b00fe2c8`) ships with
  no cmd/baha caller either (diff of #1608 vs its base touches only
  `internal/metrics/perses_prometheus_datasource.go` + test + golden; verified by
  `git diff --name-only 66ff93d1 origin/pr1608`). The ESTABLISHED product hook
  pattern of this release line is therefore the status-JSON availability face
  (077/076), which 082 now follows — plus the real-query verifier that #1608's
  Luna-r1 recipe demanded.

082 implementation (candidate `dda073da4`):

- `internal/metrics/perses_infra_dashboards.go` — new entry
  `PersesInfraDashboardAvailability(ctx, m)` /
  `PersesInfraDashboardAvailabilityAt(ctx, m, dataDir, namespace)` (~:198..:245):
  runs `VerifyPersesInfraDashboardAt` (one real `/api/v1/query` per panel via
  `httpClientSeriesProbe` over the shared `queryUp`, `prometheus_verify.go:286`)
  and maps ONLY the observed verdicts to `available|unavailable` per panel;
  any error becomes every panel unavailable with the concrete reason. No
  caller-supplied status exists anywhere on this path.
- `cmd/baha/app_status_result.go` — the production caller: the new JSON face
  `infrastructure_dashboards` (:45 field) is computed BEFORE the remote-target
  early-return (:159) from the resolved Target's provider root
  (`resolved.TargetStateRoot`, `resolved.Target.Name`) and lands on BOTH the
  remote face (:166) and the local face (:253).
- `internal/metrics/perses_prometheus_datasource.go` — Target-bound plumbing
  (`persesPrometheusDatasourceEndpointAt`, `persesPrometheusDatasourceSourcesAt`,
  `buildPersesPrometheusDatasourceAt`); the default forms delegate with empty
  bindings, no behavior change for single-root state.

Regression proof of the caller:

- `cmd/baha/app_perses_infra_dashboards_cli_test.go` (new): runs the GENUINE
  `baha status --json` command path via `runWithIO` (precedent of
  `app_perses_cli_test.go`/077 CLI face): all four panels exposed with the
  two-verdict contract, fail-closed unavailable with concrete reason without
  materialized provider state; face omitted entirely when the observability
  surface is not selected. PASS.
- `internal/metrics/perses_infra_dashboards_test.go` —
  `TestPersesInfraDashboardAvailabilityProductEntry` (face completeness +
  fail-closed + unselected=nil) and
  `TestPersesInfraDashboardAvailabilityAtTargetRoot` (the target-root binding
  `dda073da4` added after the cell diagnosis: provider state read from
  `targets/<name>` root, default root fails closed separately). PASS.

## Proof (b): real /api/v1/query witness

Unit layer (green, deterministic, CI-captured):

- `TestPersesInfraDashboardVerifiesOverRealHTTPPath`
  (`internal/metrics/perses_infra_dashboards_test.go`, ~:700..:800): the
  production probe `httpClientSeriesProbe` → `queryUp` performs REAL HTTPS
  round trips against a series-filtering endpoint (`httptest.NewTLSServer`,
  Prometheus list-syntax matcher semantics in `persesQueryMatchesSeries`);
  asserts (1) exactly one wire query per panel (`asked == 4`, queries equal the
  recorded `res.Signals[i].Query`), (2) rows present → panels filled, (3) an
  untrusted transport keeps every panel the visible gap (never a failed build,
  never a silent 0), (4) the product availability face over PKI-less state
  fails closed explicitly.
  Query-value note: the wire comparison runs against the decoded
  `r.URL.Query().Get("query")` value; `queryUp` URL-encodes it
  (`values.Encode`, `prometheus_verify.go:287-288`).
- Value-semantics finding (recorded honestly): `queryUp` returns true only for
  a sample whose value is `"1"` (`prometheus_verify.go:317-319`). The panels
  therefore fill on present-with-value-1 rows; a present-but-other-value row
  keeps the panel as the gap. The unit witness fixtures answer "1" per series.
  This is the same reading the datasource line uses; it is NOT a gap in proof
  (a scrape series with the value observed returning rows is what "answered"
  means there), but a correction lane may want to broaden it.

Cell layer (best-current-state, NOT yet green — this is the open item):

- Zone: `baha-docker:~/lanes/w082-r5` (rootless docker 29.8.1, ORAS 1.3.6, clone
  checked out at the exact SHA under test). Script: `scripts/cell-witness.sh`
  (this directory).
- What the cell DID prove, at `dda073da4`:
  - the deploy path ran end-to-end: `baha target create w082r5-ci-<epoch>` +
    `baha up --control-plane-only --yes` (Core READY), app `compose.yaml` +
    `baseharbor.yaml` (metrics source `application/api:8080/metrics`,
    observability management_ui + perses), `baha app apply` through BOTH consent
    gates — impact-ack via pty (`script(1)`, terminal-bound by
    `readerIsTerminal`) and candidate consent via the printed digest
    `--confirm-candidate <sha256>` — then `baha app up`:
    `READY shared/prometheus https://metrics.baha.localhost:18443`,
    `RUNNING application`. Prometheus containers live:
    `bh-w082r5-ci-<epoch>-shared-prometheus-1-1` (`prom/prometheus:v3.14.0`) +
    caddy access.
  - provider materialized at the TARGET root
    `state/targets/w082r5-ci-<epoch>/providers/prometheus/shared/` (runtime.env,
    compose.yaml, service-access PKI ca.pem files) — which is what surfaced the
    real product-path defect fixed in `dda073da4` (the face read the default
    root only; every earlier cell fall "no materialized Prometheus provider"
    was that bug, NOT a witness-harness artifact).
  - remaining fall, twice identically (runs 25/26 at `dda073da4` and re-confirmed
    28): the retained snapshot at
    `state/targets/<boot>/providers/prometheus/shared/runtime-sources.json`
    reads `{"...","sources":[]}` (127 bytes, empty) → fail-closed
    "no materialized Prometheus sources". The scrape-targets dir/file listing
    in `state.out` (script now captures it) shows the application source was
    NOT registered by the deploy for this repository-shape app.
  - diagnosis lead for the correction lane: the cell app has NO declared
    services (workload-only) — compare `VerifyProviderSourcesAt`'s
    `observability.ListMetrics(placement, allowedApplications, …)`
    (`prometheus_verify.go:117-150`): a workload-only dev app may leave the
    provider source registration empty; the mission's own `WithMetricsSource`
    manifest shape was exercised through the unit layer, not the full deploy
    fan-in. This is either a genuine product gap (deploy does not materialize
    an app metrics source into the shared provider snapshot) or a manifest
    shape the deploy path requires (e.g. an app SQL/metrics binding, or a
    `metrics.sources` name class). It needs the fan-in owner's view, NOT
    another blind cycle here.
- Luna qualification rule honored: NO further hosted runs were launched against
  the known 6-failure runtime set (that set was classified dispatch-context /
  cell-property in round-4; the substitute qualification stands for those
  unrelated fails only; acceptance point (b) is NOT claimed by them).
- STOP per mission/codex rule ("zwei erfolglose identische Korrekturen →
  Strategiewechsel": runs 26 and 28 fell with the identical
  `sources:[]` verdict): cycle 4 was NOT run; finding + file:line recorded
  instead. Context budget per coordinator Mahnung ended the cell iteration.

## Local verification (candidate dda073da4)

- `go build ./...` PASS; `go vet ./...` PASS; `gofmt -l cmd internal` empty.
- `go test ./internal/metrics` PASS (all 14 `TestPersesInfraDashboard*` cells
  incl. the two new face tests + real-HTTP-path witness, TMPDIR under /var/tmp).
- `go test ./internal/capability` PASS; `go test -run 'TestPersesInfra|TestBahaStatus' ./cmd/baha` PASS.
- `bash scripts/source-readability-audit.sh` PASS (size/span/ratchet).
- 0428-080 selection files byte-identical to `d2a9cd11d` (`diff -q` on
  `internal/capability/perses_selection{,_test}.go`); pos/neg dashboard
  regressions untouched; `internal/metrics/prometheus_integration_test.go`
  stray edit REVERTED (diff-clean).
- CI capture: all new tests live in `internal/metrics` + `cmd/baha` packages,
  discovered and executed by the existing ci.yml package job
  (`go test ./contracts/... ./internal/... ./spec/...`, ci.yml:124 on develop)
  and the CLI shards; the cell-witness file is build-tagged
  `perses_infra_cell` and NOT part of any CI package run (test-host rule: cell
  runs stay on named hosts; it is an evidence driver, kept out of the shipped
  default build; per mission the script lives in this evidence dir).
- Hosted exact-head CI for `dda073da4`: still gated by the documented
  PR-run allowlist doorstop (rounds 3/4 finding, TRIAGE); no new hosted run
  launched per the dispatch-discipline rule.

## Cell hygiene

- Teardown at script end: `baha app destroy` + `baha destroy` with the zone's
  state/config/target, then name-scoped `docker rm -f` for `*w082r5*`,
  `w082r5`-networks, `w082r5`-volumes.
- cleanliness: after the final run, `baha-docker` shows
  containers=0 (before: 0), zone-local config/state removed with the zone;
  no ambient `local`/core-shared resources were touched (the zone always ran
  with `XDG_CONFIG_HOME=$ZONE/config` + `BASEHARBOR_STATE_DIR=$ZONE/state`).

## Handoff

- Product commits: `081dc926d`, `dda073da4` on `lane-0428-082-perses-dashboards` (PR #1665 stays DRAFT, base unchanged).
- Open for a correction lane: cell witness (b) — make the deploy path register
  the application metrics source into the shared provider snapshot
  (`runtime-sources.json sources:[…]` non-empty for the cell app shape), then
  re-run `scripts/cell-witness.sh` (it is self-contained: it copies
  `cellwitness_test.go` into the repo tree at the exact SHA and drives the full
  deploy → product-path verify with teardown). The unit-layer real-round-trip
  witness is already green and CI-captured; the product hook and its Target-root
  binding are merged-ready independent of that last mile.
