# 0428-073 · Perses alert evaluator — round-5 evidence (luna-r2 correction)

> Correction round. Base: card t-20261114-r28-perses-alerts, PR #1613.
> Verdict under correction: act-luna-r2.md = REQUEST CHANGES.
> Recipe is Luna's own recipe in act-luna-r2.md (word-for-word).

Mission: /tmp/opencode/mission-alerts-r5.md
Card: 0428-073 · task · areas observability · lane w073-perses-alerts · PR #1613
Candidate head (before fix): 2dcbfebb88f73d539376debbf3477f6420eaceca
Base: Perses seam lane-0428-075-perses-seam @ 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08
Recipe akte: evidence/r28-welle1-2026-11-15/perses-datasources/round-2-luna-correction.md (authoritative-source fail-closed precedent)

## PLAN (nummerliste)

- Read mission + luna-r2 akte (act-luna-r2.md); confirm defect: `persesAlertValidatedRecipient` requires Perses selection and a non-empty `release.PrometheusPluginVersion`, but that field pins the Prometheus datasource plugin; `persesAlertEvaluatorFromRelease` / `VerifyPersesAlertEvaluatorHealth` return nil for that same selected+pinned manifest despite no evaluator execution or notification-sender probe.
- Verify remotes: planning repo root zone = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan; product refs: w073-perses-alerts @ 2dcbfebb88f, base lane-0428-075-perses-seam @ 66ff93d1c (ancestor of head verified), PR #1613 draft OPEN.
- Worktree /tmp/opencode/perses-identity-r3 checked out on branch w073-alerts-r5 AT 2dcbfebb88f (base attestation: 66ff93d1c ancestor of head). Used the existing product checkout to avoid the locked-index testdata files held by a live docker-compose process in another worktree.
- Reproduced defect: health verifier returned nil for selected+pinned+NO-RECIPIENT (pin-validation alone).
- Implement fail-closed fix on internal/metrics/perses_prometheus_alerts.go: evaluator + recipient bind to an AUTHORITATIVE, materialized, AUTHORIZED Prometheus rule source (the retained runtime source snapshot: materialized, provider-owned, policy-allowed), never the datasource pin; health verifier grounds in manifest + snapshot truth, pin-validation alone never passes.
- Add required negative test cells (Luna recipe): health rejects pin-only/unselected, evaluator-absent (materialized provider but no sources) fails closed, selected+pinned+NO-RECIPIENT fails closed, no RecipientValidated without concrete evidence; keep the positive TestPersesAlertEvaluatorShape + golden-file witness.
- go build ./... + go vet ./... + go test ./internal/metrics/ ./internal/capability/ green; gofmt -l clean; source-readability audit PASS.
- Commit on w073-perses-alerts (FAST-FORWARD only, no amend; ls-remote verify 2dcbfebb88f as ancestor before commit); push with explicit refspec git push origin HEAD:refs/heads/w073-perses-alerts + ls-remote witness after push.
- Commit evidence akte round-5.md + push to planning origin/main; bring down any compose (none started); post END with new head SHA.

## SCOPE DECISION

