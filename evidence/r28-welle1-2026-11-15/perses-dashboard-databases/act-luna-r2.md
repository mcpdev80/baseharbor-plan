# CODEX-REVIEW — PR #1597, correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-dashboard-databases`
**Candidate:** `7c4db737f3a3f10d5b0620e72ca3c88367e49029`
**Exact-head CI:** run `43805823564`, `pull_request`, COMPLETED SUCCESS, exact SHA.
**Base:** selection lane; correction evidence is `round-2.md`. Three files changed in this round; `git diff --check` clean.

## Verdict: REQUEST CHANGES

The invalid trailing bare `up` token was removed, but the replacement PromQL string in `internal/metrics/perses_dashboards.go` also removes the selector's closing `}`. The golden now contains `up{job="...",baseharbor_environment="$env"` with no closing brace, which is still invalid PromQL. The new `assertValidPromQL` test is a string-shape heuristic, not the Prometheus parser described in the correction evidence; it explicitly permits a query ending with a quote and no `}`. Its negative test only checks its own comma-split precondition and never calls the validator on the invalid query.

## Recipe

- **File/change:** `internal/metrics/perses_dashboards.go` and `internal/metrics/testdata/perses-dashboards/prometheus-targets.json`; restore the closing `}` after the final label matcher.
- **Tests:** use the Prometheus PromQL parser in `TestPersesDashboardQueriesAreValidPromQL` to parse every emitted PromQL expression. Make the negative test call the same parser with both the old trailing-token query and the missing-brace query and assert both fail. Keep the valid query positive case. Route the test through package CI and obtain a new exact-head green run.
- **Stop:** stop if the parser dependency is not available through the existing test setup; do not substitute a heuristic that accepts malformed selectors.

The selection dependency remains not accepted; this content review does not accept that dependency or authorize merge.

Read-only review; no merge performed.
