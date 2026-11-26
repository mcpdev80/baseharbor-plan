# w136 admission ruling: PR #1853 / card 0428-253

## PLAN

1. Preserve the exact prior admission ruling and author witnesses.
2. Append the owner-authorized CI test-mapping line as a request to the owner; make no workflow change.
3. Publish this evidence through the isolated plan PR flow.

## Prior ruling

Conditionally admit the two historical `w205` commits as commits of card lane `w205 (lane w205-0428-253)` only under this narrow exception: the plan-main claim binds the card to that lane; the named commits are explicitly enumerated; no commit history is rewritten; the lane-qualified tail is present and has exact author and committer identity; and every commit added after that tail uses the exact canonical lane string.

- Canonical owner in the verified prior plan snapshot: `w205 (lane w205-0428-253)`.
- Claim commit: `201fb31ab73a7d08359140c30577bcdfeee2ca54`.
- Historical candidate commits `90c8017b2363aef0f75aea481cd147883b312a22` and `3c1ebc6fcb71334a85a32601939de1d128de56ba` have author and committer `w205`.
- Lane-qualified tail `4ca3f46508b4b006c1fffbe7766fbe4c386e9e27` has author and committer exactly `w205 (lane w205-0428-253)`.
- This admission ruling does not clear the separate planner test mapping issue; no product workflow modification was made.

## Owner authorization line

authorize ci.yml:1363 pr-planner-tests command to match pr-gate-plan.py CI_CHECKS (4 suites incl. test_pr_ci_fallback.py)

This is an owner authorization/request line only. It does not claim that `.github/workflows/ci.yml` has been changed or that the requested suites have run.

## Evidence identity and base

- Card owner VERBATIM from prior verified plan main: `w205 (lane w205-0428-253)`.
- Evidence author: `w136-pr1836-rowsreview <w136-pr1836-rowsreview@baseharbor.local>`.
- Literal invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): append #1853 admission authorization'`.
- Pre-push gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.
- Evidence branch base: `46f7fcb0ab7c417a2f8fbebe518caf1cd6b5421a refs/heads/main`.

## Owner decision update

- Owner ruling: commits `90c8017b` and `3c1ebc6f` are admitted as the same-lane shortened identity (`w205` equals `w205-0428-253`); no rewrite and no evidence loss. This admission does not clear the independent `ci.yml:1363` scope finding and does not authorize merge. Candidate remains at `4ca3f465` until the owner workflow edit lands; normal exact-head Hosted review is still required.
- The exact requested owner line remains: `authorize ci.yml:1363 pr-planner-tests command to match pr-gate-plan.py CI_CHECKS (4 suites incl. test_pr_ci_fallback.py)`.
- Local pre-push state: `bash scripts/ci-fast-check.sh` failed at `scripts/test_ci_check_routes.py:216`, test `test_planner_validation_route_includes_planner_and_coverage_suites`. The assertion reports the current command has only `scripts/test_pr_gate_plan.py` and `scripts/test_pre_release_runtime_reuse.py`, while the expected command also includes `scripts/test_pr_ci_fallback.py` and `scripts/test_pr_gate_coverage.py`. This is a workflow-scope owner action; I made no workflow edit and stopped publication.

## Current-head and Hosted-run owner update

- Fresh PR census shows #1853 current head `030e58489389b12f1684eb1c50cebc86a276cf9d`, not `4ca3f465`; the admission exception applies only to historical commits `90c8017b` and `3c1ebc6f`.
- Hosted run `45699482849` is a completed pull_request FAILURE on exact head `030e5848`. `PR · Focused Python` failed at `scripts/test_ci_check_routes.py:216`, `test_planner_validation_route_includes_planner_and_coverage_suites`: the workflow command is missing `scripts/test_pr_gate_coverage.py` and `scripts/test_pr_ci_fallback.py` from the four-suite planner contract. `PR · Validation · ci-executor-tests` also failed on the same route assertion; `PR Selected Checks` failed. No re-trigger is authorized until the owner CI edit lands.
- There is no genuine scripts-only fix that preserves the route contract: `ci.yml:1363` explicitly invokes only two modules, while `scripts/pr-gate-plan.py:748-754` defines four. Reducing `CI_CHECKS` or indirectly importing the missing tests would weaken or obscure the real executed route.
- Explicit owner authorization request, with no edit performed: authorize changing `.github/workflows/ci.yml:1363` so the `pr-planner-tests` command matches `scripts/pr-gate-plan.py` `CI_CHECKS`: `scripts/test_pr_gate_plan.py`, `scripts/test_pre_release_runtime_reuse.py`, `scripts/test_pr_gate_coverage.py`, and `scripts/test_pr_ci_fallback.py`. The already-recorded owner authorization line is retained as requested; this ruling does not perform the workflow change and does not authorize merge.

