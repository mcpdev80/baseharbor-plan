# PR #1753 independent review

## PLAN

1. Verify the instructed hop from `50c4bce74d2d269cd985b3e66ac51fc879e0d627` to the live head and pin the current develop base.
2. Review the exact `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9...d690d7ffd4d55f1562c2c106d1424b8c0088ca6c` diff, inspect the `ce5cf8f` operator seam change, and verify exact-head hosted tests and native-runtime state without local tests.
3. Record the verdict, validate and publish evidence to Planning `origin/main`, update the live board, and post END to the Coordinator.

## Session mark

CODEX-REVIEW; read-only. No local tests, product changes, GitHub review/comment, merge, close, or workflow rerun.

## Verdict

**APPROVE** for PR #1753 exact head `d690d7ffd4d55f1562c2c106d1424b8c0088ca6c`, against `develop` `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9`.

The earlier additivity concern is resolved for this review by the refreshed mission explicitly authorizing inspection of `ce5cf8f30373e13c0d08092d84b24232e93a356a`. The requested hop is now exact and clean: comparison `c463edf...d690d7f` is ahead by 3, behind by 0, with merge base exactly `c463edf...`; only `cmd/baha/ci_integration_operator_enabled.go` and `cmd/baha/ci_integration_operator_enabled_test.go` differ from develop. Those changes directly implement and test the card’s footprint-show operator boundary, not unrelated work.

At final verification the PR was OPEN with `mergeStateStatus=CLEAN`; its live head matched the reviewed SHA. Review decision was blank. The PR file list has no `.github/**` or `scripts/**` paths.

## Operator-boundary review

`cmd/baha/ci_integration_operator_enabled.go:138-147` admits the footprint probe only when the selected `gate` is `data-capabilities` and the args match `ciIntegrationDataCapabilitiesFootprintShow`. That helper at lines 242-249 delegates to the canonical exact matcher requiring `app footprint show -o json`. The existing guided exception remains separately guarded by `gate == "guided"` at lines 135-137.

The regression `TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate` at `cmd/baha/ci_integration_operator_enabled_test.go:352-419` verifies canonical admission and scoped operator receipt on data-capabilities, rejects alternate spellings/forms and unrelated commands, preserves guided admission, and rejects lifecycle admission. The new code and test are the test-side operator seam for the card’s footprint-show behavior; the PR does not modify `cmd/baha/app_footprint_show.go` itself.

## Exact hosted evidence

- Run `44993125398` is terminal `completed / success` for exact head `d690d7ffd4d55f1562c2c106d1424b8c0088ca6c`.
- `PR · Validation · ci-integration-operator-seam-tests`, job `137118399949`, completed SUCCESS. Its log shows `go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^TestCIIntegrationOperator' -count=1 -v` and `--- PASS: TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate`.
- `PR Selected Checks`, job `137119427586`, completed SUCCESS. The run had 15 successful jobs and 21 skipped jobs; skipped jobs are not counted as passes.
- `PR · Selected Runtime`, job `137118401195`, was SKIPPED. `PR · Native · ${{ matrix.id }}`, job `137118368689`, was SKIPPED. This is the expected state before #1756 adds the data-capabilities catalog rows and is not a rejection reason under the handoff.
- `PR · Native gate plan`, job `137118338010`, completed SUCCESS. The test behavior is independently covered by the successful operator-seam validation job above.

## Scope and provenance

The live `refs/pull/1753/head` was `d690d7ffd4d55f1562c2c106d1424b8c0088ca6c`; live `refs/heads/develop` was `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9`. The compare reports `ahead_by=3`, `behind_by=0`, and merge base `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9`. The compare’s three commits are the `ce5cf8f` card-specific operator change, the mechanical hop through `50c4bce`, and the merge of current develop at `d690d7f`.

No workflow or planner files were edited by this candidate. The current PR diff contains only the two operator source/test files listed above.

## Planning validation and cleanliness

`python3 scripts/plan.py check`: 0 errors, 10 existing dependency warnings.

Planning repository remote verified before publication:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

`docker ps -a` before: PID 2905099; no containers listed.

`docker ps -a` after: PID 2906969; no containers listed. No review-owned containers or compose projects were started.

## END

END codex-rev-1747 DONE: APPROVE for `d690d7ffd4d55f1562c2c106d1424b8c0088ca6c`; the `ce5cf8f` operator/test change is card-specific, not foreign work; run `44993125398` terminal SUCCESS; `PR · Selected Runtime` SKIPPED as expected. Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.

## Planning publication witness

Fresh `origin/main` tree output:

```text
evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-headd690d7ffd4d5.md
```
