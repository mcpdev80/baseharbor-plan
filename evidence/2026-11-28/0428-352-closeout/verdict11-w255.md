# 0428-352 follow-up review r11 — w255

Date: 2026-11-28
Role: read-only review of `66991f6dc` against `d1fc495cd`; two explicitly requested dry-runs only, no `--run` and no cleanup mutation.

## Verdict

CHANGES REQUIRED. The separate w401 and w402 dry-runs each resolve to their own `claudeSessionId`, with no ambiguous-lineage failure. R11's name/parent change still does not satisfy the zero-match fail-closed contract, its test bypasses the resolver through a preseeded null-id pending entry, and the reservation assertions seed the reservation only after PARTIAL. Ticket-write failures also raise out of the helper without being caught by the caller, despite the test simulating a `None` return instead.

## Diff review

1. Exact name+parent identity before registry fallback — FAIL.

   The name+parent agent match at `release-lane.py:189-205` is useful, but it is reached only after watcher registry matching at lines 125-157. The registry match checks exact name/title and `opencode_id`, but does not require `entry.coordinator == coord`; it can return before validating the live agent's exact name+parent identity. Move exact name+parent resolution ahead of registry fallback, or constrain any registry return to the same trusted coordinator and exact selected worker identity.

2. Zero exact name+parent matches fail closed — FAIL in code and unproven by test.

   At lines 189-205, more than one exact match raises and one returns. When `len(exact) == 0`, control continues to the directory-based lineage matcher at lines 206-220. If exactly one sibling shares the directory and coordinator, it can be returned. This contradicts the docstring claim that zero exact matches return unresolved immediately.

   `test_zero_name_match_no_sibling_returned_or_removed` does not reach this resolver path. It seeds a pending entry with `opencode_id: null` but omits the `directory` and `created_at` fields (`tests/test_0428_352_session_retention.py:593-595`). On retry, `main()` takes the pending/no-id path and returns at `release-lane.py:411-415` before `open_sessions()` / `_resolve_by_reference()`. The test therefore proves only that a null-id pending ticket holds; it does not exercise zero name matches or sibling directory fall-through.

   Required recipe: add an immediate unresolved return when a name and trusted coordinator are supplied but no exact match exists. Create the regression so production resolution is actually invoked with the shared directory and a single same-directory sibling; assert the resolver returns unresolved, the sibling id is never selected, and no destructive call occurs.

3. PARTIAL retry ticket and honest failure — FAIL for real write errors; partial for existing records.

   `_persist_retry_ticket()` raises when its actual write fails (`release-lane.py:272-285`). Its callers at lines 452-465 do not catch that exception; the “NO durable ticket written” branch is reached only if the helper returns `None`, which the helper never does on write failure. The new test monkeypatches the helper to return `None` (`tests/test_0428_352_session_retention.py:671-672`), so it does not test the real failed-write path. Catch the persistence exception at the call site and report no ticket written while retaining session/reservation.

   The existing-entry check at line 267 calls `locked_json(...)[1]` and discards the returned lock without explicit unlock/close. The suite emitted `ResourceWarning: unclosed file ... .release-pending.json.lock` from this line. Use one lock/read/update/write scope and release it in `finally`; avoid a check-then-write race. When an entry already exists, inspect its actual state or use a truthful generic message without implying a new null-id ticket was written.

4. Reservation assertion — FAIL as evidence.

   In `test_partial_persists_retry_ticket_when_unresolved`, the reservation is written to the fake pool after the PARTIAL run (`:551-554`), so the assertion cannot prove that the run retained it. The persistence-failure test does the same after the run (`:692-695`). Seed each reservation before invoking `main()` and compare the pool before and after. In the implementation, unresolved returns do not call `release_pool`, which is directionally correct, but the requested regression proof is absent.

5. Same-name multiplicity test — PASS for the covered case.

   `test_ambiguous_same_name_same_parent_fails_closed` observes `name_parent` and verifies both rows survive. The shared-directory test also covers two different names. These do not cover the zero-name-match fall-through above.

## Requested read-only real-loop witnesses

Command (a), run without `--run`:

`./scripts/worker-cleanup.sh w401-0428-292-consentfix`

Output:

```text
evidence accepted from acceptance.json path: evidence/2026-11-27/0428-292/korrektur-1884-fix.md
PLAN release name=w401-0428-292-consentfix codeman=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c opencode=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c (w401-0428-292-consentfix)
DRY-RUN pool reservations: none
cleanup plan complete for w401-0428-292-consentfix (RUN=0)
```

Command (b), run independently without `--run`:

