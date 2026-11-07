# Coordinator host-ops log — Owner directives 2026-11-07

## #4 Dev-Host containers (DONE)
- 45 stray `bh-w169-ci-bootstrap-*` containers (dead lane w169, ~8h, crash-loop/Exited(127)) across 10 compose projects.
- Controlled `docker compose -p <proj> down` (no `-v`, volumes kept). Verified: dev-host `bh-*` running = 0. basics ALARM dev-host cleared.
- No active install was present on the dev-host (all bh-* were w169-ci-bootstrap); nothing with persistent data touched.

## #114 baha-docker-2 half-frozen core stack (host cleaned; validation pending)
- Stray `bh-w169-ci-bootstrap-*` (3 projects, Up 10h) + half-frozen `bh-w266dn-shared` (2 containers `Created`, postgres-init Exited(1)) from dead lanes.
- Controlled `down` of the w169-ci-bootstrap + w266dn projects. **Preserved** `bh-local-shared` / `bh-local-core-shared` (running, the shared local backend with persistent data under ~/.local/share/baseharbor). Verified: remaining bh-* = 8, all bh-local-*; non-local residual = 0. vm-lock released.
- docker-2 core stack no longer frozen; a green run still has to validate it (runs via the ci-lanes runtime cells, card 0427-021).

## #107 baha-podman-2 container-to-container / DNS routing (partially fixed; netavark gap open)
- netavark backend; only default `podman` bridge; no stray stacks.
- **Found `net.ipv4.ip_forward=0`** → set to 1 and persisted (`/etc/sysctl.d/99-baseharbor-podman-forward.conf`).
- Probe: same-network container→container by IP works (0% loss); by hostname via /etc/hosts works. BUT a real DNS query to aardvark-dns gateway `10.89.0.1:53` fails ("Message too large"/"no servers reached") and **netavark created 0 nftables rules** (`nft refs:0`). aardvark-dns processes ARE running.
- Diagnosis: residual = netavark firewall/nat rules not being installed for the rootless network → containers cannot reach the DNS gateway for real lookups → compose service startup that does DNS (apt/apk/Java/Quarkus/next runtime) times out (matches the #107 pg-init-timeout symptom). ip_forward=0 was one cause (fixed); the missing netavark nft rules is a config item (likely firewalld vs nftables backend) still open.
- Next action: configure netavark firewall backend so per-network masq/DNAT-to-aardvark rules are installed; validate by running the actual compose startup on podman-2 (coordinated with the ci-lanes runtime cells). Not marking #107 fixed until a real green run.
