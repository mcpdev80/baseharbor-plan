# w227-vm-smoke-r2 — VM Smoke Round 2 (docker + podman hosts)

## Mission
Worker lane w227, card t-20261104-r27-vm-smoke-docker-podman (Runde 2).
Smoke-test freshly-remediated test hosts baha-docker and baha-podman: old baha binary away,
build+install latest develop, smoke, then reset to factory-fresh. Pure operational stat —
no product branch, no PR, no compose/root-checkout.

## Hosts (SSH, never from the coordination machine)
- baha-docker: Host baha-docker -> 192.168.6.166, User marcel
- baha-podman: Host baha-podman -> 192.168.6.148, User marcel
Both reachable (BatchMode ssh OK), load low, 0 containers at start.

## Branch provenance / source head (Owner: branch provenance is proof)
- Source checkout: ~/baha-src-w227 (deep clone, rootfs — /tmp/opencode tmpfs was 2.2G free and failed fetches)
- Base ref cut from: refs/heads/develop = 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1
- Verify: git merge-base --is-ancestor 7c393b0d... HEAD -> YES (identical to develop tip)
- Commit log lists ONLY this develop tip (no foreign commits carried)
- Build ldflags (per .goreleaser.yaml / CI pattern): -X main.version=dev -X main.commit=7c393b0d... -X main.date=...
- Build output: 37609634 bytes, version line:
  baha dev (commit 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1, built 2026-11-06T11:04:31Z)

## (1) Pre-flight (verbatim, in akte)
baha-docker (192.168.6.166):
  container count: 0
  baha processes: none
  old baha binary: ~/.local/bin/baha 37490953 bytes, built 2026-11-04T22:17:04Z
    version: baha dev (commit ea3fb38e8f372ab2da38c10d964f3ea452fb8561, built 2026-11-04T22:17:04Z)
  baha data/config/cache paths: ~/.config/baha, ~/.baha, ~/.cache/baha all absent
  (user dirs /home/marcel/w71-demo/baha-fix, /home/marcel/setup-baha-docker.sh etc. are personal, left untouched)

baha-podman (192.168.6.148):
  container count (podman): 0
  baha processes: none
  old baha binary: ~/.local/bin/baha 37490953 bytes, built 2026-11-04T22:17:52Z
    version: baha dev (commit ea3fb38e8f372ab2da38c10d964f3ea452fb8561, built 2026-11-04T22:17:52Z)
  baha data/config/cache paths: ~/.config/baha, ~/.baha, ~/.cache/baha all absent
  (user dirs /home/marcel/baha-verify, /home/marcel/setup-baha-podman.sh etc. are personal, left untouched)

## (2) Old baha removed (owner directive) — baha-docker
  removed '/home/marcel/.local/bin/baha'
  rm -rv ~/.config/baha ~/.baha ~/.cache/baha -> none of those paths exist
  verify: ls ~/.local/bin/baha -> No such file; type baha -> not found; PATH-scan -> no baha; broker: none

Old baha removed (owner directive) — baha-podman
  removed '/home/marcel/.local/bin/baha'
  rm -rv ~/.config/baha ~/.baha ~/.cache/baha -> none of those paths exist
  verify: ls ~/.local/bin/baha -> No such file; which baha -> empty; broker: none

## (2.5) Rootless docker setup — baha-docker (owner directive 2026-11-06)
  OS: Ubuntu 26.04.1 LTS, kernel 7.0.0-34-generic, x86_64
  docker client/server: 29.8.1 (API 1.56)
  subuid marcel:100000:65536 (both /etc/subuid and /etc/subgid), marcel in docker+sudo groups
  rootless daemon: user systemd unit docker.service -> ACTIVE (running) since 2026-11-06 09:59:06 CET
    ExecStart=/usr/bin/dockerd-rootless.sh (rootlesskit/containerd-snapshotter mode)
    rootless endpoint: unix:///run/user/1000/docker.sock
    ~/.docker/run/docker.sock -> absent (this host runs the containerd-snapshotter rootless stack;
      socket lives at /run/user/$UIDP/docker.sock, symlinked from the rootless context)
    rootless context verified: docker context ls -> rootless * -> unix:///run/user/1000/docker.sock
  rootful context: default -> unix:///var/run/docker.sock, StorageDriver=overlayfs, RootDir=/var/lib/docker
  rootless info: StorageDriver=overlayfs, RootDir=/home/marcel/.local/share/docker
  daemon.json storage driver vfs: NOT needed — overlayfs works in both rootful and rootless mode
    (no daemon.json exists; no overlay failure; precedence alt-protokolle not triggered)
  smoke, both sockets, verbatim:
    [rootful] sudo docker run --rm hello-world -> "Hello from Docker! ... working correctly."
    [rootless] docker --context rootless run --rm hello-world -> "Hello from Docker! ... working correctly."
    [rootless port-map] -p 0:80 hello-world -> "Hello from Docker! ... working correctly." (EXIT 0)
    [rootful port-map] -p 0:80 hello-world -> "Hello from Docker! ... working correctly." (EXIT 0)
  container count after both-socket smoke: rootful=0, rootless=0