## Route-verification correction at exact head 030e5848

- Exact changed files on PR #1853 head `030e58489389b12f1684eb1c50cebc86a276cf9d` are seven scripts files only; `.github/workflows/ci.yml` is unchanged.
- Workflow `ci.yml:1362-1363` invokes the two existing planner suites (`test_pr_gate_plan.py` and `test_pre_release_runtime_reuse.py`). At the candidate head, `pr-check-runner.py:109-119` registers both `test_pr_ci_fallback` and `test_pr_gate_coverage` under `CI_EXECUTION_SUITES`; `pr-check-runner.py:231-249` runs each registered module in `ci-executor-tests` and checks module execution after a successful suite.
- Hosted run `45699482849` confirms `PR · Validation · ci-executor-tests` did execute `test_ci_check_routes` and `test_pr_ci_fallback` tests, but failed at `test_planner_validation_route_includes_planner_and_coverage_suites` (`scripts/test_ci_check_routes.py:216`). The same test failed in `PR · Focused Python`; `PR · Selected Checks` is red. The log does not show named `test_pr_gate_coverage` cases, and the runner's successful per-module presence guard was not reached because the suite failed. Thus the split route is in-scope by design, but this run is not qualifying execution proof for the coverage suite.
- Route ruling: GO for the scripts-side split route, NO-GO for accepting current head `030e5848`. Amend `scripts/pr-gate-plan.py` so `CI_CHECKS['pr-planner-tests']` command exactly matches the two-suite command already in `ci.yml:1363`; amend `scripts/test_ci_check_routes.py:186-223` to validate the split honestly (two modules on the planner job; both added modules in `CI_EXECUTION_SUITES`; executor command/selection remains required). Do not change `.github/**`. Then obtain a new exact-head Hosted run with Focused Python, `ci-executor-tests`, and PR Selected Checks terminal green; require the executor output/per-module assertion to prove both suites ran.
- No owner workflow-scope request is needed for this route. No rerun was requested or triggered by this review; the current run remains red. The earlier statement that there was no in-scope route is superseded by this verification.

## Correction block — w306-0428-253-rulingdoc, 2026-11-26T06:36Z (Owner ruling of 2026-11-26 06:36Z, forward-only append)

This block only adds precision. No existing line above is deleted, reworded or superseded away.

- ADMITTED SET: the shortened same-lane identity exception (`w205` equals `w205-0428-253`) admits exactly the commit set {`90c8017b2363aef0f75aea481cd147883b312a22`, `3c1ebc6fcb71334a85a32601939de1d128de56ba`} and nothing else. No other commit is admitted under this exception.
- REJECTION BOUNDARY: any other commit carrying a shortened, role-suffixed or foreign lane identity (for example bare `w205`, `wNNN-coordinator`, or another lane's registered name) is NOT admitted, and its PR must be HOLDed pending a forward provenance paragraph; no rewrite.
- FUTURE IDENTITY: future commits by any lane touching PR #1853 or card 0428-253 must use the canonical string `w205-0428-253` in BOTH author and committer, set per-command via `git -c user.name='w205-0428-253' -c user.email='w205-0428-253@baseharbor.local' commit ...`.
- LIVE GITHUB WITNESSES (re-read with `gh` by lane w306-0428-253-rulingdoc at 2026-11-26T06:38Z): PR #1853 is MERGED (`merged_at` 2026-11-25T23:57:23Z, merge commit `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`, final head `228ecc5bab28e5e6158ccc63160f442a6afc9ed3`). The final exact-head review ACCEPT is recorded in the issue comment "Final #1853 exact-head review — ACCEPT" dated 2026-11-25T23:57:20Z on head `228ecc5ba` (there is no `REVIEWED`-state reviews-API entry; the GitHub reviews API shows only two `COMMENTED` entries). Two distinct terminal runs on the same exact head `228ecc5ba`: pull_request run `45716254159` (attempt 1 SUCCESS, its `PR Selected Checks` aggregate succeeded; its attempt 2 was cancelled and is void as evidence) and pull_request run `45717496553` (attempt 1 SUCCESS, `PR Selected Checks` success). Both `PR Selected Checks` outcomes are SUCCESS on the exact head.
- NO HISTORY REWRITE: this ruling records admissions and boundaries forward-only; the repository history of PR #1853 is unchanged.
