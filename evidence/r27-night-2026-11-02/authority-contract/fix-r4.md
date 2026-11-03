# w8-authority-r4 — Verification evidence (t-20261018-r27-authority-contract)

**ROLE:** Worker, verification round on PR #1326. Coord `f49a3303`.
**Candidate inspected:** `09f14ec8e36a1fa5854e405404afc59f2b924ffc` (branch `w7-authority-r3-clean` head; worktree `/tmp/opencode/w8-authority-r4`, detached HEAD at candidate).
**Basis = w7 candidate, NOT PR-alt-head `81720acc`.** Remote `refs/heads/w7-authority-r3-clean` confirmed at candidate via `git ls-remote origin`.
**Reviewer reference:** `review-1326c2.md` (REJECT; Codex GPT-6, session `01a19e29-096b-76c2-8950-8018bf0b99ae`, 2026-11-03 04:51 UTC). Findings 1–3 are my mandate.

## PLAN
1. Read review-1326c2 + task card + candidate; open worktree on 09f14ec8.
2. Punkt 1: verify fail-closed revocation predicate + caller rejection semantics + tests.
3. Punkt 2: verify a real production call-site exists for the boundary-enforcing selection.
4. Punkt 3: verify observedAt freshness is used in a live (non-cached) fresh path.
5. Punkt 4: verify lock-file parity (stableid leaf + re-export + regression test).
6. Write this evidence; raise scope decision; END.

## Repo-rule compliance
- Read-only verification. No product files written. Worktree isolated at `/tmp/opencode/w8-authority-r4`.
- Build verified: `TMPDIR=/tmp go build ./...` → OK.
- Focused tests green: `./internal/coreinstallation`, `./internal/serviceaccess`, `./internal/stableid`, `./internal/openbao` (ok). `./internal/installauthority` has no test files. `./cmd/baha` subset (Resolve/Fresh/Selection/Revoked) ok.
- No merge, no push performed. No second cmd files touched.

## Finding 1 (Punkt 1) — FAIL-CLOSED revocation: IMPLEMENTED (verified)
- `internal/serviceaccess/local_issuer.go:323` `func (i *LocalIssuer) Revoked(ctx, serial) bool`:
  - `ctx.Err() != nil → false`; `i.load() err → false`; `revocations() err → false`; `list == nil → false`; malformed/non-positive/`BitLen()>159` serial → false. Every error path returns **false = reject**. No open-exception path.
  - Reuses private `revocations()` loader; **never writes** (no `Revoke` on verification path). Regression `TestRevocationIsReadonlyCrlUnchanged` asserts `revocations.pem` bytes unchanged.
- `internal/openbao/service_pki.go:314` `func revocationStatus(...)` + `service_issuer.go:90` `Revoked`: canonicalizes serial (bad serial → false), manager token (token/command failure → false), `exec` error (→ false), empty response (→ false). `revokedSerialInResponse` substring-matches canonical serial; empty → false. Fail-closed.
- Caller semantics: `serviceaccess.FreshlyObservedConnection` (authority.go:63) and `coreinstallation.AuthoritativeConnection` treat `issuer.Revoked(...) == true` as `ErrForeignAuthority`. `installauthority.Fresh` (fresh.go:67) likewise. So `err != nil || revoked == true` both reject. **No path downgrades "unknown" to accepted.**
- Tests: `coreinstallation/authority_test.go` `TestRevokedRevokedSerialRejectedNonMutating`, `TestRevokedMissingCrlFailsClosed` (missing CRL → not revoked → fails closed), `TestRevocationIsReadonlyCrlUnchanged`. **Punkt 1 satisfied.**

## Finding 2 (Punkt 2) — PRODUCTION SELECTION: GAP CONFIRMED (see QUESTION below)
- Boundary-enforcing wrapper `resolveManagementConnectionIssuer` (cmd/baha/application_service_issuer.go:89) **does** run `installauthority.Fresh(ctx, issuer, observed, observed.Identity)` over a real observed connection.
- **But it is called only by its own test.** Full call-site inventory:
  - `cmd/baha/application_service_issuer.go:90` (inside the wrapper itself)
  - `cmd/baha/application_service_issuer_test.go:114,135` (tests)
  - Production callers use the **older** `resolveApplicationServiceIssuer`, which runs `Status().Ready` but **NOT** `installauthority.Fresh` (no identity-match, no freshness, no revocation check):
    - `cmd/baha/app_up_lifecycle.go:213`, `app_apply_lifecycle.go:103`, `app_destroy_lifecycle.go:459`, `app_identity.go:196`, `application_restore_dependencies.go:40`, `application_gateway_retirement.go:48`, `application_identity_gateway_retirement.go:31`.
