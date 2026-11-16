# 0428-073 · Perses alert evaluator — round-4 evidence (luna-r1 correction)

> Correction round. Base: card t-20261114-r28-perses-alerts, PR #1613.
> Verdict under correction: act-luna-r1.md = REQUEST CHANGES.
> Recipe is Luna's own recipe in act-luna-r1.md (word-for-word).

Mission: /tmp/opencode/mission-fix-alerts.md
Card: 0428-073 · task · areas observability · lane w073-perses-alerts · PR #1613
Candidate head (before fix): 53300858e21f2625d53b766bf5c0fb6216af6c62
Base: Perses seam 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08
Recipe akte: evidence/r28-welle1-2026-11-15/perses-datasources/round-2-luna-correction.md (correct fail-closed health-design precedent)

## PLAN (nummerliste)

- Read mission + luna-r1 akte (act-luna-r1.md); confirm defect: VerifyPersesAlertEvaluatorHealth returns nil after pin validation alone even when the surface is unselected and no evaluator or recipient exists; persesAlertValidatedRecipient returned true on mere selection; evaluator fabricated from non-empty Prometheus datasource pin.
- Verify remotes: planning repo root zone = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan; product refs: w073-perses-alerts @ 53300858e21, base lane-0428-075-perses-seam @ 66ff93d1c (ancestor of head verified), PR #1613 draft OPEN.
- Cut worktree /tmp/opencode/w073-alerts-corr AT 53300858e21 (base attestation: 66ff93d1c is ancestor of the merge head 53300858e).
- Reproduce defect in worktree: health verifier returns nil on an unselected surface; recipient check passes on selection alone.
- Implement fail-closed fix on internal/metrics/perses_prometheus_alerts.go: VerifyPersesAlertEvaluatorHealth grounds in manifest truth — validates pinned release, checks the observability management UI + Perses selected, requires a real evaluator (pinned native Prometheus rule evaluator present), and a validated recipient (selection + real evaluator) — pin validation alone never passes; update persesAlertValidatedRecipient to require selection AND real evaluator, not selection alone.
- Add required negative test cells (Luna recipe): health verifier rejects pin-only/unselected, recipient-absent fails closed, no result claims RecipientValidated without concrete evidence; keep the positive TestPersesAlertEvaluatorShape + golden-file witness.
- go build ./... + go vet ./... + go test ./internal/metrics/ ./internal/capability/ green; gofmt -l clean; source-readability audit PASS.
- Commit on w073-perses-alerts (FAST-FORWARD only, no amend; ls-remote verify 53300858e21 as ancestor before commit); push with explicit refspec git push origin HEAD:refs/heads/w073-perses-alerts + ls-remote witness after push.
- Commit evidence akte round-4.md + push to planning origin/main (git show origin/main witness); bring down worktree/compose (none started); post END with new head SHA.

## SCOPE DECISION (coordinator-confirmed, round-1)

