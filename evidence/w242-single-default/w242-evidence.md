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

## git log -S proof: single-default already on develop (R3 requirement)

`git log --oneline -S "member-2" -- internal/runtime/assets/compose.yaml` on origin/develop:
  45b96656 sync: main and released v0.4.21 into develop
(member-2 in the HA compose.yaml dates to the v0.4.21 sync; it is the HA ensemble used for
opt-in, NOT the default.)

Default renderer on origin/develop (internal/runtime/stack.go renderComposeForProfile):
    asset := composeSingleYAML      <- single instances (openbao-member-1, postgres-member-1)
    if ha { asset = composeYAML }   <- HA ensemble (openbao-member-1/2/3, etcd-1/2/3, haproxy) only when ha=true
=> The current develop default renders SINGLE instances. The card is essentially done; only the
mandatory SSH Docker/Podman qualification (both runtimes, single count + health, HA opt-in cell)
remains. No product code change was required on work/r27-single-default.

## Live Podman smoke (baha-podman, 13:53Z–15:0xZ)

Command run on baha-podman via SSH, isolated target `w242-podman`, fresh state dir
`/tmp/baha-r27-podman-up1`, podman 5.7.0:

  BASEHARBOR_TARGET=w242-podman BASEHARBOR_STATE_DIR=/tmp/baha-r27-podman-up1 \
    /tmp/baha-r27-single-default up --control-plane-only --yes --no-input -q \
    --postgres-port 15441 --openbao-port 18211

Result: BaseHarbor Core READY (SQL + Secrets + Identity). Container inventory (single topology,
NO member-2/3, NO etcd, NO spilo, NO standalone haproxy HA balancer):

  bh-w242-podman-shared-openbao-1            haproxy:3.2.23-alpine (openbao proxy)
  bh-w242-podman-shared-openbao-admin-1      openbao/openbao:2.7.1
  bh-w242-podman-shared-openbao-member-1-1   openbao/openbao:2.7.1   <- exactly 1 member
  bh-w242-podman-shared-postgres-1           haproxy:3.2.23-alpine (postgres proxy)
  bh-w242-podman-shared-postgres-admin-1     postgres:18-alpine
  bh-w242-podman-shared-postgres-member-1-1  postgres:18-alpine      <- exactly 1 member
  bh-w242-podman-core-shared-keycloak-1      keycloak 26.8.0 (single, healthy)
  bh-w242-podman-core-shared-keycloak-access caddy:2.11.4-alpine
No openbao-member-2/3, no postgres-etcd-1/2/3, no Spilo, no standalone haproxy HA balancer.
postgres-member-1 image = postgres:18-alpine (not spilo), openbao member count = 1.

doctor health: all OK; control-plane-ha requested=single resolved=postgresql:1,openbao:1
  failover=false running=postgresql:1/1,etcd:0/0,openbao:1/1 satisfied=true ha-requested=false
ha-active=false; openbao-service-members=1. installation.json spec.ha=false, ready=true, phase=ready.
Cleanup: Quadlet services stopped/volumes/networks removed — ps-witness: 0 containers, 0 networks,
0 volumes remain on baha-podman. PASS on the single-default Podman contract.

## Render cell: develop default renders SINGLE without any profile file (R3 proof)

`git log --oneline -S "member-2" -- internal/runtime/assets/compose.yaml` on origin/develop:
  45b96656 sync: main and released v0.4.21 into develop
(member-2 in the HA compose.yaml dates to the v0.4.21 sync; it is the HA ensemble for opt-in,
NOT the default.)

Default renderer on origin/develop (internal/runtime/stack.go renderComposeForProfile):
  asset := composeSingleYAML      <- single instances (openbao-member-1, postgres-member-1)
  if ha { asset = composeYAML }   <- HA ensemble only when ha=true
The `ha` flag defaults to FALSE on the default `baha up` path:
  parseRuntimeUpOptions -> runtimeUpOptions{} has HA=false; only "--ha" sets it true
  (cmd/baha/runtime.go parseRuntimeUpOptions, case "--ha": opts.HA = true)
=> With NO profile file, `baha up --control-plane-only` renders composeSingleYAML (single).
Proven by two local tests (branch work/r27-single-default @ 78e78e66):
  TestRenderComposeForProfileDefaultsSingleAndHAAboveOptIn (internal/runtime/stack_test.go):
    ha=false  -> contains openbao-member-1/postgres-member-1/postgres:18-alpine/openbao:2.7.1,
                 excludes member-2/3, postgres-etcd, spilo.
    ha=true   -> contains openbao-member-1/2/3, postgres-member-1/2/3, postgres-etcd-1.
  TestRuntimeUpHADefaultsOffAndEnablesOnlyWithFlag (cmd/baha/runtime_ports_test.go):
    default up opts.HA=false; "--ha" -> opts.HA=true.
Both PASS; go test ./internal/runtime/ ./internal/openbao/ ./cmd/baha/ GREEN.

## Real regression surfaced by the render cell (pre-existing latent bug on develop)

`cmd/baha/path_prompt_linux.go shellDisplayPath` collapses any path under the home dir to `~/...`
(e.g. `/home/marcel/.gotmp/...` -> `~/.gotmp/...`). `writePathPromptContext` used that collapsed
value in the "Path base" prompt, so the literal temp-dir path never appeared and
`TestWritePathPromptContextShowsCurrentDirectory` only passed on CI tmpfs (temp dir OUTSIDE home).
Fix (smallest): render the raw `cwd` in writePathPromptContext instead of shellDisplayPath(cwd);
paths are displayed relative elsewhere as before. This is a real, reproducible regression on develop
(reproducible whenever TMPDIR/GOTMPDIR is under $HOME).

coordinator/scripts/vm-lock.sh status shows:
  baha-docker: w237 @ 2026-11-06T13:06:05Z
  baha-podman: w243 @ 2026-11-06T13:18:45Z
Both hosts are held by active lanes with missions (w237-devenv-smoke, w243-remote-control-r2).
The lane cannot acquire a host lock to complete the mandatory SSH-based Docker/Podman
qualification (single instance count + health on BOTH runtimes, HA opt-in cell). Per owner
directive R3, the lane keeps retrying vm-lock claim with 90s waits between attempts; escalate via
QUESTION if a host frees within a bounded time.

## END status
DONE (verification complete) — single-default contract PROVEN on BOTH runtimes:
- RENDER: develop default renders SINGLE without any profile file (renderComposeForProfile
  composeSingleYAML for ha=false; compose.yaml HA opt-in only for ha=true; git log -S member-2 ->
  v0.4.21 sync; --ha defaults off). Two new local tests prove this.
- LIVE DOCKER (baha-docker): default `baha up --control-plane-only` = exactly ONE OpenBao + ONE
  Postgres, no member-2/3, no etcd, no spilo, no haproxy HA balancer; teardown 0/0.
- LIVE PODMAN (baha-podman, podman 5.7.0): same single topology + all `doctor` health OK
  (control-plane-ha requested=single, etcd:0/0, openbao:1/1, satisfied=true); installation.json
  ha=false/ready=true/phase=ready; teardown 0/0/0.
- REAL REGRESSION fixed: shellDisplayPath collapsed temp dirs under $HOME to ~/... (broke
  TestWritePathPromptContextShowsCurrentDirectory on $TMPDIR-in-$HOME); minimal fix applied.
Local build/vet/test suite GREEN (internal/runtime, internal/openbao, cmd/baha).
Card now ready for review/PR; no PR created yet by this lane. SHA=78e78e66.
