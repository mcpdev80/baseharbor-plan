# Board owner reconcile evidence

## PLAN

1. Read mission and record numbered plan in board and evidence before Git.
2. Inspect Plan repo instructions and current main; create isolated branch from current main.
3. Verify target card owner/body and live session status; change only authorized owner/status/body text.
4. Run card-status.py --no-push if required, then render and check with zero errors.
5. Push branch, open Plan PR, verify exact-head Plan . validate SUCCESS, and merge normally.
6. Record PR/main SHA and final END status in published evidence; post coordinator END.

## Ansatz block

Frontmatter owner verbatim from fetched origin/main: `Lead Worker W03 (Codex subagent)`.
Git user.name: `w255-0428-251-demo170codex`.
Git user.email: `w255-0428-251-demo170codex@baseharbor.local`.
Literal commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit ...`.
Pre-push author gate: `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`.

## Provenance and scope

Verified Plan repository remotes before evidence commit:
`origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
`origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
Fetched base ref: `origin/main` = `b586c707eae93b2e1fa20d25bb48c4a5ff9c9c11`.
The branch will be created from this exact fetched main SHA; no candidate branch is included.

## Findings before edit

Card `t-20261116-r28-bug-apply-consent-ux` / 0428-292 on fetched main had `owner: Lead Worker W03 (Codex subagent)` and `kanban_status: active`; generated card/link owner sections repeated the phantom owner. Mission and coordinator clarification establish no live implementation lane; reconciliation target is empty owner and planned status. `codeman agent list --json` contained no session with the phantom owner name. The status field is being corrected to `planned`; generated lane/view state is left to renderer.

## Change and validation

Applied only to the target card frontmatter: `owner: ""` and `kanban_status: planned`. The renderer set `kanban_lane: ready`, updated the target card's generated checkbox tags and Owner sections to `unassigned`, and refreshed generated views. The unstarted task is now Planned/Ready; it is not Active. PRs, body authored sections, and other target-card frontmatter are unchanged.

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed: 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings. Warnings are existing accepted-dependency notices for the r27 task group.

The full renderer also refreshed the generated owner preview for `t-20261128-hunt48-metrics-endpoint-docs` to match its current frontmatter (`w397-0428-307-idfallback`); that card's authored frontmatter was not edited.

`git diff --check` reported trailing spaces in generated Markdown hard-break lines (the target card's generated card/link sections and the renderer-refreshed unrelated card preview). These are emitted by `plan.py render`; no generated text was hand-edited.

## Cleanliness

Before worktree changes: `docker ps -a` (PID 1647402) returned the header only; no containers were running.

## END

Pending PR review, validation, and merge.
