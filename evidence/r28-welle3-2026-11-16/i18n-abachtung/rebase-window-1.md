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
head b6055fd47 at 2026-11-17T05:34:23Z. Terminal outcome:

    run_id=44025048848 status=completed conclusion=failure sha=b6055fd47a160b47f55c9f2c50317a014d313091

Failed jobs (all `PR · Selected Core-less · {docker,podman} / coreless-lifecycle · application`
and the aggregate `PR Selected Checks`):

    FAIL: TestManagedRegisteredOTLPNativeConsumerHandoff (cmd/baha/application_otlp_handoff_runtime_test.go:120)
    shared Identity failed common union: complete=true changes=[{InstanceID:opentelemetry-collector/shared Action:add ...}]

Everything else green/skipped-appropriately: go-build, go-vet, cli-gofmt, documentation-audit,
mkdocs EN/DE strict, pages-candidate-build, all Go unit shards, owner-node native, Demo Pin,
Focused Python, Native gate plan, Trusted Plan.

## Root cause of the failure (base-internalization gap, not content)

- The i18n commit 55550400c was cut from develop@34c2ede5.
- Meanwhile merged PR #1657 (coreless app backend empty target) changed
  `configureTestTarget(t)` -> `configureTestTargetEmpty(t)` in the same test file
  on develop (git diff 34c2ede5..bcae1e8c -- cmd/baha/application_otlp_handoff_runtime_test.go).
- The base merge folded develop in but kept the branch side of that hunk (no textual conflict),
  so the candidate runs the OTLP test on the old (non-empty) target setup, which the shared
  coreless identity union now flags — exactly what #1657 fixed.
- The CI itself computed integration merge `30cfe779` (develop bcae1e8c + head b6055fd47);
  the failing gate ran against that merge, so the gap is real at GitHub's merge tip.

## Actions taken / needed

- No force-fix (mission rule). One normal `git merge origin/develop` (bcae1e8c) fold-in was
  already this window's job; the remaining defect is a one-line integration fix in
  application_otlp_handoff_runtime_test.go (`configureTestTarget` -> `configureTestTargetEmpty`)
  that requires a re-merge resolution or a follow-up corrective commit — FLAGGED to Coordinator
  for dispatch decision, since this lane was contractually base-freshness only.
- PR #1663 post-state: `state=OPEN isDraft=false mergeable=MERGEABLE mergeStateStatus=BLOCKED`.

## repo-rule compliance

- No `.github/**` change; no merge of the PR; no force-push; no subagent (§4.8);
  tmp under /var/tmp; only planning evidence written outside the product worktree.
