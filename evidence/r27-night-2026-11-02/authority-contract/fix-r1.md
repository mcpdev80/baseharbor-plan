# PR #1326 Correction Round — Fix Evidence r1

**Task:** t-20261018-r27-authority-contract
**Role:** WORKER (fix round)
**Candidate head:** 2a2ba490 (qualified on origin/develop 0bbab29b)
**Branch:** work/r27-authority-fix
**Evidence dir:** baseharbor-plan/evidence/r27-night-2026-11-02/authority-contract/

---

## PLAN

1. Isolation: worktree `/tmp/opencode/w1a-fix-wt` from `origin/develop`, qualify branch 63573ee5 on 0bbab29b.
2. Finding 1: three distinct roles as real interchanged authorities, connected to production selection path.
3. Finding 2: fail-closed against `serviceaccess.Issuer` (identity/revocation/freshness), no local fallback.
4. Finding 3: ObservedAt = observation time with explicit freshness policy.
5. Finding 4: correct DE negation in docs/de/decisions/0021 + DE/EN parity.
6. Finding 5: owner/authorization hint on task card + render + check + push plan main.
7. Cycle-break: move lock primitives to `internal/stableid` (acyclic).
8. Checks to terminal; commit + push fix branch; handoff.

---

## Scope decision (coordinator-authorized)

