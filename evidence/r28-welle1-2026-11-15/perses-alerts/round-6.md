# 0428-073 · Perses alert evaluator — round-6 evidence (luna-r3 correction)

> Correction round. Base: card `t-20261114-r28-perses-alerts`, PR #1613.
> Verdict under correction: **act-luna-r3.md = REQUEST CHANGES** (r6 trigger).
> Mission: `/tmp/opencode/mission-alerts-r6.md`.

**Candidate head (before fix):** `22c8f8694da072df8b01270ae98a392263f0ef4d` (r5)
**Candidate head (after fix):** `470735c1d187d8a680ae3b0539d75f592c945110` (round 6)
**Base:** `w073-perses-alerts` @ `22c8f8694` — fast-forward verified.
**Recipe akte:** `act-luna-r3.md` (word-for-word recipe + STOP clause).

## PLAN (nummerliste)

- Read mission + act-luna-r3.md; confirm the r6 trigger: Luna r3 REQUEST CHANGES.
- Reproduced the defect: `BuildPersesAlertEvaluator` returned `RecipientValidated=true` for a bare `/metrics` scrape source with no real rule evaluator or notification recipient.
- Confirmed the scope reality: this Core ships **no** real Prometheus rule-evaluation and **no** notification-owner (recipient/sender) contract. Repo-wide grep for `PrometheusRuleEvaluator | alertmanager | notification owner/recipient | rule evaluator` in `internal/ cmd/ contracts/` (non-test) is empty. The only Prometheus contract is the metrics scrape path (`internal/metrics/prometheus_render.go`, `prometheus_files.go`, `prometheus_verify.go`) — a scrape target, never an evaluator or recipient.
- Applied the mission STOP clause + Luna decision: fail-closed. `BuildPersesAlertEvaluator` and `VerifyPersesAlertEvaluatorHealth` now fail closed (`not_enabled`, `RecipientValidated=false`) for every selected, pinned surface — selection, datasource pin, and a materialized `/metrics` scrape source are all NOT evaluator or recipient proof.
- Rewrote the tests to assert fail-closed; the Luna r3 negative cell (selected+pinned+materialized `/metrics` scrape source) is a named test that fails closed.
- `go build ./...`, `go vet ./...`, gofmt clean; all 16 `internal/metrics` Perses tests PASS.
- Committed as fast-forward on `w073-perses-alerts` (base `22c8f8694` verified ancestor); pushed via explicit refspec `origin HEAD:refs/heads/w073-perses-alerts`; ls-remote witness confirms head.
- Wrote this akte + pushed to planning `origin/main`.
- Brought down any compose (none started); posted END with head SHA.

## DEFECT (reproduced before fix)

```
=== RUN   TestReproScrapeSourceProvesRecipient
    zz_repro_perses_test.go:23: REPRO: BuildPersesAlertEvaluator returned RecipientValidated=true, Reachability="configured_unverified"
    zz_repro_perses_test.go:25: DEFECT CONFIRMED: /metrics scrape source set RecipientValidated=true without a real evaluator/recipient contract
```

Luna r3: "`persesAlertValidatedRecipient` returns true solely when that source list is non-empty… `BuildPersesAlertEvaluator` consequently sets `RecipientValidated: true` without identifying or validating any recipient/receiver. No rule group, evaluation execution, notification receiver, or sender is inspected." The r5 fixture (`persesPrometheusRuleSource`) was a `/metrics` scrape target (`Class: SourcePlatformProvider`), not an evaluator or recipient.

## FIX SUMMARY (vs Luna r3 recipe)

File: `internal/metrics/perses_prometheus_alerts.go` (+ its test; no `.github/**`).

- **Removed the false-positive proof path.** `persesAlertRealEvaluator(m)` (materialized-scrape-source → `policyAuthorizedSources`) and `persesAlertValidatedRecipient(sources)` (`len(sources) > 0`) are deleted. The scrape source no longer feeds the evaluator or recipient.
- **Added `persesAlertRealEvaluatorContractPresent() bool`** returning `false` — the fail-closed gate that encodes the verified finding that no real rule-evaluation/notification-owner contract exists in this Core. Both `persesAlertEvaluatorFromRelease` and `VerifyPersesAlertEvaluatorHealth` now `if !persesAlertRealEvaluatorContractPresent() { return fail-closed PersesAlertEvaluatorError }`.
- The fail-closed error names the reason explicitly: *no real Prometheus rule-evaluation and notification-owner contract exists in this Core; selection, datasource pin and an authorized metrics scrape source are not evaluator or recipient proof, so the alerting contract is fail-closed (not_enabled)*.
- A future Owner-approved real evaluator + recipient contract would set `persesAlertRealEvaluatorContractPresent()` to `true` and gate the positive path behind it; until then the contract stays unavailable. **No evaluator, recipient, receiver, route or secret is invented.**
- Deleted the orphaned golden `internal/metrics/testdata/perses-alerts/alerting.json` — no positive contract path remains.
- Updated the file banner + `PersesAlertReachabilityConfiguredUnverified` doc to record that this Core can currently produce **only** the fail-closed `not_enabled` verdict.

