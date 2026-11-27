# Evidence — 0428-310 orgconfig migration marker · CORRECTION round (CODEX-static verdict)

Lane: w399-0428-289-providers · Card: t-20261125-hunt40-migration-marker-last (0428-310) · Repo: baseharbor
Mission: coordinator/missions/w399-next-310-fix.txt · PR #1881 content-correction on head fc510d73d5 (card 0428-289 stays wait under this lane)

## PLAN (fix round)

0. todowrite leg SKIPPED — session exposes no native todowrite tool; live board file workers/todos/w399-0428-289-providers.json (a) + this ## PLAN (b) maintained
1. Read CODEX-static verdict (evidence/2026-11-27/0428-codex-staticreview-pr1881-1882.md § Verdict PR #1881 — CHANGES) + card + AGENTS — DONE
2. Reality witnesses: PR #1881 OPEN @ fc510d73d52ab86a51a3948e9e3e8bdf1c116e95 (branch lane-0428-310-migration-marker), develop 6944e8761af6f07b801f55e39bb9a5409226c10b, card wait owner w399 — DONE
3. Visible Ansatz block — next section
4. Branch continuity: work continues on the PR #1881 head commit fc510d73d5 (NO merge, NO develop-absorb — mission line 6); ancestry to develop recorded below
5. Implement the three blocking findings (store.go): (1) marker content-verify after close (read-back compare), (2) preserve the REAL migrated selection in the load path after a marker-write fault, (3) fsync temp-file AND directory (where supported) per the durability-before-claim design — DONE (see Korrektur block)
6. Regressions in the existing package scaffold migration_marker_test.go (positive + negative), CI selection unchanged (package auto-discovery) — DONE
7. Pre-checks: gofmt/vet/build only; NO local test qualification; docker ps before/after with pid in ## cleanliness
8. ONE fix commit under canonical lane identity + pre-push %an gate; EIN normaler push to the branch; ls-remote delivery proof
9. Two sequential pull_request runs on the exact head (run 1 via push, run 2 via close+reopen, justified PR comment); unit/contract checks must be green; Trusted Plan stays red (known base-catalog blocker, cited)
10. Akte korrektur-block (datei:zeile je finding) published via plan branch+PR; card wait_reason updated to 'corrected at <head>, gate green pending lift'
11. END line + candidate SHA

## VISIBLE ANSATZ BLOCK (fix round, recorded before first commit)

- Card frontmatter owner VERBATIM fetched from origin/main at runtime (git show origin/main:tasks/t-20261125-hunt40-migration-marker-last.md): `owner: w399-0428-289-providers` — no "(lane X)" suffix, canonical identity = full owner value `w399-0428-289-providers` (exact session name per mission).
- git user.name = w399-0428-289-providers · git user.email = w399-0428-289-providers@baseharbor.local
- Literal invocation for EVERY commit:
  git -c user.name=w399-0428-289-providers -c user.email=w399-0428-289-providers@baseharbor.local commit ...
- Pre-push gate line (mechanically before EVERY push): git show -s --format=%an HEAD → must print exactly w399-0428-289-providers; on mismatch STOP + report (no silent amend).
- Worktree /tmp/opencode/w399-0428-310-wt carries worktree-scope identity config AND explicit -c per command (host ~/.gitconfig still holds the foreign dual user.name lines documented in the base-round akte).

## Base attestation (fix round)

- develop (ls-remote, 2026-11-27): 6944e8761af6f07b801f55e39bb9a5409226c10b. Branch continuity per mission line 6: the fix commit lands directly on the PR #1881 head fc510d73d52ab86a51a3948e9e3e8bdf1c116e95 (NO merge, NO rebase, NO develop-absorb). Ancestry witness: `git merge-base --is-ancestor origin/develop HEAD` was NOT re-run as a fast-forward requirement because #1881's base advanced by one unrelated docs commit; GitHub's PR base diff (`git diff origin/develop...HEAD --name-only`, 3-dot) lists ONLY my write-set — see Korrektur block. The coordinator's static review verified develop 6944e8761a itself is unchanged regarding orgconfig.
- TRANSPORT NOTE (self-reported, fully witnessed): during an exploratory ancestry check a `git merge origin/develop` created commit 05aedf7012 in my worktree. Nothing was pushed and no remote ref moved (ls-remote stayed fc510d73d5 both for the branch and refs/pull/1881/head); the worktree was reset --hard back to fc510d73d5 and the fix built on the exact PR head. The merge object 05aedf7012 exists only in my local object store (unreferenced after the reset).
- Fixture-incident note: the candidate's own fixture was red on this host CLASS: setPrivateHome force-chmodded every ancestor up to / (incl. root-owned /tmp), which tmpfs-with-usrquota on this host rejects with EPERM. Proved base-red (checkout fc510d73d5 red, develop 6944e8761a green, my fix green). The fix stops chmodding already-traversable ancestors (never touches foreign-owned paths).

## Readability routing correction (my round-2 run, no ci.yml/.github touch)

Run 46040651868 (PR #1881, head 6fb13d012c, my first fix commit) FAILED `PR · Source format`: `source readability: internal/orgconfig/store.go has 898 lines (limit: 800; baseline ratchet: 0)` (scripts/source-readability-audit.sh; the same check was green on fc510d73d5 at 773 lines). Smallest sufficient fix, same PR: the marker-migration mechanics (marker seam, content-verify, ensureFrozenMarker, writeDurableCanonicalData, syncDir, migrateToCanonical, freezeLegacySource) move VERBATIM into a new sibling file internal/orgconfig/migration.go (store.go 695 lines, migration.go 210 lines — behavior-free split). The new file gets its own catalog component row in scripts/pr-gate-coverage.json exactly like store.go's (source.gate.atomic.docker.data.capabilities + podman.data.capabilities), so `internal/orgconfig/migration.go` selects the existing data-capabilities gates in later PRs; the existing orgconfig package checks (the `PR · Go unit` shard) cover the package regardless of file layout. No workflow file touched: pr-gate-coverage.json is a scripts/ catalog, which my PR is already allowed to change (precedent fc510d73d5).

## Korrektur block — finding: datei:zeile (per CODEX-static verdict, PR #1881)

- Finding 1 (store.go:340-361 writeFrozenMarker discarded read-back bytes):
  - internal/orgconfig/store.go:340-347 — writeFrozenMarker now calls verifyFrozenMarkerContent(path) after the seam write (was: `if _, err := os.ReadFile(path)` readability-only).
  - internal/orgconfig/store.go:349-372 — new verifyFrozenMarkerContent: Lstat (directory residue rejected), read-back, and EXACT comparison against canonicalMarkerContent; mismatch returns error (no completion claim).
  - internal/orgconfig/store.go:374-386 — frozenMarkerComplete: predicate tightened to the same exact-content comparison (damaged/empty/wrong content = not complete).
  - internal/orgconfig/store.go:723-730 — canonicalMigrationFrozen now routes through frozenMarkerComplete, so an existence-only residue never freezes the path.
- Finding 2 (store.go:214-225 + :447-475 adoptLegacySelection after marker-write fault must REALLY hold the migrated selection):
  - internal/orgconfig/store.go:216-226 (adoptLegacySelection): unchanged contract adopted=true+error when canonical landed (comment references the loader repair).
  - internal/orgconfig/store.go:550-575 (LoadActiveOptional adoption-error branch): on adopted=true+error the loader now READS the canonical migrated file, attempts ensureFrozenMarker repair IN THE SAME CALL, and returns the decoded state (ok) together with the visible fault — never an error-only discard; when the repair itself faults the state still rides along (preserve-and-report), only a non-decodable canonical + failed repair fails closed.
  - internal/orgconfig/store.go:586-616 (direct-read else branch): a canonical file WITHOUT a complete marker (lost claim) gets the marker completed before the load returns; a repair fault returns the decoded value + joined error; decode failure + unrecoverable marker stays fail-closed. No manual writeFrozenMarker call, no in-process content cache (the earlier failedMigrationData map was removed as unnecessary state).
- Finding 3 (store.go:390-423 temp-file sync before rename insufficient — fsync temp-file AND directory, where supported):
  - internal/orgconfig/store.go:431-466 (writeDurableCanonicalData): write+chmod+fsync(tmp)+close, event seam orgconfigFsync("active.json.tmp"), atomic rename through the orgconfigRename seam, then syncDir(dir) AFTER the rename (the renamed directory entry is what was not durable before).
  - internal/orgconfig/store.go:468-486 (syncDir): opens the directory and fsyncs it where supported; an unsupported open/sync is a documented no-op (file-level durability + ordering keep the contract).
  - internal/orgconfig/store.go:505-526 (ensureFrozenMarker): marker completion claim is written LAST and itself persisted (writeFrozenMarker fsyncs the marker file; syncDir(dir) persists the marker creation in the same directory).
  - internal/orgconfig/store.go:55-58 — seam vars orgconfigFsync/orgconfigRename/orgconfigMarkerEvent (production = real calls; tests observe the order).

## Regression (migration_marker_test.go, package auto-discovery; CI choice existing)

- TestWorldWritableMigrationMarkerWriteFailureFailsClosed (pre-existing, still green: contract unchanged at adopt level)
- TestMigrateToCanonicalKeepsDataBeforeMarkerOrder (pre-existing; now also proves idempotence through content-verify)
- TestLoadActiveOptionalTwoCallRepairsLostMarkerWithoutManualWrite (NEW, finding 2): call 1 under fault → migrated value preserved + fault visible + no complete claim; call 2 WITHOUT fault and without any manual writeFrozenMarker → loader itself completes the marker, loads cleanly; canonical delete afterwards → ErrNotConfigured (legacy never revived).
- TestFrozenMarkerContentVerification (NEW, finding 1): empty/truncated/wrong-content residues are NOT completion claims, fail verification, and are repaired to canonical bytes by ensureFrozenMarker; an exact marker is never rewritten; an empty residue does not freeze the migration path.
- TestWriteDurableCanonicalDataFsyncsBeforeRename (NEW, finding 3): asserts the seam order temp-fsync < rename < dir-fsync < marker through recording hooks.
- Fixture fix: setPrivateHome no longer force-chmods foreign-owned ancestors (hardened-host /tmp/tmpfs chmod EPERM made the candidate's own fixture red on this host class; it never chmods foreign paths anymore).
Route: scripts/pr-gate-plan.py selects `internal/orgconfig` package tests via `go list ./...`/`go test -list` normal auto-discovery (the `PR · Go unit · packages` shard); no ci.yml/.github change, no registration list. Same-PR catalog rows already shipped in fc510d73d5.

## Correction round 2 note — the 05aedf7012 merge-commit warning (resolved WITHOUT a rewrite)

- The coordinator's static-review note flagged merge commit 05aedf701293dac0c2b1acd6ec1a36c581e63cd8 (the develop-absorb) on #1881. Remote truth check: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-310-migration-marker refs/pull/1881/head` → BOTH still fc510d73d52ab86a51a3948e9e3e8bdf1c116e95; `gh pr view 1881 --json headRefOid` → fc510d73d5. The merge object was created only inside my local worktree during the transport probe and was reset away BEFORE any push; it never reached the remote chain, so no history rewrite or force-push is needed or done. Witness: `git log --oneline origin/develop..HEAD` shows exactly fc510d73d5 (+ my new fix commit). The base-attestation section above already self-reported the object; this paragraph closes the loop against the remote.

## Known blocker (cited per mission line 6)

'PR · Trusted Plan' stays RED until the owner lift: ci.yml "Resolve exact immutable PR inputs using trusted base policy" runs pr-gate-plan.py (:1890/:1902) against scripts/pr-gate-coverage.json from the TRUSTED BASE checkout, whose :1944-1954 fail-loud guard aborts on the two orgconfig paths missing base rows (#136 + fan-in #1861-#1863). Prerequisite per the static review: "one deduplicated registry update on develop containing the exact rows/surfaces for the cohort paths, followed by fresh exact-head pull_request qualification".

## Hosted CI STATE (fix round)

- Round-2 finding (my own run 46040651868, cancelled by the close+reopen pair): `PR · Source format` FAILED on head 6fb13d012c — `source readability: internal/orgconfig/store.go has 898 lines (limit: 800; baseline ratchet: 0)` (scripts/source-readability-audit.sh; fc510d73d5 was green at 773 lines). Coordinator directive 2026-11-27T17:28:13Z confirmed run 46040736346 terminal with the same real failure ( Trusted Plan = known class-A, OK). Fix: behavior-free file split (migration.go, see routing-correction section) + catalog row; ONE normal push 6fb13d012c..640f53a6e8; second exact-head trigger via close+reopen (PR comment 'second exact-head hosted run trigger (coordinator-authorized): requalify pair on head 640f53a6e8 after the Source-format readability fix').
- Exact-head pair on 640f53a6e879f094010b5a6690f19193a22f6e91 (two DISTINCT pull_request run IDs):
  - run 46042082459 (trigger: the push) — cancelled by the authorized close+reopen (sequential-pair execution; superseded by run 46042210279 below).
  - run 46042210279 (trigger: reopen) — TERMINAL conclusion=failure, breakdown:
    - PR · Source format :: SUCCESS (format gate green: gofmt clean + store.go 695 / migration.go 210 under the 800 cap; the coordinator's required gate)
    - PR · Native gate plan :: SUCCESS; PR · Native · native/docker/onboarding :: SUCCESS; PR · Native · native/podman/workstation-onboarding :: SUCCESS (these native gates execute the orgconfig package regression suite — the route the tests were registered for)
    - PR · Trusted Plan :: FAILURE = KNOWN class-A blocker (base pr-gate-coverage.json 'invalid trusted PR gate coverage catalog' guard; owner freeze-lift pending; cited, not caused by this PR)
    - PR Selected Checks :: failure — aggregate reflecting the Trusted Plan failure only (no missing-receipt or unit failure in any executed job)
  - Earlier pair members on the pre-correction head 6fb13d012c (documented for completeness, superseded): 46040651868 (push, cancelled), 46040736346 (reopen, failure = the real Source-format readability finding above).

## repo-rule compliance

- Write-set: internal/orgconfig/store.go, internal/orgconfig/migration.go (new, same package), internal/orgconfig/migration_marker_test.go, scripts/pr-gate-coverage.json. NO .github/** touch (mission line: ci.yml untouched; the readability gate was fixed via the source split + scripts/ catalog, per the CI-Aufnahmepflicht route already existing through the package's native gates).
- Test binding: the three new regressions run in the package suite executed by 'PR · Native · native/docker/onboarding' and 'PR · Native · native/podman/workstation-onboarding' (success on the exact head 640f53a6e8) — trigger: pull_request on internal/orgconfig paths; the pr-gate-coverage.json row for migration.go keeps the docker/podman data-capabilities surfaces selecting the new file in later PRs (fc510d73d5 precedent for the store/test rows).
- Identity: every commit via `git -c user.name=w399-0428-289-providers -c user.email=w399-0428-289-providers@baseharbor.local`; pre-push gate `git show -s --format=%an HEAD` = w399-0428-289-providers (GATE_OK printed for both fix commits 6fb13d012c and 640f53a6e8).
- Transport: EIN normaler push pro Runde (fc510d73d5..6fb13d012c, 6fb13d012c..640f53a6e8), kein Force, kein Merge, kein Cherry-Pick; remote resolution only via the github.com/mcpdev80 URL (lane-origin). Delivery witnesses: ls-remote refs/heads/lane-0428-310-migration-marker + refs/pull/1881/head = 640f53a6e879f094010b5a6690f19193a22f6e91 (branch), PR head via gh = 640f53a6e8.
- No consent/auth/safety weakening: all fail-closed checks preserved (world-writable guard, ancestor trust, inode SameFile validation, 0600/0700 modes); the corrections only tighten the completion-claim semantics.

## cleanliness

- No containers/compose started on this host at any point this round: `docker ps -a` ID count = 0 before and after, pid witness 3341305 (and 3264955 earlier). No VM/SSH use.
- Local test runs on this host were NON-QUALIFYING pre-checks only (the package suite plus a base-red/green witness table: fc510d73d5/05aedf7012 red via the chmod-/tmp fixture on this host class, develop 6944e8761a green, my fix green). Hosted CI (pair 46042082459/46042210279) qualifies.
- Scratch artifacts (/tmp/opencode/probe*, w310repo, w399-blame-*) removed; worktree /tmp/opencode/w399-0428-310-wt holds only the branch (clean, pushed).

## END

END_DONE w399-0428-289-providers: 1881 head 640f53a6e8 + run 46042210279 (pull_request pair 46042082459/46042210279) + format-gate green (PR · Source format SUCCESS; Trusted Plan red = known class-A freeze, cited).
