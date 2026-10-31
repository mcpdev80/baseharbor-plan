# BLOCKER: rootless docker cannot run on GitHub-hosted ubuntu-latest (gh-ci-core)

- Task: gh-ci-core (critical path #1236/#1225)
- Candidate SHA (branch work/gh-ci-core): `7da04607`
- PR #1239: https://github.com/mcpdev80/baseharbor/pull/1239
- Failing run: CI run 41252082745, validate job 124687517480 (https://github.com/mcpdev80/baseharbor/actions/runs/41252082745)
- Status: **BLOCKED** — Owner decision required. Do not merge with native docker gate red.

## Symptom

The `validate` job on ubuntu-latest fails at "Prepare isolated hosted rootless
Docker" (~30–57s in) with exit code 1. The full job transcript shows:

```
[dockerd-rootless] exec rootlesskit --state-dir=/run/user/1001/dockerd-rootless \
  --net=slirp4netns ... --copy-up=/etc --copy-up=/run ... \
  /home/runner/.local/bin/dockerd-rootless.sh
[rootlesskit:parent] error: failed to start the child:
  fork/exec /proc/self/exe: operation not permitted
```

## Root cause

`rootlesskit` (the rootless-docker namespace fork) needs unprivileged user
namespaces. GitHub-hosted `ubuntu-latest` blocks them:

- `/proc/sys/kernel/apparmor_restrict_unprivileged_userns = 1`
- `unshare --user --map-root-user` → `write failed /proc/self/uid_map: Operation not permitted`

The original `ci-core-rootless-runtime.sh` lifted this restriction with
`sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`. That needs
passwordless sudo, which is **unavailable on the shared GitHub-hosted runner**.

The `validate` job's native docker integration tests (`TestRepositoryCompose
WorkloadUsesBaseHarborBackendsInCI`, `...OnlyLifecycleInCI`,
`TestRepositoryBuildWorkloadRebuildsSourceChangesInCI`,
`TestMultiInstanceComposeLifecycleInCI`) call `testruntime.Resolve()`, which
defaults Docker `mode` to `"rootless"` and hard-rejects rootful
(`internal/runtime/docker_engine.go:121-122`). So the preinstalled **rootful**
docker daemon (which works on ubuntu-latest without userns) is not accepted.

## Why the iterations failed (evidence trail)

1. apt install `docker-ce-rootless-extras` → `chmod /etc/apt/keyrings Operation
   not permitted` (locked down /etc/apt).
2. `.deb` URL wrong (missing `pool/`) → curl 404.
3. `VERSION_CODENAME` unbound under `set -u` (not exported by runner).
4. `case "$RUNNER_TEMP/extras-root/data.tar.*"` glob never expanded → "unknown
   .deb data payload" (fixed: array + nullglob).
5. `dbus-run-session -- dockerd-rootless.sh` → `failed to exec
   'dockerd-rootless.sh'` (dbus execs without inherited PATH).
6. Absolute path → `failed to exec ''` (copied only setuptool.sh; daemon needs
   dockerd-rootless.sh + rootlesskit).
7. Full toolchain copied → rootlesskit fork/exec denied by apparmor (root cause).

The .deb does ship the full toolchain: `dockerd-rootless.sh`,
`dockerd-rootless-setuptool.sh`, `rootlesskit`, `rootlesskit-docker-proxy`.
Extraction (`data.tar.xz`) and daemon startup were verified working on a local
host where userns is permitted; the blocker is the shared-runner apparmor policy,
not the script.

## CI status (run 41252082745)

- All PR/CI Python gates pass: `ci-actionlint`, `ci-policy`,
  `ci-executor-verifier-tests`, `pr-planner-tests`, `receipt-execution-tests`,
  `Workflow policy`, `PR Trusted Plan`, `PR Focused Python`.
- `validate` (native docker gate) = **fail**. `PR Selected Checks` = **fail**
  (coverage-unresolved, gate not yet green).

## UPDATE 2026-11-01 (run 41253201931, SHA 1afb91e8): tunable fix works; new separate blocker

The owner nudge (2026-11-01) permitted the runner-specific sudo tunable lift on
the shared GH-hosted runner (runner user HAS NOPASSWD sudo there). Committed
`1afb91e8` in the write-set: `scripts/ci-core-rootless-runtime.sh` (tunable lift
+ fail-open warning) and `scripts/test_ci_docker_runtime_doctor.py` (doctor now
permits the runner-specific `sudo -n sysctl`, still forbids generic sudo /
loginctl enable-linger).

Transcript of run 41253201931 (validate job 124690816812) PROVES the fix works:
`kernel.apparmor_restrict_unprivileged_userns = 0` applied; the rootless daemon
started and `docker info` reported `[name=rootless name=cgroupns]`. The original
rootlesskit fork/exec denial is GONE.

A NEW, SEPARATE blocker now appears: an unprivileged `docker run` on
ubuntu-latest cannot START a container:

```
unable to apply cgroup configuration:
unable to start unit "docker-<id>.scope":
Access denied as the requested operation requires interactive authentication.
However, interactive authentication has not been enabled by the calling program.
```

D-Bus systemd1 / polkit interactive (PAM) auth denial on cgroup v2 (lo-fi) unit
activation — a separate shared-runner limitation, in the integration gate's
`compose up` (openbao/haproxy lines 921–1089, multi-instance 1707), not the
fail-open smoke test (line 311). OUTSIDE the 4-file write-set. Requires an Owner
/ infra decision: (d) a self-hosted/delegated runner that lets the shared
`runner` user activate cgroup units, (e) a runner image/group with
UserNamespacesUnprivileged + lo-fi delegation, or (f) documented gap / deferral.

Do NOT merge with the native-docker gate red. CI resolver + PR Selected Checks
stay red until the gate runs green on a permitted runner.
