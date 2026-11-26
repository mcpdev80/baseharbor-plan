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

END placeholder — replaced at the last action.

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
