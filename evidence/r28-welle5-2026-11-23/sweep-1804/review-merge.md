# PR #1804 correction-round review

ROLE: REVIEW
Session: codex-rev-1747, ID fecbada9-9fd8-4df4-9305-d49b53a6e7a7, GPT-6-Luna (screen-reported model)
Review time: 2026-11-23

## PLAN

1. Read `/tmp/opencode/m_rev_1804.md.g` and verify candidate, exact base, run, scope, and required evidence.
2. Refresh the authorized GitHub remote, PR refs, exact diff, and terminal run #7507.
3. Compare formatting and test assertions with existing app-init and app-prune usage conventions.
4. Issue the literal review verdict and an actionable repair recipe if any criterion fails.
5. Publish this review only in the actual Planning repository with remote and cleanliness witnesses.
6. Tick the live board and post the matching END verdict.

## Mission and candidate

The mission assigns read-only REVIEW for PR #1804 at head `854c7cefff1e4483b2885026b91354944312522f`, against exact base `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb` (develop). No product changes, PR mutation, merge, or workflow action was performed.

PR state observed through GitHub API: open, not draft, not merged. Exact compare reports `ahead`, one commit, zero behind; merge base is `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb`. The complete changed-file list is:

- `cmd/baha/app_new_wizard.go`
- `cmd/baha/app_new_wizard_org_default_test.go`

## Review findings

The production correction is correct and minimal: `guidedStackProfile` now passes `fmt.Sprintf("organization default stack %q ...", name)` to `usageError`, so the message interpolates and quotes the organization default stack name. The test asserts that the message contains the quoted `"ghost"` and excludes literal `%q`. The patch contains no catalog or `.github/**` changes.

The production formatting follows the requested conventions. `app_init_prompts.go:399` uses `usageError(fmt.Sprintf("... %q ...", line), ...)`; `app_prune.go:299` uses the same formatted-message convention. The new multiline call in `app_new_wizard.go:508-511` is semantically and stylistically consistent.

Blocking CI coverage finding: run #7507 is bound to exact candidate `854c7cefff1e4483b2885026b91354944312522f`, completed successfully, and its terminal `PR Selected Checks` aggregate succeeded at 2026-11-23 13:25:18 UTC. Job `PR · Validation · wizard-app-new-tests` (job ID `137714484816`) also completed successfully. However, its own receipt output lists `matched_tests` and omits `TestGuidedStackProfileOrgDefaultMissingStackUsageError`, the test function containing the added regression assertions. Thus the green job did not execute the test changed by this PR; the test-to-CI gate requirement is unmet.

Repair recipe: rename the test function to a name beginning `TestAppNewWizard`, for example `TestAppNewWizardOrgDefaultMissingStackUsageError`, to match the existing selector `scripts/pr-check-runner.py:26` (`wizard-app-new-tests`: `^TestAppNewWizard`). Run the resulting exact candidate through CI and confirm the job receipt explicitly lists and executes this test with success. Do not treat a green job whose receipt omits this test as coverage.

## Repo-rule compliance

This was a read-only review. I did not run local package tests, edit product code, change `.github/**`, dispatch or rerun workflows, alter PR state, merge, or start containers. The only writes are this review evidence and the required live board progress entry. Candidate identity and CI evidence were independently read from GitHub. `python3 baseharbor-plan/scripts/plan.py render && python3 baseharbor-plan/scripts/plan.py check` was run; render completed, but check exited 1 with `error: tasks/t-20261123-wizard-org-default-usageerror.md: resolution is only valid on a checked card` (698 tasks, 7 epics, 13 releases, 24 decisions; 1 error, 10 warnings). The task card currently has `kanban_status: active` and `resolution: accepted`; I left this planning-card state unchanged because this mission assigns review-only and the acceptance-state correction is outside the review evidence write set. The final verdict is REQUEST CHANGES because the changed regression assertion was absent from its named CI receipt.

## Remote witnesses

Product GitHub remote resolved from `git remote -v`: `lane-origin` points to `https://github.com/mcpdev80/baseharbor.git` (other listed product remotes also resolve to this same authorized owner/repository). Planning remote verified before evidence publication: `origin https://github.com/mcpdev80/baseharbor-plan.git`.

Before review:

```text
ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb	refs/heads/develop
854c7cefff1e4483b2885026b91354944312522f	refs/pull/1804/head
```

After review:

```text
ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb	refs/heads/develop
854c7cefff1e4483b2885026b91354944312522f	refs/pull/1804/head
```

The PR API also still reports head `854c7cefff1e4483b2885026b91354944312522f`, base `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb`, open, not merged.

## CI receipt

Run #7507, run ID `45180964447`: head `854c7cefff1e4483b2885026b91354944312522f`, event `pull_request`, completed `success`. Named job `PR · Validation · wizard-app-new-tests`, job ID `137714484816`: completed `success`. Run-level aggregate `PR Selected Checks`: job ID `137723729471`, completed `success` at 2026-11-23 13:25:18 UTC. The validation log receipt named check `wizard-app-new-tests`, but its `matched_tests` array did not include `TestGuidedStackProfileOrgDefaultMissingStackUsageError`; this is the blocking gap.

## Cleanliness

Before review, `docker ps -a` was run by PID `2531703`; output contained only the header and no containers. After review, `docker ps -a` was run by PID `2536537`; output contained only the header and no containers. No compose project was started.

## VERDICT

REQUEST CHANGES

Required correction: route the changed regression test through the existing `wizard-app-new-tests` validation by renaming it to match `scripts/pr-check-runner.py:26` (`^TestAppNewWizard`), then provide an exact-head CI receipt whose `matched_tests` includes and executes it successfully. The code fix and requested two-file scope otherwise pass review.

END codex-rev-1747 DONE — REQUEST CHANGES for `854c7cefff1e4483b2885026b91354944312522f`.


## Published evidence path witness

Command: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep '^evidence/r28-welle5-2026-11-23/sweep-1804/review-merge.md$'`

Exact command output:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/r28-welle5-2026-11-23/sweep-1804/review-merge.md
```
