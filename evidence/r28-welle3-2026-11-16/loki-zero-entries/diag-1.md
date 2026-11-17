# DIAGNOSIS AKTE 0428-113 — Docker Loki `total_entries=0` (prometheus/workload `up` series query)

- **Card / mission:** t-20261117-docker-loki-ingestion-timeout (0428-113) / mission-113-lokidiag
- **Author / model:** agentgateway/worker-ornith1.5 (self-run, no subagents)
- **Date:** 2026-11-17
- **Type:** DIAGNOSE only — no product change. Findings point to an owned, already-open candidate.

## 1. Reality attestation (remote truth via `git ls-remote`)

- Planning repo (authoritative): `origin/main` = `58a4e06ae7655beb0f66e700d01ab96468c0ea7d`
  (`git ls-remote origin main`, at /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan).
- baseharbor product repo remote HEAD (via lane-origin, the live pin):
  - `git ls-remote lane-origin develop` -> `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`
  - `git ls-remote lane-origin main` -> `c000c5db2560c471fe84842136e03d6e54d96779`
- PR #1677 head: `git ls-remote origin refs/pull/1677/head` -> `36bb9019654e5db150928614a6e5892b6c1a365b`
  (lane `lane-0428-102-app-class-signal-registry`, base `origin/develop`).
