# 0428-352 follow-up review r8 — w255

Date: 2026-11-27
Role: read-only review of commit `f08ff8546` against `b16d7e63a` and Verdict 7.

## Verdict

CHANGES REQUIRED for the requested test evidence. The status gate and DB fixture are corrected, and the test reaches the resolver's unresolved PARTIAL path. But it does not assert the requested no-lineage-observer condition or prove all fixture rows remained unchanged. The observer currently records branch entry, so it records `lineage` even when the child has no matching parent.

## Requested checks

1. Status gate — PASS.

   The lone child now has `status="idle"` (`tests/test_0428_352_session_retention.py:319-322`), satisfying the status guard before resolution.

2. DB fixture without a coordinator-anchored row — PASS.

   The fixture changes the sibling's parent to `other-coord` and deletes rows anchored to `coord` before running the case (`:323-329`). This leaves no DB row for the resolver's parent-anchored query while preserving an unrelated sibling row.

3. Resolver reached and unresolved/PARTIAL result — PASS.

   The test passes the selectable `lone` fixture to `_run()` and expects return code 10 (`:330-342`). The actual suite output included `PARTIAL: exact OpenCode id unresolvable (no identity-bearing source); durable reference retained under cm-lone-0428 for retry`, distinguishing this outcome from the earlier selector and status gates.

4. No `lineage` event — NOT PROVEN; observer semantics conflict with the requested assertion.

   The test creates `obs` and assigns it to `_branch_observers`, but has no assertion about `obs` in this case. `_resolve_by_reference()` calls `_note_branch("lineage")` on entering the lineage branch, before filtering children; therefore with a known coordinator and this live child the observer records `lineage` even though the missing parent means the child is not a lineage match. The code behavior is fail-closed, but the requested “no lineage event” proof is absent and the current event means “branch visited,” not “lineage match.”

   Recipe: either make the observer report successful lineage matches rather than branch entry and assert no match event, or state and assert the intended contract as “lineage branch visited, zero matching children, unresolved result.” Do not claim no `lineage` observer event while `_note_branch` is an entry witness.

5. Rows unchanged — PARTIAL.

   The test queries `oc-target` and `oc-sibling` after the run (`:343-347`) but only asserts that the sibling remains. The target row was intentionally deleted during fixture setup (`:326-329`), so it cannot witness that the resolver left all remaining fixture rows unchanged. Snapshot the row set after setup and compare the complete row set after the run (or explicitly assert target remains absent and sibling remains unchanged).

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 33 tests in 0.579s` and `OK`. Existing `card-status.py` ResourceWarnings were emitted. The suite pass does not establish the missing observer assertion or full row-set comparison.

## Recommendation

Keep the candidate in CHANGES until the observer contract is made explicit and asserted, and the lone-child test compares the complete post-setup row set with the post-run row set.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r8 review requires observer and row-set evidence; reviewed commit f08ff8546.
