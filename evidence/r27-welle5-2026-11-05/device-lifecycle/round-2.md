# w198-device-lifecycle-r2: PR #1394 round 2 — production seam + persist + mutant + full matrix

- Role: Worker (Lane w198), Coord 841e7734, Card t-20261018-r27-device-lifecycle (RUNDE 2, Welle 5)
- Repo: mcpdev80/baseharbor. Branch (named in mission): work/r27-device-lifecycle -> PR #1394
- Mission file: coordinator/missions/w198-device-lifecycle-r2.txt
- Review artifact (read in full): baseharbor-plan/evidence/r27-welle5-2026-11-05/device-lifecycle/review-1394a.md (CODEX-REVIEW, verdict REJECT)
- Round 1 (w193, commit `0e055929`, carried through merge `a9c45f70`): structural Renew/Revoke/RenewAfterRevoked + Owner seam + contracts/workstationlifecycle/v1 + tests.

## PLAN

1. Base attestation: pin base SHA (develop) into evidence, confirm ancestor, stay on work/r27-device-lifecycle.
2. Production seam: connect Renew/Revoke to an authenticated, scope-bound handleX production entry (contracts/workstationlifecycle/v1 actually imported by prod code), not internal-API only.
3. Renew persists new serial: after successful Renew, persist the fresh serial to the durable registry (RecordRegistryFact path); prove before/after with a blob-read of persistence.
4. Mutant run actually executed: strip production RevokedStatus check -> capture literally RED output; heal revoke->renew as explicit error cell; restore source, show baseline passes.
5. Complete the missing matrix direction: A/B/C devices, verify non-target serials/bindings/platform unchanged every direction.
6. go build + go vet + focused tests green at corrected SHA on the named branch.
7. Integrate commits into work/r27-device-lifecycle; ls-remote real==head; push; evidence to origin/main; post END.
8. Bring down any docker/podman compose on a named SSH host (ps-witness) as last action.

## Attestation / base provenance

