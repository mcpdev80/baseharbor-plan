# PR #1801 review and merge

Role: REVIEW, then MERGE only if all contract criteria pass.

## PLAN

- 372. Read the #1801 review contract and create the numbered plan in the live board and Planning evidence.
- 373. Resolve the GitHub remote and verify PR #1801 exact head, base, current draft state, diff, and current develop.
- 374. Review the app_edit.go and test-only diff against card 0428-257; verify no consent, fail-closed, provider, or workflow changes.
- 375. Verify the on-screen acknowledgement reflects the toggle state and inspect the exact test execution route.
- 376. If scope checks pass, perform the authorized gh pr ready action and observe its new exact-head pull_request run through terminal TP and PR Selected Checks.
- 377. Merge normally only if the exact-head named test receipt and all other criteria pass; otherwise record an exact repair recipe.
- 378. Verify remote outcome, record cleanliness, validate and publish evidence, update board, and post END.


## Review findings

- Review role is REVIEW. MERGE role was not entered because the exact write-set fails the contract.
- Product repository remote verification, first Git action: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push).
- Exact remote witnesses from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1801/head`: develop `304b3ad1d88647377ea647d0d94174bfc9298e14`; PR head `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`.
- Live PR #1801 is OPEN, base `develop` at `304b3ad1d88647377ea647d0d94174bfc9298e14`, head `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`. It was draft on inspection. The explicitly authorized `gh pr ready 1801` succeeded; the PR remains at the same head and is no longer draft.
- Exact candidate diff contains three paths: `cmd/baha/app_edit.go` (+6), `cmd/baha/app_edit_apply_test.go` (+54), and `cmd/baha/app_wizard_controller.go` (+17); 77 additions, zero deletions. The contract allows only `app_edit.go` and its test. The controller file is an out-of-scope change and blocks merge.
- The `app_edit.go` change reads the selected kind before `SelectNeed` and emits a selected/deselected acknowledgement afterward. Test `TestReview918SpaceToggleAcknowledgesOnScreen` covers the acknowledgement direction. The added controller helpers are not in the allowed write-set. No changes were found to consent, fail-closed behavior, provider selection, or `.github/**`.
- The linked hunt evidence identifies the F5 symptom at `cmd/baha/app_edit.go:283` and recommends a one-line status acknowledgement there; card 0428-257 requires a minimal fix in the named file and no side changes. Repair recipe: remove `cmd/baha/app_wizard_controller.go` from the candidate and implement the needed acknowledgement using the existing in-scope surface in `cmd/baha/app_edit.go`, retaining the focused regression in `cmd/baha/app_edit_apply_test.go`; if the controller helper is essential, obtain an explicit write-set correction and re-review that corrected contract.
- No local tests were run. The focused GitHub CI job is `PR · Validation · wizard-app-edit-tests` (job 137625416438) on exact-head pull_request run 45154911807; it completed success. Its exact named-test log receipt is pending terminal run log availability.
- `gh pr ready` caused pull_request run 45154911807 at exact head `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`, created 2026-11-23T10:18:39Z. `PR · Trusted Plan` job 137625283228 succeeded and reported `previous source/base ancestry not proven; reused validations=0; reused runtime gates=0`. Workflow policy, native gate plan, source format and focused wizard app edit tests passed. Selected Docker lifecycle job 137626091451 completed success. Docker data-capabilities job 137626091354 remains in progress; terminal `PR Selected Checks` aggregate has not yet been observed. Draft run 45152943243 is not counted: the selected checks were skipped there.
- Review-process constraint: no workflow edits, manual reruns, or workflow_dispatch were used. The ready action above was expressly required by the review contract.

## cleanliness

- Before: PID 1869877; `docker ps -a` output was only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`); no containers were present. No local Docker or Podman workloads were started.
- After: pending final evidence update.

## repo-rule compliance

- Evidence is in the actual Planning repository `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, not under `workers/`. Its verified remote is `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- The candidate was inspected read-only; no product-repository files were changed. Evidence contains plain bullets and no Markdown checkbox lines.
- Merge decision is withheld because the PR diff exceeds the task write-set. No merge was performed.

## Verdict

VERDICT: REQUEST CHANGES — do not merge PR #1801.

END BLOCKED codex-rev-1747: REQUEST CHANGES #1801; controller file is outside the allowed write-set; exact-head run 45154911807 still in progress; no merge SHA.
