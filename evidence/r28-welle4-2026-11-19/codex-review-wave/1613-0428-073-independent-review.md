# Independent read-only review — PR #1613 / 0428-073

Reviewed 2026-11-19.

- Head `d8838f622b551cdc8a7f8e8320c3f122b2ae5783`, base `da76c5cf9c963207038d5599bd130b89ecb1e8a4`; GitHub reports DIRTY/CONFLICTING against current develop `558dc42d0c8c9d798fcdf5938be2ea14e432b754`.
- Exact-head run `44495425072` passed selected checks, unit shards, build/vet and source format. It is stale relative to current develop; rebase and rerun are required.
- No edits/comments/claim/merge by this review.

## Findings

1. `internal/metrics/perses_prometheus_alerts.go:181-182` hardcodes `persesAlertRealEvaluatorContractPresent()` false, so `BuildPersesAlertEvaluator` cannot return a contract and its success branch is unreachable. This may be an intentional fail-closed placeholder while evaluator/notification ownership is absent; reconcile with acceptance before treating it as a defect.
2. If that stub is ever enabled, `VerifyPersesAlertEvaluatorHealth` (`:194-212`) does not verify that the manifest selected `ObservabilityManagementUI`/Perses, so it could return success for an unselected service.
3. `TestPersesAlertEvaluatorNoSecretInContract` (`internal/metrics/perses_prometheus_alerts_test.go:283-299`) requires the builder to error, then compares a fixed provider constant against secret-name strings. It never inspects a contract and does not substantiate its name/claim.
