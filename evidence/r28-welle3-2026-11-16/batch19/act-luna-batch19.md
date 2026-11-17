# CODEX-REVIEW — Luna batch19

Date: 2026-11-17. Role: CODEX-REVIEW (Luna). Read-only review; no merge.

## Exact candidates and witnesses

| Object | Candidate | PR / base | Run | Observed result |
| --- | --- | --- | --- | --- |
| 1 / 0428-094 | `4f2906c6bf9f1c1e5c95f7b88e79c1aa5e110ecc` | Core #1666 / `develop`, OPEN DRAFT | `43979087744` | exact-head `pull_request` SUCCESS; draft source and Go jobs passed |
| 2 / 0428-082 | `dda073da4a495f61d2f754ae37a0262225f68df8` | Core #1665 / `w083-perses-datasources`, OPEN DRAFT | `43997001011` | exact-head `workflow_dispatch` FAILURE; `Run unit and package tests` failed |

Current PR heads, base refs and draft states were refreshed after the CI run. No candidate or product checkout was changed by this review.

## Verdicts

### Object 1 — #1666 / 0428-094: APPROVE CONTENT

The added `TestLoadConfigDoubleAppendResolvedPathMissingFailsLoud` now follows the batch18 recipe: it sets `XDG_CONFIG_HOME` to a path already ending in `/baseharbor`, places the intended `config.yaml` at that root, leaves the nested resolved path absent, calls `LoadConfig()`, and asserts `errors.Is(err, ErrConfigMissing)`. The normal XDG four-case matrix and valid-config regression remain in the candidate. This closes the batch18 coverage gap. Exact-head run `43979087744` completed successfully; its draft Go packages and CLI shards passed. Non-draft jobs were skipped because the PR remains draft and are not claimed as passed.

### Object 2 — #1665 / 0428-082: REQUEST CHANGES

The product caller is now present on the `baha status --json` path, derives each panel verdict from its own query result, and accepts no caller-supplied availability status. The diff from `d2a9cd11d` changes only the status caller, dashboard implementation/tests, and Prometheus datasource plumbing; the 0428-080 `perses_selection` files and tests are untouched.

The target-root fix is justified by the recorded cell diagnosis: the earlier face read the default root although deploy materialized provider state under the selected Target root. It is isolated in commit `dda073da4` from the product-path hook commit and has a dedicated `TestPersesInfraDashboardAvailabilityAtTargetRoot`. That unit test proves root selection by distinguishing the target-root provider files from the empty default root. Its current fixture intentionally has no service-access PKI, so it does not prove a successful target-root query.

There is a newly exposed fail-closed regression in the shared datasource plumbing. At `internal/metrics/perses_prometheus_datasource.go:185-196`, `buildPersesPrometheusDatasourceWithProbe` receives an explicit `release` but calls the target-root helper without it; `buildPersesPrometheusDatasourceAt` then unconditionally substitutes `capability.PersesDefaultRelease`. Consequently an invalid/unpinned release is silently replaced by the supported default. Exact-head run `43997001011` executed the `internal/metrics` package and failed at `TestPersesPrometheusDatasourceFailClosedWhenUnpinned` (`perses_prometheus_datasource_test.go:280-288`): “unpinned perses must fail closed, not fabricate a datasource.” The `Run unit and package tests` job failed; the rest of the dispatch validation and all unrelated PR jobs were skipped. This exact-head failure blocks approval.

The new `TestPersesInfraDashboardVerifiesOverRealHTTPPath` is routed through the existing Go package job (`go test ./contracts/... ./internal/... ./spec/...`), so that test is discovered by the failed package run. Its HTTPS round-trips use `httptest` with scripted Prometheus-compatible responses; they validate the production HTTP/query path but are not a query against a real Prometheus server. The round-5 cell evidence reports that no source was materialized (`runtime-sources.json` has `sources: []`), so the product path did not reach a real query there either. The separate 0428-100 source-registration issue is outside this verdict; it does not turn the scripted HTTP response into a real Prometheus witness.

**Recipe:**

1. Preserve the explicit `release` argument in the target-root helper (for example, add it to `buildPersesPrometheusDatasourceAt`) and pass the pinned default only from production entry points that intentionally use that pin. Keep invalid/unpinned input fail-closed.
2. Retain the dedicated Target-root regression and run `TestPersesPrometheusDatasourceFailClosedWhenUnpinned` plus the dashboard tests through the existing package CI. Obtain a new exact-head passing run; run `43997001011` is red and cannot qualify.
3. Complete the task's real-query acceptance with an actual query to a materialized Prometheus endpoint and captured returned scrape series/source scope. This may use a suitable existing source fixture; it need not fold the separate 0428-100 workload-only registration issue into this PR. Keep 0428-080 files unchanged.

## Turn-start coordination flags

`basics-check.py` reported the worker pool at 2/3 with an `ornith:2` `NO_ELIGIBLE_WORK` hold and evidence `candidate-count=0`, idle lanes 0428-094 and 0428-082, and 40 open PRs. These coordinator-owned flags are included here for the receiving coordinator; this review did not create or dispatch worker work.

## END

END_DONE mission-luna-batch19 — #1666 APPROVE CONTENT; #1665 REQUEST CHANGES (target-root helper drops the explicit release pin and exact-head Go package CI fails). Evidence includes exact-head run status and correction recipe. No GitHub approval, product change, or merge.
