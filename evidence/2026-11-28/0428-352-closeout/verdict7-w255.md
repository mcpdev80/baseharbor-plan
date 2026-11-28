# 0428-352 follow-up review r7 — w255

Date: 2026-11-27
Role: read-only review of commit `b16d7e63a` against `31c2a2e46` and Verdict 6.

## Verdict

CHANGES REQUIRED. The test now passes the lone-child fixture to `_run`, so the old selector-miss is gone. It still does not reach the resolver: the fixture lacks the required lane status and exits at the live-agent status gate. Even if status were set to idle, the fixture DB still contains one row under the trusted coordinator and same directory, so the DB fallback would resolve `oc-target` rather than demonstrate an unresolved lone child.

## Review

1. Selectable agent fixture passed to `_run` — PASS.

   `test_lone_child_missing_parent_stays_unresolved` now passes its `lone` list to `_run()` at `tests/test_0428_352_session_retention.py:329`; `_run()` uses that argument for `rl.agents`. The prior mismatch between the requested target id and `env.agent()` is fixed.

2. Resolver reached and HOLD comes from resolver — FAIL.

   The lone fixture at `tests/test_0428_352_session_retention.py:319-322` has id `cm-lone-0428` but no `status` field. `release-lane.py` checks status before calling `open_sessions()` (`:255-258`). The test run emitted `HOLD: lane status is ''; session retained`, so it exits before the resolver. The asserted nonzero result is still not evidence for the missing-parent resolution behavior.

3. Fixture DB also prevents the claimed unresolved outcome — FAIL.

   `FakeEcosystem` seeds `oc-target` with `parent_id="coord"` and the same `.models/ornith` directory (`tests/test_0428_352_session_retention.py:85-96`). With a valid `status="idle"`, the lone child is skipped by the lineage matcher due to its absent parent id, but `_resolve_by_reference()` then queries the DB for rows under the known `coord` and directory. The target row is a unique match, so the resolver returns it; it does not return unresolved as the test comment claims.

   Recipe: give the lone child `status="idle"`, and set up the fake DB so no row is anchored to the trusted coordinator in that directory (while retaining rows with a different parent if the test needs to assert they remain unchanged). Then assert the resolver branch was reached, `lineage` was not observed, the final result is the resolver's unresolved/PARTIAL outcome, and all target/sibling rows remain. The test should distinguish this result from the earlier status gate.

4. Prior requested checks — unchanged from r5.

   The watcher coordinator is loaded before registry lookup; the ambiguous-lineage test asserts the lineage observer and preserves both rows; the live-agent pending-first PARTIAL-to-retry test remains unchanged. No r7 product-code diff was present.

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 33 tests in 1.337s` and `OK`. The output contained `HOLD: lane status is ''; session retained`, confirming the lone-child case did not reach reference resolution. Existing `card-status.py` ResourceWarnings were also emitted.

## Recommendation

Keep the candidate in CHANGES until the lone-child fixture passes the status gate and its DB fixture makes the expected resolver outcome true. Then rerun the suite.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r7 review requires lone-child resolver fixture correction; reviewed commit b16d7e63a.