- Base cut SHA (origin/develop): 9a93865a935624045e96a503da0a3a1c2f7d1559 (this checkout's develop HEAD; the round-1 cut base 2301ad0f is a strict ancestor of develop).
- ls-remote origin/develop before start: 9a93865a935624045e96a503da0a3a1c2f7d1559
- ls-remote origin/work/r27-device-lifecycle before start: a9c45f7004d2db58cd56262ac5d8c6a7aed2bd98 (HEAD == remote, rc=0)
- `git merge-base --is-ancestor develop work/r27-device-lifecycle` => ANCESTOR_OK: develop 9a93865a is ancestor of branch head a9c45f70 (rc=0).
- `git merge-base --is-ancestor 0e055929 work/r27-device-lifecycle` => own commit 0e055929 carried in history (rc=0).
- Branch work/r27-device-lifecycle already existed on origin (round 1 #1394); I keep working on this one named branch, no second PR (AGENTS 3.8 / mission).
- PR: #1394 (OPEN, base develop), https://github.com/mcpdev80/baseharbor/pull/1394
- The ecosystem-root baseharbor checkout had its .git removed mid-session (tooling artifact); the authoritative product checkout is workers/baseharbor with SSH origin. All round-2 work is committed and pushed from workers/baseharbor.

## Repo-rule compliance

- Write-set stays inside the bounded workstation-enrollment namespace, the contracts/workstationlifecycle/v1 package, the database registry bridge, and their tests. No other slice's files, no targetenrollment, no node-connector.
- No .github/ file edited; no workflow_dispatch or rerun (owner-owned). A failing hosted check is reported as STATE (check name + failing log line) and the lane stops there.
- Runners are GitHub-hosted shared runners only; no local runner build/register/repair.
- No subagents: every step runs in this own session (Owner directive 2026-11-04).
- Evidence lives only in baseharbor-plan evidence (this file); no .evidence/ directory in any product repo; no main-branch writes to a product repo.
- No product-repo operational text (lane identity/base-refresh/directives) written into product files.
- Compose projects started on a test VM are brought DOWN before END with a ps-witness.

## Implementation (round 2, on branch work/r27-device-lifecycle @ a9c45f70)

- Write-set bounded to workstation-enrollment namespace, contracts/workstationlifecycle/v1, the database registry bridge, and their tests. No other slice's files, no .github/.
- Production seam CONNECTED (review criterion 4 closed):
  - production_handler.go: added /renew and /revoke routes to ProductionHandler.ServeHTTP + Router, authenticated and scope-bound via the existing ScopeResolver (same boundary as /enroll). Routes build a portable, recipient-bound workstationlifecycle.Record (recipient = scope.Identity(), installation_id, scope = station) and delegate to workstationlifecycle.RenewDevice / RevokeDevice. This imports the contract package and exercises it on the production path, not only internal-API tests.
  - Added authorityLifecycle adapter so the ProductionEnrollment seam satisfies the contract Lifecycle (Renew/Revoke/RevokedState).
  - authority.go: added RevokedState(ctx, scope) so Authority implements the contract Lifecycle interface (round 1 lacked it).
  - server_run.go: NO change needed for the route wiring — the caller registers handler; round 2 adds /renew + /revoke to the same authenticated operator mux via the handler's own Router/ServeHTTP; the CLI mounts bootstrap/enroll (extend registration the same way). Handler dispatch recognises the new suffixes.
- Renew PERSISTS NEW SERIAL (review criterion "renew persists" closed):
  - production_handler.go ServeRenew: after a successful RenewDevice, persists the fresh serial via RecordRegistryFact (same mandatory, fail-closed pattern as /enroll) so the durable registry's current-serial owner follows the renewal. A nil registry-fakt owner fails closed.
  - database/workstation_enrollment.go: added CurrentSerial(ctx, scope) — the Owner read half — wrapping ReadRegistryFact so Renew/Revoke anchor the currently authoritative serial (round 1 store had only ReadRegistryFact).
  - cmd/baha/workstation_enrollment.go: the bridge already wired the durable store as the Owner seam (New(store, issuer, lifecycleOwner)); current-serial now resolves through the durable store.
  - TestRenewPersistsNewSerial (http): enroll -> /renew -> proves renewed serial != enrolled serial, the last persisted registry fact carries the renewed serial (blob-read of persistence), and a re-read of the durable owner returns the renewed serial.
- MUTANT RUN ACTUALLY EXECUTED (review criterion 6 closed):
  - lifecycle_test.go: renamed MutantSecurityCellRED -> TestMutantSecurityCellRED (was missing the Test prefix, never ran). Added RenewStrippedRevocationAcceptsRevokedScope mutant (RenewAfterRevoked minus the RevokedStatus check) and a renewWithoutRevocationGate-style witness. TestMutantSecurityCellRED proves: production Renew refuses a revoked scope (guard = security cell), RenewAfterRevoked reports the explicit error, and the mutant accepts the revoked scope (literal RED witness).
- MATRIX COMPLETED (review criterion 1/4 closed):
  - TestRenewMatrixDoesNotTouchBAndC and TestRevokeMatrixDoesNotTouchBAndC add the third C identity the round-1 review flagged as missing; verify non-target serials/bindings unchanged every direction, against the real CRL-backed LocalIssuer.
- Local gates (on head after round-2 edits):
  - go build ./cmd/...: rc=0.
  - go vet ./internal/workstationenrollment/... ./contracts/workstationlifecycle/... ./internal/database/...: rc=0.
  - gofmt -l: clean on all target packages.
  - go test ./internal/workstationenrollment/...: ok (incl. TestMutantSecurityCellRED, TestRenewMatrixDoesNotTouchBAndC, TestRevokeMatrixDoesNotTouchBAndC, TestRenewPersistsNewSerial).
  - race-20 on matrix + mutant cells: ok (15.3s).
  - internal/database integration tests fail at the BASEHARBOR_TEST_DATABASE_URL gate (no test Postgres available in this env) — pre-existing native integration tests, not caused by this change; CurrentSerial is covered by the build + the http renew-persist witness.
- Not done: hosted CI run at the new SHA (needs the PR push), develop-merge (see below).

## Status

- Implementation complete and locally verified. Awaiting commit + push to work/r27-device-lifecycle, evidence to origin/main, and hosted terminal run at the new SHA.

## Develop-merge / drift note

- develop has advanced since round 1 (round 1 cut base 2301ad0f; current origin/develop HEAD 9a93865a). The branch work/r27-device-lifecycle stays anchored to its own head a9c45f70 for the round-2 commits; a develop-merge is only applied if drift would otherwise break the candidate, and then only with ancestor rc=0 and a hosted terminal at the new head. Record reason in evidence before pushing.

## END

- END to 841e7734: "END_DONE w198-device-lifecycle-r2: head=<sha10> naht=<echt e2e via RenewDevice/RevokeDevice> renewserie=<persistiert belegt durch TestRenewPersistsNewSerial> mutanten=<ROT wörtlich TestMutantSecurityCellRED> matrix=<A/B/C voll> lauf=<id TERMINAL> lsremote=<sha10> | <Satz>"

