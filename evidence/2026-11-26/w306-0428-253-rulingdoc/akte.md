# w306-0428-253-rulingdoc — akte: card 0428-253 ruling-document correction (plan-only)

Mission: `coordinator/missions/w306-0428-253-rulingdoc.txt`. PR #1853 (already MERGED), card 0428-253. Documentation-only correction on plan main. No product repo writes, no new cards, no CI triggers or reruns, no merges, no local test execution.

## PLAN

1. Read mission; verify plan repo remote; fetch live plan main tip. — done
2. Re-verify ruling file on origin/main (size 6961 B, blob 0c7f786d892d71abdbba7a0c3e790d09892a64a6). — done
3. Re-read GitHub witnesses for #1853 with gh before writing them down. — done
4. Create isolated plan worktree `workers/w306-0428-253-rulingdoc-plan` from the fetched main tip; visible ANSATZ block below. — done
5. Append dated forward-only correction block to the ruling file (admitted set, rejection boundary, canonical identity, live witnesses). — done
6. Fill the empty `evidence:` frontmatter list on card 0428-253 with the ruling + akte paths. — done
7. Write this akte incl. date-integrity finding, witnesses, cleanliness, END line. — done
8. render + check in a clean /var/tmp clone: fixed point, zero new errors, 10 pre-existing warnings unchanged. — pending at first commit, result appended below
9. Commit under canonical lane identity, push branch, open ONE plan PR (never merged by this lane). — pending
10. Watch own Plan validate run to terminal (Eigenes-Run-Pflicht); append run id + conclusion. — pending
11. Verify evidence path on origin/main, remove worktree, post END. — pending

## ANSATZ (visible identity block, written before first commit)

- Card owner VERBATIM fetched from origin/main (`tasks/t-20261123-planner-deleted-source-advisory.md`, line 10): `w205 (lane w205-0428-253)`
- git identity for ALL commits of this lane: `user.name=w306-0428-253-rulingdoc`, `user.email=w306-0428-253-rulingdoc@baseharbor.local`
- Literal invocation: `git -c user.name='w306-0428-253-rulingdoc' -c user.email='w306-0428-253-rulingdoc@baseharbor.local' commit -m '<msg>'`
- Pre-push gate line: `git show -s --format='%h an=%an cn=%cn' HEAD` must print `an=w306-0428-253-rulingdoc cn=w306-0428-253-rulingdoc` before any push.

## Remote and base attestation

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` shows `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)` — verified BEFORE the first evidence commit; the shared checkout was used read-only (`git show origin/main:...`, `git ls-tree`); the branch lives in an isolated worktree per the shared-checkout rule.
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` → `1b9b2bc70201d9da6615a9ec16942103c20e96a1 refs/heads/main` (2026-11-26T06:38Z, ≥ mission-stated tip 1b9b2bc70).
- Branch `w306-0428-253-rulingdoc` cut from exactly `1b9b2bc70201d9da6615a9ec16942103c20e96a1`; ancestry gate: `git merge-base --is-ancestor 1b9b2bc70201d9da6615a9ec16942103c20e96a1 HEAD` (shown in the commit/push section below).

## Task 1 — ruling-file re-verification (mission step "re-verify, then act")

- Blob on origin/main: `0c7f786d892d71abdbba7a0c3e790d09892a64a6`, size `6961 B` — both confirmed via `git cat-file -s` / `git rev-parse origin/main:<path>`.
- Content confirmed: names both shas (3 mentions of each short prefix), narrow exception, canonical owner `w205 (lane w205-0428-253)`, claim commit `201fb31ab73a7d08359140c30577bcdfeee2ca54`, and "no commit history is rewritten".
- Gap (1) CONFIRMED: `grep -i -E 'foreign|reject'` over the whole file → 0 matches. Rejection boundary was implicit only.
- Gap (2) CONFIRMED: card frontmatter `evidence: []`.

## Task 1 — appended correction block

Appended (forward-only, 10 lines, diff shows zero deletions) to `evidence/r29-welle6-2026-11-28/0428-253/w136-pr1853-admission-ruling.md`:
- admitted set exactly {`90c8017b`, `3c1ebc6f`} and nothing else;
- explicit REJECTION BOUNDARY sentence (shortened/role-suffixed/foreign lane identities are NOT admitted, PR HOLD pending forward provenance paragraph, no rewrite);
- canonical-string rule (`w205-0428-253` in BOTH author and committer via `git -c`) for future commits touching #1853 / card 0428-253;
- live GitHub witnesses re-read with gh (see next section);
- no-history-rewrite statement.

## Task 1(d) — live GitHub witnesses (re-read with gh at 2026-11-26T06:38Z)

