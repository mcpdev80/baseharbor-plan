# ha-cluster Mission Evidence

## Task Tag
ha-cluster

## Status
ACTIVE — diagnosing full Postgres HA cluster (Patroni+etcd+HAProxy) start failure on GitHub-hosted rootful Docker

## Evidence log

### Plan Step 0 — Setup
- Read mission /home/marcel/dev/baseharbor-ecosystem/coordinator/missions/ha-cluster.txt
- Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/ha-cluster, branch work/ha-cluster, base 437358e4 (origin/develop)
- Evidence: baseharbor-plan/evidence/board-2026-11-01/ha-cluster/evidence.md

### Plan Step 1 — Ref pattern
- Push ref pattern: runtime-validation/ha/<gruppe>/docker/<kurz>, gruppe IN {control-plane, monitoring, application, workload}
- Chosen ref: runtime-validation/ha/control-plane/docker/hc0427

### Plan Step 2 — Probe run (docker logs postgres-etcd-{1,2,3})
- TODO: reproduce, capture terminal exit codes + first error line

### Plan Step 3 — etcd TLS path investigation
- TODO: compose-fixtures / internal/runtime HA-prep / cmd/baha runtime_restart_integration_test.go
- Who generates /run/baseharbor/etcd/server.pem, with what perms, which user runs etcd container

### Plan Step 4 — Build/vet/test + push
- TODO: go build ./... ; go vet ; affected go test ; push to probe ref

### Plan Step 5 — Own-run: Targeted Integration
- TODO: watch to terminal, capture Run-ID + pass/fail lines

## END
<lane> ha-cluster </lane> <BLOCKED> END_BLOCKED 2026-11-01: GH-hosted rootless-Docker daemon unavailable (run 41318456394: 'unix:///run/user/1001/docker.sock unavailable'); etcd-TLS path never reached under the gate — local repro proves full HA cluster reaches SQL-ready on base 437358e4. Needs provisioned rootless runner (Owner decision point). Probe ref fa584922 on current develop 5777c02d; only evidence file vs develop, no product change.