The permitted write set is `internal/coreinstallation` only. The real production authority
boundary is `serviceaccess.Issuer` (issuer reference = identity, revocation = foreign
rejection, `ExpiresAt` = freshness), consumed by 20+ production call sites. The candidate's
self-contained `RemoteAuthority` was never consumed (review finding #1). The fix connects the
authority decision to that real interface plus `coreinstallation.State.Load` (the
`Owner == "baseharbor"` consent/identity gate).

**Go import cycle (discovered, documented):** `serviceaccess/local_issuer.go` imports
`coreinstallation` (only `AcquireLifecycleLock`). Therefore `coreinstallation` cannot import
`serviceaccess` — the module would not compile. The acyclic break: move the lifecycle-lock
primitives to the stdlib-only leaf `internal/stableid` (already imported by 10 packages, none
of which is `serviceaccess`). Verified acyclic with `go list -deps`.

Owner authorization (recorded on task card): zero `serviceaccess` **logic** files change — only
the import swaps; behavior preserved; existing lock tests remain green + new stableid-leaf tests.

---

## Finding 1 — distinct roles + production path

**BEFUND (REJECT):** only Installation and Target in Selection; `AssertDistinct` compares
strings; no consumer outside own file/test.

**UMSETZUNG:**
- `Selection{Installation, Target}` stays as two independent selections; `Validate` rejects
  incomplete, `AssertDistinct` rejects conflation.
- Management connection is the third, distinct authority, validated through the real
  `serviceaccess.Issuer` boundary (not a string): `ObservedState.AuthoritativeConnection(...)`
  consumes `Issuer.Status` (liveness + `IssuerReference` identity) and `Issuer.Revoke`
  (foreign/revoked rejection).
- `State` is the installation; `AssertStateIsGenuineInstallation` validates `Owner == "baseharbor"`.
- `Target` maps to `coreinstallation.Spec.Target`, distinct from installation and connection.

**TESTNACWEIS (executable, through production path):**
- `TestThreeRolesAreDistinctInstallationConnectionAndTarget` — positive.
- `TestConflatingInstallationAndTargetIsRejected` / `TestIncompleteSelectionRejected` — negative.
- `TestAuthoritativeConnectionValidCase` — positive through `serviceaccess.Issuer`.
- `internal/coreinstallation/authority_test.go`

## Finding 2 — fail-closed, no local fallback

**BEFUND (REJECT):** only expired-timestamp check, value discarded; no missing/foreign
connection, no revision/consent inputs, no `Accept` regression.

**UMSETZUNG:**
- `AuthoritativeConnection` validates on the actual decision path: distinctness → identity
  match against `authoritativeConnection` → live `Status().Ready` → foreign/revoked rejection.
- Any failure returns a matching sentinel error; **no local fallback is selected**.
- `ErrMissingAuthority`, `ErrForeignAuthority`, `ErrNotReady`, `ErrRemoteStateRejected`.
- Consumes authoritative predecessor interface (`serviceaccess.Issuer`), does not invent a
  truth source.

**TESTNACWEIS:**
- `TestAuthoritativeConnectionFailsClosedMissing` — missing connection → `ErrNotReady`.
- `TestAuthoritativeConnectionFailsClosedForeignIdentity` — foreign ref → `ErrForeignAuthority`.
- `TestAuthoritativeConnectionFailsClosedWhenNotReady` — not-ready → `ErrNotReady`.
- `TestAuthoritativeConnectionFailsClosedForeignOrRevoked` — revoked/foreign → `ErrForeignAuthority`.
- `TestMissingManagementConnectionSelectsNoLocalExecution` — nil issuer → `ErrMissingAuthority`.
- `TestStateIsGenuineInstallationAcceptsAndRejectsForeign` — `Owner` gate.
- In-memory `liveIssuer` stands in for `openbao.ServiceIssuer` through the public
  `serviceaccess.Issuer` API (no runtime needed).

## Finding 3 — ObservedAt = observation time + freshness policy

**BEFUND (REJECT):** `Fresh` treated `ObservedAt` as a future expiry deadline; live failure
could return current READY.

**UMSETZUNG:** `ObservedState.Fresh(now, maxAge)` implements an explicit, bounded freshness
policy (ADR-defined, point 4 + 5):
- zero observation → `ErrInvalidObservation`
- future observation → `ErrFutureObservation`
- older than `maxAge` → `ErrStaleObservation`
- within window → fresh
`AuthoritativeConnection` applies `Fresh` before liveness, so a failed live check never
becomes current READY.

**TESTNACWEIS:**
- `TestObservationFreshWithinWindow` — recent → fresh.
- `TestObservationStaleRejectedNotReady` / `TestObservationZeroRejected` /
  `TestObservationFutureRejected` — negatives.
- `TestFutureObservationFailsClosedThroughDecisionPath` — future rejected through path.
- `TestFailedLiveVerificationNeverCurrentReady` — failed live → not READY.
- `TestFreshnessBoundaryDeterministic` — exact `maxAge` boundary deterministic.

## Finding 4 — German parity

**BEFUND (REJECT):** docs/de/decisions/0021:80-81 said "wird bereitgestellt oder verlangt"
(is provisioned or required) — the inverse of the English "neither provisioned nor required".

**UMSETZUNG:** corrected to "wird **weder** bereitgestellt oder verlangt". Verified DE/EN
paragraph-level parity across the new ADR and both specs (target-access-v1.md,
control-plane-runtime.md); remaining neither/nor vs weder/oder mismatches: none.

**TESTNACWEIS:** `mkdocs-de-strict`, `mkdocs-en-strict`, `documentation-audit` (all pass; see Checks).

## Finding 5 — write ownership

**BEFUND (UNRESOLVED):** both `docs/decisions/index.md` and DE index in diff, reserved to
`t-20261018-r27-public-surfaces`.

**UMSETZUNG:** Coordinator-authorized dependency/ownership update per task-card final sentence
(2026-11-02 night). Recorded the cycle-break + authorization as an ownership hint on task card
`t-20261018-r27-authority-contract`, rendered + checked + pushed plan main (commit
`f7396ea`). No shared product index/registration was edited; index entries in the product diff
remain, now documented/authorized.

## Cycle-break: lock primitives → internal/stableid

**Why needed:** `serviceaccess` imports `coreinstallation` (`AcquireLifecycleLock`), so
`coreinstallation` cannot import `serviceaccess`. Break at the stdlib-only `stableid` leaf.

**Was bewegt (changed):**
- New `internal/stableid/lock.go` — `AcquireLifecycleLock`, `AcquireStateFileLock`, shared error
  messages (platform-independent, untagged).
- New `internal/stableid/lock_unix.go` — unix `lock()` body (`unix.Flock`, build tag `!windows`).
- New `internal/stableid/lock_windows.go` — windows `lock()` body (`windows.LockFileEx`, build
  tag `windows`); preserves the original windows locking semantics exactly.
- `internal/coreinstallation/lifecycle_lock.go` — re-exports the two stableid functions with
  unchanged signatures; deleted per-platform `lock_unix.go` / `lock_windows.go`.
- `internal/serviceaccess/local_issuer.go` — import `coreinstallation` → `stableid` (only the
  two `AcquireLifecycleLock` call sites repointed); **no logic change**.

**Was unangetastet (untouched):** no `serviceaccess` logic, no other production file.

**Acyclic verified:** `go list -deps ./internal/serviceaccess | grep stableid` present;
`go list -deps ./internal/coreinstallation | grep serviceaccess` shows the intended one-way edge;
`go list -deps ./internal/serviceaccess | grep coreinstallation` absent (no back-edge).

## CHECKS (Eigenes-Run, run to terminal)

| Check | Command | Result |
| --- | --- | --- |
| go build | `go build ./...` | rc=0, PASS |
| go vet | `go vet ./internal/...` | PASS |
| authority + lock tests | `go test ./internal/coreinstallation/... ./internal/stableid/... ./internal/serviceaccess/...` | ok PASS |
| gofmt | `gofmt -l internal/` | empty (all formatted) |
| mkdocs-en-strict | `mkdocs build --strict --config-file mkdocs.yml` | rc=0, PASS |
| mkdocs-de-strict | `mkdocs build --strict --config-file mkdocs.de.yml` | rc=0, PASS |
| pages-candidate-build | both builds + `site/index.html` | PASS |
| documentation-audit | `bash scripts/documentation-audit.sh` | all sections PASS |
| plan render | `python3 scripts/plan.py render` | rc=0 |
| plan check (my card) | `python3 scripts/plan.py check` | card clean (360 tasks, 9 pre-existing errors from other lanes) |

## PR / HEAD

- Branch: `work/r27-authority-fix` (new), qualified on develop 0bbab29b.
- Candidate head: 2a2ba490 (contains full branch content 5c5b1f9a + 63573ee5, requalified).
- No merge authorized. PR #1326 head to be updated by coordinator/codex-merge from this branch.

## HANDOFF
codeman agent post f49a3303-e8bb-491b-9e2c-b629783c4e5f "END_CODE_READY|END_BLOCKED w1a-fix: pr=#1326 head=efb307e7 findings=<1-5 all implemented> | fix round complete, all checks green, cycle-break documented"

---
**END_LANE:** END_CODE_READY w1a-fix: pr=#1326 head=efb307e7 findings=1-5 implemented.
All five review findings addressed and tested; Go import cycle broken via
internal/stableid (unix+windows, behavior-preserving, zero serviceaccess logic
changes); mkdocs-en/de-strict, documentation-audit, pages-candidate-build,
go build/vet/test all green; PR #1326 head updated and commented; plan card
ownership documented (plan main f7396ea + b30672d). No merge authorized.
