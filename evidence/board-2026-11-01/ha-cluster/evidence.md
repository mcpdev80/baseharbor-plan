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

## NEW DEFECT + SCOPE DECISION (Coordination required, NOT worker write-set)

Root cause now identified (Coord finding on run 41318456394, job 'Targeted runtime · docker', 124883413744): the `v0421_ha` job 'Targeted runtime · ${{ matrix.runtime }}' (.github/workflows/targeted-integration.yml:1103-1167) has NO 'Prepare verified rootless runtime' step. Every other heavy job calls `bash scripts/ci-core-rootless-runtime.sh` (e.g. lines 951-952, 995-996, 1035-1036, 1077-1078, 1254-1255); this job only has a Podman-conditional 'Prepare hosted Podman runtime' step (1130-1137). With `matrix.runtime==docker` the active Docker context is never set, so the test's fail-closed engine detection errors at setup before etcd is ever reached.

Fix (existing mechanism, no product/endpoint change — endpoint logic is correct): add a docker-conditional step to the `v0421_ha` job, identical semantically to the Podman step:
```yaml
      - name: Prepare verified rootless runtime
        if: matrix.runtime == 'docker'
        shell: bash
        run: bash scripts/ci-core-rootless-runtime.sh
```
This is a CI-workflow change only; it does not touch the write-set.

SCOPE DECISION (escalated, not self-executed): `.github/workflows/*` is explicitly OUTSIDE my mission write-set (compose/fixtures/HA-prep + cmd/baha/runtime_restart_integration_test.go + internal/runtime HA cert prep; AGENTS.md §3.7 / mission EXKLUSIVES WRITE-SET). CI-workflow triggers are an owner-coordination decision (§3.7/§5.1). Requesting Owner/Coordinator to (a) approve/apply the one-line workflow fix, and (b) re-dispatch the gate on my probe ref. No cosmetic green, no product code change attempted.
