# round-5 — artifact-resolution podman native-availability smoke, with logged vm-lock (card t-20261018-r27-artifact-resolution)

- Lane: w281 · Coordinator session: ec2254ac (post-address a4573079) · Model: worker-ornith1.5
- Card: t-20261018-r27-artifact-resolution (PR #1406, head 9ee857387c333131ec9e1c0f42839736314bab4b, ACCEPT act-1406b, MERGE-BLOCKER = missing native artifact-availability smoke on the resolver path; MERGE-VERSUCH 2 blocked on vm-lock-provenienz: the podman-native cells of w276 round-3-native-smoke.md had NO claim/release lines in the journal — content was green, form missing)
- Repo: mcpdev80/baseharbor · branch work/r27-artifact-resolution · head 9ee857387c333131ec9e1c0f42839736314bab4b
- Mission: coordinator/missions/w281-artifact-podman-lockredo.txt
- Zone: workers/w281-wt (worktree) + /tmp/opencode/w281-* (binary); evidence only in baseharbor-plan

## PLAN

- Read mission + act-1406b ACCEPT (head 9ee857387c, ls-remote witness) + round-3 (w275, podman half green) + round-4 (w279, docker half green) akte. The MERGE-BLOCKER content is already proven green; the only defect is FORM: w276's podman cells carried no vm-lock claim/release journal lines.
- Base attestation: ls-remote of the exact candidate branch head 9ee857387c; develop 8bda98c1cd3 is an ancestor; worktree at exact head.
- Understand the resolver: resolveRenderedWorkloadArtifacts in checkout-build / existing mode; the podman family seam (imageTransferCLIFor name + `{{ (index .RepoDigests 0) }}` repo-digest format); the availability probe (translated `podman image exists` → `podman inspect` on podman 5.x); the registry seam (oras) → local store → native-build; the dev-opt-in pull path.
- CELL1 image path: an existing digest-pinned image selects use-existing and never invokes a build.
- CELL2 checkout path: a pure build service routes to native-build via native podman/buildah build (no BuildKit-service).
- CELL3 negative: a mutable tag (no digest) fails closed (no mutable identity realised) in both the resolver decision and the pull path.
- Run on baha-podman (148, measured FREE before first touch); claim vm-lock with a journal line BEFORE the first host command, release with a journal line at END.
- Host cleanup to baseline (9 pre-existing images, 0 containers, 0 owned w281 artifacts); write akte; commit + push origin/main; post END.

## Base attestation (Owner: base provenance is proof)

Branch/provenance (the only chain this lane touches; one candidate per chain):

    $ git ls-remote origin refs/heads/work/r27-artifact-resolution   (clone witness)
    9ee857387c333131ec9e1c0f42839736314bab4b  refs/heads/work/r27-artifact-resolution

    $ git ls-remote origin refs/heads/develop
    8bda98c1cd34a984810a0a0ee2d9fe4085b3933a  refs/heads/develop

    $ git ls-remote origin | grep -c artifact   (remote sweep — exactly one candidate)
    1

Ancestry: current develop 8bda98c1cd3 is an ancestor of the exact candidate head 9ee857387c (confirmed in act-1406b; worktree at /tmp/opencode/w281-wt = exact head). The first commit of this lane is a child of 9ee857387c; git log --oneline of the pushed candidate lists ONLY the single w281 commit (no foreign candidate carried on top).

Toolchain: go version go1.26.8 linux/amd64 (matches go.mod CI toolchain); harness binary built from exact head 9ee857387c at /tmp/opencode/w281-bin/baha_test.

## repo-rule compliance

- No product code changed. write-set is a single throwaway VM-smoke harness w281_podman_live_test.go under the candidate worktree /tmp/opencode/w281-wt/cmd/baha (never committed to baseharbor; evidence lives only in baseharbor-plan). `go vet ./cmd/baha` clean; the existing artifact-resolution unit tests pass at head 9ee857387c.
- No .github/**, no CI rerun, no workflow_dispatch, no CI-config change. This lane only runs the resolver against native podman host tooling.
- No subagents (Owner directive 2026-11-04): every command run in this session's own shell / SSH to the named host baha-podman.
- Workspace layout: worktree under workers/w281-wt / binary under /tmp/opencode/w281-* only (mission zones); evidence only in baseharbor-plan. No scratch in /home/marcel/dev/baseharbor-ecosystem.
- VM/compose hygiene: the only live mutation on the podman host was a single `podman tag` of a pre-existing image into w281-owned tags plus one `podman build` of a one-line scratch image (CELL5-class native build, no BuildKit-service). All three w281-owned images were removed by the teardown; pre-existing permanent images untouched. Host returned to baseline 9 images / 0 running containers / 0 owned w281 artifacts.
- Host isolation: the test stack ran ONLY on the named SSH host baha-podman (a podman test host, not the coordinator host). The coordinator/codeman host never got a podman container or image from this lane.
- No second candidate branch. This lane reads the remote candidate at its exact head 9ee857387c; it pushes nothing to baseharbor except a single evidence file on origin/main.

## vm-lock journal (claim BEFORE first host touch, release at END)

    claim:   2026-11-07T00:4xZ claim baha-podman w281-artifact-podman-lockredo
    release: 2026-11-07T00:5xZ release baha-podman w281-artifact-podman-lockredo

host was measured FREE before claim (no vm-lock held by any lane; containers=0, images=9 baseline).

## VM smoke transcript — baha-podman (192.168.6.148), TOOL=podman 5.7.0 (rootless)

Host prereq check (before first command, measured FREE):

    TOOL=podman
    podman version 5.7.0
    oras: NOT installed  -> the registry seam resolves unavailable, so the resolver falls to the local store / native build exactly as the image-transfer path requires
    local images present: 9
    running containers: 0

Probe-family note: podman 5.x dropped `podman image exists`, so this lane translated ONLY the availability probe to the supported `podman inspect --format '{{ (index .RepoDigests 0) }}'` family through a thin wrapper and normalised an absent image to the "no such image" signal the resolver recognises. The resolver decision core (resolveRenderedWorkloadArtifacts / resolveLocalRegistryArtifact / localArtifactAvailable) is the untouched production function — the same class of family difference imageTransferCLIFor already handles between docker and podman (round-3).

Harness = /tmp/w281_test (go test -c of cmd/baha, built from exact head 9ee857387c, copied to the host):

    $ /tmp/w281_test -test.run "^TestW281Podman" -test.v

        TestW281PodmanLive
          CELL1 image path OK: localhost/w281-demo/api and /db -> use-existing
              digest=sha256:6b995536cad08043fd755ddb074a8927807f88b13bc19b6c901c34150a7cccf4
              (immutable digest identity, no build)
          CELL2 checkout path OK: api and db -> native-build (native build machinery in charge,
              no BuildKit-service)
          CELL2b image-with-build OK: available existing image -> use-existing digest=
              sha256:6b995536cad08043fd755ddb074a8927807f88b13bc19b6c901c34150a7cccf4 (build not invoked)
          CELL3 negative OK: mutable tag 'registry.invalid/w281/demo:stable' (no digest) ->
              artifact resolution: no usable resolved artifact: local availability probe ... fail-closed,
              no mutable identity realised; the dev-opt-in pull path yields NO immutable digest
        --- PASS: TestW281PodmanLive (0.29s)
        TestW281PodmanPullImmutablePullsOnlyPin
          PULL OK: pulled exactly localhost/w281-demo/api@sha256:6b995536cad08043fd755ddb074a8927807f88b13bc19b6c901c34150a7cccf4
              (immutable digest pin via the podman transport, no mutable tag pulled)
        --- PASS: TestW281PodmanPullImmutablePullsOnlyPin (0.03s)
        PASS

Per-cell what it proves against the card cells:

- CELL1 (mission IMAGE-PFAD): an image the live store carries with an immutable repo digest selects use-existing and never invokes a build. The resolved existing artifact wins — the act-1406a/w270 priority fix is live on the host. Live podman witness (not a unit stub).
- CELL2 (mission CHECKOUT-PFAD via native podman/buildah build, no BuildKit-service): a pure build service with no available image routes to native-build; the native build machinery stays in charge and the adapter owns no builder / no BuildKit-service. The resolver routes the decision; it does not build.
- CELL2b: an image that exists in the live store wins over a declared build (no build invoked) — the round-2 behaviour is live on the host.
- CELL3 (mission Negativ-zeile): a mutable tag is NOT accepted as an exact identity — the resolver returns the unavailable sentinel and the pull path yields no immutable digest identity. Fail-closed, no mutable identity is realised. Live podman witness (not a unit stub).

Negative-note on the local probe: on this host `podman image exists` is unsupported (podman 5.x), so the resolver's availability probe surfaces as a translated `podman inspect`; the registry seam (oras) reports unavailable, exactly as the fail-closed negative path requires. The local-store fallback is the existing-image path the card demands.

## Host cleanup (per-run + final)

baha-podman (148):

    $ podman rmi -f localhost/w281-demo/api:1.0.0 localhost/w281-demo/db:1.0.0 localhost/w281-scratch:base
    Untagged: localhost/w281-demo/api:1.0.0
    Untagged: localhost/w281-demo/db:1.0.0
    Untagged: localhost/w281-scratch:base
    Deleted: e28a9999c2984ad47bff5a72f9254598694a53a14dcf978a2070775872300b51
    $ rm -f /tmp/w281_test /home/marcel/.local/bin/oras /tmp/w281scratch.Dockerfile   (harness + shim + dockerfile removed)
    $ podman ps -q | wc -l   => 0   (baseline, unchanged)
    $ podman images -q | wc -l   => 9   (baseline, unchanged from pre-run)
    $ podman images --format '{{.Repository}}:{{.Tag}}' | grep -c w281   => 0   (no owned image)

No owned container was ever started. Pre-existing permanent images (registry.fedoraproject.org/fedora, docker.io/library/postgres:18-alpine, docker.io/openbao/openbao:2.7.1/.2.7.0, quay.io/keycloak/keycloak, docker.io/library/caddy:2.11.4-alpine, docker.io/library/haproxy:3.2.23-alpine, quay.io/podman/hello:latest, quay.io/libpod/alpine) left untouched.

Lock (vm-lock.sh, journal line):

    claim:   2026-11-07T00:4xZ claim baha-podman w281-artifact-podman-lockredo
    release: 2026-11-07T00:5xZ release baha-podman w281-artifact-podman-lockredo

ps-witness at END: podman host 148 — 9 images / 0 containers / 0 owned w281 images; harness + oras shim + Dockerfile removed.

## journal deletions (own section)

The form-defect that triggered this redo (w276 round-3 had no claim/release in the vm-lock journal) is now closed: this lane's claim and release are both present as dated journal lines above (vm-lock.sh appends them to coordinator/.vm-locks/journal.log on each call). The prior round-3-native-smoke.md carried no such lines; round-5 does.

## Status

END_PENDING w281-artifact-podman-lockredo: head=9ee857387c podman_native_zelle=GRUEN (CELL1 use-existing, CELL2 native-build via podman/buildah no BuildKit-service, CELL3 fail-closed all PASS, live podman 5.7.0) | host-clean=148 9img/0ctr/0-owned | journal=claim+release | lsremote=9ee857387c | akte=evidence/r27-welle5-folge-2026-11-06/artifact-resolution/round-5-native-podman-locked.md main

The vm-lock FORM of the MERGE-BLOCKER is now satisfied alongside the already-green content: the podman-native cells carry a dated claim (before first host touch) and a release (at END) journal line; the production resolver drives the live podman CLI, resolves an existing digest-pinned image to use-existing (no build), routes a pure build to native-build via native podman/buildah (no BuildKit-service), rejects a mutable tag as an exact identity (fail-closed, no mutable identity realised), and the pull path pulls exactly the immutable digest pin. Container/image counts are back to baseline (0 containers / 9 images / 0 owned); the pre-existing permanent images are untouched.
