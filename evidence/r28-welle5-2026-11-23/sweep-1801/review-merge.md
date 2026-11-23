# PR #1801 review and merge

Role: REVIEW, then MERGE only if all acceptance criteria pass.

## PLAN

- 372. Read the #1801 review contract and create the numbered plan in the live board and Planning evidence.
- 373. Resolve the GitHub remote and verify PR #1801 exact head, base, current draft state, diff, and current develop.
- 374. Review the app_edit.go and test-only diff against card 0428-257; verify no consent, fail-closed, provider, or workflow changes.
- 375. Verify the on-screen acknowledgement reflects the toggle state and inspect the exact test execution route.
- 376. If scope checks pass, perform the authorized gh pr ready action and observe its new exact-head pull_request run through terminal TP and PR Selected Checks.
- 377. Merge normally only if the exact-head named test receipt and all other criteria pass; otherwise record an exact repair recipe.
- 378. Verify remote outcome, record cleanliness, validate and publish evidence, update the board, and post END.

## Review findings

- GitHub product remote was resolved as `https://github.com/mcpdev80/baseharbor.git` before other Git actions. Planning repository remote was verified before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- The initially reviewed exact head was `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`, based on `develop` `304b3ad1d88647377ea647d0d94174bfc9298e14`. While run 45154911807 was executing, the PR head advanced by merging current develop. The final exact head is merge commit `ff81c5a17ba0ba6c1f784773302497771ab089d8`; its parents are prior candidate `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c` and develop `f6ab22b7dc9793ccd2872cb7717402816561c401`.
- Final remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1801/head`:
  - `f6ab22b7dc9793ccd2872cb7717402816561c401 refs/heads/develop`
  - `ff81c5a17ba0ba6c1f784773302497771ab089d8 refs/pull/1801/head`
- Live PR state at final review: OPEN, ready for review, base `develop` at `f6ab22b7dc9793ccd2872cb7717402816561c401`, head `ff81c5a17ba0ba6c1f784773302497771ab089d8`, not merged. `gh pr ready 1801` had succeeded as directed; the pull_request run for the updated head was run 45157306258.
- The updated-head PR diff still has three paths: `cmd/baha/app_edit.go` (+6), `cmd/baha/app_edit_apply_test.go` (+54), and `cmd/baha/app_wizard_controller.go` (+17), for 77 additions and zero deletions. The contract allows only `app_edit.go` and its test. `app_wizard_controller.go` remains an out-of-scope file, so merge is not authorized.
- `app_edit.go` captures the kind before `SelectNeed` and prints `<kind> selected` or `<kind> deselected`. `TestReview918SpaceToggleAcknowledgesOnScreen` checks both toggle directions. The added controller helpers supply the pre-toggle state but reside outside the allowed write-set. No changes were found to consent, fail-closed behavior, provider selection, or `.github/**`.
- The linked hunt evidence identifies F5 at `cmd/baha/app_edit.go:283` and recommends a one-line status acknowledgement there. Card 0428-257 requires a minimal fix in the named file and no side changes. Repair recipe: remove the `app_wizard_controller.go` change and implement the acknowledgement using the in-scope `app_edit.go` surface, with the regression retained in `app_edit_apply_test.go`; if the controller helper is necessary, obtain an explicit write-set correction and submit the corrected candidate for a new review.
- Exact-head CI run 45157306258 was triggered by `pull_request` for `ff81c5a17ba0ba6c1f784773302497771ab089d8`. It reached terminal `success`. `PR · Trusted Plan` job 137636814651 passed; `PR · Validation · wizard-app-edit-tests` job 137636924913 passed; selected Docker lifecycle job 137637625078 and selected Docker data-capabilities job 137637625087 both passed; terminal `PR Selected Checks` job 137645497479 passed. The aggregate reports `pr_runtime_selected: success`; native selected integration, Podman, and Go unit shards were skipped/not selected (`unit_scope: none`). These skipped jobs are not counted as passes.
- The named test receipt is missing. The exact-head `wizard-app-edit-tests` job log shows its `cli-guided-tests` invocation as `go test ./cmd/baha -run '^TestGuided' -count=1`; this does not match `TestReview918SpaceToggleAcknowledgesOnScreen`. Searching that exact-head job log for the new test name returned no match. The validation job's success therefore does not prove execution of the required regression test.
- The earlier ready-triggered run 45154911807 was for the superseded head `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`; its overall conclusion was cancelled after the PR advanced. It is not used as final-head evidence. Its selected aggregate and runtime jobs had reported success, but the current-head run above is the relevant terminal run.
- No local tests were run. No workflow edit, manual rerun, or workflow_dispatch was used. The only PR mutation was the explicitly directed `gh pr ready 1801` action. No merge was performed.

## cleanliness

- Before: PID 1869877; `docker ps -a` showed only the header, with no containers.
- After: PID 1951770; `docker ps -a` showed only the header, with no containers. No local Docker or Podman workloads were started.

## repo-rule compliance

- Review was read-only against the product repository. The evidence file is in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, the actual Planning repository, not in `workers/` or a product repository.
- Evidence uses plain bullets and contains no Markdown checkbox lines.
- Merge was withheld because both the write-set and exact named-test receipt criteria fail. The PR remains open and unmerged.

## Verdict

VERDICT: REQUEST CHANGES — do not merge PR #1801.

END DONE codex-rev-1747: REQUEST CHANGES #1801; out-of-scope controller file and missing exact named-test receipt; no merge SHA.

## Published evidence path witness

evidence/r28-welle5-2026-11-23/sweep-1801/review-merge.md
