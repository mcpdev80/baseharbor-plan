# Coordinator host-ops log — Owner directives 2026-11-07

## #4 Dev-Host containers (DONE)
- 45 stray `bh-w169-ci-bootstrap-*` containers (dead lane w169, ~8h, crash-loop/Exited(127)) across 10 compose projects.
- Controlled `docker compose -p <proj> down` (no `-v`, volumes kept). Verified: dev-host `bh-*` running = 0. basics ALARM dev-host cleared.
- No active install was present on the dev-host (all bh-* were w169-ci-bootstrap); nothing with persistent data touched.

## #114 baha-docker-2 half-frozen core stack (host cleaned; validation pending)
- Stray `bh-w169-ci-bootstrap-*` (3 projects, Up 10h) + half-frozen `bh-w266dn-shared` (2 containers `Created`, postgres-init Exited(1)) from dead lanes.
- Controlled `down` of the w169-ci-bootstrap + w266dn projects. **Preserved** `bh-local-shared` / `bh-local-core-shared` (running, the shared local backend with persistent data under ~/.local/share/baseharbor). Verified: remaining bh-* = 8, all bh-local-*; non-local residual = 0. vm-lock released.
- docker-2 core stack no longer frozen; a green run still has to validate it (runs via the ci-lanes runtime cells, card 0427-021).

## #107 baha-podman-2 container→external routing (FIXED by ip_forward)
- Owner correction 2026-11-07: these systems run **no firewall** (no firewalld/nftables policy). My earlier "netavark created 0 nft rules / firewalld conflict" theory is therefore WRONG and dropped — `nft refs:0` is the expected clean state, not a defect.
- Real root cause found and fixed: **`net.ipv4.ip_forward=0`** (reboot reset) → set to 1 and persisted (`/etc/sysctl.d/99-baseharbor-podman-forward.conf`). Without it, rootless podman cannot masquerade/forward container→external, which is exactly the path a compose `pg-init`/dependency DNS resolution uses → the historical pg-init timeout.
- Validation on a real container (fresh network): container→external DNS now resolves (`nslookup google.com` → address returned), container→`host.containers.internal` ping 0% loss, container→1.1.1.1 reachable. Internal container→container by IP and by hostname also fine. aardvark-dns running.
- #107 host defect considered REPAIRED at the network layer. Final closure = a real compose start reaching READY on baha-podman-2 (exercised by cards #003 greenfield-stacks and #118 broker, now running), which is the genuine end-to-end witness. Not relying on my synthetic probe alone.

## #114 docker-2 Health-Check 2026-11-07 (owner directive: accept after confirmed health)
- All bh-local core services Up ~17h, no crash-loop/Created/Exited: keycloak (healthy), openbao+member+admin, postgres+member+admin.
- Fresh 2-container sanity on a new network: container-to-container ping OK, name resolution OK.
- pg_isready/curl exec "not found" = probe-tooling artifact of minimal images (services themselves Up), NOT a stack defect.
- VERDICT: docker-2 core stack HEALTHY, half-frozen state resolved. Owner-authorized ACCEPT after confirmed health-check.
