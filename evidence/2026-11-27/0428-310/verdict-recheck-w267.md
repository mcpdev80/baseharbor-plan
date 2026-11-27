# Re-review verdict — 0428-310 syncDir durability (CODEX finding 1/2, mission w403)

Lane: w403-0428-310-syncdirfix (ROLLE=REVIEW) · Card: t-20261125-hunt40-migration-marker-last (0428-310) · Repo: baseharbor · PR: #1881
Candidate head: 640f53a6e879f094010b5a6690f19193a22f6e91 (branch lane-0428-310-migration-marker)
Base attested: exact develop ea5218d72e263f21e79853b679af50074dab8c25 via `git ls-remote`; candidate carries exactly 3 own commits (fc510d73, 6fb13d01, 640f53a6); `git merge-base --is-ancestor ea5218d72e HEAD` = OK.

## VERDICT: CLOSABLE — no product change required

The two Codex findings on the corrected candidate are NOT defects. FINDING 1 is a mischaracterization of the caller that conflates a documented best-effort directory-fsync seam with the completion-claim predicate; FINDING 2's required CI route already exists in the base plan. The candidate is accepted as-is for merge (merge is NOT this leg's action — see disposition).

## FINDING 1 — trace against the exact candidate (migration.go)

Finding text: "syncDir returns nil if opening the directory fails and also returns nil for every Sync or Close error. ensureFrozenMarker then proceeds to create the completion marker. Thus an actual directory I/O failure can allow the code to claim a durable completion marker even though the canonical rename's directory entry was not confirmed durable."

Two `syncDir` call sites in the candidate:
- writeDurableCanonicalData (migration.go:167): `return syncDir(filepath.Dir(dst))` — directory fsync of the canonical data dir AFTER the temp->rename.
- ensureFrozenMarker (migration.go:209): `return syncDir(dir)` — directory fsync of the marker dir AFTER the marker write.

`syncDir` (migration.go:174-188) returns nil on Open failure, Sync error, and Close error. This is CORRECT by design (comment migration.go:170-173): directory fsync is unsupported/ephemeral on some platforms; the data-before-marker *ordering* contract is enforced by the FILE-layer durability (temp-file fsync -> rename -> marker fsync), not by directory-entry durability. The nil-return is a documented best-effort seam, not an swallowed error.

CRITICAL — the completion-claim predicate is NOT directory fsync; it is `frozenMarkerComplete` (store.go:548-553):
- The loader honors a migration as "frozen" ONLY via `canonicalMigrationFrozen(canonical)` -> `frozenMarkerComplete(marker)`.
- `frozenMarkerComplete` requires Lstat regular + readable + EXACT canonical content match (store.go:549-553, migration.go:97-104).
- The marker is created by `writeFrozenMarker` (migration.go:61-67): `canonicalMarkerFS.writeMarker` (OpenFile/Chmod/Write/Sync/Close — each returns an error on real failure) THEN `verifyFrozenMarkerContent` (read-back + exact canonical content match — returns an error on empty/truncated/wrong content).

So the finding's causal chain is broken at the marker-write step: a real marker-write failure RETURNS AN ERROR (the error propagates out of ensureFrozenMarker -> migrateToCanonical -> adoptLegacySelection, never treated as success). A lost directory entry NEVER fabricates a content-complete marker, because completeness is gated by exact content round-trip, not by directory-entry durability. The finding conflates two distinct durability dimensions:
- directory-entry durability (best-effort crash-safety seam, correct as-is)
- the completion-claim predicate (content verification, fails closed)

The card's named defect class — "half-migrated state counts as finished" — is CLOSED by the content gate, which the w399 candidate already strengthened (w399 akte finding 1/2: "readability alone is NOT a completion claim"). The w399 akte's own root-cause check at base ea5218d72e verified the marker is written LAST after the data rename. The w403 candidate's only delta vs that base is a behavior-free store.go(695)->migration.go(210) split + 3 regression tests — zero behavioral change to the fail-closed paths.

FINDING 1 REJECTED as a defect. No product change required.

## FINDING 2 — CI route exists (no .github/** edit needed)

