# CODEX-REVIEW — PR #1597 correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-dashboard-databases`
**Candidate:** `540ed13cec363a231241a17baa68c8d32ebdae63`
**Exact-head CI:** run `43810693985`, `pull_request`, COMPLETED SUCCESS, exact candidate SHA. The active Draft source/routing, packages, and CLI shards succeeded; the tagged real-parser test was not selected by this run.
**Reviewed delta:** parent `7c4db737f3a3f10d5b0620e72ca3c88367e49029` → candidate; six files, `git diff --check` clean. PR #1597 remains open/draft.

## Verdict: REQUEST CHANGES — CI routing only

The query fix closes the emitted `up{...}` selector. The local evidence in `round-3.md` records that the `promqlparser`-tagged real Prometheus parser test passes and rejects both the old malformed selector and a missing closing brace. I accept that as local content evidence, per the mission clarification.

The hosted exact-head run exercises the default heuristic path, but does not run `perses_dashboards_promql_test.go`: that file requires `-tags promqlparser`. The card requires every changed test to route through and execute in GitHub CI. The lane evidence itself says `.github/workflows/ci.yml:124` is the required Owner-scope route and was not changed. Thus the source correction is sound, but required durable test evidence is absent.

## Recipe / stop

- **Owner-scope change:** in `.github/workflows/ci.yml` at the metrics test invocation (currently line 124), add `-tags promqlparser` or add a focused job that runs `go test ./internal/metrics/ -tags promqlparser -run 'TestPersesPrometheusParserRejectsMalformedSelectors|TestPersesDashboardQueriesAreValidPromQL'`.
- **Required check:** run the changed parser test on the exact resulting candidate SHA; record the triggering check and result. Keep the default CI coverage as well.
- **Stop:** do not accept the card or treat the local parser run / current green Draft shards as satisfying CI routing. No product changes made by this review; no merge.

Read-only, SHA-exact review. Local parser evidence is recognized; acceptance remains gated on the Owner CI route and exact-head execution.
