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

Read-only checks (report findings, do NOT modify):
  - scripts/pr-gate-plan.py, scripts/pr-check-runner.py, all receipt-* scripts:
    confirm NO self-hosted runner dependency is hard-wired. Findings captured in evidence.

Repo rules followed: baseharbor/AGENTS.md, DEVELOPMENT_GUIDELINES.md, task write-set only.
