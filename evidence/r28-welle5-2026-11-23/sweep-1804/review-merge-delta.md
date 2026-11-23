# PR #1804 post-merge review delta

ROLE: REVIEW
Card: t-20261123-wizard-org-default-usageerror (0428-258).
Reviewer session: codex-rev-1747, session fecbada9-9fd8-4df4-9305-d49b53a6e7a7, model GPT-6-Luna.
Review date: 2026-11-23.

## PLAN

1. Read the #1804pm mission and record its role, exact candidate/base, acceptance checks, and evidence path.
2. Refresh authorized remote refs and inspect exact PR/diff/task state required by the mission.
3. Verify specified review, CI, ancestry, and acceptance evidence from authoritative sources.
4. Record the literal verdict and actionable recipe for any unmet criterion.
5. Publish review evidence only in the actual baseharbor-plan repository.
6. Confirm the published evidence path, tick this board, and post the required END.

## merge and candidate witnesses

- Product GitHub remote: `https://github.com/mcpdev80/baseharbor.git`. Planning repository: `https://github.com/mcpdev80/baseharbor-plan.git`.
- Planning `git remote -v` witness: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; the push URL is the same GitHub repository.
- PR #1804 was merged by auto-merge at `2026-11-23T15:12:30Z`. PR API reports base SHA `fdced23de19866d9cdc435c009c9c069350dffb5`, head `74175064c3dbf540d25086fcff485aa0e0ced874`, and merge commit `7e09afc382c21dda6cc2b741a4ef4e4ada173d80`.
- Fresh product `git ls-remote` at review: `7e09afc382c21dda6cc2b741a4ef4e4ada173d80 refs/heads/develop`; `74175064c3dbf540d25086fcff485aa0e0ced874 refs/pull/1804/head`.
- The exact PR diff is four paths: `cmd/baha/app_new_wizard.go`, `cmd/baha/app_new_wizard_org_default_test.go`, `scripts/pr-check-runner.py`, and `scripts/pr-gate-plan.py` (17 additions, 2 deletions). No `.github/**` path changed.
- No product change, PR review submission, merge, workflow dispatch, rerun, or local test was performed by this reviewer.

## run and test evidence

- Pull request run #7519, run ID `45198327048`, is `completed / success` on exact head `74175064c3dbf540d25086fcff485aa0e0ced874`. `PR Selected Checks` check run `137789325837` is completed success, from GitHub Actions integration `15368`.
- `PR · Validation · wizard-app-new-tests`, job `137774812506`, completed success. Its `matched_tests` receipt lists the `TestAppNewWizard...` cases but does not print these three org-default IDs: `TestGuidedStackProfileOrgDefaultMissingStackUsageError`, `TestGuidedStackProfileOrgDefaultPresentStackResolves`, and `TestOrgDefaultStackNotInCatalog`. I do not treat that receipt as direct name evidence for those three.
- The exact candidate source contains all three tests in `cmd/baha/app_new_wizard_org_default_test.go`. None of their test bodies calls `t.Skip`.
- The candidate's `scripts/pr-go-unit-shard.py` uses the first eight SHA-256 bytes of the test's shard key, big-endian, modulo four; only the separate owner-loan regression cohort is remapped to a file key. These three tests are outside that cohort. Reproducing the candidate's mapping gives:
  - `TestGuidedStackProfileOrgDefaultMissingStackUsageError` -> `cli-1`, job `137774812222`.
  - `TestGuidedStackProfileOrgDefaultPresentStackResolves` -> `cli-2`, job `137774812439`.
  - `TestOrgDefaultStackNotInCatalog` -> `cli-3`, job `137774812236`.
- The three mapped pull_request shard jobs all completed success on the exact candidate. Their logs report `PASS cli-1: 454 passed / 10 intentionally skipped / 464 discovered; CLI inventory total=1916`, `PASS cli-2: 469 passed / 24 intentionally skipped / 493 discovered; CLI inventory total=1916`, and `PASS cli-3: 449 passed / 17 intentionally skipped / 466 discovered; CLI inventory total=1916`. The shard executor verifies each selected test has a run event and ends either passed or skipped before emitting PASS; these three specific bodies have no skip branch.
- Classification: the dedicated wizard matched-tests receipt omits the three names, so the proof is package-only. The exact name-to-shard mapping plus successful owner-shard receipts follows the #1606 package-receipt precedent recorded in `evidence/r28-welle5-2026-11-23/sweep-1723/review-merge-delta.md`; this is valid execution evidence for these ordinary Go tests and resolves the named-log omission.

## current selector and usageError review

- On merged `develop` SHA `7e09afc382c21dda6cc2b741a4ef4e4ada173d80`, `scripts/pr-check-runner.py:26` includes `^TestGuidedStackProfile` and `^TestOrgDefault` in `wizard-app-new-tests`. The tests' names match those patterns.
- `scripts/pr-gate-plan.py:206` maps `cmd/baha/app_new_wizard_org_default_test.go` to `wizard-app-new-tests`.
- Current `cmd/baha/app_new_wizard.go` passes `fmt.Sprintf("organization default stack %q is not available in the effective stack catalog", name)` to `usageError`. The `%q` is expanded before `usageError` receives the message; the regression test asserts the message contains the quoted `"ghost"` value and does not contain a literal `%q`.

## verdict

APPROVE-delta

The three org-default tests are covered by successful exact-head CLI package receipts under the documented #1606 method, despite their absence from the dedicated wizard receipt's `matched_tests` list. The current selector and file-to-check route are correct, and the merged error message expands the stack name before creating the `usageError`.

## repo-rule compliance

- Review only. No product code or Planning task metadata was changed; evidence is confined to the actual Planning repository.
- No `.github/**` edits, workflow dispatch, rerun, or PR mutation.
- No subagents were used. No local test was run.
- Evidence uses plain numbered plan steps and plain bullets, with no Markdown checkbox lines.

## cleanliness

- Before review, PID `66331`: `docker ps -a` returned only the header; no containers were present.
- After review, PID `74011`: `docker ps -a` returned only the header; no containers were present. This session started no containers or compose projects.
- A neighboring tracked artifact at `evidence/r28-welle5-2026-11-23/sweep-1804pm/review-merge.md` was restored byte-for-byte from `origin/main` after the exact mission path was read; it is not part of this review change.

END_DONE codex-rev-1747: APPROVE-delta for merged PR #1804; exact-head run 45198327048 passed and the three org-default tests map to passing cli-1/cli-2/cli-3 package receipts on 74175064c3dbf540d25086fcff485aa0e0ced874.
