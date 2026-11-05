# Round 2 Evidence — stage-versions lifecycle reference-map fix

- Lane: w197 (Worker)
- Task: t-20261018-r27-stage-versions · Deployments: isolate version and configuration per stage
- Coord: 841e7734
- Model: worker-ornith1.5
- PR: #1391 (open), branch work/r27-stage-versions
- Fix commit: 73809ed46ce06c922b98fbd7832222c3be1fc880
- Base: develop 3d8fc207deabc2840bcfd888f46d2394cc5a7d36
- Review verdict corrected: review-1391a.md (REJECT, recipe applied)

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

- git ls-remote origin refs/heads/work/r27-stage-versions => 73809ed46ce06c922b98fbd7832222c3be1fc880 (exact == head)
- push record: 13192efa..73809ed4 work/r27-stage-versions -> work/r27-stage-versions

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

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/42114826167 (CI · PR #1391, run #4833, head 73809ed4, event pull_request)
- Terminal conclusion: failure. The failure is a runner/infrastructure gate, NOT a test assertion failure.
- Failing jobs: PR · Validation · go-unit-tests, PR · Validation · cli-guided-tests,
  PR · Validation · cli-package-tests, and the aggregating PR Selected Checks.
- The failing step in each is "Execute existing validation owner without publication" (ci.yml:782).
- go-unit-tests runs scripts/pr-unit-database.sh, which starts a Docker fixture
  (docker run postgres:18-alpine --publish 127.0.0.1:5433:5432); the fixture never became available on the
  runner, so the gate failed before any test ran. cli-package-tests / cli-guided-tests route through
  scripts/pr-check-runner.py execute, which needs a Docker/Podman runner that was not available.
- Passing jobs (directly relevant to this change): PR · Validation · deployment-package-tests = SUCCESS,
  PR · Validation · go-build = SUCCESS, PR · Validation · go-vet = SUCCESS, PR · Validation · cli-gofmt =
  SUCCESS, PR · Validation · source-contracts = SUCCESS.
- This is a runner/infrastructure STATE (Docker/Podman not available on the shared hosted runner right now),
  not a defect in the fix. The same check type failed on an identical-content candidate run; the code-level
  packages (deployment-package-tests, go-build, go-vet, cli-gofmt) are green.
- Per mission scope: .github/workflows are Owner-owned; I did not edit any workflow or trigger
  workflow_dispatch / rerun. Reported as STATE.

## Scope compliance

- No .github file edited. No workflow_dispatch / rerun triggered.
- No second branch for this card; worked only on the named branch work/r27-stage-versions.
- Evidence written only in baseharbor-plan (round-2.md). No .evidence/ dir, no main-branch writes.
- No operational text written into the product repo. No subagents used.
- Workspace layout fixed: worktree under /tmp/opencode/<lane>-wt, no scratch in the ecosystem root.
- Docker/Podman: NOT started on this host (coordinator/codeman server). No compose project started.

## END

END_DONE w197-stage-versions-r2: head=73809ed4 fix=load-merge-refs applied+observed+intended preserved matrix=lifecycle race20 green mutants=2/2 red (A merged-cell, B drop-applied) downsql=not-applicable(no migration/JSON-only) develop=ndrift(rc0) ci=42114826167 STATE-deploy-runner-unavailable | round-2 lifecycle reference-map fix delivered on PR #1391; deployment-package-tests/go-build/go-vet/cli-gofmt green; unit/package runner-gate blocked by unavailable Docker/Podman runner (STATE, not code)
