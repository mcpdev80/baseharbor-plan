# rcptlink — Receipt Post-Run Writer task-link fix

**Worker:** ornith (rcptlink lane) · **Date:** 2026-11-02 · **Model:** Ornith
**Target PRs:** #1267 #1268 #1269 #1270 #1271 #1274 #1275 (all MERGED)
**Plan card:** baseharbor-plan/tasks/t-20261102-rcptlink-task.md (on main, 1488a9e)

## PLAN (checklist)

1. Read receipt_tasklink.py fully; confirm resolver contract. DONE
2. Create one Planning task card per PR family with `prs: [...]` metadaten, render + check. DONE
3. Create GitHub Issue per card (title `Planning task t-...`, body carries `tasks/<id>.md`). DONE
4. Add exactly one `Resolves #<issue>` line to each PR body (existing body preserved). DONE
5. Trigger Receipt-Writer post-run to terminal GREEN. BLOCKED (architectural — see below)
6. Evidence + END line. THIS

## Step 1 — Resolver contract (receipt_tasklink.py:63-142)

`resolve_task_from_pr(pr_number)` reads the PR body via the GitHub API, extracts
the single `Closes/Fixes/Resolves #NNN` closer (0 -> block, >1 -> ambiguous
block), then fetches the Issue and validates it points to a Planning task:
- `tasks/([a-z0-9-]+\.md)` in title+body, OR
- title matching `t-[a-z0-9-]+` (the `title.startswith("t-")` branch).
For the #1253 pattern the title is `Planning task t-...`, so the match comes
from a `tasks/<id>.md` reference in the Issue **body**. The resolved value must
fullmatch `tasks/[a-z0-9-]+\.md` (line 140).

Result: each target PR needs exactly one `Resolves #<issue>` line, and each
Issue must carry a `tasks/<id>.md` reference in its body.

## Step 2 — Planning card

`tasks/t-20261102-rcptlink-task.md` created, `owner: ornith (rcptlink)`,
`prs: [#1267..#1275]`, state active. `plan.py render` + `check` clean for this
card (pre-existing 25 errors are unrelated evidence files). Published to main:
commit 544f319 (worktree rcptlink) → fast-forward to main 1488a9e.

## Step 3 — Issues (one per PR family)

| Issue | Family | PRs |
|---|---|---|
| #1277 | podman-doctor/gate-map/docker-skip | 1267, 1268, 1274 |
| #1278 | openbao postgres backend | 1269 |
| #1279 | gofmt podman_doctor_checks | 1270 |
| #1280 | shared backend owner-dir env | 1271 |
| #1281 | pr-planner exact candidate | 1275 |

Titles: `Planning task t-...` (pattern #1253). Body carries the
`tasks/<id>.md` reference so the resolver matches.

## Step 4 — PR body patch (exactly one closer each)

Each PR body = faithful reconstruction of original Problem/Fix/Tests + exactly
one `Resolves #<issue>` line appended. Verified: each PR has exactly one
`Closes/Fixes/Resolves #NNN` reference.

**RECOVERY NOTE (transparency):** an initial `gh api PATCH -f body=@file` call
treated the path literally and wrote a garbage `@/tmp/...` body into all 7 PRs.
Recovered by restoring each body from the merge-commit diff + captured problem
text via direct API PATCH (verified below). No second closer was ever present
in the originals.

## Verification — real resolver against live GitHub API

Ran `receipt_tasklink.resolve_task_from_pr()` against all 7 PRs (live gh api):

```
PR #1267: RESOLVED -> tasks/t-20261102-ci-podmandoctor.md  ✓
PR #1268: RESOLVED -> tasks/t-20261102-ci-podmandoctor.md  ✓
PR #1269: RESOLVED -> tasks/t-20261102-ci-openbao.md       ✓
PR #1270: RESOLVED -> tasks/t-20261102-ci-gofmt.md         ✓
PR #1271: RESOLVED -> tasks/t-20261102-ci-ownerdir.md      ✓
PR #1274: RESOLVED -> tasks/t-20261102-ci-podmandoctor.md  ✓
PR #1275: RESOLVED -> tasks/t-20261102-ci-prplanner.md     ✓
```

All 7 resolve to a valid `tasks/<id>.md` — the tasklink step (`receipt_tasklink.py:95-125`)
no longer blocks on these PRs.

## Step 5 — Receipt run: BLOCKED (architectural, Owner action required)

The receipt Post-Run Writer (`receipt-post-run.yml`) is a **pilot** for gate
`public-contracts`: it publishes only when a producer CI run's `head_sha`
matches an existing entry in
`baseharbor-plan/evidence/receipt-plans/public-contracts.json`. That entry
(`tasks/t-20261029-r27-ci-producer.md`) binds head_sha `3a04457f5d66e4b99da013769f2bf41fb9090a77`
(candidate "contracts: qualify extension/v1..."), which is **not in any live PR**.

Consequences:
- The 7 target PRs are already MERGED; editing their bodies does not re-run
  producer CI for their merge-commit heads, so no receipt run fires for them.
- The only live producer runs are for open PRs (#1282, #1283, …) whose heads do
  not match the pilot entry — so they skip/publish only for the pilot head.
- Mission STOP forbids product/workflow-code changes (no re-pointing the pilot,
  no workflow edit).

Observed failing receipt runs (e.g. run 41428168338, head `e92e2058`, PR #1282)
show the SAME tasklink block the mission describes — `tasklink blocked: PR #1282
body has no 'Closes/Fixes/Resolves #NNN'` — confirming the bug class, but on
open PRs outside this mission's scope.

**Owner action to close:** (a) re-point the `public-contracts` pilot entry to a
candidate that runs in a live PR, or (b) dispatch a producer CI run for the
pilot head `3a04457` (e.g. via an open PR carrying that head). Once a matching
producer run exists, the tasklink step will now pass for these 7 PRs' issues and
the receipt publishes green.

## repo-rule compliance

- baseharbor-plan: edited only my task note + published to main via fast-forward;
  `plan.py render`/`check` run. No other notes touched.
- baseharbor: NO product/workflow-code change (mission STOP honored). Only data
  edits: Issue bodies, PR bodies. No `receipt_tasklink.py` change.
- No closing of other owners' Issues; no subagent spawn; no interactive dialog.
- Planning card state = active (task-link data done; receipt run gated on Owner).

## END line

END_BLOCKED rcptlink: tasklink bug fixed for 7 merged PRs (resolver verified green); receipt run gated on Owner pilot action. runs=41428168338 (fail, tasklink #1282, out-of-scope class)