- Candidate SHA under test (from run + mission + card): `d144945af13641e5bdb1564f77b807b2d52b81cb`
  (PR #1677 commit 3 of 5, "test(observability): update registry list call sites").
- Parent of PR #1677 (i.e. develop at merge base, `pr1677-head~5`) used as the develop baseline for all diffs below.
- Card state (local planning checkout, NOT the workers/ phantom copy): `kanban_status: planned`, release v0.4.28, unassigned, handoff note says "ZWEIFEL — queued for an independent lane; do not attribute to #102 without evidence."
- Ancestry: develop SHA `62eaea2c8` is the base the PR targets; the PR's own merge commit `36bb9019` contains it (verified via `git log` in the fetched `pr1677-head` ref; the diff was computed as `origin/develop...pr1677-head`).

## 2. Reproduced selector path (source-only; no container needed)

The failing selector is the metrics `up` series query the Prometheus driver issues during `Verify` (app-acceptance gate):

- `internal/metrics/prometheus.go:345` (develop, `origin/develop`):
  `up{job="baseharbor-applications",baseharbor_application=%q,baseharbor_environment=%q,baseharbor_source=%q}`
  gated by `queryUp(...)` at line 354, 45s deadline -> `context deadline exceeded` at 47.2s on retry 2 (run 44051420634 / 44049176474).
- This query is served from Prometheus scrape target files under `job=baseharbor-applications`. The scrape config for that job is rendered from **registration target files** (`prometheus_files.go` / `prometheus_render.go`), not from the observability registry. So the *scrape* side and the *registry* side are independent.
- The `total_entries=0` result means: Prometheus returned HTTP 200 (healthy target list) but the `up` query matched zero series for the `(application, environment, source)` tuple. The query is correct; no series exist for that tuple.

## 3. Root cause — class=application metrics never written to the observability signal registry (registration side)

Two independent, mutually-consistent defects on the registration side at `d144945...` / develop:

1. **`internal/metrics/realization.go` `runtimePrometheusRealization.RegisterTarget` returns `nil`** (develop).
   - develop (`origin/develop`), end of `RegisterTarget`: `return nil`.
   - The PR adds, instead of `return nil`:
     `return observability.Update(observability.MetricsSource{ ID: observability.ApplicationMetricsSourceID(...), Class: observability.SourceApplication, Scope: capability.ScopeApplication, ... })`
   - Consequence in develop: on `app apply -> ProvisionAndBind`, `driver.Bind -> RegisterTarget` writes the Prometheus target *file* (so the `baseharbor-applications` scrape job has the target) but **never inserts the class=application source into the observability signal registry**. `git grep` confirms the develop `internal/metrics` tree has **zero** references to `observability.Update` / `ApplicationMetricsSourceID`. The registry write is entirely absent.

2. **`internal/observability/registry.go` `List()` drops `SourceApplication`** (develop), line 409:
   ```go
   case SourceApplication:
       continue
   ```
   - `ListMetrics(..., includeApplicationProviders, includePlatformProviders)` only ever passes provider flags; it never requests `SourceApplication`, and even a caller that did would be filtered out at the switch. So `observability.ListMetrics` can never return the class=application source — the verify/`prometheus_verify.go` path that reads `ListMetrics` (line 141) therefore sees **0 application-class sources** and asserts nothing for them.

Both facts converge on the **registration/source-availability side**, not the query side.

## 4. Why the query side is NOT the bug (rules out #1616 Loki-source as cause)

- The Loki `up`/series query path that fails is the **Prometheus** driver's `verifyApplicationSourcesAt` (`prometheus.go:345`), which queries Prometheus `up` series — a Prometheus-side scrape/series gap, not a Loki read path.
- PR #1616 (0428-086 Perses Loki datasource read path, `internal/logs/loki_datasource.go`, head `7d6538b45`, still open/draft) is a **separate** concern: it reads Loki logs for the Perses management UI. It does not touch the Prometheus `up` series query or the class=application metrics registry path. It is not the owner of this failure. The gate that timed out is `internal/metrics/prometheus.go` + `app_observability_acceptance_test.go`, owned by the 0428-102 candidate.

## 5. Fix owner (which PR heals this)

- The heal is **PR #1677 (0428-102), head `36bb901965`, base `origin/develop`**. It:
  - registers the class=application Prometheus source into the registry in `RegisterTarget` (realization.go),
  - threads `includeApplicationSources` through `List` and stops `List()` from silently dropping `SourceApplication`,
  - adds `ListApplicationMetrics`, `ApplicationMetricsSourceID`, `PruneApplicationMetrics`,
  - makes `verifyProviderSourcesAt` query `up{job="baseharbor-applications",...}` for application sources (the exact selector from `prometheus.go:345`), and
  - preserves the workload-only verification no-op.
- The mission's "0428-102 snapshot-only-flow (102/100)" is consistent: in the current develop snapshot, the class=application registration step is the missing link; the PR closes it.

## 6. Verdict (per mission)

- The source of the `total_entries=0` failure is **attributable to an owned, already-open candidate: PR #1677 (0428-102), head `36bb9019654e5db150928614a6e5892b6c1a365b`, base `origin/develop`**.
- Per mission instruction (3): **NO product change.** The diagnosis akte IS the deliverable. The fix is the open candidate; making it pass (and Docker gate green) is that candidate's lane, not this diagnostics lane.
- If, contrary to this evidence, the cause were unattributable, the sanctioned move would be a tiny own-PR regression that fails before / passes after the fix preserving the consent negative — but that precondition does not hold here.

## 7. Scope / compliance

- No product file edited. No `.github/**` touched. No container/compose started (no docker/podman run; pure source forensics). No evidence path written into a product repo (this akte lives only in baseharbor-plan evidence/).
- Branch provenance: diagnosis done against the fetched read-only ref `pr1677-head` and `origin/develop` (live pin via `lane-origin`); no branch cut, no commits made.

## 8. Evidence witnesses

- `git ls-remote origin main` (planning) -> `58a4e06ae7655beb0f66e700d01ab96468c0ea7d`
- `git ls-remote lane-origin develop` -> `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`
- `git ls-remote origin refs/pull/1677/head` -> `36bb9019654e5db150928614a6e5892b6c1a365b`
- Candidate SHA under test: `d144945af13641e5bdb1564f77b807b2d52b81cb`
- Evidence akte path on origin/main (commit `49c976ad84ed0f5994aae977b7b91e63b70441e6`): `evidence/r28-welle3-2026-11-16/loki-zero-entries/diag-1.md` (origin/main before END = `58a4e06ae7655beb0f66e700d01ab96468c0ea7d`; after my rebased push = `49c976ad84ed0f5994aae977b7b91e63b70441e6`, only my commit on top of `1ad37129`).
- Run: 44051420634 / 44049176474, Docker observability gate, Loki/prometheus workload `up` series, 200 but total_entries=0, context deadline exceeded after 47.2s retry 2.

## END: mission-113-lokidiag DONE
