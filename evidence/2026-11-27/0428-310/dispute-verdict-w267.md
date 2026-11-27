# Dispute verdict — PR #1881 / card 0428-310

ROLE=REVIEW
Reviewer lane: `w267-0428-284-pridentity`.
Decision: retain CHANGES on durability; accept w403's CI-route correction. PR #1881 is not lift-ready unchanged.

## PLAN

1. Refresh Plan main and the product PR head; locate w403's published re-verdict.
2. Read the exact candidate implementations for directory sync, marker verification, and unit-package discovery.
3. Verify run 46042210279's exact-head event, failing jobs, and UNIT_SCOPE state.
4. Decide whether the exact-content marker predicate closes the directory-durability failure mode; state the CI-route disposition separately.
5. Stage this dispute verdict only. Do not edit or merge the product PR.

## Exact refs and published evidence

Plan `origin/main`: `b3e572ecf374ed1d54d4172396fb298cfac03a30`.
W403 review commit: `a03b217df8bb7857b7eceb929efcd3a2a1fcba72`, ancestor of current Plan main.
W403 re-review: https://github.com/mcpdev80/baseharbor-plan/blob/a03b217df8bb7857b7eceb929efcd3a2a1fcba72/evidence/2026-11-27/0428-310/verdict-recheck-w267.md
Current 0428-310 akte: https://github.com/mcpdev80/baseharbor-plan/blob/b3e572ecf374ed1d54d4172396fb298cfac03a30/evidence/2026-11-27/0428-310/akte.md

Product remote refs: `refs/pull/1881/head` = `640f53a6e879f094010b5a6690f19193a22f6e91`; `refs/heads/develop` = `6944e8761af6f07b801f55e39bb9a5409226c10b`. The candidate head is unchanged.

## Finding 1 — retained: content-complete marker does not prove canonical rename durability

W403 is correct that marker validity is content-based. On the exact candidate, `migration.go:61-67` writes and reads back the canonical marker; `migration.go:97-104` and `store.go:548-553` require the marker to be present, readable, and byte-for-byte equal to `canonicalMarkerContent`. A failed marker-file write or failed content verification is returned as an error. Those checks prevent an empty, truncated, or wrong-content marker from being treated as complete.

They do not establish the durability of `active.json`'s directory entry. The exact write sequence is:

- `migration.go:153-167`: fsync the temp file, rename temp to `active.json`, then call `syncDir` for the canonical directory.
- `migration.go:170-187`: `syncDir` returns nil for every directory open, sync, and close error; it does not distinguish unsupported directory fsync from a real I/O error.
- `migration.go:203-209`: after the data step returns success, create and verify the marker, then call `syncDir` again.
- `store.go:548-553`: later migration suppression is based only on the static marker content, not on the presence, content, or digest of `active.json`.

A marker entry surviving recovery with exact content is not evidence that the earlier rename entry survived. If data-directory sync fails and the rename is lost across a crash while the marker file remains, `frozenMarkerComplete` still accepts the marker and `canonicalMigrationFrozen` prevents legacy recovery; the canonical selection can be absent while migration is recorded as complete. The completion predicate and marker-file write are sound for marker-content integrity, but they do not cure the suppressed data-directory-sync failure. W403's “lost directory entry never fabricates a content-complete marker” addresses loss of the marker entry; the failure mode here is loss of the canonical data entry while a content-complete marker remains.

Correction recipe: make the data-directory sync result part of the data-before-completion contract. Propagate real directory open/sync/close I/O errors and do not create the completion marker after such an error. If a platform explicitly does not support directory fsync, identify that unsupported case rather than treating every error as unsupported; either use a platform-specific durability mechanism or fail closed without claiming the once-only migration is durable. Add a deterministic injected data-directory-sync failure regression proving the marker is not reported complete, then verify retry/recovery retains the canonical selection and never silently accepts a missing canonical file under a complete marker. Keep the exact marker-content checks.

## Finding 2 — retracted: package selection route exists

I accept w403's code-path finding. Exact-head `scripts/pr-go-unit-shard.py:118-135` implements `packages()` by running `go list ./...`, collecting every package, separating only the CLI package, then running `go test -count=1` on every remaining package. `internal/orgconfig` is therefore auto-discovered and selected; the added `migration_marker_test.go` belongs to that package. No `.github/**` change or additional test-registration row is required for this existing package route.

This retracts any implication that the test is absent from the unit selector. It does not make the current exact-head test evidence green, because the trusted planner aborted before the selector ran.

## Run 46042210279 and empty UNIT_SCOPE

The run is terminal `completed/failure`, event `pull_request`, on exact head `640f53a6e879f094010b5a6690f19193a22f6e91` and branch `lane-0428-310-migration-marker`. `PR · Trusted Plan` failed first. The `PR · Go unit` job was skipped; `PR Selected Checks` then logged `UNIT_SCOPE` empty and `UNIT_RESULT=skipped`, followed by `REJECT: Go test selection missing or invalid`.

The empty scope is consistent with w403's explanation that the upstream Trusted Plan failure prevented package selection; it is not evidence against `packages()`'s auto-discovery. The observed run metadata only establishes `event=pull_request`; it does not establish a `ready_for_review` action. Across the exact head, the two observed PR runs are `46042082459` (cancelled) and `46042210279` (failure); neither is a passing test receipt, and no exact-head run is currently in progress.

## Final technical disposition

CHANGES retained solely for `migration.go:170-187` suppressing all directory-sync errors before the completion marker. CI-route finding retracted. The candidate is not closable/lift-ready unchanged on this review; no product edits, test runs, PR mutation, or merge were performed. The corrective recipe above is the required next change.

END_DONE w267-0428-284-pridentity: dispute review completed; retain #1881 CHANGES for directory durability, retract CI-route finding; candidate 640f53a6e879f094010b5a6690f19193a22f6e91 unchanged.
