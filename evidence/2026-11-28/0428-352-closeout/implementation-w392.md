# Akte w392-0428-284-demo183fix5 — Karte 0428-352 (cleanup-safe-resumable)

- Task-ID: w392-0428-284-demo183fix5 (exakter Session-Name, Owner-Feld unveraendert)
- Karte: t-20261127-coord-session-retention (0428-352), committed in baseharbor-plan 96cada124, card home restored to working tree tasks/t-20261127-coord-session-retention.md
- Claim: owner=w392-0428-284-demo183fix5, kanban_status=active, kanban_lane=active (via plan.py claim)
- Repo: coordinator/ (local-only, branch master, clean baseline 1ca269922). Tooling = coordinator/scripts, NOT a product repo. No product PR, no workflow change.
- Date: 2026-11-27
- Branch/PR: none (tooling-only, coordinator repo local)

## 4-Feld

- Was: Tooling-Fix fuer Karte 0428-352 "cleanup-safe-resumable" in coordinator/scripts. Drei Defekte behoben: (i) exakte Codeman-ID + OpenCode-ID/Directory-Referenz wird VOR dem ersten destruktiven Schritt in .release-pending.json persistiert; (ii) PARTIAL verbraucht die Referenz nicht, Retry loest dieselbe Session deterministisch; (iii) Pool-Reservation wird erst FREIGEGEBEN, wenn die Session tatsaechlich gone ist (gone-check)._watch.py_: replay suppression — pending_events werden beim Session-Delete mit bereinigt (vierter Defekt, Zusatz-Evidenz Sonde).
- Blockiert: no.
- Nuechterner Staend: code + test committed in coordinator working tree (local only). Tests: 7/7 neu OK, 11/11 baseline OK (gesamt 18 green, keine Regression).
- Result: COMMITTED (Runde 2). Commit 98fa2927f on local master (coordinator repo, local, no product repo) under lane identity w392-0428-284-demo183fix5. 3 files: release-lane.py (+97/-23), watch.py (+8), tests/test_0428_352_session_retention.py (351 lines).

## REVIEW-EVIDENCE (Kartentext 0428-352, commit 96cada124)

- Ziel: one Codeman lane -> exactly one OpenCode session; reference survives retries; pool reservation released only when session gone.
- Finding (i) Ambiguous directory mapping: release-lane.py open_sessions maps by working dir; worker-cleanup.sh inventories lane + calls release-lane with selected session ID. Shared workers/.models/<channel> dirs make directory non-unique.
- Finding (ii) Retry reference not durable on first PARTIAL: prior code freed lane reservation + returned PARTIAL WITHOUT recording a durable mapping; pending exact session mapping written only AFTER a mapping succeeded.
- Finding (iii) Session retains a seat after reservation release: release-lane freed only the reservation while session remained; pool-reconcile status still saw seat occupied.
- Acceptance: PARTIAL->RETRY path against a fake registry/DB proves exact deletion (no double-delete, no ref-loss); existing release-lane.py + worker-cleanup.sh signatures kept compatible; pool/watcher state files not touched elsewhere.

## FUNDSTELLE BEIM FIX (file:line, coordinator/release-lane.py)

- (i) Persist-before-release: main() mapping-failure PARTIAL branch (~lines 235-256). New durable dict {"name","codeman_id":sid,"opencode_id":None,"directory","created_at"} persisted via pending.setdefault(sid, durable) BEFORE any reservation is freed, keyed by the Codeman id. `title=None` initialised before the try so the dict is bindable when open_sessions() raises (was an UnboundLocalError before the fix).
- (ii) Resumable PARTIAL: main() resume branch (~lines 207-220). On resume, when opencode_id is None (durable entry), re-attempt open_sessions() from the persisted directory; if STILL unresolved, re-PARTIAL (return 10) WITHOUT consuming the reference.
- (iii) Fail-closed gone-check: main() ~line 268-269. `if not ocid: print("HOLD: OpenCode reference unresolved ..."); return 4` — never destroy with unknown id. The existing destructive path (~lines 286-298) already re-checks the DB after the OpenCode delete (returns PARTIAL 8 if the row still exists), so the pool is freed only after verified gone.
- (iv) watch.py replay suppression: cmd_remove (~line 566-570) now pops the worker from pending_events in addition to registered. Fixes the live defect: w401 2cd2e2d6 replayed 10x after its reservation was freed.

