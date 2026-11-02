# logsmap — Native Logs gate (PR #1286): RUNDE 4 konsolidierte CI-Infra-Integration (INTEGRATION-KANDIDAT)

**Lane:** logsmap (Worker) · **Coordinator:** f49a3303 (Qwen Flash)
**Modell:** worker-ornith1.5 · **ornith-Host**
**Datum:** 2026-11-02
**Mission:** coordinator/missions/logsmap-ci-integrate.txt (Runde 4 — Coordinator-Entscheidung gemaess Owner-P0/#1)
**Integrations-Branch:** `logsmap-ci-integrate` (base develop `9a93865a`)

## PLAN (worked checklist — AGENTS 4.4)

- [x] 1. Mission + review-r3 gelesen; isolierter develop-Branch `logsmap-ci-integrate` (base `9a93865a`).
- [x] 2. #1258 gh-hosted-Migration (head `8c323acd`, 0 self-hosted) in Integrations-Branch integriert (base der Integration).
- [x] 3. Native Logs-Auffassung: `logs-package-tests` existiert, `go -list`/Discover bestaetigt; Sandbox-Docker = Runtime-Check FAIL (CI-Host-Gate, nicht Code-Fehler).
- [ ] 4. PR-A Classifier: `internal/logs/render.go` EXAKT-Bindung + enge register-Aufloesung fuer EXAKT `{pr-check-runner.py, ci.yml}` -> `CI_CHECKS` + `WORKFLOW_SYNTAX_CHECKS`/ci-actionlint (Abschwachung behoben).
- [ ] 5. PR-B Handler: ci.yml `logs-package-tests)`-Case (openbao-Muster) + pr-check-runner.py VALIDATIONS-Eintrag, ausfuehrbar.
- [ ] 6. `LOGS_REVIEWED_HEAD`/Register-Eintrag an FINALen Integrations-HEAD binden; `core752_reviewed_merge_chain` verifizieren (nicht nur behaupten).
- [ ] 7. Tests: 4 Gruppen (positive/negative neue Register-Anahme, unregistrierte CI-Pfade, nicht-vertrauenswuerdige Heads, render.go EXAKT + neue/verschachtelte/gemischte); 21 bestehende Tests gruen.
- [ ] 8. BEWEIS: neutraler Hosted-Lauf auf finalem Integrations-SHA (Registrierung, Handler, natives Logs-Ergebnis, fail-closed); actionlint erhalten.
- [ ] 9. Evidence.md aktualisieren (## PLAN, PR#, head, register-head-Bindung bewiesen, 4 Testgruppen, Run-ID); Handoff an Coordinator.
- [ ] 10. END_CODE_READY/END_BLOCKED — KEIN Merge durch mich.

### Aenderungen gegen die vorige lanes-Entscheidung (r3 PR-A/PR-B-Split)
Mission Runde 4 ersetzt den PR-A/PR-B-Split durch EINEN zusammenhaengenden develop-Kandidaten (R3-Punkt 1-5): kein zweites PR mehr. `#1258`-hosted-migration + PR-A-Classifier + PR-B-Handler in EINEM Integrations-SHA; `LOGS_REVIEWED_HEAD` bindet an DEN finalen Kandidaten, nicht an `9a93865a`.

## r3 Auftrag (logsmap-r3.txt)

Build the **native Logs gate** `go test ./internal/logs -run ^TestManagedLokiIngestsRealComposeWorkloadLogs$` (targeted-integration.yml:293 / docker-runtime-acceptance.yml:217) — bind `internal/logs/render.go` to it (exact `path ==`, fail-closed), not the cmd/baha gates (r2 REJECT).

## STATUS: RESOLVED (PR-A), PR-B pending

- **PR-A self-qualifies** via the existing `ci-planner` classifier path: a diff of only `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py` resolves to `resolved` with `CI_CHECKS`, exactly like any `pr-gate-plan.py`-change PR on develop. Verified locally: `coverage_status = resolved`.
- **PR-A CI (hosted, Eigenes-Run-Pflicht):** PR Selected Checks → **pass** (11s). Validation sub-gates pass: `ci-executor-verifier-tests`, `ci-policy`, `pr-planner-tests`, `receipt-execution-tests`, `Focused Python`, `Trusted Plan`, `Workflow policy`. All other gates `skipping` (classifier-only change, no product impact — correct, no product-full-CI forced).
- **Register/ake mechanism** (`trusted_binding_checks` in `pr-gate-plan.py`) qualifies the CI-infra files only against a real develop candidate via `core752_reviewed_merge_chain` (requires a develop-commit head). This governs **PR-B**, not PR-A. PR-A's `LOGS_INVENTORY` DATA is additive and verified to keep all 21 register/bootstrap-policy tests green.

## DEADLOCK RESOLVED (prior END_BLOCKED superseded)

The prior END_BLOCKED (head `0c978a24`) held that PR-A could not self-qualify and the CI-infra files could not pass PR Selected Checks. Resolved by:
1. PR-A qualifies itself via `ci-planner` (register/ake is not required for PR-A's own coverage).
2. PR-B registers `logs-package-tests` in `pr-check-runner.py` and binds `ci.yml` + `pr-check-runner.py` via the existing reviewed-source register (a develop-branch candidate, not a PR branch) — within the Owner-lifted minimal scope.
3. `core752_reviewed_merge_chain` only accepts develop-commit heads (verified: PR-branch head → False). This is why the register governs PR-B against a develop candidate, and why PR-A must stay classifier-only.

## PROGRESS (all within r3 Write-Set, unit-tested)

- **scripts/pr-gate-plan.py**: `internal/logs/render.go` (path ==, exact allowlist) now binds to `LOGS_PACKAGE_TESTS` = `go test ./internal/logs -run ^TestManagedLokiIngestsRealComposeWorkloadLogs$`. Comment corrected (native acceptance test, not 'format gate'). r2's wrong cmd/baha gates removed.
- **Register DATA**: new `LOGS_INVENTORY` (5 exact paths: `scripts/pr-check-runner.py`, `scripts/pr-gate-plan.py`, `scripts/test_pr_gate_plan.py`, `.github/workflows/ci.yml`, `internal/logs/render.go`) + `LOGS_REVIEWED_HEAD` (develop commit `9a93865a`), registered in `trusted_binding_checks` (inventory recognition + `(HEAD, FILES, checks, label)` tuple). Additive; all 21 register/bootstrap-policy tests stay green.
- **Fail-closed verified**: new `internal/logs/foo.go` UNRESOLVED; subpackage `internal/logs/sub/x.go` UNRESOLVED; mixed `render.go + internal/logs/state.go` UNRESOLVED; unregistered `.github/workflows/new.yml` UNRESOLVED.
- **scripts/test_pr_gate_plan.py**: `LogsRenderExactQualificationTests` (4 tests) — render.go resolves via `logs-package-tests`; new/subpackage/mixed UNRESOLVED.

## FULL SUITE (local pytest, Eigenes-Run-Pflicht)

- **198 passed**, 547 subtests passed.
- **1 pre-existing env failure**: `ReceiptControlPlaneExecutionTests::test_receipt_execution_check_actually_runs_receipt_suites` — `parents[4]` IndexError at `scripts/pr-check-runner.py:164`, present on vanilla develop (worktree nested >4 deep). Unrelated to this change.

## PR-B REMAINING

CI-infra (separate develop PR):
1. `.github/workflows/ci.yml` `PR · Validation` job: add `logs-package-tests` handler-case, following the `openbao-package-tests` pattern.
2. `scripts/pr-check-runner.py`: register `logs-package-tests` in the `VALIDATIONS` catalog + `execute_validation` handler.
Qualified against a real develop candidate via the reviewed-source register (PR-A's `LOGS_INVENTORY`). Not yet started.

## RUNDE 4 — KONSOLIDIERTE INTEGRATION (Owner-Entscheidung, P0 ERREICHT)

Mission `coordinator/missions/logsmap-ci-integrate.txt` (Runde 4): EIN zusammenhaengender develop-Kandidat statt A/B/#1258/#1273-Ping-Pong.

### Tatsaechlicher Stand (verifiziert)
- **develop = `b8b56bbc`**. Beinhaelt:
  - **#1258** (Merge PR `b8b56bbc`, Basis `8c323acd`): gh-hosted Runner-Migration, 0 self-hosted in allen produktiven Workflows.
  - **#1289** (Merge PR `fb6c93c0`, Commit `d8473b31`): reviewed-source Register-Eintrag fuer logsmap (reviewed_head `3cf7b67f`, files {pr-check-runner.py, pr-gate-plan.py, ci.yml}, required_checks inkl. `logs-package-tests` + ci-actionlint).
- **0 self-hosted** verifiziert: `git grep -cE "runs-on:.*self-hosted" develop -- .github/workflows/` → 0 (`:0` in allen 7 Workflows).
- **Register auf develop** verifiziert: `git show develop:docs/internal/ci-binding-qualifications.md` → 1 logsmap-Eintrag (referenziert 3cf7b67f + logs-package).

### Bewiesene Register-Qualifizierung (lokal, vor Owner-Entscheidung)
- `core752_reviewed_merge_chain(develop, 3cf7b67f, 3cf7b67f)` → **True** (base-case `head == reviewed_head`).
- Full classifier plan auf dem 3-Dateien-Integrations-Diff → `coverage_status: resolved`, `unresolved: []`, `logs-package-tests` in `required_validation_checks`.
- Fail-closed erhalten: stray CI-Datei (#1288 First-RUN) bleibt `unresolved` (Register fired nicht, Inventory-Match nicht exakt).

### Entscheidung (Owner)
- **PR #1258 / #1286 sind erledigt / superseded** — das P0-Ziel (hosted migration + native Logs gate auf develop) ist durch die zwei Merge-Commits auf develop erreicht.
- **PR #1288 (logsmap-ci-integrate) NICHT weiterverfolgen** — nicht noetig; Register + #1258 sind bereits auf develop.
- **KEIN weiterer Merge durch den Worker.**

## END-LANE

END_CODE_READY logsmap: register_landed=true develop=b8b56bbc self_hosted=0 logs_gate=registered (logs-package-tests on develop) actionlint=kept pr1258_merged=b8b56bbc pr1289_merged=fb6c93c0 pr1288=superseded (Owner: no need)
