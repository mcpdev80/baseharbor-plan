# r27 state-owner r8 — fix-r8 evidence (w28-stateowner-r8)

- Role: Worker, lane w28-stateowner-r8, coord f49a3303.
- Base: head e4af28c2, branch work/r27-state-owner (remote `origin/work/r27-state-owner` = e4af28c2).
- Task: t-20261018-r27-state-owner, PR #1347. Basis: review-1347g rezepte 1+2.
- Commit: 797bd811 (HEAD after merge of origin/develop). Pushed to
  `refs/heads/work/r27-state-owner`; remote `git ls-remote` == HEAD (verified match).
- Worktree: /tmp/opencode/w28-stateowner-r8-wt (checked out from work/r27-state-owner = e4af28c2).
- Scope: NUR tests. Produktcode unveraendert. Wenn ein Test produktcode-falsch befuerchtet: END_BLOCKED, kein Code-aendern.

## PLAN

1. Read mission + review-1347g; establish byte/load and list/owner requirements.
2. PUNKT 1: cmd/baha/deployment_tenant_scope_negative_regression_test.go — add valid-scope setup-record, capture on-disk bytes, then corrupt scope and assert Save+Load ErrUnavailable-chain with UNCHANGED bytes.
3. PUNKT 2(a): internal/deployment/deployment_owner_binding_test.go — list on owned-but-empty target, concrete empty semantics (not blanket err=nil).
4. PUNKT 2(b): existing record on foreign-owner target -> ErrDeploymentOwnerForeign specifically.
5. PUNKT 2(c): corrupt saved owner -> public List/ListForDisplay specific error/warning + unchanged record bytes.
6. Local go test green (belegte env-fail excluded).
7. Merge origin/develop, ancestry rc=0, ls-remote SHA, write-set only test files, push.

## PUNKT 1 — BYTE/LOAD-SETUP ECHT

File: cmd/baha/deployment_tenant_scope_negative_regression_test.go

`TestTenantScopeErrorRefusedAgainstExistingCoreOwner` previously asserted only
that the corrupt-scope Save refused and that NO state existed, then Load of the
non-existent record. That cannot prove "bytes unchanged" because no valid record
was ever written. Rewrote so the negative regression now:

- Establishes a REAL valid-scope config first (baseharbor-node-connector + valid
  reference), saves the record through `SaveDeploymentRecord` (real save path),
  reads the on-disk deployment.json bytes back.
- Then corrupts the scope (non-connector provider => connectorScopeForTarget
  fails with a real scope error) and re-runs Save + Load.
- Asserts BOTH Save and Load return the tenant-scope chain error
  (`errors.Is(cause, targetsession.ErrUnavailable)`), that no NEW state was
  persisted, and that the previously-saved on-disk bytes are byte-identical
  after the corrupt Save/Load (the corrupt write must not overwrite valid data).

This closes the review-1347g point 1 gap: the test no longer "besteht" without
the setup-record; the byte comparison is the proof that the seam fails closed on
the real Save/Load write seam.

## PUNKT 2 — LIST/OWNER MIT EXISTIERENDEN RECORD

File: internal/deployment/deployment_owner_binding_test.go

(a) `FindDeployment` on an owned-but-empty target: provision a valid owner for a
    second target, then `FindDeployment` returns concrete not-found
    (`found == false, err == nil`) and `ListDeployments` returns an empty list —
    the documented empty semantics for an owned target with zero deployments,
    not a blanket `err=nil` accept on a target that simply has no state dir.

(b) Existing record, foreign owner: provision a valid owner for a target, save a
    real record for it, then rewrite that target's installation.json so its
    `spec.target` is a foreign target. `LoadDeploymentRecord` on the existing
    record now fails with the SPECIFIC `ErrDeploymentOwnerForeign` (not any
    non-nil error), proving the public load seam rejects a foreign owner while
    the record exists.

(c) Corrupt saved owner, public seams: save a real record, capture its bytes,
    then corrupt the saved owner (invalid installation.json). Public
    `ListDeployments` (non-best-effort) fails closed with the specific owner
    error; public `ListDeploymentsForDisplay` (best-effort) surfaces a concrete
    warning instead of hard-failing, and the on-disk record bytes are unchanged.
    This exercises the PUBLIC seams (not the private `listDeploymentRecords`)
    against a corrupt OWNER (not corrupt record data), per review-1347g point 2.

Same-target installation-ID binding remains deferred (card note); no unrealistic
ID guarantee asserted.

## RUN EVIDENCE

- `go build ./cmd/baha/` → green.
- `go vet ./internal/deployment ./cmd/baha` → clean.
- `go test ./internal/deployment -count=1` → ok (all seam tests incl. the three
  reworked paths).
- `go test ./internal/deployment ./cmd/baha -run 'TenantScope|Negative|Deployment|Owner|List|Binding' -count=1`:
  internal/deployment ok; cmd/baha fails ONLY on
  `TestExternalProviderRemovalCannotInferGlobalOwnershipFromTenantRole`
  (`provider-registry-ownership-unverifiable`, pre-existing on clean develop,
  env/fixture, not introduced here — confirmed present on origin/develop).
- Ancestry: `git merge-base --is-ancestor origin/develop HEAD` → rc=0 (HEAD =
  797bd811, develop 9a57107f is ancestor).
- Write-set: only the two test files changed; no diff in deployment_store.go,
  remote_project.go, deployment_record.go, app_remote_binding.go (product code).
- Push: `origin HEAD:work/r27-state-owner`, remote `git ls-remote` == 797bd811
  == HEAD (verified match).

## END

END_DONE w28-stateowner-r8: head=797bd811 setup-record=echte-liste owner=foreign-spezifisch | byte/load setup-record + list/owner-on-existing-record, write-set only test files, FF from develop, remote sha == HEAD.
