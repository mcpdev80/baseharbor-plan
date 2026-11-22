# mission-1577-headfix (corrected order) — base-freshness merge, PR #1577

**Lane:** mission-1577-headfix
**Reviewer model:** worker-ornith1.5
**Date:** 2026-11-17
**PR:** #1577 | branch: 0428-092-perses-boundary | remote head before work: 70b7bfc8e | base develop: 8db0d9bdf
**Worktree:** /var/tmp/1577-fix-wt (isolated; no containers/compose started)

## Corrected order (owner/coordinate confirmed 2026-11-17)

The original FENSTERWERK premise was a coordinator error (Luna's story taken unverified).
Confirmed by lineage: `git merge-base ab9086f5 70b7bfc8e == ab9086f5` — the current head
`70b7bfc8e` **contains** the approved candidate `ab9086f5` and is newer. Therefore:
- NO content-checkout, NO revert of ab9086f5, NO force/rebase/reset.
- Real work = base-freshness: merge origin/develop, verify, push, PR #1577 ready, exact-head CI to terminal.

## PLAN

 - Reality sync (first action): ls-remote develop + branch; rev-parse HEAD == origin branch == 70b7bfc8e.
  - 0428-092-perses-boundary = 70b7bfc8e99c79cb20acc6974c67dcf2c037d446
  - develop = 8db0d9bdf8d9ae77db94c9ddce9c209001c4da54
  - Work at /var/tmp/1577-fix-wt (isolated worktree), aligned to remote head 70b7bfc8e.
* ( )git merge origin/develop (8db0d9bdf) — normal merge-commit, NO force/reset/rebase.
* ( )build/vet/gofmt + affected boundary tests green.
* ( )refspec-push + ls-remote witness; confirm my 70b7bfc8e base is ancestor of push; PR #1577 READY (gh pr ready if draft).
* ( )exact-head pull_request CI run to terminal (Eigenes-run-pflicht; cancelled => rerun).
* ( )append lineage block (merge-base proof, 572865ed stands) to akte evidence/r28-welle3-2026-11-16/perses-release-boundary/rebase-window-1.md.
* ( )END post to owner; GUI todos worker/todos/mission-1577-headfix.md.json.

## Repo-rule compliance

- No .github/** touched. No force/reset/rebase. No subagent. No product-repo writes outside /var/tmp worktree.
- No containers/compose started (no daemon pollution).
- One integration candidate only; worked only on branch 0428-092-perses-boundary.

## Reality witnesses

- ls-remote: `git ls-remote origin 0428-092-perses-boundary develop` => 70b7bfc8e / 8db0d9bdf.
- rev-parse: `git rev-parse HEAD` == `git rev-parse origin/0428-092-perses-boundary` == 70b7bfc8e.
- Lineage (from prior stop-report, 572865ed): merge-base ab9086f5..70b7bfc8e == ab9086f5; 70b7bfc8e is a newer superset.

## END

END_DONE mission-1577-headfix.md: base-freshness merge develop onto 0428-092-perses-boundary (70b7bfc8e), PR #1577 ready, CI to terminal.
