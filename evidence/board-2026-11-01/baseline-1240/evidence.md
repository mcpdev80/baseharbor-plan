# baseline-1240 — DER BASIS-DURCHLAUF — Evidence

## Task
Mission `baseline-1240` (Owner-Direktive): der kleine echte PR #1240 (openbao→postgres TLS/SASL-Fix)
sollte vollständig durch die EXISTIERENNE neue CI-Kette laufen — Kandidat auf die aktuelle,
korrigierte Basis heben und die Kette beweisen. Keine neuen Gates, keine Features.

## PLAN (Bullets)
- #1240 (b8446716) war ein Integration-Merge [437358e4, 116adb3d] und blockierte NUR am stale-base
  diff-resolver (behoben in #1251 = d56e9ddd, noch NICHT auf develop).
- Basis = develop (437358e4) + diff-resolver-fix (d56e9ddd).
- Branch `work/baseline-1240` ab d56e9ddd; #1240-Produkt-Diff (116adb3d gegen seinen alten Base
  cb6b7387, `internal/`, 3 Dateien) als EINEN Applikations-Commit (kein Merge-Commit) auf d56e9ddd ziehen.
- PR #1252 gegen develop eröffnen; #1240 als "superseded by #1252" markieren (Referenz-Kommentar,
  nicht.closeen — erst nach Grün des Nachfolgers).
- Eigenes-Run-Pflicht: kompletten PR-Lauf bis terminal beobachten; 'PR Selected Checks' SUCCESS.
- Do nothing else: kein Force-Push, keine develop-Pushes, keine ci.yml-Änderungen.

## Candidate
- Branch: `work/baseline-1240` @ `e93d797d` (single commit, parent d56e9ddd — kein Merge-Commit)
- Diff vs d56e9ddd = exakt die 3 #1240-Produkt-Dateien (internal/runtime/, +96/-7):
  - internal/runtime/openbao_runtime_prepare.go — PGSSLMODE=verify-ca auf psql-Init + Health-Checks; DSN sslmode=verify-full → verify-ca (HAProxy übernimmt Server-Hostnamen)
  - internal/runtime/openbao_sslmode_guard_test.go (neu) — Regression-Guard für insecure TLS-Modi
  - internal/runtime/stack_test.go — Erwartungen auf verify-ca + pinnte PGSSLMODE aktualisiert

## Local Checks (Worker-Eigenlauf)
- `go build ./...` → 0
- `go vet ./internal/runtime/...` → 0
- `go test ./internal/runtime/...` → ok (incl. TestOpenBaoSSLModeGuard, stack TLS tests PASS)

## PR
- #1252 — "baseline: port #1240 openbao TLS fix onto develop + diff-resolver-fix"
  - base: develop (437358e4), head: work/baseline-1240 (e93d797d)
  - https://github.com/mcpdev80/baseharbor/pull/1252
  - mergeable; mergeStateStatus BLOCKED nur (vor) Grün — normal
- #1240: OFFENER Zustand (bewusst offen), Referenz-Kommentar "superseded by #1252" gesetzt.

## Run-ID + Job-Tabelle
Run: `41312529590` — `CI · PR #1252` (event=pull_request, headSha=e93d797d)
Terminal-State: **conclusion=success**, 20/20 Jobs completed.

| Job | Status | Conclusion | Anmerkung |
| --- | --- | --- | --- |
| Workflow policy | completed | **success** | fixed workflow surface + syntax |
| PR · Trusted Plan | completed | **success** | resolve exact immutable PR inputs (trusted base) |
| PR · Exact Candidate | completed | **success** | SHA-exaktes Artefakt e93d797d |
| PR · Demo Pin | completed | **success** | |
| PR · Runner Interface | completed | **success** | |
| PR · Focused Python | completed | **success** | diff/planner/verifier/pins regressions |
| PR · Validation · source-contracts | completed | **success** | go test ./internal/application/... ./contracts/... |
| PR · Validation · cli-build | completed | **success** | go build ./cmd/baha |
| PR · Validation · ci-policy | completed | **success** | scripts/ci-workflow-policy.sh |
| PR · Validation · cli-guided-tests | completed | **success** | go test ./cmd/baha -run ^TestGuided |
| PR · Validation · cli-vet | completed | **success** | go vet ./cmd/baha |
| PR · Validation · pr-planner-tests | completed | **success** | test_pr_gate_plan.py |
| PR · Validation · ci-executor-verifier-tests | completed | **success** | |
| PR · Validation · receipt-execution-tests | completed | **success** | receipt control plane |
| PR · Selected Runtime (atomic/docker/lifecycle) / docker · lifecycle | completed | **success** | **runtime gate = PASS** (gelaufen, nicht skipped) |
| PR Selected Checks | completed | **success** | terminal summary |
| Targeted HA · docker | completed | skipped | Go lifecycle gate nicht vom Planner selected |
| Targeted HA · podman | completed | skipped | Go lifecycle gate nicht vom Planner selected |
| validate | completed | skipped | |
| Release Source Preflight | completed | skipped | Release-Qualifikationspunkt, nicht hier |
| PR · Consumer Pins | completed | skipped | |
| PR · Public Contracts | completed | skipped | |

