# w242-single-default: control-plane single-default task

Card: t-20261106-r27-control-plane-single-default
Lane: w242 · Coord: 841e7734 · Branch: work/r27-single-default
Base (origin/develop, attested): 78e78e66c5a809ad17482d015539dcf3940d5f9b

## Summary

The single-default implementation was ALREADY present and complete on origin/develop.
This lane did not need to make product code changes: the develop branch already renders
SINGLE control-plane instances by default and HA only via explicit --ha opt-in. The lane
verified the existing implementation with local Go tests and a live Docker smoke test on
baha-docker (before the vm-lock rule). SSH-based Docker/Podman qualification is now blocked
on vm-lock (both hosts held by active lanes w237/w243).

## Acceptance mapping (per card)

- Default IS single per service (one OpenBao, one Postgres, no member-2/3, no etcd, no
  haproxy HA balancer, no quorum): renderComposeForProfile defaults to composeSingleYAML
  when ha=false.
- HA only via documented opt-in: compose.yaml (HA ensemble, 3 members + etcd) renders only
  when ha=true.
- No silent mode switch on existing installs: ensureControlPlaneProfile/validateSingleControlPlane
  enforce topology.json conflict detection; ExistingFilesForProject reads profile back.
- validateSingleControlPlane exists and guards the single path.

## Source facts

- internal/runtime/stack.go renderComposeForProfile:
    asset := composeSingleYAML
    if ha { asset = composeYAML }
  (composeSingleYAML is the single-instance asset; compose.yaml is the HA ensemble.)
- internal/runtime/assets/compose.yaml = HA ensemble (openbao-member-1/2/3, postgres-etcd-1/2/3,
  haproxy) — used only for opt-in.
- internal/runtime/assets/compose-single.yaml = single instances (openbao-member-1,
  postgres-member-1) — the shipped default.
- validateSingleControlPlane rejects spilo / postgres-etcd / member-2 / member-3 / /openbao/file / /openbao/raft.

## Local tests (run on dev-host, no containers)

Branch: work/r27-single-default @ 78e78e66c5a809ad17482d015539dcf3940d5f9b (origin/develop)

Build: go build -o /tmp/baha-r27-single-default ./cmd/baha -> BUILD OK
Vet: go vet ./internal/runtime/ -> OK
Tests: go test ./internal/runtime/ ./internal/openbao/ -count=1
  ok github.com/mcpdev80/baseharbor/internal/runtime 0.252s
  ok github.com/mcpdev80/baseharbor/internal/openbao 5.040s

Existing coverage includes:
  TestControlPlaneDefaultSingleAndExplicitHAPreserveProfileThroughTLS (single + ha, profile
  round-trip, haproxy config, openbao.hcl ha_enabled, profile-change refusal)
  TestControlPlaneRefusesMissingPreFreezeProfileAndSymlink

## Live Docker smoke (baha-docker, before vm-lock rule)

Command run on baha-docker via SSH with an isolated target (w242-smoke), fresh state dir:
  BASEHARBOR_TARGET=w242-smoke BASEHARBOR_STATE_DIR=/tmp/baha-r27-iso \
    /tmp/baha-r27-test up --control-plane-only --yes --no-input -q \
    --postgres-port 15434 --openbao-port 18202

Result: Core started with SINGLE instances. Container inventory (docker ps):
  bh-w242-smoke-shared-openbao-1             haproxy (openbao proxy)
  bh-w242-smoke-shared-openbao-admin-1       openbao/openbao:2.7.1
  bh-w242-smoke-shared-openbao-member-1-1    openbao/openbao:2.7.1   <- exactly 1 member
  bh-w242-smoke-shared-postgres-1            haproxy (postgres proxy)
  bh-w242-smoke-shared-postgres-admin-1      postgres:18-alpine
  bh-w242-smoke-shared-postgres-member-1-1   postgres:18-alpine      <- exactly 1 member
No openbao-member-2/3, no postgres-etcd-1/2/3, no Spilo, no standalone haproxy HA balancer.
postgres-member-1 image = postgres:18-alpine (not spilo), openbao member count = 1.
installation.json spec.ha = false. PASS on the single-default contract.

Cleanup: all bh-w242-smoke containers and baseharbor-w242* networks removed (ps-witness: 0 containers, 0 networks remain).

## vm-lock blocker (current)

coordinator/scripts/vm-lock.sh status shows:
  baha-docker: w237 @ 2026-11-06T13:06:05Z
  baha-podman: w243 @ 2026-11-06T13:18:45Z
Both hosts are held by active lanes with missions (w237-devenv-smoke, w243-remote-control-r2).
The lane cannot acquire a host lock to complete the mandatory SSH-based Docker/Podman
qualification (single instance count + health on BOTH runtimes, HA opt-in cell). Per owner
directive: do not wait, escalate via QUESTION.

## END status
BLOCKED — SSH-based Docker/Podman qualification blocked on vm-lock (both hosts held by active lanes).
Local verification (build/vet/existing tests + one live Docker smoke) is complete and GREEN.
The single-default product implementation already exists on develop; no code change was required.
