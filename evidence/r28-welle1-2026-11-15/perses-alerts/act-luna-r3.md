# CODEX-REVIEW — PR #1613 correction follow-up

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-alerts`  
**Candidate:** `22c8f8694da072df8b01270ae98a392263f0ef4d`  
**Base:** `lane-0428-075-perses-seam` @ `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`  
**Exact-head CI:** run `43819734753`, event `pull_request`, created `2026-11-16T06:52:07Z`, COMPLETED SUCCESS, exact head. Full base-to-head diff is three lane commits; current correction delta `2dcbfebb..22c8f869` changes the alert implementation and tests. `git diff --check` clean.

## Verdict: REQUEST CHANGES

The datasource pin-only false positive is removed, but the replacement still confuses an authorized metrics scrape source with both an alert-rule evaluator and a notification recipient. `persesAlertRealEvaluator` accepts any policy-authorized `observability.MetricsSource` from the retained runtime scrape snapshot (lines 203–221); the test fixture is a Prometheus `/metrics` target (`persesPrometheusRuleSource`, test lines 80–89), not an alert rule or rule-evaluation path. Then `persesAlertValidatedRecipient` returns true solely when that source list is non-empty (implementation lines 250–260). `BuildPersesAlertEvaluator` consequently sets `RecipientValidated: true` without identifying or validating any recipient/receiver. No rule group, evaluation execution, notification receiver, or sender is inspected. This does not satisfy the card's explicit requirement to define the real rule evaluator and notification owner, nor Luna r2's requirement for a concrete evaluator/recipient or explicit unavailable state.

## Recipe / stop

- **File/change:** `internal/metrics/perses_prometheus_alerts.go`. Do not treat `MetricsSource` membership as rule-evaluator or recipient proof. Bind the contract to an existing supported Prometheus rule-evaluation and notification-owner contract, or keep alerting unavailable/fail-closed and leave `RecipientValidated=false` until an Owner-approved real contract exists. Do not invent a notification receiver or secret.
- **Required tests:** selected + materialized + policy-authorized `/metrics` scrape source, with no rule evaluator and no notification receiver, must still fail closed or remain explicitly unavailable. A positive case must use the actual supported rule-evaluator contract and a separately validated recipient/owner. Assert health verification does not pass without the actual runtime evaluation/notification path.
- **Checks:** after correction, run the focused `internal/metrics` tests and obtain exact-head `pull_request` SUCCESS for the corrected SHA; retain the current negative selection, authorization, and secret tests.
- **Stop:** if no supported evaluator/recipient contract exists, keep the alert contract unavailable and request the required owner/API decision. Do not claim the Prometheus scrape source is an evaluator or recipient.

The alert card's datasource dependency remains unaccepted. This review does not satisfy it, accept the card, or authorize merge. Read-only SHA-exact review; no product files changed; no merge.
