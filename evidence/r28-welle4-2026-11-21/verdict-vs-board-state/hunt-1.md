# H-V40 — Verdict gegen Zustand des KartBoards (hunt-1)

Lane: 0428-221-huntverd · ROLLE: Worker (BUG-HUNT, reine Befundung) · Slice: says the board what the verdict files say?
Datum: 2026-11-21 (UTC). Basis plan repo: origin/main (baseharbor-plan).

## PLAN

1. Collect all verdict-bearing files of the window from baseharbor-plan origin/main via `git ls-tree -r --name-only origin/main -- evidence/` (r28-welle4-2026-11-19/codex-review-wave, r28-welle4-2026-11-20/codex-review-wave, r28-welle4-2026-11-21/**), grep Verdict/Verdikt. Done — 156 candidate files, 73 carry an explicit verdict token.
2. Extract per file: PR number, ROLLE label, verdict, timestamp, candidate SHA. Done.
3. Per PR: card (card_number, prs field), kanban_status, resolution from tasks/. Done.
4. Actual PR head and state via `gh pr view` / `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/<N>/head` (real GitHub URL only; never the quarantined checkout). Done.
5. Classify contradiction classes (a)-(d); for (a) compute `git rev-list --count <verdict-sha>..<head>` and ancestry. Done.
6. Write this evidence file, commit and push to baseharbor-plan main, verify on origin/main, END post. Done in final steps.

## Method and remote witnesses

- Planning repo remote witness (run before any evidence work): `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)` — this is the real planning repo at /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (NOT workers/baseharbor-plan).
- Product remote truth was read only via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/...` and `gh pr view --repo mcpdev80/baseharbor`; an existing worker worktree (workers/0428-210-finalhop-wt, remote `origin https://github.com:mcpdev80/baseharbor.git` resolves to github.com/mcpdev80) was used only to fetch pull refs for ancestry math, never as a remote-truth witness.
- develop at measurement time: `77c1e60f51b91003ac3ddc391008c15e4a713a5c`.
- A verdict SHA reported as OBJECT-MISSING means: it is not reachable from the current PR head nor from develop after a full fetch of `refs/pull/<N>/head`; the branch history carrying it was rewritten (rebase hop or force-push).

## Verdict inventory (latest verdict per open PR) + board state

Only verdict-bearing files for PRs that are still OPEN (window 19.–21.11. files) and the decisive merged/closed cases are listed; merged PRs were folded into their final merge receipts.

| PR | card | kanban_status | verdict (latest, file) | verdict-sha | aktueller head | klasse |
| --- | --- | --- | --- | --- | --- | --- |
| #1596 | 0428-056 / 0428-149 (shared PR) | wait / review | REQUEST CHANGES (1627-wave r-akten) | 6135e73a (on-head) | 6135e73a | d |
| #1613 | 0428-073 | active | REQUEST CHANGES (codex-review-wave/1613-0428-073.md, 19.11.) | d8838f62 | d2bbcaf1 (CLOSED, unmerged) | a + b |
| #1627/#1736 | 0428-055 | active | REQUEST CHANGES (1627-independent-review) | 202b984e | 1627 head 202b984e; stacked PR #1736 head 8f11a34d not containing it | d |
| #1645 | 0428-091 | active | REQUEST CHANGES (codex-review-wave/1645-0428-091.md, ROLLE CODEX-REVIEW) | 0449f065 (OBJECT-MISSING) | 4d73aa97 | a |
| #1650 | 0428-078 | wait | REQUEST CHANGES r8 (codex-review-wave/1650-0428-078-r8.md, 20.11. 13:07) | 9add5e8a (OBJECT-MISSING) | 28c18f02 | a |
| #1684 | 0428-083 | closed accepted | APPROVE CONTENT owner-wire-blocked (1684-0428-083-r3.md) | 738ed514 (OBJECT-MISSING) | CLOSED; card accepted via #1745 (17bb0ffe, merged 21.11.) | c (read-back) |
| #1702 | 0428-142 | review | REQUEST CHANGES review-4 (21.11. 07:15) | b2f2fd3a (OBJECT-MISSING) | 2e4a570a | a + d |
| #1704 | 0428-073 | active | REQUEST CHANGES r3 (1704-0428-073-r3.md, 19.11. 22:05) | f5dcf128 (on-head, anc-of-head yes) | f5dcf128 | d (+ card not even in review) |
| #1709 | 0428-168 | closed accepted | APPROVE (1709-0428-168-r4.md) on 489e4e66 | 489e4e66 | MERGED 20.11., merged head 489e4e66 = verdict sha | clean |
| #1712 | 0428-166 | closed accepted | BLOCKED mid-review (1712-0428-166.md), then post-merge PASS (post-merge-068-166-develop-96f2ae11.md) | 5b016319 BLOCKED | MERGED a83fcc70 | c (read-back) |
| #1714 | 0428-183 | wait | REQUEST CHANGES (1714-0428-183.md, 20.11. 16:23) | 18e84809 (on-head) | 88290d3e | d |
| #1723 | 0428-199 | active | no verdict file found | — | 26755fc1 | — |
| #1725 | 0428-201 | wait | no verdict file found | — | cfd8851f (note 9bf4a72f) | — |
| #1733 | 0428-211 | closed accepted | APPROVE content-only (review-1.md, 21.11. 01:12) on 3a8b4a8b | 3a8b4a8b | MERGED head 3aec8701 (merge moved head after verdict) | a + c (read-back) |
| #1734 | 0428-212 | closed accepted | APPROVE (review-2.md, 21.11. 02:30) on 45d181ab | 45d181ab | MERGED head 2584cc81 | a + c (read-back) |
| #1735 | 0428-207 | closed accepted | REQUEST CHANGES (app-edit-core-activation/review-1.md, 21.11. 01:47) on 09cf55bb | 09cf55bb | MERGED 5617fd4e; no approve-file found — acceptance rests on the merged correction alone | c-variant (accepted without an APPROVE akte) |
| #1737 | 0428-213 | review | REQUEST CHANGES review-1 on 5be4f003; review-2 on 3010b212 (Verdikt REQUEST CHANGES) | 3010b212 (on-head lineage? no: 5be4f003 NOT ancestor; 3010b212 ancestor of head) | 37587b0e | d (review without fresh round after review-2) |
| #1738 | 0428-214 | active | REQUEST CHANGES review-1 (bdc3fcb6), review-2 (a8079303, OBJECT-MISSING) | a8079303 | 7e679293 (card round-6 cites REVIEW REQUEST CHANGES) | a |
| #1739 | 0428-210 | review | APPROVE CONTENT review-2 (21.11. 10:27) then review-3 (21.11. ~11:19, plan commit 0e70d7cf, AFTER this hunt's snapshot) | bb98e225 (review-3, on-head); 52866ae3 (review-2) | bb98e225 | a (review-2 stale; review-3 fresh — see Fund-1) |
| #1740 | 0428-209 | wait | APPROVE CONTENT (native-cell-operator-seam/review-1.md, 21.11. 05:19) | 0ffe0933 (on-head) | 0ffe0933 | b (APPROVE, card on wait; aggregate red via #1739) |
| #1741 | 0428-218 | review | REQUEST CHANGES review-1 on de4a45ec; review-2 (Verdikt REQUEST CHANGES) on fb5a5dea | fb5a5dea (on-head, 1 commit after de4a45ec) | fb5a5dea | d (needs new correction round) |
| #1742 | 0428-217 | review | REQUEST CHANGES review-1 on 0df7efc0 (21.11. 06:41) | 0df7efc0 | 719d28a8 — verdict-sha ancestor of head yes, NOT ancestor of develop; `rev-list --count` = 158 | a |
| #1746 | 0428-208 | review | no verdict file found | — | 0a710235 | — |
| #1747 | 0428-060 | — | no verdict file found | — | 8103f006 | — |

## Funde (Widersprüche)

- Fund-1 (klasse a, PR #1739 / card 0428-210): the APPROVE CONTENT in review-2 was bound to 52866ae3, which is NOT an ancestor of the then-current head bb98e225 (`rev-list --count` = 31) and is not an ancestor of develop — a hop rewrite dropped it. While this hunt ran, review-3 published an APPROVE CONTENT on the exact current head bb98e225 (plan commit 0e70d7cf, 21.11. ~11:19 UTC), resolving the staleness for the current head; review-1/2 remain stale-sha documents.
- Fund-2 (klasse a, PR #1742 / card 0428-217): the card sits in review although the only verdict is REQUEST CHANGES; and that verdict was written on 0df7efc0, which is 158 commits behind the current head 719d28a8 (monotonic, but no verdict exists for the current head).
- Fund-3 (klasse a, PR #1702 / card 0428-142): REQUEST CHANGES review-4 names b2f2fd3a; that object is unreachable from the current head 2e4a570a and from develop — the branch was rewritten after the verdict. No verdict file exists for the current head.
- Fund-4 (klasse a, PR #1650 / card 0428-078): five verdict shas (ac2a5450, 7705a336, cb985bde, 0baeaf55, 9add5e8a) are all unreachable from the current head 28c18f02 (only the base-side 681700ca survives). Every r-Verdict in the window describes a rewritten-away candidate.
- Fund-5 (klasse a, PR #1645 / card 0428-091): verdict sha 0449f065 unreachable from current head 4d73aa97; card additionally sits `active` with a PR that had an exact-head REQUEST CHANGES.
- Fund-6 (klasse a, PR #1738 / card 0428-214): review-2 sha a8079303 unreachable from current head 7e679293; card is `active` (not review) with REQUEST CHANGES open.
- Fund-7 (klasse a, PR #1733 / card 0428-211, closed): APPROVE bound to 3a8b4a8b; the PR merged as head 3aec8701 (post-APPROVE hop). Read-back for the merge window: acceptance content-wise OK, but the accepted sha differs from the merged sha.
- Fund-8 (klasse a, PR #1734 / card 0428-212, closed): APPROVE bound to 45d181ab, merged as 2584cc81 (same pattern as Fund-7).
- Fund-9 (klasse b, PR #1740 / card 0428-209): APPROVE CONTENT on the current head 0ffe0933 (review-1.md 21.11. 05:19), but the card sits `wait` — no card movement after the approval; the stated reason (aggregate red through 0428-210's test) is real state, yet the board field combination wait+APPROVE is not one of the defined transitions.
- Fund-10 (klasse b, PR #1613, closed unmerged): after the 19.11. REQUEST CHANGES no further review akte; the PR was closed without merge and card 0428-073 stayed active on the stacked PR #1704 (whose verdict is also REQUEST CHANGES, see Fund-12). APPROVE trail never existed, close without acceptance akte.
- Fund-11 (klasse c, read-back of the H-V36 pattern): accepted cards 0428-083 (#1608, #1684 CLOSED) and 0428-198/0428-204 (#1726 CLOSED) each list a PR that never merged; a merged successor carries the real content (#1745; #1726's work landed via other PRs). No accepted card with a truly unmerged outcome was found, but the accepted-card `prs` field contains dead PR refs — merge-window read-back needed.
- Fund-12 (klasse d, PR #1704 / card 0428-073): latest verdict REQUEST CHANGES (r3, 19.11. 22:05) at the current head f5dcf128; card is `active`, not `review`; no correction-round akte since.
- Fund-13 (klasse d, PR #1596 / cards 0428-056 wait, 0428-149 review): REQUEST CHANGES at the current head 6135e73a; 0428-149 sits review with no correction akte since (dual-card PR: one card waits on it, the other reviews it).
- Fund-14 (klasse d, PR #1714 / card 0428-183): REQUEST CHANGES at the current head (18e84809 anc yes), card `wait` — no new correction round recorded in tasks/akten since 20.11. 16:23.
- Fund-15 (klasse d, PR #1737 / card 0428-213): review-2 (21.11. 08:27) Verdikt REQUEST CHANGES; card on `review` but no correction round (round-5) after review-2; also the review-1 head 5be4f003 is not an ancestor of the current head (rewrite between r1 and r2).
- Fund-16 (klasse d, PR #1741 / card 0428-218): review-2 is a REQUEST-CHANGES correction round on fb5a5dea; card stays `review` awaiting the next hop; aggregate note says exact-head required checks failed/skipped/queued — the verdict-stop is honored, listed for completeness.
- Fund-17 (klasse c adjacent, PR #1627 / card 0428-055 `active`): the 19.11. independent review REQUEST CHANGES sha 202b984e is not an ancestor of stacked PR #1736 head 8f11a34d; no verdict exists for the stacked candidate; card active.
- Fund-18 (klasse a, PR #1691 / card 0428-121, closed): the r1 REQUEST CHANGES (b66b76c6) and the APPROVE (e5a943d1) both sit on branch history unreachable from develop (squash merge e1dc2cf6); the merged content descends from them but the verdict shas are not ancestors of the merged develop tree — same "verdict binds a non-mergeable sha" shape as the merged #1733/#1734 read-backs.

## Summen je Klasse (against OPEN PRs of the window; merged cases noted separately)

- (a) veraltetes APPROVE/RC an einem SHA, der nicht mehr im Branch ist: 6 Funde offene PRs (#1739, #1742, #1702, #1650, #1645, #1738) + 2 read-back merged cases (#1733, #1734) = 8.
- (b) APPROVE ohne Kartenwechsel: 1 Fund (#1740/0428-209), plus Fund-10 variant (verdictlos geschlossener PR) = 2.
- (c) karte accepted / PR nicht gemerged: 3 Karten-Zeilen (0428-083, 0428-198, 0428-204) mit CLOSED PR-Refs, jeweils durch gemergten Nachfolger aufgelöst; 0 echte accepted-with-dead-outcome Fälle im Fenster.
- (d) REQUEST CHANGES, Karte auf review/wait/active ohne neue Korrekturrunde: 7 Funde (#1704, #1596×2 cards, #1714, #1737, #1741, #1627/#1736).

## Gegenprobe: Karten 'accepted' mit nicht-merged PR (H-V36-stoff)

All cards in the window whose prs field names a baseharbor PR were checked against `gh pr view <N> --json state,mergedAt` (21.11. measurements): every `resolution: accepted` card with a PR shows state MERGED (e.g. #1575, #1577-#1582, #1590-#1592, #1598-#1600, #1602, #1616-#1618, #1621-#1626, #1628-#1635, #1638-#1644, #1648, #1651-#1661, #1663-#1666, #1668-#1683, #1685-#1699, #1701, #1703, #1705-#1713, #1715-#1723, #1725-1728 refs noted below, #1729-#1735, #1743-#1745). Exceptions found:
- #1684 (card 0428-083 accepted): CLOSED-unmerged, superseded inside the same card by #1745 which IS merged — acceptance is truthful, the prs field simply records the whole lineage. No contradiction.
- #1601/#1610/#1619/#1662/#1667/#1669/#1672/#1679-adjacent CLOSED-unmerged PRs: each belongs to a card whose prs field also lists the merged successor or whose resolution is superseded/dropped. No accepted-card-with-dead-PR found.
- #1613 (0428-073) and #1684's old head are CLOSED-unmerged while the card is not accepted — consistent.
Conclusion: the H-V36 class-(c) pattern (accepted card, unmerged PR) repeats in one shape: cards 0428-083 (accepted, `prs` lists CLOSED-unmerged #1608 and #1684) and 0428-198/0428-204 (accepted, `prs` lists CLOSED-unmerged #1726). In every case a merged successor is present (#1745 for 083; the develop path for 198/204), so acceptance is truthful but the `prs` field of an ACCEPTED card still names a PR that never merged — the board must not be read as "PR merged" from these cards. Non-accepted cards citing CLOSED PRs (0428-073/#1613, 0428-078/#1606, 0428-085/#1619, 0428-091/#1610) are consistent lineage records, and 0428-202 is superseded with CLOSED #1732 by design.

## Class (a) SHA-distance detail

| PR | verdict-sha | head | rev-list count verdict..head | verdict-sha ancestor of head | verdict-sha ancestor of develop |
| --- | --- | --- | --- | --- | --- |
| #1739 | 52866ae3 (r2) | bb98e225 | 31 | no | no (dropped by hop rewrite); r3 on bb98e225 is fresh |
| #1739 | 6442955f (r1) | bb98e225 | 79 | no | no |
| #1742 | 0df7efc0 | 719d28a8 | 158 | yes | no |
| #1702 | b2f2fd3a | 2e4a570a | NA (unreachable) | no | no |
| #1650 | 9add5e8a (r8) | 28c18f02 | NA (unreachable) | no | no |
| #1645 | 0449f065 | 4d73aa97 | NA (unreachable) | no | no |
| #1738 | a8079303 (r2) | 7e679293 | NA (unreachable; bdc3fcb6 r1 also not ancestor) | no | no |
| #1733 | 3a8b4a8b | merged 3aec8701 | merge-time hop after APPROVE | yes→merged | yes |
| #1734 | 45d181ab | merged 2584cc81 | merge-time hop after APPROVE | yes→merged | yes |

## cleanliness

No container, network, volume or state directory was created by this lane (read-only desk hunt: git ls-tree/ls-remote/fetch of pull refs, gh pr view / read-only evidence greps; no go test, no docker/podman commands beyond `docker ps -a` observation).

cleanliness: docker ps -a before = 0 rows, after = 0 rows (coordinator host; ambient bh-* stack untouched).

    $ docker ps -a --format '{{.ID}} {{.Names}} {{.Status}}'  # before (pid 2163400)
    (no rows)
    $ docker ps -a --format '{{.ID}} {{.Names}} {{.Status}}'  # after
    (no rows)

## Remote and delivery witnesses

Planning repo remote (verified before first evidence commit, per workspace rule):

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

Evidence delivery proof (second-to-last action):

    $ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep verdict-vs-board-state
    evidence/r28-welle4-2026-11-21/verdict-vs-board-state/hunt-1.md

Evidence commit: 872a24ec (tip at final push) on baseharbor-plan main; base at first evidence cut: 0e70d7cf, which already contained the concurrent review-3 publication for #1739. No product-repo commit, no PR action, no card change.

## repo-rule compliance

- ROLLE respected: reine Befundung; keine Produktdatei geändert, kein commit an baseharbor, keine PR-Aktion, keine Karten-Änderung (board fixes are the coordinator's work per mission GRENZEN).
- No subagents (AGENTS 4.8); every step executed in this session.
- Remote truth only via github.com/mcpdev80 URLs (`git ls-remote`, `gh pr view`); the quarantined workers/baseharbor checkout was never cited (worktree usage limited to object ancestry math after explicit https-URL fetches, ls-remote witnesses inline).
- No `git add -A`, no `git stash`, no bare `go test ./cmd/baha/`, no .github/** edits, no CI reruns.
- Evidence lives only in baseharbor-plan evidence/r28-welle4-2026-11-21/verdict-vs-board-state/ (no checkboxes anywhere in this file).
- Window note: card 0428-221 (this hunt's parent card `base-branch-provenance-loss`) references the same rewritten-history phenomenon the Fund-1/4/5/6 class-(a) rows independently confirm.


- ROLLE respected: reine Befundung; keine Produktdatei geändert, kein commit an baseharbor, keine PR-Aktion, keine Karten-Änderung (board fixes are the coordinator's work per mission GRENZEN).
- No subagents (AGENTS 4.8); every step executed in this session.
- Remote truth only via github.com/mcpdev80 URLs (`git ls-remote`, `gh pr view`); the quarantined workers/baseharbor checkout was never cited (worktree usage limited to object ancestry math after explicit https-URL fetches, ls-remote witnesses inline).
- No `git add -A`, no `git stash`, no bare `go test ./cmd/baha/`, no .github/** edits, no CI reruns.
- Evidence lives only in baseharbor-plan evidence/r28-welle4-2026-11-21/verdict-vs-board-state/ (no checkboxes anywhere in this file).
- Window note: card 0428-221 (this hunt's parent card `base-branch-provenance-loss`) references the same rewritten-history phenomenon the Fund-1/4/5/6 class-(a) rows independently confirm.

END_DONE 0428-221-huntverd: verdict-vs-board desk complete — 18 Funde: class (a) stale-sha verdicts on 6 open PRs (#1739 #1742 #1702 #1650 #1645 #1738, several verdict objects unreachable after hop rewrites) + 3 merged read-backs (#1733 #1734 #1691); class (b) APPROVE without card change: #1740/0428-209 (wait) + verdictless closed #1613; class (c): 0 accepted-unmerged outcomes, 3 accepted cards cite CLOSED PRs (#1684/#1608/#1726, successors merged); class (d) RC without correction round: 7 (#1704, #1596 x2 cards, #1714, #1737, #1741, #1627/#1736). Live-window movement observed during the hunt: 0428-210 went review→closed/accepted (#1739 merged) after review-3 approved exact head bb98e22599ab1f77edc056de73c682fdfdedd88a. Evidence commit 872a24ec on baseharbor-plan main.

## Late-window state changes (measured during writing, 21.11.)

- Card 0428-210 (#1739): moved review -> closed/accepted while this desk ran; #1739 merged. Its review-3 APPROVE binds the exact final head bb98e22599ab1f77edc056de73c682fdfdedd88a (fresh, not stale), so the Fund-1 class-(a) row applies only to review-1/2 documents.
- Card 0428-220 (#1732-class lineage check): `target-hotfix-inspection/round-1.md` carries a "Verdict"-word token only, no review verdict; card 0428-220 is `planned`, prs empty; its round-1 diagnosis concludes the bug no longer reproduces on current base and the card is stale. Excluded from the inventory as verdictless (task evidence, not a review akte).
- PR #1739 head re-verified by fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1739/head` = bb98e22599ab1f77edc056de73c682fdfdedd88a.
- Closing remote snapshot (final `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1738/head`): develop 97b2ba5543f07b820b5c18a688058fd932c4516f (advanced again after the earlier 77c1e60f measurements), #1738 head 7e6792939c552f89c66a53958c8eb7bcd255a1b3 unchanged. All class-(a) ancestor counts above were computed against develop 77c1e60f and remain valid for the verdict-sha-versus-head relation (head values did not move).
