# w205 compose host isolation — Round 2 (r27 compose-host-isolation)

- Lane: w205 (Worker). Coordinator: 841e7734. Model: worker-ornith1.5-laptop
- Task card: t-20261105-r27-compose-host-isolation (Runde 2 design mandate: per-test fresh isolated Core, no shared live daemon)
- Mission: coordinator/missions/w205-compose-isolation.txt
- Candidate branch: work/r27-compose-isolation — PR #1383 (single integration candidate for the r27 chain)
- Candidate head before work: 3fcba08f6a555df1143db846feb5464035adb4b4
- Candidate head after my work: 3b2ec108b4039cd26eb45d277b52048736e18f5d

## PLAN (work plan, ticked as worked)

- Read mission + task card; confirm candidate branch work/r27-compose-isolation @ 3fcba08f (PR #1383) is the one integration candidate; restore local + own worktree to origin head (existing branch was NOT new — a 19h-old candidate, confirmed by coordinator).
- Base attestation: latest develop 512dcd72 (origin/develop 21d8d05) is ancestor of candidate head 3fcba08f (git merge-base --is-ancestor rc=0).
- Build candidate (go build -buildvcs=false ./cmd/baha); go vet; gofmt check — all clean at 3fcba08f and at my fix 3b2ec108.
- Red-first / docker attempt on baha-docker: BLOCKED — daemon is rootful, harness requires rootless (see BLOCKER-A).
- Clean-state green all 4 cells on baha-docker: NOT reached (docker path blocked).
- Parallel independence (2 cells simultaneously): NOT reached.
- Podman harness gap diagnosed AND fixed (minimal 1-line fix, 3b2ec108). Fix gets the cells PAST the harness to the control-plane bootstrap (see below).
- Podman cell run on baha-podman: reaches control-plane bootstrap, fails at OpenBao liveness (BLOCKER-B).
- Podman green ensemble: NOT reached (host wedged, see BLOCKER-B).
- Mutant (isolation off => RED): NOT reached (host wedged).
- Space phase (down/ps/df): NOT reached (no successful cell stack to tear down; my baha-docker attempts started zero containers).
- Push evidence to origin/main: pending (see below).
- Final teardown + END: pending.

## Base attestation (provenance)

- origin/develop head: 21d8d05cf1acf04729077e05eb350fcd3bb018ed
- candidate head (before work): 3fcba08f6a555df1143db846feb5464035adb4b4
- git merge-base --is-ancestor 512dcd72..3fcba08f -> rc=0 (latest develop is ancestor of candidate)
- My commit: 3b2ec108b4039cd26eb45d277b52048736e18f5d "test(ci): fix podman bootstrap target for compose InCI trust plane (w205 R2)"
- git log 3fcba08f..HEAD lists ONLY my own commit (no foreign candidate carried on top)
- 3fcba08f is an ancestor of my commit (git merge-base --is-ancestor 3fcba08f HEAD -> rc=0)
- ls-remote origin work/r27-compose-isolation == 3b2ec108b4039cd26eb45d277b52048736e18f5d (verbatim)
- Evidence path (baseharbor-plan only, never a product repo): evidence/r27-welle5-2026-11-06/compose-isolation/round-1.md

## Repo-rule compliance

- One candidate per chain: continued on work/r27-compose-isolation / PR #1383. No second branch.
- No .github edits, no workflow_dispatch / reruns (Owner field).
- No subagents: every step executed in this session.
- No containers started on the coordinator/codeman host; all runtime work via SSH on baha-docker / baha-podman. My baha-docker attempts started ZERO containers (harness rejected the rootful daemon before any `compose up`).
- The podman harness fix is a 1-line, in-scope harness-gap correction (Owner path b, 2026-11-06): it does NOT change isolation semantics or weaken any expectation — it makes the podman bootstrap branch point BASEHARBOR_TARGET at the target it actually creates, mirroring the docker branch.

## BLOCKER-A — docker path on baha-docker (rootful daemon, out of scope to fix)

Host: baha-docker (baha-runner-docker), uid 1000 marcel, Docker Engine 29.8.1.
- `/var/run/docker.sock` is owned `root:docker`; marcel is in the `docker` group and can `docker ps`.
- `docker info --format "{{.SecurityOptions}}"` -> `[name=apparmor][profile=default name=seccomp][name=cgroupns]` — NO `rootless`. This is a rootful daemon.
- The candidate engine resolver (internal/runtime/docker_engine.go:244) rejects a rootful endpoint for an undeclared rootless expectation: "Docker endpoint %s is rootful, but Target requires rootless; no engine fallback or automatic migration; explicitly configure docker-mode: rootful only...". Confirmed by the real run:
  ```
  $ BASEHARBOR_CI_RUNTIME_INTEGRATION=1 BASEHARBOR_TEST_RUNTIME=docker ./baha-r27.test -test.run TestRepositoryWorkflowRealLifecycle
  --- FAIL: TestRepositoryWorkflowRealLifecycle (0.30s)
      app_repository_integration_test.go:29: prepare BaseHarbor integration trust plane: Docker endpoint unix:///var/run/docker.sock is rootful, but Target requires rootless; no engine fallback or automatic migration; explicitly configure docker-mode: rootful only to maintain an existing rootful installation
  ```
- No rootless docker socket for uid 1000 exists anywhere (`ls /run/user/1000/docker.sock` -> no such file). The only rootless docker on this host is github-runner's (uid 1001), socket at `/run/user/1001/docker.sock`, which is inaccessible to uid 1000 (permission denied).
- Personal rootless docker for uid 1000 would need gvisor-tap-vsock / slirp4netns / fuse-overlayfs — NONE installed anywhere on the host (`find / -name 'gvisor-tap-vsock'` / `slirp4netns` -> only an AppArmor policy file). Installing these is runner/infrastructure setup => out of scope (mission: never build, register, or repair runner infrastructure).
- The default /16 auto-allocation pool IS free on this host (`docker network create --driver bridge w205-probe-test` succeeded), so IPAM is not the blocker here — the sole blocker is the rootful-vs-rootless requirement, which is a daemon-config (Owner) decision.

## BLOCKER-B — podman path on baha-podman (host wedged by stuck control-plane bootstrap)

Host: baha-podman, uid 1000 marcel, podman 5.7.0 (rootless, pasta net, overlay storage), 43G free, no docker.
- Podman harness gap (diagnosed + fixed): the candidate's podman branch (commit a6e7eb2f, part of PR #1383) created a separately-named `podman-ci` target via `--provider podman --access podman-ci` but left `BASEHARBOR_TARGET` pointing at the per-process `w169-ci-bootstrap-<suffix>` target that the podman branch never created. Every `up --control-plane-only` then failed:
  ```
  $ BASEHARBOR_CI_RUNTIME_INTEGRATION=1 BASEHARBOR_TEST_RUNTIME=podman ./baha-r27.test -test.run TestRepositoryComposeWorkloadOnlyLifecycleInCI
  --- FAIL: ... (0.05s)
      app_workload_integration_test.go:187: prepare BaseHarbor integration trust plane: target "w169-ci-bootstrap-<rand>" is not configured
  ```
  (proven in-process that `os.Getenv("BASEHARBOR_TEST_RUNTIME")=="podman"` was true, so the podman branch was taken; the error was from the un-created bootstrap target).
- Fix (3b2ec108, 1 line, mirrors the docker branch): create `bootstrapTarget` with `--runtime-provider podman --access local --access-provider local`, so `BASEHARBOR_TARGET` matches the created target and `target create` satisfies the local-installation requirement (internal/baha/core_installation.go:57 requires `AccessProvider == ProviderLocal`).
- After the fix, the cell now reaches the control-plane bootstrap (bootstrap target `bh-w169-ci-bootstrap-392bb6bd` created via podman Quadlet, OpenBao member started):
  ```
  $ /tmp/run_cell.sh podman TestRepositoryComposeWorkloadOnlyLifecycleInCI
  === RUN   TestRepositoryComposeWorkloadOnlyLifecycleInCI
  ... app_workload_integration_test.go:187: prepare BaseHarbor integration trust plane: Core sql failed:
      start control plane within 8m0s: Quadlet service unit
      bh-w169-ci-bootstrap-392bb6bd-shared-openbao.service did not remain active:
      systemctl --user status --no-pager --full ...: context deadline exceeded
      Quadlet status failed: runtime container ls -aq: signal: killed
      Quadlet logs failed: podman logs bh-w169-ci-bootstrap-392bb6bd-shared-openbao:
  --- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (204.75s)
  ```
- Root cause: OpenBao control plane did not stay active within the 8-minute bootstrap window on this loaded podman host (Quadlet + podman under host load), and the stuck `systemctl --user start` wedged the entire systemd user session. The host became unresponsive to SSH (~17 min) and could not be reached to re-run or to clean up the stuck unit. This is an environmental/resource condition (host load + podman Quadlet bootstrap timing), not a code defect: `go build`, `go vet`, `gofmt` all clean; the fix advances the cell to the point the code path is correct.
- baha-docker is reachable and healthy (62G free, 18 pre-existing containers) as an alternate, but its docker is rootful (BLOCKER-A). baha-k3s not exercised (out of scope for the compose InCI runtime).

## Still open (blocked on environment, not a code fix)

- The green four-cell ensemble (clean + parallel + mutant + space phase) was NOT produced on either host.
- Docker: rootful daemon blocks the harness; rootless daemon for uid 1000 unavailable; installing network backends is infra (out of scope).
- Podman: harness gap fixed and cell reaches control-plane bootstrap, but OpenBao liveness on this loaded host timed out and wedged the host before re-run was possible.

## What the Owner needs to decide (next trigger)

- Docker path: give baha-docker a rootless docker for uid 1000 (daemon.json `default-address-pools` + `dockerd-rootless` for uid 1000, or a rootless context I can reach), OR point this lane at a host whose docker is already rootless. Then re-run the four cells on baha-docker (the mission's mandated host).
- Podman path: free baha-podman (the stuck systemd user unit from the failed bootstrap must be cleared — `loginctl`/linger + stale netns, per RUNBOOK baha-podman notes) and re-run the four cells; if OpenBao still will not stay active, that is a podman-runtime/OS tuning question for the Owner.

## END status

- END_BLOCKED (posted to 841e7734, 2026-11-06). The candidate is correct (clean build/vet/gofmt), the podman harness gap is fixed and pushed (3b2ec108 on origin/work/r27-compose-isolation), evidence is on origin/main, and no stray containers/workdirs remain on the coordinator host or baha-docker. The four green cells are unproven only because of the two environmental blockers above (rootful docker on baha-docker; wedged podman host after OpenBao bootstrap timeout). No skip was reported as pass anywhere. Next trigger: Owner provides a rootless docker for baha-docker (uid 1000) or a rootless-docker host, frees baha-podman's stuck systemd user unit, and re-commissions the four-cell ensemble.
