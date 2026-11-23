# PR #1805 post-merge review

ROLE: REVIEW
Card: t-20261121-static-gate-registration (0428-208), supersedes #1746.
Reviewer session: codex-rev-1747, session fecbada9-9fd8-4df4-9305-d49b53a6e7a7, model GPT-6-Luna.
Review date: 2026-11-23.

## PLAN

1. Read the #1805 mission and record its role, exact candidate/base, acceptance checks, and evidence path.
2. Refresh the authorized GitHub refs and inspect the exact PR diff and current review/merge state.
3. Verify the named CI receipts and each task acceptance criterion against authoritative evidence.
4. Issue the literal review verdict and actionable repair recipe for any failed criterion.
5. Publish review evidence only in baseharbor-plan with remote and cleanliness witnesses.
6. Tick the board, confirm evidence on origin/main, and post the required END.

## scope and provenance

- Product repository: https://github.com/mcpdev80/baseharbor.git. Planning repository: https://github.com/mcpdev80/baseharbor-plan.git.
- Planning `git remote -v` witness: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; push URL is the same GitHub repository.
- PR #1805 exact candidate head: `76ad7a733797d86ab7e0d878d1afe4bb1ddd20ed`.
- PR base SHA: `f3d84787462f324a6311e2e95928441c64a09296`.
- PR #1805 is closed and merged. GitHub reports merge commit `fdced23de19866d9cdc435c009c9c069350dffb5`; `develop` currently resolves to that SHA. The PR head remains the stated candidate at `refs/pull/1805/head`.
- The recorded owner-takeover witness in `evidence/r28-welle5-2026-11-23/sweep-1746/owner-takeover.md` identifies `51ff183bfdcceaa4b383281a5c68421d1b770814` as an ancestor of the candidate. GitHub compare independently showed that same commit as the merge base of the candidate; the PR base `f3d84787462f324a6311e2e95928441c64a09296` is included in its ancestry. The candidate was squash-merged, so it is not claimed as an ancestor of the resulting develop commit.
- The resolved product remotes `lane-origin`, `origin`, and `upstream` all point to `https://github.com/mcpdev80/baseharbor.git`; only that URL was used for remote truth. No PR mutation, review submission, merge, workflow dispatch, or rerun was performed by this reviewer.
- GitHub PR file listing contains exactly these 15 paths: `.github/workflows/pre-release-runtime-suite.yml`, `.github/workflows/pre-release.yml`, `CHANGELOG.md`, `docs/releases/v0.4.28.demo-ref`, `scripts/ci-fast-check.sh`, `scripts/pr-gate-coverage.json`, `scripts/pr-gate-plan.py`, `scripts/pre-release-check-plan.py`, `scripts/pre-release-runtime-impact.json`, `scripts/release-requirements.json`, `scripts/test_ci_v0427_gate_catalog.py`, `scripts/test_pr_gate_coverage.py`, `scripts/test_pre_release_check_plan.py`, `scripts/test_pre_release_runtime_reuse.py`, `scripts/validate-pr-gate-coverage.py`. `.github/workflows/ci.yml` is not in the diff.

## acceptance review

- Fail-closed behavior is retained. `scripts/pr-required-final.py` preserves the error `selected gate has no workflow executor`; `scripts/test_pr_required_final.py` tests that an unknown atomic static gate still has no executor and remains rejected. The test appears in both the `PR · Focused Python` job and the `PR · Validation · ci-executor-tests` receipt.
- The 1797 routing gap is closed in source: `.github/workflows/pre-release-runtime-suite.yml` has an explicit `ci-fast-check` case invoking `bash scripts/ci-fast-check.sh`. `.github/workflows/pre-release.yml` passes the selected static gate through to the reusable runtime suite. The selector fails closed if a catalog gate lacks registration in both the static catalog and runtime dispatch.
- `scripts/test_pre_release_check_plan.py` asserts the v0.4.28 atomic static requirements include `atomic/static/ci-fast-check` and `atomic/static/mcp`, checks the selector output and direct workflow executor, and retains the unknown-gate rejection test.
- Exact-head pull_request run: workflow run `45194909490` (#7517), head `76ad7a733797d86ab7e0d878d1afe4bb1ddd20ed`, terminal conclusion success. The `PR Selected Checks` aggregate completed success; no active or failed jobs remained. The job listing includes skipped jobs, which are not counted as passing evidence.
- Named executed receipts: `PR · Focused Python` succeeded; its log reports `Ran 24 tests ... OK`, including `scripts/test_pr_required_final.py`. `PR · Validation · ci-executor-tests` succeeded and its `matched_tests` receipt lists `test_pr_required_final.py` and `test_pre_release_check_plan.py`. `PR · Validation · pr-planner-tests` succeeded; logs report 45 tests and then 221 tests, both OK.
- Remaining acceptance gap: no exact-candidate Pre-Release Runtime Suite run was observed that executes `atomic/static/ci-fast-check` together with the pre-existing static gates. The PR pull_request run is not that release qualification: the generic `PR · Selected Runtime` job was skipped, and the release-only static gate itself did not execute. The task contract for 0428-208 requires live same-candidate evidence for the existing static jobs plus the new gate; catalog and routing tests alone do not satisfy that positive runtime criterion.

## verdict

REQUEST CHANGES

The code-level checks pass: unknown gates remain fail-closed, the new gate has a real workflow executor, and the named exact-head Python/validation jobs are green. Task acceptance remains unproven because there is no live release-suite receipt demonstrating the new static gate and existing static gates together. Since #1805 is already merged, this is a post-merge acceptance finding; it is not a request submitted to the closed PR and it does not authorize another workflow run.

Repair recipe: on the next owner-authorized v0.4.28 Pre-Release Runtime Suite execution at the merged `develop` SHA `fdced23de19866d9cdc435c009c9c069350dffb5`, preserve the terminal run/job receipts showing `atomic/static/ci-fast-check` and each pre-existing static gate executed and passed in the same qualification. If any gate is skipped, missing, or fails, leave 0428-208 unaccepted and record the exact job and failing log line; do not infer success from the selector or PR checks.

## remote witnesses

- Product GitHub `ls-remote` after review: `fdced23de19866d9cdc435c009c9c069350dffb5 refs/heads/develop`; `76ad7a733797d86ab7e0d878d1afe4bb1ddd20ed refs/pull/1805/head`.
- Planning GitHub `ls-remote` before publication: `5cf1249cdf8ec26475c14f38746246dea71dec31 refs/heads/main`.
- Planning delivery witness after the first evidence push: `40b59ef97b5fbf03c24cad0747ed4612c54f589a refs/heads/main`.
- Exact output of `git fetch origin main && git ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1805/review-merge.md$'`:
  `evidence/r28-welle5-2026-11-23/sweep-1805/review-merge.md`

## repo-rule compliance

- Review-only; no product changes and no local test run. Evidence is written only in the actual `baseharbor-plan` repository.
- No `.github/**` edits, workflow dispatch, reruns, merge, or PR review submission.
- No subagents used.
- No local evidence checklists; the plan is a numbered list.

## cleanliness

- Before review, PID 4166129: `docker ps -a` returned only the header; no containers were present.
- After review, PID 4175647: `docker ps -a` returned only the header; no containers were present. This session started no containers or compose projects.
- Planning worktree began on `main` at `5cf1249cdf8ec26475c14f38746246dea71dec31`; no unrelated worktree changes were staged or included.

END codex-rev-1747 BLOCKED
