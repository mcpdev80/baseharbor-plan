# PR #1753 exact-head review preparation

## PLAN

1. Verify product and Planning remotes, then refresh live PR #1753 head and current develop refs from the real GitHub remote.
2. Proceed with candidate review only if the live PR head is an ancestor of current develop and `git rev-list --count <head>..develop` is zero; otherwise keep the prior candidate on hold.
3. For a current head, inspect the exact diff for canonical `app footprint show -o json` admission and fail-closed behavior, then verify positive and negative test lines.
4. Verify the exact hosted run and executed data-capabilities job for that full head SHA; issue a verdict only with terminal evidence.
5. Write the exact-head evidence at the requested `review-1753-head<sha>.md` path, publish it to Planning origin/main, update the board, and post END; do not merge or close.

## Status

Awaiting live-ref check. No verdict issued.

## Live hold state

Verified product remote: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push). Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1753/head refs/heads/develop` returned:

```text
6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop
03ef125e610f3a3db60042b70784d8e463f11500 refs/pull/1753/head
```

`gh pr view 1753 --repo mcpdev80/baseharbor --json number,state,isDraft,baseRefName,headRefName,headRefOid,mergeStateStatus` reported open, non-draft, base `develop`, head `03ef125e610f3a3db60042b70784d8e463f11500`, and `mergeStateStatus=BEHIND`. This is not the post-hop exact candidate. No code or test inspection, verdict, CI action, merge, or close was performed. Resume only when a fresh live head is current with develop (back=0), then inspect the canonical admission, fail-closed behavior, positive/negative regression, and terminal data-capabilities job for that exact SHA.

## Planning remote witness

Verified before committing evidence:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## cleanliness

Shell PID `1317826`: `docker ps -a` before and after showed the same eight pre-existing exited containers (IDs `268b7d8b4612`, `34cf9576dc2b`, `e88b00795b5c`, `1451a7b5b3c6`, `d7ba821c0e08`, `957a80e73b57`, `45bddf32278e`, `9d3f1a2b1e0e`). No container or compose project was started or changed.

END_BLOCKED codex-rev-1747: #1753 remains behind develop; exact current candidate required before review. Current stale head 03ef125e610f3a3db60042b70784d8e463f11500; no verdict.
