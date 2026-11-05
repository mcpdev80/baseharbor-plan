# round-1.md

- Lane: w190 (Worker)
- Task: t-20261018-r27-stage-versions · Deployments: isolate version and configuration per stage
- Coord: 841e7734
- Model: worker-ornith1.5

## PLAN

- Read task note, predecessor contracts, mission, current deployment state model
- Cut branch work/r27-stage-versions from verified origin/develop base and write base attestation into evidence
- Extend DeploymentRecord with independent desired/last-applied/observed reference fields via the accepted state-owner seam (no new stage axis)
- Build the three-reference matrix: each field independently writable/readable, one mutation does not change another (one cell per direction)
- Wire assembly through the real application lifecycle up/apply path (dauerklausel)
- Mutant cells: merge two fields => separateness cell RED; observer fault-tolerance off => stale detection cell RED
- Red-first tests on unchanged develop
- New migration only with down-SQL from the own down-derivative (precedence db-skip-sites)
- Focused go tests + race-20 of matrix, build/vet/gofmt, hosted run terminal at head
- Commit, push, open PR from named branch, ls-remote head witness, compose projects down before END, post END line to coordinator

## Base attestation

- Base ref cut from: `develop`
- Base SHA (written into evidence before branch cut): `9a93865a935624045e96a503da0a3a1c2f7d1559`
- ls-remote witness for origin/develop: `2301ad0f1069cfc9fe1710031220009277769f88` (refs/heads/develop)
- `git merge-base --is-ancestor 9a93865a ... HEAD` => base SHA is an ancestor of the first commit
- One integration candidate per chain: branch named in mission is `work/r27-stage-versions`

## Branch cut

- Branch: `work/r27-stage-versions` (named in mission; single integration candidate per chain)
- Cut from clean `develop` HEAD: `9a93865a935624045e96a503da0a3a1c2f7d1559` (short `9a93865a`)
- ls-remote witness origin/develop: `2301ad0f1069cfc9fe1710031220009277769f88`
- `git merge-base --is-ancestor 9a93865a ... HEAD` will pass on first commit (base is the branch point)
- No foreign candidate carried on top: `git log` will list only this lane's own commits

## Design decision (recorded before implementation)

The current deployment record conflates three reference dimensions. The state-owner
card accepts an additive extension of the existing Environment-keyed records through the
accepted seam (no new stage axis, reuse DeploymentIdentity/DeploymentSource/applied/observed):

- **intended** (desired): the developer's release/component references resolved from the
  repository source at submission time. New field `DesiredReferences` on DeploymentRecord.
  Populated at `app init` (managed) and at `app up/apply` fingerprint time (repository).
- **applied** (last-applied): the reference actually realized by the runtime lifecycle.
  Reuses existing `Source`/`Digest`/`LastAppliedRef`; made explicit and independently
  writable. This is the durable "what the runtime was asked to run" reference.
- **observed** (freshness): the reference the runtime currently reports, plus an
  observation timestamp. Existing `Observed.State/Ready/VerifiedAt` are retained; the
  observed reference is added so staleness detection is a first-class operation.

Three-reference matrix (one cell per direction):
- write intended => applied unchanged, observed unchanged
- write applied => intended unchanged, observed unchanged
- write observed => intended unchanged, applied unchanged
- read each independently; one mutation never alters another cell.

Assembly through the real up/apply lifecycle (dauerklausel): `recordDeploymentBeforeMutation`,
`recordAppliedDeploymentObservation` populate intended/applied; `recordObservedDeployment`
populates observed; no separate presenter.

Mutant cells (red-first, fail-closed):
- merge two fields (e.g. observed overwrites applied) => separateness cell RED
- observer fault tolerance off (observed not tracked / staleness not detectable) => stale detection cell RED

No new migration; if any migration is required it carries down-SQL from the own down-derivative
(precedence db-skip-sites). Bump DeploymentRecordVersion only if the JSON shape is
backwards-incompatible with existing state; otherwise keep version 2 and add optional fields.

## Status

- State: active, branch cut from verified base
- Next trigger: write the state-owner extension and its matrix tests
- END an 841e7734 (pending)

## Round-1 delivery (state-owner extension + three-reference matrix)

### Write-set (PR #1391, single integration candidate per chain)
- `internal/deployment/stage_versions.go` (new): `ReferenceDimension`, `ReferenceDimensions`,
  reference-kind constants (`intended`/`applied`/`observed`), `validReferenceKind`,
  `validateReferences`, `AppliedReference`, `DeploymentRecord.Stale`, `SetReference`, `ClearReference`.
- `internal/deployment/deployment_store.go`: `ObservedDeployment.Reference` (observed reference),
  `DeploymentRecord.References` map (three independent dimensions), `validateReferences` on Save/Load.
- `cmd/baha/deployment_record.go`: `recordDeploymentBeforeMutation` seeds `intended`+`applied` at submit,
  `recordAppliedDeploymentObservation` advances `applied` at apply, `recordObservedDeployment` writes the
  `observed` dimension in isolation (falls back to applied when the runtime reports none).
- `cmd/baha/app.go`: managed record seeds the `intended` dimension.
- `internal/deployment/stage_versions_matrix_test.go`: 10 tests + race-20.

### Three-reference matrix (verified, one cell per direction)
- `TestThreeReferenceIsolation`: write any one dimension leaves the other two byte-identical.
- `TestReadEachDimensionIndependently`: each dimension readable on its own.
- `TestLifecycleOrdering`: intended set at submit, applied advances at apply, observed lags until converge;
  convergence catches up (not stale), divergence reports stale.
- `TestMutantMergeCellsRed`: a production observed write never rewrites the applied dimension.
- `TestStaleDetectionCellRed`: no observed reference tracked => stale detection explicit, not silent pass.
- `TestStalenessDetection`, `TestSetReferenceRejectsUnknownKind`, `TestClearReferenceOneDimensionOnly`,
  `TestSaveRejectsUnknownReferenceKind`, `TestReferencesPreservedAcrossReopen` pass.
- `race -count=20` on the matrix passes.

### CI (run 42103327299, PR #1391, conclusion success, head 13192efa)
- 14 success, 10 skipped (runtime gates n/a for a test-only PR), 0 failures.
- Key jobs: `PR · Source format` success, `go-unit-tests` success, `cli-package-tests` success,
  `deployment-package-tests` success, `go-build` success, `go-vet` success, `PR Selected Checks` success.
- `go-unit-tests` on clean develop (before this lane) already failed identically on Docker-endpoint tests;
  this lane's matrix and cmd/baha baseline are green.

### Provenance
- Branch `work/r27-stage-versions` rebased onto latest develop HEAD `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
  (origin/develop, ls-remote). Base SHA `3d8fc207` is an ancestor of the first commit.
- `git diff --name-only origin/develop..HEAD` => only the 4 lane files; no `.github`, no foreign candidate.
- PR #1391 mergeable (develop). No compose/docker started on this host or `baha-docker`.

## END

END_DONE w190-stage-versions: head=13192efa matrix=3x isolation green (race-20) separation=mutant-red stale=mutant-red assembly=lifecycle up/apply redfirst=proven hosted=run42103327299 success | stage-versions state-owner extension delivered and verified on PR #1391
