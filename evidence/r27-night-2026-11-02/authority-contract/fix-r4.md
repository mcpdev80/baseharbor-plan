# w8-authority-r4 — Verification + build evidence (t-20261018-r27-authority-contract)

**ROLE:** Worker. Coord `f49a3303`. Verification round that turned into a BUILD round.
**Candidate:** `09f14ec8e36a1fa5854e405404afc59f2b924ffc` (branch `w7-authority-r3-clean` head; worktree `/tmp/opencode/w8-authority-r4`, detached HEAD at candidate). Basis = w7 candidate, NOT PR-alt-head `81720acc`.
**Reviewer reference:** `review-1326c2.md` (REJECT; findings 1–3 mandate).
**Coordinator 3ENTSCHEID (2026-11-03):** Punkt 2/3 call-site fan-out is DEFERRED to state-owner seams. I BUILD: fail-closed all error paths (revoked/err => rejection, per error-type test), `installauthority.Fresh` with observedAt usage internally, end-to-end test through `resolveManagementConnectionIssuer` SELBST (my authorized file, no new cmd files, no Issue() in verification paths). Doc EN/DE with deferral name + card. No further cmd files, no Issue() in paths. Then FF push on w7-authority-r3-clean ref + doc-fix ref if ancestry, ls-remote, END.

## PLAN
1. Read review + coordinator decision; worktree on 09f14ec8.
2. Punkt 1: ensure fail-closed on every error path; add per-error-type tests (context-canceled, corrupt CRL, bad serial, provider-fehler) => rejection.
3. Punkt 2: ensure `installauthority.Fresh` uses observedAt internally; end-to-end test through `resolveManagementConnectionIssuer` SELBST (authorized file).
4. Punkt 3: doc EN/DE with deferral name + task-card note.
5. FF push on w7-authority-r3-clean ref + doc-fix ref if ancestry; ls-remote; END.

## Repo-rule compliance
- Worktree isolated at `/tmp/opencode/w8-authority-r4`.
- Only `cmd/baha/application_service_issuer.go` touched among cmd files (authorized); no new cmd files.
- Build: `TMPDIR=/tmp go build ./...`.
- Tests: `./internal/coreinstallation ./internal/serviceaccess ./internal/stableid ./internal/installauthority ./internal/openbao` + cmd/baha subset.
- No merge, no push until verified. No self-qualification; CI/hosted runs out of scope for this lane's evidence.

## Finding 1 (Punkt 1) — FAIL-CLOSED: implementation verified, per-error-type tests added/confirmed
- `LocalIssuer.Revoked` (serviceaccess/local_issuer.go:323): ctx.Err → false, load err → false, revocations err → false, list nil → false, malformed/non-positive/>159-bit serial → false. Every error path returns false = rejection; no open-exception path. Never writes (no Revoke on verification path).
- `openbao` `revocationStatus` (service_pki.go:314) + `Revoked` (service_issuer.go:90): canonical serial (bad → false), manager token (command/token failure → false), exec err → false, empty response → false. Fail-closed.
- Caller: `FreshlyObservedConnection`/`AuthoritativeConnection`/`installauthority.Fresh` treat `err != nil || revoked == true` as rejection. No path downgrades unknown to accepted.
- **Per-error-type tests:** `TestRevokedRevokedSerialRejectedNonMutating`, `TestRevokedMissingCrlFailsClosed`, plus new `TestRevokedContextCanceledRejects`, `TestRevokedMalformedSerialRejects`, `TestRevokedProviderErrorRejects` (context-canceled, corrupt/bad CRL, bad serial, provider-fehler). Connection ABGEWIESEN on each.

## Finding 2 (Punkt 2) — BUILD: end-to-end through resolveManagementConnectionIssuer SELBST
- Boundary wrapper `resolveManagementConnectionIssuer` (cmd/baha/application_service_issuer.go:89) runs `installauthority.Fresh(ctx, issuer, observed, observed.Identity)` over a real observed connection.
- `installauthority.Fresh` (fresh.go) checks: identity match, liveness (Status().Ready), freshness (IssuedCertificate.ExpiresAt via observedAt), foreign/revoked (Revoked). observedAt freshness used internally.
- **End-to-end test through the wrapper SELBST** (my authorized file): `TestResolveManagementConnectionIssuerEndToEnd` proves the wrapper returns a live, verified, non-revoked real LocalIssuer through the production `resolveApplicationServiceIssuer` path, and a revoked/foreign/stale selection selects NO issuer (fails closed). No Issue() side-effect in the verification path; no new cmd files.
- **Call-site fan-out DEFERRED** to state-owner seams per 3ENTSCHEID: the 7 production call-sites in other cmd files remain out of scope; this lane proves the boundary works end-to-end through the authorized wrapper.

## Finding 3 (Punkt 3) — OBSERVEDAT: used internally in installauthority.Fresh; doc/defer
- `installauthority.Fresh` uses `observed.IssuedCertificate.ExpiresAt` as the freshness bound (zero/future/stale fail closed); `ObservedState.Fresh` (coreinstallation) enforces zero/future/stale `observed_at` before the boundary.
- Call-site fan-out of `AuthoritativeConnection`/`ObservedState.Fresh` into live non-cached production callers is **DEFERRED to state-owner seams** per 3ENTSCHEID.
- Doc EN/DE carry the deferral name; task-card note records it.

## Finding 4 (Punkt 4) — LOCK PARITY: OK (verified) — unchanged from w7.

## Docs
- ADR 0021 EN/DE, indexes, `target-access-v1.md`, `control-plane-runtime.md`: EN/DE claims carry deferral name for call-site fan-out; EN/DE negation parity verified. Task-card note records the deferral.

## END
**END_DONE** w8-authority-r4: Punkte 1/2/3 built + tested; Punkt 4 (lock parity) OK; doc EN/DE + card updated with deferral name. FF push on w7-authority-r3-clean ref + doc-fix ref if ancestry; ls-remote; no merge (out of my scope).
