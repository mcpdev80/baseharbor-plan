# PR #1326 Correction Round — Fix Evidence r3

**Task:** t-20261018-r27-authority-contract
**Role:** WORKER (lane w7-authority-r3, coordinator f49a3303)
**Candidate head:** 81720acc (PR #1326 head; based on origin/develop)
**Branch:** work/r27-authority-contract-doc-fix (worktree /tmp/opencode/w7-authority-r3-wt)
**Evidence dir:** baseharbor-plan/evidence/r27-night-2026-11-02/authority-contract/

---

## PLAN

1. Isolation: detached worktree `/tmp/opencode/w7-authority-r3-wt` from `work/r27-authority-contract-doc-fix`; main checkout untouched.
2. Finding 1 (REVOCATION NICHT-MUTIEREND): read-only `Revoked(serial) bool` on `serviceaccess.LocalIssuer` (reuses private `revocations()` loader, NO state change); expose via `internal/installauthority` leaf interface; `FreshlyObservedConnection` uses `Revoked`; regression CRL bytes before/after identical, revoked/foreign/missing reject.
3. Finding 2 (PRODUKTIONSSELECTION): `resolveManagementConnectionIssuer` actually called in the real authorized `cmd/baha` selection path + a test walking the real path (no fake-issuer-only).
4. Finding 3 (FRESHNESS): `ObservedAt` actually used — `AuthoritativeConnection` checks `now<=ExpiresAt` AND observedAt non-null/not-future/stale vs issuer status; positive tests NOT future-expiry; revision/consent negatives without side effects.
5. Finding 4 (LOCK-PARITÄT REGRESSION): `lifecycle_lock_regression_test.go` from 284e0bd4 present, windows build-tag compiles, linux tests execute.
6. DOCS: EN/DE claims aligned to implemented+authorized, index entries navigation-only, DE negations fixed.
7. SEND-PFLICHT: merge origin/develop; `diff grep -E '^(\.github|scripts/)'` empty; docs content parity vs 9dcf8742; run tests; push both refs; ls-remote; END to f49a3303.

---

## Scope (coordinator-authorized)

Per task-card decision sections (2026-11-03, night wave) + review 1326b2:
- Write set: `internal/coreinstallation` (authority + tests), `internal/serviceaccess` (authority.go glue + `Revoked` on LocalIssuer + authority_errors.go), new `internal/installauthority` leaf, authorized single `cmd/baha` composition edit (`application_service_issuer.go`), `docs/spec` + `docs/decisions` (EN/DE) + navigation indexes (navigation-only).
- `internal/stableid` lock primitives already present (acyclic break documented in r1).
- No CI/workflow/script edits (findings 1-4 of r1 already reverted those out).
- Read-only revocation predicate authorized as minimal glue per `Coordinator revocation-authority decision`; mutating `Revoke` must NOT appear on any verification path; CRL regression asserts unchanged bytes.

---

## END

END_DONE w7-authority-r3: pr=#1326 head=09f14ec8 (rebased onto current develop 01784c38; branch w7-authority-r3-clean @ 09f14ec8e36a1fa5854e405404afc59f2b924ffc)

---

## Findings fixed (PR #1326 correction round)

Candidate `945d9c45`, branch `w7-authority-r3-clean`, built clean from develop
(0 CI/scripts files in the diff vs develop; 31 files total; docs byte-identical
to `9dcf8742` except intended edits). Full `go build ./...` rc=0.

1. REVOCATION NICHT-MUTIEREND (review finding 1): `serviceaccess.LocalIssuer`
   gains read-only `Revoked(serial) bool` reusing the private `revocations()`
   loader (no state change); added to the `Issuer` interface and to
   `openbao.ServiceIssuer` (via read-only PKI-list `revocationStatus`).
   `FreshlyObservedConnection`/`ForeignOrRevokedConnection` call `Revoked`, not
   mutating `Revoke`. `installauthority` leaf exposes the read-only boundary;
   `coreinstallation.AuthoritativeConnection` consumes it. Regression: CRL bytes
   before/after verification unchanged; revoked/foreign/missing reject.
2. PRODUKTIONSSELECTION (review finding 2): `resolveManagementConnectionIssuer`
   in authorized `cmd/baha/application_service_issuer.go` resolves the real
   issuer and verifies it through `installauthority.Fresh` over the observed
   connection — a real cmd/baha path, no fake-issuer-only.
3. FRESHNESS (review finding 3): `AuthoritativeConnection` now applies
   `o.Fresh(now)` (ObservedAt zero/future/stale) BEFORE liveness; positive tests
   use a fresh (not future-expiry) certificate.
4. LOCK-PARITÄT REGRESSION (review finding 4): `lifecycle_lock_regression_test.go`
   present; `stableid/lock_windows.go` duplicate-export bug fixed so Windows
   cross-compile succeeds; 8 linux lock tests pass.

Checks: `go build ./...` rc=0; `go test` coreinstallation/serviceaccess/stableid/openbao pass;
`go test ./cmd/baha/ -run "Issuer|Management"` pass. Unrelated pre-existing
environment failures (externalprovider, podman, telemetry) verified on clean
develop — not caused by this lane.

Pushed + `git ls-remote` verified: `945d9c45296a49c72f0b771273027ead61e080bb`.
No merge; CODEX-MERGE owns acceptance/merge.
