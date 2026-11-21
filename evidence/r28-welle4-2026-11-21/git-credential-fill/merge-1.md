ROLLE: MERGE

# PR #1742 merge evidence

Karte: `t-20261121-git-credential-fill-bootstrap-hang` (0428-217)
Zeit: 2026-11-21 13:10 UTC
Backend/Modell: Codex via OpenAI AgentGateway; exact model ID is not exposed in this session.

## PLAN

1. Read the merge mission and verify exact scope, required gates, and stop conditions.
2. Resolve product and planning GitHub remotes and measure live develop and PR refs.
3. Verify exact-head CI, review evidence, planning ownership, dependencies, and effective merge rules.
4. Merge only PR #1742 at the approved head, using a head-SHA guard and merge commit.
5. Verify the merged PR, merge commit, and develop ancestry; record all witnesses.
6. Publish only this merge evidence and verify it on planning origin/main.

## Pre-merge checks

### 1a. PR state and head

Command:

```text
gh pr view 1742 --repo mcpdev80/baseharbor --json state,isDraft,mergeable,headRefOid,baseRefName
```

Output immediately before merge:

```json
{"baseRefName":"develop","headRefOid":"6f8fa120f7e5e79d260ed89d486633bc152105de","isDraft":false,"mergeable":"MERGEABLE","state":"OPEN"}
```

### 1b. Develop ancestry and freshness

Command:

```text
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
```

Output:

```text
97b2ba5543f07b820b5c18a688058fd932c4516f refs/heads/develop
```

For the ancestry check I used GitHub's live compare API against those exact remote SHAs rather than the quarantined stale-ref checkout:

```text
gh api repos/mcpdev80/baseharbor/compare/97b2ba5543f07b820b5c18a688058fd932c4516f...6f8fa120f7e5e79d260ed89d486633bc152105de
```

Output fields:

```json
{"ahead_by":3,"behind_by":0,"merge_base_commit":"97b2ba5543f07b820b5c18a688058fd932c4516f","status":"ahead"}
```

This remote witness proves develop is an ancestor of the candidate and `develop..head` has no commits (`behind_by=0` in the compare direction). I did not cite refs or logs from `workers/baseharbor`, which is quarantined.

### 1c. Required CI

Command:

```text
gh pr checks 1742 --repo mcpdev80/baseharbor
```

Required output lines:

```text
PR Selected Checks pass https://github.com/mcpdev80/baseharbor/actions/runs/44905476380/job/136851092065
PR · Go unit · cli-0 pass https://github.com/mcpdev80/baseharbor/actions/runs/44905476380/job/136850045521
PR · Go unit · cli-1 pass https://github.com/mcpdev80/baseharbor/actions/runs/44905476380/job/136850045574
PR · Go unit · cli-2 pass https://github.com/mcpdev80/baseharbor/actions/runs/44905476380/job/136850045487
PR · Go unit · cli-3 pass https://github.com/mcpdev80/baseharbor/actions/runs/44905476380/job/136850045507
PR · Trusted Plan pass https://github.com/mcpdev80/baseharbor/actions/runs/44905476380/job/136850001543
Workflow policy pass https://github.com/mcpdev80/baseharbor/actions/runs/44905476380/job/136850001359
```

`PR Selected Checks` check-run has `head_sha=6f8fa120f7e5e79d260ed89d486633bc152105de`, `conclusion=success`, and `app_id=15368`. The active `develop - required checks` ruleset requires this context from integration 15368. The CLI shards are terminal pass. Unselected runtime/release checks are skipped and were not counted as passes.

### 1d. Review verdict and prerequisite evidence

The published review file contains the exact verdict SHA and pre-merge condition:

```text
**Verdict: APPROVE CONTENT** for exact candidate `6f8fa120f7e5e79d260ed89d486633bc152105de`.
**Pre-merge condition: publish `round-4-clone-env.md` before merge.** It is already published at the fetched `origin/main` revision recorded below.
```

Fetched `origin/main` contained both required files before merge:

```text
evidence/r28-welle4-2026-11-21/git-credential-fill/round-4-clone-env.md
evidence/r28-welle4-2026-11-21/git-credential-fill/review-4.md
```

The round-4 file records the child-environment regression and both requested red mutations. The task card was `state: review`, owner `0428-217-cloneenv`, with no dependencies. GitHub reports no unresolved review threads. The exact-head independent Codex review is `review-4.md`; GitHub's `reviewDecision` is empty, and no active ruleset requires a formal review.

### Live merge rules and permissions

Product remote resolution:

```text
git -C /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor remote -v
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)
```

Live rulesets before merge:

```text
23754541 develop - integration branch enforcement=disabled
25223521 develop - required checks enforcement=active; required context PR Selected Checks; integration_id=15368
```

The repository reports merge commits allowed. No bypass, admin option, force-push, or protection change was used. The direct mission authorizes this one PR merge; no general production activation or release action is inferred.

## Merge action

Command, guarded against any change to the approved candidate head:

```text
gh pr merge 1742 --repo mcpdev80/baseharbor --merge --match-head-commit 6f8fa120f7e5e79d260ed89d486633bc152105de
```

The command returned without an error. No other PR was merged.

## Post-merge proof

Command:

```text
gh pr view 1742 --repo mcpdev80/baseharbor --json state,mergedAt,mergeCommit,headRefOid,baseRefName
```

Output:

```json
{"baseRefName":"develop","headRefOid":"6f8fa120f7e5e79d260ed89d486633bc152105de","mergeCommit":{"oid":"ddfa80f7202a0aca3cf68c4542158132c0c2795b"},"mergedAt":"2026-11-21T13:09:38Z","state":"MERGED"}
```

Command:

```text
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
```

Output:

```text
ddfa80f7202a0aca3cf68c4542158132c0c2795b refs/heads/develop
```

The post-merge GitHub compare used base `6f8fa120f7e5e79d260ed89d486633bc152105de` and head `ddfa80f7202a0aca3cf68c4542158132c0c2795b`. It returned `status=ahead`, `ahead_by=1`, `behind_by=0`, `merge_base_commit=6f8fa120f7e5e79d260ed89d486633bc152105de`. Thus the approved PR head is an ancestor of the new develop head, which is the merge commit itself.

## Repo-rule compliance

This session performed only the authorized merge of PR #1742. The exact-head review and required check were verified before the merge. The merge used the requested merge-commit strategy and an expected-head guard. No PR comment, close, card edit, workflow rerun, workflow dispatch, bypass, force-push, or subagent was used. No test was run during this merge session.

## cleanliness

Before merge, `docker ps -a` at 2026-11-21 13:01 UTC (shell PID 2850483) returned only the header and zero containers; this session started no containers between that observation and merge. After merge, `docker ps -a` at 2026-11-21 13:10 UTC (shell PID 2954156) also returned only the header and zero containers. No compose project was started.

## Evidence publication witness

After `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main`, the exact path lookup returned:

```text
evidence/r28-welle4-2026-11-21/git-credential-fill/merge-1.md
```

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main` returned:

```text
2d0246a6c63ef10451d12b57fc34987ee2a49f62 refs/heads/main
```

END MERGE DONE — PR #1742 merged as `ddfa80f7202a0aca3cf68c4542158132c0c2795b`; develop now points to that commit.