`./scripts/worker-cleanup.sh w402-0428-315-constfix`

Output:

```text
evidence accepted from acceptance.json path: evidence/2026-11-27/0428-315/korrektur-1882-fix.md
PLAN release name=w402-0428-315-constfix codeman=e0ed81d0-fac2-4f3d-aae3-0009e872f466 opencode=e0ed81d0-fac2-4f3d-aae3-0009e872f466 (w402-0428-315-constfix)
DRY-RUN pool reservations: none
cleanup plan complete for w402-0428-315-constfix (RUN=0)
```

Both are separate exact-name dry-run results; neither inferred w402 from w401. Neither reported ambiguous lineage. Both show no pool reservation currently present. These commands did not remove Codeman/OpenCode sessions, worktrees, or files.

## Test verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 38 tests in 1.062s` and `OK`. Existing `card-status.py` ResourceWarnings appeared, as did new unclosed release-pending lock warnings from `release-lane.py:267`. Passing tests do not close the resolver, persistence, or reservation-proof gaps above.

## Recommendation

Keep 0428-352 in CHANGES. Make the name+parent zero-match decision final before any directory fallback; ensure registry returns are parent/worker-identity anchored; make real retry-ticket write exceptions truthful and lock-safe; and seed reservation assertions before the PARTIAL. Then rerun the suite and exact-name dry-runs. No cleanup `--run` is authorized by this review.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r11 review finds name-zero fallback, registry-parent ordering, persistence exception, and reservation-test gaps; both dry-runs resolve exact IDs; 38 tests pass.

---

# 0428-352 follow-up review r12 — w392 (CHANGES RESOLVED)

Date: 2026-11-28
Role: implementing worker on existing card 0428-352 write-set (coordinator/scripts + coordinator/tests). No product repo, no .github/**, no product auth/consent touched.

## Resolution of each verdict11 point

1. Exact name+parent identity before registry fallback — RESOLVED.
   `_resolve_by_reference()` now decides exact name+parent BEFORE any registry fallback
   (release-lane.py:157-173). The registry return is additionally anchored to
   `entry.coordinator == trusted coord` (release-lane.py:183-194); when the watcher
   coord is still None the registry's own coordinator field becomes the anchor, so a
   stale bare-directory registry entry can no longer resurrect a sibling.

2. Zero exact name+parent matches fail closed — RESOLVED in code and proven by test.
   When name + trusted coord present but `len(exact) == 0`, the resolver returns None
   immediately (release-lane.py:171-173); the docstring now states this and the code
   agrees. New production-resolver regression
   `test_zero_name_match_production_resolver_never_selects_sibling` invokes the real
   `_resolve_by_reference()` with a shared directory and one same-directory sibling
   (different name), asserting None, sibling id never selected, `name_parent` witness
   fired, `lineage` never reached. The prior `test_zero_name_match_no_sibling_returned_or_removed`
   was retained.

3. PARTIAL retry ticket and honest failure — RESOLVED for real write errors.
   `_persist_retry_ticket()` now RAISES on a real write failure; both unresolved PARTIAL
   callers (release-lane.py:497-506 and :510-518) catch the exception and report
   truthful 'durable ticket written' only on a real write, 'exists' when a durable entry
   already exists, and 'no durable ticket written' on write failure while retaining
   session/reservation. The existing-entry check now shares one lock/read/update/write
   scope with the write and releases in `finally`, fixing the
   `ResourceWarning: unclosed file ... .release-pending.json.lock`. Suite run under
   `python3 -W error::ResourceWarning` shows no release-pending lock warning.

4. Reservation assertion — RESOLVED as evidence.
   `test_partial_persists_retry_ticket_when_unresolved` now seeds the reservation BEFORE
   the PARTIAL run and compares the pool before and after (`set(before) == set(after)`).

5. Same-name multiplicity — unchanged; still PASS for the covered case.

## Test verification

`python3 -m unittest discover -s tests` -> `Ran 39 tests in ~1.1s` and `OK` (was 38;
+1 new production-resolver regression). `python3 -W error::ResourceWarning` run is clean
of release-pending lock warnings (only pre-existing card-status.py warnings remain).

## Commit

`0bcb37d0c` fix(coordinator): 0428-352 r12 — resolver order, zero-match final, real
persist, reservation-before-seed. Base HEAD `66991f6dc` (proven ancestor:
`git merge-base --is-ancestor 66991f6dc HEAD` OK). Author and committer both
`w392-0428-284-demo183fix5@baseharbor.local`. Coordinator repo local-only (no remote).

0428-352 now READY for Maintainer review. Card 0428-284 stays on wait — no action.
