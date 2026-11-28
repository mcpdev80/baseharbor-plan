# 0428-352 follow-up review r2 — w255

Date: 2026-11-27
Role: read-only review of commit `98fa2927fcf7c8bfb0dc2730ac72fb09430e57f8` in the local coordinator repository.

## Verdict

CHANGES REQUIRED. The ambiguity guards and reservation exit checks are improved, but the exact-reference retry is not consulted when the Codeman agent is still selectable. The regression test forces the agent-absent route, so it does not verify the requested live-agent case.

## Findings against the requested criteria

1. Exact reference before retry with a live agent — FAIL.

   `scripts/release-lane.py:232-252` consults a pending entry only in the `except LookupError` branch, which means `select_agent()` did not find the Codeman agent. If the agent is still present, execution follows the `else` branch at lines 254-258 and calls `open_sessions()` again using its working directory. It does not prefer the durable `opencode_id` already stored under that Codeman id.

   The test `test_durable_exact_id_removed_only_target_on_retry` at `tests/test_0428_352_session_retention.py:193-232` seeds the pending exact id, then explicitly replaces `select_agent` with a function that raises `LookupError` at line 230. It therefore verifies only the agent-absent route, contrary to the live-agent requirement.

   There is a related first-PARTIAL issue: after the initial `open_sessions()` raises, the live-agent handler calls the same `open_sessions()` again at lines 280-284 and persists only if this second lookup succeeds. If the original failure was the actual ambiguous shared-directory lookup, the repeated lookup remains ambiguous and no durable exact id is stored. The code comment that the live agent's directory is unique is not supported by the mission premise (shared `.models/<channel>` directory).

   Recipe: check the pending ledger by exact Codeman id before choosing the live-agent path, and resume from a validated stored OpenCode id while that agent remains live. For the first PARTIAL, obtain the exact id from an identity-bearing source (per-lane unique directory or exact persisted session id/registration); do not repeat an ambiguous directory lookup and call it exact. Add a test that persists a PARTIAL through the real code, retries while `agents()` still returns the Codeman agent, and asserts the resolver is not re-run and only the stored target is deleted.

2. Fail-closed multiple matches in registry, lineage, and DB — PARTIAL PASS.

   Registry matches now count and raise on more than one at `release-lane.py:97-110`; lineage matches count and raise at lines 112-127; DB rows count and raise at lines 128-145. The new tests exercise ambiguous registry (`test_ambiguous_registry_fails_closed`) and DB (`test_ambiguous_db_parent_fails_closed`) paths with same-directory fixtures and assert neither target nor sibling is removed.

   I do not find a dedicated lineage-multiplicity test in this commit. Also, `coord` is populated only by a unique registry hit; when there is no such hit it remains `None`, and the lineage predicate can then match entries whose `parentSessionId` is empty. Add a lineage fixture with two qualifying children and assert fail-closed, and ensure lineage matching is anchored to a known coordinator identity rather than treating absent parent ids as a common parent.

3. Real-code two-session / one-directory regression — PARTIAL PASS.

   The test fixture seeds `oc-target` and `oc-sibling` under the same directory (`tests/test_0428_352_session_retention.py:78-97`). The ambiguous registry and DB tests exercise production `open_sessions()` / `_resolve_by_reference()` without stubbing `open_sessions()`. The durable retry test does not stub `open_sessions()`, but seeds the pending record directly and forces `select_agent()` to fail. Consequently the suite does not test the complete real-code first-PARTIAL-to-retry flow, nor the same retry with the agent live.

4. Reservation only after exact session exit — PASS for the tested deletion path.

   The release path verifies the exact OpenCode DB id and checks it is absent after the delete command before clearing pending state and releasing the pool (`release-lane.py:319-340` in this commit). `test_reservation_released_only_after_exact_exit` asserts the reservation remains when the row remains; the successful retry test asserts the reservation is gone after target deletion and the sibling remains. This supports the ordering claim for the tested fake subprocess path.

5. Test hygiene — CHANGES.

   `ReplaySuppressionAfterDelete` creates a UUID-named watcher-state file under `scripts/`, but its teardown globs and removes every `.w352-fake-watcher-state-*.json` file (`tests/test_0428_352_session_retention.py:288-300`). A concurrent test invocation can therefore delete another invocation's fixture. The test also sets `CODEMAN_WATCH_STATE` at lines 325 and 340 without restoring the prior environment value. Watcher writes create sibling `.lock` files, and teardown does not remove its own lock file. Use a unique temporary directory on the same filesystem, or at minimum remove only the test's own state and lock paths; restore environment and argv in `finally`/teardown.

## Verification

Ran the explicitly requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 30 tests in 0.897s` and `OK`. The run emitted expected PARTIAL/ack fixture output and ResourceWarnings from existing `card-status.py` tests. Passing this suite does not close finding 1 because the live-agent retry route is not exercised.

## Recommendation

Keep the candidate in CHANGES. Make pending exact-id lookup precede live-agent remapping, establish the id from an unambiguous identity source before persisting PARTIAL, and add the live-agent end-to-end fake regression. Add the lineage-multiplicity test, close the watcher fixture cleanup race, then rerun the suite.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r2 review requires changes; reviewed commit 98fa2927fcf7c8bfb0dc2730ac72fb09430e57f8.