- **Consequence:** on the real production management-connection path, a foreign identity, an expired (stale) leaf, or a revoked serial is **not** rejected — it selects an issuer anyway. This is exactly REJECT finding #2; it remains **open** in the candidate.
- The intended fix per task card (composition-wiring authorization 2026-11-03): bind `serviceaccess.Issuer` into coreinstallation authority **only in `cmd/baha/application_service_issuer.go`**, no other cmd file. But the 7 prod call-sites are in OTHER cmd files; wiring must therefore go through the shared function `resolveApplicationServiceIssuer` (which lives in the authorized file) — however that function is used in BOTH the preflight phase (verification OK) AND the mutation phase (`app_destroy_lifecycle.go:459`), where the wrapper's `observedThroughBoundary` calls `issuer.Issue` (a certificate issuance = forbidden side-effect on a verification path, and a mutation-phase side-effect). See QUESTION.

## Finding 3 (Punkt 3) — OBSERVEDAT FRESHNESS: implemented+tested, NOT wired to a live non-cached caller
- `coreinstallation/authority.go` `ObservedState.Fresh(now)`: zero → `ErrInvalidObservation`, future → `ErrFutureObservation`, within window → fresh. `AuthoritativeConnection` runs `o.Fresh(time.Now())` **before** the boundary check (freshness reported, not downgraded).
- Tests present: `TestFreshWithinExpiresAt`, `TestFreshExpiredPastExpiresAt`, `TestFreshZeroRejected`, `TestFreshFutureRejected`, `TestAuthoritativeConnectionUsesObservedAtFreshness`.
- **Gap:** `AuthoritativeConnection` / `ObservedState.Fresh` are **not called from any production (non-test) code** (`grep` for `AuthoritativeConnection` / `ObservedState{...}` outside tests = none). The boundary's own `installauthority.Fresh` freshness uses `IssuedCertificate.ExpiresAt` (cert expiry), which is a DIFFERENT concept from `ObservedAt` (observation time). No production path enforces the `observed_at` freshness against a live, non-cached-READY observation. **Open pending scope decision** (same root cause as finding 2: no wired production entry that carries `ObservedAt` from a real selection).

## Finding 4 (Punkt 4) — LOCK PARITY: OK (verified)
- `internal/stableid/lock.go` (+ `lock_unix.go`, `lock_windows.go`, `lock_test.go`) — stdlib-only leaf. `internal/coreinstallation/lifecycle_lock.go:14` `AcquireLifecycleLock` re-exports unchanged signature. `serviceaccess/local_issuer.go:249` re-imports stableid (import swap only).
- Regression `internal/coreinstallation/lifecycle_lock_regression_test.go` present; `lock_windows.go` build-tag compiles (dup-export fixed in w7). **Point 4 satisfied.**

## Docs
- ADR 0021 (EN + DE), indexes, `target-access-v1.md`, `control-plane-runtime.md` present. Claims (fail-closed, observed-at enforced) partly exceed wired production surface. EN/DE parity + negation not independently byte-checked this round (not in mandate; points 1–3 are code).

## Net
- Punkt 1 ✅ implemented & tested. Punkt 4 ✅ implemented & tested.
- Punkt 2 ❌ OPEN (boundary wrapper orphaned; no prod call-site). Punkt 3 ⚠️ policy+tests present but not wired to a live non-cached caller.
- Root cause of 2 & 3 is shared: **no authorized production entry is wired to the new boundary.** Fixing requires a scope decision (issue-side-effect vs. 7 prod call-sites across non-authorized cmd files). This is an Owner/Coordinator decision, not a Worker write.

## END
**END_BLOCKED** w8-authority-r4: verification complete; Punkt 2 (and the wiring for Punkt 3) is an open gap that requires an Owner/Coordinator scope decision on how to bind the boundary into the production selection without an Issue side-effect in the mutation phase. Candidate 09f14ec8 alone is NOT a mergeable/clean candidate. No merge, no push.
