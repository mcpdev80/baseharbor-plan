# CODEX-REVIEW PR #1419 r6

## PLAN

1. Read the r6 mission and verify fresh exact PR head/base remote SHAs.
2. Inspect the exact candidate delta and determine whether the positive regression runs the real CLI apply lifecycle.
3. Verify the prior red/green and fail-closed evidence on planning origin/main.
4. Check exact-head CI and owner-gated runtime cell state.
5. Record the SHA-specific verdict, actionable correction, and remote evidence witnesses.
6. Publish this review evidence to genuine planning origin/main and verify the remote tree entry.

## Review identity and remote candidate

Role: CODEX-REVIEW. Card t-20261106-r27-remote-up-podman-owner-missing (0427-117). Product repo mcpdev80/baseharbor. Fresh product remote witness from a new clone in `/tmp/opencode/codex-1419-rereview-d-wt`:

```
eee11d50b7a7b55675a282f03d4a1a78e4511cf0 refs/heads/develop
f69f2a6c2823b65240604685191ccb8ec6e78cb8 refs/pull/1419/head
```

PR #1419 is OPEN, non-draft, mergeable, base `develop`, head `f69f2a6c2823b65240604685191ccb8ec6e78cb8`. Base `eee11d50b7a7b55675a282f03d4a1a78e4511cf0` is an ancestor of the head (`git merge-base --is-ancestor` returned 0).

The requested delta comparison `438895466eed1838bd50f3f9838184e4b7d7ebc1..f69f2a6c2823b65240604685191ccb8ec6e78cb8` is exactly one modified file:

```
cmd/baha/deployment_owner_loan_regression_test.go | 128 +++++++++++++++++++---
1 file changed, 113 insertions(+), 15 deletions(-)
```

The change is test-only; no production code or `.github/**` file changed.

## Verdict

**REJECT_LANE_FIX** on the remaining positive-regression requirement. The change replaces `saveThroughApplySeam` with the production function `recordDeploymentBeforeMutation`, which is a meaningful improvement: that function installs the apply context and invokes the production owner verification/write path. However, the test still does not execute the real `app apply` command lifecycle requested by r6.

In `cmd/baha/deployment_owner_loan_regression_test.go:381-390`, the test manually builds a `resolvedApplication`, calculates a consent digest, builds a context, and calls `recordDeploymentBeforeMutation` directly. It never calls `runApplicationApplyLifecycle` or `executeApplicationApplyLifecycle`. The record assertion at lines 394-405 therefore verifies the direct write-function call, rather than a deployment record produced after the actual apply runner. This retains the central limitation of a write-seam test even though it no longer uses the custom `saveThroughApplySeam` helper.

Fix recipe: drive `runApplicationApplyLifecycle` or `executeApplicationApplyLifecycle` for the repository-sourced application selected on the isolated local Podman target, using only focused test hooks needed to make the lifecycle deterministic. Then find and assert the owner-backed pending deployment record after that call returns. Preserve the base red discriminator with the literal `deployment.ErrDeploymentOwnerMissing` sentinel and candidate green result; retain the connector-bound and unmarked fail-closed cases.

## Regression evidence on planning origin/main

The requested prior act was checked on the genuine planning remote. Planning checkout identity before this evidence commit:

```
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

`git rev-parse --show-toplevel` returned `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. Planning main before this review was `d8eb289d7da4ef6bbb9cff965dd996a2aaccd984`.

Exact remote tree witness for the prior act:

```
100644 blob 13473491d6281c691f6e016b271f714d4bc214b5	evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-6.md
```

That origin/main evidence records the red-first test on the stashed base failing with the literal sentinel `deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable`, and the same test passing on candidate `f69f2a6c`. It also records connector-bound and unmarked cases remaining fail-closed on both sides with `ErrDeploymentOwnerMissing`. These are prior-run claims verified in the published evidence; this review did not rerun product tests.

The previously accepted production-code change remains untouched in this r6 delta. This rereview is restricted to whether the requested new positive regression now exercises the real apply lifecycle.

## Exact-head CI and runtime gates

GitHub run `42356028515` (run number 4991, `pull_request`, exact head `f69f2a6c2823b65240604685191ccb8ec6e78cb8`) is terminal success. `PR · Validation · cli-package-tests` job `128354232810` succeeded; `PR Selected Checks` job `128355686673` succeeded. The CLI package run covers `./cmd/baha`, including this regression file.

`Targeted HA · docker` job `128354201794` and `Targeted HA · podman` job `128354202162` were skipped. The mission identifies these skips as the owner `ci.yml` push-ref gate. They are not a rejection reason, and no workflow rerun or dispatch was performed.

## Repo-rule compliance

This was a read-only, exact-head review. No product code, tests, workflow files, PR state, or CI runs were changed. No merge was attempted. Review evidence is being published only in the verified `baseharbor-plan` repository. No subagents or containers were used.

## END CODEX-REVIEW DONE

CODEX-REVIEW 0427-117/#1419-rereview-d: verdict=REJECT_LANE_FIX head=f69f2a6c2823b65240604685191ccb8ec6e78cb8 delta=test-only-ok real_cli_apply=still-write-function-not-runApplicationApplyLifecycle regression=un-gated GREEN + base RED verbatim sentinel recorded + connector/unmarked fail-closed recorded ci=4991 TERMINAL runtime_cells=owner-gate recipe=call runApplicationApplyLifecycle/executeApplicationApplyLifecycle and assert the persisted owner record afterward
