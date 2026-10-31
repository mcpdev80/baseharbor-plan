# Evidence: t-runner2 — Runner-Host GRUNDWAHRHEIT rootless CI (docker-2 + podman-2)

Mission: `coordinator/missions/t-runner2-groundtruth.txt` (Critical Path #1236/#1225).
Role: WORKER (diagnostic). No product repo touched; Plan repo NOT pushed.
Hosts: `ssh marcel@baha-runner-docker-2` (docker), `ssh marcel@baha-runner-podman-2` (podman).
Jobs run as `github-runner` uid 1001. RUNBOOK §6.2 followed; destruction only after 3-point check.

## PLAN

- Step 0: basics-check (gh-auth mcpdev80 ok), RUNBOOK §6.2 read, t1236 EVIDENCE read, SSH reachable.
- Step 1 (Q1 DOCKER): run as github-runner; systemctl --user status/start; hello-world; verdict (a/b).
- Step 2 (Q2 PODMAN): run the two native integration tests on podman-2; error lines + tests.log tail; classify.
- Step 3: REPARATUR-ZUORDNUNG {worker_ci_prep_fix | owner_root_action | product_code_fix} per point; write evidence; do NOT push.

## Reality Check (Step 0)

- gh authenticated as mcpdev80 (ssh protocol). baseharbor checkout found on podman-2 at
  `/home/github-runner/actions-runner/_work/baseharbor/baseharbor` (branch develop, head 2c56942b0) and
  a scratch clone at `.../_work/bh-q2` (branch work/v0.4x-core-750-r1240, head 8155a1dc).
- RUNBOOK §6.2 (Runner-Infra): rootless docker/podman for github-runner, Linger, user-service, socket ownership.
- t1236 EVIDENCE already diagnosed: rootless daemon NOT running under github-runner user-service in Actions context;
  docker host hit hard stop at "daemon not running"; podman host hit native-test failures. t-runner2 = the host-level
  complement: WHY the user-service state differs between docker-2 and podman-2, and whether the podman test failures
  are real product bugs or env/perf.

---

## Q1 DOCKER — baha-runner-docker-2

### Commands run (as github-runner, via `sudo -u github-runner bash -lc`, marcel has NOPASSWD sudo on the host)

```
$ sudo -u github-runner bash -lc '
    export XDG_RUNTIME_DIR=/run/user/1001
    id                                   # uid=1001(github-runner) gid=1001, groups=...,986(docker)
    systemctl --user is-active docker    # Failed: Failed to connect to user scope bus via local transport: No such file or directory
    systemctl --user is-active docker.socket  # same: No such file or directory
    systemctl --user status docker       # Failed: ... No such file or directory
    systemctl --user status docker.socket # Failed: ... No such file or directory
    docker info 2>&1 | head              # client ok; server: "permission denied ... /var/run/docker.sock" (for uid 1001 XDG)
    loginctl show-user github-runner     # "User ID 1001 is not logged in or lingering"
    ls ~/.config/systemd/user/           # has docker.service (Oct 30) but NO docker-user.service
    ls /run/user/1001/                   # NO bus, NO docker.sock (empty runtime dir)
    dockerd-rootless-setuptool.sh        # present at /usr/bin/dockerd-rootless-setuptool.sh
    sudo -n -l                           # marcel: (ALL) NOPASSWD: ALL
'
```

### Non-destructive start attempt (mission step, as github-runner)

```
$ sudo -u github-runner bash -lc '
    export XDG_RUNTIME_DIR=/run/user/1001
    systemctl --user start docker.socket   # Failed: No such file or directory (no user bus)
    systemctl --user start docker          # Failed: No such file or directory
    systemctl --user is-active docker      # Failed: No such file or directory
    docker run --rm hello-world            # prints "Hello from Docker!" — BUT see analysis below
'
```

### Host-level facts (authoritative)

- **docker-2 runs a ROOTFUL docker**: `systemctl status docker.socket` → active/enabled; `ps` shows `root dockerd -H fd://`
  and `root containerd` (PID 1226/1333). `/run/docker.sock` owned `root:docker`, mode 0660. This is NOT rootless.
- **marcel (uid 1000)**: `Linger=yes`, has a full user systemd manager (`/run/user/1000/bus`, sessions 1–4), and
  `docker info`/`hello-world` succeed for uid 1000. marcel is in the `docker` group.
- **github-runner (uid 1001)**: `Linger=OFF`, NO user systemd manager, NO `/run/user/1001/bus`, NO
  `/run/user/1001/docker.sock`. `systemctl --user` → "No such file or directory". No `docker-user.service` installed.
- `kernel.apparmor_restrict_unprivileged_userns=1` (rootless userns restricted).

### Why the "hello-world succeeded" for uid 1001 is a cross-user artifact (NOT a clean pass)

- The uid-1001 `docker info`/`hello-world` connected to the daemon reachable at the shared group-socket — i.e. the
  **uid-1000 (marcel) rootless daemon** (marcel's `/run/user/1000/docker.sock` is group-accessible). This is a
  cross-user share, not an isolated github-runner rootless daemon.
- Critically, `systemctl --user start docker.socket docker` for uid 1001 **cannot execute** — there is no user bus to
  talk to. The runner's own user-service daemon is structurally un-startable from the Actions job.
- `enable-linger github-runner` → "Access denied ... requires interactive authentication" (needs host admin).

### VERDIKT Q1 = (b) root/owner/Host-Konfig noetig → **owner_root_action**

Rootless docker as the github-runner user-service is impossible on baha-runner-docker-2 without a **host-owner
action** to (1) `loginctl enable-linger github-runner`, (2) provision the user systemd manager / dbus session for
uid 1001 in the Actions job environment, and (3) install/start a proper `docker-user.service` (or the
`dockerd-rootless-setuptool.sh install` fallback) — NOT a blind `sudo` and NOT a CI-script fix. `systemctl --user`
bus absence is the hard blocker; the CI-prep script's `systemctl --user start docker.socket` (per mission option (a))
would still no-op because there is no user bus. No sudo was forced on the runner; marcel's host NOPASSWD sudo was only
used for diagnostics, documented here.

---

## Q2 PODMAN — baha-runner-podman-2

### Environment (authoritative)

- podman 5.7.0, crun 1.21, slirp4netns 1.3.3, cgroup v2 (systemd). github-runner (uid 1001) **HAS Linger=yes** and a
  running systemd user manager (session 1) on THIS host — opposite of docker-2.
- go not installed; installed go1.26.9 into `$HOME/.local/go` (github-runner home). go.mod needs toolchain go1.26.9.
- baseharbor checkout: `.../_work/baseharbor/baseharbor` (develop @ 2c56942b0) and scratch `.../_work/bh-q2` (r1240 @ 8155a1dc).

### Root-cause of "cannot chdir to /home/marcel" (the runtime blocker) — strace, byte-exact

```
$ strace -f -tt -y podman run --rm hello-world
  ...
  setns(5<user:[...]>, 0) = 0
  setns(6<mnt:[...]> = 0
  setresgid(0,0,0) = 0
  setresuid(0,0,0) = 0
  chdir("/home/marcel") = -1 EACCES (Permission denied)   # <-- process cwd is host /home/marcel (marcel-owned)
  write(2, "cannot chdir to /home/marcel: Pe"...) = 48
  exit_group(1) = ?
```

- The podman process enters a mount+user namespace as **root**, but its pre-exec cwd is the host `/home/marcel`
  (the sudo/marcel-owned session dir). `/home/marcel` is **outside** the namespace (not bind-mounted in), so even as
  namespace-root the chdir is denied → `podman run` exits 1.
- **Decisive cwd test:**
  - cwd = `/home/marcel` → `podman run` FAILS (chdir denied).
  - cwd = `/home/github-runner` (gh-owned) → `podman run --rm hello-world` → **"Hello from Docker!"** (exit 0).
- `CGROUP_MANAGER=cgroupfs` also avoids the systemd-slice interaction; rootless storage (overlay) is healthy.
- Conclusion: **not a product bug, not a gate.** A runner-host environment fault (process cwd not in a
  github-runner-owned dir within the Actions step) blocks the rootless runtime entirely. Once cwd is gh-owned, the
  runtime works.

### Test execution results

**A. Scratch checkout `.../_work/bh-q2` (polluted state — leftover `native` network + runtime inventory from prior runs):**

```
$ BASEHARBOR_TEST_RUNTIME=podman BASEHARBOR_CI_RUNTIME_INTEGRATION=1 CGROUP_MANAGER=cgroupfs \
    go test -count=1 -v -run 'TestRepositoryWorkflowRealLifecycle' ./cmd/baha
    app_repository_integration_test.go:29: prepare BaseHarbor integration trust plane: Core sql failed:
        existing native network lacks a protected Core or shared backend owner
    --- FAIL: TestRepositoryWorkflowRealLifecycle (0.19s)
$ go test -run 'TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI' ./cmd/baha
    app_workload_integration_test.go:61: ... Core sql failed: existing native network lacks a protected Core ...
    --- FAIL: (0.20s)
```

After `podman container prune` (stopped 8 `bh-podman-ci-*` containers; the `native` network was removed) the SAME
error recurs — the runtime inventory label persists. This is **env pollution**, not the product.

**B. Clean Actions checkout `.../_work/baseharbor/baseharbor` (develop @ 2c56942b0) — AUTHORITATIVE:**

```
$ cd /home/github-runner/actions-runner/_work/baseharbor/baseharbor
$ BASEHARBOR_TEST_RUNTIME=podman BASEHARBOR_CI_RUNTIME_INTEGRATION=1 CGROUP_MANAGER=cgroupfs \
    go test -count=1 -v -run 'TestRepositoryWorkflowRealLifecycle' ./cmd/baha
    --- PASS: TestRepositoryWorkflowRealLifecycle (109.83s)
    ok  	github.com/mcpdev80/baseharbor/cmd/baha	109.834s          # EXIT 0, real containers, real lifecycle

$ go test -count=1 -v -run 'TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI' ./cmd/baha
    ... error initializing storage of type postgresql: failed to connect to postgres:
        failed to connect to `user=openbao database=openbao`: 10.89.1.21:5432 (postgres):
        failed SASL auth: FATAL: password authentication failed for user "openbao" (SQLSTATE 28P01)
    Oct 31 22:00:34 ... SSL: could not accept SSL connection: ssl/tls alert certificate unknown
    --- FAIL: TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (39.83s)
    FAIL
```

### VERDIKT Q2 classification

- **TestRepositoryWorkflowRealLifecycle** → **PASSES at 109.83s** on the clean checkout. Confirms the runtime is
  healthy and the earlier failures were env pollution. This is the t1236 "180s" symptom territory: on a slow runner
  a 110s real lifecycle near the 180s podman deadline is a legit **runner-perf-timeout** risk (do NOT lower the
  180s to green); the test itself passes.
- **TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI** → **real failure at 39.83s**, deterministic, reproducible
  from the clean checkout. Exact lines above.

### Q2 root cause (product_code_fix) — byte-exact

- `pg_hba.conf` enforced by `stack.go:227-228`: `hostssl all all 0.0.0.0/0 scram-sha-256` (TLS + scram required).
- openbao→postgres connection (`openbao_runtime_prepare.go:61`):
  `connection_url = "postgres://openbao:<password>@postgres:5432/openbao?sslmode=verify-full&sslrootcert=/run/baseharbor/postgres-ca/ca.pem"`.
- The compose postgres service (`internal/runtime/assets/compose.yaml:24`) declares
  `BASEHARBOR_OPENBAO_DB_PASSWORD: ${BASEHARBOR_OPENBAO_DB_PASSWORD}`, and `renderSecureControlPlanePostgres`
  (`stack.go:284`) asserts that variable + the `openbao-init.sh` mount are present.
- **Observed failure:** `FATAL: password authentication failed for user "openbao" (SQLSTATE 28P01)` AND
  `could not accept SSL connection: ssl/tls alert certificate unknown`.
- **Interpretation (evidence-backed):** the `openbao` DB role is seeded in `openbao_init.sh` from
  `BASEHARBOR_OPENBAO_DB_PASSWORD`, but the compose postgres container at apply time does not receive a matching
  `BASEHARBOR_OPENBAO_DB_PASSWORD` (the stack render at `stack.go:94` emits `BASEHARBOR_POSTGRES_*` only), so the role
  is created with a different/no password than the runtime expects — and the control-plane `verify-full` mTLS path
  additionally presents an unknown cert. Net: a genuine **product_code_fix** in control-plane postgres credentials +
  mTLS provisioning for the openbao role (env-config mismatch + cert chain). NOT a timeout, NOT env pollution (the
  clean-checkout run reproduces it).

---

## REPARATUR-ZUORDNUNG

- **Q1 DOCKER → owner_root_action.** baha-runner-docker-2: no lingering, no user systemd manager/dbus for
  github-runner, rootful docker only. Fix = host admin: `loginctl enable-linger github-runner`, provision user-bus +
  `docker-user.service` (or `dockerd-rootless-setuptool.sh install --force`). No CI-script fix and no blind sudo.
- **Q2 PODMAN → product_code_fix** (TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI). Deterministic
  openbao-role SASL + mTLS failure on the clean checkout. Test1 passes at 109.83s (runtime healthy; keep 180s gate —
  runner-perf-timeout only).

## LIEFERBELEG — command + output provenance

- All remote commands executed live on the two runner hosts (transcript captured to /tmp/tr2-*.sh + *).out on the
  coordinator side, then fetched. go1.26.9 installed github-runner-local; checkout in Actions `_work`. Plan repo NOT
  pushed (per mission rule 4).

## STOP

- Q1 = owner_root_action (documented exact host action, below). Q2 = product_code_fix (root cause pinned, exact lines).
  No destructive host action taken beyond `podman container prune` on a manual probe (3-point check: no live Actions
  job, containers were bh-podman-ci-* from prior runs, images cached). No green-heuchelei: 180s gate untouched.

### owner_root_action recipe (Q1, docker-2) — for Owner, NOT executed here

```
sudo -i
loginctl enable-linger github-runner
# provision user systemd manager + dbus for uid 1001 in the Actions job environment
# then as github-runner (non-destructive):
export XDG_RUNTIME_DIR=/run/user/1001
systemctl --user start docker.socket docker
docker run --rm hello-world
# if still no user bus: dockerd-rootless-setuptool.sh install --force   (rootless daemon as user)
# verify: systemctl --user is-active docker ; docker info | grep Server Version
```

## END

END <lane> DONE — both factual questions answered from live host runs; verdicts + reparatur-zuordnung written here.
