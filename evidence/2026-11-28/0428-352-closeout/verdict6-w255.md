# 0428-352 follow-up review r6 — w255

Date: 2026-11-27
Role: read-only review of commit `31c2a2e46` against `3d24488fe` and Verdict 5.

## Verdict

CHANGES REQUIRED. The intended lone-child fixture is defined with a selectable id, but the test still passes the wrong agent list into the helper. The resolver is not reached, so the prior finding remains open.

## Review points

1. Points 1-3 from the previous review — UNCHANGED.

   The r6 diff changes only the lone-child test. The r5 implementation reads the watcher coordinator identity before registry resolution, and its lineage branch has an observer-backed ambiguous-multiplicity test. The live-agent pending-first retry test and its PASS evidence are unchanged from the prior review.

2. Lone-child resolver reachability — FAIL.

   In `test_lone_child_missing_parent_stays_unresolved`, the test sets `rl.agents` to return `cm-lone-0428` at `tests/test_0428_352_session_retention.py:319-322`, but then invokes `_run(rl, "cm-lone-0428", ["--run"], env.agent(), env)` at line 329. `_run()` replaces `rl.agents` with the `agent` argument (`:135-145`), and `env.agent()` returns the unrelated `cm-18352` fixture (`:116-120`). Thus `select_agent()` cannot find `cm-lone-0428`; `main()` exits before reference resolution.

   The observed suite output confirms this path: `HOLD: exact lane not found and no pending release record`. The test's nonzero result and preserved DB row are a selector-miss, not proof that a lone lineage child with an absent parent id remains unresolved.

   Recipe: pass the selectable lone-child list to `_run`, for example the same list assigned to `rl.agents`, and assert the observed release path reaches the resolver. Then assert no `lineage` observer event, the unresolved/HOLD outcome, and unchanged target and sibling rows. Do not use a selector miss as the negative result.

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 33 tests in 2.198s` and `OK`. The output included `HOLD: exact lane not found and no pending release record` for the lone-child case, confirming the test exits before the resolver. Existing `card-status.py` ResourceWarnings were also emitted.

## Recommendation

Keep the candidate in CHANGES until the lone-child test passes its selectable fixture to `_run` and demonstrates that the production resolver rejects the missing-parent child.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r6 review requires the lone-child fixture passed through _run; reviewed commit 31c2a2e46.
