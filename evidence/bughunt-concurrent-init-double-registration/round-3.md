# 0427-175 round 3 — repair path must be executable, recovery regression on the real destroy path, tighter race asserts

Mission: `/tmp/opencode/mission-175-r3.md`. Lane: worker-flash (session zone `workers/.models/flash`).
Remote-truth witnesses (first three actions of this lane, own reads):

    git ls-remote origin refs/pull/1512/head  -> a6afd633ce38a4cedfb74bc71d6703d3df56312b  refs/pull/1512/head
    gh pr view 1512 --json headRefName,headRefOid -> 0427-175-initlock a6afd633ce38a4cedfb74bc71d6703d3df56312b
    gh api "repos/mcpdev80/baseharbor/actions/runs?head_sha=a6afd633c...": <run id recorded when it appears>

Base: branch `0427-175-initlock`. The mission named head `135c8be1a`, but while this lane read the
review, the branch advanced to `a6afd633c` (three commits: `54d9b9ef1` docs EN/DE repair section,
`9de8c993b` its merge with my `135c8be1a`, `a6afd633c` DE wording cleanup). `135c8be1a` IS an ancestor
of `a6afd633c` (`git merge-base --is-ancestor`, rc=0), so this lane continues on the same chain — no
second candidate, no rebase-over. Everything below was written against `a6afd633c` content.
PR: https://github.com/mcpdev80/baseharbor/pull/1512. No `.github/**` changes. No subagents (AGENTS §4.8).

Planning-repo witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel`
→ `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (canonical planning repo, not `workers/baseharbor-plan`).

## PLAN

- Read act-1512-review-r2.md verdict lines; fetch remote truth (PR head/branch, runs on head)
- Reproduce finding (1): repair text advertises `app destroy --uuid <id> --full-reset`; show the actual CLI face on the BUILT binary (lesson 162)
- Reproduce finding (2): recovery test asserts status (not destroy) and accepts a conflict error as success
- Reproduce finding (3): race test discards childErr
- Decide the fix direction for (1) with a justified delta: implement destroy UUID selection through resolve→authorize→preflight→mutate (keeping the exact identity), rather than downgrading the advice
- Implement (1); implement (2) as a real-path production regression incl. counterfactual and fail-closed omission/invalid-uuid cases; implement (3) child-outcome asserts + interrupted-registration regression
- Verify: build, vet, gofmt, readability + documentation audits, deployment/cmd cells, -race, built-binary repair face
- Commit, push to 0427-175-initlock (ancestry + own-commit witnesses), watch exact-head hosted run to terminal
- Publish this evidence to plan origin/main, verify remote witness, END line + inbox post

## Reproductions (facts, before any change)

- To be filled from the built binary and the code lines.

## Fix decision and delta

- To be filled.

## Runs and results

- To be filled.

## repo-rule compliance

- To be filled.

## State at END

- To be filled.

END_PENDING
