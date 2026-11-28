# 0428-352 follow-up review r9 — w255

Date: 2026-11-28
Role: read-only review of commit `61b692302` against `f08ff8546` and Verdict 8.

## Verdict

PASS. The lone-child test now states and asserts the observer contract, reaches the unresolved resolver path after the status gate, and compares the complete post-setup DB row set with the post-run set. The prior coordinator anchoring, reachable ambiguous-lineage guard, and live-agent retry evidence remain intact.

## Review

1. Observer contract — PASS.

   The code now emits `lineage_match` only after a child actually matches the trusted coordinator and directory (`scripts/release-lane.py`, lineage resolver). The lone-child test documents the distinction between branch entry and a successful match, asserts `lineage` is present and `lineage_match` absent, and thus proves the resolver visited lineage but did not select the child (`tests/test_0428_352_session_retention.py`, `test_lone_child_missing_parent_stays_unresolved`).

2. Complete row-set snapshot — PASS.

   After fixture setup, the test snapshots all `(id,title,parent_id,directory)` rows and asserts the only remaining setup row is the sibling under `other-coord`. After the unresolved release attempt, it snapshots the complete row set again and asserts exact equality. This proves fixture rows are unchanged, not merely that one sibling remains.

3. Resolver outcome and status-gate separation — PASS.

   The lone fixture is selectable and has `status="idle"`; it is passed through `_run()`. The exact run output contains `PARTIAL: exact OpenCode id unresolvable (no identity-bearing source)`, and the test expects return code 10. This distinguishes the resolver's unresolved result from the earlier selector-miss and missing-status HOLDs. The DB fixture has no row under the trusted coordinator in the target directory, so it cannot accidentally resolve a different session.

4. Prior requirements — PASS, unchanged from the preceding review.

   The watcher state's coordinator identity is loaded before registry matching. The ambiguous-lineage test proves a reachable lineage branch and fail-closed behavior. The live-agent test still covers a selectable agent, first PARTIAL, pending exact-id retry while the agent remains live, target-only deletion, sibling preservation, and reservation release only after exit.

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 33 tests in 0.608s` and `OK`. Existing `card-status.py` ResourceWarnings were emitted. The lone-child output showed the resolver-generated unresolved PARTIAL.

END_DONE w255-0428-251-demo170codex: 0428-352 r9 review PASS on 61b692302; full suite 33 tests OK.