- `gh api repos/mcpdev80/baseharbor/pulls/1853` → state closed, merged true, `merged_at 2026-11-25T23:57:23Z`, head `228ecc5bab28e5e6158ccc63160f442a6afc9ed3`, merge commit `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`.
- Reviews API: only two COMMENTED entries (no REVIEWED/ACCEPTSTATE review object). The final exact-head ACCEPT exists as the issue comment "## Final #1853 exact-head review — ACCEPT" (2026-11-25T23:57:20Z), which states: "Two distinct terminal-success pull_request runs on this exact head: 45716254159 attempt 1 and 45717496553 attempt 1. Both PR Selected Checks aggregates succeeded. Attempt 2 of run 45716254159 was cancelled and is excluded." (Merged via plan PR #47, merge `c11494fbd9c6b7b186f991a0ef988f099295a2ab`.)
- Run 45716254159: default view (attempt 2) = cancelled; attempt 1 via `gh api .../actions/runs/45716254159/attempts/1` = completed/SUCCESS, event pull_request, head 228ecc5ba.
- Run 45717496553: completed/SUCCESS, event pull_request, head 228ecc5ba, attempt 1.
- Check-runs on head 228ecc5ba: `PR Selected Checks` SUCCESS at details_url .../runs/45717496553/job/139568337781 and SUCCESS for attempt 1 of 45716254159 (the failure-suffixed aggregate row belongs to cancelled attempt 2).
- Witness nuance recorded forward-only: the mission phrasing "runs ... on the same head" is TRUE; run 45716254159 is only qualifying at attempt 1 — its attempt 2 was a rerun (same run id), CANCELLED, and is VOID as pair evidence per owner lesson 2026-11-25. Correction-block wording was written to match the re-read facts exactly.

## Task 2 — card evidence-field fill

- `tasks/t-20261123-planner-deleted-source-advisory.md`: `evidence: []` replaced with a three-item frontmatter reference list (ruling file, w205 lane akte `evidence/r29-welle6-2026-11-25/w205-0428-253-planner-deleted-source/akte.md` — exists on main, this akte). No status change, no contract text change.
- Schema note: the first fill used bare repository-relative paths; `scripts/plan.py check` rejected them with `error: ... evidence must be https links` (validator at `scripts/plan.py:435`, the board schema, not card-status). Per the established convention on other cards, the entries were rewritten as `https://github.com/mcpdev80/baseharbor-plan/blob/main/<path>` links. After that, `plan.py render` reports only the target file as updated and `plan.py check` is clean. `scripts/card-status.py` was not needed (no status change).

## Task 3 — date-integrity finding (FUTURE-DATED directory)

- FINDING: the ruling file lives under `evidence/r29-welle6-2026-11-28/0428-253/` — a directory label one to two days AHEAD of the host clock (`date -u` → 2026-11-26T06:36Z). The content-date label mismatch is recorded here as a date-integrity finding with the path; the file is NOT moved (moving would break links other lanes cite) and no second copy was created. Consistent with the AGENTS note that the '25.11'-style labels are date citations whose content, not label, is authoritative.

## Validation (render + check in clean /var/tmp clone)

- Clean clone: `git clone --branch main --single-branch https://github.com/mcpdev80/baseharbor-plan.git /var/tmp/w306-plan-verify` at tip `1b9b2bc70201d9da6615a9ec16942103c20e96a1`; the exact three-file change set was applied there and verified FIRST, then mirrored into the worktree (the shared detached checkout at 08b1f66bb and its stashes were never touched).
- Baseline check on the untouched clone tip: the 10 pre-existing warnings are the `accepted although dependencies are not accepted` lines listed by `plan.py check`.
- After the change: `python3 scripts/plan.py render` → `updated tasks/t-20261123-planner-deleted-source-advisory.md` and nothing else; re-running render afterwards produces no further diff (fixed point, confirmed in both clone and worktree).
- `python3 scripts/plan.py check` → `785 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings`. Zero NEW errors; the 10 warnings did not grow.
- The only generated diff is the `**Evidence:** [proof 1..3]` line inside the `<!-- generated:card -->` block of the edited card, which is the renderer's derived output and is committed with the frontmatter change.
- Clean-clone scratch was removed after validation (`rm -rf /var/tmp/w306-plan-verify` at END).

## Commit / PR / run witnesses

- Placeholder — appended below.

## Cleanliness

- No containers, networks, volumes or state directories were created by this lane (no docker/podman use at all; plan-only work).
- Created: git worktree `workers/w306-0428-253-rulingdoc-plan` (removed at END) and the clean validation clone under `/var/tmp/w306-plan-verify` (removed after validation).
- Shared checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`: untouched — read-only fetch/show only; no rebase/reset/stash/checkout/add there. `docker ps -a` witness line appended below.



## Commit / PR / run witnesses

- Commit `dd09ca4dc95d8160498e344efddb632c20d003ef` on branch `w306-0428-253-rulingdoc`, cut from plan main `1b9b2bc70201d9da6615a9ec16942103c20e96a1`.
- Identity gate: `git log --format='%h an=%an cn=%cn' -1` → `dd09ca4dc9 an=w306-0428-253-rulingdoc cn=w306-0428-253-rulingdoc` (author AND committer canonical, before push).
- Ancestry: `git merge-base --is-ancestor 1b9b2bc70201d9da6615a9ec16942103c20e96a1 HEAD` → OK.
- Log-line scope gate: `git log --oneline origin/main..HEAD` before the commit → empty (0 lines); after the commit → exactly `dd09ca4dc9 docs(plan): append forward-only correction block to 0428-253 admission ruling; fill card evidence refs` — only this lane's own commit.
- Diff-name gate: `git diff origin/main...HEAD --name-only` → akte.md, w136-pr1853-admission-ruling.md, t-20261123-planner-deleted-source-advisory.md (exact three-file write set).
- Forward-only gate: `git diff` on the ruling file shows `1 file changed, 10 insertions(+)`, zero deletion lines.
- Delivery witness after push: `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w306-0428-253-rulingdoc refs/heads/main` → `1b9b2bc70201d9da6615a9ec16942103c20e96a1 refs/heads/main` and `dd09ca4dc95d8160498e344efddb632c20d003ef refs/heads/w306-0428-253-rulingdoc`.
- Plan PR: https://github.com/mcpdev80/baseharbor-plan/pull/108 (opened ready, not draft; this lane never merges it).
- Own Hosted run (Eigenes-Run-Pflicht): workflow `Validate planning`, run `45770188193`, event pull_request, head `dd09ca4dc`, terminal `completed / SUCCESS`, observed by this lane to terminal.

## Final head, second own run, cleanliness

- Final head `0f8840b6772f6a2b12e4766c430b8b13896000c0` (`git log --format='%h an=%an cn=%cn' -1` → `0f8840b677 an=w306-0428-253-rulingdoc cn=w306-0428-253-rulingdoc`); `git log --oneline origin/main..HEAD` lists exactly this lane's two commits (`0f8840b677`, `dd09ca4dc9`) — no foreign commits.
- `git diff origin/main...HEAD --name-only` at final head → exactly: `evidence/2026-11-26/w306-0428-253-rulingdoc/akte.md`, `evidence/r29-welle6-2026-11-28/0428-253/w136-pr1853-admission-ruling.md`, `tasks/t-20261123-planner-deleted-source-advisory.md`.
- Second own run on final head: `Validate planning`, run `45770346080`, event pull_request, head `0f8840b67`, terminal `completed / SUCCESS` (observed by this lane). Run `45770188193` on `dd09ca4dc` was also SUCCESS; both watched to terminal per Eigenes-Run-Pflicht.
- cleanliness: this lane ran no docker/podman commands and started no compose projects on this host or any SSH host; `docker ps -a` shows only pre-existing ambient stacks (untouched, e.g. bh-* development containers belonging to other lanes). No test-owned containers, networks, volumes or state directories exist from w306. Created paths: worktree `workers/w306-0428-253-rulingdoc-plan` (removed after publishing) and validation clone `/var/tmp/w306-plan-verify` (removed after validation). The shared plan checkout was never written to.

## Coordinator correction turn (06:50Z) and final-state witnesses

- Coordinator order executed: one comment posted on plan PR #108 stating (a) the future-dated-path finding (`evidence/r29-welle6-2026-11-28/0428-253/` versus host date 2026-11-26) with the deliberate no-move/no-copy rationale and the akte section pointer, and (b) the admitted-set confirmation {`90c8017b`, `3c1ebc6f`} plus the verbatim rejection-boundary sentence. Witness: https://github.com/mcpdev80/baseharbor-plan/pull/108#issuecomment-7184778295
- Delivery witness after last push: `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w306-0428-253-rulingdoc refs/heads/main refs/pull/108/head` → main `1b9b2bc70…`, branch `5cda57e58a48dc451de6e00f2e036049b5ab3f20`, pull/108/head at that moment still `0f8840b67` (GitHub PR-head sync lag; branch ref is authoritative).
- Own third run (Eigenes-Run-Pflicht): `Validate planning`, run `45770501800`, event pull_request, head `5cda57e58`, terminal `completed / SUCCESS`, observed by this lane. Earlier runs `45770188193` (`dd09ca4dc`) and `45770346080` (`0f8840b67`) were likewise observed SUCCESS.
- Final identity gate: `git log --format='%h an=%an cn=%cn' -1` → `5cda57e58a an=w306-0428-253-rulingdoc cn=w306-0428-253-rulingdoc`; `git log --oneline origin/main..HEAD` lists exactly the three w306 commits; `git diff origin/main...HEAD --name-only` shows exactly the three write-set files. `plan.py render` fixed point, `plan.py check` → 0 errors, 10 pre-existing warnings.

[superseded by the final END_DONE line at the end of this file]

## Main-refresh and origin/main existence gate (last actions before END)

- New plan main `c30b1143b4a6c6b8046bd9f909674d3bf846783f` appeared (unrelated w281 content); absorbed via `git merge origin/main` under this lane's canonical identity (`git log --format='%h an=%an cn=%cn' -1` → `4074bfb129 an=w306-0428-253-rulingdoc cn=w306-0428-253-rulingdoc`), no force, no rebase, no cherry-pick. `git diff --name-only origin/main...HEAD` after the merge still shows exactly the three write-set files.
- Fourth own run on final head `4074bfb12`: `Validate planning`, run `45770819061`, terminal `completed / SUCCESS` (observed by this lane). Runs now watched to terminal: 45770188193, 45770346080, 45770501800, 45770680218, 45770819061 — all SUCCESS.
- Coordinator correction turn (06:50Z): #108 comment posted with the future-dated-path finding, no-move rationale, akte pointer, admitted-set {90c8017b, 3c1ebc6f} confirmation and the verbatim rejection-boundary sentence: https://github.com/mcpdev80/baseharbor-plan/pull/108#issuecomment-7184778295
- The akte path is introduced by this PR and is therefore on the PR head branch until merge; it cannot appear on origin/main before an authorized merge (precedent recorded in w136-1853-owner-ruling.md). Post-merge, re-verify with: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-26/w306-0428-253-rulingdoc/akte.md`.

## Ancestry confirmation for the coordinator (06:59Z order)

- (a1) `git ls-remote origin refs/pull/108/head` → `db736bfb0501abfbe1f1909f77146bbe76d34ef7 refs/pull/108/head`
- (a2) `gh pr view 108 --json headRefOid,mergeable` → head `db736bfb0501abfbe1f1909f77146bbe76d34ef7`, `MERGEABLE`
- (b) `git merge-base --is-ancestor c30b1143b4a6c6b8046bd9f909674d3bf846783f HEAD` → exit 0, ANCESTOR_OK (the absorb merge `4074bfb129` in this file's previous section is exactly that event; behind=0 on the compare is therefore genuine).
- (c) Plan validate run on the exact live head `db736bfb0`: run `45770951699`, startedAt `2026-11-26T06:50:09Z`, completed SUCCESS, observed to terminal by this lane.
- Explanation of the coordinator's two reports: the behind=1 observation keyed to `8a87f5d` predates the `git merge origin/main` absorb commit `4074bfb129`; the akte commit `db736bfb05` sits on top of that merge, so the current head contains `c30b1143b` and reports behind=0 ahead=5. No merge commit was needed for this confirmation turn.
- Date-integrity finding stands exactly as written: ruling file stays at `evidence/r29-welle6-2026-11-28/0428-253/` (no move, no copy); w267 rules whether the card also needs a dated forward note.

[superseded by the frozen-head END_DONE line at the end of this file]

## Candidate frozen (coordinator freeze order 07:04Z)

- Freeze order received; this is the LAST commit of this lane. Head before freeze was `351423ad6f` (the ancestry-confirmation akte commit), pushed in direct response to the 06:59Z confirmation order; the coordinator's SHA chain quote (5cda57e58 -> 4074bfb12 -> db736bfb0) predates that commit by minutes. The multi-push churn came from the three sequential coordinator correction turns plus one main-absorb merge, not from voluntary rework.
- Final head: `25a4758e17c766633e4602582e86d51577f58504` (identity at freeze: `git log --format='%h an=%an cn=%cn' -1` → `25a4758e cn=w306-0428-253-rulingdoc an=w306-0428-253-rulingdoc`; exact values pasted in the coordinator report).
- (2) Main ancestry: `git merge-base --is-ancestor origin/main HEAD` (origin/main = `c30b1143b4a6c6b8046bd9f909674d3bf846783f`) → exit 0 TRUE — c30b1143b is already an ancestor via merge commit `4074bfb129`; no new merge needed.
- (3) Plan validate run on THIS exact head — id, startedAt and conclusion pasted in the coordinator report and watched to terminal by this lane.
- Writing stops here: no further commits, pushes, file moves or copies. The date-integrity finding stands; the ruling file stays at `evidence/r29-welle6-2026-11-28/0428-253/`. Any further change is a reviewer-requested correction round.

END_DONE w306-0428-253-rulingdoc: #108 frozen single head 25a4758e (contains main c30b1143b, ancestor TRUE), own Plan validate run on that head watched to terminal SUCCESS; akte complete; lane stops.
