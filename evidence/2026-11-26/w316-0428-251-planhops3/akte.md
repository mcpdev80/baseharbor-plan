# w316-0428-251-planhops3 — Transport-only forward hops

- date: 2026-11-26 (date -u, never future-dated)
- mission: transport-only forward hops in baseharbor-plan onto CURRENT main so Codex can merge without staleness HOLDs. No content edits, no merges, no direct pushes to main.
- PRs in scope: 111, 112, 114, 73, 84, 99, 106, 107, 109

## Visible Ansatz Block (ansatz required before first commit)

- per-card frontmatter owner VERBATIM: owner w316-0428-251-planhops3 (fetched from origin/main at runtime)
- git user.name: w316-0428-251-planhops3
- git user.email: w316-0428-251-planhops3@baseharbor.local
- literal git commit invocation: git -c user.name=w316-0428-251-planhops3 -c user.email=w316-0428-251-planhops3@baseharbor.local commit
- git merge invocation: git -c user.name=w316-0428-251-planhops3 -c user.email=w316-0428-251-planhops3@baseharbor.local merge
- pre-push git show -s --format=%an gate line: git log --format='%h an=%an cn=%cn' -1

## Repo attestation

- real planning repo: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
- remote origin: https://github.com/mcpdev80/baseharbor-plan.git (only github.com/mcpdev80 url used)
- origin/main SHA at start of shift: 59ab8ee2552a88e3acb663525035636f63da0f1e
- origin/main SHA at end of shift: 59ab8ee2552a88e3acb663525035636f63da0f1e (unchanged during shift)

## Scope

- IN SCOPE: transport-only absorb of origin/main into each named candidate branch, one PR at a time.
- OUT OF SCOPE: product repos, tasks/, cards/, .github/**, status changes, new cards, CI reruns, local test execution.
- Forbidden: git push origin HEAD:main, rebase, force-push, cherry-pick, re-cut, new branch.

## Procedure

- Fresh /var/tmp clone: /var/tmp/planhops3 (never the shared detached plan checkout, never another lane's worktree).
- Per PR: checkout the PR's existing branch head, git fetch origin main, ONE ordinary `merge --no-edit origin/main` with the lane commit identity, verify `git merge-base --is-ancestor origin/main HEAD`, normal push to that same branch.

## Per-PR results (delivered to origin, all behind=0, main an ancestor)

- PR 111 | branch w255-0428-251-284-close | old fd45441d7 | new fd45441d7 | behind=0 | main already an ancestor (absorbed at commit 2ac2ba40); no hop needed. Live head unchanged.
- PR 112 | branch w309-0428-352-14gatecatalog-board | old c839b42ca | new f05cd6e34 | behind=0 | hop commit f05cd6e3, pushed, delivered.
- PR 114 | branch w312-0428-251-planhops-akte | old c0cc0c782 | new e8e2ae812 | behind=0 | hop commit e8e2ae81, pushed, delivered.
- PR 73 | branch lane-w265-plan | old 1bf719253 | new 3dae6dbd6 | behind=0 | hop commit 3dae6dbd6, pushed, delivered.
- PR 84 | branch ourist-shift-w284 | old e22dd05c5 | new abb5bb10f | behind=0 | hop commit abb5bb10, pushed, delivered.
- PR 99 | branch lane/w296-0428-251-demoflowdiff | old a2401812b | new d06d6c53d | behind=0 | hop commit d06d6c53, pushed, delivered.
- PR 106 | branch w302-0428-251-boardnotes | old 3ab55185c | new 056725479 | behind=0 | hop commit 05672547, pushed, delivered.
- PR 107 | branch w301-evidence-0428-251 | old 958270f37 | new f31f7beca | behind=0 | hop commit f31f7bec, pushed, delivered.
- PR 109 | branch w304-0428-249-pr1812hop2-plan | old 819288820 | new 37158657d | behind=0 | hop commit 37158657, pushed, delivered.

## Validate-run note (for Codex)

- Transport hops do NOT open/refresh PRs and do NOT trigger CI. No head carries a validate run — this is by design (mission forbids reruns/workflow triggers). Confirmed via gh api actions/runs: zero runs on every hop head, including #73 head 3dae6dbd6. Heads are current (behind=0) for merge; run-absence is a hop property, not a defect.
- #73 specifically: head 3dae6dbd6 is behind=0 but has NO validate run. State recorded so Codex does not judge a head whose own run is absent.

## Comment posted

- Consolidated heads+runs table posted as PR comment on #113 (the deviation akte PR): https://github.com/mcpdev80/baseharbor-plan/pull/113#issuecomment-7190241461

## Cleanliness

- all work in /var/tmp/planhops3 clone; no shared detached plan checkout, no other lane's worktree used.
