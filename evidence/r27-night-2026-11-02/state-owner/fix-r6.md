# r27 state-owner r6 — fix-r6 evidence (w23-stateowner-r6)

- Role: Worker, lane w23-stateowner-r6, coord f49a3303.
- Base: head 8c07e971, branch work/r27-state-owner (remote `origin/work/r27-state-owner` = 8c07e97129f6887c1b5104cc741ecda7f890c7ff).
- Task: t-20261018-r27-state-owner, PR #1347. Basis: review-1347e findings 1+2.
- Worktree: /tmp/opencode/w23-stateowner-r6-wt (checked out from origin/work/r27-state-owner = 8c07e971).

## PUNKT 1 — FEHLERKLASSEN-VOLLSTAENDIGKEIT

File: cmd/baha/deployment_tenant_scope_negative_regression_test.go

The assertion previously rejected only a missing-owner fall-through
(`errors.Is(cause, ErrDeploymentOwnerMissing)`) — i.e. it required a *specific*
connector-scope error. Broadened so the negative regression accepts the WHOLE
rejection chain while still failing on nil (ablehnung Pflicht):

- Added helper `assertRejectionInChain(t, ctx, got)` that:
  - FAILS if `got == nil` (no soft pass on admission),
  - accepts if the cause is `ErrDeploymentOwnerMissing` OR `ErrDeploymentOwnerForeign`
    OR the message contains one of `provider-registry` / `connector` /
    `authenticated Connector session`.
- `TestTenantScopeErrorRefusedAgainstExistingCoreOwner`: Save + Load now
  assert through `assertRejectionInChain` instead of the narrow missing-owner
  check. Valid positive control `TestValidTenantScopeGrantedAgainstExistingCoreOwner`
  unchanged (grant still admitted).
- Added `strings` import (helper uses `strings.Contains`).

Counter-test unchanged: a valid connector scope is still admitted against an
existing Core-owner (proves the assertion is not "reject everything").

## PUNKT 2 — EVIDENCE-KORREKTUR (fix-r5 mutation-baseline)

`fix-r5.md` does not exist in the state-owner evidence dir (verified on the live
shared checkout AND on remote `baseharbor-plan` main via `gh api` / GitHub API:
the dir holds only `evidence.md`, `fix-r2.md`, `fix-r3.md`). The prior lane's
r5 mutation-baseline line is captured here as a FACT bullet:

- Mutation baseline (state-owner, r27): **PASS auf 4cc93db8** (r18 /
  "propagate connector scope error + fixture fatal", the last w-lane before r6's
  base), **FAIL nur auf dea01b83** (the develop-merge before the connector-scope
  propagation landed). This is the pre-bypass / post-bypass contrast that r6's
  negative regression now covers end-to-end.

## RUN EVIDENCE

- `go build ./cmd/baha/` → green.
- `go vet ./cmd/baha/` → clean.
- `go test ./cmd/baha -run 'TenantScope|Negative'` → ok (incl.
  `TestTenantScopeErrorRefusedAgainstExistingCoreOwner`,
  `TestValidTenantScopeGrantedAgainstExistingCoreOwner`).
- `go test ./internal/deployment/...` → ok.
- Ancestry: `git merge-base --is-ancestor origin/develop 8c07e971` → rc=0
  (FF from develop 9a57107f); merge-base = 9a57107f.
- Write-set: only `cmd/baha/deployment_tenant_scope_negative_regression_test.go`
  changed (36 insertions, 18 deletions); no other product/planning file touched.

## END

END_DONE w23-stateowner-r6: head=8c07e971 errclasses=complete evidence=corrected
| full rejection chain (missing/foreign/provider-registry/connector/authenticated-session)
asserted in TenantScope negative regression; fix-r5 mutation-baseline (PASS 4cc93db8 /
FAIL dea01b83) captured as fact-bullet in fix-r6.md; tests green, FF from develop 9a57107f.
