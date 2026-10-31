# gh-ci-core — Plan

Mission: `coordinator/missions/gh-ci-core.txt`
Task/tag: `gh-ci-core` (critical path #1236/#1225)
Write-set (ONLY these 4 files, exclusive):
  - .github/workflows/ci.yml
  - .github/workflows/nextjs-greenfield-e2e.yml
  - scripts/ci-core-rootless-runtime.sh
  - scripts/test_ci_docker_runtime_doctor.py

Owner goal: 100% GitHub-hosted CI, real+full+secure coverage. NO self-hosted / custom runners.

## PLAN checklist

1. ci.yml `validate` job (line 277): change
   `runs-on: [self-hosted, Linux, X64, baseharbor, docker]`
   -> `runs-on: ubuntu-latest` (Docker is preinstalled there).
   Keep the job's real docker gates (compose config, CLI smoke, native
   runtime integration tests via ci-runtime-reset.sh).

2. nextjs-greenfield-e2e.yml `nextjs-docker` job (line 11): same change
   `runs-on: [self-hosted, Linux, X64, baseharbor, docker]`
   -> `runs-on: ubuntu-latest`. Keep the real docker build/start/HTTP-200/destroy gate.

3. ci-core-rootless-runtime.sh: KEEP necessary isolation/setup functions
   (registry-mirror / image cache, daemon-config, XDG for rootless podman
   when a job runs rootless podman). REMOVE provably redundant RUNNER-specific
   logic only:
     - line 5:  `test "$(id -u)" -ne 0`      -> non-root requirement: GH-hosted ubuntu-latest runs as a non-root 'runner' user. KEEP.
     - line 6:  `sudo apt-get update`        -> sudo unavailable on GH-hosted (no passwordless sudo). REMOVE.
     - line 7:  `sudo apt-get install -y uidmap slirp4netns dbus-user-session` -> packages ship on ubuntu-latest (slirp4netns + fuse-overlayfs present for rootless containers; dbus-user-session not needed for a single script run). REMOVE.
     - line 8:  `sudo loginctl enable-linger ...` -> linger is a persistent-host assumption, irrelevant on ephemeral GH-hosted runner. REMOVE.
     - line 9:  `export XDG_RUNTIME_DIR=/run/user/$(id -u)` -> /run/user/<uid> is mounted on GH-hosted runners for the runner user. KEEP.
     - line 10: `export DBUS_SESSION_BUS_ADDRESS=...` -> points at XDG_RUNTIME_DIR bus; harmless on GH-hosted. KEEP.
     - line 11: `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` -> requires sudo + changes host sysctl on a shared runner (unsafe). REMOVE; unprivileged userns is permitted on GH-hosted ubuntu-latest.
     - line 12: append XDG/DBUS to $GITHUB_ENV -> required so subsequent steps see the rootless socket env. KEEP.
     - lines 14-23: public-image-cache bootstrap (cache_endpoint file, BASEHARBOR_CI_PUBLIC_IMAGE_CACHE export). KEEP — real cache isolation, host-agnostic.
     - docker branch (26-57): install docker-ce-rootless-extras + dockerd-rootless-setuptool.sh, set registry-mirrors in daemon.json, set DOCKER_HOST. KEEP (docker rootless needs the extras binary; it is NOT preinstalled). Just drop the `sudo` before curl/apt/install so it works as root on GH-hosted (the rootless daemon still listens on the user XDG socket).
     - podman branch (58-81): apt-install podman + registries.conf mirror config. On GH-hosted, keep the registries.conf mirror caching (real isolation) but drop `sudo apt-get install podman` (podman is preinstalled on ubuntu-latest; apt+sudo unavailable).
     - `*)` unsupported branch: KEEP (fail-closed guard).

   Justify every retained/removed line in evidence.

4. test_ci_docker_runtime_doctor.py: adjust the `supported_hosted_setup_precedes_every_reset_and_doctor`
   assertion so it checks the GH-hosted path (the doctor test already asserts
   `runs-on: ubuntu-latest` / no `self-hosted` in docker-runtime-acceptance.yml —
   that workflow is untouched, so update only the parts that assume rootless
   runtime-script setup that we removed). Keep all fail-closed receipt/parser
   assertions intact.