## FINDING (file:line — Fund→Karte Pflicht)

- **No real Prometheus rule-evaluation / notification-owner contract exists in this Core.**
  - Evidence: repo-wide non-test grep in `internal/ cmd/ contracts/` for `PrometheusRuleEvaluator | alertmanager | notification owner|notification recipient|rule evaluator` returns nothing. The sole Prometheus contract is the metrics scrape path:
    - `internal/metrics/prometheus_render.go` (render)
    - `internal/metrics/prometheus_files.go` (`ExistingProviderFiles`)
    - `internal/metrics/prometheus_verify.go`
  - Fail-closed gate placed at: `internal/metrics/perses_prometheus_alerts.go:155` (build), `:181` (`persesAlertRealEvaluatorContractPresent`), `:204` (health verify).
- **Fund→Karte-Pflicht (Owner-Direktive 2026-11-08):** this finding is poured into a follow-up card. Recommended card: **`t-20261114-r28-perses-alerts-contract`** (or fold into the existing `t-20261114-r28-perses-contact-routing`/`perses-native-proof` required-by cards): *define the real Prometheus rule-evaluation + notification-owner contract in an Owner-approved contract, or record the explicit unavailable decision*. The round-6 card itself is the fail-closed stop; the real-contract work is the follow-up.

## WITNESSES

ls-remote base head and alert head (origin):
```
$ git ls-remote origin refs/heads/w073-perses-alerts   (before commit)
22c8f8694da072df8b01270ae98a392263f0ef4d	refs/heads/w073-perses-alerts
$ git ls-remote origin refs/heads/w073-perses-alerts   (after push)
470735c1d187d8a680ae3b0539d75f592c945110	refs/heads/w073-perses-alerts
$ git ls-remote origin refs/heads/main
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```
git merge-base ancestry (fast-forward):
```
$ git merge-base --is-ancestor 22c8f8694da072df8b01270ae98a392263f0ef4d HEAD && echo OK
OK
```

## FOCUSED TESTS (internal/metrics, all PASS)

```
=== RUN   TestPersesAlertEvaluatorFailsClosedWithScrapeSource        # Luna r3 exact defect cell → fails closed
=== RUN   TestPersesAlertEvaluatorFailsClosedWithoutScrapeSource
=== RUN   TestPersesAlertEvaluatorFailClosedWhenUnpinned
=== RUN   TestPersesAlertEvaluatorFailClosedWhenUnselected
=== RUN   TestPersesAlertEvaluatorFailsClosedWhenRecipientAbsent
=== RUN   TestPersesAlertEvaluatorNoRecipientValidatedWithoutConcreteEvidence
=== RUN   TestPersesAlertEvaluatorValidateHealthFailsClosed
=== RUN   TestPersesAlertEvaluatorValidateHealthRejectsPinOnly
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosedWithoutEvaluator
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosedWhenUnpinned
=== RUN   TestPersesAlertEvaluatorFailsClosedNoEvaluatorContract
=== RUN   TestPersesAlertEvaluatorNoSecretInContract
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.007s
```
Positive/negative both covered: the positive contract path is deliberately unreachable (fail-closed), and every selected+pinned surface is asserted to fail closed. `go build ./...` and `go vet ./...` clean; `gofmt -l` clean.

## CI

Exact-head CI for `470735c1d` on PR #1613 is dispatched by the coordinator (per mission: "CI dispatcht coord"). No CI result recorded in this akte yet.

## STOP / NOT-CLOSED

- This round is a **fail-closed correction**, not acceptance. No real evaluator/recipient contract is defined; that is the STOP outcome required by Luna r3 and the mission.
- **Fund→Karte follow-up outstanding:** a card for the real Prometheus rule-evaluation + notification-owner contract (or the explicit unavailable Owner decision) has not yet been opened — recommend `t-20261114-r28-perses-alerts-contract`.
- Card `t-20261114-r28-perses-alerts` state stays **review**; PR #1613 stays OPEN/MERGEABLE. No merge, no ready_for_review, no force-push.

<!-- round-6 | candidate 470735c1d187d8a680ae3b0539d75f592c945110 | fail-closed (luna-r3) -->
