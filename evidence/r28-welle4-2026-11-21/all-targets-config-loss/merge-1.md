# PR #1739 merge record

ROLLE: MERGE

Timestamp: 2026-11-21 11:28 UTC
Backend/model: Codex API, GPT-6

## PLAN

1. Create the numbered merge plan in the live board and merge-1 evidence.
2. Measure fresh `develop` and PR head refs and confirm the approved candidate remains unchanged.
3. Verify PR state, mergeability, and every specifically required check.
4. If all pre-merge gates pass, merge PR #1739 without squash and verify merge commit and `develop` ancestry.
5. Publish only merge-1.md to planning origin/main and verify publication.
6. Post the completed or blocked merge status with candidate and merge SHA evidence.

## Pre-merge measurements

1. Exact command: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1739/head`

   Exact output:

   ```text
   77c1e60f51b91003ac3ddc391008c15e4a713a5c refs/heads/develop
   bb98e22599ab1f77edc056de73c682fdfdedd88a refs/pull/1739/head
   ```

   Both refs match the approved review-3 base and candidate.

2. The requested `gh pr view ... --json state,isDraft,mergeable,mergeableState,headRefOid,baseRefOid` fields `mergeableState` and `baseRefOid` are unsupported by the installed `gh` CLI. Its supported `mergeStateStatus` maps the mergeability state; the base object ID was read from the PR API. Successful command/output:

   ```text
   $ gh pr view 1739 --repo mcpdev80/baseharbor --json state,isDraft,mergeable,mergeStateStatus,headRefOid,baseRefName
   {"baseRefName":"develop","headRefOid":"bb98e22599ab1f77edc056de73c682fdfdedd88a","isDraft":false,"mergeStateStatus":"CLEAN","mergeable":"MERGEABLE","state":"OPEN"}
   $ gh api repos/mcpdev80/baseharbor/pulls/1739 --jq '{baseRefOid:.base.sha,baseRefName:.base.ref,headRefOid:.head.sha}'
   {"baseRefName":"develop","baseRefOid":"77c1e60f51b91003ac3ddc391008c15e4a713a5c","headRefOid":"bb98e22599ab1f77edc056de73c682fdfdedd88a"}
   ```

3. `gh pr checks 1739 --repo mcpdev80/baseharbor` returned these required checks, all `pass`:

   ```text
   PR Selected Checks	pass	12s	https://github.com/mcpdev80/baseharbor/actions/runs/44897396931/job/136826999989
   PR · Go unit · cli-0	pass	2m41s	https://github.com/mcpdev80/baseharbor/actions/runs/44897396931/job/136825924476
   PR · Go unit · cli-1	pass	2m37s	https://github.com/mcpdev80/baseharbor/actions/runs/44897396931/job/136825924472
   PR · Go unit · cli-2	pass	4m23s	https://github.com/mcpdev80/baseharbor/actions/runs/44897396931/job/136825924468
   PR · Go unit · cli-3	pass	3m14s	https://github.com/mcpdev80/baseharbor/actions/runs/44897396931/job/136825924490
   PR · Trusted Plan	pass	10s	https://github.com/mcpdev80/baseharbor/actions/runs/44897396931/job/136825874392
   Workflow policy	pass	22s	https://github.com/mcpdev80/baseharbor/actions/runs/44897396931/job/136825874022
   ```

   The same output also reported `PR · Native gate plan`, packages, owner, source format, focused Python, go-build, go-vet, and cli-gofmt as `pass`. Other non-selected jobs reported `skipping`; none of the required checks above were skipped or queued.

The independent review is recorded in `evidence/r28-welle4-2026-11-21/all-targets-config-loss/review-3.md`, published at planning commit `588e5f4c79cfe6e44911948ce5f79777c0df09c7`, and approves this exact candidate. The task's positive installed-then-destroyed regression and negative anonymous authorization regression are covered by the passing `./cmd/baha/` Go unit shards above.

Rules were inspected before merge. Effective branch rules report the required `PR Selected Checks` context from GitHub Actions integration `15368`; it passed above. The separate integration-branch ruleset `23754541` currently reports enforcement `disabled`; classic branch protection returns 404. No bypass will be used. Repository settings permit merge commits (`allow_merge_commit=true`), so the requested non-squash merge method is available.

## Merge action

Command executed, with expected-head guard and without `--admin` or squash:

```text
gh pr merge 1739 --repo mcpdev80/baseharbor --merge --match-head-commit bb98e22599ab1f77edc056de73c682fdfdedd88a --subject 'Merge PR #1739: tolerate missing config after operator authorization'
```

The command returned exit status 0. Post-merge command and exact output:

```text
$ gh pr view 1739 --repo mcpdev80/baseharbor --json state,mergedAt,mergeCommit,headRefOid,baseRefName
{"baseRefName":"develop","headRefOid":"bb98e22599ab1f77edc056de73c682fdfdedd88a","mergeCommit":{"oid":"97b2ba5543f07b820b5c18a688058fd932c4516f"},"mergedAt":"2026-11-21T11:29:00Z","state":"MERGED"}
```

## Post-merge measurements

5. Exact command and output:

   ```text
   $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1739/head
   97b2ba5543f07b820b5c18a688058fd932c4516f refs/heads/develop
   bb98e22599ab1f77edc056de73c682fdfdedd88a refs/pull/1739/head
   ```

   The new `develop` head equals merge commit `97b2ba5543f07b820b5c18a688058fd932c4516f`. GitHub commit API confirms that merge commit's parents are `77c1e60f51b91003ac3ddc391008c15e4a713a5c` and `bb98e22599ab1f77edc056de73c682fdfdedd88a`; therefore the reviewed candidate is a direct parent and an ancestor of current `develop`. This remote parent witness avoids consulting the quarantined local `workers/baseharbor` refs.

Planning repo remote, reverified before evidence commit:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

No squash or protection bypass was used. No other PR was merged and no Planning card was closed.

END MERGE DONE
