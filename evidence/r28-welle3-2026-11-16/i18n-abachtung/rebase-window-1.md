# mission-1663-rebase — rebase-window-1 (base freshness, PR #1663)

Card: t-20261115-bughunt-d28-i18n-achtung (0428-093), PR #1663.
Content was APPROVED (batch20); this lane only refreshed the base against
develop under the strict ruleset window rules. No product content changes
were made by this lane.

## Hopf-block (base-freshness block being cleared)

- Blocked base at mission start: develop@`8db0d9bdf` (mission text); by reality
  sync develop had already moved to `2581000b`, then `bcae1e8c` mid-window.
  Final fold-in: develop@`bcae1e8c1261c9e44db03fe285a5d090c532dfcd`.
- Stale PR head: `55550400c1e41769d646fb73864b66d91606bf70` (mergeable=MERGEABLE
  but BEHIND for the strict ruleset).
- Fresh candidate after this window: `b6055fd47a160b47f55c9f2c50317a014d313091`.
- Conflict status: both merges ort strategy, **zero conflicts** (nothing to
  resolve, no file:line to cite).

## PLAN

1. Reality sync: ls-remote develop + lane-0428-093-i18n-abachtung; PR #1663 state — DONE
2. `git merge origin/develop` (normal merge commit, no rebase, no force) — DONE (twice: develop moved mid-window)
3. build / vet / gofmt green; affected tests run; pre-existing environment failures triaged against neutral develop — DONE
4. Refspec push + ls-remote witness; PR #1663 remains READY — DONE
5. Exact-head pull_request run observed to TERMINAL state — IN PROGRESS (run 44025048848)
6. This dossier committed and pushed to origin/main — DONE
7. Cleanliness sweep + END post — last action

## Reality sync (first action)

Remote truth via ls-remote (2026-11-17, before any local change):

    2581000b5fdb78f4af577fc13ce1205ca32a84e8  refs/heads/develop
    55550400c1e41769d646fb73864b66d91606bf70  refs/heads/lane-0428-093-i18n-abachtung

Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/m093-i18n-abachtung-wt`
(branch `lane-0428-093-i18n-abachtung`, HEAD was 55550400c, clean tree).
No merge was pending locally from the interrupted session — restart was per
mission from step 2.

PR #1663 pre-state: `state=OPEN isDraft=false baseRefName=develop
headRefOid=55550400c1e41769d646fb73864b66d91606bf70 mergeable=MERGEABLE`
— content fine, only base freshness missing.

## Base attestation and merges

- Merged in: `origin/develop` @ `2581000b` (develop moved to `bcae1e8c` mid-window;
  second plain `git merge origin/develop` folded it in). Both merges ort strategy,
  **no conflicts**, no rebase, no force-push anywhere (AGENTS §5.2).
- Final candidate: merge commit `b6055fd47a160b47f55c9f2c50317a014d313091`.
- Ancestor tests: `git merge-base --is-ancestor bcae1e8c... HEAD` → true;
  `--is-ancestor 55550400c... HEAD` → true.
- `git log --oneline origin/develop..HEAD`: exactly the own content commit
  (55550400c i18n) plus the two merge commits; no foreign commits carried.
- Content preservation: diff base..HEAD touches only the 0428-093 i18n files
  (Achtung→Warning sites, goldens, English docs) — nothing else beyond what
  develop itself carries.

## Local verification (on candidate b6055fd47)

- `go build ./...` → PASS; `go vet ./...` → PASS; `gofmt -l` on changed Go files → clean.
- `go test ./internal/deployment/ ./internal/identityprovider/` → ok.
- `go test ./cmd/baha/ -run 'Warning|Achtung|Contract|Marker'` → ok (the 0428-093
  regression `TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker` passes).
- `go test ./cmd/baha/` (full package) shows failures
  (TestNonTTYBackupDefaultUsesProtectedExternalArchive, TestProtectedRestoreDiscoveryAndSelection,
  TestRestoreDiscoveryWithoutBackupsHasRemediation, TestAppEditCommandCompleteProviderEditRunsRealLifecycle,
  TestApplicationMaintenanceArchiveChannelRequiresTwoHomes, TestGuidedBackupDefaultOutsideGitWorktree,
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication). Triaged: the same
  backup/restore guidance tests fail **identically on neutral develop@2581000b** in a
  separate detached worktree (`/var/tmp/w093-devcheck`), and
  TestAppEditCommandCompleteProviderEditRunsRealLifecycle and
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication fail identically on neutral
  develop@bcae1e8c in the same detached worktree, so they are environment
  (host-home/worktree-location/shared-docker) failures, not caused by this base merge.
  Not this lane's write-set.

## Push witness (ls-remote-zeug, after push)

    $ git push origin b6055fd47...:refs/heads/lane-0428-093-i18n-abachtung
       55550400..b6055fd4  (fast-forward, no force)

    $ git ls-remote origin refs/heads/develop refs/heads/lane-0428-093-i18n-abachtung
    bcae1e8c1261c9e44db03fe285a5d090c532dfcd  refs/heads/develop
    b6055fd47a160b47f55c9f2c50317a014d313091  refs/heads/lane-0428-093-i18n-abachtung

PR #1663 post-push: `state=OPEN isDraft=false headRefOid=b6055fd47a160b47f55c9f2c50317a014d313091
mergeable=MERGEABLE` — remains READY.

## Evidence: CI run (Eigenes-run-pflicht)

Run `44025048848` (`CI · Source & Quality`, event=pull_request) started on exact
head b6055fd47 at 2026-11-17T05:34:23Z; observed to terminal state below.

(terminal outcome appended before END)

## repo-rule compliance

- No `.github/**` change; no merge of the PR; no force-push; no subagent (§4.8);
  tmp under /var/tmp; only planning evidence written outside the product worktree.
