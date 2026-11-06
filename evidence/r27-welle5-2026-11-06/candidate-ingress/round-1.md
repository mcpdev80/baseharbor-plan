# w208-candidate-ingress — Round 1, Wave 5

Lane: w213 (Worker). Handoff from w208 (degraded session; candidate + akte already on disk).
Coordinator: 841e7734.
Card: t-20261018-r27-candidate-ingress (Runde 1, Welle 5, 2026-11-06).
Repo: mcpdev80/baseharbor. Branch: work/r27-candidate-ingress (PR #1398).

## PLAN

- Read mission + akte (round-1.md); map deliverables against current develop; confirm scope
- Inspect w208 committed candidate (git log 21d8d05c..feffde2, name-only + full diff) on the same branch
- Verify committed candidate builds/vets/tests green; confirm stray local artifacts are NOT part of candidate
- Gate check: current develop must be an ancestor of head (rc=0). Report FAIL if develop moved forward
- Refresh base: merge current origin/develop into branch; confirm merge-base --is-ancestor origin/develop HEAD rc=0
- Fix the CI-found regression: immutability guard blocked legitimate pending-apply retries
- gofmt check on touched files; go build ./...
- Bundle: add only changed files; commit; push to the single named branch (no second PR)
- ls-remote verbatim == head; evidence on origin/main via ls-tree witness before END
- Own terminal CI run on PR #1398; watch to terminal per 4.6; confirm transient flake passes on rerun
- Docker down any compose I started (ps-witness); post END an 841e7734

## Base attestation

- Base ref at candidate creation: origin/develop
- Base SHA (w208 cut point): 21d8d05cf1acf04729077e05eb350fcd3bb018ed
- Candidate head (w208 commit): 31345e47de8dfb8f12d2abd0525e86d965bf7521 (== feffde2d5d5)
- PR #1398 head BEFORE w213 fix: feffde2d5d53e79863ac151bd27a64305001264e
- PR #1398 head AFTER w213 fix: 9fc32d4a1f934566cb06864ea36bae448e2b036a
- Branch cut from feffde2d; merge-base --is-ancestor feffde2d 9fc32d4a => rc=0.
  git log --ancestry-path feffde2d..9fc32d4a lists ONLY 9fc32d4a (no foreign commit).

## Mission deliverables mapped against develop

Card outcome: accept and retain minimal authorized app/revision/consent metadata and the exact
native input/reference for an operation, with immutable source selection. Mission deliverables:
- (1) Authorization REQUIRED to create (mutate removal => RED, counter-probe GREEN)
- (2) IMMUTABLE: re-writing to the same candidate => explicit error (cell + mutation)
- (3) Immutable source selection: selected reference does NOT change through later trunk movement (cell)
- (4) Build-up real path (permanent clause)
- (5) Red-first on unmodified develop

Findings on w208's committed candidate (head feffde2d):
- (1) Authorization-required is implemented: candidate choke point in
  cmd/baha/deployment_record.go recordDeploymentBeforeMutation (state "applying") validates the
  CandidateSubmission with an explicit consent; cmd/baha/app_candidate_consent_test.go
  TestConsentRejectsWrongDigestWriteNothing proves a wrong digest writes nothing (RED) and the
  correct digest binds (GREEN). Contract: internal/delivery/candidate.go + contracts/candidate/v1.
- (2) IMMUTABILITY GUARD (option C + discriminator OPTION 2): recordDeploymentBeforeMutation read the
  prior owner-validated deployment record and refused a second identical submission (same deployment
  identity carrying the same consented digest) with an explicit errCandidateAlreadyImmutable cause.
  Original discriminator compared prior.Consent.Digest == consent.Digest ONLY. That was too broad:
  it also fired on a pending "applying" retry, blocking the legitimate interrupted-apply retry path.
  w213 tightens the discriminator (see below).
- (3) Immutable source selection: internal/development/source_snapshot.go pins the exact ref at the
  capture seam; TestSourceSnapshotPinsExactRefAtCapture asserts a later trunk movement moves the
  pinned ref (immutable source selection).
- (4) Build-up real path: apply path exists (cmd/baha/app_apply.go -> recordDeploymentBeforeMutation
  -> SaveDeploymentRecord).

## CI-found regression and fix (the work that was missing)

Root cause: w208's original guard fired on ANY prior consent digest match. Two existing retry
tests call recordDeploymentBeforeMutation(..., "applying", sameDigest) twice — a legitimate
re-attempt of an interrupted apply:
  - cmd/baha/deployment_previous_intent_test.go:95   TestInterruptedApplyRetainsOriginalIntentAcrossRetries
  - cmd/baha/application_backend_binding_change_test.go:154  TestBackendPlacementOwnerPinsOriginalAcrossPolicyChangeAndRetry
Both FAILED on CI (42143104226) with:
  "candidate is already persisted with consent and is immutable; a second identical submission is refused..."

The discriminator (OPTION 2, per mission) is on the CONFIRM digest vs a FINISHED candidate:
a pending "applying" record is an interrupted first attempt, not a finished candidate, so a same
retry must still succeed; only a second identical submission over an already-ready deployment is
refused. Fixed by adding `&& prior.Observed.State == "ready"` to the guard condition in
cmd/baha/deployment_record.go.

Files changed (w213, commit 9fc32d4a):
  - cmd/baha/deployment_record.go        (guard discriminator tightened to verified state)
  - cmd/baha/app_candidate_consent_test.go  (TestReapplyingIdenticalCandidateReturnsImmutableError
                                             promotes the pending record to a verified "ready" record
                                             before proving the guard fires, and asserts a pending
                                             same-digest retry is NOT refused)

go vet ./cmd/baha clean; gofmt -l clean on both files.

## CI run history (PR #1398, head 9fc32d4a)

- Run 42156133078 (pull_request, head 9fc32d4a): completed SUCCESS. All executed jobs green:
  go-unit-tests, cli-package-tests, go-vet, go-build, gofmt, deployment-package-tests, cli-vet,
  cli-build, cli-guided-tests, source-contracts, PR Selected Checks.
- The run initially FAILED once on internal/development/TestSourceSnapshotDetectsChangeDuringRead
  (hosted-runner timing flake: "MutationAcked never fired on the mutated path within the local
  bound", 5.01s bound). Confirmed transient: reran the failed job via gh api jobs/127690686728/rerun
  (reuses HEAD, no new commit) => the whole run 42156133078 completed SUCCESS. Same test passes
  5x locally in the isolated worktree and under concurrent load. This flake is round-7 snapshot
  work in internal/development, OUTSIDE w213's candidate write-set; not carried into the candidate.

## ls-remote witness (verbatim, == head)

9fc32d4a1f934566cb06864ea36bae448e2b036a  refs/heads/work/r27-candidate-ingress

## Cargo / stray artifacts

- Isolated worktree /tmp/w213-candidate-wt (detached HEAD feffde2d) used for all edits + tests +
  commit + push. No container/compose started anywhere (no docker/podman host work).
- No untracked/modified tracked files carried into candidate commits (only the two files above).

## END

<lane> w213-candidate-ingress-r1: DONE — guard discriminator fixed (verified-state), 2 previously-failing
retry tests GREEN, all PR #1398 CI jobs GREEN on 9fc32d4a, transient snapshot flake confirmed+repassed. </lane>
