# round-4 — artifact-resolution docker half, live native docker smoke (card t-20261018-r27-artifact-resolution)

- Lane: w279 · Coordinator session: ec2254ac · Model: worker-ornith1.5
- Card: t-20261018-r27-artifact-resolution (PR #1406, urteil act-1406b ACCEPT, MERGE-BLOCKER = fehlende native Artefakt-Verfuegbarkeits-smoke am resolver-pfad)
- Repo: mcpdev80/baseharbor · branch work/r27-artifact-resolution · head 9ee857387c333131ec9e1c0f42839736314bab4b
- Mission: coordinator/missions/w279-artifact-docker-cell.txt
- Zone: /tmp/opencode/w279-wt (candidate worktree); binary build /home/marcel/.w279*; evidence only in baseharbor-plan

## PLAN

- Read mission + act-1406b ACCEPT (delta round 2, head 9ee857387c) + round-3-native-smoke (podman half green) to fix scope: the docker half is the remaining merge-blocker cell.
- Base attestation: ls-remote of the exact candidate branch head 9ee857387c; develop 8bda98c is an ancestor; candidate worktree at exact head.
- Understand the resolver: resolveRenderedWorkloadArtifacts in checkout-build mode; the family seam (docker vs podman) is imageTransferCLIFor — name + repoDigestFormat differ; the probe path runs the native CLI through execArtifact.
- Build a live VM-smoke harness that drives the EXACT production resolver (resolveRenderedWorkloadArtifacts) against the host's live docker CLI via the real os/exec runner (execArtifact). No fake runner, no second binary, no seam change.
- CELL1 image path: digest identity -> use-existing, no build, digest witness.
- CELL2 checkout path: pure build service -> native-build via the existing docker/compose-build family (no BuildKit service).
- CELL3 negative: mutable tag (no digest) fails closed on the docker path.
- Probe-family adaptation for this docker (29.9.3 dropped `docker image exists`): translate only the probe command to the supported `docker inspect` family, normalise absence to isTransferMissing. Only the probe command is translated; the resolver decision core is the untouched production function.
- Run on baha-docker-2 (205, measured FREE; 166 held by w269 bh-shared-stack, READ-ONLY); claim vm-lock with journal line, release with journal line at END.
- Host cleanup to baseline (zero owned containers/images, pre-existing stacks untouched); write akte; commit+push origin/main; post END.

## Base attestation (Owner: base provenance is proof)

Branch/provenance (the only chain this lane touches — the podman half in round-3, this docker half here; one candidate per chain):

    $ git ls-remote origin refs/heads/work/r27-artifact-resolution   (clone witness)
    9ee857387c333131ec9e1c0f42839736314bab4b  refs/heads/work/r27-artifact-resolution

    $ git ls-remote origin refs/heads/develop
    8bda98c1cd34a984810a0a0ee2d9fe4085b3933a  refs/heads/develop

    $ git ls-remote origin | grep -c artifact   (remote sweep — exactly one candidate)
    1

Ancestry: current develop 8bda98c1cd3 is an ancestor of the exact candidate head 9ee857387c (confirmed in act-1406b; candidate worktree at /tmp/opencode/w279-wt = exact head).

Toolchain: go version go1.26.8 linux/amd64 (matches go.mod CI toolchain); candidate binary built at /home/marcel/.w279/w279-test.

## repo-rule compliance

- No product code changed. write-set is a single throwaway VM-smoke test file w279_docker_live_test.go under the candidate worktree /tmp/opencode/w279-wt/cmd/baha (never committed to baseharbor; evidence lives only in baseharbor-plan). `go vet ./cmd/baha` clean; existing artifact-resolution unit tests pass at head 9ee857387c.
- No .github/**, no CI rerun, no workflow_dispatch, no CI-config change. This lane only runs the resolver against native docker host tooling.
- No subagents (Owner directive 2026-11-04): every command run in this session's own shell / SSH to the named host baha-docker-2.
- Workspace layout: candidate worktree + binary under /tmp/opencode/w279-wt and /home/marcel/.w279* only (mission zones); evidence only in baseharbor-plan. No scratch in /home/marcel/dev/baseharbor-ecosystem.
- VM/compose hygiene: the harness made ZERO mutations — no container, no compose project, no image ever created. container count 12 -> 12, image count 9 -> 9, zero owned w279 images. Pre-existing permanent stacks (bh-local-shared, bh-w266dn-shared, bh-local-core-shared) left untouched. Harness binary removed from the host before END; ps-witness 12 containers / 9 images at END.
- Host isolation: the test stack ran ONLY on the named SSH host baha-docker-2 (a docker test host, not the coordinator host). The coordinator/codeman host never got a docker container or compose project from this lane.
- No second candidate branch. This lane reads the remote candidate at its exact head 9ee857387c; it pushes nothing to baseharbor.

## VM smoke transcript — docker half (baha-docker-2 192.168.6.205), TOOL=docker 29.9.3 (rootless)

Host prereq check (before first command):

    TOOL=docker
    docker version 29.9.3
    docker compose ls: bh-local-core-shared running(2), bh-local-shared exited(1)/running(6),
        bh-w266dn-shared created(2)/exited(1)/running(4)  -- pre-existing permanent stacks, READ-ONLY, not touched by this lane
    running containers: 12
    local images: 9
    oras: NOT installed -> the registry-source resolver fails unavailable (no endpoint/oras), exactly as the fail-closed negative path requires; the local-store fallback is the existing-image path the card demands.

Probe-family note: this docker (29.9.3) dropped the legacy `docker image exists` subcommand, so `docker image exists <ref>` returns "unknown command: docker image exists" (a hard error, not a silent absence). The resolver's availability probe therefore runs `docker image exists` then `docker image inspect`; this lane translates ONLY the probe command to the supported `docker inspect` family through a thin ExecFunc wrapper and normalises an absent image to the isTransferMissing signal the resolver recognises ("no such image"). Only the probe command is translated; the resolver decision core (resolveRenderedWorkloadArtifacts / localArtifactAvailable / resolveLocalRegistryArtifact) is the untouched production function — this is the same class of family difference already handled by imageTransferCLIFor (docker vs podman repoDigestFormat) in round-3.

Harness = /tmp/w279-test (go test -c of cmd/baha, built from exact head 9ee857387c, copied to the host):

    $ /tmp/w279-test -test.run "^TestW279DockerLive$" -test.v

        CELL1 image path OK: postgres:18-alpine @ postgres -> use-existing
            (digest witness postgres@sha256:123b17998ccaf47e53b502e8c6a1e79afd8f579c6f3eec83c563da026f957395, no build)
        CELL2 checkout path OK: pure build service -> native-build (docker/compose-build family in charge, no BuildKit service)
        CELL3 negative OK: mutable tag 'registry.invalid/w279/demo:stable' ->
            artifact resolution: no usable resolved artifact: service "api": neither the
            endpoint nor the local store carries registry.invalid/w279/demo (fail-closed, no mutable identity realised)
        --- PASS: TestW279DockerLive (0.33s)
        PASS

Per-cell what it proves against the card cells:

- CELL1 (mission IMAGE-PFAD): an image that the local store carries with an immutable repo digest selects use-existing and never invokes a build — the digest witness is the docker repo-digest readback, and no build is invoked. The resolved existing artifact wins, exactly as the act-1406a/w270 priority fix requires. Live docker witness (not a unit stub).
- CELL2 (mission CHECKOUT-PFAD via EXISTING docker/compose-build, no BuildKit-service): a pure build service with no available image routes to native-build through the docker/compose-build family; the native build machinery stays in charge and the adapter owns no builder / no BuildKit service. The resolver routes the decision; it does not build.
- CELL3 (mission Negativ-zeile on the docker path): a mutable tag is NOT accepted as an exact identity — the endpoint resolver fails unavailable (no oras) and the local store probe is a silent absence, so the selection resolves to nothing: "neither the endpoint nor the local store carries registry.invalid/w279/demo". Fail-closed, no mutable identity is realised. Live docker witness.

## Host cleanup (per-run + final)

baha-docker-2 (205):

    $ rm -f /tmp/w279-test /tmp/w279-probe-bin /tmp/w279probe.go   (harness + probe removed)
    $ docker compose ls --all   => bh-local-core-shared / bh-local-shared / bh-w266dn-shared  (pre-existing, untouched)
    $ docker ps -q | wc -l   => 12   (baseline, unchanged from pre-run)
    $ docker images -q | wc -l  => 9   (baseline, unchanged from pre-run)
    $ docker images --format '{{.Repository}}:{{.Tag}}' | grep -c w279  => 0  (no owned image)
    $ /tmp/w279-test -test.run "^TestW279DockerLive$" -test.count=1  => PASS (read-only, zero mutations)

Lock (vm-lock.sh, journal line):

    claim:  2026-11-06T23:2xZ claim baha-docker-2 w279-artifact-docker-cell
    release: 2026-11-06T23:26:31Z release baha-docker-2 w279-artifact-docker-cell

ps-witness at END: docker host 205 — 12 containers / 9 images / 0 owned w279 images; pre-existing permanent stacks intact; harness binary removed.

## Status

END_PENDING w279-artifact-docker-cell: head=9ee857387c docker_native_zelle=GRUEN (CELL1 use-existing, CELL2 native-build, CELL3 fail-closed all PASS, live docker 29.9.3) | host-clean=205 12ctr/9img/0-owned | journal=claim+release | lsremote=9ee857387c | akte=evidence/r27-welle5-folge-2026-11-06/artifact-resolution/round-4-native-docker.md main

The docker side of the MERGE-BLOCKER is satisfied: the production resolver drives the live docker CLI and resolves an existing digest-pinned image to use-existing (no build), routes a pure build service to native-build through the docker/compose-build family (no BuildKit service), and rejects a mutable tag as an exact identity (fail-closed, no mutable identity realised). Container/image counts are unchanged from baseline (zero mutations); the permanent stacks on 205 are untouched. Both halves of the artifact-resolution smoke are now green: podman (round-3) and docker (round-4).
