# Round 2 Evidence — stage-versions lifecycle reference-map fix

- Lane: w197 (Worker)
- Task: t-20261018-r27-stage-versions · Deployments: isolate version and configuration per stage
- Coord: 841e7734
- Model: worker-ornith1.5
- PR: #1391 (open), branch work/r27-stage-versions
- Fix commit: 60d5896c9c4aec9018786e40aa63e626916e5b01 (merge develop 21d8d05c + fix commits 73809ed4 + 142642ef)
- Base: develop 3d8fc207deabc2840bcfd888f46d2394cc5a7d36
- Review verdict corrected: review-1391a.md (REJECT, recipe applied)

## Final state (measured — read this first)

- Branch head: work/r27-stage-versions == 60d5896c9c4aec9018786e40aa63e626916e5b01
  (git ls-remote origin refs/heads/work/r27-stage-versions, rc=0; == local HEAD)
- develop (21d8d05cf1a) IS ancestor: git merge-base --is-ancestor origin/develop HEAD => rc=0
- CI 42131821530 (run #4847) at head 60d5896c => status=completed, conclusion=success (ALL jobs SUCCESS, go-unit-tests incl.)
- This head = merge origin/develop + my fix commits 73809ed4 + 142642ef. Round-2 terminal green.

## PLAN

- Read task note, mission, review-1391a, round-1; confirm base develop 3d8fc207 is ancestor of candidate head 13192efa5 (rc=0)
- Worktree w197-stage-versions-r2-wt at named branch work/r27-stage-versions (head 13192efa5); base attestation written to evidence
- FIX recordAppliedDeploymentObservation: load existing References map, update only applied, preserve intended + observed
- FIX recordObservedDeployment: load existing References map, update only observed, preserve intended + applied (do not rebuild fresh map)
- Matrix test drives real lifecycle writers (recordAppliedDeploymentObservation / recordObservedDeployment) with -race -count=20 in /tmp writable env
- Mutant A (merge applied+observed fields) run individually RED; Mutant B (drop applied on convergence) run individually RED, both w/ terminal output
- Down-SQL verdict: not applicable — no migration in candidate diff; references are additive optional JSON field, no SQL schema
- go test (matrix+lifecycle) + go vet + go build + gofmt; fix failures
- develop-merge: if drift + ancestor rc=0; branch already up to date (no drift)
- Push named branch head witness; terminal hosted run; evidence round-2.md; compose down before END; END line to 841e7734

## Base attestation

- Base ref cut from: develop (origin/develop)
- Base SHA written into evidence before branch cut: 3d8fc207deabc2840bcfd888f46d2394cc5a7d36
- ls-remote witness origin/develop: 3d8fc207deabc2840bcfd888f46d2394cc5a7d36
- git merge-base --is-ancestor 3d8fc207... HEAD => rc=0 (base is an ancestor of the fix commit)
- Single integration candidate per chain: branch named in mission is work/r27-stage-versions; no second branch invented
- Branch history linear on top of develop (round-1 PR #1391 at 13192efa + my single fix commit 73809ed4; no foreign candidate on top)
- name-only diff develop..73809ed4 = the PR #1391 file set (app.go, deployment_record.go, deployment_store.go, stage_versions.go, stage_versions_matrix_test.go) + my new stage_versions_lifecycle_test.go; no .github file touched

## Workspace / worktree

- Worktree: /tmp/opencode/w197-stage-versions-r2-wt (under /tmp, not in ecosystem root)
- Branch: work/r27-stage-versions (the named candidate branch)
- HEAD at start: 13192efa5d5ce1d4a855a43ceb8e9000ded5188c (matches remote exactly)
- Fix commit: 73809ed46ce06c922b98fbd7832222c3be1fc880

## ls-remote head witness

- (r1, superseded) git ls-remote origin refs/heads/work/r27-stage-versions => 73809ed46ce06c922b98fbd7832222c3be1fc880
  push record: 13192efa..73809ed4 work/r27-stage-versions -> work/r27-stage-versions
- (current, measured) git ls-remote origin refs/heads/work/r27-stage-versions =>
  60d5896c9c4aec9018786e40aa63e626916e5b01 (== local HEAD, rc=0)

## Defect (from review-1391a criterion 2, the round-2 target)

- recordAppliedDeploymentObservation (cmd/baha/deployment_record.go) built a fresh References map with ONLY
  the applied dimension. Advancing applied dropped the intended (desired) and prior observed dimensions.
- recordObservedDeployment built a fresh References map with ONLY the observed dimension (the intended
  re-add wrote into its own freshly-created map, a no-op). The applied dimension was deleted on convergence.
- Consequence: DeploymentRecord.Stale() (stage_versions.go) saw no applied dimension and returned nil, so
  stale detection could silently pass after convergence. Real production-path data loss (up -> apply ->
  new map), not only a test gap.

## Correction

- Both writers now LoadDeploymentRecord first, touch only their own dimension, and save the merged map so
  intended/applied/observed stay independent through the real up/apply lifecycle.
- recordAppliedDeploymentObservation: preserves intended + observed while advancing applied.
- recordObservedDeployment: preserves intended + applied while writing observed (fall back to applied ref).
- Diff is 2 files (cmd/baha/deployment_record.go fixed + cmd/baha/stage_versions_lifecycle_test.go new).
- gofmt clean, go vet clean, go build clean.

## Matrix / race-20 (real lifecycle, writable /tmp env)

- New test file cmd/baha/stage_versions_lifecycle_test.go drives the REAL lifecycle writers through a real
  up/apply fixture (configureTestTarget + httpsAdoptionFixture + resolveApplication + recordPendingDeployment
  + recordAppliedDeploymentObservation + recordObservedDeployment) — not SetReference helper calls.
- TestLifecycleThreeDimensionsPreserved: submit seeds intended+applied; apply advances applied only
  (intended survives); convergence writes observed only (applied AND intended survive). All three readable
  after every transition.
- TestLifecycleStaleAfterConvergence: observed catches up to applied => not stale; applied dim still exists.
- race-20 (go test -race -count=20) on the lifecycle + mutant tests => ok (rc=0).

### Red-first proof (the fix is necessary)

- On the ORIGINAL candidate (before fix) TestLifecycleThreeDimensionsPreserved FAILS:
  "intended dropped after apply (the round-1 defect)" — the test is RED on the bug.

## Mutant runs (isolated, each turned RED, then reverted)

- Mutant A (merge applied+observed fields in recordObservedDeployment): TestMutantMergeAppliedObservedRed
  turned RED with the exact failing line:
  stage_versions_lifecycle_test.go:144: MUTANT-RED: applied reference rewritten by observed write:
  "merged-observed" != "bae1cf608d191b59cc587695f793d0ba5adf6bda4b5f04920b00c391d4a12340"
  rc=1 (FAIL). Reverted to fixed.
- Mutant B (drop the applied dimension on convergence = the round-1 defect): TestLifecycleThreeDimensionsPreserved
  turned RED with:
  stage_versions_lifecycle_test.go:91: applied dropped on convergence (the round-1 defect)
  rc=1 (FAIL). Reverted to fixed.
- After revert to the fixed source, TestLifecycleThreeDimensionsPreserved + TestMutantMergeAppliedObservedRed
  pass (rc=0).

## Down-SQL verdict (requirement 4)

- NOT APPLICABLE. The candidate diff changes no migration SQL and adds no migration file (verified:
  git diff --name-only develop..13192efa contains no migrat/sql/schema path). The three reference
  dimensions are stored as an additive optional JSON field (DeploymentRecord.References) on the existing
  Environment-keyed deployment record. There is no database schema to derive down-SQL for. Backwards
  compatible with existing records (missing references key is tolerated by validateReferences).

## develop-merge (requirement 5)

- origin/develop unchanged (3d8fc207, ls-remote). merge-base develop..HEAD = 3d8fc207.
  git merge-base --is-ancestor develop HEAD => rc=0.
- No drift: develop has zero commits the branch lacks. develop-merge not needed; branch already up to date.

## Hosted run (CI)

### Run 4837 (run 42114826167) — head 73809ed4 — TERMINAL FAILURE, real regression
- Terminal conclusion: failure. This run exposed a REAL regression from the first fix.
- The first fix loaded the prior record and returned its error unconditionally. On the FIRST
  apply/observe there is no prior deployment.json yet, so the write was aborted and no
  deployment.json was persisted, breaking every downstream load.
- Failing jobs: go-unit-tests, cli-guided-tests, cli-package-tests, PR Selected Checks.
- Failing test log line (go-unit-tests, source_snapshot_test.go:224 is unrelated flake; the real
  failures were in cmd/baha/application_backend_binding_change_test.go:40 and 20+ other tests):
  `incomplete deployment state for docker-dev// [<uuid>]: deployment.json is missing: file does not exist`
  (104 occurrences across internal/application/* and cmd/baha/*).
- These are NOT a runner-unavailable STATE. A FAIL line is code or flake, both reportable with witness:
  this was a CODE regression in my fix.

### Fix for the regression
- Both writers now accept os.ErrNotExist from LoadDeploymentRecord and start from an empty
  References map instead of aborting the write:
    `if loadErr != nil && !errors.Is(loadErr, os.ErrNotExist) { return loadErr }`
- Verified: TestConsentRejectsWrongDigestWriteNothing, TestGuidedRead*, TestGuidedBackup*,
  TestPromptDigestEqualsBindDigest, TestInterruptedApply*, TestInstallationChildScope* all green.
- go vet clean; go build clean; gofmt clean.

### Run 4837 corrected commit — 142642ef (head) — CI run 42121706077
- Committed 142642ef "do not abort recordWrites on missing prior record" on top of 73809ed4.
- Pushed 73809ed4..142642ef; ls-remote 142642efd08dc01c112c833ea4ff211fd4bf23f5.
- CI run 42121706077: deployment-package-tests/go-build/go-vet/cli-gofmt/source-contracts/cli-package-tests/
  cli-guided-tests/cli-build/cli-vet SUCCESS. Only go-unit-tests terminal FAILURE.
- Remaining failure: TestSourceSnapshotDetectsChangeDuringRead (internal/development/source_snapshot_test.go:224):
  "expected change-during-read guard to abort the capture". This test is a GOROUTINE race test
  (repeatedly os.Chtimes a file during the snapshot walk). It is unrelated to deployment records.
- Flake proven, NOT a regression: locally it passes 5/5 on my branch AND 5/5 on clean develop.
  The single CI miss was a timing/disk-quota artifact (run 42121706077 hit /tmp disk-quota during
  compile — internal/runtime/gc: write ... disk quota exceeded in the run log).
- Net: the code-level regression is fixed; the only remaining CI miss is a pre-existing flaky
  timing test, demonstrated non-blocked by repeated local runs.

### FINAL — merge origin/develop (21d8d05c, r27-device-lifecycle, contains the flaky-test heal) — CI 42131821530 SUCCESS
- Coordinator directive: last END (73809ed4) was superseded; develop is the ancestor (not "no drift");
  the go-unit-tests rot was most likely the chronic flake that was just merged-healed on develop 21d8d05cf1a.
- Merge origin/develop into work/r27-stage-versions (rc=0); commit 60d5896c (merge + my two fix commits
  on top of 21d8d05c); push 142642ef..60d5896c; remote head 60d5896c9c4aec9018786e40aa63e626916e5b01.
- CI run 42131821530 (run #4847, head 60d5896c, event pull_request): ALL jobs terminal SUCCESS, including
  go-unit-tests (the flaky TestSourceSnapshotDetectsChangeDuringRead now passes). PR Selected Checks = success.
- Acceptance checks per directive: ls-remote real == new head 60d5896c (rc=0); ancestor rc=0
  (git merge-base --is-ancestor origin/develop HEAD => rc=0, develop IS the ancestor).
- Measured witnesses (this run, not asserted from memory):
  git ls-remote origin refs/heads/work/r27-stage-versions =>
  60d5896c9c4aec9018786e40aa63e626916e5b01  (exact == local HEAD 60d5896c, rc=0)
  git rev-parse HEAD => 60d5896c9c4aec9018786e40aa63e626916e5b01
  git merge-base --is-ancestor origin/develop HEAD => rc=0 (develop 21d8d05c IS the ancestor)
  CI 42131821530 (run #4847) at head 60d5896c => status completed, conclusion success
  (gh api .../runs/42131821530 --jq '{status,conclusion}'); PR Selected Checks = success.
- Net: terminal green on the real branch head. Round-2 delivered and accepted.

## Local verification summary

- cmd/baha targeted regression (the packages CI reported failing): green.
- internal/application: green (106.661s, rc=0) — the package with the most CI failures.
- internal/development/TestSourceSnapshotDetectsChangeDuringRead: passes 5/5 on this branch and 5/5 on clean develop — confirmed pre-existing flaky race test, not a regression.
- Pre-existing local failures (environment/test-isolation, NOT my code): TestQuickInit*, TestAppInit* with "deployment has no authoritative installation owner for its Target" and TestWritePathPromptContextShowsCurrentDirectory (tmpdir/cwd). Verified identical failures on clean develop with the same local setup. These pass in the real CI runner environment.
- go vet clean; go build clean; gofmt clean.
- Env remediation: another lane's `go env -w` had set GOCACHE/GOMODCACHE/GOPATH/GOTMPDIR to the stray
  broken worktree r27-dl-wt (now removed). Reset to clean values; backup at
  /home/marcel/.config/go/env.bak.w197.

- Cache hygiene (Coordinator HYGIENE directive): my go cache/tmpdir had been inside the product repo
  (baseharbor/.tmp, reached 4.8G and another lane collided). Per directive, moved GOCACHE+TMPDIR to
  /tmp/opencode/w197-stage-versions-r2-wt/.cache/ (gocache + tmp subdirs). Verified with a small
  TestSourceSnapshotDetectsChangeDuringRead run (ok, rc=0). baseharbor/.tmp still holds stale logs/bin
  and old cache-* subdirs (no live process uses them); root-tilgung of baseharbor/.tmp left to
  Coordinator after my END (no ps-backed live process to spare — nothing was running when switched).

## Scope compliance

- No .github file edited. No workflow_dispatch / rerun triggered.
- No second branch for this card; worked only on the named branch work/r27-stage-versions.
- Evidence written only in baseharbor-plan (round-2.md). No .evidence/ dir, no main-branch writes.
- No operational text written into the product repo. No subagents used.
- Workspace layout fixed: worktree under /tmp/opencode/<lane>-wt, no scratch in the ecosystem root.
- Docker/Podman: NOT started on this host (coordinator/codeman server). No compose project started.

## END

END_DONE w197-stage-versions-r2: head=60d5896c9c4aec9018786e40aa63e626916e5b01 (merge develop 21d8d05c + fix 73809ed4+142642ef) fix=accept-os.ErrNotExist-init-empty-References-map first-write-now-persists matrix=lifecycle race20 green mutants=2/2 red downsql=not-applicable(no-migration/JSON-only) ancestor=rc0(develop IS vorfahr) | PR #1391 round-2 lifecycle reference-map fix TERMINAL GREEN; CI 42131821530 run #4847 head 60d5896c measured status=completed conclusion=success ALL jobs SUCCESS incl go-unit-tests (flaky TestSourceSnapshotDetectsChangeDuringRead healed by develop 21d8d05cf1a); ls-remote real==60d5896c rc0; ancestor is-ancestor origin/develop HEAD rc0. go vet/build/gofmt clean.
