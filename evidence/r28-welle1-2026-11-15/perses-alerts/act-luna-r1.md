# CODEX-REVIEW — PR #1613

**ROLLE: REVIEW**
**Task:** t-20261114-r28-perses-alerts
**Candidate:** 53300858e21f2625d53b766bf5c0fb6216af6c62
**Base:** Perses seam 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08; head merges the seam into recovered alert candidate 9e897b5f5e037a5afc0a2d20f4058a1dd4d580bc. The correction from round 2 is a gofmt-only change.
**Exact-head CI:** run 43794278593, pull_request, COMPLETED SUCCESS, exact SHA; Draft source/routing, CLI shards 0–3, and packages passed. Native/release jobs were skipped under draft selection. git diff --check clean.

## Verdict: REQUEST CHANGES

The implementation invents "PrometheusRuleEvaluator" as a real evaluator based only on the non-empty Prometheus datasource plugin pin. persesAlertValidatedRecipient returns true merely when Perses is selected; no recipient is identified or validated. BuildPersesAlertEvaluator then returns RecipientValidated: true and configured_unverified, despite the card requiring a real evaluator and notification owner contract. Most directly, VerifyPersesAlertEvaluatorHealth returns nil after pin validation alone, even when the surface is unselected and no evaluator or recipient exists; this contradicts the function's fail-closed contract. The green package test accepts this result, so it is not evidence of the required negative behavior.

## Recipe

- **File/change:** internal/metrics/perses_prometheus_alerts.go; remove the fabricated evaluator/recipient claims. If no supported rule evaluator and validated recipient contract exists, return an explicit not-enabled/unavailable result and make verification fail closed. If an existing Prometheus rule path is supported, bind to that real contract and validate an actual recipient without storing secrets.
- **Tests:** assert the health verifier rejects pin-only, unselected, evaluator-absent, and recipient-absent cases; assert no result claims RecipientValidated without concrete validation evidence. Add a positive test only against the actual supported rule/persistence path. Route the tests through CI and obtain a new exact-head run.
- **Stop:** stop if the real evaluator or recipient owner is not defined; do not treat datasource pin or Perses selection as either proof.

The datasource dependency is still unaccepted. This review does not accept it or authorize merge.

Read-only review; no merge performed.
