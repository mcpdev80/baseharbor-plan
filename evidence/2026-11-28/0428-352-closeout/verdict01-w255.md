# 0428-352 independent review — w255

Date: 2026-11-27
Role: read-only review of the uncommitted candidate in the coordinator working tree.

## Reviewed candidate

- `scripts/release-lane.py` (+51/-9)
- `scripts/watch.py` (+8)
- `tests/test_0428-352_session_retention.py` (untracked, seven tests)
- Card contract: `tasks/t-20261127-coord-session-retention.md`, card 0428-352, from Plan main `96cada1245dcaaf325a7785644371e471a264f17`.
- Related implementation note: `evidence-staging/2026-11-27/w392-0428-352-fix.md`.
- Candidate has no commit SHA; this verdict applies only to the reviewed working-tree contents.

## Verdict

CHANGES REQUIRED. The candidate improves reservation retention and adds replay cleanup, but does not yet prove that a retry resumes the exact intended OpenCode session. The acceptance test mocks out the lookup where the ambiguity exists.

## Findings

1. Session selection and PARTIAL retry — CHANGES.

   `scripts/release-lane.py:76-96` returns the first watcher registration matching a shared working directory. A shared `workers/.models/<channel>` directory can match multiple worker registrations, so iteration order can select a sibling. The following agent/DB resolution at lines 98-117 also returns the first match, rather than proving uniqueness. This violates the card's exact lane-to-session mapping and sibling-protection contract.

   The persisted PARTIAL entry at lines 236 onward is keyed by Codeman id, but stores `opencode_id=None` plus the shared directory. The pending-resume code at lines 206-220 resolves from that directory. Meanwhile, when the Codeman agent still exists, control follows the live-agent branch at lines 222-227 and calls `open_sessions()` from its working directory again. Thus the persisted entry is not itself an exact OpenCode-session reference, and the retry still depends on the ambiguous lookup.

   The test `test_retry_resolves_exact_reference_and_deletes_once` does not exercise this risk: after the first PARTIAL it replaces `open_sessions` with a lambda returning the intended id. The `_fresh_env` fixture does contain a sibling row in the same directory, but the test never invokes the real lookup against that fixture. The sibling-preservation test similarly stubs `open_sessions` to the intended id. These tests cannot establish that production mapping selects the intended session or fails closed when the mapping is ambiguous.

   Required recipe: make the working directory unique per lane, or persist a validated exact OpenCode session id/reference before retry. The retry must consult that durable exact reference even while the Codeman agent remains present. Every registry/lineage/DB lookup must reject multiple matches rather than return the first. Add regression coverage using the actual `open_sessions()` and `_resolve_by_reference()` code with two same-directory sessions/registrations; simulate the first missing-reference PARTIAL and a retry without a newly supplied spawn reference; assert only the target is removed and the sibling remains. Retain the reservation until the exact session is gone.

2. Reservation ordering and deletion checks — PASS with residual acceptance gap.

   The first mapping-failure PARTIAL writes the pending record and keeps the pool reservation (`release-lane.py:236-257`). The destructive path checks the exact OpenCode DB id and verifies deletion before clearing pending state and releasing the pool (`:287-308`). This is directionally consistent with “release only when gone.” However, the candidate tests inspect the fake pool JSON and DB directly; they do not run the card-required `worker-cleanup.sh <lane> --run` followed by `python3 coordinator/scripts/pool-reconcile.py status` and assert the seat is vacant. Add that acceptance-level test or document the separately executed acceptance proof before claiming the full card contract.

3. Replay suppression in `scripts/watch.py` — PASS, with one test hygiene change requested.

   `cmd_remove()` now removes the worker's `pending_events` entry as well as its registration (`watch.py:566-575`). In the release path, `release-lane.py` acknowledges the event before invoking remove (`:309-313`), so the purge follows successful release acknowledgement. `prune-watch.sh:21-25` also uses remove only for registrations whose worker ids are absent from the live Codeman agent list; purging a dead worker's stale replay entry is consistent with that cleanup purpose.

   The replay test asserts both registration and pending-event removal. But `_watch_env()` writes to the fixed source-tree path `scripts/.w352-fake-watcher-state.json` (`tests/test_0428-352_session_retention.py:288-301`) rather than an isolated temporary path. The file was absent after the requested suite completed, but the fixed path can collide across runs or survive interruption. Put the fake state in a unique temporary directory on the same filesystem as the production state file (for atomic replace), and clean it in a `finally`/temporary-directory scope. Restore environment variables and `sys.argv` after each test; `_install()` mutates release-related environment variables and the replay test mutates `CODEMAN_WATCH_STATE`/`sys.argv` without restoring them.

4. Test isolation — PARTIAL PASS.

   The new release tests redirect DB, pending ledger, receipts, pool, and paths to a `TemporaryDirectory`; `accepted` is stubbed and subprocess calls are replaced with fakes. The replay test points the loaded module at fake watcher JSON. Inspection shows no command targeting the real Plan repository, real pool, real OpenCode DB, or real Codeman/OpenCode session. The requested test run completed successfully. The fixed source-tree fake file and process-global environment/argv leakage above are test-hygiene defects, not evidence that real pool/session state was mutated.

5. Backward compatibility — PASS for Python function signatures.

   The reviewed changes do not alter the signatures of `open_sessions`, `cmd_remove`, or the relevant CLI entry points. New persisted fields are read with `.get()` and the pending record is additive. This review did not establish compatibility with every historical JSON shape beyond those code paths.

## Verification

Command run as explicitly requested from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 24 tests in 0.519s` and `OK`. The run also printed ResourceWarnings from existing tests and the expected structural-conflict fixture message. Passing the suite does not close finding 1 because the relevant lookup was stubbed in the new retry tests.

## Recommendation to w392

Before requesting PASS, implement one exact-session strategy (unique per-lane directory or durable exact OpenCode id/reference), make resolution fail closed on multiple matches, and revise the retry test to exercise the actual production resolver against the same-directory sibling fixture. Add the cleanup/pool-reconcile acceptance proof. Isolate the watcher test state and restore test process environment/argv. Then rerun the requested suite and provide the output.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 review requires changes; candidate remains uncommitted (no candidate SHA).
