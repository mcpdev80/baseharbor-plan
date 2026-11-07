# CODEX-MERGE 0427-036 / PR #1405

## PLAN

1. Verify the accepted PR head and develop ref, live PR status, and real planning repository.
2. Check live merge protections and exact-head checks/review required for this authorized merge.
3. Attempt the specified merge-commit with exact-head protection; stop if blocked.
4. Verify the merged SHA and accepted-head ancestry on develop; record the result.
5. Publish merge evidence on baseharbor-plan origin/main, verify it, and post END.


## Pre-merge authorization and gates

- This turn follows the explicit Owner CODEX-MERGE mission for PR #1405. GitHub account verified as `mcpdev80`.
- Planning repository identity: `git -C baseharbor-plan rev-parse --show-toplevel` returned `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; origin remotes are `https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.
- Fresh product witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1405/head`:

```text
934be499b9d2d894f80889fc23cd811884c8aec4	refs/heads/develop
6014a8fcd2697f34ab0c52353d328dd55cc9a1a5	refs/pull/1405/head
```

- Live PR is OPEN, non-draft, base `develop`, mergeable, and still at the accepted head. The independent CODEX-REVIEW `ACCEPT` is published in `evidence/r27-welle5-folge-2026-11-06/management-host/act-1405d-review.md` on planning `origin/main` commit `18e991930c87122279a8c06c08d31281d8187457`. Current card `t-20261018-r27-management-host` remains in review; all six declared predecessors are accepted.
- Exact candidate run `42338548731` is terminal success. `PR Selected Checks` succeeded with GitHub Actions integration `15368`; source format, focused Python, authority-package-tests, cli-gofmt, go-unit-tests, go-build, and go-vet succeeded. Targeted Docker, Podman, and selected-runtime cells were skipped by the designated-ref owner gate, as explicitly considered in the accepted review. No workflow rerun or dispatch was done.
- Effective merge controls rechecked live: rulesets `23754541` (develop integration) and `25223541` (develop required checks) report `disabled`; `GET /branches/develop/protection` reports 404 `Branch not protected`; repository settings allow merge commits. The standard `--merge` strategy is enabled. No admin/bypass option will be used. The installed `gh` supports `--match-head-commit`, which will guard the exact accepted PR head.
- No unresolved GitHub review is required by active branch protections; the independent SHA-specific review artifact above is present. No changed code followed that review.



## Merge result

- Executed without `--admin`, bypass, force, squash, or rebase:
  `gh pr merge 1405 --repo mcpdev80/baseharbor --merge --match-head-commit 6014a8fcd2697f34ab0c52353d328dd55cc9a1a5`.
- GitHub then reported PR #1405 `MERGED`, base `develop`, accepted head `6014a8fcd2697f34ab0c52353d328dd55cc9a1a5`, merge commit `66310729e1789a59e3025fcbfb270015f83b8d08`, merged at `2026-11-07T04:53:03Z`.
- Fresh post-merge `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1405/head`:

```text
66310729e1789a59e3025fcbfb270015f83b8d08	refs/heads/develop
6014a8fcd2697f34ab0c52353d328dd55cc9a1a5	refs/pull/1405/head
```

- A fresh clone under `/tmp/opencode/codex-1405-merge-e-wt` fetched `develop` at `66310729e1789a59e3025fcbfb270015f83b8d08`. `git merge-base --is-ancestor 6014a8fcd2697f34ab0c52353d328dd55cc9a1a5 origin/develop` returned rc=0; the merge commit itself is also an ancestor (rc=0).
- No release, tag, promotion, workflow edit, rerun, or dispatch was made.

## Planning repository pre-push witness

Before this evidence is committed, `git -C baseharbor-plan rev-parse --show-toplevel` returned:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

`git -C baseharbor-plan remote -v` returned:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Exact pre-push `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` output:

```text
cc6373c06bdcc0ebe336b23a0c7b8b2f38fc3464	refs/heads/main
```

## END

END_DONE codex-1405-merge-e: result=MERGED merged_head=66310729e1789a59e3025fcbfb270015f83b8d08 develop_at_merge=66310729e1789a59e3025fcbfb270015f83b8d08; latest_develop=eee11d50b7a7b55675a282f03d4a1a78e4511cf0; accepted_head_and_merge_commit_are_ancestors_rc0; akte=this file


## Planning closeout and final publication

Coordinator commit `b1f7cd2d94bb9b2aeb2c3a2ba5eaecf11d13990f` independently published the management-host card as `closed` with `resolution: accepted` and the merged PR evidence. `python3 scripts/plan.py show t-20261018-r27-management-host` reports state accepted and all predecessors accepted. This lane did not rewrite that card. The merge-evidence push preserved the closeout; Git reported `b1f7cd2d..98bfb025` advancing `origin/main` to this evidence commit.

Final planning-main witness before this evidence addendum:

```text
98bfb025b37720366b36cfe9aad782dc07f61c7c	refs/heads/main
```


## Final remote freshness check

After the merge, `develop` advanced again to `eee11d50b7a7b55675a282f03d4a1a78e4511cf0` (a separate merge, recorded by planning receipt `evidence/receipts/commits/eee11d50b7a7b55675a282f03d4a1a78e4511cf0.json`). A fresh fetch in the lane's own clone confirmed both the accepted PR head `6014a8fcd2697f34ab0c52353d328dd55cc9a1a5` and merge commit `66310729e1789a59e3025fcbfb270015f83b8d08` remain ancestors of current `origin/develop`, both `git merge-base --is-ancestor` rc=0.

Latest product witness:

```text
eee11d50b7a7b55675a282f03d4a1a78e4511cf0	refs/heads/develop
```

Latest planning `origin/main` witness before this addendum:

```text
3451f12640329fa3dc56a6df865bc07053690287	refs/heads/main
```
