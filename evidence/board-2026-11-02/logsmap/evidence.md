# logsmap — Native Logs gate (PR #1286, r3): END_CODE_READY (PR-A green, PR-B pending)

**Lane:** logsmap (Worker) · **Coordinator:** f49a3303 (Qwen Flash)
**Modell:** worker-ornith1.5 · **ornith-Host**
**Datum:** 2026-11-02
**Branch:** `classifier-logs-map`
- **PR-A (this lane, DONE):** head `5fe5208b` — classifier + register data, PR #1286 → develop, CI green.
- **PR-B (pending):** CI-infra (`ci.yml` `logs-package-tests` handler-case + `pr-check-runner.py` registration).
**End-LANE:** **END_CODE_READY** for PR-A — classifier self-qualifies, CI Selected Checks pass. PR-B is the remaining split (Owner-Stop lifted for the minimal `pr-check-runner.py` registration).

### Owner-Entscheidung (lifts the prior END_BLOCKED)
Owner-Stop is lifted **only** for the minimal `pr-check-runner.py` registration of `logs-package-tests` (the ONLY runnable path for the native gate). No blanket CI-file reclassification. Split into two develop PRs:
- **PR-A** = `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py` only. PR-A qualifies itself via the existing `ci-planner` path (like any `pr-gate-plan.py`-change PR on develop) — register/ake entries are DATA in `pr-gate-plan.py`, no develop-commit authorship needed.
- **PR-B** = CI-infra: `ci.yml` `logs-package-tests` handler-case + `pr-check-runner.py` `logs-package-tests` registration, following the `openbao-package-tests` pattern.

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

## END-LANE

END_CODE_READY logsmap: pr_a=1286 head_a=5fe5208b develop=9a93865a classifier=resolved pr_b=pending
