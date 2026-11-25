# #1842 final current-head review

## PLAN

1. Re-read the final-review mission and capture the four-step review/merge plan before repository inspection.
2. Verify the exact PR head/base/parents, five changed paths, corrected pin/body, author identity, and two distinct Hosted PR runs with job-level logs.
3. Review the full candidate diff and card contract; record ACCEPT and merge only if all required changed tests actually ran in Hosted CI.
4. Record the exact review result, #1812 sequencing consequence, and final #1853 scope ruling.

## Scope and decision

Independent exact-head review of BaseHarbor PR #1842 for card 0428-284. No product changes and no CI dispatches were made. Review verdict: CHANGES, recorded as GitHub review COMMENTED id 6066220597 on commit 5d9965944ff6cd265cbd5d042d59cf522b38b76d. No merge was executed.

The substantive blocker is test-to-CI reachability. The PR modifies scripts/test_pr_gate_coverage.py with 156 added lines, but neither qualifying run executed that file. In run 45716226824, PR · Validation · pr-planner-tests job 139562948542 logged the command `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pre_release_runtime_reuse.py`; PR · Focused Python job 139562948211 invokes scripts/test_pr_check_runner.py and scripts/test_pr_ci_fallback.py; ci-executor-tests job 139562948406 also lists test_pr_ci_fallback.py, but not test_pr_gate_coverage.py. Run 45717078703 showed the same two-suite planner command in job 139565887122, and the same coverage file is absent from all executed test commands. The successful PR Selected Checks aggregates do not prove execution of this changed regression suite.

Fix recipe: with workflow-owner authorization, add scripts/test_pr_gate_coverage.py to the existing Hosted planner-test command at .github/workflows/ci.yml:1363; then require two distinct full pull_request SUCCESS run IDs on the corrected exact head. No rerun was triggered by this review. PR · Demo Pin was skipped in both runs; the pin value was independently confirmed, but this review does not count the skip as execution.

## Exact-head evidence

- PR #1842 is open, ready (draft=false), mergeable=true, merge_state=clean. Candidate head is 5d9965944ff6cd265cbd5d042d59cf522b38b76d; PR base and current develop were both ae70964d7b80b779822b76107b70ea76782f998e.
- Candidate parents are 996fe5ffa0afd81ffcd864ba23e6e4da4c5f5e52 and ae70964d7b80b779822b76107b70ea76782f998e. Candidate author and committer are both w198-0428-284-demo-parser, matching the card owner.
- Exact PR paths: docs/releases/v0.4.28.demo-ref; scripts/pr-check-runner.py; scripts/pr-gate-plan.py; scripts/test_pr_check_runner.py; scripts/test_pr_gate_coverage.py.
- The pin file and corrected PR body both name 5ca92a7cd2f746934890cfd7096a48068bdf218e. Demo develop resolves to that commit.
- Runs 45716226824 and 45717078703 are distinct pull_request run IDs, both terminal SUCCESS on this exact head. Each had 39 jobs terminal with zero failures and PR Selected Checks SUCCESS (jobs 139565153006 and 139567718240). Required-check ruleset 25223521 is active and requires PR Selected Checks from integration 15368. The changed coverage regression file nevertheless was not executed, as detailed above.
- No PR review objects existed before this review. GitHub review COMMENTED id 6066220597 is the exact-head CHANGES verdict. Merge withheld.

## Scope wording and sequence

For #1842, “pin-file only” evidence means the pin value is independently correct; it does not mean the PR has one changed path. The accepted payload description still has five paths, including release-aware scripts/tests. #1812 remains unaccepted and must absorb the eventual #1842 merge tip before its own requalification.

#1853 scope ruling: FINAL GO for the current 228ecc5bab28e5e6158ccc63160f442a6afc9ed3 scope only; the four-suite route at .github/workflows/ci.yml:1363 is explicitly owner-authorized. Run 45717496553 is a distinct terminal-success pull_request run on that head, and job 139567483027 executed all four suites including test_pr_gate_coverage.py and test_pr_ci_fallback.py. Run 45716254159 attempt 2 is void/cancelled; attempt 1 is the other distinct green cited by the owner. This is not blanket authorization for workflow edits.

## Visible identity and base attestation

0428-284 card owner verbatim from plan origin/main: `w198-0428-284-demo-parser`.
Evidence commit identity: user.name `w136-pr1836-rowsreview`; user.email `w136-pr1836-rowsreview@baseharbor.local`.
Literal commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): record #1842 review disposition'`.
Pre-push identity gate: `git show -s --format=%an HEAD` must print `w136-pr1836-rowsreview`.
Planning remote witness: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`.
Plan base at worktree creation: 132ee736b0fabfb55a2f8488ae25b677be5f35f1 (origin/main); this was the exact fetched ref used to create the isolated worktree.

END w136-pr1836-rowsreview DONE
