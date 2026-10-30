ROLLE: CODEX-REVIEW

## PLAN
1. erledigt: 0. Read dispatch and binding policies; record plan. Native TodoWrite unavailable.
2. erledigt: 1. Refresh candidate and review resolver executor mapping and negative coverage.
3. erledigt: 2. Run focused tests and verify exact-head checks, threads and rules.
4. erledigt: 3. Merge only if acceptance and mandatory gates pass; verify develop and checks.

## ROLLE: CODEX-REVIEW

Verdict: REQUEST_CHANGES. Reviewed head de0e50646a5694033da7685f7e687e162022ffd0 against develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376 in detached /tmp/review1225/deep/worktrees/product. HTTPS ls-remote witnessed both. Net diff touches only scripts/pr-gate-plan.py and scripts/test_pr_gate_plan.py; contrary to dispatch it does not change the trusted runner or CI workflow dispatch.

1. Required real resolver gates remain unsupported. scripts/pr-check-runner.py:90-98 has no resolver IDs, and :112-119 rejects them. Direct `python3 scripts/pr-check-runner.py execute --check resolver-package-tests --repository .` fails `ValueError: unsupported executable validation`. No resolver case exists in .github/workflows/ci.yml. Worker recipe: register each planner-selected resolver check in the trusted execution path and CI dispatch, ensure the implementation runs the real check against the candidate, and test planner output through the actual executor and selected-check gate.
2. scripts/pr-gate-plan.py:796-810 creates a separate matrix without validating IDs against the executor registry; a single unknown string is accepted. test_pr_gate_plan.py:928-962 only asserts planner.matrix output and checks duplicate phantom IDs, not one unique unknown ID or actual execution. Worker recipe: remove the misleading parallel matrix or bind it to the trusted executor; add unique unknown/unresolved negative tests and an end-to-end test that proves every mapped ID is executed, not merely named. Stop until independent review and exact-head mandatory CI pass.

Local MappingTests: 35 passed; direct receipt postrun: 13 passed. These tests do not repair the executor gap. Exact-head hosted run 41056092451: PR Selected Checks SUCCESS app 15368, selected Python/validation jobs successful, non-selected skipped. Threads empty; develop required-check ruleset 25223521 active, integration ruleset 23754541 disabled, main active; none changed.

## repo-rule compliance
Read-only product review; no product changes, approval, protection change or merge. Coordinator reminders remain unresolved.

## ROLLE: CODEX-MERGE

BLOCKED by the requested executor and fail-closed criteria. No merge; post-merge checks inapplicable.

END rv1225 DONE
