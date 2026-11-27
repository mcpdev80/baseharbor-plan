# Board wait disposition: 0428-306 and 0428-307

## PLAN

1. Read the board-wait mission; incorporate coordinator correction to update only 0428-306 because 0428-307 is already blocked on main.
2. Verify current Plan main, card 0428-306 owner/status/PR, product PR #1874 head and exact run results; confirm 0428-307 is already blocked on main and untouched.
3. Record the owner-directed wait reason on card 0428-306 only using card-status helper in no-push mode.
4. Render and validate the isolated Plan clone; verify 0428-306 fields and 0428-307 unchanged from main.
5. Commit only the 0428-306 note, generated views, and this receipt on one branch; open one Plan PR and wait for exact-head validation.
6. Independently verify the PR, merge normally only on PASS, and record main SHA and claim reconciliation.

## Visible identity and base block

- Target card owner 0428-306 read from current origin/main: `owner: "w396-0428-306-goldenhelp"`; this value remains unchanged and is not the commit author. Card 0428-307 owner remains `w397-0428-307-idfallback` and is outside this correction.
- Assigned Codex session canonical identity: `w255-0428-251-demo170codex`.
- Git user.name: `w255-0428-251-demo170codex`.
- Git user.email: `w255-0428-251-demo170codex@baseharbor.local`.
- Commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit ...`.
- Pre-push identity gate: `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`.
- Planning remote witness before first evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Exact branch base fetched from real GitHub main: `ed7b8a601a16e3a17a1e0b77136d7ad4db68ea0c` (`refs/heads/main`); the isolated clone was fast-forwarded to this SHA before creating the candidate branch.

## Live evidence

- 0428-306 current card: active, owner `w396-0428-306-goldenhelp`, PR `mcpdev80/baseharbor#1874`.
- Product PR #1874 is OPEN at `b143395545bd2c5c4bd637ad476a5c4cc78630a4`.
- Runs `45993109149` and `45994654068` are both terminal FAILURE on that exact head; failing gates are `PR · Trusted Plan` (develop catalog missing rows) and downstream `PR Selected Checks`. Neither is qualification evidence.
- 0428-307 was already published on main by w267 at `ed7b8a601a16e3a17a1e0b77136d7ad4db68ea0c` as blocked, owner `w397-0428-307-idfallback`, PR refs `#1875`, `#1876`, and `#1877`; it is not changed by this candidate.
- Product PR #1877 is OPEN at `013fdfb82cf9dcab862aa430459bd880c0a806fd`; run `45998693008` is terminal FAILURE on that exact head. `PR · Trusted Plan` fails on the develop-catalog ordering; `PR Selected Checks` fails downstream. #1875/#1876/#1877 references remain unchanged.
- Codeman live-session metadata: `w396-0428-306-goldenhelp` and `w397-0428-307-idfallback` were `busy` when checked. The mission explicitly directs both cards to wait while the external catalog/fan-in prerequisite is unresolved.
- Owner-directed exact wait reason for 0428-306: `isolated per owner-check 2026-11-27: exact-head runs fail only on develop-catalog ordering (owner freeze-lift + scripts/pr-gate-map-v1.json release label). carriers: 306=#1874 at b14339554 (runs 45993109149/45994654068), 307=#1877 at 013fdfb82c (run 45998693008). resume trigger: fan-in #1861/#1862/#1863 merged to develop.`

## Intended mutation

Only card 0428-306 lifecycle/wait fields are changed through `coordinator/scripts/card-status.py` in no-push mode; preserve its owner and PR refs. Card 0428-307 is restored to its fetched main version and remains blocked. The renderer-generated views are the only other planned file changes.

## Scope correction, implementation, and validation

- Coordinator update at 2026-11-27T12:51:59Z narrowed the mission: w267 already published 0428-307 as blocked on main, so this candidate changes only 0428-306. The 0428-307 task note was restored byte-for-byte to fetched main and is absent from the final diff.
- Current Plan main remained `ed7b8a601a16e3a17a1e0b77136d7ad4db68ea0c`; `git ls-remote` returned `ed7b8a601a16e3a17a1e0b77136d7ad4db68ea0c refs/heads/main`.
- `coordinator/scripts/card-status.py t-20261125-hunt36-golden-help-guard wait --wait-reason '<owner-specified text>' --no-push` completed successfully in the isolated clone, configured via a temporary runtime config that pointed only at this clone. The helper cleared the blank blocker field as required for wait; owner and PR references were unchanged.
- Card 0428-306 is now wait with the exact owner-specified wait reason; owner remains `w396-0428-306-goldenhelp`; PR `mcpdev80/baseharbor#1874` and evidence run URLs remain intact.
- 0428-307 remains blocked on main, owner `w397-0428-307-idfallback`, blocker and PR refs #1875/#1876/#1877 unchanged; no 0428-307 file change is present.
- Final local `python3 scripts/plan.py render && python3 scripts/plan.py check`: 784 tasks, 0 errors, 10 existing dependency warnings.
- Generated Markdown contains renderer-required trailing spaces for line breaks in the wait rows; `plan.py check` passes. Intended tracked files are only `tasks/t-20261125-hunt36-golden-help-guard.md`, `views/kanban-dashboard.md`, `views/overview.md`, and `views/releases/v0.4.28.md`; plus this receipt.
- Candidate branch `w255-0428-251-demo170codex-board-wait306-307` is cut from exact main `ed7b8a601a16e3a17a1e0b77136d7ad4db68ea0c`. Precommit ancestry check `git merge-base --is-ancestor origin/main HEAD` succeeded; no foreign commits are on this branch.

## First candidate commit receipt

- Commit `cb7ed62dc746f488522facb79e5337f5e6a1699c`: author `w255-0428-251-demo170codex`; committer `w255-0428-251-demo170codex`. Pre-push identity line: `cb7ed62dc an=w255-0428-251-demo170codex cn=w255-0428-251-demo170codex`.
