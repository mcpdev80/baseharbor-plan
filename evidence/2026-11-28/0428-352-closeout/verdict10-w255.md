# 0428-352 follow-up review r10 — w255

Date: 2026-11-28
Role: read-only review of `d1fc495cd` against `61b692302`, plus the specifically authorized w401 dry-run. No cleanup `--run` was performed.

## Verdict

CHANGES REQUIRED. The exact name+parent branch successfully resolves w401 in the required dry-run, and same-name multiplicity fails closed. Two fail-closed/truthfulness gaps remain: zero exact name+parent matches fall through to directory-only matching (which can choose a sibling), and retry-ticket persistence failures are ignored while the caller claims the ticket was retained.

## Requested points

1. Exact name+parent identity; directory as context — PARTIAL.

   `release-lane.py:161-187` resolves one exact lane name under the trusted coordinator and returns its `claudeSessionId`; the shared directory is not part of that exact match. The new tests cover two different lane names sharing one directory and two same-name/parent matches.

   However, if the exact name+parent match count is zero, execution falls through at line 188 into directory-based lineage at lines 189-200 and may return the only other child in that directory. That is a sibling-selection risk and violates the requested zero-match fail-closed rule. Also, watcher-registry directory matching runs before the name+parent branch (`:125-139`) and can raise on multiple directory registrations even when the selected lane has one exact name+parent match. The name-based identity must be applied before directory-only fallback, including registry fallback.

   Required recipe: when `name` and a trusted coordinator id are present, exactly one name+parent match resolves; zero returns unresolved/PARTIAL immediately; more than one raises ambiguous. Do not fall through to another lane's directory match. Restrict registry matching by the exact selected worker id/name, or place the exact name+parent resolution ahead of directory-only registry matching. Add a regression with zero name matches and exactly one same-directory sibling; assert no sibling id is returned or removed.

2. Truthful PARTIAL retry-ticket persistence — PARTIAL.

   `_persist_retry_ticket()` atomically writes an `opencode_id: null` ticket and returns `False` on any write failure (`release-lane.py:233-263`). The two error branches call it but ignore its return and unconditionally print “retry ticket retained” (`:437-447`). If the write fails, the output falsely claims persistence. In addition, `setdefault()` preserves any existing entry under that Codeman id, which may not be the newly described null-id ticket; the log should reflect the persisted entry actually present.

   Required recipe: check the helper result and emit “retry ticket persisted” only on success. On failure, report that no durable ticket was written, retain the reservation/session, and return the unresolved PARTIAL. If an entry already exists, validate/use it and report its actual state; do not claim a null-id ticket unless that is what the file contains. Add a persistence-failure test (e.g. an unwritable/failing pending path) and assert the message/state is truthful.

3. Reservation until gone proof — PASS in the reviewed control flow; test assertion could be stronger.

   Neither ambiguity nor unresolved branches call `release_pool`, so they retain the reservation/session. On the successful path, the code writes the exact mapping before destructive work and only reaches `release_pool()` after the exact OpenCode DB row has been verified absent (`release-lane.py:382-424`). The new retry-ticket test verifies ticket contents and sibling retention, but does not explicitly assert the pool reservation remains on an unresolved PARTIAL; add that assertion to make the card's reservation requirement durable.

4. Named tests — PASS for the tested cases, with the zero-match gap above.

   `test_name_parent_resolves_uniquely_under_shared_dir` exercises distinct exact names sharing a directory. `test_ambiguous_same_name_same_parent_fails_closed` exercises multiple exact identity matches. Neither covers zero exact matches with one live sibling, which is the fall-through risk.

## Authorized w401 dry-run

Command run exactly without `--run`:

`./scripts/worker-cleanup.sh w401-0428-292-consentfix`

Output:

```text
evidence accepted from acceptance.json path: evidence/2026-11-27/0428-292/korrektur-1884-fix.md
PLAN release name=w401-0428-292-consentfix codeman=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c opencode=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c (w401-0428-292-consentfix)
DRY-RUN pool reservations: none
cleanup plan complete for w401-0428-292-consentfix (RUN=0)
```

The current read-only Codeman record for this exact name has parent `e6ca7696-b1f8-492d-b226-876b16925fc5`, and both its `id` and `claudeSessionId` equal `2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c`; the shared working directory is `/home/marcel/dev/baseharbor-ecosystem/workers/.models/flash`. The exact-id OpenCode DB query returned no matching `session_v2` rows. The dry-run therefore demonstrates exact w401 name/parent resolution, no ambiguous-lineage failure, and an already-absent OpenCode row. It reports no current pool reservation. No Codeman/OpenCode state was changed.

I did not run a w402 cleanup dry-run; no conclusion about its current exact mapping is inferred from w401.

## Verification

Ran the requested command from the coordinator repository:

`python3 -m unittest discover -s tests`

Result: `Ran 36 tests in 0.692s` and `OK`. Existing `card-status.py` ResourceWarnings were emitted. Passing tests do not cover the zero-name-match sibling fall-through or failed retry-ticket write.

## Recommendation

Keep 0428-352 in CHANGES. Fix zero exact-match behavior and ticket-write reporting, add the two focused regressions, and retain the explicit reservation assertion. After review, the w401 dry-run indicates its exact OpenCode session is already gone; with the corrected code, a separately authorized cleanup run can remove the still-live Codeman agent and reconcile the lane state. Re-capture w402's exact-name/parent and DB witnesses before any cleanup run for that lane.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 r10 review finds zero-match directory fallback and retry-ticket write-report defects; w401 dry-run exact match confirmed, no mutation.
