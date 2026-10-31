# codex-rv1227 — independent review

ROLLE: REVIEW  
UTC: 2026-10-31T02:04:37Z  
Verdict: REQUEST_CHANGES

## PLAN

- Done: 0. Read coordinator policies and mission. Native TodoWrite is unavailable; the mission file does not specify a PLAN step 0.
- Done: 1. Verify exact candidate and base in an isolated worktree.
- Done: 2. Review candidate and q253 / rv1221b–g evidence.
- Done: 3. Run required checks and verify worktree after review.
- Done: 4. Record verdict and publish after Planning validation.

## Findings and worker recipe

1. **Production API fails for every compare.** `.github/workflows/receipt-post-run.yml:191,203` uses `BASE..HEAD`; authenticated `gh api repos/mcpdev80/baseharbor/compare/72ba7a99ff7dcd4b04ee3cf16516991ef567d376..bcf4ca8ccbd6ac0c636fdab356b9cb9211fa4bd5` returned HTTP 404, rc=1. The same request using `BASE...HEAD` returned rc=0 and the four changed filenames. The workflow therefore fails closed even for valid eligible and non-producer PR runs. The test stub accepts the invented two-dot path, so its positive tests cannot prove the committed API works. Worker: use the documented three-dot endpoint for both calls; test actual endpoint construction using a real-contract fixture or bounded authenticated read-only smoke, plus positive and failed lookups.
2. **Completeness remains unproved, allowing phantom skip.** Lines 184–219 claim pagination proves a complete file set, but [GitHub's compare API documentation](https://docs.github.com/en/rest/commits/commits#compare-two-commits) limits changed files to 300 on the first page even with pagination. A contracts change omitted after that limit could be classified absent; checking that a separate response begins with `[` does not prove completeness. Previous rv1221d/e/f findings are not closed by the narrow rv1221g pass. Worker: derive a provably complete immutable base/head file set or fail closed when completeness cannot be established; validate full JSON types and pagination, including >300 files with omitted contracts touch, truncation, and error negatives.
3. **Mandatory local suite fails.** `scripts/test_receipt_tasklink.py:1395–1512` failed its real Planning validator test with empty diagnostics; the test runs the clone's plan.py with `--root`, then prints render stdout and stderr rather than check output. Worker: diagnose and correct this test against the actual committed Planning API, preserve full output and negative control, and ensure clone/ref failures cannot silently count as coverage; rerun the required suite.

Separate integration prerequisite: #1225 remains OPEN, head 5060cb236ffdc8248f07663f6ccac22fd0e45b66. On this candidate `python3 scripts/pr-check-runner.py execute --check resolver-package-tests --repository .` returned rc=1, `ValueError: unsupported executable validation`; planner selects the ID at `scripts/pr-gate-plan.py:395`. Resolve via the independently reviewed executor fix before merge readiness. Stop until corrected candidate, independent exact-head review and applicable mandatory CI all pass.

## Exact candidate and cross-check

Product worktree: `/home/marcel/dev/baseharbor-ecosystem/baseharbor/worktrees/codex-rv1227`; pwd checked. Before and after: clean `git status --porcelain`, HEAD `bcf4ca8ccbd6ac0c636fdab356b9cb9211fa4bd5`; `git merge-base --is-ancestor 72ba7a99ff7dcd4b04ee3cf16516991ef567d376 HEAD` rc=0. HTTPS `git ls-remote` and `gh pr view` agree PR #1227 OPEN, head bcf4ca8ccbd6ac0c636fdab356b9cb9211fa4bd5 and develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376. Run 41087310166 authenticated payload has that run head and PR association base/head. Hosted PR Selected Checks and selected jobs report success, ten jobs skipped; these do not exercise a post-run compare against the live endpoint. The run-bound base extraction and differing-base negative address the narrow rv1221f drift finding, but do not close the above broader gaps.

## Checks

The requested `/home/marcel/tmp-ops` cache location is outside this session's writable roots: mkdir returned `Read-only file system` (rc=1). Fallback caches were set to `/tmp/codex-rv1227/{go,py}`; no product files changed.

- `PYTHONPATH=scripts PLANNING_CLONE_ORIGIN=/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan PLANNING_CLONE_REF=main python3 -m pytest -q scripts/test_receipt_postrun.py scripts/test_receipt_tasklink.py scripts/test_receipt_verifier.py`: rc=1, **1 failed, 239 passed, 2 skipped** in 20.21s. Failure: `TestEvidenceEditDesign.test_real_plan_check_runs_on_production_planning`, AssertionError `real plan.py render+check failed on minimal note`, empty reported RENDER/CHECK diagnostics.
- `bash scripts/ci-workflow-policy.sh`: rc=0, `Workflow policy PASS: 22 approved workflow files.`

## repo-rule compliance

Independent read-only product review; no product code change, merge, protection or label change. Planning publication limited to this dossier. Native TodoWrite unavailable; the durable plan above records actual work. The requested cache path could not be written under the sandbox. No claim or task status changed.

END codex-rv1227 REVIEW-DONE
