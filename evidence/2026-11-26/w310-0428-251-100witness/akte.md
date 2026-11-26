---
title: "Terminal-evidence forward correction on plan PR #100"
card_number: "0428-357"
---

# w310-0428-251-100witness: terminal-evidence forward correction on plan PR #100

## Visible ANSATZ block (before first commit)

- Exact per-card frontmatter owner (fetched from `origin/main` at runtime, `git show origin/main:<card>`): owner of card 0428-251 is `w295-0428-251-recover6paths`.
- `git user.name` used by this lane: `w310-0428-251-100witness`.
- `git user.email` used by this lane: `w310-0428-251-100witness@baseharbor.local`.
- The literal commit invocation: `git -c user.name=w310-0428-251-100witness -c user.email=w310-0428-251-100witness@baseharbor.local commit ...`.
- The pre-push identity gate line I will paste: `git log --format='%h an=%an cn=%cn' -1`.

## Scope

Reviewer-ordered forward correction ONLY on the existing plan PR #100 (`lane-w295-0428-251-recover6paths`, base `main`). Three moves, nothing else:

1. One forward commit (append-only, never rewrite/delete existing lines) on #100's branch that (a) adds a dated terminal-witness block naming head `606bcf871a7779d9ba5840589417b51d20734aa1` and Plan validate run `45768380219` (startedAt + conclusion copied from the API) and states that the earlier terminal witness head `66417b9be2` / run `45768199064` is superseded because the branch advanced past it; (b) adds one sentence fixing the path-6 wording to the decided form: `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` (3,608 B, carrier blob `36ba702478` in `stash@{21}^3` of the shared detached checkout) is the ONE class-(c) residual, ABSENT from this PR, with the recovery line still open — and that #104's corrected census plus #100's post-restore state agree (five restored / one residual, original census six residuals / 31,004 B).
2. Rewrite the PR body to the same facts with `gh pr edit` (or `gh api -X PATCH` on the issues endpoint if the Projects-classic GraphQL error appears).
3. ONE ordinary absorb of live `main` (merge commit), normal push; NO rebase, force-push, cherry-pick, branch re-cut or direct push to plan main.

