# CODEX-REVIEW — PR #1613 correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-alerts`
**Candidate:** `2dcbfebb88f73d539376debbf3477f6420eaceca`
**Base:** Perses seam lane; correction delta is one commit over previously reviewed `53300858e21f2625d53b766bf5c0fb6216af6c62`.
**Exact-head PR CI:** run [43812894758](https://github.com/mcpdev80/baseharbor/actions/runs/43812894758), `pull_request`, COMPLETED SUCCESS, exact candidate SHA. Draft source/routing, packages and CLI shards succeeded.
**Diff:** two files (`internal/metrics/perses_prometheus_alerts.go`, its tests); `git diff --check` clean. PR is open/draft.

## Verdict: REQUEST CHANGES

The r1 failure remains. `persesAlertValidatedRecipient` now requires Perses selection and a non-empty `release.PrometheusPluginVersion`, but that field pins the Prometheus datasource plugin; it does not prove a Prometheus rule evaluator exists or identify/validate a notification recipient. `persesAlertEvaluatorFromRelease` nevertheless sets `RecipientValidated: true` from those two declarations. `VerifyPersesAlertEvaluatorHealth` returns nil for that same selected/pinned manifest despite having no evaluator execution or notification-sender probe. The new “recipient absent” test passes an unselected manifest, so it does not test a selected surface with no recipient; the new positive health test blesses the pin-only state. This contradicts the r1 recipe and the card requirement for an actual evaluator and notification owner.

## Recipe / stop

- **File/change:** `internal/metrics/perses_prometheus_alerts.go`: do not treat `PrometheusPluginVersion` as a rule evaluator or recipient. Bind to an existing supported Prometheus rule-evaluation/persistence contract and a concrete validated notification owner/recipient, or return an explicit unavailable/not-enabled result with `RecipientValidated=false`.
- **Tests:** with Perses selected and datasource pin valid, assert evaluator-absent and recipient-absent both fail closed; assert health verification does not return nil without the actual supported evaluator/recipient path. Add a positive case only against that concrete path. Keep the unselected negative case.
- **Stop:** if no real evaluator or recipient contract is available, keep alerting unavailable; do not claim an evaluator or recipient from selection/plugin pins.

A separate same-SHA `workflow_dispatch` run 43814341275 failed broad runtime integration tests because the CI runtime setup could not install ORAS non-interactively. This is distinct from the successful requested PR run and does not alter the source finding. No merge.
