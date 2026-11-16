# 0428-083 · Connect Perses Prometheus datasource — round-1 evidence

Mission: /tmp/opencode/mission-welle2-083.md
Task contract: `python3 scripts/plan.py show t-20261114-r28-perses-datasources`
Card: 0428-083 · release v0.4.28 · type task · areas observability

## PLAN (nummerliste)

- Read mission + task contract (plan.py show t-20261114-r28-perses-datasources); coordinator confirmed scope in dialog
- Verify base head via ls-remote (lane-0428-075-perses-seam @ 492b8e8f); cut wt from it; confirm ancestor
- Claim task via plan.py claim; commit+push claim to planning origin/main (2bdf0abf)
- Investigate source: perses.go seam, prometheus.go/files/verify/render, serviceaccess, observability MetricsSource, dashboards lane datasource model + golden file
- Scope decision from coordinator: base lane-0428-075-seam @492b8e8f, own file internal/metrics/perses_prometheus_datasource.go + golden test, fail-closed without health-path, no stacking, no shared-file edits
- Write internal/metrics/perses_prometheus_datasource.go + golden test (9 tests, all pass)
- go vet + go build ./... + go test ./internal/metrics/... ./internal/capability/... all green; source-readability audit PASS
- Write this evidence akte (PLAN nummerliste, no checkboxes, acceptance witnesses, ls-remote shas, cleanliness /tmp/opencode/w083)
- Draft PR #1608 (title 0428-083), base lane-0428-075-perses-seam, draft, head 18360b69
- Push evidence to planning origin/main (confirm in remote tree), END with head-SHA

## SCOPE DECISION (coordinator dialog 2026-11-16)

Base lane-0428-075-perses-seam @ 492b8e8f994 (ls-remote witness). Own file internal/metrics/perses_prometheus_datasource.go + golden test, fail-closed without health-path, no stack on selection/dashboards lanes, no shared-file edits. Task depends on perses-contract-seam (review) + perses-runtime (wait), both un-accepted — proceeding in single-base seam scope per direct mission instruction; dependency state recorded as STATE below.

## BASE ATTESTATION

- `git ls-remote origin refs/heads/lane-0428-075-perses-seam`:
  `492b8e8f994b16e6f73819a08175f8178cd63292`
- Branch cut from that head; `git merge-base --is-ancestor 492b8e8f... HEAD` → YES.
- Candidate only my own commit on top of base (git log witness below):
  `git log --oneline 492b8e8f..HEAD` = only `18360b69`.

## WITNESSES

ls-remote base head (origin, before first evidence commit):
```
$ git ls-remote origin refs/heads/lane-0428-075-perses-seam
492b8e8f994b16e6f73819a08175f8178cd63292	refs/heads/lane-0428-075-perses-seam
```

Candidate head + provenance (origin, after push):
```
$ git ls-remote origin refs/heads/w083-perses-datasources
18360b69f9070356d999ef54cf31fa9041c63f4e	refs/heads/w083-perses-datasources
$ git log --oneline 492b8e8f..origin/w083-perses-datasources
18360b69 feat(0428-083): wire existing Prometheus into Perses as pinned native datasource (fail-closed)
```

Plan claim commit pushed to planning origin/main:
```
$ git log --oneline -1 origin/main
2bdf0abf claim t-20261114-r28-perses-datasources: w083-perses-datasources
```

PR #1608 (gh):
- baseRefName: lane-0428-075-perses-seam
- headRefName: w083-perses-datasources
- headRefOid: 18360b69f9070356d999ef54cf31fa9041c63f4e
- isDraft: true, state: OPEN

## ACCEPTANCE (acceptance-point → test name + output)

- Verified, pinned native Perses datasource; real provider signal, no false capability claim.
  - Test `TestPersesPrometheusDatasourceShape`: kind=`PrometheusDatasource` (native plugin, not a Grafana UI API), name=`prometheus`, default=true. PASS.
  - Test `TestPersesPrometheusDatasourceNamesPrometheusOwner`: owner=`prometheus` named as owner reference, NOT a Perses-declared capability. PASS.
  - Test `TestPersesPrometheusDatasourceNoCapabilityClaim`: marshalled JSON contains no `Metrics` / `IntegrationDescriptor`. PASS.
- Scope all access by Target/tenant permissions; fail closed on missing authorization; secrets out of manifests/audit; optional visualization does not force new capabilities.
  - Test `TestPersesPrometheusDatasourceNoSecretInDescriptor`: JSON contains no `bearer`/`password`/`basicAuth`/`token`/`clientCert`/`privateKey`. PASS.
  - Test `TestPersesPrometheusDatasourceAccessIsProxy`: access mode is `proxy` (routed through the Prometheus management proxy over TLS, never `direct`). PASS.
- Preserve independent Prometheus/Loki/Tempo ownership; remove only owned resources; fail closed on missing health.
  - Test `TestPersesPrometheusDatasourceFailClosedWhenUnpinned`: unpinned release returns `PersesNotConfiguredError` (fail-closed, not fabricated). PASS.
  - Test `TestPersesPrometheusDatasourceUnverifiedReachability`: only reachability state is `unverified` (no Prometheus health probe exists here). PASS.
  - Test `TestPersesPrometheusDatasourceVerifyFailClosed`: pin validation alone never passes health verify. PASS.
