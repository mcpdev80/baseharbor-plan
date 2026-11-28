# 0428-352 follow-up review r3 — w255

Date: 2026-11-27
Role: read-only review of commit `f9b2b7774` and its diff against `98fa2927f`.

## Verdict

CHANGES REQUIRED. The pending exact-id lookup now precedes live-agent selection, the replay-fixture teardown is scoped to its own files, and the exit check remains fail-closed. The lineage fallback is still not anchored when the coordinator id is unknown, and the new lineage test does not exercise that branch. The live-agent retry test also supplies an agent fixture but does not establish that `select_agent()` would find it, because the new pending-first path skips agent discovery entirely.

## Requested checks

1. Pending exact-id lookup before live-agent remapping — PASS.

   `scripts/release-lane.py` loads the pending ledger at lines 214-229, then selects the durable-id path at lines 231-240 before calling `agents()`/`select_agent()` at lines 241 onward. An existing pending entry with an `opencode_id` therefore takes precedence over a live-agent directory remap.

2. Unique OpenCode id before PARTIAL persistence — PARTIAL.

   The initial mapping-failure handler now calls `_resolve_by_reference()` and only persists the returned id (`release-lane.py:305-328`); it no longer repeats the ambiguous `open_sessions()` directory lookup. Registry multiplicity is rejected, and lineage/DB multiplicity is rejected when those lookups are anchored to a known coordinator/parent. However, if there is no matching registry entry, `coord` remains `None`. The lineage predicate at lines 117-123 compares `parentSessionId` with `str(coord or "")`, so an agent with no parent id and the same directory can be treated as a match; one such row is returned as if its identity were proven. That is not a validated exact id under the shared-directory scenario.

   Recipe: do not use lineage unless a nonempty coordinator id was established from a trusted source. When the identity is absent, skip lineage and use only a unique, explicitly parent-anchored DB row or return unresolved/PARTIAL. Add a test for one and multiple children with missing `parentSessionId`; neither should be selected as the target.

3. Live-agent end-to-end retry regression — PARTIAL.

   `test_durable_exact_id_live_agent_uses_stored_not_lookup` seeds a pending exact id and supplies the Codeman agent fixture. It proves the pending id is used and the sibling survives, but `_run()` only installs `rl.agents = lambda: agent`; the new durable branch bypasses `agents()` and `select_agent()`, and the test does not assert that the target agent is actually selectable. It also seeds the pending record rather than producing it through a first PARTIAL attempt.

   The core live-agent bypass behavior is implemented correctly by the early durable branch. To satisfy the stated end-to-end proof, assert the fixture is selectable with the production selector (or instrument selection), and preferably create the pending exact id through the real first-PARTIAL path before retrying with that agent still live.

4. Lineage multiplicity fails closed — FAIL as tested; PARTIAL in implementation.

   The implementation counts multiple lineage matches and raises when `coord` is known (`release-lane.py:112-127`). But `test_ambiguous_lineage_fails_closed` uses an empty registry (`tests/test_0428_352_session_retention.py:174-201`), so `coord` remains `None`. Its two agents have `parentSessionId="coord"`, which does not match the empty parent identity. The lookup proceeds to the DB path, where the fixture has two rows and fails there. The test's non-release assertion therefore does not demonstrate the lineage branch. More importantly, absent parent ids do match an empty `coord`, as noted in item 2.

   Recipe: establish the coordinator identity in a fixture that permits the lineage branch without an earlier registry return, exercise two matching live children and assert the explicit lineage ambiguity error; separately assert empty/unknown parent identity returns unresolved and never selects a lone child.

5. Fixture race and cleanup — PASS.

   The teardown now removes only its own UUID state file and matching lock file, restores `CODEMAN_WATCH_STATE` and `sys.argv`, and removes its temp directory (`tests/test_0428_352_session_retention.py:366-398`). The prior broad glob that could delete another test invocation's fixture is gone.

6. Reservation release after exact exit — PASS for covered behavior.

   The shared destructive path verifies the exact DB id and, after delete, checks that the row is absent before clearing the pending entry and releasing the reservation (`release-lane.py:357-378` in this commit). The success regression asserts target removal, sibling retention, and reservation release; the negative regression keeps the row present and asserts reservation retention.

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 32 tests in 1.831s` and `OK`. Existing ResourceWarnings from `card-status.py` were printed. The passing suite does not resolve the lineage finding because the purported lineage-multiplicity test reaches the DB fallback instead.

## Recommendation

Keep the candidate in CHANGES. Guard lineage resolution on a known coordinator identity, make the regression prove it actually exercises that branch, and strengthen the live-agent test so agent selectability and the first-PARTIAL-to-retry sequence are evidenced. Then rerun the suite.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r3 review requires changes; reviewed commit f9b2b7774.
