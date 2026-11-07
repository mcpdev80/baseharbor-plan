# CODEX-MERGE 0427-051 / PR #1418

## PLAN

1. Read the merge mission and repository authority, then verify the exact PR head/base and accepted review evidence.
2. Check required CI and branch protection gates on the exact candidate without rerunning workflows.
3. Confirm merge eligibility and perform only the mission-authorized merge action.
4. Verify the remote merge result, record evidence in baseharbor-plan, and post END.

## Planning repository verification

The planning checkout is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. Exact remote output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The remote is the real GitHub planning repository, not the quarantined `workers/baseharbor-plan` phantom zone. Evidence belongs only in this planning repository.

## Candidate and gate preflight

Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1418/head` before merge:

```text
66310729e1789a59e3025fcbfb270015f83b8d08	refs/heads/develop
a91debbb047d6ea7a0f258194c0a3474978687bd	refs/pull/1418/head
```

The PR head matched the accepted review SHA exactly. PR #1418 was open, non-draft, targeting `develop`, and GitHub reported it mergeable. The branch had diverged from current develop (8 commits behind); per the merge mission, I did not rebase or refresh the accepted candidate.

Accepted independent review record: [act-1418b-review.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-material/act-1418b-review.md), committed on planning main as `07a8eb4b584490142c5a4c8ec5871490deb3cae5`. It reviewed exact head `a91debbb047d6ea7a0f258194c0a3474978687bd` against base `934be499b9d2d894f80889fc23cd811884c8aec4`, mapped F1/F2/F3, and issued ACCEPT.

Run 4984 (`42338068531`) was terminal success for the exact candidate. `PR Selected Checks` succeeded and its GitHub Actions app integration ID was 15368. The Go unit, build, vet, source-format, trusted-plan, focused Python, workflow-policy and selected-check aggregator jobs succeeded. Docker/Podman targeted HA and Release Source Preflight were skipped by their owner-gated push-ref conditions; the accepted review determined these skips did not invalidate the PR unit evidence. No workflow rerun was triggered.

Current live ruleset API results showed both `develop - integration branch` and `develop - required checks` with `enforcement=disabled`; no protections were changed and no bypass option was used. The merge follows the explicit mission's merge-commit instruction.

## Merge and remote witnesses

Executed with expected-head guard:

```text
gh pr merge 1418 --repo mcpdev80/baseharbor --merge --match-head-commit a91debbb047d6ea7a0f258194c0a3474978687bd
```

GitHub PR state after the command:

```text
state=MERGED
headRefOid=a91debbb047d6ea7a0f258194c0a3474978687bd
mergeCommit=eee11d50b7a7b55675a282f03d4a1a78e4511cf0
mergedAt=2026-11-07T04:57:39Z
mergedBy=mcpdev80
```

Fresh `git ls-remote` after merge:

```text
eee11d50b7a7b55675a282f03d4a1a78e4511cf0	refs/heads/develop
a91debbb047d6ea7a0f258194c0a3474978687bd	refs/pull/1418/head
```

GitHub compare of accepted head against current `develop` returned `status=ahead`, `ahead_by=9`, `behind_by=0`, merge base equal to the accepted head. A fresh clone in `/tmp/opencode/codex-1418-merge-c-wt` independently verified ancestry:

```text
git -C /tmp/opencode/codex-1418-merge-c-wt merge-base --is-ancestor a91debbb047d6ea7a0f258194c0a3474978687bd refs/remotes/origin/develop
ancestry_rc=0
```

No tag, release, or deployment was created.

## Planning closeout

The task card `t-20261018-r27-remote-material` is being closed as accepted after the confirmed merge. The acceptance evidence URL is this file on planning `origin/main`. Planning render/check and remote publication witnesses will be recorded after the status update.

## repo-rule compliance

No product files or workflows were modified. No CI reruns, force pushes, Docker/Podman projects, or release actions were performed. The accepted candidate was merged unchanged with the specified merge-commit method and an expected-head guard.

END_DONE codex-1418-merge-c: PR #1418 merged as eee11d50b7a7b55675a282f03d4a1a78e4511cf0; accepted head a91debbb047d6ea7a0f258194c0a3474978687bd is an ancestor of develop (rc 0).

Exact planning `origin/main` witness after `git pull --rebase origin main` and before publishing this evidence:

```text
4da251f857fb2c0549f9ed8be9e1fe69f2e1459e\trefs/heads/main
```