5. Quality: no artificial PASS/SKIP, no coverage downgrade. Keep candidate-SHA
   binding / Required Checks / receipt chain UNCHANGED. Keep existing self-hosted
   Required-Check dependency until green ubuntu-latest replacement exists.

6. Proof: local check (python3 -m unittest scripts/test_ci_docker_runtime_doctor.py),
   push branch, open PR against develop, watch the HOSTED run to terminal
   (own-run obligation), target: affected jobs run on ubuntu-latest and are
   truly green. Plan repo NOT pushed by this lane.

## END_BLOCKED gh-ci-core: SHA 7da04607 · PR #1239 · validate/native-docker BLOCKED — rootless docker blocked by GH-hosted apparmor (unprivileged userns denied); Owner decision needed (rootful-mode change OR permitted runner)

## DIAGNOSIS (own-run, PR #1239, runs 4066–4072) — blockers found and fixed

- CI coverage resolver (pr-required-final.py) flags ci.yml /
  nextjs-greenfield-e2e.yml / ci-core-rootless-runtime.sh /
  test_ci_docker_runtime_doctor.py as "native qualification required", so the
  PR merge gate fails until the validate native docker gate actually RUNS GREEN.
- The validate job never started a docker daemon; on ubuntu-latest docker's
  default daemon is rootful, but the runtime integration tests require
  mode=rootless at unix:///run/user/<uid>/docker.sock -> 4 real tests failed.
- Attempt 1: install docker-ce-rootless-extras via apt -> `chmod /etc/apt/keyrings
  Operation not permitted` (runner steps run as root; /etc/apt locked down).
- Attempt 2: fetch .deb -> wrong URL (missing `pool/`) -> curl 404; also
  `VERSION_CODENAME unbound variable` (not exported by runner) under set -u.
- Attempt 3: fetch .deb from download.docker.com, extract tool, start daemon
  with `dockerd-rootless.sh` -> `.deb data payload` glob bug + `data.tar.xz`
  extraction (fixed). Daemon still did not open the socket.
- Attempt 4: wrapped daemon in `dbus-run-session` -> `failed to exec
  'dockerd-rootless.sh'` (dbus execs without inherited PATH).
- Attempt 5: absolute path -> `failed to exec ''` (copied only
  dockerd-rootless-setuptool.sh; daemon needs dockerd-rootless.sh + rootlesskit).
- Attempt 6: copy full toolchain -> **`rootlesskit:parent] error: failed to
  start the child: fork/exec /proc/self/exe: operation not permitted`**.

## ROOT CAUSE (EXTERNAL BLOCKER — Owner decision required)

`rootlesskit` needs unprivileged user namespaces. GitHub-hosted
`ubuntu-latest` blocks them: `/proc/sys/kernel/apparmor_restrict_unprivileged
_userns=1` and `unshare --user` fails with "Operation not permitted". The
original script lifted this via `sudo sysctl -w ...=0` — that needs sudo, which
is unavailable on the shared runner. Verified on a local host too: apparmor
blocks `unshare --user` and refuses to write the sysctl even as root.

The `validate` job's native docker integration tests (TestRepositoryCompose*
etc.) call `testruntime.Resolve()` which defaults to `mode: rootless` and
hard-rejects rootful (`docker_engine.go:121-122`). Rootful docker (preinstalled,
works without userns) is therefore NOT accepted by the gate.

## Recommendation to Owner (next trigger: this END_BLOCKED)

Reconcile the two hard requirements (100% GH-hosted + native docker stays real)
by choosing ONE:
(a) allow `docker-mode: rootful` in the validate compose contract (change the
    test to accept rootful on GH-hosted — a source change, needs review), or
(b) run the validate native docker gate on a runner image that permits userns,
    or (c) accept a documented gap / defer the GH-hosted native docker gate
    until a permitted runner is available.
Do NOT merge with the native docker gate red. CI resolver + PR Selected Checks
stay red until (a)/(b)/(c) is resolved and the gate runs green.

## UPDATE (2026-11-01, run 41253201931) — tunable fix WORKS; new separate blocker found