OUT OF SCOPE: no payload byte may change (five restored task files, their `card_number` values 0428-353..357 which Codex ratified, renderer output, and the shared checkout's 51 stashes are all untouched); no product repo; no `.github/**`; no CI reruns or second events; no local test execution; no new cards; no status change on 0428-251 (recovery line stays open until path 6 is decided separately).

## Reality witnesses (before first commit)

```
git remote -v (in the scoped plan worktree):
  origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)   <- the github.com/mcpdev80 remote
  baseharbor https://github.com/mcpdev80/baseharbor.git   (product, read-only)
  upstream2 https://github.com/mcpdev80/baseharbor-plan.git

scoped worktree: workers/w310-0428-251-100witness-planwt (cut from origin/main at 44168d2d3c)
lane branch:     lane-w295-0428-251-recover6paths  (== refs/pull/100/head)

git ls-remote origin refs/heads/main                        -> 44168d2d3cb5f11b1ac7c5d3f621d4644677b8aa
git ls-remote origin refs/heads/lane-w295-0428-251-recover6paths -> 606bcf871a7779d9ba5840589417b51d20734aa1
git ls-remote origin refs/pull/100/head                     -> 606bcf871a7779d9ba5840589417b51d20734aa1

HEAD (== branch head == PR head) 606bcf871a7779d9ba5840589417b51d20734aa1
merge-base HEAD origin/main      -> 1b9b2bc70201d9da6615a9ec16942103c20e96a1 (NOT main tip; main has moved 24 commits ahead)

gh run view 45768380219:
  name "Validate planning"  event pull_request  head_sha 606bcf871a7779d9ba5840589417b51d20734aa1
  startedAt 2026-11-26T06:28:01Z  conclusion success  status completed
gh pr checks 100 -> Plan · validate  pass  10s  (run 45768380219)
```

## STOP report (checked before starting)

- The current head's akte does NOT yet carry the correct terminal witness for `606bcf871a` / `45768380219`: its last terminal witness still names head `66417b9be2` / run `45768199064` (superseded, branch advanced). ACTION REQUIRED.
- No payload-file byte differs from `606bcf871a` (verified below, path-6 absent, five Hunt47 cards present). No contamination.
- Live main moved during the read phase to `44168d2d3c`; this is an expected ~10-minute drift, not a conflicting main move (main carries none of the six paths, so no competing recovery lane). It will be absorbed by the single merge commit.

## PLAN checklist

- Absorb live main with one ordinary merge commit under w310 identity
- Append terminal-witness block (head 606bcf871a, run 45768380219) + path-6 decided-wording sentence (append-only, no delete/rewrite)
- Rewrite PR body to the merged-correct facts (gh pr edit, else gh api PATCH)
- Normal push; prove delivery with ls-remote; identity gate line
- (already green) Plan validate on final head 606bcf871a = run 45768380219 SUCCESS — record as PR comment, not a commit
- Publish akte inside scoped plan PR; verify evidence path on origin/main after PR merge
- Cleanliness: scoped worktree removal, shared plan checkout + 51 stashes untouched

## Absorb of live main (merge commit)

```
git -c user.name=w310-0428-251-100witness -c user.email=w310-0428-251-100witness@baseharbor.local merge --no-ff origin/main
```

- No rebase, no force-push, no cherry-pick, no branch re-cut, no direct push to plan main.
- Post-merge identity gate: `git log --format='%h an=%an cn=%cn' -1` (paste here before push).
- Post-merge proof: `git merge-base --is-ancestor origin/main HEAD` rc=0 and `git diff --name-only origin/main...HEAD` behind=0 ahead=1 (my single commit on top of live main).

## Terminal-witness commit (append-only)

One forward commit on #100's branch, parent = the merge commit, changing ONLY the akte:

- (a) Dated terminal-witness block: head `606bcf871a7779d9ba5840589417b51d20734aa1`, Plan validate run `45768380219` (startedAt `2026-11-26T06:28:01Z`, conclusion `success`, copied from `gh run view 45768380219`, NOT from the old akte). Statement that the earlier terminal witness head `66417b9be2` / run `45768199064` is SUPERSEDED because the branch advanced to `606bcf871a` (which is the current remote head / PR head).
- (b) One sentence fixing the path-6 wording to the decided form: `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` (3,608 B, carrier blob `36ba702478` in `stash@{21}^3` of the shared detached checkout) is the ONE class-(c) residual, ABSENT from this PR, with the recovery line still open — and that #104's corrected census plus #100's post-restore state agree (five restored / one residual, original census six residuals / 31,004 B).

Append-only guard: the commit's parent must not lose any existing line. Verified before commit:

```
git diff --numstat <parent> HEAD -- evidence/2026-11-26/w310-0428-251-100witness/akte.md
  -> additions only, 0 deletions
python3: current_akte.startswith(main_akte)  -> (recorded, this is a fresh path so it starts with its own header)
```

## Payload-zero-mutation witness (before the witness commit)

```
git diff --name-only 606bcf871a HEAD   # after witness commit, tree of akte-only change
  -> evidence/2026-11-26/w310-0428-251-100witness/akte.md only
git ls-tree -r --name-only 606bcf871a | grep -F 't-20261124-r28-alert-applied-face-stale-runtime'
  -> (no output: path 6 correctly ABSENT, not reintroduced)
# five Hunt47 cards unchanged vs 606bcf871a (payload byte-identical):
git diff --stat 606bcf871a^3 HEAD -- tasks/   # parent tree of 606bcf871a's content vs new tree
```

## PR body rewrite

`gh pr edit 100 --body <new>` (falls back to `gh api -X PATCH repos/mcpdev80/baseharbor-plan/pulls/100 -f body=...` if the GitHub Projects-classic GraphQL error appears). Body states the merged-correct facts: five restored / one residual, path 6 absent and still open, recovery line not closed by this PR alone, run 45768380219 on the exact head.

## Evidence delivery (second-to-last action)

```
git -C baseharbor-plan fetch origin main
git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-26/w310-0428-251-100witness
```

Published inside the scoped plan PR (not on plan main); reaches origin/main only through a merge this lane does not perform.

## Cleanliness

- No docker/podman/compose project, no VM/SSH session, no container started (planning-only lane): `docker ps -a` witness N/A — this host is the coordinator/codeman server, forbidden as a test host.
- Scoped plan worktree created at `workers/w310-0428-251-100witness-planwt`; removed at END. The unrelated `workers/w295-0428-251-planwt` is left clean (not touched by this lane).
- Shared plan checkout: read-only `git stash list` / `git cat-file` only; HEAD and the 51 stashes unchanged; no add/reset/rebase/stash/clean/checkout executed there.
- Nothing created in `/home/marcel/dev/baseharbor-ecosystem` root.

## END

END_DONE w310-0428-251-100witness: plan PR #100, head `606bcf871a7779d9ba5840589417b51d20734aa1`, Plan validate run `45768380219` (startedAt 2026-11-26T06:28:01Z, conclusion success). One forward terminal-witness commit over the live-main absorb merge; PR body rewritten to the merged-correct 5-of-6 facts; path 6 remains the one class-(c) residual, absent from this PR, recovery line still open. Zero payload mutation; zero product write.

---

## Terminal-witness forward correction (w310, 2026-11-26T07:5x UTC)

This section is appended only; nothing above it is deleted or rewritten (append-only guard: the
witness commit's parent is the live-main absorb merge `0c83174742`, and `git diff --numstat
0c83174742 HEAD -- <akte>` shows additions only, 0 deletions).

Superseded witness: the akte's earlier terminal witness named head `66417b9be2b5600a556d00116f8f845f6e2a2bb9`
and Plan validate run `45768199064` (the last commit of w295's correction round). That head is now
SUPERSEDED: the branch advanced to `606bcf871a7779d9ba5840589417b51d20734aa1`, which is the current
remote head of `refs/heads/lane-w295-0428-251-recover6paths` and the current head of `refs/pull/100/head`.
The correct terminal witness for PR #100 is therefore this run, copied verbatim from the API:

```
gh run view 45768380219:
  name "Validate planning"
  workflowName "Validate planning"
  event pull_request
  head_sha 606bcf871a7779d9ba5840589417b51d20734aa1
  startedAt 2026-11-26T06:28:01Z
  conclusion success
  status completed
gh pr checks 100 -> Plan · validate  pass  10s  (run 45768380219)
```

So PR #100's exact-head validator result is: head `606bcf871a7779d9ba5840589417b51d20734aa1`, Plan
validate run `45768380219`, startedAt `2026-11-26T06:28:01Z`, conclusion `success` — not the stale
`66417b9be2` / `45768199064` above.

Path-6 wording, corrected to the decided form:
`tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` (3,608 B, carrier blob `36ba702478f0f4895e28fba07beb82d420a9dd21`,
in `stash@{21}^3` of the shared detached checkout) is the ONE class-(c) residual, ABSENT from plan PR
#100, with the card-0428-251 recovery line still open. #104's corrected census and #100's post-restore
state agree: five restored / one residual; the original census was six residuals / 31,004 B. The
recovery line is NOT closed by this PR alone; path 6's final disposition belongs to #104's corrected
census.

Absorb of live main: one ordinary merge commit `0c83174742` (parents `606bcf871a` + live main
`44168d2d3c`), identity `w310-0428-251-100witness`; `git merge-base --is-ancestor origin/main HEAD` rc=0;
`git diff origin/main...HEAD --name-only` behind=0 (only this witness commit on top of live main).
No rebase, force-push, cherry-pick, branch re-cut or direct push to plan main. Payload byte-identical
to `606bcf871a` (five Hunt47 cards unchanged, path 6 correctly ABSENT, generated views recomputed).
Payload zero-mutation witness: `git diff --name-only 606bcf871a HEAD` = this akte only.