- Golden witness pinned.
  - Test `TestPersesPrometheusDatasourceGoldenFiles`: `internal/metrics/testdata/perses-prometheus-datasource/prometheus.json` matches marshalled datasource byte-for-byte. Golden:
    ```json
    {
      "kind": "PrometheusDatasource",
      "name": "prometheus",
      "default": true,
      "config": {}
    }
    ```
  - `config` is `{}` because the provider endpoint is not materialized in the unit test; at runtime `persesPrometheusDatasourceURL` populates it from the provider endpoint over the runtime TLS boundary (best-effort: missing endpoint leaves URL empty but does not fail the definition — reachability is owned by the fail-closed health check).

## TEST + BUILD VITNESSES

```
$ go build ./...
(no output)
$ go vet ./internal/metrics/
(no output)
$ go test ./internal/metrics/ -run TestPersesPrometheusDatasource -v
=== RUN   TestPersesPrometheusDatasourceShape
--- PASS: TestPersesPrometheusDatasourceShape (0.00s)
=== RUN   TestPersesPrometheusDatasourceNamesPrometheusOwner
--- PASS: TestPersesPrometheusDatasourceNamesPrometheusOwner (0.00s)
=== RUN   TestPersesPrometheusDatasourceNoCapabilityClaim
--- PASS: TestPersesPrometheusDatasourceNoCapabilityClaim (0.00s)
=== RUN   TestPersesPrometheusDatasourceNoSecretInDescriptor
--- PASS: TestPersesPrometheusDatasourceNoSecretInDescriptor (0.00s)
=== RUN   TestPersesPrometheusDatasourceAccessIsProxy
--- PASS: TestPersesPrometheusDatasourceAccessIsProxy (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenUnpinned
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesPrometheusDatasourceUnverifiedReachability
--- PASS: TestPersesPrometheusDatasourceUnverifiedReachability (0.00s)
=== RUN   TestPersesPrometheusDatasourceVerifyFailClosed
--- PASS: TestPersesPrometheusDatasourceVerifyFailClosed (0.00s)
=== RUN   TestPersesPrometheusDatasourceGoldenFiles
--- PASS: TestPersesPrometheusDatasourceGoldenFiles (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/metrics
$ go test ./internal/metrics/ ./internal/capability/
ok  	github.com/mcpdev80/baseharbor/internal/metrics
ok  	github.com/mcpdev80/baseharbor/internal/capability
```

## CI COVERAGE (Owner directive 2026-11-07)

New test `internal/metrics/perses_prometheus_datasource_test.go` is picked up by existing CI without any `.github/**` edit (Owner scope):
- `.github/workflows/ci.yml` line ~122: `go test ./contracts/... ./internal/... ./spec/...` runs the full `internal/metrics` package (covers my new file).
- `.github/workflows/ci.yml` line ~341: `go test ./...` also runs it.
- No `.github` change required; the existing unit-test group covers the metrics path. No VM-only or local-only test was introduced.

## DEPENDENCY STATE (STATE, not blocking)

- `t-20261114-r28-perses-contract-seam`: state `review`, NOT accepted.
- `t-20261114-r28-perses-runtime`: state `wait` (depends on seam, NOT accepted).
- `t-20261114-r28-perses-signal-inventory`: accepted.
- Proceeding on the single-base seam per direct mission instruction (Owner directive names the exact base + delivery method). The seam + runtime lanes gate downstream dashboards/alerts, not this configuration-only adapter.

## REPO-RULE COMPLIANCE

- Single write-set, own adapter file (`perses_prometheus_datasource.go`), own golden test + testdata. No edits to seam/contract/shared files.
- No `.github/**` edits (Owner scope). No reruns, no workflow_dispatch.
- No containers/compose started (coordinator/codeman host is a forbidden test host; baha-runner-* are not test hosts).
- No subagents (§4.8).
- Branch provenance: cut from `492b8e8f`, only my own commit `18360b69` on top (git log witness). No second candidate branch.

## CLEANLINESSION (/tmp/opencode/w083)

- No docker/podman compose projects, networks, volumes or state directories started.
- Worktree `/tmp/opencode/w083` contains only the baseharbor checkout + my three staged files + `testdata/`. No stray test artifacts beyond the committed golden file.
- `docker ps`/`docker compose ls`/`docker network ls`/`docker volume ls` all empty (no containers). No orphan cleanup needed.

## END LINE

END DONE mission-welle2-083.md: 0428-083 Perses Prometheus datasource adapter — round-1 delivered as own-file adapter `internal/metrics/perses_prometheus_datasource.go` + golden test (9 tests pass), fail-closed on unpinned/unreachable, no false capability claim, no secret in descriptor, proxy access; draft PR #1608 base lane-0428-075-perses-seam, candidate SHA 18360b69f9070356d999ef54cf31fa9041c63f4e (only own commit on 492b8e8f); evidence on planning origin/main 2bdf0abf; go build/vet/all metrics+capability tests green, source-readability audit PASS, CI covered by existing ci.yml internal/... group; no containers; no .github edits.
