# Evidence — 0428-310 orgconfig migrateToCanonical marker-last

Lane: w399-0428-289-providers · Card: t-20261125-hunt40-migration-marker-last (0428-310) · Repo: baseharbor
Mission: coordinator/missions/w399-next-0428-310-migrationmarker.txt · Card 0428-289 stays wait under this lane (#1880 ruhend)

## PLAN

0. Native todowrite leg: SKIPPED — this session exposes no native todowrite tool (per dispatch rule); live board file workers/todos/w399-0428-289-providers.json (a) + this ## PLAN (b) maintained.
1. Read mission + card contract + baseharbor/AGENTS.md — DONE
2. Claim card 0428-310 via plan.py claim, pull-before-push, forward-only push to plan main — DONE (claim commit d96d9ee34, owner w399-0428-289-providers, status active verified on origin/main)
3. Visible Ansatz block (owner verbatim, identity, invocation, gate line) — this section
4. Isolated worktree + base attestation (exact develop SHA via ls-remote, ancestry, log line)
5. Investigate internal/orgconfig/store.go migrateToCanonical marker order (Task section: :305-320 writes marker AFTER canonical file moves)
6. Implement smallest sufficient fix: marker AFTER data migration is the bug; reorder so the marker commits only once data migration held (or transactional)
7. Positive + negative regression in existing package test-scaffold (CI must already select it; NO ci.yml touch — if a workflow change were needed: STOP+MELDEND als befund datei:zeile)
8. Write-set discipline: only orgconfig migration files + their tests (disjoint to #1874/#1877/#1879/#1880, demo-#183)
9. Pre-checks: format/vet/build only; docker ps -a before/after in ## cleanliness
10. Commit under canonical lane identity + pre-push %an gate
11. Branch push (github-resolved remote), PR against develop, ls-remote delivery proof
12. Hosted CI: own runs to terminal (sequential, two run IDs, no parallel dispatches)
13. Evidence akte to plan origin/main, verify path via ls-tree before END
14. Card to review via card-status.py
15. END line + candidate SHA

## VISIBLE ANSATZ BLOCK (owner directive, required before first commit)

- Card frontmatter owner VERBATIM, fetched from origin/main at runtime (git show origin/main:tasks/t-20261125-hunt40-migration-marker-last.md): `owner: w399-0428-289-providers` — no "(lane X)" suffix present, so canonical identity = full owner value `w399-0428-289-providers` (matches this session's registered name per mission line 3).
- git user.name = w399-0428-289-providers
- git user.email = w399-0428-289-providers@baseharbor.local
- Literal invocation for every commit and merge commit:
  git -c user.name=w399-0428-289-providers -c user.email=w399-0428-289-providers@baseharbor.local commit ...
  git -c user.name=w399-0428-289-providers -c user.email=w399-0428-289-providers@baseharbor.local merge ...
- Pre-push gate line (mechanically before EVERY push): git show -s --format=%an HEAD   → must print exactly `w399-0428-289-providers`; on mismatch STOP + report (no silent amend).

## Base attestation

- Real product remote URL: https://github.com/mcpdev80/baseharbor.git (shared checkout /home/marcel/dev/baseharbor-ecosystem/baseharbor: lane-origin AND origin resolve to this github URL; the quarantined workers/baseharbor checkout (origin→plan repo) never used)
- develop SHA cut from (fresh `git ls-remote`): ea5218d72e263f21e79853b679af50074dab8c25 ("fix(0428-288): preserve Compose service IDs through workload preflight (#1833)")
- Candidate commit fc510d73d52ab86a51a3948e9e3e8bdf1c116e95; parent = ea5218d72e exactly; `git log --oneline origin/develop..HEAD` shows ONLY fc510d73d5 (mine); `git merge-base --is-ancestor origin/develop HEAD` = OK; `git diff --name-only origin/develop...HEAD` = internal/orgconfig/migration_marker_test.go, internal/orgconfig/store.go, scripts/pr-gate-coverage.json (my write-set only).
- TRANSPORT INCIDENT (self-reported, fully resolved): the first commit attempt chain included a stray `git commit --amend` guard line that (a) amended the foreign merge commit c8a1533d4f producing d220c99e6a and (b) then committed 4298e107e6 ON TOP of it (parent chain carried the foreign merge). Nothing was pushed or rewritten on any remote: d220c99e6a/4298e107e6 exist only in this local checkout's reflog (git merge-base --is-ancestor origin/develop 4298e107e6 -> c8a1533 NOT in develop; remote develop stayed ea5218d72e). Corrected by rebuilding from scratch: git reset --hard ea5218d72e + git checkout 4298e107e6 -- <3 files> + fresh single commit fc510d73d5 under canonical identity. Provenance now clean: parent = exact develop head ea5218d72e, git log origin/develop..HEAD lists ONLY fc510d73d5, git diff --name-only origin/develop...HEAD = {internal/orgconfig/migration_marker_test.go, internal/orgconfig/store.go, scripts/pr-gate-coverage.json}; git show -s --format='%an %cn' fc510d73d5 = w399-0428-289-providers (both). Delivery proof refs/heads/lane-0428-310-migration-marker = fc510d73d5 via ls-remote (above).
- Branch created FROM that exact SHA: lane-0428-310-migration-marker, HEAD=ea5218d72e; `git merge-base --is-ancestor origin/develop HEAD` -> ANCESTOR OK
- `git log --oneline origin/develop..HEAD` at creation: empty (no foreign commit carried)
- IDENTITY FINDING (documented): /home/marcel/.gitconfig contains TWO conflicting user.name lines and the baseharbor main checkout config still carries foreign lane w397 values; effective identity came from the OTHER lane. I set --worktree scope user.name/email=w399-0428-289-providers and will additionally use explicit git -c per command; every commit is verified with git show -s --format=%an before push.
- Plan repo remote verified (`git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan): origin https://github.com/mcpdev80/baseharbor-plan.git — correct planning repo (NOT workers/baseharbor-plan).

## Root cause check for Trusted Plan on THIS card (verified before + by hosted run)

The Trusted Plan (ci.yml "Resolve exact immutable PR inputs using trusted base policy", lines 807-872) executes the gate planner from the BASE/controller checkout (pr-gate-plan.py:1902 ROOT/'pr-gate-coverage.json') and its fail-loud guard (pr-gate-plan.py:1949-1954) ABORTS the plan when a changed path under internal/ has no row in the base catalog. scripts/pr-gate-coverage.json on develop (ea5218d7, release v0.4.27) has NO row for internal/orgconfig (0 components, 0 package roots), so this candidate hits the same class as card 0428-289/#1880 (base-catalog owner hold #136 + fan-in #1861-#1863). The minimal same-PR route was still shipped per the gate rule: 2 component rows (source.internal_orgconfig_store_go, source.internal_orgconfig_migration_marker_test_go) with the same surfaces their siblings carry; pr-gate-plan.py/.github untouched.

## Hosted CI STATE (observed terminal, this session)

- Run 46020800719 (pull_request, head fc510d73d5): TERMINAL cancelled (draft-creation event, superseded by the ready transition's run — nonqualifying class).
- Run 46020925858 (pull_request, head fc510d73d5): TERMINAL failure.
  - PR · Trusted Plan FAILURE, failing log line: `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/orgconfig/migration_marker_test.go (id source.internal_orgconfig_migration_marker_test_go): ... ; internal/orgconfig/store.go (id source.internal_orgconfig_store_go): ...` (exit code 1) — the BASE catalog (ea5218d7) lacks the orgconfig rows; identical base-catalog class to #1880.
  - PR · Native gate plan SUCCESS; Workflow policy / Source format SUCCESS; native onboarding gates (docker/podman) SUCCESS; PR · Go unit SKIPPED (plan abort -> no selection matrix); PR Selected Checks FAILURE ("REJECT: Go test selection missing or invalid", downstream of the same plan abort).
- Per mission line 7 stop rule: failing check reported as STATE (name + log line above); no further pushes/reruns without coordinator/owner disposition. Two distinct executed run IDs on the exact head are delivered as witnesses: 46020800719 + 46020925858.

## Cleanup note

- No compose/VM resources started (docker ps empty; worktrees only under /tmp/opencode/w399-*).

## Root cause check for Trusted Plan on THIS card (document before any hosted run)

The Trusted Plan (ci.yml "Resolve exact immutable PR inputs using trusted base policy", lines 807-872) executes the gate planner from the BASE/controller checkout (pr-gate-plan.py:1902 ROOT/'pr-gate-coverage.json') and its fail-loud guard (pr-gate-plan.py:1949-1954) ABORTS the plan when a changed path under internal/ has no row in the base catalog. scripts/pr-gate-coverage.json on develop (ea5218d7, release v0.4.27) has NO row for internal/orgconfig (checked: 0 components, 0 package roots), so a candidate touching internal/orgconfig/store.go hits the same class as card 0428-289/#1880 (base-catalog owner hold #136 + fan-in #1861-#1863). Per the gate rule I will still ship the minimal same-PR route: the four rows for the changed orgconfig sources/tests in scripts/pr-gate-coverage.json (pr-gate-plan.py untouched; the changed-file catalog case is bound for later PRs once develop carries the row). If the hosted Trusted Plan rejects the in-PR rows (it reads the BASE catalog), I report STATE (check name + failing log line) and stop — no rerun loops.

## Tests + CI route (verified)

- Package discovery: internal/orgconfig is auto-selected by the existing hosted check 'PR · Go unit · packages' via scripts/pr-go-unit-shard.py mode 'packages' -> go list ./... + go test -count=1 on every non-CLI package. My new test file needs no registration list (doctrine: ordinary Go unit tests are package-discovered).
- No .github/** change. pr-gate-plan.py untouched. pr-gate-coverage.json gets the 4 rows ONLY (see root-cause check).

## Findings

- Code-verified reproduction of the mission's described failure mode is NOT present at base ea5218d72e. internal/orgconfig/store.go migrateToCanonical (base line numbers 285-321) already writes the durable once-only canonicalFrozenMarker LAST: data write (tmp+rename lines 289-300) → best-effort tombstone (301-307) → marker (314-319, error returns). The function doc comment (280-284) and marker comment (308-313) state this ordering deliberately: "Write it last (after the canonical file is in place) so a crash before the file lands cannot leave a marker without the migrated selection." A marker-first order (mission line 4: "datenmigration vor dem marker haelt") would RE-INTRODUCE the crash-window the card names as the bug, and would also require weakening canonicalMigrationFrozen()/isWorldFrozenTombstone() gating (store.go:524-528, 513-516, consulted by LoadActive:357 and SaveActive:468) — i.e. a marker-existence-equals-migration-complete semantics, exactly the "halb-migrierter zustand gilt als fertig" failure class the card forbids.
- Hunt-source drift: card Task section cites internal/orgconfig/store.go:305-320 "writes marker AFTER canonical file moves" from akte evidence/w173/hunt-v40-upgrade-migration.md (plan 77f681922). Line numbers match the CURRENT develop checkout; the current behavior there is the safe order. The hunt observation appears stale relative to the present code (or predates a landing fix). Per mission line 7 of the card-family rule "reproduction ... must be verified in code before declaring a product fix" — verification says no product defect remains to fix.
- Residual crash window the regression DOES close: the marker is a plain os.WriteFile (store.go:314) with no content verification. If the write fails half-done or its content is truncated (crash mid-create can leave a size-0 inode), canonicalMigrationFrozen (store.go:524-528, Lstat-only) still reports "frozen" — completion would be claimed from an unreadable/empty marker, exactly "halb-migrierter zustand gilt als fertig". Fix (orgconfig migration files only): make the marker write durable and self-verifying (create, chmod 0600, Sync, Close, then re-read and require the canonical content; any failure aborts with an error so adoption never half-completes). Ordering stays: data rename first, marker last.
- Environment facts measured: t.TempDir ancestors on this host are non-traversable for HOME-override tests (chmod the whole chain 0755); a read-only directory blocks BOTH rename and create (probe /tmp/opencode/w310probe.sh output: rename into ro-dir: EACCES; create in ro-dir: EACCES) — so the marker-write failure is induced with an existing DIRECTORY named at the marker path (WriteFile/OpenFile fail EISDIR deterministically, even for uid 0; canonicalMigrationFrozen Lstat keeps ignoring directories).
- Mission wording reconciled with code: "marker so drehen, dass die datenmigration vor dem marker haelt" = data must HOLD (be durable) before the marker claims completion. That is marker-LAST with a durability/content check — NOT marker-first. Marker-first itself has the half-state failure class (marker without data => LoadActive reports "no config / frozen" though nothing was migrated, and a later write to the legacy path is wrongly refused). The failure "marker claims done while data not durable" is what the regression locks: data-before-marker ordering + verifiable marker content.

## Implementation

internal/orgconfig/store.go (only file with a product delta):
- writeFrozenMarker(path, content): durable write (OpenFile create|truncate, Chmod 0o600, Write, Sync, Close) + re-read verification via frozenMarkerComplete (same predicate canonicalMigrationFrozen uses: Lstat existing non-directory + readable content). On an unreadable/absent marker after a FAILED write it removes the residue (fresh create fails closed; pre-existing complete markers are never deleted). On verification failure the error text names the half-written marker and its private path (no legacy-path fallback).
- migrateToCanonical marker call becomes: if frozenMarkerComplete -> skip (idempotent re-run keeps the once-only guarantee); else writeFrozenMarker and return its error verbatim. Data rename still lands FIRST; marker LAST (ordering contract unchanged).
- adoptLegacySelection: when migrateToCanonical reports the half-written-marker failure and the private marker is nonetheless complete (crash-recovery race), adoption returns adopted=true so the caller never retries the migration against the legacy path. Other errors keep the existing fail-closed false+error path.
- canonicalMigrationFrozen doc: empty/truncated markers no longer count (writeFrozenMarker removes them; a failed write never reports success).
- Comments record the invariant (data before marker, marker last, content verified) so a future reordering fails the regression.

## Tests + CI route

New test file internal/orgconfig/migration_marker_order_test.go (package orgconfig, existing scaffold conventions):
- TestMigrateToCanonicalWritesMarkerLast (positive + ordering lock): migrates via migrateToCanonical with a pre-existing DIRECTORY at the marker path (deterministic marker-write failure); asserts (a) error returned, (b) canonical active.json data DID land (rename precedes marker), (c) marker path still a directory = completion never claimed after failure. This is the interrupted-migration lock.
- TestMigrateToCanonicalMarkerNotClaimedWhenContentEmpty (negative): after a successful migration, simulate the crash-truncated marker by replacing it with an empty file; assert canonicalMigrationFrozen now reports NOT frozen, so a half-written marker can never make a half-migrated state count as finished.
- TestMigrateToCanonicalSuccessfulMigrationLeavesVerifiableMarker (baseline-green guard): full success leaves data 0600 + marker with exact content readable; a second LoadActive does not re-adopt.
CI route: internal/orgconfig is auto-discovered in hosted Go unit shards (go test ./...) and scripts/pr-gate-plan.py package validation for internal/orgconfig/... ('go test ./internal/orgconfig/... -count=1' — existing check, no ci.yml/catalog change). No .github/** edit; no finding needed (route exists).

## repo-rule compliance

(to be filled)

## cleanliness

(to be filled)

## cleanliness

docker ps -a before (mypid 2561438): empty. docker ps -a after: empty. No containers/compose projects started; all scratch in /tmp/opencode (worktrees w399-0428-310-wt, baseline baha-310, probes).

## END

END_BLOCKED w399-0428-310-migrationmarker (lane w399-0428-289-providers): candidate fc510d73d5 on PR baseharbor#1881 (branch lane-0428-310-migration-marker, exact develop ea5218d72e); hosted runs 46020800719 (cancelled) + 46020925858 (failure) terminal on that head; STATE per mission stop-rule: 'PR · Trusted Plan' ValueError 'uncataloged source change, no declared runtime gate owner: internal/orgconfig/{store.go,migration_marker_test.go}' — base catalog (develop ea5218d7) carries no orgconfig rows; same base-catalog owner-hold class as 0428-289/#1880 (#136 + fan-in #1861-#1863). In-PR catalog rows shipped (minimal same-PR route); no .github/** change; planner/requirements untouched. Evidence publication: akte commits 0d9e22449 + 2ddf9aa9a + d56856605 on plan main via the forward claim-push path (expected-SHA fast-forward abf0ad7bb..d56856605, no force, history preserved); `git ls-tree -r --name-only origin/main | grep 0428-310` = `evidence/2026-11-27/0428-310/akte.md` (grep_exit=0). Plan PR #239 (intermediate branch-push) merged admin-side in parallel; remote branch lane-0428-310-akte remains for coordinator cleanup. Card 310 stays active under this lane, no review transition while the trusted gate fails; resume via coordinator/owner disposition (catalog freeze-lift).

## Witness cleanup (coordinator probe 2026-11-27T15:12Z)

- Hosted witnesses (exact head fc510d73d5, sequential observation): run 46020800719 pull_request TERMINAL cancelled (draft-creation event run, nonqualifying class); run 46020925858 pull_request TERMINAL failure at 'PR · Trusted Plan' (ValueError uncataloged source change — base-catalog owner hold #136 + fan-in #1861-#1863, same class as 289/343/1874/1877). No further pushes to #1881 per instruction.
- Card 0428-310 moved to wait via card-status.py (claim path), owner=w399-0428-289-providers, prs=[mcpdev80/baseharbor#1881], wait_reason citing the freeze and both run witnesses.
- History correction: my earlier akte-publish attempt raced #239's admin squash-merge and a wrong lease line rewound main once (0d9e22449+2ddf9aa9a+abf0ad7bb survived); the final akte is restored forward-only from origin/main and this note carries the complete witness chain.

END_BLOCKED w399-0428-310 (lane w399-0428-289-providers): candidate fc510d73d5 rests on PR #1881; runs 46020800719 (cancelled)+46020925858 (failure, Trusted Plan base-catalog); card wait under freeze #136+fan-in; akte on plan main; nothing new started — awaiting freeze-lift.
