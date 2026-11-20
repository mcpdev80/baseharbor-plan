# coord-publish-integrity round-1 (0428-175)

- lane: coord-0428-175-publish-gates
- base SHA (branch cut from, coordinator master): 63565328
- my commit SHA: b2ddb78e (branch coord-0428-175-publish-gates, in worktree /tmp/coord-175-wt)
- base 63565328 IS an ancestor of b2ddb78e (verified: `git merge-base --is-ancestor 63565328 HEAD`)
- scope: coordinator/ repo only (self-protecting local repo, no remote). No product code, no baseharbor, no .github/**
- Owner-mandated worktree discipline: edits were applied in the main working tree by mistake and remain there for the Owner to restore; my committed work lives ONLY on branch coord-0428-175-publish-gates in the worktree. I did NOT run `git checkout`/`git reset` in the main tree.

## PLAN

- 1. Reproduce both defects against the current source (card-status.py payload, watch.py rm short id).
- 2. Add payload gate to card-status.py: check every field text it writes (note, blocker, resolution, summary) with the same rules as sanitize.py — character set (no CJK/kana/hangul/compatibility graphemes, EXACTLY sanitize.py's ranges) and the word-list Sprachregel (AGENTS.md 3.3 rule 7), referencing coordinator/scripts/wort-check.py as the authority.
- 3. Make card-status.py gate only the text the call intends to rewrite (diff-only scope), never the whole file, so existing cards are not blocked.
- 4. Fix watch.py: `rm`/`remove` must accept short OR full session id (unique prefix); an ambiguous prefix is refused; list must not show a removed entry; `rm --help` shows the real signature.
- 5. Write regression tests, each red-then-green: (a) CJK token in note -> exit 9 + no write; (b) forced Germanisation of an English Fachwort (example read from wort-check.py) -> exit 9 + no write; (c) `watch.py rm <short-sid>` against a temp registry -> entry gone; plus a parity test.
- 6. Run `bash -n` / `python3 -m py_compile` on every changed file; record output in the akte.
- 7. Check whether coordinator has a GitHub-CI home; if not, report the CI-coverage-deed with file:line to the coordinator (do NOT touch .github/**).
- 8. Commit only own files in the worktree; do not touch the main tree (Owner restores it); ls-remote witness in the evidence.

## repo-rule compliance

- Worked on branch coord-0428-175-publish-gates (worktree /tmp/coord-175-wt), cut from 63565328.
- Did NOT touch the coordinator's RUNBOOK.md, TICK-DUTIES.md, QUEUE.md, NOTRISS-*, or baseharbor-plan cards other than this evidence file.
- No product code, no baseharbor, no .github/** edits, no reruns/workflow_dispatch.
- No subagents: every step executed inside this session (AGENTS 4.8).
- No containers/networks/volumes started (cleanliness: none).
- Evidence lives ONLY in baseharbor-plan/evidence; nothing written into a product repo.
- Main-tree discipline: my edits were applied to the main working tree by mistake. They remain there for the Owner to restore; my committed work lives ONLY on my branch. I did NOT run `git checkout`/`git reset` in the main tree (Owner command 2026-11-20).

## tests und ergebnis

### DEFECT 1a — CJK token in note -> gate must fail, no write
- command: `python3 scripts/card-status.py <task> active --note "<CJK>" --no-push`; expect exit 9 and no change to file.
- result: exit 9, "ABGEBROCHEN (payload-gate): zeichensatz (note): nicht-lateinisches zeichen 0x4e2d", card unchanged. Unit test `test_cjk_note_rejected_no_write` green.

### DEFECT 1b — forced Germanisation of English Fachwort -> gate must fail, no write
- command: card-status.py with a note containing a word read live from wort-check.py's BAD list; expect exit 9 and no write.
- result: exit 9, "sprachregel (note): ...". Unit test `test_germanised_note_rejected_no_write` green.

### watch.py rm short id -> entry gone
- command: `python3 scripts/watch.py rm <8-char>` against a temp registry; expect entry removed, `list` no longer shows it, `rm --help` shows the real signature.
- result: short id removed cleanly (exit 0); full id removed; ambiguous prefix refused (exit 2); `rm --help` shows `wid`. Unit tests green.

### parity test (0428-175 point 3) — gate must mirror sanitize.py EXACTLY
- command: run identical samples through both /var/tmp/sanitize.py and payload_check.py; expect the same bad-char verdict on every sample.
- result: all 10 samples agree (clean/café/U+2014 -> not bad; CJK/kana/fullwidth/compatibility -> bad; hangul -> not bad, same as sanitize.py). `test_gate_agrees_with_sanitize_on_every_sample` green. `test_em_dash_is_allowed` confirms U+2014 passes the gate (matches sanitize.py).

### syntax
- command: `python3 -m py_compile scripts/card-status.py scripts/watch.py scripts/payload_check.py tests/test_publish_integrity_0428_175.py`
- result: PY_COMPILE OK.

### full run
- command: `python3 -m pytest tests/test_publish_integrity_0428_175.py`
- result: 10 passed (CJK rejected, Germanisation rejected, watch rm short/full/ambiguous, help, 2 parity).

## parity table: sanitize.py vs payload_check gate (in akte)

sanitize.py CJK ranges = U+0400-04FF (kirillisch), U+0300-036F (kombinierte diakritika), U+3000-4DBF + U+4E00-9FFF (CJK/kana), U+F900-UAFFF (compatibility), U+FF00-FFEF (halbvollbreite). It strips those, blocks (prints FK) if any present.

| input | sanitize.py | gate | agree |
| --- | --- | --- | --- |
| clean latin | not bad | not bad | OK |
| café (umlaut) | not bad | not bad | OK |
| note with U+2014 em-dash | not bad (allowed) | not bad (allowed) | OK |
| U+4E2D (CJK) | bad | bad | OK |
| U+306E (kana) | bad | bad | OK |
| U+AC00 (hangul) | not bad | not bad | OK |
| U+0301 (combining accent) | bad | bad | OK |
| U+FF21 (fullwidth) | bad | bad | OK |
| U+F900 (cjk-compat) | bad | bad | OK |
| U+4E00 (ideographic) | bad | bad | OK |

## CI coverage debt

- The coordinator repo has NO .github/workflows and no existing test runner of its own (tests/ holds only test_coord_tooling_fixes.py with no discoverable CI). Coordinator scripts are therefore NOT covered by any GitHub-CI job.
- Per §5.3 (CI-Aufnahmepflicht) and the mission's scope split, I will NOT edit .github/**. The tests above run locally as evidence, but they are NOT picked up by a GitHub-CI job. This is a CI-coverage-deed that must be handed to the coordinator (who reports it to the Owner).
- Needed change (file:line, for the Owner to implement): add a coordinator CI workflow (e.g. .github/workflows/coordinator-tests.yml) that runs `python3 -m pytest tests/` on the coordinator repo on every push; or add the coordinator scripts to an existing group's test selection. Until that trigger exists the local self-tests are the only evidence.

## evidence on origin/main

- command: `git ls-remote origin refs/heads/main`
- result: `7252d620fef140ffc5a81c827555784ef77d9fc3  refs/heads/main` (at time of writing; remote HEAD moves as coordination continues)
- my evidence file round-1.md verified present at origin/main HEAD (commit c11b0d4c): `git show origin/main:evidence/r28-welle4-2026-11-20/coord-publish-integrity/round-1.md` -> starts `# coord-publish-integrity round-1 (0428-175)`.

## r2/r3: conflict-tragend publish (owner, 2026-11-20)

- Third measured conflict (2026-11-20): two publications of coordinator/scripts/card-status.py got stuck with 'Automatic merge failed; fix conflicts and then commit the result' because another world (Codex lane, PR-sweep) AND this lane wrote to the same cards at the same time in the shared baseharbor-plan checkout. The Owner had to resolve by hand twice.
- Requirement added to the performance list (point 3): card-status.py must publish conflict-tragently instead of leaving the working tree in a merge conflict. Implemented in card-status.py:
  (a) before publish: `git fetch` + `git rebase origin/main`;
  (b) conflict in a note/blocker/wait_reason line: keep BOTH texts (union, timestamp order), never --ours/--theirs (no text loss);
  (c) conflict in kanban_status/owner/prs: ABORT with exit 2 (two writers must not silently merge structural ownership);
  (d) never leave the working tree with an open MERGE_HEAD; on unresolvable: `git merge --abort` + report to coordinator.
- Test: two clones publishing the same card's note one after another -> both texts present, MERGE_HEAD empty. Plus a structural-conflict test: two different owner values must abort, not merge. 12 tests, green 8/8 runs (flakiness was a test-isolation + marker-position bug, now fixed).

## main-tree restore handoff (Owner action)

- main working tree /home/marcel/dev/baseharbor-ecosystem/coordinator still had my modified scripts (uncommitted); the Owner restored it.
- patch backup (main-tree diff): /var/tmp/coord-175-main-diff.patch
- file backups: /var/tmp/coord-175-payload_check.py.bak, /var/tmp/coord-175-tests.bak
- my committed work (to cherry-pick once the main tree is restored): branch coord-0428-175-publish-gates, commits b2ddb78e (r1), 26a99705 (r2), 16096c0d (r3)

## branch + commit-sha for Owner merge

- branch: coord-0428-175-publish-gates (worktree /tmp/coord-175-wt)
- commits: b2ddb78e (r1 gates) -> 26a99705 (r2) -> 16096c0d (r3)
- base 63565328 confirmed ancestor of all three; no foreign commits in 63565328..HEAD
- Owner merges (I do not merge): report branch + commit-sha, Owner merges.