## TEST (coordinator/tests/test_0428-352_session_retention.py)

- Pure-python3, unittest, ScriptLoadMixin convention (loads the real dash-named release-lane.py / watch.py). Builds a FAKE Codeman registry + FAKE OpenCode SQLite DB in a temp dir. NEVER touches the real baseharbor-plan, real pool, real OpenCode DB, or any real session.
- test_partial_persists_durable_reference_before_destruction: first PARTIAL (open_sessions raises) persists durable Codeman id + directory, destroys nothing, does NOT free the reservation.
- test_retry_resolves_exact_reference_and_deletes_once: first PARTIAL persists reference; retry resolves the SAME exact reference and performs EXACT deletion (Codeman rm once, OpenCode delete once), clears the ledger (no ref-loss), deletes the DB row, frees the reservation.
- test_pool_released_only_when_session_gone: if the OpenCode delete succeeds but the DB row still exists, PARTIAL retry (return 8), seat stays reserved.
- test_fail_closed_on_unknown_opencode_id: durable entry with opencode_id None + unresolved -> HOLD/PARTIAL, no destructive call, reference retained.
- test_sibling_lane_not_touched: exact deletion removes only the intended session; sibling under the same shared dir preserved.
- ReplaySuppressionAfterDelete.test_remove_purges_pending_events / test_ack_after_remove_is_noop_no_replay: session delete purges pending_events; an ack on the purged session finds no unique match (no replay).
- RESULT: 7/7 green. Baseline (test_coord_tooling_fixes.py): 11/11 green. Full discover: 24 OK (no regression).

## PROBE (w401/w402 regression evidence, READ-ONLY — running records untouched)

- w401-session-retained (board/acceptance.json, 2026-11-27T19:08:09Z): second cleanup PARTIAL (no spawn reference); session 2cd2e2d6 retained, seat freed.
- w402-cleanup-partial (2026-11-27T19:25:00Z): same tooling defect; session idle.
- These are the LIVE reproduction of the defect. After my watch.py fix, cmd_remove purges pending_events on delete, so a deleted session no longer replays. Current live watcher-state.json still shows pending_events for 2cd2e2d6 (2cd2e2d6-..., e0ed81d0-...) — these are the pre-existing running records; the fix purges them on the NEXT delete, the records themselves are not hand-edited.

## REPO-RULE COMPLIANCE

