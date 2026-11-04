# Path reservation proposal: `internal/nodeservice`

**Lane:** w105-node-service · Coordinator decision 2026-11-04 (answering the 2026-11-04 QUESTION at `END_BLOCKED`)
**Scope:** PROPOSAL ONLY — no silent contract/task edit. Shared indexes/registrations stay with `t-20261018-r27-public-surfaces`; the service card stays with `t-20261018-r27-node-service`.

## Decision (b) with tight bounds

The coordinator authorized the new package under (b): a thin `internal/nodeservice` that adds connector **service lifecycle** (install / start / restart / uninstall) and **re-enrollment rules**, reusing the existing security-critical enrollment primitives in `internal/targetaccess` instead of copying them. The card's callable production path must be a real, wired function — a standalone unused adapter is not complete.

## (1) Existing packages do NOT already carry this orchestration

Checked before choosing a path:

- `internal/connector` (`Service`, `TargetAccess`, `service.go`): drives **Core-authorized** mTLS operations over the transport (runtime detect, resource lifecycle, quadlet/compose realization, logs, exec, health). It never owns the connector as a **node service** on the host, and it never performs re-enrollment. Its `Service` type is a runtime adapter container, not a host service manager.
- `internal/deployment` (`contracts.go`): declares bounded Core-driven realization/observation interfaces (`RuntimeRealizer`, `QuadletRealizer`, `Observation`). It is an interface contract, not a host-service install/enable implementation.
- `internal/health` (`Collector`, `Snapshot`, `NodeMemory`): node memory / capacity observation only. No lifecycle.
- `internal/runtime/quadlet` (`Manager`): applies **Core-managed** `.container`/`.network`/`.volume` units with foreign-resource preservation; it is deliberately NOT the connector's own self-service unit lifecycle.
- `internal/runtime/container` (`Lifecycle`): docker/podman container primitives for Core workloads, not the connector binary itself.
- `internal/fssecure` (`Root`, `Root.OpenRoot`, protected dirs, bundle publish/verify): the **protected state-root** mechanism the connector already uses for `StagingRoot`. Reused as the trust boundary for service state — not re-implemented here.

Conclusion: no existing package wires the connector's own rootless host-service lifecycle + re-enrollment. A new thin package is justified; it does not overlap another slice's files.

## (2) Chosen path and why

`internal/nodeservice` (no dash), package `nodeservice`.

- **Thin:** only host-service lifecycle + re-enrollment determinism, exactly the two things the card asks for. No container runtime, no Core transport, no desired-state owner.
- **Reuses, does not copy:**
  - `internal/targetaccess.EnsureEnrollmentPrivateKey` — one-time protected key generation (mode 0600, idempotent, symlink-fail-closed).
  - `internal/targetaccess.BootstrapEnroll` + `BootstrapConfig` — HTTPS enrollment with pinned server identity, nonce-bound one-time token, strict destination rules.
  - `internal/targetaccess.InstallEnrollment` — client-only leaf + expected URI + local key + exact expiry + strict PEM/CA rules.
  - `internal/targetaccess.NodeIdentity` / `EnrollmentResponse` — existing wire identities.
  - `internal/fssecure.Root` — protected state root for service metadata.
- **No desired-state / placement authority on node:** the package only manages the connector's OWN unit and only reports observed local activation. It never authorizes/selects Core placement or owns desired state (matches the release note's `Native delivery and stages` boundary).

## (3) Write-set reservation (proposal)

- **New files (this lane):** `internal/nodeservice/*.go` + `internal/nodeservice/*_test.go` — connector repository only, disjoint from every core lane.
- **Untouched:** `internal/connector`, `internal/deployment`, `internal/health`, `internal/targetaccess`, `internal/runtime/**`, `.github/**`, all CI.
- **Shared registration:** NONE. No new public surface, command, or contract registration is added by this lane; wiring into a `cmd` entrypoint (if any) is `t-20261018-r27-node-cli`/`public-surfaces` territory, not this slice.
- **Public surfaces / authority contract:** if this package is later wired into a `baha node` command or an accepted interface, `t-20261018-r27-public-surfaces` and `t-20261018-r27-authority-contract` own that shared-write decision, not this slice.

## (4) PR #4 precedent

Preserved. No historical PR #4 / source branch rewritten. Current main (`2a02a9a`) already contains the security-critical enrollment material (the r27-night reconcile showed `missing=0`); this lane extends it with a thin, reviewed service-lifecycle package only.
