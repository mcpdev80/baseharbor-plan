# 0428-352 follow-up review r4 — w255

Date: 2026-11-27
Role: read-only review of commit `1d179ec72` against `f9b2b7774` and the Verdict 3 recipe.

## Verdict

CHANGES REQUIRED, limited to the lineage branch proof. Pending-first retry and the live-agent PARTIAL-to-retry regression now meet the requested behavior. But the claimed lineage regression still does not exercise the lineage branch, and the current resolver structure makes that branch unreachable with a known coordinator identity.

## Review points

1. Lineage anchored to a known coordinator identity — IMPLEMENTED, but the lineage branch is unreachable.

   `scripts/release-lane.py:108-129` now gates lineage lookup on a nonempty `coord`, preventing absent parent ids from matching an empty identity. However, `coord` is assigned only inside the registry `if matches` block at lines 100-107, which immediately returns the registry OpenCode id. If there is no registry match, `coord` stays `None` and lineage is skipped. Therefore this branch cannot currently run with a known coordinator id; the branch is fail-closed by being dead code rather than by actually checking lineage multiplicity.

   Required recipe: source the coordinator id independently from the matching worker registration (for example, the trusted watcher coordinator field) before attempting the registry/lineage resolution, while preserving fail-closed behavior on ambiguous registrations. Then the lineage lookup can run with a nonempty, trusted coordinator id and count matches.

2. Branch witness for lineage regression — FAIL.

   The test named `test_ambiguous_lineage_fails_closed` at `tests/test_0428_352_session_retention.py:254-292` explicitly documents and asserts `"db" in obs`, not `"lineage"`. Its registry is empty, so `coord` remains `None`; the two fixture agents with `parentSessionId="coord"` do not match the guarded lineage branch. The test fails closed through the DB ambiguity branch. `_branch_observers` confirms the DB branch only and is not evidence that lineage multiplicity was checked.

   Required recipe: add a test whose observer asserts `"lineage"`, with a known coordinator identity and two same-directory children under that parent. Assert the explicit ambiguous-lineage failure and that neither target nor sibling is removed. Also cover a lone child with a missing parent id and prove it remains unresolved.

3. Live-agent test with selectability and PARTIAL-to-retry sequence — PASS.

   `test_durable_exact_id_live_agent_uses_stored_not_lookup` now calls the production `select_agent()` and asserts the Codeman fixture is selectable (`tests/test_0428_352_session_retention.py:295-297`). It performs a first release attempt with that live agent, persists `oc-target`, and receives PARTIAL because the fake delete leaves the DB row (`:327-348`). It then retries with the same live-agent fixture and pending reference; the pending-first branch skips remapping, the resolver spy remains at zero, only `oc-target` is removed, the sibling remains, and the reservation is released after exit (`:350-370`). This directly covers the previously missing live-agent retry behavior.

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 32 tests in 0.603s` and `OK`. Existing ResourceWarnings from `card-status.py` were emitted. The passing suite does not close the lineage finding because its branch witness reports DB, not lineage.

## Recommendation

Keep the candidate in CHANGES until the resolver has a reachable, trusted-parent lineage path and a test asserts that the lineage branch actually ran and rejected multiple matching children.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r4 review requires lineage fix; reviewed commit 1d179ec72.