Own file internal/metrics/perses_prometheus_alerts.go + golden test. This correction round is scoped to that file + its test: the Luna recipe names exactly the fail-closed health verifier and the recipient validation. No shared-seam, datasource, dashboards or contract-file edits; no invented notification-channel secret; no .github/**. Umbau drumherum nur mit Begründung in der Akte.

## BASE ATTESTATION

- `git ls-remote origin refs/heads/lane-0428-075-perses-seam`:
  `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`
- `git ls-remote origin refs/heads/w073-perses-alerts`:
  `53300858e21f2625d53b766bf5c0fb6216af6c62`
- Base seam 66ff93d1c IS an ancestor of the alert head 53300858e: `git merge-base --is-ancestor 66ff93d1c 53300858e` → YES.
- Alert branch content = merge of base seam 66ff93d1c + my two own commits (c043d143 round-1 + 9e897b5f round-2 gofmt). This correction is a fast-forward add on top of 53300858e (only my own commit on top).

## FIX SUMMARY (vs recipe / Luna r1)

- File/change (internal/metrics/perses_prometheus_alerts.go):
  - VerifyPersesAlertEvaluatorHealth now grounds in manifest truth instead of returning nil after pin validation alone. It validates the pinned Perses release, checks the observability management UI (Perses) is selected in the manifest, requires a real evaluator (the pinned native Prometheus rule evaluator present — an empty PrometheusPluginVersion fails closed), and requires a validated recipient. Pin validation alone can NEVER pass; an unselected / evaluator-less / recipient-less surface returns the fail-closed PersesAlertEvaluatorError. This matches the datasources precedent (VerifyPersesPrometheusDatasourceHealth: pin never passes; unverified/unreachable returns an error).
  - persesAlertValidatedRecipient now requires BOTH selection (ObservabilityManagementUI + Perses) AND a real evaluator (non-empty pinned native Prometheus rule evaluator). Selection alone is no longer recipient proof, and the datasource pin alone is no longer evaluator proof. This addresses Luna's "selection != recipient-validierung" finding.
  - No fabricated evaluator is produced: the produced contract still names the native Prometheus rule evaluator kind + Prometheus owner, but only after the real evaluator (pin) and recipient are both concretely present.
- Tests (internal/metrics/perses_prometheus_alerts_test.go): added TestPersesAlertEvaluatorHealthRejectsPinOnly (health verifier must NOT pass on datasource-pin alone when the surface is unselected), TestPersesAlertEvaluatorFailClosedWhenRecipientAbsent (selection alone with a real evaluator but no recipient fails closed), TestPersesAlertEvaluatorNoRecipientValidatedWithoutConcreteEvidence (no RecipientValidated without concrete evidence). Kept the positive TestPersesAlertEvaluatorShape + golden-file witness.

## WITNESSES

ls-remote base head and alert head (origin, before first evidence commit):
```
$ git ls-remote origin refs/heads/lane-0428-075-perses-seam
66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08	refs/heads/lane-0428-075-perses-seam
$ git ls-remote origin refs/heads/w073-perses-alerts
53300858e21f2625d53b766bf5c0fb6216af6c62	refs/heads/w073-perses-alerts
```
git merge-base ancestry:
```
$ git merge-base --is-ancestor 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08 53300858e21f2625d53b766bf5c0fb6216af6c62 && echo OK
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
$ go test ./internal/metrics/ -run TestPersesAlert -v
=== RUN   TestPersesAlertEvaluatorShape
--- PASS: TestPersesAlertEvaluatorShape (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWhenUnpinned
--- PASS: TestPersesAlertEvaluatorFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWhenUnselected
--- PASS: TestPersesAlertEvaluatorFailClosedWhenUnselected (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWithoutRealEvaluator
--- PASS: TestPersesAlertEvaluatorFailClosedWithoutRealEvaluator (0.00s)
=== RUN   TestPersesAlertEvaluatorNoSecretInContract
--- PASS: TestPersesAlertEvaluatorNoSecretInContract (0.00s)
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosed
--- PASS: TestPersesAlertEvaluatorValidateHealthFailClosed (0.00s)
=== RUN   TestPersesAlertEvaluatorHealthRejectsPinOnly
--- PASS: TestPersesAlertEvaluatorHealthRejectsPinOnly (0.00s)
=== RUN   TestPersesAlertEvaluatorFailClosedWhenRecipientAbsent
--- PASS: TestPersesAlertEvaluatorFailClosedWhenRecipientAbsent (0.00s)
=== RUN   TestPersesAlertEvaluatorNoRecipientValidatedWithoutConcreteEvidence
--- PASS: TestPersesAlertEvaluatorNoRecipientValidatedWithoutConcreteEvidence (0.00s)
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosedWhenUnpinned
--- PASS: TestPersesAlertEvaluatorValidateHealthFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesAlertEvaluatorGoldenFiles
--- PASS: TestPersesAlertEvaluatorGoldenFiles (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/metrics
$ go test ./internal/metrics/ ./internal/capability/
ok  	github.com/mcpdev80/baseharbor/internal/metrics
ok  	github.com/mcpdev80/baseharbor/internal/capability
```

## CI COVERAGE (Owner directive 2026-11-07)

- All new/changed tests live in package internal/metrics; they run in the existing CI unit group: `.github/workflows/ci.yml:124` (`go test ./contracts/... ./internal/... ./spec/...`) on the `Test` job (pull_request, paths: '.github/**', '**.go', 'go.mod', 'go.sum', 'spec/**', 'contracts/**'). My changes touch only internal/**.go test files => trigger satisfied.
- Formatting signature (`Check formatting`, ci.yml:106 `gofmt -l cmd internal spec contracts`) is clean at head (witness above).
- No new test is VM-only or local-only; no .github/** edit was needed or made. Owner scope: no rerun, no workflow_dispatch.

## WITNESSES (after commit + push)

```
$ git ls-remote origin refs/heads/w073-perses-alerts
2dcbfebb88f73d539376debbf3477f6420eaceca	refs/heads/w073-perses-alerts
$ git log --oneline 53300858e21f2625d53b766bf5c0fb6216af6c62..origin/w073-perses-alerts
2dcbfebb8 fix(0428-073): fail-closed Perses alert health verifier + recipient validation (luna-r1)
```
- Only my own commit on top of 53300858e (no foreign commit in that range). Push was a NORMAL fast-forward `git push origin HEAD:refs/heads/w073-perses-alerts` (53300858e..2dcbfebb8, no -f, no amend).
- PR #1613 after push (gh): baseRefName lane-0428-075-perses-seam, isDraft true, state OPEN; headRefOid 2dcbfebb88f73d539376debbf3477f6420eaceca.
- Evidence on planning origin/main:
```
$ git ls-remote origin main
2df2a87e62028594ba6a78f57c1f53d745fcc067	refs/heads/main
```

## REPO-RULE COMPLIANCE

- Single write-set, own file internal/metrics/perses_prometheus_alerts.go + test. No shared/seam/datasource/dashboard/contract-file edits.
- No .github/** edits (Owner scope). No reruns, no workflow_dispatch, no merge, no ready_for_review, no force-push, no amend.
- No containers/compose started (coordinator/codeman host is a forbidden test host; baha-runner-* are not test hosts); nothing to bring down.
- No subagents (§4.8); all work in this session.
- Planning zone verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.

## END LINE

END_DONE mission-fix-alerts.md: 0428-073 Luna-r1 correction — alert health verifier now fail-closed (grounds in manifest truth: pinned release + Perses selected + real evaluator + validated recipient; pin-validation-alone never passes, unselected/unpinned/no-recipient/evaluator-less returns PersesAlertEvaluatorError), persesAlertValidatedRecipient requires selection AND real evaluator (selection != recipient, datasource pin != evaluator); added negative test cells (health rejects pin-only/unselected, recipient-absent fails closed, no RecipientValidated without concrete evidence); go build ./... + go vet ./... + go test ./internal/metrics/ ./internal/capability/ green (11 TestPersesAlert* PASS), gofmt -l clean, source-readability audit PASS, CI covered by existing ci.yml internal/... group (no .github edit); single fast-forward commit 2dcbfebb88f73d539376debbf3477f6420eaceca on w073-perses-alerts head 53300858e21 (own commit only, base 66ff93d1c verified ancestor); PR #1613 draft OPEN head 2dcbfebb88 base seam lane-0428-075-perses-seam unchanged; evidence on planning origin/main 7fcea0cf.
