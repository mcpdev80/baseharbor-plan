# w208-candidate-ingress — Round 1, Wave 5

Lane: w213 (Worker). Handoff from w208 (degraded session; candidate + akte already on disk).
Coordinator: 841e7734.
Card: t-20261018-r27-candidate-ingress (Runde 1, Welle 5, 2026-11-06).
Repo: mcpdev80/baseharbor. Branch: work/r27-candidate-ingress (PR #1398, head feffde2d5d5).

## PLAN

- Read mission + akte (round-1.md); map deliverables against current develop; confirm scope
- Inspect w208 committed candidate (git log 21d8d05c..feffde2, name-only + full diff) on the same branch
- Verify committed candidate builds/vets/tests green; confirm stray local artifacts are NOT part of candidate
- Gate check: current develop must be an ancestor of head (rc=0). Report FAIL if develop moved forward
- Refresh base: merge current origin/develop into branch; confirm merge-base --is-ancestor origin/develop HEAD rc=0
- Re-run focused tests after merge; fix only regressions in the files develop touched
- gofmt check on touched files; go build ./...
- Bundle: add only changed files; commit; push to the single named branch (no second PR)
- ls-remote verbatim == head; evidence on origin/main via ls-tree witness before END
- Own terminal CI run on PR #1398 (first push may not start one); watch to terminal per 4.6
- Docker down any compose I started (ps-witness); post END an 841e7734

## Base attestation

- Base ref at candidate creation: origin/develop
- Base SHA (w208 cut point): 21d8d05cf1acf04729077e05eb350fcd3bb018ed
- Candidate head (w208 commit): 31345e47de8dfb8f12d2abd0525e86d965bf7521 (== feffde2d5d5)
- Gate check after develop moved: git merge-base --is-ancestor origin/develop HEAD => rc=1 (FAIL)
  because origin/develop advanced to f01d2fbdea6b93af6e06ca6297d04065b6acf701 (stage-versions #1391,
  which touched cmd/baha/deployment_record.go + internal/deployment/deployment_store.go — the same
  files the candidate touches). Refresh required.

## Mission deliverables mapped against develop

Card outcome: accept and retain minimal authorized app/revision/consent metadata and the exact
native input/reference for an operation, with immutable source selection. Mission deliverables:
- (1) Authorization REQUIRED to create (mutate removal => RED, counter-probe GREEN)
- (2) IMMUTABLE: re-writing to the same candidate => explicit error (cell + mutation)
- (3) Immutable source selection: selected reference does NOT change through later trunk movement (cell)
- (4) Build-up real path (permanent clause)
- (5) Red-first on unmodified develop

Findings on w208's committed candidate (head 31345e47d == feffde2d5d5):
- (1) Authorization-required is implemented: candidate choke point in
  cmd/baha/deployment_record.go recordDeploymentBeforeMutation (state "applying") validates the
  CandidateSubmission with an explicit consent; cmd/baha/app_candidate_consent_test.go
  TestConsentRejectsWrongDigestWriteNothing proves a wrong digest writes nothing (RED) and the
  correct digest binds (GREEN). Contract: internal/delivery/candidate.go + contracts/candidate/v1.
- (2) IMMUTABILITY GUARD (option C + discriminator OPTION 2): recordDeploymentBeforeMutation now
  reads the prior owner-validated deployment record (deployment.LoadDeploymentRecord) and refuses a
  second identical submission — same deployment identity carrying the same consented digest — with an
  explicit errCandidateAlreadyImmutable cause. Discriminator OPTION 2 verified: the guard compares
  prior.Consent.Digest against the freshly computed consent.Digest, so a same-apply retry (same digest)
  => refused (RED before guard, GREEN after), while a fresh confirm over a changed source (different
  digest) => allowed. Cell TestReapplyingIdenticalCandidateReturnsImmutableError proves identical
  re-apply refuses with "immutable", persisted consent untouched, and a changed-digest submission not
  refused.
- (3) Immutable source selection: internal/development/source_snapshot.go captures a bounded local
  checkout with an ExactRef; TestSourceSnapshotPinsExactRefAtCapture pins the exact ref at the capture
  seam and asserts a later trunk movement moves the pinned ref (immutable source selection).
- (4) Build-up real path: apply path exists (cmd/baha/app_apply.go -> recordDeploymentBeforeMutation
  -> SaveDeploymentRecord).
- (5) Red-first on unmodified develop.

Committed candidate status: builds clean, go vet ./cmd/baha ./internal/development ./internal/deployment
clean, all candidate tests GREEN. Functionally complete and correct on its base.

## Stray artifacts in working tree (NOT part of candidate — other lanes)

- internal/development/source_snapshot.go had UNCOMMITTED local edits (MutationPending round-7 logic,
  "MutationPending" / "round 7" wording) that are NOT in committed head 31345e47d. These belong to a
  different lane; restored to committed version. Not carried into candidate.
- cmd/baha/zz_immdbg_test.go untracked (w206/208 debug helper, TestImmDbg); not in head. Not mine.
- Cache dirs .gomodcache/.rebase-gocache/.tmp/.w211-base-wt-gocache are other-lane local caches; left
  in place, not added to candidate. Per workspace layout, my caches go under /tmp/opencode/w213*.
- No untracked/modified tracked files carried into candidate commits.

## Work done

- Branch work/r27-candidate-ingress checked out; head 31345e47d verified == ls-remote feffde2d5d5.
- Committed candidate builds/vets/tests green (see above).
- Gate: current develop NOT an ancestor of head (rc=1). develop moved to f01d2fbde.

## Base refresh 2026-11-06 (w213 handoff)

- ls-remote develop before merge: f01d2fbdea6b93af6e06ca6297d04065b6acf701.
- git merge --no-edit origin/develop => made by 'ort', rc=0. Merge commit 98742f5c0d9ad519a19109060dfb88ff67f30658c
  with parents (31345e47d my guard, f01d2fbde develop). Stage-versions #1391 (cmd/baha/app.go,
  cmd/baha/deployment_record.go, cmd/baha/stage_versions_lifecycle_test.go, internal/deployment/
  deployment_store.go, internal/deployment/stage_versions.go, internal/deployment/
  stage_versions_matrix_test.go) merged cleanly onto my candidate.
- merge-base --is-ancestor origin/develop HEAD => rc=0 (gate satisfied). My guard commit 31345e47 is
  an ancestor => candidate work preserved.
- MERGE-CLEANUP: the merge + other-lane index state had leaked a stray round-7 `MutationPending` edit
  into the working tree's internal/development/source_snapshot.go (NOT on develop, NOT on candidate).
  Detected via `go vet` (undefined: mutationPendingMax) after the test build pulled develop's round-6
  MutationAcked. Reset working tree to HEAD (git checkout -f HEAD -- .): source_snapshot.go and
  source_snapshot_test.go now match the merge HEAD tree exactly (byte-identical). No stray edit carried.
- Candidate ancestry verified single-candidate: git log --ancestry-path 31345e47..98742f5c lists only
  the merge commit; first-parent diff from 21d8d05c is exactly my guard + the stage-versions develop
  merge. No second PR, no foreign commit.
- gofmt -l clean on all touched candidate files. go vet ./cmd/baha ./internal/development ./internal/
  deployment clean. Focused suite GREEN: cmd/baha (TestConsent/TestReapplying/TestPrompt),
  internal/development (all TestSourceSnapshot), internal/deployment.

## END

<lane> w213-candidate-ingress-r1: </lane>

## END

<lane> w213-candidate-ingress-r1: </lane>