## pr-plan.json (selected_gates + base) — Artifact `trusted-pr-plan` (run 41312529590)
```json
{
  "schema": "baseharbor.pr-gate-plan/v1",
  "head_sha": "e93d797d2390759f79171b3d46862a06079cc55a",
  "merge_base_sha": "437358e494a97a45080c805d5537ec774017eb78",
  "target_base_sha": "437358e494a97a45080c805d5537ec774017eb78",
  "coverage_status": "resolved",
  "selected_gates": ["atomic/docker/lifecycle"],
  "unresolved_coverage": [],
  "reasons": [
    "internal/runtime/openbao_runtime_prepare.go: runtime-docker-engine",
    "internal/runtime/openbao_sslmode_guard_test.go: runtime-docker-engine",
    "internal/runtime/stack_test.go: runtime-docker-engine",
    "scripts/pr-diff-base.py: ci-planner",
    "scripts/test_pr_diff_base.py: ci-planner"
  ],
  "validation_contract": "Enforce all required_validation_checks ... never treat as no checks or
    automatically run the complete release catalog."
}
```
- `target_base_sha` = `merge_base_sha` = `437358e4` = develop OHNE Fix d56e9ddd.
  → Linear-/Stale-Fall, den der diff-resolver selbst bestimmt (kein `--base-tip`).
- `selected_gates` = `atomic/docker/lifecycle`; `coverage_status` = resolved.

## Runtime-gate-Evidence — Artifact `pre-release-gate-docker-lifecycle-evidence` (run 41312529590)
```json
{
  "schema": "baseharbor.pre-release.gate-evidence/v1",
  "id": "docker/lifecycle", "runtime": "docker", "gate": "lifecycle", "class": "runtime",
  "candidate_sha": "20be16d33c5d3a3f17ccf65bca80f42c4ba66f72",
  "demo_ref": "073e065f88b0dd9155cb000a4bece175a862605a",
  "outcome": "success", "cleanup_outcome": "success",
  "workflow_run_id": "41312529590", "workflow_run_attempt": 1
}
```
Runtime gate: **PASS** (summary.md: "Runtime gate | **PASS** | lifecycle").
Job-Schritte: Run runtime gate → success; Run static gate → skipped (Go lifecycle gate nicht selected,
Planner-Befund, nicht blockierend).

## Auswertung (Mission-Abgleich)
Erwartet: 'Workflow policy', 'PR · Trusted Plan', 'PR · Focused Python', 'PR · Validation *' + mind.
EIN Runtime-Lifecycle-Gate werden ausgeführt (NICHT skipped), 'PR Selected Checks' SUCCESS.
Ergebnis: alle genannten Jobs SUCCESS; "Run runtime gate" EXECUTED + PASS; "PR Selected Checks" SUCCESS.
Der stale-base Blocker ist behoben — der diff-resolver hat target_base_sha=437358e4 korrekt als
Lineare/Stale-Base bestimmt und die Kette lief sauber durch.
'Skipped' Go lifecycle gate (Targeted HA docker/podman) = Planner-Befund, nicht blockierend.

## EXKLUSIVES WRITE-SET (eingehalten)
- Nur PR-Zweig work/baseline-1240 + PR-Kommentar zu #1240. Kein Force-Push, kein develop-Push,
  keine ci.yml-Änderung.

## END
END_LANE DONE (baseline-1240: PR=#1252 head=e93d797d SelectedChecks=green Run=41312529590)
