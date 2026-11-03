# w9-authority-r5 — review-1326c3 fix (t-20261018-r27-authority-contract)

- **ROLE:** Worker. Coord `f49a3303`. Fix of review-1326c3.md points 1 and 2
  (and Punkt 3 doc parity) on PR #1348 candidate head `3c63e8e0`
  (`w7-authority-r3-clean`).
- **Candidate:** `878be0db5f94c00454696c33ee44743b98c00984` (FF push to
  `w7-authority-r3-clean`, `3c63e8e0..878be0db`). Worktree `/tmp/opencode/w9-authority-r5-wt`.
- **Reviewer reference:** `review-1326c3.md` (REJECT; points 1–2 mandate).

## PLAN (checklist)
1. Read review-1326c3 + card notes; base = `3c63e8e0`.
2. Punkt 1: single tri-state `RevokedStatus` call in `installauthority.Fresh`;
   reject `err != nil || revoked`; drop boolean `Revoked()` from check path;
   LocalIssuer distinguishes empty CRL from unreadable; openbao parses+validates JSON.
3. Punkt 2: `Fresh(ObservedAt, maxAge)` zero/future/stale fail closed;
   `ObservedState.Fresh` single source; wrapper supplies observation time.
4. Punkt 3: ADR 0021 + target-access-v1.md EN/DE state behaviour-preserving
   lock relocation to `internal/stableid`.
5. build + vet + focused tests + wrapper e2e + doc audit; FF push; ls-remote.

## Repo-rule compliance
- Worktree isolated at `/tmp/opencode/w9-authority-r5-wt`, detached at base.
- Write-set vs develop: `docs` (ADR 0021 EN/DE, target-access-v1.md EN/DE),
  `internal/coreinstallation`, `internal/installauthority`,
  `internal/serviceaccess` (glue only), `internal/stableid`, authorized
  `cmd/baha/application_service_issuer.go`. No new cmd files; no `.github/scripts`.
- No force-push; FF only; no run-logs.

## Finding 1 (Punkt 1) — tri-state single call, verified
- `installauthority.Fresh` now takes `RevokedStatus(ctx, serial) (bool, error)`
  and rejects on `err != nil || revoked`. Exactly one authoritative call; no
  boolean `Revoked()` in the check path (boolean kept backward-compat, unused).
  `internal/installauthority/fresh.go` + `fresh_test.go`: `(false,nil)` accepts,
  `(true,nil)` rejects, `(nil,err)` rejects; call count == 1.
- `LocalIssuer.RevokedStatus` (serviceaccess): unreadable/unverifiable CRL →
  `errMissingRevocationStatus`; absent CRL is a valid readable "not revoked";
  malformed/non-positive/overflow serial → `errMalformedSerial`.
- `openbao ServiceIssuer.RevokedStatus`: parses+validates JSON, exact canonical
  serial match (not substring); empty valid list → not revoked; malformed JSON /
  failed provider / bad serial → `err != nil` (fail closed).
  `internal/openbao/service_issuer_test.go` covers all four.

## Finding 2 (Punkt 2) — observed-at freshness, verified
- `installauthority.Fresh(observedAt, maxAge)`: zero → `ErrInvalidObservation`,
  future → `ErrInvalidObservation`, `now - observedAt > maxAge` →
  `ErrStaleObservation`; default 5-min window when `maxAge == 0`.
- `coreinstallation.ObservedState.Fresh` is the single source (zero/future/stale
  with `MaxAge`); `CertificateStatus.ObservedAt` wired; wrapper
  `resolveManagementConnectionIssuer` supplies its own observation time.
  `cmd/baha` e2e `TestResolveManagementConnectionIssuerSuppliesObservedAtFreshness`
  proves recent accept + zero/future/stale reject through the real path.

## Finding 3 (Punkt 3) — lock relocation doc parity
- ADR 0021 + target-access-v1.md EN/DE state the lifecycle-lock primitives live
  in stdlib-only `internal/stableid`, behaviour-preserving relocated to break the
  `coreinstallation -> serviceaccess` cycle; `coreinstallation` re-exports with
  unchanged signatures; per-caller regression tests (`stableid/lock_test.go`,
  `coreinstallation/lifecycle_lock_regression_test.go`) prove parity.

## Tests (all green)
- `./internal/installauthority` (new), `./internal/coreinstallation`,
  `./internal/serviceaccess`, `./internal/stableid`, `./internal/openbao` (new
  `TestRevokedStatusParsesAndValidatesRevocationList`) pass.
- `./cmd/baha` `TestResolveManagementConnectionIssuer*` +
  `TestApplicationServiceIssuer*` pass.
- `go build ./...`, `go vet` clean.
- Doc audit: structure PASS, DE technical integrity PASS (160 paired pages),
  EN/DE coverage OK.

## Push
- FF push `origin 878be0db:w7-authority-r3-clean`: `3c63e8e0..878be0db`.
- **ls-remote verified** `refs/heads/w7-authority-r3-clean` == `878be0db`.
- No force-push, no run-logs.

## develop-merge (coordinator Pflichtschrift)
- `develop` (9a57107f) was NOT an ancestor of `878be0db` (develop continued,
  incl. profile-squash #1324). Merged `origin/develop` in an isolated worktree
  (`/tmp/opencode/w9-authority-r5-merge`, detached at `878be0db`); 'ort' strategy,
  no content conflicts (profile/credential files re-added by develop).
- New merge commit `f58fb18054265ae247858fa3ce1b2b915aca8a77`.
- Build: `go build ./...` OK.
- Tests: `./internal/installauthority ./internal/coreinstallation ./internal/serviceaccess ./internal/stableid` PASS; `./cmd/baha` core-authority tests PASS. The only `cmd/baha` failures are environmental (Docker daemon unavailable,
  provider-registry ownership unverifiable without remote state) and fail
  identically on clean `develop`.
- FF push `origin HEAD:w7-authority-r3-clean`: `878be0db..f58fb180`.
- **merge-base --is-ancestor origin/develop HEAD → rc=0** (develop now ancestor).
- **ls-remote** `w7-authority-r3-clean` == `f58fb180` == HEAD. No force-push,
  no content change beyond the develop merge.

## END
**END_DONE** w9-authority-r5: review-1326c3 points 1–2 fixed + Punkt 3 doc parity;
build/vet/focused tests/wrapper e2e/doc audit all PASS; FF-pushed to
`w7-authority-r3-clean` (878be0db, ls-remote verified), then merged develop
(pfo858fb180, ls-remote verified == HEAD, merge-base --is-ancestor origin/develop rc=0);
no force-push. PR #1348 head unchanged by this lane (no new PR); no merge (out of
worker scope).
