# #1853 Hosted route verdict

## PLAN

1. Inspect Hosted pull_request run job lists for this repository and era (per_page=100); identify a run showing planner and executor semantics.
2. Verify whether the two-suite planner command and CI_EXECUTION_SUITES execute test_pr_gate_coverage.py and test_pr_ci_fallback.py; capture exact job names and output evidence.
3. Record a GO/NO-GO one-line verdict with job citations in planning evidence and deliver it to the coordinator; no repository changes.

## Scope

Read-only review of Hosted job evidence for #1853. No product or workflow repository changes.

## Hosted evidence and verdict

- #1853 PR run `45699482849` was a `pull_request` run on head `030e58489389b12f1684eb1c50cebc86a276cf9d`. Job `PR · Validation · ci-executor-tests` (`139505586492`) executed 225 tests, including `test_pr_ci_fallback.py` cases, but failed `test_planner_validation_route_includes_planner_and_coverage_suites` because the workflow command contained only `test_pr_gate_plan.py` and `test_pre_release_runtime_reuse.py`, while the expectation included four suites.
- Green same-era PR run `45711869496` on #1850: `PR · Validation · ci-executor-tests` (`139548148860`) succeeded and its `matched_tests` included `test_pr_ci_fallback.py` but not `test_pr_gate_coverage.py`; `PR · Validation · pr-planner-tests` (`139548148916`) succeeded with the actual command `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pre_release_runtime_reuse.py`, a two-suite route. `PR · Focused Python` also executed `python3 scripts/test_pr_ci_fallback.py`.
- Hosted logs for these runs do not show execution of `test_pr_gate_coverage.py`; the route regression in 45699482849 is explicitly red. Therefore the combined claim that both named files execute through the current two-suite planner route plus `CI_EXECUTION_SUITES` is not proven.

**NO-GO —** #1853 Hosted evidence does not prove both files execute: `PR · Validation · ci-executor-tests` ran `test_pr_ci_fallback.py` but its matched list omits `test_pr_gate_coverage.py`; `PR · Validation · pr-planner-tests` ran only the two-suite command.

END_DONE w136-pr1836-rowsreview: #1853 route verdict delivered as NO-GO on candidate `030e58489389b12f1684eb1c50cebc86a276cf9d`.

## Publication identity and base

- Current card owner VERBATIM from plan `origin/main` (`c66cab2e1e513255aa1990721b7275a51c0ce45d`): `w205 (lane w205-0428-253)`.
- Planning remote verified: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Evidence commit identity: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): record #1853 hosted route verdict'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.
- The evidence update is on a branch cut from plan `main` at `c66cab2e1e513255aa1990721b7275a51c0ce45d`; ancestry must be verified before commit.

## Final scope ruling — current head 228ecc5bab28e5e6158ccc63160f442a6afc9ed3

This addendum supersedes the current-head implication of the earlier NO-GO line. That NO-GO was tied to the old head 030e58489389b12f1684eb1c50cebc86a276cf9d and its two-suite route. It remains valid history for that old candidate only.

**FINAL GO for scope and route** on current head 228ecc5bab28e5e6158ccc63160f442a6afc9ed3. The owner-authorized path is the exact four-suite command at `.github/workflows/ci.yml:1363`, required by card 0428-253's planner-route coverage and expressly authorized by the owner line directing `pr-planner-tests` to match `pr-gate-plan.py` CI_CHECKS, including `test_pr_ci_fallback.py`. This is narrow authorization for that route only, not general workflow-edit authority.

Hosted confirmation on the exact current head:

- Distinct run 45716254159, attempt 1, event pull_request, terminal SUCCESS; `PR · Validation · pr-planner-tests` job 139563055289 and `PR Selected Checks` job 139563707682 both succeeded. Its job log shows the four-suite command and `Ran 49 tests ... OK`. Attempt 2 on the same run ID is cancelled and is void as a separate run; it does not erase the successful attempt 1 evidence.
- Distinct run 45717496553, attempt 1, event pull_request, terminal SUCCESS; `PR · Validation · pr-planner-tests` job 139567483027 and `PR Selected Checks` job 139568337781 both succeeded. Its log shows the same four-suite command and `Ran 49 tests ... OK`.
- These are two different run IDs on the same exact head. No new trigger was initiated in this disposition.

The final disposition is therefore GO; w233 may proceed without another trigger solely to establish the route. Any separate acceptance, review, or merge criteria remain independent.

END w136-pr1836-rowsreview DONE

## Addendum publication provenance

- Exact plan `origin/main` base before this addendum: `ea9f7ab6583542ab3bd1b782e7652585ca567d04`. `git merge-base --is-ancestor ea9f7ab6583542ab3bd1b782e7652585ca567d04 HEAD` completed with exit 0.
- `git show -s --format=%an HEAD` printed `w136-pr1836-rowsreview`.
- Before publication, `git log --oneline origin/main..HEAD` listed only `13e973661 docs(evidence): finalize #1853 route ruling`.
