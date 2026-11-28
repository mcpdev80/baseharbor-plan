# 0428-352 follow-up verdict 12

Role: read-only review. Candidate `0bcb37d0cb2cd4f2f00e0316a10c816fe99d1f4a`, reviewed against `66991f6dc` and the verdict 11 recipe. No product or plan state was mutated. The two requested cleanup invocations were dry-run only, with no `--run`.

## Verdict

CHANGES REQUIRED. Most of the R12 changes address the requested paths, but the zero-match contract and its regression proof are incomplete.

1. Name plus trusted parent is evaluated before registry when `name`, `coord`, and a truthy `items` list exist (`scripts/release-lane.py:157-177`). However, the guard is `if name and coord and items`. An authoritative empty result (`items == []`) falls through to registry matching at `scripts/release-lane.py:179-214`, so a stale matching registry entry can resolve a lane after the live-agent lookup found zero matches. Make the branch run whenever the agent listing completed, including an empty list, and return unresolved immediately for zero exact matches before registry/lineage fallback. Treat lookup failure separately and fail closed unless a separately validated durable exact reference is available.

2. The added production-resolver regression constructs `sibling_child` but never injects it into `rl.agents` (`tests/test_0428_352_session_retention.py:628-670`). It directly calls `_resolve_by_reference`, which therefore consults the real agent-listing function rather than the controlled same-directory sibling fixture. Its `name_parent` observer assertion does not prove which live-agent list was evaluated. Inject the fixture into the production resolver's agent source and add a case with an empty completed list plus a matching stale registry record; assert unresolved and no sibling selection/removal.

3. Reservation assertion: the unresolved PARTIAL test writes the reservation before its second `_run`, snapshots the pool, and compares the complete key set afterward (`tests/test_0428_352_session_retention.py:558-574`). This does prove reservation retention over that retry invocation. It does not cover the earlier first invocation; keep the current retry assertion and add/retain a pre-run snapshot for the invocation claimed by the test as the first PARTIAL if that is part of the intended acceptance contract.

The retry-ticket helper uses a single lock/read/update/write scope with unlock and close in `finally` (`scripts/release-lane.py:283-321`). The caller reports write failure without claiming persistence in the test at `tests/test_0428_352_session_retention.py:720-758`; the test simulates a helper return of `None`, while the helper's actual failure mode raises. Consider making the end-to-end failure case raise from the helper or exercise an actual write exception so it proves the new exception catch path.

## Verification

Command: `python3 -m unittest discover -s tests`

Result: `Ran 39 tests in 1.071s` / `OK`. Existing `ResourceWarning`s remain in `scripts/card-status.py:76` for unclosed task file handles; no test failure.

Dry-run command: `./scripts/worker-cleanup.sh w401-0428-292-consentfix`

Output:

```text
evidence accepted from acceptance.json path: evidence/2026-11-27/0428-292/korrektur-1884-fix.md
PLAN release name=w401-0428-292-consentfix codeman=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c opencode=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c (w401-0428-292-consentfix)
DRY-RUN pool reservations: none
cleanup plan complete for w401-0428-292-consentfix (RUN=0)
```

Dry-run command: `./scripts/worker-cleanup.sh w402-0428-315-constfix`

Output:

```text
evidence accepted from acceptance.json path: evidence/2026-11-27/0428-315/korrektur-1882-fix.md
PLAN release name=w402-0428-315-constfix codeman=e0ed81d0-fac2-4f3d-aae3-0009e872f466 opencode=e0ed81d0-fac2-4f3d-aae3-0009e872f466 (w402-0428-315-constfix)
DRY-RUN pool reservations: none
cleanup plan complete for w402-0428-315-constfix (RUN=0)
```

Both dry-runs resolved independently to the expected exact lane names and IDs; neither reported ambiguous lineage, and neither executed cleanup.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 R12 has outstanding zero-match fallback and regression-fixture gaps; candidate 0bcb37d0cb2cd4f2f00e0316a10c816fe99d1f4a

---

## r13 resolution (0428-352 R13, w392)

Runde 13 (verdict12 CHANGES) mission executed. Two points, both implemented and proven by the full suite (40 tests OK).

PLAN (board file workers/todos/w392-0428-284-demo183fix5.json, evidence ## PLAN below):

- Read mission w392 Runde 13 + akte 0428-352-verdict12-w255.md.
- Implement point 1: authoritative empty listing + fail-closed lookup error.
- Implement point 2: production-resolver fixture injection + empty-list/stale-registry case.
- Run full suite python3 -m unittest discover -s tests -> all green. Commit r13 under lane identity w392-0428-284-demo183fix5 on base 0bcb37d0c (prove ancestor). Update akte with ## PLAN + results. Report END_DONE/candidate SHA to sonde.

CHANGES (candidate 2d357c3df, base 0bcb37d0c proven ancestor; only scripts/release-lane.py + tests/test_0428_352_session_retention.py; only own commit 2d357c3df on top).

Point 1 (verdict12 item 1) — scripts/release-lane.py _resolve_by_reference():

- The live-agent listing is now consumed and its result is authoritative. The listing is wrapped so `listing_ok` records whether it returned a list; `items` stays None and `listing_ok` stays False only when the listing RAISED (lookup not complete).
- The exact name+parent guard now runs on a completed listing: `if name and coord and listing_ok and items is not None:`. An empty list `[]` (authoritative null) therefore runs the name+parent branch and returns None on zero exact matches, before registry/lineage — a stale registry entry can no longer resurrect a sibling after an authoritative empty live lookup.
- New guard: `if name and not listing_ok: return None`. A listing that raised (items None, lookup incomplete) is a lookup ERROR, NOT an authoritative empty result; with a requested identity the resolver fails closed and does NOT guess from a stale registry/lineage match. The caller fails closed unless it supplies its own separately validated durable exact id.
- Docstring updated to state the completed-listing vs listing-error distinction.

Point 2 (verdict12 item 2) — tests/test_0428_352_session_retention.py:

- test_zero_name_match_production_resolver_never_selects_sibling now injects the controlled sibling fixture into the production resolver's agent source (`rl.agents = lambda: sibling_child`) so the real _resolve_by_reference() consults the controlled same-directory sibling list, not the production codeman agent listing. The name_parent witness now proves which live-agent list was evaluated.
- NEW test_zero_name_match_empty_listing_stale_registry_fails_closed: completed empty listing (rl.agents = lambda: []) + a STALE registry entry anchored to the trusted coord AND naming our lane title (exactly the entry the r12 guard would have resolved if items had been truthy). Asserts the resolver returns None (unresolved), never the stale registry id, the registry branch is never consulted (registry witness absent), name_parent ran, and the sibling DB row is untouched.

Full suite: `python3 -m unittest discover -s tests` -> Ran 40 tests in ~1.0s / OK (39 prior + 1 new). The ResourceWarnings remain in scripts/card-status.py:76/94 for unclosed task file handles; no test failure. The ABGEBROCHEN line at the tail of output is the unrelated card-status structural-conflict test writing to stderr; that test still asserts and passes.

Commit gate: git show -s --format=%an HEAD == w392-0428-284-demo183fix5 (exact). git merge-base --is-ancestor 0bcb37d0c HEAD passes. git log --oneline 0bcb37d0c..HEAD lists only 2d357c3df.

END_DONE w392-0428-284-demo183fix5: 0428-352 R13 complete (authoritative empty listing + fail-closed lookup error + production-resolver fixture injection); candidate 2d357c3df
