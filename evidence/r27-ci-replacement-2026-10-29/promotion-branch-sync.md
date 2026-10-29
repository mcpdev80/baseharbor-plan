# t-20261027-r27-cutover-pr3 — BRANCH-SYNC #1205 (o219)

Owner-Direktive 2026-10-29 Option 2. Dispatch: `evidence/board-2026-10-29/prompts/o219.txt`.
Referenced policy/merge evidence: `evidence/board-2026-10-29/codex-merge-1206.md` Abschnitt m1206g.

## PLAN

- [✔] 0. Read dispatch + referenced m1206g; record plan. Native TodoWrite used; plan recorded here.
- [☐] 1. worktree add at develop head 1f94951d; create `-new` branch; `-s ours` merge origin/main (7a417d37) so main is an ancestor of the promotion head.
- [☐] 2. VERIFY paste (removed-line grep = 0), `diff 1f94951d HEAD --stat` empty, `merge-base --is-ancestor origin/main HEAD` exit 0.
- [☐] 3. push `-new` branch; PATCH PR #1205 head to `-new`; read back `gh pr view 1205` mergeable/mergeStateStatus.
- [☐] 4. Await exact-head PR Checks to terminal (poll max 8 min).
- [☐] 5. Record all SHAs + command outputs; END.

## ZUSTAND (before)

- develop `1f94951d2dc014ff924f35777b08a96e75781c06` (tree `da634e74`, contains all main hardening)
- main `7a417d378292724e1820c976b110fe3c107eba45`
- PR #1205 base `main`, head `work/r27-promote-ci-registration`, standing at `f95b3446`, CONFLICTING
- Role: MERGE lane only — branch SYNC, PR-patch, push. NO PR merge, NO ruleset change. (Per m1206g: #1206 already squash-merged; develop is now `1f94951d`, parent `f95b3446`.)

## RESULT

END o219 ...
