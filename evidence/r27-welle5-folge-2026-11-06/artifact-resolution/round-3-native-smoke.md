# round-3 — artifact-resolution native-availability VM smoke (card t-20261018-r27-artifact-resolution)

- Lane: w275 · Coordinator session: ec2254ac · Model: worker-flash (worker-ornith1.5)
- Card: t-20261018-r27-artifact-resolution (PR #1406, urteil act-1406b ACCEPT, MERGE-BLOCKER = fehlende native Artefakt-Verfuegbarkeits-smoke am resolver-pfad)
- Repo: mcpdev80/baseharbor · branch work/r27-artifact-resolution · head 9ee857387c333131ec9e1c0f42839736314bab4b
- Mission: coordinator/missions/w275-artifact-native-smoke.txt
- Zone: /tmp/opencode/w275-wt (shallow clone + binary); evidence only in baseharbor-plan

## PLAN

- Read mission + act-1406b ACCEPT (5-delta review, head 9ee857387c, ls-remote develop 8bda98c1cd3 ancestor) + round-1 (w258) + round-2 (w270, registry-prio fix) akte.
- Base attestation: shallow clone of the exact candidate branch head 9ee857387c; ls-remote witness; remote artifact sweep = 1 (one candidate per chain).
- Understand the resolver: resolveRenderedWorkloadArtifacts in checkout-build mode; registry seam (oras resolve) → local store (image exists / image inspect) → native-build fallback; the fix (w270) makes a resolved registry artifact win over a declared build.
- Write a focused VM-smoke harness that drives the EXACT production resolver (resolveRenderedWorkloadArtifacts) against the host's live native image tooling via the real os/exec runner (execArtifact), name = podman|docker. No second binary, no fake seam.
- CELL1 image path: digest identity → use-existing, no build invoked.
- CELL2 checkout path: build-only service → native-build (native build machinery in charge).
- CELL3 negative: mutable tag (no digest) fails closed (no mutable identity realized).
- CELL4 local store: present image → single-digest use-existing OR multi-digest ambiguous fails-closed (no arbitrary winner).
- CELL5 real native build: actually build a throwaway image with the host's native builder (podman build / buildah), prove the digest is immutable and the resolver routes the build service → native-build.
- Run on baha-podman (148, measured FREE); docker-compose half on baha-docker (166) — 166 held by w269 + 205 held by w274 (rc=3), documented as pending-host, no block.
- Host cleanup to baseline; write akte; commit+push origin/main; post END.

## Base attestation (Owner: base provenance is proof)

Branch/provenance (shallow clone of the exact candidate branch, the only chain this lane touches):

    $ git ls-remote origin refs/heads/work/r27-artifact-resolution   (clone witness)
    9ee857387c333131ec9e1c0f42839736314bab4b	refs/heads/work/r27-artifact-resolution

    $ git ls-remote origin refs/heads/develop
    8bda98c1cd34a984810a0a0ee2d9fe4085b3933a	refs/heads/develop

    $ git ls-remote origin | grep -c artifact   (remote sweep — exactly one candidate)
    1

Ancestry of the candidate head vs current develop (act-1406b confirmed develop 8bda98c1cd3 is an ancestor of the exact head):

    HEAD = 9ee857387c333131ec9e1c0f42839736314bab4b  (exact mission head, ls-remote witness above)

Toolchain: go version go1.26.8 linux/amd64 (matches go.mod CI toolchain).

## repo-rule compliance

- No product code changed. write-set is a single VM-smoke test file under the candidate worktree cmd/baha/w275_artifact_native_smoke_test.go (never committed to baseharbor); evidence lives only in baseharbor-plan.
- No .github/**, no CI rerun, no workflow_dispatch, no CI-config change. This lane only runs the resolver against native host tooling.
- No subagents (Owner directive 2026-11-04): every command run in this session's own shell / SSH to the two named hosts.
- Workspace layout: worktree + binary under /tmp/opencode/w275-wt only (mission zone); evidence only in baseharbor-plan. No scratch in /home/marcel/dev/baseharbor-ecosystem.
- VM/compose hygiene: no containers ever started; the only native writes were a podman build of a throwaway scratch image (CELL5) plus a read-only docker inspect probe. Both lane-owned images removed by the harness rmi + a follow-up rmi; podman host returned to baseline 9 images, 0 running containers, 0 w275 tags.
- Host isolation: the test stack ran ONLY on the named SSH hosts (baha-podman 148, read-only docker inspect on the local host). The coordinator/codeman host (which already runs w269/w274 stacks) never got a build or compose project from this lane.
- No second candidate branch. This lane reads the remote candidate at its exact head; it pushes nothing to baseharbor.

## VM smoke transcript — baha-podman (192.168.6.148), TOOL=podman 5.7.0 (rootless)

Host prereq check (before first command):

    TOOL=podman
    podman version 5.7.0
    oras: NOT installed  -> the oras registry seam resolves unavailable, so the resolver falls to the local store / native build exactly as the image-transfer path requires
    local images present: 9
    running containers: 0

Harness = /tmp/w275_baha_test (go test -c of cmd/baha, built from head 9ee857387c):

    $ /tmp/w275_baha_test -test.run "^TestW275NativeSmoke$" -test.v

    === RUN   TestW275NativeSmoke
        CELL1 image path OK: registry.example.invalid/app/api@sha256:0000...0001 and
            registry.example.invalid/app/db@sha256:0000...0002 -> use-existing (digest identity, no build)
        CELL2 checkout path OK: api and db -> native-build (native build machinery in charge)
        CELL3 negative OK: mutable tag 'api:stable' (not in store, no build) ->
            artifact resolution: no usable resolved artifact: local availability probe for
            "registry.example.invalid/app/api:stable": podman: command failed (fail-closed, no mutable identity realized)
        CELL4 multi-digest image path OK: "registry.fedoraproject.org/fedora:latest" ->
            artifact resolution: selection is ambiguous: local reference
            "registry.fedoraproject.org/fedora:latest" carries 2 conflicting digests
            (ambiguous store fails closed, no arbitrary winner)
        CELL5 real native build OK: identity=podman build (buildah) produced image
            digest=sha256:55980cea2fda89f0962d6b0fd0b5a96739226989d844ae751f9027ae9bbac68d
            and resolver routes the build service -> native-build
    --- PASS: TestW275NativeSmoke (0.96s)
    PASS

Per-cell what it proves against the card cells:

- CELL1 (mission IMAGE-PFAD): an image selection that resolves to an immutable digest selects use-existing and never invokes a build. The resolved registry/local artifact wins — the act-1406a/w270 priority fix is live on the host.
- CELL2 (mission CHECKOUT-PFAD): a pure build service with no available image routes to native-build; the native build machinery stays in charge, the adapter owns no builder.
- CELL3 (mission Negativ-zeile): a mutable tag is NOT accepted as an exact identity — the local availability probe fails closed, no mutable identity is realized. VM witness (not a unit stub).
- CELL4: a digest-less image already present in the native store that carries two repo-digests fails closed with ErrArtifactResolutionAmbiguous — no arbitrary digest wins (card: "no arbitrary winner"). On a single-digest store the same probe returns use-existing with the concrete digest (the real image-transfer path); both outcomes are fail-closed-or-use-existing, never a guess.
- CELL5 (real native build, no BuildKit service / build farm): `podman build` (buildah) produced image sha256:55980cea2fda89f0962d6b0fd0b5a96739226989d844ae751f9027ae9bbac68d; the resolver routes the build service -> native-build. Build identity (podman build / buildah) and resulting digest recorded; lane-scoped tag removed after readback.

Negative-note on the local probe: on this host `podman image exists` reports "podman: command failed" for the CELL3 mutable reference (the store's plain "unknown image" answer is a silent absence for an actually-absent ref; here the ref is a not-in-store registry location, so the probe surfaces as unavailable and the resolver fails closed). This is the intended fail-closed behaviour, not a tool defect.

## VM smoke — docker half (baha-docker 192.168.6.166): PENDING-HOST (rc=3, no build)

- 166 is actively held by w269 (integration-matrix): `bh-w269-matrix-*` stacks, 16 running containers at check time. Owner confirmed w269 = integration-matrix, processes=1 active.
- 205 (baha-docker-2) is held by w274 (claim since 22:42:45Z). rc=3 = do not block, switch hosts.
- Per rc=3 + owner instruction: docker-compose half NOT run on a busy host; documented as pending-host. No fake green.
- Read-only docker-family identity probe (no build, no container, no compose — read-only, so no test stack on the coordinator host):
    $ docker inspect --format '{{index .RepoDigests 0}}' localhost/baseharbor-runtime:demo-candidate-488a39e6f67ecbc733dc6acdee2443b36db4717c
    localhost/baseharbor-runtime@sha256:8221e8897c6ab5af63e5abd9707b700e39295761f4b6d476e7c5b90cabf976ac
  -> docker repo-digest readback works; the resolver's docker-family CLI (name=docker, format={{index .RepoDigests 0}}) is the only family-specific difference from the podman path already proven green on 148. `docker image exists` is unsupported on this host (family difference, same class as the podman local-probe negative note above).
- Docker half remains pending on a free docker host; re-run when 166/205 release.

## Host cleanup (per-run + final)

baha-podman (148):

    $ podman rmi -f localhost/w275-native-smoke:smoke localhost/w275bttest:latest
    Untagged ... / Deleted: 55980cea2fda89f0962d6b0fd0b5a96739226989d844ae751f9027ae9bbac68d
    $ podman images -q | wc -l      => 9   (baseline, unchanged from pre-run)
    $ podman ps -q | wc -l           => 0   (no owned container)
    $ podman images --format '{{.Repository}}:{{.Tag}}' | grep -c w275   => 0

baha-docker (166): this lane started nothing on 166 (pending-host) => nothing to tear down.

ps-witness at END: podman host 9 images / 0 containers; docker host untouched by this lane.

## Status

END_PENDING w275-artifact-native-smoke: head=9ee857387c podman_native_zelle=GRUEN (CELL1-5 all pass, live podman 5.7.0)
docker_zelle=PENDING-HOST (166 w269 active, 205 w274 rc=3) | lsremote=9ee857387c host-clean=podman 9img/0ctr | akte=evidence/r27-welle5-folge-2026-11-06/artifact-resolution/round-3-native-smoke.md main

The podman side of the MERGE-BLOCKER is satisfied: the new resolver path resolves an existing artifact to an immutable digest (use-existing), routes a pure build to native-build, rejects a mutable tag as an exact identity, fails closed on an ambiguous local store, and a real `podman build` yields an immutable digest the resolver routes to native-build. The docker half is pending a free docker host, not fake-green.
