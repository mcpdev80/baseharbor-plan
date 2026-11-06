# w208-candidate-ingress — Round 1, Wave 5

Lane: w208 (Worker). Coordinator: 841e7734.
Card: t-20261018-r27-candidate-ingress (Runde 1, Welle 5, 2026-11-06).
Repo: mcpdev80/baseharbor. Branch: work/r27-candidate-ingress.

## PLAN

- Read mission + task card; map deliverables against current develop; confirm scope
- Verify machinehttp execution/journal files are w207's field (do not touch); confirm file ownership
- Cut branch work/r27-candidate-ingress from origin/develop (base 21d8d05c); confirm ancestor rc=0
- Red-first: regression cell proving a second identical candidate silently overwrites an already-consented record (no error today)
- Implement bounded immutability guard in internal/deployment: re-record of an already-consented candidate identity+digest returns an explicit error; mutate guard off -> RED; counter-probe -> fires
- Immutable-source-selection cell: selected reference unchanged by later trunk movement (in-scope only; keep out of machinehttp files)
- Focused Go unit/vet/gofmt build on internal/deployment + cmd/baha; go build ./...
- Bundle, stage only changed files, commit, push; ls-remote == head with real witness
- Own terminal CI run on candidate path; record run ID + status
- Push evidence to origin/main; paste ls-tree witness into evidence; post END

## Base attestation

- Base ref: origin/develop
- Base SHA: 21d8d05cf1acf04729077e05eb350fcd3bb018ed
- Branch cut from that exact SHA; merge-base --is-ancestor origin/develop HEAD => rc=0

## Mission deliverables mapped against develop (scope decision)

Card outcome: accept and retain minimal authorized app/revision/consent metadata and the exact
native input/reference for an operation, with immutable source selection. Mission deliverables:
- (1) Authorization REQUIRED to create (mutate removal => RED, counter-probe GREEN)
- (2) IMMUTABLE: re-writing to the same candidate => explicit error (cell + mutation)
- (3) Immutable source selection: selected reference does NOT change through later trunk movement (cell)
- (4) Build-up real path (permanent clause)
- (5) Red-first on unmodified develop

Findings on develop (base 21d8d05c):
- (1) Authorization-required is implemented: candidate choke point in
  cmd/baha/deployment_record.go recordDeploymentBeforeMutation (state "applying") validates the
  CandidateSubmission with an explicit consent; cmd/baha/app_candidate_consent_test.go
  TestConsentRejectsWrongDigestWriteNothing proves a wrong digest writes nothing (RED) and the
  correct digest binds (GREEN). Contract: internal/delivery/candidate.go + contracts/candidate/v1.
- (2) IMMUTABILITY GAP: SaveDeploymentRecord (internal/deployment/deployment_store.go) never
  compares the prior already-consented candidate digest. A second identical apply overwrites the
  persisted consent without an explicit "cannot re-record the same immutable candidate" error. This
  is the bounded gap for this round.
- (3) Immutable source selection: internal/development/source_snapshot.go (candidate-pack, #1381)
  already captures a bounded local checkout with an ExactRef; the selected reference is not rewritten
  by later trunk movement in the snapshot contract. Cell covers snapshot/identity stability.
- (4) Build-up real path: apply path exists (cmd/baha/app_apply.go -> recordDeploymentBeforeMutation
  -> SaveDeploymentRecord).
- (5) Red-first on unmodified develop.

## File ownership

- Write-set for the immutability guard: internal/deployment/deployment_store.go, cmd/baha/deployment_record.go,
  cmd/baha/*_test.go (my bounded reservation; card says "bounded server candidate
  ingress/store/handler files").
- NOT touched: internal/machinehttp/* (execution/journal = w207's field). Queried read-only to
  confirm the boundary. No cross-write.

## Work done

- Branch cut from 21d8d05c; ancestor rc=0 confirmed.
- (Details continue below as the round proceeds.)

## END

<lane> w208-candidate-ingress: ... </lane>