Own file internal/metrics/perses_prometheus_alerts.go + test. This correction round is scoped to that file + its test: the Luna recipe names exactly the fail-closed health verifier and the recipient validation. No shared-seam, datasource, dashboards or contract-file edits; no invented notification-channel secret; no .github/**.

## BASE ATTESTATION

- `git ls-remote origin refs/heads/lane-0428-075-perses-seam`:
  `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`
- `git ls-remote origin refs/heads/w073-perses-alerts`:
  `2dcbfebb88f73d539376debbf3477f6420eaceca`
- Base seam 66ff93d1c IS an ancestor of the alert head 2dcbfebb8: `git merge-base --is-ancestor 66ff93d1c 2dcbfebb8` → YES.
- Branch cut exactly at that head (checkout w073-alerts-r5 at 2dcbfebb88f); own commit 22c8f8694 is a fast-forward add on top.

## FIX SUMMARY (vs recipe / Luna r2)

- File/change (internal/metrics/perses_prometheus_alerts.go):
  - Removed the datasource-pin evaluator/recipient proof: `release.PrometheusPluginVersion` no longer feeds either `persesAlertValidatedRecipient` or the evaluator path. The datasource pin is a datasource reference, never a rule evaluator.
  - New `persesAlertRealEvaluator(m)` grounds the evaluator in an AUTHORITATIVE, materialized, AUTHORIZED Prometheus rule source: `ExistingProviderFiles` (materialized provider, fail-closed on missing provider dir) → `readRuntimeSourceSnapshot` (retained `runtime-sources.json` validated against provider placement: missing/foreign/invalid/ambiguous all propagate) → `policyAuthorizedSources` (metrics-collection authorization). Absent sources, denied/foreign-owned sources, or an empty snapshot return the fail-closed error. Pin validation alone can NEVER pass.
  - `persesAlertValidatedRecipient` now takes the authorized sources and requires `len > 0` — selection alone and the datasource pin alone are no longer recipient proof.
  - `BuildPersesAlertEvaluator` and `VerifyPersesAlertEvaluatorHealth` both ground in manifest truth (pinned release + Perses selected + real, authorized evaluator + validated recipient). The selected+pinned+NO-RECIPIENT surface now fails closed instead of returning nil.
  - No fabricated evaluator, no notification-channel secret, no SUPPORTED-HA claim.
- Tests (internal/metrics/perses_prometheus_alerts_test.go): added `TestPersesAlertEvaluatorValidateHealthFailClosedWithoutEvaluator` (selected+pinned, materialized provider but no rule sources → fails closed — the untested case Luna r2 named), aligned `TestPersesAlertEvaluatorFailClosedWithoutRealEvaluator` to the materialized-source path; added the `persesMaterializeAlertProvider` fixture (materializes a provider-owned Prometheus rule source) and `persesPrometheusRuleSource`. Kept the positive `TestPersesAlertEvaluatorShape` + golden-file witness.

## WITNESSES

ls-remote base head and alert head (origin, before first evidence commit):
```
$ git ls-remote origin refs/heads/lane-0428-075-perses-seam
66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08	refs/heads/lane-0428-075-perses-seam
$ git ls-remote origin refs/heads/w073-perses-alerts
2dcbfebb88f73d539376debbf3477f6420eaceca	refs/heads/w073-perses-alerts
```
git merge-base ancestry:
```
$ git merge-base --is-ancestor 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08 2dcbfebb88f73d539376debbf3477f6420eaceca && echo OK
OK
```

## TEST + BUILD VITNESSES

```
$ gofmt -l internal/metrics/perses_prometheus_alerts.go internal/metrics/perses_prometheus_alerts_test.go
(empty = clean)
$ go build ./...
(no output)
$ go vet ./...
(no output)
$ go test ./internal/metrics/ -run TestPersesAlert -count=1 -v
=== RUN   TestPersesAlertEvaluatorShape
--- PASS: TestPersesAlertEvaluatorShape (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWhenUnpinned
--- PASS: TestPersesAlertEvaluatorFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWhenUnselected
--- PASS: TestPersesAlertEvaluatorFailClosedWhenUnselected (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWithoutRealEvaluator
--- PASS: TestPersesAlertEvaluatorFailClosedWithoutRealEvaluator (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWhenRecipientAbsent
--- PASS: TestPersesAlertEvaluatorFailClosedWhenRecipientAbsent (0.00s)
=== RUN   TestPersesAlertEvaluatorNoRecipientValidatedWithoutConcreteEvidence
--- PASS: TestPersesAlertEvaluatorNoRecipientValidatedWithoutConcreteEvidence (0.00s)
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosed
--- PASS: TestPersesAlertEvaluatorValidateHealthFailClosed (0.00s)
=== RUN   TestPersesAlertEvaluatorValidateHealthRejectsPinOnly
--- PASS: TestPersesAlertEvaluatorValidateHealthRejectsPinOnly (0.00s)
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosedWithoutEvaluator
--- PASS: TestPersesAlertEvaluatorValidateHealthFailClosedWithoutEvaluator (0.00s)
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosedWhenUnpinned
--- PASS: TestPersesAlertEvaluatorValidateHealthFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesAlertEvaluatorNoSecretInContract
--- PASS: TestPersesAlertEvaluatorNoSecretInContract (0.00s)
=== RUN   TestPersesAlertEvaluatorGoldenFiles
--- PASS: TestPersesAlertEvaluatorGoldenFiles (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/metrics
$ go test ./internal/metrics/ ./internal/capability/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/metrics
ok  	github.com/mcpdev80/baseharbor/internal/capability
$ bash scripts/source-readability-audit.sh
... PASS (file size / function span / regression ratchet)
```

## CI COVERAGE (Owner directive 2026-11-07)

- All new/changed tests live in package internal/metrics; they run in the existing CI unit group: `.github/workflows/ci.yml:124` (`go test ./contracts/... ./internal/... ./spec/...`) on the `Test` job (pull_request, paths: '.github/**', '**.go', 'go.mod', 'go.sum', 'spec/**', 'contracts/**'). My changes touch only internal/**.go test files => trigger satisfied.
- Formatting signature (`Check formatting`, ci.yml:106 `gofmt -l cmd internal spec contracts`) is clean at head (witness above).
- No new test is VM-only or local-only; no .github/** edit was needed or made. Owner scope: no rerun, no workflow_dispatch.

## WITNESSES (after commit + push)

```
$ git ls-remote origin refs/heads/w073-perses-alerts
22c8f8694da072df8b01270ae98a392263f0ef4d	refs/heads/w073-perses-alerts
$ git log --oneline 2dcbfebb88f73d539376debbf3477f6420eaceca..origin/w073-perses-alerts
22c8f8694 fix(0428-073): fail-closed Perses alert evaluator + recipient (luna-r2)
```
- Only my own commit on top of 2dcbfebb88f (no foreign commit in that range). Push was a NORMAL fast-forward `git push origin 22c8f8694:refs/heads/w073-perses-alerts` (2dcbfebb8..22c8f8694, no -f, no amend).
- PR #1613 after push (gh): baseRefName lane-0428-075-perses-seam, isDraft true, state OPEN.
- Evidence on planning origin/main:
```
$ git ls-remote origin main
7f32a6b0f9e9d15fe67ce0b9bd66e8cc4f7fd068	refs/heads/main
```

## repo-rule compliance

- Single write-set, own file internal/metrics/perses_prometheus_alerts.go + test. No shared/seam/datasource/dashboard/contract-file edits.
- No .github/** edits (Owner scope). No reruns, no workflow_dispatch, no merge, no ready_for_review, no force-push, no amend.
- No containers/compose started (coordinator/codeman host is a forbidden test host; baha-runner-* are not test hosts); nothing to bring down.
- No subagents (§4.8); all work in this session.
- Planning zone verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.

## END LINE

END_DONE mission-alerts-r5.md: 0428-073 Luna-r2 correction — alert evaluator + recipient now bound to an AUTHORITATIVE, materialized, AUTHORIZED Prometheus rule source (retained runtime source snapshot: materialized provider + policy-allowed source of this project), not the datasource pin; pin-validation alone never passes, selected+pinned+NO-RECIPIENT and evaluator-absent/foreign-owned/empty-snapshot all fail closed (PersesAlertEvaluatorError), RecipientValidated requires concrete source evidence, golden + 12 TestPersesAlert* PASS, go build ./... + go vet ./... + go test ./internal/metrics/ ./internal/capability/ green, gofmt -l clean, source-readability audit PASS, CI covered by existing ci.yml internal/... group (no .github edit); single fast-forward commit 22c8f8694da072df8b01270ae98a392263f0ef4d on w073-perses-alerts head 2dcbfebb88f (own commit only, base 66ff93d1c verified ancestor); PR #1613 draft OPEN base seam lane-0428-075-perses-seam unchanged; evidence on planning origin/main 7f32a6b0.
