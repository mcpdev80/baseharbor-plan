# PR ancestry rule clarification

## PLAN

1. Read the ruleproof mission and identify its exact evidence path, target, and acceptance criteria.
2. Verify PR #1627 historical branch heads and distinguish them from unrelated ancestry.
3. Apply the same ancestry check to PRs #1723, #1725, and #1645 against current develop `acc34323968`.
4. Write the ancestry clarification with one rule and three evidence-backed examples.
5. Publish to Planning main, record the tree witness, update the board, and post coordinator handoff.

Role: CODEX-REVIEW of the ancestry rule only. No product verdict, merge, close, comment, test, or subagent action.

regel: Classify an ancestor against the exact base and the PR's own historically observed head sequence: an own prior head is not foreign; an unrelated PR head absent from that sequence and absent from the exact base is foreign; after the commit is merged into develop and the reviewed PR is based on that develop head, it is inherited base content rather than foreign for that current comparison.

## Three walkthroughs

### Own ancestor: PR #1627

PR #1627's exact candidate was `fe4027f7986502a825b2c701fb53725f39434435`, merged as `acc343239681feb235a33cf00c8ea754c537291f` with parents `52a3c5446f41a1dd8678d99875e4cb1eee67874c` and the candidate. Its GitHub PR commit list includes `0768274c6f692bc0779202a1b9dc1fb222fce2ef`; first-parent history contains merge `bfd01276`, whose parents are base `52a3...` and `0768274...`. Owner clarification identifies `0768274` as PR #1627's own earlier candidate head. Its ancestry in #1627 is therefore own history, not contamination, even though the same commit was also present on sibling candidates at that time.

### Foreign ancestor: PR #1725 before the develop merge

PR #1725 was opened with initial candidate `9bf4a72f` on 2026-11-20. Its task `t-20261120-shared-backend-state-version-message` has `depends_on: []`. The old PR #1723 head `12a62523fc5f2259220aece4cc5619dcb8f4ae4d` is not in develop `acc343...`, but it is an ancestor of #1725 head `d65e9a25419798950a01676ab259967345721a25`: #1725's first-parent chain is `d65e9a -> 4851035 -> 12a6252`, and `4851035` has `12a6252` as its first parent. The old #1723 head is not #1725's original candidate head; it was imported after the independent PR was opened. This is foreign sibling ancestry for #1725 under the rule. The current #1725 diff confirms the effect: against current develop `acc343...`, it still contains the four workload-port paths from #1723 plus its three shared-state-version paths. The current full #1723 head `9355afe129b9fa7e11837b9fcbe5b7fc40c3d2e9` is not an ancestor of current #1725 head; the foreign ancestry is the older #1723 head `12a6252`, not the newer PR head.

### Previously foreign, later in develop: PRs #1723 and #1725

The merge commit that brought #1627 into develop is `acc343239681feb235a33cf00c8ea754c537291f`, with parents `52a3...` and `fe4027...`. Thus `0768274...` and the old #1627 candidate are now ancestors of current develop. Current #1723 (`9355afe...`) and #1725 (`d65e9a...`) both have current develop `acc343...` as an ancestor and both inherit `0768274...` through that base. The old #1627 commit is therefore not foreign relative to their current develop-based comparisons. Their current diffs are four files for #1723 and seven files for #1725. This does not erase the earlier contamination finding for their pre-merge heads, nor does it clear #1725's separate imported #1723 workload-port content described above.

## PR #1645 check

PR #1645 is open at head `326ca9005267c135feb31cdfde8ac69a3c17508e`, with base `52a3c5446f41a1dd8678d99875e4cb1eee67874c`. The cited #1627 commit `0768274...`, #1627 head `fe4027...`, #1723 historical head `12a6252...`, #1725 head `4851035...`, and current #1723/#1725 heads are all non-ancestors of #1645. #1645 is also not an ancestor of #1723 or #1725. It does not carry the cited sibling ancestry; it remains on its older base and its own Tempo change-set is 35 files. This is ancestry classification only, not a product verdict for #1645.

## Current remote witnesses

- Product remote `git remote -v`: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1627/head refs/pull/1723/head refs/pull/1725/head refs/pull/1645/head` returned:

```text
acc343239681feb235a33cf00c8ea754c537291f	refs/heads/develop
fe4027f7986502a825b2c701fb53725f39434435	refs/pull/1627/head
9355afe129b9fa7e11837b9fcbe5b7fc40c3d2e9	refs/pull/1723/head
d65e9a25419798950a01676ab259967345721a25	refs/pull/1725/head
326ca9005267c135feb31cdfde8ac69a3c17508e	refs/pull/1645/head
```

- Current PR states: #1627 merged; #1723 open; #1725 open; #1645 open.
- Planning remote `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` output:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

- Current develop ancestry: `0768274...` and `fe4027...` are ancestors of `acc343...`; `12a6252...` is not.
- PR #1645 ancestry checks: the six named sibling commits/heads above are not ancestors of its head; its head is not an ancestor of #1723 or #1725.
- Current diff sizes against `acc343...`: #1723 four files; #1725 seven files. Historical pre-merge diffs against `52a3...`: #1723 sixteen files; #1725 nineteen files.

## Cleanliness

- `docker ps -a` before review recording, shell PID 3185223: header only; no containers listed.
- `docker ps -a` after review recording, shell PID 3187140: output was the header only, no containers listed. No containers or compose projects were started or changed.

END_DONE codex-rev2-1736: ancestry rule clarified with own-history #1627/076, foreign #1723-old-head 12a imported into independent #1725, and 076 later inherited from develop acc343; #1645 does not carry those refs. Planning publication pending.
