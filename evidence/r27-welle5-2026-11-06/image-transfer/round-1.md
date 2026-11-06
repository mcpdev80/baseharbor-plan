# r27 image-transfer — Evidence (Round 1, Lane w225)

## PLAN

- Read mission + card; verify base (origin/develop ea656d1fcfce9ee14145a8dfaffb9e993fd29497); create work/r27-image-transfer worktree under /tmp/opencode/w225-wt
- Decide transfer path (native registry pull/copy over OCI) vs target-native store vs save/load/OCI archive; record rationale + rejected alternatives in this file
- Implement cmd/baha/application_image_transfer.go: digest-preserving copy + immutable reference (no trunk-drift) + explicit failure on transfer-target errors (no half-success)
- Write positive (digest-preserving copy, digest/architecture verification) + negative (hostile/truncated archive, wrong digest, wrong architecture, tag drift) tests, all real
- Local gates: build, vet, gofmt, race-20
- Hosted Docker + Podman isolated load/pull smokes on named SSH hosts only
- Push candidate, draft->ready PR against develop; show base SHA as ancestor + real ls-remote == head
- Publish evidence to origin/main (ls-tree witness), bring down compose, END to coordinator

## Base attestation

- Base ref cut from: origin/develop
- Base SHA: ea656d1fcfce9ee14145a8dfaffb9e993fd29497
- Branch: work/r27-image-transfer (new, per mission; no existing remote branch)

## Transfer-path decision (card requirement)

Chosen path: native registry pull/copy over OCI (Docker/Podman/Skopeo semantics
via a thin native tool runner). The adapter `cmd/baha/application_image_transfer.go`
copies the immutable repository@digest pin through the target's native transport,
then proves the transferred image carries the same digest, platform-manifest
digest and architecture that were verified on the source.

Rationale for the chosen path over the alternatives the card lists:
- Native registry pull/copy (chosen): preserves the immutable sha256 digest pin
  across hosts, reuses the host's native Docker credential helper / Podman auth
  (no credential cloning), implements no layer-transfer protocol and no private
  container format, and satisfies the "no trunk-drift in transferred identity"
  requirement. It mirrors the accepted predecessor `application_registry_source.go`
  (t-20261018-r27-registry-access, accepted), which addresses native tools and
  pins an immutable digest with fail-closed semantics. This is the only path that
  is digest-preserving across hosts.
- Target-native image store (rejected): no cross-host portability; a digest pin
  verified on host A is not guaranteed to be loadable on host B from the same
  store, so it cannot carry an immutable identity across hosts.
- Native save/load / OCI layout / archive (rejected): an archive is a
  snapshot of one host's store; loading it does not prove the payload still
  matches the source digest unless the digest is re-verified, and it does not
  preserve the index->platform-manifest pin as cleanly as a registry copy. Used
  only as a last-resort local load when a native registry is unavailable, and
  always after a digest re-verify (fail closed on mismatch).
- Never assume Docker image ID == registry manifest digest (card): the adapter
  compares the OCI sha256 manifest digest, not the image ID; a mismatch between
  them is exactly the tag-drift/silent-substitution class this path rejects.

Immutable reference (no trunk-drift): the transfer only ever addresses
repository@sha256:digest; a mutable tag is never pulled or reported complete.
Digest, manifest and architecture re-verification on the target fail closed on
any divergence (ErrImageTransferDigestMismatch / ErrImageTransferArchitectureMismatch).

Failure on transfer-target error (no half-success): a failing target copy or an
unverifiable transfer propagates ErrImageTransferUnavailable; no partial copy is
reported. The only mutable fallback (developer opt-in) lives in
application_registry_source.go and is class-gated; a denied or public-default
source fails closed with ErrImageTransferTargetRefused before any copy.

Cross-write check (mission): app_broker*.go, internal/development/source_snapshot*,
internal/deployment/stage_versions*, and the w224 registry-optin path were read;
no write-set overlap. The adapter writes only cmd/baha/application_image_transfer.go.

Red-first fixtures (all pass, race-20 clean): digest-preserving copy; failing
target copy => explicit error; wrong digest on target => digest mismatch; wrong
architecture => architecture mismatch; unverifiable target => fail closed;
public-default source => target-refused before any native call; mutable-tag
source identity => fail closed; unreachable host => fail closed.

## Gate state

- build/vet/gofmt/race-20: PASS locally on work/r27-image-transfer (HEAD
  68cd9ea59f61a438803cb40bf31e3cc02b3035ec).
- Hosted Docker/Podman isolated load/pull smokes: BLOCKED as STATE. The mission
  names hosts `baha-runner-docker` / `baha-podman` but neither resolves from this
  environment (no DNS, no SSH config entry; only `baha-docker`/`baha-podman`
  exist in ~/.ssh/config). Containers may not run on the session host
  (coordinator/codeman server, off-limits), so the native smoke cannot run here.
  Reported as STATE to the coordinator; awaiting a reachable runner host or an
  explicit instruction to proceed without the hosted smoke.
- PR: #1402 (ready for review) against develop, head == remote head 68cd9ea5...,
  base ea656d1f is an ancestor of the head (confirmed via git merge-base).
