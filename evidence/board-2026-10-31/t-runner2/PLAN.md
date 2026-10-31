# PLAN — t-runner2 (Runner-Host GRUNDWAHRHEIT rootless CI)

- Step 0: basics-check (gh-auth mcpdev80 ok), RUNBOOK §6.2 read, t1236 EVIDENCE read, SSH to both runners reachable
- Step 1 (Q1 DOCKER, baha-runner-docker-2): ran as github-runner — `systemctl --user status/start docker docker.socket`, hello-world, linger/dbus/user-unit/daemon-process inspection
- Step 2 (Q2 PODMAN, baha-runner-podman-2): go1.26.9 installed; ran both native tests on clean Actions checkout + scratch checkout; strace of chdir blocker; root cause pinned
- Step 3: REPARATUR-ZUORDNUNG {owner_root_action (Q1) | product_code_fix (Q2)} written; evidence published to `board-2026-10-31/t-runner2/`; Plan repo NOT pushed

## Verdikte (one line)

- Q1 DOCKER: user-service daemon structurally un-startable for github-runner (no linger/user-bus/dbus on docker-2) → **owner_root_action** (host: `loginctl enable-linger github-runner` + provision user systemd manager / `docker-user.service`; no blind sudo, no CI-script fix).
- Q2 PODMAN: runtime blocked by process cwd = host `/home/marcel` (outside userns) → fixable (gh-owned cwd → hello-world works); Test1 **PASS @109.83s** (runtime healthy, keep 180s); Test2 **real product_code_fix**: openbao-role SASL `28P01` + `ssl/tls alert certificate unknown` on clean checkout → env-config/mTLS defect.

## Evidence

- `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-10-31/t-runner2/EVIDENCE.md`
