# PR #1753 exact-head review

Session mark: CODEX-REVIEW (read-only)
Task: t-20261122-footprint-show-not-admitted-in-data-capabilities-gate (0428-227)

## PLAN

1. Read the redirected #1753 native-gate review scope and capture its exact head, base, hosted run, required gate receipts, and read-only boundaries.
2. Verify the live PR head/base, exact terminal hosted run, native/runtime gate execution, and additive develop-only hop without running local tests.
3. Record a SHA-specific verdict and receipts, validate and publish this evidence to Planning origin/main, verify the evidence path, update the live board, and post END to the Coordinator.

## Review state

- Product GitHub remote: `https://github.com/mcpdev80/baseharbor.git`.
- PR #1753 state: OPEN; head `a40b76764c3c08ec690e723def0ca167ce989c2b`; base `develop` at `52a3c5446f41a1dd8678d99875e4cb1eee67874c`; `mergeStateStatus=BLOCKED`.
- GitHub compare `52a3c544...a40b767`: `ahead_by=4`, `behind_by=0`, merge base exactly `52a3c5446f41a1dd8678d99875e4cb1eee67874c`.
- Previous reviewed head: `d690d7ffd4d55f1562c2c106d1424b8c0088ca6c`.
- Additive comparison `d690d7f...a40b767`: the only newly added product files are `scripts/ci-native-pr-gate.sh`, `scripts/pr-gate-coverage.json`, `scripts/test_pre_release_runtime_reuse.py`, and `scripts/validate-pr-gate-coverage.py`, from the #1756 develop merge. The PR's task diff remains exactly `cmd/baha/ci_integration_operator_enabled.go` and `cmd/baha/ci_integration_operator_enabled_test.go`.
- Exact-head hosted run: `44994268323`, workflow `CI · Source & Quality`, event `pull_request`, SHA `a40b76764c3c08ec690e723def0ca167ce989c2b`, terminal conclusion `failure`. `PR Selected Checks` job `137124048433` also concluded failure. Five failed jobs total: the two Native matrix jobs, the two Selected Runtime jobs, and `PR Selected Checks`.
- Focused exact-head validation `PR · Validation · ci-integration-operator-seam-tests`, job `137121841608`, succeeded.
- Native gate plan job `137121803257` succeeded. Native matrix length was two: `native/podman/data-capabilities`, job `137121839379`, and `native/docker/data-capabilities`, job `137121839425`. Both executed and failed; neither was skipped.
- Selected Runtime matrix length was two: Podman `data-capabilities`, job `137122169299`, and Docker `data-capabilities`, job `137122169353`. Both executed and failed; neither was skipped.

## STATE

Per the workflow-failure reporting boundary, stop review at these failed exact-head checks; no rerun, workflow dispatch, PR update, or source change was made.

- `PR · Native · native/podman/data-capabilities` (job `137121839379`): `TestApplicationCapabilityLifecycleExistingCore/secrets` failed; logged `[FAIL] Starting secure runtime broker - failed (4m57s)` and `--- FAIL: TestApplicationCapabilityLifecycleExistingCore/secrets (314.35s)`. The associated log reports readiness unhealthy / HTTP 503.
- `PR · Native · native/docker/data-capabilities` (job `137121839425`): `TestApplicationCapabilityLifecycleExistingCore/secrets` failed; logged `Starting secure runtime broker: application runtime broker readiness failed: application runtime broker container health is unhealthy` and `--- FAIL: TestApplicationCapabilityLifecycleExistingCore/secrets (145.53s)`.
- `PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) / Executed podman · data-capabilities` (job `137122169299`): log line `RuntimeError: actual native CLI JSON/MCP Footprint contracts differ`; summary lines `demo-data-capabilities       FAIL` and `RESULT                       FAIL`. The preserved original failure is `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`.
- `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities` (job `137122169353`): log line `RuntimeError: actual native CLI JSON/MCP Footprint contracts differ`; summary lines `demo-data-capabilities       FAIL` and `RESULT                       FAIL`. The preserved original failure is `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`.
- `PR Selected Checks` (job `137124048433`): log reports `NATIVE_RESULT: failure` followed by `##[error]Process completed with exit code 1.`

## Verdict

HOLD. The additive hop is develop-only and behind count is zero, but the exact terminal hosted run failed in selected Native and Selected Runtime gates. The prior approval at `d690d7f` does not cover these newly executed failing receipts.

merge-empfehlung: HOLD; do not merge until the failed exact-head checks are resolved and a new exact-head run is terminal.

## Planning remote

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Cleanliness

- Shell PID `2975405`; `docker ps -a` before review and after review returned only the header and no containers.
- No containers or compose projects were started.

## END codex-rev-1747 BLOCKED

PR #1753 exact head `a40b76764c3c08ec690e723def0ca167ce989c2b`; HOLD due terminal run `44994268323` failure with five failed jobs, including executed Native and Selected Runtime matrices; Planning evidence remote verified above.
