# 0427-165 r11 — rebase lane abandoned: card SUPERSEDED + session-role conflict

- Card/mission: mission-165-refresh.md (0427-165 landing-refresh, on PR #1500 head `f5883e1e9`)
- Session: `594fd2f5-4e80-43b6-9841-92879146a85e` — the **Coordinator (Codeman, Qwen Flash)**, name `w1-baseharbor: coordinator`
- Role of this lane per mission: a fresh **Worker** lane to linearly rebase PR #1500 head onto develop 8a2912c62, keep the regression split (lock-fall without orphans / refusal case) UNCHANGED, produce a terminal-green exact-head run with `--- PASS: TestUpNameResumesThroughCommandEntrypoint` in the raw job log, and hand off via `codeman agent post` to the coordinator session.

## BLOCK — two independent, authoritative blockers

### Blocker 1: card 0427-165 is SUPERSEDED
The authoritative task contract `tasks/t-20261108-bughunt-target-delete-orphan-records.md` (planning repo, `origin/main`) line 24 reads `superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak`. CardBoard `kanban_status` still shows `active` — that is stale; the `superseded_by` field governs. The mission asks to rebase/PR a card that is no longer live work.

### Blocker 2: my session is the Coordinator, not a Worker lane
`codeman agent list --json` shows my session id `594fd2f5...` = `w1-baseharbor: coordinator`. AGENTS.md (ecosystem coordinator rules) forbids the Coordinator from implementing product/worker code ("KEINE Produktimplementierung in dieser Session"). A linear rebase of PR #1500 onto develop is a **product-repo write** — precisely the worker action the Coordinator must not take. The rebase would also have to be committed to the baseharbor checkout, which is a product repo, not the planning repo.

Both blockers independently forbid executing the rebase. This is an Owner decision, not a silent skip.

## Facts I verified (so the Owner is not working blind)
- PR #1500 head: `git ls-remote origin refs/pull/1500/head` -> `f5883e1e9897869686d9879675489bc1496c3156` ✓ (matches mission)
- Branch `0427-165-target-delete-orphanrec` exists at `f5883e1e9` ✓ (matches mission)
- develop: `8a2912c62869cc89adc35bd6680b18724c5eac8d`; contains card-181 fix `d9bf3d94e` ✓ (card 181 GELANDET / develop 8a2912c62 enthaelt d9bf3d94e)
- Branch base (merge-base) = `fea92f37` (Merge PR #1507 0427-176). f5883e1e9 is NOT an ancestor of develop (linear rebase would be needed).
- Four NEW develop commits since branch base: `d9bf3d94e` (#1516 TestUpNameResumesThroughCommandEntrypoint isolation), `13fca4f9` (#1515 lifecycle flock validity probe), `230221700` (#1499 detect damaged deployment before generic budget check — possible cmd/baha error-classification touch), `8a2912c62` (#1511 owner-failure classification).

## No action taken
- No branch cut, no rebase, no commit, no push, no CI run, no `.github/**` change, no subagent (per AGENTS 4.8 and mission).
- Existing fresh lane `089b8a60` (session `0427-165-refresh`, `busy`) left untouched — per AGENTS 3.6 a second lane / replacement is not allowed while it is still active.
- A QUESTION line was posted to the coordinator session `594fd2f5-4e80-43b6-9841-92879146a85e` asking the Owner to either (a) authorize the Coordinator to run this specific worker task via an explicit Owner release, or (b) confirm the Coordinator abandons this stale rebase lane and reports card 165 as superseded on the board.

## END_BLOCKED 0427-165-refresh: cannot execute the rebase — card 0427-165 is superseded (contract `superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak`) AND session 594fd2f5 is the Coordinator whose rules forbid worker/product-code work. Verified: PR#1500 head f5883e1e9, branch 0427-165-target-delete-orphanrec at f5883e1e9, develop 8a2912c62 contains card-181 fix d9bf3d94e, 4 new develop commits since base fea92f37 (d9bf3d94e,13fca4f9,230221700,8a2912c62). No branch cut / commit / push / CI / subagent taken; existing lane 089b8a60 left idle; QUESTION posted to coordinator. Awaiting Owner decision (abandon+superseded vs explicit Owner release authorizing the Coordinator).
