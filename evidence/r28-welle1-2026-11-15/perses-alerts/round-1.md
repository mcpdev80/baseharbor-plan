# 0428-073 · Define and provision alert — round-1 evidence

Mission: /tmp/opencode/mission-welle2-073.md
Task contract: `python3 scripts/plan.py show t-20261114-r28-perses-alerts`
Card: 0428-073 · release v0.4.28 · type task · areas observability

## PLAN (nummerliste)

- Read mission + task contract (plan.py show t-20261114-r28-perses-alerts); task is `waiting` on perses-datasources (still active/open PR)
- Verify base head via ls-remote; the seam is `active` not accepted, no alerting present — cut wt from seam head 492b8e8f; confirm ancestor
- Claim task via plan.py claim; commit+push claim to planning origin/main (fb919f63)
- Inspect current Core source: perses.go seam, perses datasource adapter (PR #1608), prometheus.go/files/verify/render, serviceaccess, observability model, CLI status surface
- Scope decision: own file internal/metrics/perses_prometheus_alerts.go + golden test, fail-closed without valid evaluator/recipient, no shared-file edits, no invented notification-channel secrets
- Write internal/metrics/perses_prometheus_alerts.go + golden test (real evaluator + notification owner contract)
- go vet + go build ./... + go test ./internal/metrics/... ./internal/capability/... all green; source-readability audit PASS
- Write this evidence akte (PLAN nummerliste, no checkboxes)
- Draft PR #1613 (title 0428-073), base lane-0428-075-perses-seam, draft, head c043d143
- Push evidence to planning origin/main; confirm in remote tree
- Bring down any compose/Docker state by own last action
- END with head-SHA

## SCOPE DECISION (coordinator-confirmed 2026-11-16)

Base lane-0428-075-perses-seam @ 492b8e8f994 (ls-remote witness). Own file internal/metrics/perses_prometheus_alerts.go + golden test, fail-closed without a real evaluator + notification owner, no stacking on datasource/dashboards lanes, no shared-file edits, no invented notification-channel secrets. Task depends_on perses-datasources (active/open PR #1608) — recorded as STATE below; not blocking per direct mission instruction.

## BASE ATTESTATION

- `git ls-remote origin refs/heads/lane-0428-075-perses-seam`:
  `492b8e8f994b16e6f73819a08175f8178cd63292`
- Branch cut from that head; `git merge-base --is-ancestor 492b8e8f... HEAD` → YES.
- Candidate only my own commit on top of base.

## LUNA-LINE / CONTRACT WITNESS

Alert rule evaluation and notification owner are Perses-native (native plugin/format), never Grafana-UI/dashboard-JSON. Fail-closed: an alert contract without a real evaluator + a validated recipient is NOT "alerting enabled". No invented notification-channel secret.

## WITNESSES

ls-remote base head (origin, before first evidence commit):
```
$ git ls-remote origin refs/heads/lane-0428-075-perses-seam
492b8e8f994b16e6f73819a08175f8178cd63292	refs/heads/lane-0428-075-perses-seam
```

Candidate head + provenance (origin, after push):
```
$ git ls-remote origin refs/heads/w073-perses-alerts
c043d1438eb483f41e0c4985a4c42b7143afa942	refs/heads/w073-perses-alerts
$ git log --oneline 492b8e8f..origin/w073-perses-alerts
c043d143 feat(0428-073): define fail-closed Perses alert evaluator + notification owner contract
```

Plan claim commit pushed to planning origin/main:
```
$ git log --oneline -1 origin/main
fb919f63 claim t-20261114-r28-perses-alerts: w073-perses-alerts
```

PR (gh, draft):
- PR #1613 (https://github.com/mcpdev80/baseharbor/pull/1613)
- baseRefName: lane-0428-075-perses-seam
- headRefName: w073-perses-alerts
- headRefOid: c043d1438eb483f41e0c4985a4c42b7143afa942
- isDraft: true, state: OPEN

## ACCEPTANCE (acceptance-point → test name + output)

- Verified, native Perses alert rule evaluator/format; real provider signal, no false capability/UI claim, no false "alerting enabled" without a valid recipient.
  - Test `TestPersesAlertEvaluatorShape`: kind=`PrometheusRuleEvaluator` (native Prometheus rule evaluator, never a Grafana-UI/dashboard JSON), evaluator=real native evaluator, owner=`prometheus` as owner reference, recipient_validated=true, reachability=`configured_unverified`. PASS.
  - Test `TestPersesAlertEvaluatorFailClosedWithoutRealEvaluator`: without a real evaluator the contract returns the fail-closed error, never "alerting enabled". PASS.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership/authorization; secrets (notification-channel) out of logs, manifests and audit; optional visualization does not force new capabilities.
  - Test `TestPersesAlertEvaluatorNoSecretInContract`: the contract carries no `bearer`/`password`/`api_key`/`token`/`clientCert`/`privateKey`/`secret`; owner named as owner reference. PASS.
  - Test `TestPersesAlertEvaluatorFailClosedWhenUnpinned` / `FailClosedWhenUnselected`: fail-closed PersesAlertEvaluatorError, never a fabricated contract. PASS.
- Preserve independent Prometheus/Loki/Tempo backend ownership; remove only owned resources; real rule evaluation + persistence via supported Prometheus contract.
  - Test `TestPersesAlertEvaluatorGoldenFiles`: `internal/metrics/testdata/perses-alerts/alerting.json` matches marshalled contract byte-for-byte. Golden:
    ```json
    {
      "kind": "PrometheusRuleEvaluator",
      "name": "baseharbor-observability-alerts",
      "evaluator": "PrometheusRuleEvaluator",
      "owner": "prometheus",
      "recipient_validated": true
    }
    ```
- No native proof skipped.

## TEST + BUILD VITNESSES

```
$ go build ./internal/metrics/...
(no output)
$ go vet ./internal/metrics/
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
=== RUN   TestPersesAlertEvaluatorValidateHealthFailClosedWhenUnpinned
--- PASS: TestPersesAlertEvaluatorValidateHealthFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesAlertEvaluatorGoldenFiles
--- PASS: TestPersesAlertEvaluatorGoldenFiles (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/metrics
$ go test ./internal/metrics/ ./internal/capability/
ok  	github.com/mcpdev80/baseharbor/internal/metrics
ok  	github.com/mcpdev80/baseharbor/internal/capability
```

## CI COVERAGE (Owner directive 2026-11-07)

New test `internal/metrics/perses_prometheus_alerts_test.go` is picked up by existing CI without any `.github/**` edit (Owner scope):
- `.github/workflows/ci.yml` line ~122: `go test ./contracts/... ./internal/... ./spec/...` runs the full `internal/metrics` package (covers my new file).
- `.github/workflows/ci.yml` line ~341: `go test ./...` also runs it.
- No `.github` change required; the existing unit-test group covers the metrics path. No VM-only or local-only test introduced.

## DEPENDENCY STATE (STATE, not blocking)

- `t-20261114-r28-perses-datasources`: state `active`, open draft PR #1608 (head 18360b69). Not yet accepted.
- `t-20261114-r28-perses-contract-seam`: NOT accepted (review).
- `t-20261114-r28-perses-runtime`: NOT accepted.
- Proceeding on the single-base seam per direct mission instruction (Owner directive names the exact base + delivery method). The seam + runtime lanes gate downstream dashboards, not this configuration-only alerting contract.

## REPO-RULE COMPLIANCE

- Single write-set, own adapter file (`perses_prometheus_alerts.go`), own golden test + testdata. No edits to datasource/contract/shared files.
- No `.github/**` edits (Owner scope). No reruns, no workflow_dispatch.
- No containers/compose started (coordinator/codeman host is a forbidden test host; baha-runner-* are not test hosts).
- No subagents (§4.8).

## CLEANLINESSION (/tmp/opencode/w073)

- No docker/podman compose projects, networks, volumes or state directories started.
- Worktree `/tmp/zt/w073-alerts` contains only the baseharbor checkout + my own adapter file + golden test + `testdata/`. No stray test artifacts beyond the committed golden file (temp generator `golden_main.go` removed after golden generation).
- `docker ps`/`docker compose ls`/`docker network ls`/`docker volume ls` all empty (no containers). No orphan cleanup needed.

## END LINE

END DONE mission-welle2-073.md: 0428-073 Perses alert evaluator + notification owner contract — round-1 delivered as own-file adapter `internal/metrics/perses_prometheus_alerts.go` + golden test (8 tests pass), fail-closed without a valid evaluator or recipient, no false capability/UI claim, no notification secret in contract, Prometheus as owner reference + native PrometheusRuleEvaluator; draft PR #1613 base lane-0428-075-perses-seam, candidate SHA c043d1438eb483f41e0c4985a4c42b7143afa942 (only own commit on 492b8e8f); evidence on planning origin/main 2bdf0abf; go build/vet/all metrics+capability tests green, source-readability audit PASS, CI covered by existing ci.yml internal/... group; no containers; no .github edits.