Owner nudge `coordinator/missions/gh-ci-core-nudge.txt` (2026-11-01): the shared
GitHub-hosted runner grants the non-root `runner` user NOPASSWD sudo (the
self-hosted runners forbade it), so `sudo -n sysctl -w kernel.apparmor_restrict
_unprivileged_userns=0` should lift the userns block — a code fix, not an Owner
decision.

- Committed `1afb91e8` on branch `work/gh-ci-core` (PR #1239). Write-set: only
  `scripts/ci-core-rootless-runtime.sh` (tunable lift + fail-open warning) and
  `scripts/test_ci_docker_runtime_doctor.py` (doctor now permits the runner-specific
  `sudo -n sysctl` tunable lift, still forbids generic sudo/loginctl enable-linger).
- CI run 41253201931 (`CI · PR #1239`, validate job 124690816812) outcome:
  `validate` = **failure**, all other gates green, `PR Selected Checks` = **fail**
  (coverage-unresolved).

### The tunable fix resolved the ORIGINAL blocker (proven from the transcript)
Line 311 of the job log: `kernel.apparmor_restrict_unprivileged_userns = 0`
applied. The rootless daemon then started and `docker info` reported
`[name=seccomp,profile=builtin name=rootless name=cgroupns]` (line 312).
**The original rootlesskit fork/exec denial (`fork/exec /proc/self/exe:
operation not permitted`) is gone** — the tunable-lift fix works on the shared
runner.

### NEW, SEPARATE BLOCKER: unprivileged `docker run` cannot START a container
The daemon is reachable (no "Cannot connect"), but every `docker run` in the
integration tests' `compose up -d` fails identically:

```
Error response from daemon: failed to create task for container:
  failed to create shim task: OCI runtime create failed: runc create failed:
  unable to start container process: unable to apply cgroup configuration:
  unable to start unit "docker-<id>.scope":
  Access denied as the requested operation requires interactive authentication.
  However, interactive authentication has not been enabled by the calling program.
```

This is the classic shared-runner unprivileged **D-Bus `systemd1` / polkit
interactive (PAM) authentication** denial on cgroup v2 (lo-fi) unit activation,
a *separate* shared-runner limitation from the userns block. It occurs in the
native-docker integration gate itself (compose up of the BaseHarbor control
plane: openbao/haproxy at lines 921–1089, and multi-instance runtime at 1707),
NOT in the smoke test (which is fail-open, line 311).

### Why this is OUTSIDE the 4-file write-set and needs Owner / infra decision
The only in-scope lever would be making the daemon run rootful or
usernamespaces-free (a `docker_engine.go` source change — out of write-set — or
a runner-group / runner-image change). The cgroup/lo-fi + polkit denial cannot
 be worked around from the write-set: it is enforced by the shared runner's
unprivileged `runner` user lacking interactive PAM auth for systemd unit
activation. Options for Owner / infra:
- (d) run the validate native-docker gate on a **self-hosted or delegated
  runner** that allows the shared runner's `runner` user to activate cgroup
  units (the original self-hosted runner worked pre-nudge), or
- (e) a runner image / runner-group with `UserNamespacesUnprivileged` and
  lo-fi delegation enabled, or
- (f) accept a documented gap / defer the GH-hosted native-docker gate.
Do NOT merge with the native-docker gate red. CI resolver + PR Selected Checks
stay red until the gate runs green on a permitted runner.

## END_BLOCKED gh-ci-core (2026-11-01): SHA 1afb91e8 · PR #1239 · run 41253201931

The tunable-lift fix WORKS (rootless daemon now starts on shared GH-hosted
runner; original rootlesskit userns denial gone). A NEW separate shared-runner
limitation now blocks the gate: an unprivileged `docker run` on
ubuntu-latest cannot START a container (cgroup/lo-fi unit activation requires
D-Bus systemd1 interactive/PAM auth the unprivileged runner lacks). This is
outside the 4-file write-set and needs an Owner / infra decision
(runner-group/image (d/e) or documented gap/deferral (f)). CI resolver +
PR Selected Checks stay red until the native-docker gate runs green.

Repo rules followed: baseharbor/AGENTS.md, DEVELOPMENT_GUIDELINES.md, task write-set only.