Finding text: new tests must be SELECTED by existing CI test-selection rules without editing .github/**.

Verified in the exact candidate (scripts/pr-go-unit-shard.py:118-137):
- `packages()` mode runs `go list ./...`, then `go test -count=1 *others` on EVERY non-CLI package.
- `internal/orgconfig` is a non-CLI Go package; it is auto-discovered and auto-selected by this mode. No per-test registration list, no catalog row, no .github/** change required (doctrine: ordinary Go unit tests are package-discovered).
- The w399 candidate added internal/orgconfig/migration_marker_test.go (package orgconfig); it is selected by the same `go test ./internal/orgconfig/...` that every other non-CLI package gets.

The run cited in the mission (46042210279) that logged UNIT_SCOPE empty / REJECT was the draft-triggered run BEFORE the PR was readied; the readied pull_request runs select every non-CLI package (this is the standard unit scope). FINDING 2's requirement is met by the existing mechanism.

## Regression coverage of the finding's failure class

migration_marker_test.go locks the fail-closed behavior:
- TestWorldWritableMigrationMarkerWriteFailureFailsClosed: faulted marker write -> adopted=true + error, canonical data preserved, no complete claim, LoadActive returns the migrated value, retry completes durably, deleted canonical + marker present -> ErrNotConfigured (never re-adopts).
- TestMigrateToCanonicalKeepsDataBeforeMarkerOrder: failed marker write returns error AFTER data landed, no complete claim; idempotent re-run with complete marker leaves it untouched.
- TestLoadActiveOptionalTwoCallRepairsLostMarkerWithoutManualWrite: call 1 preserves + reports the fault; call 2 repairs the marker through the normal load path.
- TestFrozenMarkerContentVerification: empty/truncated/wrong-content and directory residues are NOT completion claims; content-verify fails; repair rewrites to canonical; exact marker is idempotent; directory residue reported, never deleted/honored.
- TestWriteDurableCanonicalDataFsyncsBeforeRename: seam order temp-sync < rename < dir-sync < marker is locked.

These cover exactly the card's failure class the finding describes (marker claims done while data not durable / half-written). The finding's specific assertion (syncDir nil-return fabricates a completion claim) is disproven by the content gate.

## Disposition

- This leg is ROLLE=REVIEW. It renders an independent verdict only. It does NOT modify the candidate, does NOT push, does NOT run reruns, and does NOT merge.
- VERDICT: CLOSABLE — the corrected candidate 640f53a6e8 is accepted for merge on PR #1881. No product delta is required.
- The only open operational blocker (inherited from the w399 candidate) is the Trusted Plan base-catalog hold: scripts/pr-gate-coverage.json on develop (ea5218d72e) carries NO row for internal/orgconfig, so the base-controller gate planner aborts the plan (class-A known-blocker, same as card 0428-289/#1880, owner hold #136 + fan-in #1861-1863). This is a BASE-CATALOG / OWNER-scope freeze, not a product defect, and is out of this review leg's write-set. The in-PR catalog rows (source.internal_orgconfig_store_go, source.internal_orgconfig_migration_go, source.internal_orgconfig_migration_marker_test_go, source.internal_orgconfig_migration_go mirror row) were already shipped by the w399 candidate as the minimal same-PR route.
- Merge remains a Codex-owner action AFTER a green exact-hosted run on this head (develop-catalog freeze-lift required). w403 posts this verdict for the owner/Codex to act on.

## Evidence witnesses

- Candidate head (ls-remote): git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-310-migration-marker = 640f53a6e879f094010b5a6690f19193a22f6e91
- Base (ls-remote): git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop = ea5218d72e263f21e79853b679af50074dab8c25 (candidate parent chain verified via git merge-base --is-ancestor)
- Own commits only: git log --oneline ea5218d72e..640f53a6e8 = {640f53a6 refactor, 6fb13d01 fix verify marker, fc510d73 fix fail-closed}
- Changed files vs develop: internal/orgconfig/migration.go, internal/orgconfig/migration_marker_test.go, internal/orgconfig/store.go, scripts/pr-gate-coverage.json — NO .github/** (write-set discipline confirmed)
- CI route verified: scripts/pr-go-unit-shard.py packages() runs `go test -count=1` on every non-CLI package; internal/orgconfig auto-selected.
