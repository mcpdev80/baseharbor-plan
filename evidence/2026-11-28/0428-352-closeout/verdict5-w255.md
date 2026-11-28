# 0428-352 follow-up review r5 — w255

Date: 2026-11-27
Role: read-only review of commit `3d24488fecfe4095441ed6fe26eae90c49679a6a` against `1d179ec72` and Verdict 4.

## Verdict

CHANGES REQUIRED, limited to the lone-child regression. The resolver now reads the watcher coordinator identity before registry lookup, making lineage reachable and anchored; the ambiguous-lineage test proves that branch ran and failed closed. The lone-child test does not reach the resolver because its requested target id differs from the agent fixture id.

## Review points

1. Trusted coordinator id before registry/lineage — PASS with source assumption stated.

   `scripts/release-lane.py:97-119` reads `watcher.coordinator` from the watcher-state file before examining worker registrations. A unique registration may then supply the coordinator id only as fallback. This makes lineage resolution possible when there is no matching worker registration while preventing absent `parentSessionId` from matching an empty identity. The implementation relies on the watcher-state coordinator field being the trusted local authority described in the code comments.

2. Reachable lineage branch — PASS.

   With an empty registration list and a nonempty `watcher.coordinator`, `_resolve_by_reference()` reaches the guarded lineage branch at lines 140-152. It counts matches and raises on multiplicity instead of choosing the first child.

3. Lineage branch witness and ambiguous fail-closed regression — PASS.

   `test_ambiguous_lineage_fails_closed` now seeds `watcher.coordinator="coord"`, leaves the registry empty, provides two children with that parent and the same directory, and asserts `"lineage"` in the observer. It also verifies both OpenCode rows remain. This addresses the prior test that only witnessed the DB branch.

4. Lone child with absent parent remains unresolved — FAIL (test does not exercise the claim).

   `test_lone_child_missing_parent_stays_unresolved` calls `_run(rl, "cm-lone", ..., env.agent(), env)` at `tests/test_0428_352_session_retention.py:326`. But `env.agent()` returns only the Codeman agent with id `cm-18352` (see `FakeEcosystem.agent()` at lines 116-120). The target is therefore not selectable; `main()` exits through the “no exact lane found” path before calling `open_sessions()` or `_resolve_by_reference()`. The test's nonzero result and preserved DB row do not prove that a lone lineage child with no parent id is rejected by the resolver.

   Recipe: make the target agent fixture selectable (or call the real resolver directly while retaining a release-path assertion). Assert the branch observer excludes `lineage`, assert the resolver returns unresolved/raises as intended, and verify the target and sibling state remain unchanged. Avoid relying on a selector miss as the expected fail-closed outcome.

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 33 tests in 1.805s` and `OK`. Existing `card-status.py` ResourceWarnings were emitted. The suite pass does not validate the lone-child case because that test exits before reference resolution.

## Recommendation

Keep the candidate in CHANGES until the lone-child test reaches the resolver with a selectable target and proves that the absent-parent lineage entry is not selected.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r5 review requires lone-child regression correction; reviewed commit 3d24488fecfe4095441ed6fe26eae90c49679a6a.