baha-podman remains rootless podman (unchanged, verified):
  podman 5.7.0 (API 5.7.0), rootless uid 1000, cgroup v2 / systemd, slirp4netns 1.3.3
  0 containers at start; no stray baha config

## (3) New build + install
  source HEAD (develop tip, verified ancestor): 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1
  baha-docker install: ~/.local/bin/baha 37609634 bytes
    version: baha dev (commit 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1, built 2026-11-06T11:04:31Z)
  baha-podman install: ~/.local/bin/baha 37609634 bytes
    version: baha dev (commit 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1, built 2026-11-06T11:04:31Z)
  Note: ~/.local/bin is in PATH only for login shells (bash -lc); invoke baha via full path or login shell.

## (4) Smoke, both hosts — command + output verbatim
baha-docker:
  [docker rootful hello-world] -> "Hello from Docker! ... working correctly."
  [docker rootless hello-world] -> "Hello from Docker! ... working correctly."
  [docker port-map rootless nginx-alpine] -> pulled nginx:alpine, ran, container cleaned; count=0
  runtime doctor (control-plane section): postgres FAILED / openbao FAILED / Core Identity FAILED /
    control-plane-ha FAILED (no Core stack deployed on this runtime-only host — expected)
  runtime section: os OK / podman OK / quadlet OK / selected-runtime OK / host-trust-ownership OK
  baha version: baha dev (commit 7c393b0d..., built 2026-11-06T11:04:31Z)

baha-podman:
  [podman run quay.io/podman/hello] -> pulled, ran (SIGPIPE from head = EXIT 141, run succeeded)
  [podman run fedora:latest] -> "podman-rootless-smoke-ok" (EXIT 0)
  [podman run registry-1.docker.io/library/hello-world] -> "Hello from Docker!" (EXIT 13 from head)
  nginx:alpine short-name -> did not resolve (no unqualified-search registries) — informational,
    fully-qualified images pull and run fine
  runtime doctor (control-plane): postgres FAILED / openbao FAILED / Core Identity FAILED /
    control-plane-ha FAILED (no Core stack on this runtime-only host — expected)
  runtime section: os OK / podman OK / quadlet OK / selected-runtime OK / host-trust-ownership OK
  baha version: baha dev (commit 7c393b0d..., built 2026-11-06T11:04:31Z)
  load: 0.37 / 0.32 / 0.22 (well under the load>4 pause threshold)

## (5) Factory reset — both hosts, verbatim
baha-docker:
  removed '/home/marcel/.local/bin/baha'
  ~/.config/baha ~/.baha ~/.cache/baha -> none of those paths exist
  type baha -> "not found"; ls ~/.local/bin/baha -> "No such file"; PATH-scan -> "no baha in any PATH dir"
  broker process: none; docker containers (rootful+rootless) = 0; load 0.27/0.27/0.18

baha-podman:
  removed '/home/marcel/.local/bin/baha'
  ~/.config/baha ~/.baha ~/.cache/baha -> none of those paths exist
  type baha -> "not found"; ls ~/.local/bin/baha -> "No such file"; PATH-scan -> "no baha in any PATH dir"
  broker process: none; podman containers = 0; load 0.26/0.30/0.22

## Gate summary
- Both hosts: old baha gone, new build installed (commit 7c393b0d proven by version line), smoke green
  on runtime, both docker sockets + podman rootless stack functional, reset to factory-fresh (0 containers,
  baha not found, no broker). Load stayed low throughout; no load>4 pauses needed.
- No subagents used. No product branch, no commit in a product repo, no compose/root-checkout.
- Workspace: source under ~/baha-src-w227, build under ~/baha-w227-build, helper scripts under ~;
  no scratch files created under /home/marcel/dev/baseharbor-ecosystem.

## Status
DONE — all steps executed, both hosts verified factory-fresh, evidence committed to origin/main.
END lane w227 DONE.
