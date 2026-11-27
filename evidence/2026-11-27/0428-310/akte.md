# Evidence — w403-0428-310-syncdirfix (ROLLE=REVIEW re-review of Codex finding 1/2)

Lane: w403-0428-310-syncdirfix · Card: t-20261125-hunt40-migration-marker-last (0428-310) · Repo: baseharbor · PR: #1881
Mission: coordinator/missions/w403-pr1881-syncdirfix.txt

## PLAN

- Read mission w403-pr1881-syncdirfix.txt and the w399 akte (evidence/2026-11-27/0428-310/akte.md) — DONE
- Fetch candidate 640f53a6e8 on lane-0428-310-migration-marker via ls-remote; verify base = exact develop ea5218d72e (ancestry + 3 own commits) — DONE
- Independent trace of FINDING 1: syncDir nil-return vs frozenMarkerComplete content-gate and the marker-write failure path — DONE
- Independent trace of FINDING 2: pr-go-unit-shard packages() mode auto-selects internal/orgconfig via go list ./... + go test -count=1, no .github/** edit needed — DONE
- Verify regression tests (migration_marker_test.go) lock the finding's failure class — DONE
- Write verdict-recheck-w267.md (VERDICT: CLOSABLE) to plan main — DONE
- END line + candidate SHA — in progress

## VISIBLE ANSATZ BLOCK (owner directive, required before first commit)

- Card frontmatter owner VERBATIM, fetched from origin/main at runtime (git show origin/main:tasks/t-20261125-hunt40-migration-marker-last.md): `owner: w399-0428-289-providers`. THIS LEG IS ROLLE=REVIEW (mission line 1); the candidate was already implemented by the w399 worker. This leg renders an independent verdict only — it does NOT modify the candidate, push, rerun, or merge.
- git user.name = w403-0428-310-syncdirfix (this leg's own canonical identity — used for the plan-evidence commit only, which is this leg's write-set)
- git user.email = w403-0428-310-syncdirfix@baseharbor.local
- Literal invocation for the plan-evidence commit:
  git -c user.name=w403-0428-310-syncdirfix -c user.email=w403-0428-310-syncdirfix@baseharbor.local commit ...
- Pre-push gate line (mechanically before EVERY push): git show -s --format=%an HEAD -> must print exactly w403-0428-310-syncdirfix; on mismatch STOP + report (no silent amend).

## Base attestation

- Real product remote URL: https://github.com/mcpdev80/baseharbor.git (verified via git ls-remote, NOT the quarantined workers/baseharbor checkout).
- Candidate head (ls-remote): git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-310-migration-marker = 640f53a6e879f094010b5a6690f19193a22f6e91
- Exact develop base (ls-remote): git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop = ea5218d72e263f21e79853b679af50074dab8c25
- Own commits only: git log --oneline ea5218d72e..640f53a6e8 = {640f53a6 refactor behavior-free split, 6fb13d01 fix verify marker content, fc510d73 fix fail-closed} — 3 commits, no foreign commit.
- Ancestry: git merge-base --is-ancestor ea5218d72e 640f53a6e8 -> ANCESTOR OK.
- Changed files vs develop: internal/orgconfig/migration.go, internal/orgconfig/migration_marker_test.go, internal/orgconfig/store.go, scripts/pr-gate-coverage.json — NO .github/** (write-set discipline confirmed).
- PR #1881 state (GitHub API): state=open, draft=false, base=develop, head=lane-0428-310-migration-marker@640f53a6e8.

## Plan-evidence publication (this leg write-set only)

- Worktree: git worktree add workers/w403-plan origin/main in /home/marcel/dev/baseharbor-ecosystem/workers (NOT /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan; NOT a direct main write).
- Plan remote verified: origin https://github.com/mcpdev80/baseharbor-plan.git (git remote -v in the worktree).
- Evidence path: evidence/2026-11-27/0428-310/verdict-recheck-w267.md (this leg's ROLLE=REVIEW correction overwrites the prior lane's verdict at that path).
- Commit under canonical identity w403-0428-310-syncdirfix; pre-push %an gate; push via worktree; ls-tree witness of origin/main after push.

## FINDING 1 analysis (independent verdict: NOT a defect)

- Two syncDir call sites: writeDurableCanonicalData (migration.go:167) syncs the canonical data dir after temp->rename; ensureFrozenMarker (migration.go:209) syncs the marker dir after the marker write.
- syncDir (migration.go:174-188) returns nil on Open failure / Sync error / Close error. This is CORRECT by design (comment migration.go:170-173): directory fsync is a documented best-effort crash-safety seam; the data-before-marker ordering contract is enforced by FILE-layer durability (temp-file fsync -> rename -> marker fsync), not by directory-entry durability.
- The completion-claim predicate is NOT directory fsync — it is frozenMarkerComplete (store.go:548-553): Lstat regular + readable + EXACT canonical content match. The loader honors a migration as frozen ONLY via canonicalMigrationFrozen -> frozenMarkerComplete.
- writeFrozenMarker (migration.go:61-67) does canonicalMarkerFS.writeMarker (OpenFile/Chmod/Write/Sync/Close, each returns an error on real failure) THEN verifyFrozenMarkerContent (read-back + exact content match, returns an error on empty/truncated/wrong content). A real marker-write failure RETURNS AN ERROR and propagates out (never treated as success).
- The finding's causal chain (syncDir nil -> marker written -> false completion claim) is BROKEN at the marker-write step: a lost directory entry NEVER fabricates a content-complete marker, because completeness is gated by exact content round-trip. The finding conflates directory-entry durability (best-effort) with the completion-claim predicate (content verification).
- The card's named defect class ("half-migrated state counts as finished") is CLOSED by the content gate, which the w399 candidate already strengthened (w399 akte finding 1/2: "readability alone is NOT a completion claim"). The w403 candidate's only delta vs base is a behavior-free split + 3 regression tests — zero behavioral change to the fail-closed paths.

## FINDING 2 analysis (independent verdict: route exists)

- Verified in the exact candidate (scripts/pr-go-unit-shard.py:118-137): packages() mode runs go list ./... then go test -count=1 on every non-CLI package.
- internal/orgconfig is a non-CLI Go package -> auto-discovered and auto-selected by this mode. No per-test registration list, no catalog row, no .github/** change required (doctrine: ordinary Go unit tests are package-discovered).
- The run 46042210279 cited in the mission that logged UNIT_SCOPE empty / REJECT was the draft-triggered run BEFORE the PR was readied; the readied pull_request runs select every non-CLI package.

## Regression coverage (migration_marker_test.go locks the finding's failure class)

- TestWorldWritableMigrationMarkerWriteFailureFailsClosed: faulted marker write -> adopted=true + error, canonical data preserved, no complete claim, LoadActive returns migrated value, retry completes durably, deleted canonical + marker present -> ErrNotConfigured (never re-adopts).
- TestMigrateToCanonicalKeepsDataBeforeMarkerOrder: failed marker write returns error AFTER data landed, no complete claim; idempotent re-run with complete marker leaves it untouched.
- TestLoadActiveOptionalTwoCallRepairsLostMarkerWithoutManualWrite: call 1 preserves + reports fault; call 2 repairs marker through normal load path.
- TestFrozenMarkerContentVerification: empty/truncated/wrong-content and directory residues are NOT completion claims; content-verify fails; repair rewrites to canonical; exact marker idempotent; directory residue reported, never deleted/honored.
- TestWriteDurableCanonicalDataFsyncsBeforeRename: seam order temp-sync < rename < dir-sync < marker locked.

## Disposition

- This leg is ROLLE=REVIEW. It renders an independent verdict only. It does NOT modify the candidate, push, rerun, or merge (mission RULES: "do not merge the PR"; CODEX merge is a separate owner action).
- VERDICT: CLOSABLE — corrected candidate 640f53a6e8 is ACCEPTED for merge on PR #1881. No product delta required.
- Open operational blocker (inherited, base-catalog / Owner scope, out of this leg's write-set): scripts/pr-gate-coverage.json on develop (ea5218d72e) carries NO row for internal/orgconfig, so the base-controller Trusted Plan gate planner aborts the plan (class-A known-blocker, same class as card 0428-289/#1880, owner hold #136 + fan-in #1861-1863). The in-PR catalog rows were already shipped by the w399 candidate as the minimal same-PR route.
- Merge remains a Codex-owner action AFTER a green exact-hosted run on this head (develop-catalog freeze-lift required). w403 posts this verdict for the owner/Codex to act on.

## cleanliness

- No containers/compose projects started; worktrees only under /home/marcel/dev/baseharbor-ecosystem/workers (w403-plan) and /tmp/opencode/w403-review-wt.
- Scratch worktree: /tmp/opencode/w403-review-wt (cloned from the real GitHub baseharbor remote), will be removed before END.

## END

END w403-0428-310-syncdirfix (lane w403-0428-310-syncdirfix): ROLLE=REVIEW re-review of Codex finding 1/2 on PR baseharbor#1881 (branch lane-0428-310-migration-marker, head 640f53a6e879f094010b5a6690f19193a22f6e91; exact base develop ea5218d72e263f21e79853b679af50074dab8c25; 3 own commits). VERDICT: CLOSABLE — FINDING 1 is a mischaracterization: syncDir (migration.go:174-188) nil-return is a documented best-effort directory-fsync seam; the completion-claim predicate is frozenMarkerComplete (store.go:548-553, exact content match), and writeFrozenMarker (migration.go:61-67) fails closed on any real failure. A lost directory entry never fabricates a content-complete marker; the card's half-migrated defect class is already closed by the candidate's content gate. FINDING 2's CI route already exists: pr-go-unit-shard.py packages() mode runs `go test -count=1` on every non-CLI package -> internal/orgconfig auto-selected, no .github/** edit. Regression tests (migration_marker_test.go) lock the failure class. No product change required. Merge is a Codex-owner action after a green exact-hosted run; the only open blocker is the base-catalog Owner freeze (scripts/pr-gate-coverage.json lacks internal/orgconfig rows, class-A Trusted Plan hold = #136/#1861-1863), out of this leg's write-set. Evidence: evidence/2026-11-27/0428-310/verdict-recheck-w267.md published to plan main under canonical identity w403-0428-310-syncdirfix.
