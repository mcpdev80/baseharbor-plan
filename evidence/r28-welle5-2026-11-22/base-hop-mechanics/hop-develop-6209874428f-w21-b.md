# Base-hop mechanics — hop to develop 6209874428f (two hops, coordinator directive w21hops2.g.md)

Lane: `w21-pr1702-0428-142-compat`
Directive: `/var/tmp/w21hops2.g.md` (two mechanical base-hops; PR #1754 .github exception does NOT apply here — .github/** and scripts/** must NOT be touched)
develop anchor: `6209874428f08dc3e90d6e29a42b30683ce9932a`
Product boundary: NO rebase, NO amend, NO force-push, NO content change. Conflict => STOP, name file, notify owner.

## PLAN
- Bullet 1: HOP A PR #1725 — fetch develop (rev-parse MUST be 6209874428f), fetch PR head, prove pre-head 0208f725996, additive `merge --no-ff` develop, `rev-list --count HEAD..develop` = 0, push OHNE force on branch from `gh pr view 1725 --json headRefName`.
- Bullet 2: HOP B PR #1597 — same procedure (pre-head 074678d149e).
- Bullet 3: watch each new PR-run to terminal (run-id + status + failed/skipped job names).
- Bullet 4: akte to evidence/r28-welle5-2026-11-22/base-hop-mechanics/hop-develop-6209874428f-w21-b.md.

## Method
- Remote: `origin` = `https://github.com/mcpdev80/baseharbor.git` (resolved via `git remote -v`).
- Dedicated worktrees: `hop-1725-wt` (branch w201-0428-201-statever), `hop-1597-wt` (branch perses-dashboard-databases-lane).
- Branch provenance: `git merge-base --is-ancestor origin/develop HEAD` => OK on both.

## HOP A — PR #1725 (branch w201-0428-201-statever)
- branch headRefName (gh pr view 1725): `w201-0428-201-statever`.
- fetch develop => `6209874428f` (anchor confirmed).
- fetch PR #1725 head => `0208f725996dbd3dd2889c984e045a2527454499` (pre-head).
- `git merge --no-ff 6209874428f` => additive merge commit (ort strategy).
- `git rev-list --count HEAD..6209874428f` => `0` (back=0).
- new head: `1ec67313ca0ff583d2faf0ad2e0c814e95c0d6aa`.
- push: `git push origin HEAD:refs/heads/w201-0428-201-statever` => `0208f725..1ec67313`, OHNE force.
- delivery witness (ls-remote): pre `0208f725996...` -> branch now carries `1ec67313`.
- new PR-run: `44975262053` (CI · PR #1725, pull_request).

## HOP B — PR #1597 (branch perses-dashboard-databases-lane)
- branch headRefName (gh pr view 1597): `perses-dashboard-databases-lane`.
- fetch develop => `6209874428f` (anchor confirmed).
- fetch PR #1597 head => `074678d149e5b8d0f899c55da92debf52bf0fd46` (pre-head).
- `git merge --no-ff 6209874428f` => **CONFLICT** in `cmd/baha/app_status_result.go` (merge conflict, HEAD/develop markers at lines 28-70).
- STOP: conflict NOT resolved. Branch unchanged (`074678d149e`), nothing committed, nothing pushed.
- Conflict file: `cmd/baha/app_status_result.go` (git status `UU`, markers at lines 28 `<<<<<<< HEAD`, 42 `=======`, 70 `>>>>>>> 6209874428f…`).
- Per directive: STOP, name file, notify owner. Owner resolves/decides.

## Run watching (AGENTS 4.6) — terminal
- HOP A PR #1725 run `44975262053`: **completed / FAILURE** (terminal, 02:24Z). Jobs: **16 SUCCESS, 14 SKIPPED, 0 FAILED jobs**. The aggregate FAILURE is a Required-Checks / workflow-level gate (all jobs success/skipped) — an Owner/CI-policy matter, documented only, not adjudicated.
- HOP B PR #1597: no run — STOP before push (conflict). No run to watch.
- skipped gates are NOT a proof; any selected-runtime job skipped is cited as skipped.

## Boundaries honored
- No rebase, no amend, no force-push, no content change to branch work. Hop A additive only.
- No .github/** or scripts/** touched on either hop.
- No local `go test`/`go vet`/compile (sha256 d65b09b8ffed). No subagents (AGENTS 4.8). No merge/close/GitHub comment.
- No container/compose project started by this sitz.
- Hop B conflict left unresolved and branch unpushed (correct STOP; not a defect).

## END
END_DONE w21-pr1702-0428-142-compat: two mechanical hops (w21hops2.g.md). HOP A PR #1725 w201-0428-201-statever 0208f725996 -> 1ec67313ca0ff583d2faf0ad2e0c814e95c0d6aa (additive merge --no-ff of develop 6209874428f, back=0, push OHNE force); new run 44975262053 terminal completed/FAILURE (16 SUCCESS / 14 SKIPPED / 0 FAILED jobs — aggregate FAILURE is a Required-Checks/workflow gate, Owner/CI-policy, documented only). HOP B PR #1597 perses-dashboard-databases-lane STOPPED on merge CONFLICT in cmd/baha/app_status_result.go (lines 28-70, HEAD vs develop markers); branch left at 074678d149e, nothing committed/pushed, conflict NOT resolved (owner decides). No further branch. Evidence: evidence/r28-welle5-2026-11-22/base-hop-mechanics/hop-develop-6209874428f-w21-b.md. 0428-226 round-2 fix STILL WAITING owner push to cli2-env-delete.
