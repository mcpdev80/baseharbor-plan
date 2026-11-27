# w384-0428-321-1866pre — disjunct prerequisite akte (state, no push)

**Card:** 0428-321 (document baha exit-code taxonomy) · **Repo:** mcpdev80/baseharbor · **PR:** #1866
**Lane identity (verbatim from mission):** `w384-0428-321-1866pre` (email `w384-0428-321-1866pre@baseharbor.local`)
**Lane type:** WORKER lane — "NO merges" absolute; no push, no hosted run, no workflow_dispatch, no product edit.
**Commit identity rule for any future commit (visible SATSZ block):** author+committer `git -c user.name=w384-0428-321-1866pre -c user.email=w384-0428-321-1866pre@baseharbor.local commit ...`; pre-push gate `git show -s --format=%an HEAD` must equal `w384-0428-321-1866pre` exactly.

## (a) PR #1866 witness

Command: `gh pr view 1866 --repo mcpdev80/baseharbor --json headRefOid,headRefName,baseRefName,state,mergeable`
```
{"baseRefName":"develop","headRefName":"w334-0428-321-exitcodedocs","headRefOid":"3702c09502203e82633d664690eac9484a370df9","mergeable":"MERGEABLE","state":"OPEN"}
```

- baseRefName: `develop`
- headRefName: `w334-0428-321-exitcodedocs` (matches card blocker-text head)
- headRefOid: `3702c09502203e82633d664690eac9484a370df9` (matches mission ref `3702c095`)
- state: OPEN
- mergeable: MERGEABLE

Reference attestations (own `git ls-remote`, remote URL `https://github.com/mcpdev80/baseharbor.git`):
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w334-0428-321-exitcodedocs
3702c09502203e82633d664690eac9484a370df9	refs/heads/w334-0428-321-exitcodedocs
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
ea5218d72e263f21e79853b679af50074dab8c25	refs/heads/develop
```

## (b) Own worktree

Created detached worktree from the PR head (NOT from develop, NOT from another candidate):
`/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w384-0428-321-1866pre`
HEAD `3702c0950` ("Merge remote-tracking branch 'origin/develop' into w357-hop-1866", detached).

## (c) develop merge (local only, no push)

Pre-merge base attestation: `git ls-remote ... refs/heads/develop` → `ea5218d72e263f21e79853b679af50074dab8c25`.
`git fetch https://github.com/mcpdev80/baseharbor.git develop:refs/remotes/bh-develop` (local ref `bh-develop`).
`git merge bh-develop` → **clean**, exit 0, no conflicts. No STOP required.

Merge commit: `4dd073d24` "Merge remote-tracking branch 'bh-develop' into HEAD".
- `git merge-base --is-ancestor bh-develop HEAD` → YES (develop is ancestor of merge head).
- `git merge-base --is-ancestor 3702c095... HEAD` → YES (PR head preserved on top).
- `git diff bh-develop..HEAD --name-only` → ONLY the card's 9 exit-code files:
  `cmd/baha/main.go, docs/de/reference/cli.md, docs/de/reference/errors.md, docs/reference/cli.md, docs/reference/errors.md, internal/cli/cli.go, internal/cli/cli_test.go, scripts/documentation-audit.sh, scripts/exit_code_taxonomy_audit.py`.
- `git log bh-develop..HEAD` → develop + only `0428-321` exit-code commits (cdb6e4d97, d73fdef9a, 03354deb8, 6609608f5, c0c39f3b9, 33754a9a0, 2f7334988, abeba2c1a, 3702c0950). No foreign commit on top.

NOTE (identity hygiene): the working tree's git identity was still `w373-0428-284-demo183fix` (stale from a previous lane). The local merge commit `4dd073d24` therefore carries author/committer `w373-0428-284-demo183fix`. This merge is analysis-only and is NOT pushed and NOT evidence. Any future commit under this lane MUST use identity `w384-0428-321-1866pre` per the visible SATSZ block above.

## (d) Check / run situation on the current head (3702c095, nothing changed)

Terminal run for this head: **run 45916731635** (event `pull_request`, conclusion `failure`, updated 2026-11-27T00:40:46Z). Both other runs are superseded (run 45909111789 cancelled 00:25:43Z).

`gh pr checks 1866` aggregate result: `PR Selected Checks  fail  7s  .../runs/45916731635/job/140242097317`.

Within run 45916731635 the executed jobs are all green (20 success / 10 skipped / 0 failed by the jobs API), including both `PR · Native · native/docker/data-capabilities` and `PR · Native · native/podman/data-capabilities` → success. The failing aggregate is the **`PR Selected Checks`** union, driven by the **`Selected Runtime (atomic/…/data-capabilities, docker|podman)`** job — reported by `gh pr checks` as FAIL at job ids 140238551139 (docker) / 140238551015 (podman), run 45916731635. Those two job ids do NOT appear in the run's 30-job list and `gh api …/jobs/<id>` returns 404, so they belong to a run attempt that was superseded; the aggregate per-check state still reports FAIL for that union.

Why the union fails: the PR head carries the stacked pagination chain (`contracts/machine/v1/read-models.golden.json`, `read-models.schema.json`, `internal/apierror/pagination.go` + pagination contract tests, spec docs) that the exact-candidate `data-capabilities` gate validates. That gate is a Docker/Podman native gate — it executes on the named SSH test hosts (`baha-docker` / `baha-podman`), **never** on this coordinator host, and the mission forbids a hosted re-run here.

