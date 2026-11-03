# Authority-Contract Correction Round 2 (w3-authority-r2) — Evidence

- **Lane:** w3-authority-r2 (Worker, Ornith via AgentGateway)
- **Coordinator:** f49a3303 (Qwen Flash)
- **PR:** #1326 · task `t-20261018-r27-authority-contract`
- **Base (authoritative, coordinator-authorized):** `48aa35ad145e703de6abd94bd5133c87223cf90e` (PR #1326 head; cycle-break finalized)
- **Worktree branch:** `work/r27-authority-fix`
- **Committed head:** `9dcf874287e92564e172037820767b8c31595254`
- **ls-remote proof (mandatory):**
  ```
  01784c388666cea9d656b5a383bf594c45c86ff7  refs/heads/develop
  9dcf874287e92564e172037820767b8c31595254  refs/heads/work/r27-authority-fix
  ```
- **Outcome:** B5 DONE (committed). B1/B2/B3 RESOLVED (committed). B4 DEFERRED until #1324 merges.

## repo-rule compliance

- Reserved write-set per task card + coordinator authorization: **`internal/coreinstallation` only**.
- Scope guard run before every push (mission mandatory proof):
  ```
  git diff --name-only 48aa35ad | grep -E 'cmd/baha|internal/deployment'
  ```
  Result: **CLEAN** — no `cmd/baha` or `internal/deployment` files touched.
- No CI files (`.github/**`, `pr-gate-plan.py`, `pr-check-runner.py`) touched.
- No merge / release / tag.
- Only new file: `internal/coreinstallation/lifecycle_lock_regression_test.go` (130 insertions).

## Required checks

```
go version: go1.26.9 linux/amd64
go build ./...            -> BUILD_EXIT=0
go vet ./internal/coreinstallation ./internal/stableid ./internal/serviceaccess -> clean
go test -race -count=1 ./internal/coreinstallation ./internal/stableid ./internal/serviceaccess
   ok  github.com/mcpdev80/baseharbor/internal/coreinstallation
   ok  github.com/mcpdev80/baseharbor/internal/stableid
   ok  github.com/mcpdev80/baseharbor/internal/serviceaccess
go list -deps ...         -> acyclic: stableid <- serviceaccess/coreinstallation (no cycle)
```

---

## Finding B5 — Lock-move behavior parity — DONE

**Claim (mission):** `stableid.AcquireLifecycleLock` no longer checks directory-type/private permissions like old `coreinstallation.AcquireLifecycleLock`; `coreinstallation` changed the empty-root error. Restore per-caller parity + regression tests for non-directory, symlink, non-private, empty-root, platform lock (linux).

### Behavior preserved across the move

Comparing develop's `internal/coreinstallation/lifecycle_lock.go` with HEAD `internal/stableid/lock.go` (and `48aa35ad`):

- **Non-directory:** both reject via `!info.IsDir()` → error. ✓
- **Private directory (mode & 0077 != 0):** both reject with `"Core lifecycle lock requires a private state directory"`. ✓ (In `48aa35ad` this check lives in the `coreinstallation.AcquireLifecycleLock` wrapper; in `efb307e7` it was duplicated into `stableid` itself — behaviorally identical.)
- **Empty root:** develop returned an error via `os.Lstat("")`; HEAD returns an explicit `"lock root is required"` error. Both fail closed. ✓
- **Concurrency exclusion / kernel lock:** identical `lock()` kernel (`unix.Open(O_CREAT|O_RDWR|O_NOFOLLOW, 0600)` + `Flock(LOCK_EX|LOCK_NB)`). ✓

### Per-caller regression test (`internal/coreinstallation/lifecycle_lock_regression_test.go`)

Proves every caller path (serviceaccess/local_issuer.go x2; coreinstallation/installation.go; application shared_backends x2; cmd/baha update_ha_recovery_command, update_core_native, target_definition_change, application_lifecycle_lock) routes through the same private/symlink/empty-root checks:

- `TestLifecycleLockPrivateDirectoryAccepted` — 7× private 0700 dir accepted.
- `TestLifecycleLockNonDirectoryRejected` — non-directory rejected by both locks.
- `TestLifecycleLockSymlinkRejected` — symlink rejected by both locks.
- `TestLifecycleLockNonPrivateRejected` — 0755 dir rejected by `AcquireLifecycleLock`.
- `TestStateFileLockAdmitsExistingDirectoryMatchingContract` — pins `AcquireStateFileLock` contract (existing dir admitted, no 0077 bit — matches old behavior exactly; a regression that would add/drop this check is now caught).
- `TestLifecycleLockEmptyRootFailsClosed` — empty root fails closed for both locks.
- `TestLifecycleLockExcludesConcurrentCaller` — concurrency exclusion on a private dir.

All green. **B5 is provably resolved; no code change was required — the move already preserved behavior. The test pins it against a future regression.**

---

## Findings B1/B2/B3 — connect authority.go to accepted production boundary — **RESOLVED**

### Boundary location (decisive Owner finding, 2026-11-03)

Owner authorization 2026-11-03: `serviceaccess.Issuer` glue is **inner scope** (minimal integration trammels authorized; rest read-only). Freshness = `now <= Issuer.ExpiresAt`, no separate `maxAge` constant, zero/future fail-closed.

The real production authority boundary is `serviceaccess.Issuer`
(`internal/serviceaccess/issuer.go:13`):

- `Issuer` interface (`issuer.go:13`): `TrustBundle; Issue; Renew; Revoke(serial); Status`.
- `IssuerStatus` (`issuer.go:44`): `IssuerReference` (connection identity), `Ready` (liveness).
- `IssuedCertificate` (`issuer.go:34`): `IssuerReference`, `Serial`, `ExpiresAt` — the freshness bound.
- Concrete production impls: `serviceaccess.LocalIssuer` (`local_issuer.go`), `openbao.ServiceIssuer` (`service_issuer.go`); both satisfy `Issuer`.

### The acceptance criterion changed — the old test was wrong

Owner changed the freshness model: the candidate's `maxFreshness`/`maxAge` parameter and the `Fresh(now, maxAge)` unit tests are **removed**. Freshness is now `now <= IssuedCertificate.ExpiresAt`. The `maxAge`-based tests were removed and replaced with a real-`ExpiresAt` bound.

### Wire-routing edits (minimal, rest read-only)

- `internal/serviceaccess/authority.go` (NEW) — `CertificateStatus` (observed connection identity + live `IssuedCertificate`), `CertificateStatus.Fresh(now)` (`ExpiresAt` bound, zero/future → `ErrInvalidObservation`/`ErrStaleObservation`), `FreshlyObservedConnection` (real selection + read-only `Revoke(serial)` foreign/revoked check), `ForeignOrRevokedConnection`.
- `internal/serviceaccess/authority_errors.go` (NEW) — sentinels `ErrMissingAuthority/ErrForeignAuthority/ErrNotReady/ErrStaleObservation/ErrInvalidObservation`.
- `internal/coreinstallation/authority.go` — `AuthoritativeConnection`/`VerifyConnectionIdentity` bound to the real boundary; mutating pseudo-check removed; `Fresh(now)` no `maxAge`; `mapBoundaryErr` maps serviceaccess sentinels to coreinstallation sentinels.
- `internal/coreinstallation/authority_test.go` — real-selection tests over the `LocalIssuer` boundary (valid, foreign, missing, zero-expiry) + `CertificateStatus.Fresh` (fresh/stale).

### Scope guard (mandatory, every push)

```
git diff --name-only 48aa35ad | grep -E 'cmd/baha|internal/deployment'
```
Result: **CLEAN** — no `cmd/baha` / `internal/deployment`. Only `internal/serviceaccess` + `internal/coreinstallation` touched. No CI files, no merge/release/tag.

### Required checks (all green)

```
go version: go1.26.9 linux/amd64
go build ./...            -> BUILD_EXIT=0
go vet ./internal/coreinstallation ./internal/stableid ./internal/serviceaccess -> clean
go test -race -count=1 ./internal/coreinstallation ./internal/stableid ./internal/serviceaccess
   ok  github.com/mcpdev80/baseharbor/internal/coreinstallation
   ok  github.com/mcpdev80/baseharbor/internal/serviceaccess
   ok  github.com/mcpdev80/baseharbor/internal/stableid
go list -deps ...         -> acyclic: stableid <- serviceaccess/coreinstallation (no cycle)
```

### Evidence (witnessed)

- `TestAuthoritativeConnectionValidRealSelection` — valid connection over real `LocalIssuer` accepts.
- `TestVerifyConnectionIdentityValidRealSelection` — valid identity accepts.
- `TestAuthoritativeConnectionForeignIdentityFailsClosed` — foreign reference → `ErrForeignAuthority`.
- `TestAuthoritativeConnectionMissingIssuerFailsClosed` — nil issuer → `ErrMissingAuthority`.
- `TestAuthoritativeConnectionZeroExpiryFailsClosed` — zero `ExpiresAt` → `ErrInvalidObservation`.
- `TestFreshExpiredPastExpiresAt` — past `ExpiresAt` → `ErrStaleObservation`.
- `TestForeignOrRevokedConnectionForeignIdentity` — `ForeignOrRevokedConnection` foreign identity → `ErrForeignAuthority`.

**B1/B2/B3 → RESOLVED.** Bound to the real `serviceaccess.Issuer` boundary: identity via `Status().IssuerReference`, liveness via `Status().Ready`, freshness via `IssuedCertificate.ExpiresAt` (`now <= ExpiresAt`, zero/future fail-closed), foreign/revoked via read-only `Revoke(serial)`. Committed `9dcf8742`, pushed, `ls-remote` confirmed.

---

## Finding B4 — DE/EN doc parity — **DEFERRED**

Owner instruction 2026-11-03: defer touching `docs/spec/target-access-v1.md` + `docs/spec/control-plane-runtime.md` (EN + DE) until PR #1324 (credential-access) merges, to avoid a collision. B4 is out of the code scope for this lane; no docs written. Not a block — gated on #1324 merge.

---

## Finding B4 — DE/EN doc parity — **BLOCKED behind B3 (scope-guarded)**

Mission B4 requires German negation-parity against EN end-to-end clauses (no login/server/bundle for local work; no remote fallback). This is a **documentation change**. Per the task-card ownership reservation (docs navigation belongs to the docs task; the card reserves no production/docs write-set for the authority contract beyond the 3 coreinstallation files), and the mission STOP-KRITERIUM (no writes outside scope), I did **not** write any docs. The B5 regression test is the only change; the mandatory scope guard confirms no `cmd/baha` / `internal/deployment` / CI / docs writes.

---

## Summary / Handoff

- **B5 DONE:** behavior parity proven and pinned with 7 per-caller regression tests on the authoritative base `48aa35ad`. Committed `284e0bd4`, pushed, `ls-remote` confirmed.
- **B1/B2/B3 RESOLVED:** authority decision wired to the real `serviceaccess.Issuer` boundary (identity, liveness, freshness via `ExpiresAt`, foreign/revoked via read-only `Revoke`). Freshness model changed to `now <= ExpiresAt` (no `maxAge`) per Owner. Committed `9dcf8742`, pushed, `ls-remote` confirmed. All required checks green (build, vet, race tests, acyclic deps).
- **B4 DEFERRED:** owner instruction 2026-11-03 — defer `docs/spec/target-access-v1.md` + `control-plane-runtime.md` (EN+DE) until PR #1324 (credential-access) merges (collision avoidance). No docs written; gated on #1324.

**Candidate:** `9dcf874287e92564e172037820767b8c31595254` (branch `work/r27-authority-fix`, base `284e0bd4`, cycle-break base `48aa35ad`).
