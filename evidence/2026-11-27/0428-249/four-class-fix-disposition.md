# ROLLE: REVIEW — four CI failure-class disposition for 0428-249

## Decision and boundary

The accepted 0428-249 edit set remains the exact 14 evidence-workflow files in `qualification-workflow-integrity.md:17-34`, with its resolver and evidence-job contract in `:9-15,36-160,226-253`. The independent ACCEPT authorizes implementation of that bounded set only (`workflow-integrity-review.md:89-98`). This disposition does not authorize editing CI policy, executor, actionlint configuration, planner, or production scripts.

The two test files `scripts/test_ci_check_routes.py` and `scripts/test_pr_selected_runtime_matrix.py` may receive narrow test-only fixture/assertion updates when they encode the old workflow shape. This is a purpose-bound addition to make the accepted resolver/SHA behavior testable, allowed by AGENTS.md §1's explicit rule for additions needed to fulfill an approved card. Record it here and in the implementation handoff; do not weaken assertions or broaden the test surface. No other Python test file is included.

## Disposition by failure class

| Reported class | Authorized repair | Stop condition |
| --- | --- | --- |
| Workflow policy | Fix the offending YAML or expression only in one of the 14 accepted workflow files, preserving the approved triggers, selected-check graph, and exact-SHA/non-cancelling requirements. Use the terminal policy log's file and line. | If the policy failure requires changing the policy checker, executor, protected workflow inventory, or adding an unapproved workflow/path, stop and report the exact log line. Do not relax the policy. |
| `ci-actionlint` | Correct only the action/workflow syntax at the cited line in an accepted workflow file. Keep action SHAs and gate semantics. | Do not change actionlint configuration, suppress a finding, or edit a file outside the 14-file list. |
| `ci-executor-tests` | First classify the exact failing assertion. If it is a test-only expectation/fixture for the approved resolver output, exact checkout, or run-unique group, update only the two named test files above and retain positive and negative assertions. | If the test exposes a defect in executor/policy implementation or requires changing `scripts/pr-check-runner.py`, `scripts/pr-gate-plan.py`, another executor, or production code, this card does not authorize that change; stop and request a separately scoped disposition. |
| Focused Python | If the terminal traceback is in `scripts/test_ci_check_routes.py` or `scripts/test_pr_selected_runtime_matrix.py` and the only mismatch is the old workflow shape, update the relevant fixture/assertions to require the resolver output and independent gate/runtime group. | Preserve checks that unrelated changes do not expand selection, that the selected-check aggregator remains base-plan-owned, and that each relevant job depends on/checks out the verified candidate. No broad expectation replacement or deletion of coverage. |

## Evidence status and handoff

At this read, PR #1812 remote head was `6ab5310d17358bc0f4c86ef09bea476b82517e3e`. Runs `45930995254` and `45931118156` were still in progress, so their job failure names were visible but terminal failure logs were unavailable. The four-class disposition is therefore conditional on the terminal job/step log; it is not an acceptance of the reported fixes or a finding that the four failures are resolved.

The shared w362 worktree at the same read had three **unstaged** changes: `targeted-demo-acceptance.yml`, `supplemental-release-validation.yml`, and `targeted-integration.yml`; it had no staged diff. Do not describe those edits as staged until `git status` confirms that state. The late workflow edits and both allowed test-file changes require inclusion in one coherent exact-head candidate and fresh Hosted validation; existing runs on earlier heads cannot qualify them. No tests or edits were run by this reviewer.

## Explicit fixture ruling — 2026-11-27T03:24:27Z

**YES: w362 may include test-only fixture/assertion corrections in its next forward commit; it does not need to wait for the baseline family to make those two test files align with the approved workflow contract.** The owner confirms commit `8c83c709` contains no fixture changes, so those edits are still outstanding and no earlier run validates them. The allowed test-only paths are exactly `scripts/test_ci_check_routes.py` and `scripts/test_pr_selected_runtime_matrix.py`; update only the fixtures/assertions that encode the old ref/check-out or concurrency shape, retain coverage, and do not edit executor/policy implementation or other scripts. If the terminal logs show an actual executor implementation failure rather than a stale test expectation, this permission does not apply: stop and report it separately. These limits supplement, and do not enlarge, the named 0428-249 authority in `workflow-integrity-review.md:89-98` and the evidence contract in `qualification-workflow-integrity.md:9-15`.