**What a qualifying run on the NEW head must deliver (two distinct run IDs on the exact pinned head):**
- Exactly ONE `PR Selected Checks` SUCCESS (the union) — i.e. every check the CI policy selects for this PR's impact green on the exact post-pin head — AND a second independent qualifying run, i.e. a **second distinct run ID** on that same exact head, produced by **close+reopen** (`gh pr close --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen`). A rerun of the same ID (run_attempt) is VOID as pair evidence.
- Both run IDs must show the `data-capabilities` exact-candidate gate actually executed (not skipped) on the new head.
- These runs are the pin-transport lane's responsibility AFTER the #183 merge (merged as `08cd018d4`) and after `BASEHARBOR_PR_DEMO_SOURCE_SHA` is advanced — NOT this lane.

## (e) Doc state on develop (file:line)

`git show bh-develop:docs/reference/cli.md | grep -ciE "Process exit codes"` → **0**. The exit-code taxonomy section is **NOT** on develop.

Content enters the tree at commit `cdb6e4d97` "0428-321 document baha exit-code taxonomy + machine coverage check", follow-up fix `d73fdef9a` "route context.Canceled->130 through cli.ResolveProcessExitCode regression". Documented anchors present on the head:
- `docs/reference/cli.md` line 20 `## Process exit codes`; table rows 26/29/30/32/34 (`0`, `2`, `130`, `143`, passthrough `1-255`), source-line anchors `internal/cli/cli.go:102-127`, `:114-117`, `SignalExitCode`, `ResolveProcessExitCode`.
- `docs/reference/errors.md` line 5 cross-links `cli.md#process-exit-codes` (`0` success, `1` runtime, `2` usage, `130` SIGINT, `143` SIGTERM, passthrough `1-255`).
- Machine-coverage check added: `scripts/documentation-audit.sh` row (lines 245-264) runs `python3 scripts/exit_code_taxonomy_audit.py`; audit file `scripts/exit_code_taxonomy_audit.py` (documented set exactly `{0,1,2,130,143}` + passthrough `1-255`).
- Go contract test: `internal/cli/cli_test.go` + `main_test.go` in pr-gate (per card commit c0c39f3b9).

Conclusion: a re-run on develop would re-audit a **non-empty** change — the doc content is absent on develop and present on the head. Re-run is not a no-op.

## What is owed after the #183 merge + pin

The card 0428-321 implementation (doc + audit + contract test) already sits on PR #1866 head 3702c095. What remains, for the pin-transport lane (NOT this one):
1. #183 merged (as `08cd018d4`) as the chain base, then advance `BASEHARBOR_PR_DEMO_SOURCE_SHA` for the demo pin.
2. Cut the next head from that pin, push it (own lane identity `w384-…`), and book **two** distinct Hosted runs (close+reopen pair) on the exact pinned head so the exact-candidate `PR Selected Checks` union — including the Docker/Podman `data-capabilities` gate — executes and goes green on the new head.
3. Native Docker + rootless Podman `data-capabilities` each executed (not skipped) on the new head.
4. `git log origin/<base>..HEAD` lists only the lane's own commits; pre-push `git show -s --format=%an HEAD == w384-0428-321-1866pre`.

## Cleanliness
- No containers/compose started this lane; no docker/podman daemon touched on any host.
- Worktree `workers/worktrees/w384-0428-321-1866pre` left in place (detached HEAD `3702c0950`, merge commit `4dd073d24` local, unpushed). Foreign worktrees untouched.
- No product file edited; no plan field or generated view touched.
- No push (this lane), no workflow_dispatch, no merge, no subagent.

## Publishing addendum (blocker: shared-checkout push race)

The akte content above is complete and correct (blob, 92 lines + addendum). Publishing the single plan-evidence commit to `origin/main` via the isolated worktree `workers/worktrees/w384-0428-321-1866pre-plan` was BLOCKED by an aggressive concurrent writer on the shared baseharbor-plan checkout: since ~07:31 origin/main moved every 2-3 min by lanes w383/w386/w351, and every `git push` landed server-side but was superseded by a concurrent push within milliseconds, so the akte commit never became the durable tip (fast-forward push rejected on the next attempt). Tight loops (up to ~200 attempts, multiple 600s+ timeouts) never won the final race. Per Coordinator 2026-11-27 answer (no writer-pause, no holding the shared checkout): the dirty shared checkout is a blocked publish path — left it and pushed from a fresh clone at `/var/tmp/qa-plan-marcel/w384`. No force push, no --no-ff, no merge, no hosted run; akte blob sha recorded below as counter-proof.

## END
`END_BLOCKED w384-0428-321-1866pre` — disjunktive Vorarbeit COMPLETE: PR witness (a), own worktree from PR head (b), clean local develop merge onto card head with no foreign commit / no conflict (c), check/run situation documented (d), doc-absence-on-develop proven with file:line (e). The single remaining step — publishing the akte commit to `origin/main` — was blocked by an aggressive concurrent writer on the shared baseharbor-plan checkout (addendum); publishing relocated to fresh clone `/var/tmp/qa-plan-marcel/w384`. No content blocker.
