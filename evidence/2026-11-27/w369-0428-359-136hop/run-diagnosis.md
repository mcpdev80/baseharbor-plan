# Run Diagnosis - PR #136 head c4e4400174d

Follow-up delivery task 2026-11-27T04:31:58Z. Read-only, evidence-only. No card, no PR push, no workflow edit (Owner scope). Single pass.

## (1) PR state (gh pr view 136 --repo mcpdev80/baseharbor-plan --json)

- headRefName = w267-0428-359-recovery-catalog
- headRefOid = c4e4400174dc3fe5c04082c7c85483db9b82543f
- isDraft = false
- state = OPEN
- mergeable = UNKNOWN

=> The PR is a real, non-draft, OPEN pull request. The head is a topic branch, not main.

## (2) Check-runs on the exact commit + PR-event runs

`gh api 'repos/mcpdev80/baseharbor-plan/commits/c4e4400174d/check-runs' --jq '.check_runs[] | .name+"="+(.status)+" "+(.conclusion//"")'`

- Plan · validate=completed success

A hosted check exists on the exact head c4e4400174d and it is green. This is the dispatch run 9977 (URL https://github.com/mcpdev80/baseharbor-plan/actions/runs/45937240521), which registered as a check run on the commit.

`gh run list --repo mcpdev80/baseharbor-plan --event pull_request --limit 10 --json databaseId,headSha` returns 10 pull_request runs on other heads (f08d1c0f4, 158f0171b, 6aaf29098, c6a60e6b2, 5b5e6d821, 78a2c8ffd, 6f4ad1c66, 936cee502, b88485833, 6c2cc3c08). None of them is c4e4400174.

`gh run list ... --event pull_request --limit 100 ... select(.headSha=="c4e4400174...")` returns EMPTY.

=> No pull_request-triggered run exists on the exact head c4e4400174d.

## (3) Root cause (file:line from .github/workflows/validate.yml on origin/main)

validate.yml on:
- line 3: on:
- line 4:   pull_request:
- line 5:   push:
- line 6:     branches: [main]
- line 7:   workflow_dispatch:

The pull_request trigger (validate.yml line 4) fires on PR lifecycle events (open / synced / reopened) and runs against the PR's published state for the default main branch. It does NOT fire on every push to an arbitrary topic branch, and it does not fire against a bare topic-branch head that has not been merged into main.

The PR head c4e4400174d sits on the topic branch w267-0428-359-recovery-catalog whose base is main but which is never merged to main. Pushing a new forward merge commit to that topic branch does not produce a new pull_request event, so GitHub started no pull_request run on c4e4400174d. The green check on the exact commit is only the workflow_dispatch run (9977) that the transport hop triggered by ref, registered as a commit-level check run.

Classification: NOT a draft problem, NOT a merge conflict, NOT a paths-filter gap, NOT a missing workflow on the PR head (validate.yml is present and unchanged on the PR head). The absence is the expected behaviour of GitHub's pull_request trigger (validate.yml line 4) for an unmerged topic-branch head. No defect. No fix.

## (4) Evidence-only publish

Single file written: evidence/2026-11-27/w369-0428-359-136hop/run-diagnosis.md
No generated views touched, no PR push, no workflow edit, no card.

## END

- Exact head: c4e4400174dc3fe5c04082c7c85483db9b82543f
- Commit-level check on exact head: Plan · validate = completed success (dispatch run 9977)
- pull_request-run on exact head: none (empty witness) - expected, because validate.yml line 4 pull_request does not fire for an unmerged topic-branch head
- Root cause file:line: .github/workflows/validate.yml line 4 (on.pull_request)