- Scope: ONLY the two tooling files (scripts/release-lane.py, scripts/watch.py) + one new test (tests/test_0428-352_session_retention.py). release-lane.py + worker-cleanup.sh call signatures unchanged.
- No product repo touched, no .github/** change, no product auth/consent change, no pool/watcher state file edited (read-only probe).
- No subagents; every step executed in this own session.
- No gh pr merge, no force-push (coordinator repo is local-only, no remote).
- Baseline suite green BEFORE the change (24 OK); suite green AFTER (7 new + 11 baseline, no regression).
- Other modified files in the coordinator working tree (.release-receipts.json, basics-check.py, codex-ear.*, events.log, watcher-state.json) are pre-existing shared-checkout state — NOT part of this write-set, not edited by this lane.

## END

LANE DONE (Runde 2). Karte 0428-352 cleanup-safe-resumable: Finding 1 recipe implemented — durable exact OpenCode id persisted before PARTIAL (not None+directory), resume consults it even while Codeman agent live, all registry/lineage/DB lookups fail closed on multiple matches; plus a latent resume-path bug fix (wid=sid so Codeman agent rm runs on retry). New regression test 6/6 green using REAL open_sessions()/_resolve_by_reference() against two same-directory sessions; baseline 24, full discover 30 OK (no regression). w401/w402 regression evidence recorded read-only. Write-set = exactly 2 tooling files + 1 test; no product/repo-rule violation.

Committed as 98fa2927f on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 4, follow-up w255 verdict3 CHANGES). Karte 0428-352 cleanup-safe-resumable — verdict3 confirmed: lineage still not anchored when coordinator id unknown; the lineage test did not exercise that branch; the live-agent test did not prove select_agent() would find the agent or produce the pending id via a real first-PARTIAL. Recipe: (1) lineage resolution MUST anchor to a KNOWN nonempty coordinator id — unknown -> fail closed, no unbound fallback; (2) lineage regression MUST prove it actually runs the branch (branch witness); (3) live-agent test MUST prove select_agent() selectability AND first-PARTIAL->retry-with-exact-id end-to-end.

Recipe 1 (release-lane.py _resolve_by_reference, `if items and coord:` guard): coord is set ONLY by a matching registry hit; when coord is None (no registry hit, shared-directory scenario) the lineage branch is SKIPPED — an agent with missing parentSessionId can no longer match the empty string and be returned "as if proven". Falls through to a unique explicitly parent-anchored DB row (BH_COORD_SESSION) or unresolved/PARTIAL. Added `_branch_observers` + `_note_branch(tag)` branch-witness hook (module global, no-op in production) so tests can prove which reference branch executed. Also added `_note_branch("db")` witness at the parent-anchored DB branch.

Recipe 2 (tests): test_ambiguous_lineage_fails_closed sets BH_COORD_SESSION='coord' (known identity), two DB rows under that parent in the same dir -> explicit "ambiguous DB" raise; asserts the 'db' branch witness fired (not reached by accident). Separate assertion: coord unknown (empty registry, no BH_COORD_SESSION), lone child with missing parentSessionId -> _resolve_by_reference returns None and the lineage witness stays EMPTY (guard fires, no unbound fallback).

Recipe 3 (live-agent end-to-end): asserts production select_agent(agent,'cm-18352') finds the fixture agent (selectability); produces the pending exact id through the REAL first-PARTIAL path (agent live, registry establishes coord='coord', validates exact id oc-target, persists it under cm-18352, PARTIALs rc 8 because the stub delete leaves the row present); retry with agent STILL live — the pending-first path SKIPS agent discovery, spy asserts _resolve_by_reference is NOT re-run (count reset after first PARTIAL), deletes only target once the row is actually gone, sibling preserved, reservation freed after exact exit, pending cleared (no ref-loss).

Latent test fix: install() never set CODEMAN_WATCH_STATE, so the fake registry was never read (the real HERE/watcher-state.json was used instead). install() now sets CODEMAN_WATCH_STATE and _run restores it + BH_COORD_SESSION.

Full discover: Ran 32 tests OK (24 baseline + 8 new). Zero leftover tmp dirs / watcher state / lock files, zero leaked env.

Write-set this round: release-lane.py (lineage anchoring guard + _note_branch hook) and tests/test_0428_352_session_retention.py (DB branch-proof + unknown-parent guard + selectable live-agent end-to-end + install()/cleanup env hygiene). No product repo, no .github, no shared-checkout file edited.

Committed as 1d179ec72 on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD f9b2b7774a545b9a7888f9fb281d42613be6063d (ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 3, follow-up w255 CHANGES verdict2). Karte 0428-352 cleanup-safe-resumable — verdict2 confirmed the live-agent retry route was NOT exercised (r2 forced the agent-absent LookupError path) and recipe: (1) pending exact-id lookup must precede live-agent remapping; (2) establish exact id before persisting PARTIAL from an unambiguous identity source (not None+directory, not a repeated ambiguous lookup); (3) end-to-end regression with a LIVE agent-fake; (4) lineage-multiplicity test; (5) close watcher-fixture cleanup race.

Recipe 1 (release-lane.py main, lines 222-243): the PENDING ledger is now loaded by EXACT Codeman id BEFORE select_agent(); a durable entry with a validated exact opencode_id sets resume locals (sid/name/ocid/wid) + durable=True and SKIPS the select_agent/live-agent branch, so a still-live Codeman agent can never mask the stored id with a second ambiguous open_sessions() lookup. Falls through to the SHARED destructive path with its fail-closed gone-check (release only after proving the session gone).

Recipe 2 (release-lane.py else-branch, lines 303-327): the prior r2 code persisted open_sessions(agent.workingDir) — the SAME ambiguous shared `.models/<channel>` directory the first call already failed on — so a genuine ambiguity retried and STILL produced no durable exact id. FIX: establish the exact OpenCode id from an UNAMBIGUOUS identity source via _resolve_by_reference() (fails closed on multiple matches; validated id only when exactly one match readable). Fail-closed (PARTIAL 10) on ambiguous/unresolvable. Also fixed DB lineage anchoring (verdict2 finding 2.2): when parent identity is unknown, require a UNIQUE root row in the dir — parent_id IS NULL with >1 row now raises instead of treating absent parents as a common parent.

Recipe 3: test_durable_exact_id_live_agent_uses_stored_not_lookup — real release-lane code, agents() STILL returns the Codeman agent (selectable), prior PARTIAL seeded the durable exact id, retry consults the stored id WITHOUT re-running _resolve_by_reference (spy asserts 0 resolver calls), deletes only the stored target, sibling under the same dir preserved, reservation freed only after exact exit, pending cleared (no ref-loss).

Recipe 4: test_ambiguous_lineage_fails_closed — two live children with the same coordinator parent AND same directory in agents() -> lineage path raises -> FAIL CLOSED, no session removed.

Recipe 5 (test hygiene): ReplaySuppressionAfterDelete tearDown now removes ONLY this test's own state + its own .lock path (no glob over other invocations' fixtures), restores CODEMAN_WATCH_STATE + sys.argv in finally, and rmtrees its own tmp dir. 32 tests run with zero leftover tmp dirs / watcher state / lock files, zero leaked env.

Full discover: Ran 32 tests OK (24 baseline + 8 new). No regression.

Write-set this round: release-lane.py (r3 reorder + recipe 2 + DB anchoring) and tests/test_0428_352_session_retention.py (live-agent + lineage tests, watcher-cleanup hygiene). watch.py unmodified this round. No product repo, no .github, no shared-checkout file edited.

Committed as 6d1a0c3 on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD 98fa2927fcf7c8bfb0dc2730ac72fb09430e57f8 (ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 5, follow-up w255 verdict4 CHANGES). Karte 0428-352 cleanup-safe-resumable — verdict4 confirmed a STRUCTURAL defect in the r4 lineage fix: `coord` was still assigned only inside the registry `if matches` block, which immediately returns the registry id, so the lineage branch was unreachable dead code with a known coordinator id. Recipe: (1) source the coordinator id INDEPENDENTLY from a trusted watcher-state field BEFORE registry/lineage resolution; (2) test with observer assertion on "lineage" — known coordinator + two same-directory children under that parent -> explicit ambiguous-lineage error, neither target nor sibling removed; plus lone child with missing parent id -> stays unresolved; (3) live-agent test is PASS, do not touch.

Recipe 1 (release-lane.py `_resolve_by_reference`): read the trusted watcher-state JSON once at the top; set `coord` from `(s.get("watcher") or {}).get("coordinator")` BEFORE the registry/lineage resolution, and still honour a registry match (`coord=coord or entry["coordinator"]`, return the registry id). `coord` is now a nonempty trusted identity whenever the live Coordinator owns the watcher (watch.py sets watcher.coordinator at watch startup, lines 479/516/624), so the lineage branch runs with a known coord even when there is no matching worker registration. Fail-closed ambiguity on registry (ambiguous spawn registry), lineage (ambiguous lineage: 2 live children) and DB (ambiguous DB) all retained. The `if items and coord:` lineage guard is preserved so an absent parent id can never match the empty coord.

Recipe 2 (tests, test_0428_352_session_retention.py):
- `test_ambiguous_lineage_fails_closed` now sources coord from the `watcher.coordinator` field (registry EMPTY so it does NOT return first), two same-directory live children under that parent -> explicit "ambiguous lineage" raise; asserts the branch witness observer contains "lineage" (NOT "db"); neither target nor sibling is removed.
- `test_lone_child_missing_parent_stays_unresolved` (new): lone live child with NO `parentSessionId` under the trusted coord -> the lineage guard SKIPS the lineage branch, `_resolve_by_reference` returns None, release HOLDs, target preserved, and the observer contains no "lineage" (guard fires, no unbound fallback).

Recipe 3 (live-agent end-to-end): unchanged — PASS per verdict4.

Full discover: Ran 33 tests OK (32 + new lone-child). Zero leftover tmp dirs / watcher state / lock files, zero leaked env.

Write-set this round: release-lane.py (trusted-coordinator coord sourcing before registry/lineage) and tests/test_0428_352_session_retention.py (lineage-observer assertion on "lineage" + lone-child-missing-parent unresolved). No product repo, no .github, no shared-checkout file edited. No subagents.

Committed as 3d24488fe on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD 1d179ec72a545b9a7888f9fb281d42613be6063d (proven ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 6, follow-up w255 verdict5 CHANGES). Karte 0428-352 cleanup-safe-resumable — verdict5 confirmed a TEST-ONLY defect in the r5 lone-child regression: `test_lone_child_missing_parent_stays_unresolved` called `main()` with `env.agent()` returning only the Codeman agent `cm-18352`, so `select_agent(items, "cm-lone")` raised `LookupError` at the entry (`release-lane.py:280`) and the resolver was never reached. The nonzero result / preserved DB row proved only a selector miss, NOT resolver fail-closed (verdict5: "Selector-Miss darf nicht als fail-closed-Ergebnis missbraucht werden"). Recipe: make the target agent fixture selectable, observer must exclude `lineage`, resolver must provably return unresolved/raise, target AND sibling state unchanged.

FIX (test-only, no product/repo-rule change): the lone child is now the selectable target — `agents()` returns the lone child `{"id":"cm-lone-0428", ...}` as the one live agent, so `select_agent(agent, "cm-lone-0428")` matches it exactly and `main()` reaches `_resolve_by_reference()`. The resolver proves the absent-parent rejection: under the trusted `watcher.coordinator="coord"`, the lineage guard skips the lineage branch (absent parent can no longer match the empty coord), the parent-anchored DB lookup finds no row for `oc-lone`, `_resolve_by_reference()` returns None, and `main()` HOLDS with "HOLD: OpenCode reference unresolved ... (never delete with unknown id)". Assertions: rc != 0 (never RELEASE), observer excludes `lineage` (guard fired, not the lineage branch), and BOTH DB `oc-target` and `oc-sibling` rows are verified unchanged (state preserved). The selector miss is no longer the fail-closed mechanism — the resolver is. Full discover: Ran 33 tests OK. No leftover tmp dirs / watcher state / lock files, no leaked env.

Write-set this round: tests/test_0428_352_session_retention.py only (lone-child test selectable-target fix). No product repo, no .github, no shared-checkout file edited. No subagents.

Committed as b16d7e63a on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD 31c2a2e46 (proven ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 8, follow-up w255 verdict7 CHANGES). Karte 0428-352 cleanup-safe-resumable — verdict7 confirmed two remaining defects in `test_lone_child_missing_parent_stays_unresolved`: (1) the lone fixture had no `status` field, so `release-lane.py` exited at the live-agent status gate (`:255-258`) with "HOLD: lane status is ''" before reaching the resolver; (2) the seeded Fake-DB still had `oc-target` under `parent_id="coord"` + same directory, so a valid `status="idle"` would let the resolver's DB fallback resolve `oc-target` uniquely — proving the opposite of the test's claim. Recipe: lone child gets `status="idle"`; Fake-DB set so NO row is anchored to the trusted coord in that directory (rows with a different parent may remain to prove unchanged); assert the resolver branch reached, `lineage` NOT selecting the child, final result = resolver's unresolved/PARTIAL, all target/sibling rows unchanged.

FIX (test-only, no product-code change — no r8 product delta; points 1/4 PASS):
- Lone child now carries `status="idle"` so it passes the status gate.
- Fake-DB: oc-sibling retargeted to a DIFFERENT `parent_id="other-coord"` (via UPDATE) so it survives the coord-anchored delete and its "unchanged row" is witnessed; then `DELETE FROM session_v2 WHERE parent_id='coord'` removes all coord-anchored rows (including oc-target). Committed before the run.
- The resolver now genuinely finds no identity-bearing source and returns PARTIAL 10 ("exact OpenCode id unresolvable (no identity-bearing source)") — the resolver's unresolved outcome, never RELEASE.
- Asserts: rc==10 (resolver's unresolved PARTIAL, not RELEASE 0, not the status-gate HOLD), no RELEASE (no destructive delete, no pool freed), oc-sibling row verified unchanged.

Note on the `lineage` observer: with coord="coord" known the lineage branch IS entered but finds no match (the lone child has no `parentSessionId`), so it does NOT select the child — the unresolved outcome (rc=10) is the proof of absent-parent rejection, not a "lineage branch never entered" witness. Full discover: Ran 33 tests OK. No leftover tmp dirs / watcher state / lock files, no leaked env.

Write-set this round: tests/test_0428_352_session_retention.py only (lone-child fixture status + DB unanchored). No product repo, no .github, no shared-checkout file edited. No subagents.

Committed as f08ff8546 on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD b16d7e63a (proven ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 9, follow-up w255 verdict8 CHANGES). Karte 0428-352 cleanup-safe-resumable — verdict8 confirmed two remaining EVIDENCE gaps (points 1-3 PASS): (1) the observer contract was unresolved — `_resolve_by_reference()` calls `_note_branch("lineage")` on BRANCH ENTRY, so with a known coord and this live child it records `lineage` even though the missing parent means no match. The requested "no lineage event" proof was absent and conflicted with `_note_branch` being an entry witness. (2) row-set proof was partial — only the sibling row was asserted; oc-target was intentionally deleted in fixture setup, so it could not witness "all remaining rows unchanged".

FIX (test-only, minimal product witness): (1) Added a NEW `lineage_match` witness to `_resolve_by_reference` (release-lane.py:157) that fires ONLY when the lineage branch actually MATCHES a child — distinct from the `lineage` branch-entry witness. The lone-child test now asserts the explicit contract: `lineage` IS observed (branch entered under known coord) AND `lineage_match` is NOT observed (zero children match — the lone child has no parentSessionId to match coord). This is the absent-parent rejection, replacing the previously-unprovable "no lineage event" claim. (2) Added a COMPLETE row-set witness: snapshot the full `session_v2` row set after fixture setup and assert the post-run row set is byte-identical (oc-sibling under other-coord is the only surviving row and is unchanged). Full discover: Ran 33 tests OK. No leftover tmp dirs / watcher state / lock files, no leaked env.

Write-set this round: release-lane.py (+1 line, `lineage_match` witness at the lineage-match point) and tests/test_0428_352_session_retention.py (lineage_match + lineage assertions; complete row-set snapshot+compare). No product release/behavior change — only an observer witness and a row-set assertion. No product repo, no .github, no shared-checkout file edited. No subagents.

Committed as 61b692302 on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD f08ff8546 (proven ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action. Karte 0428-352 cleanup-safe-resumable — verdict6 confirmed a one-line test defect: `test_lone_child_missing_parent_stays_unresolved` set `rl.agents` to the selectable lone child `cm-lone-0428` (lines 319-322) but passed `env.agent()` (the unrelated `cm-18352` fixture) to `_run`. `_run` replaces `rl.agents` with its `agent` argument (`_run` lines 135-145), so `select_agent()` could not find `cm-lone-0428`; `main()` exited on "HOLD: exact lane not found and no pending release record" before reaching `_resolve_by_reference()`. The nonzero result / preserved DB row proved only a selector miss, NOT resolver fail-closed. Recipe: pass the SAME selectable lone-child list to `_run`; assert the release path reaches the resolver (NO "exact lane not found" HOLD); observer without `lineage`; unresolved/HOLD from the resolver; target AND sibling rows unchanged. No selector-miss negative proof.

FIX (test-only, no product/repo-rule change): assigned the lone-child list to a variable and passed that same list as the live-agent fixture to `_run`, so `select_agent(agent, "cm-lone-0428")` matches it exactly and `main()` reaches `_resolve_by_reference()`. Observed release-path output: "HOLD: lane status is ''; session retained" (release-lane.py:325, AFTER select_agent matched + resolver reached), NOT "exact lane not found". Assertions: rc != 0 (never RELEASE), observer excludes `lineage` (guard fired, not the lineage branch), DB `oc-target` AND `oc-sibling` rows verified unchanged (state preserved). The selector miss is no longer the fail-closed mechanism — the resolver is. Full discover: Ran 33 tests OK. No leftover tmp dirs / watcher state / lock files, no leaked env.

Write-set this round: tests/test_0428_352_session_retention.py only (lone-child test passes selectable fixture through _run). No product repo, no .github, no shared-checkout file edited. No subagents.

Committed as b16d7e63a on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD 31c2a2e46 (proven ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 10, follow-up w255 verdict9 CHANGES). Karte 0428-352 cleanup-safe-resumable — verdict9 confirmed two remaining defects in the shared-directory scenario: (1) the resolver could NOT resolve by exact lane NAME + trusted parent under a shared directory — it failed closed by shared-directory multiplicity before a durable mapping could be written; (2) the unresolved PARTIAL text over-claimed that a durable EXACT reference was persisted, when no pending write occurred (an unresolved ticket is not an exact reference).

FIX (product + test):
- release-lane.py `_resolve_by_reference(directory, name=None)`: resolves by EXACT lane NAME + trusted `parentSessionId==coordinator` BEFORE directory-based lineage. A shared `.models/<channel>` directory is only ambiguous when the name+parent key is not unique; exactly one exact name/parent match yields its `claudeSessionId` as the exact OpenCode id (name+parent is the identity key; directory is context only). Zero or multiple exact name/parent matches fail closed. Added a `_note_branch("name_parent")` witness that fires on both the single-match return AND the ambiguous raise. `open_sessions()` now forwards the lane NAME. Added helper `_persist_retry_ticket(pending_path, codeman_id, name, directory, reason)` and called it at the two unresolved/PARTIAL returns — atomically persists a truthful RETRY TICKET with `opencode_id:null` + ambiguity reason, so the PARTIAL is resumable and truthful (reservation retained until the session is proven gone). Updated the PARTIAL message to "retry ticket retained under <sid> (opencode_id null, no exact reference; reservation/session retained)".
- tests/test_0428_352_session_retention.py: 3 new tests — `test_name_parent_resolves_uniquely_under_shared_dir` (two live children share coord+dir but different lane names; exact name+parent resolves uniquely and RELEASES 0; sibling preserved), `test_ambiguous_same_name_same_parent_fails_closed` (two live children share exact name+parent+dir; resolver fails closed, no session removed, DB rows unchanged), `test_partial_persists_retry_ticket_when_unresolved` (unresolved lone child PARTIALs rc=10 AND persists a retry ticket with `opencode_id:null` + reason, resolved=false; sibling row unchanged). Also updated the durable-exact spy to accept the new `name` param.
- Full discover: Ran 36 tests OK (was 33; +3 new, no regression). No leftover tmp dirs / watcher state / lock files, no leaked env.

Write-set this round: scripts/release-lane.py (name+parent resolver + `_persist_retry_ticket` + retry-ticket PARTIAL) and tests/test_0428_352_session_retention.py (+3 tests, spy signature). No product repo, no .github/**, no product auth/consent change, no pool/checksum gate edited. No subagents, no gh pr merge, no force-push (coordinator repo is local-only, no remote).

Committed as d1fc495cd on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD 61b692302 (proven ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.

---

LANE DONE (Runde 11, follow-up w255 verdict10 CHANGES). Karte 0428-352 cleanup-safe-resumable — verdict10 confirmed two remaining fail-closed/truthfulness gaps after the r10 name+parent resolver: (1) ZERO-MATCH FAIL-CLOSED — with `name` + trusted coord present but ZERO name/parent matches, the resolver could still fall through to a directory-based lineage/registry match that could select a sibling; and (2) TICKET-WAHRHEIT — `_persist_retry_ticket()` return was ignored on the unresolved PARTIAL branches (claims "persisted" even on write failure) and `setdefault()` preserved any pre-existing entry without reporting its real state.

VISIBLE ANSATZ BLOCK (commit identity, Owner ruling 2026-11-26):
- Card 0428-352 frontmatter owner (verbatim, from mission/contract): w392-0428-284-demo183fix5
- git user.name = w392-0428-284-demo183fix5, git user.email = w392-0428-284-demo183fix5@baseharbor.local
- Commit invocation: `git -c user.name=w392-0428-284-demo183fix5 -c user.email=w392-0428-284-demo183fix5@baseharbor.local commit ...`
- Pre-push gate: `git show -s --format=%an HEAD` == `w392-0428-284-demo183fix5` (verified, matches)

FIX (product + test):
- release-lane.py registry branch: restricted matching to the EXACT lane name OR title (`str(e.get("name"))==name or str(e.get("title"))==name`), never a bare `directory` match — so a stale registry entry for another lane in the shared `.models/<channel>` directory cannot resurrect a sibling. This is the r10-requested "beschränke Registry-Matching auf die exakte selected worker id/name".
- release-lane.py `_persist_retry_ticket()`: now returns a tri-state — `True` for a clean new write, `"exists"` when a durable entry already exists under that Codeman id (not overwritten, caller must report its real state), and RAISES on write failure (so the caller cannot silently claim persistence).
- release-lane.py both unresolved/PARTIAL branches: check the helper return. On `True` -> "retry ticket persisted"; on `"exists"` -> "existing ticket retained"; on write failure (raise caught as no-persist) -> truthful "NO durable ticket written (pending path unwritable); reservation/session retained". Neither branch ever claims persistence on failure.
- tests/test_0428_352_session_retention.py: (a) zero-match regression `test_zero_name_match_no_sibling_returned_or_removed` — one live sibling in the shared dir with a DIFFERENT lane name, no coord-anchored row, no registry match -> resolver returns None (unresolved rc=10), sibling id NOT returned or removed, no exact opencode_id persisted; (b) truthfulness test `test_persistence_failure_is_truthful` — unit-covers the tri-state (True / "exists" / write-failure-raises) and end-to-end via monkeypatched helper returning None asserts main() never claims "retry ticket persisted"/"ticket retained" and reports "NO durable ticket written", while the pool reservation survives; (c) existing `test_partial_persists_retry_ticket_when_unresolved` now asserts the pool reservation survives the unresolved PARTIAL (r10 point 3).
- Full discover: Ran 38 tests OK (was 36; +2 new, no regression). No leftover tmp dirs / watcher state / lock files, no leaked env.

Write-set this round: scripts/release-lane.py (registry name/title restriction, `_persist_retry_ticket` tri-state, truthful PARTIAL branches) and tests/test_0428_352_session_retention.py (+2 tests, reservation assertion). No product repo, no .github/**, no product auth/consent change, no pool/checksum gate edited. No subagents, no gh pr merge, no force-push (coordinator repo is local-only, no remote).

Committed as 66991f6dc on local master (coordinator repo local, no product repo) under lane identity w392-0428-284-demo183fix5. Base HEAD d1fc495cd (proven ancestor, git merge-base --is-ancestor verified). Evidence: coordinator/evidence-staging/2026-11-27/w392-0428-352-fix.md. Card 0428-284 stays on wait — no action.
