# CI-ERROR — Belege (Wortlaut)

## Source of the script (ref b9b2112e0703081768e3cf3b79bf9d03e82029c7)
`gh api repos/mcpdev80/baseharbor/contents/scripts/ci-core-rootless-runtime.sh?ref=b9b2112...`

```bash
#!/usr/bin/env bash
set -euo pipefail
runtime="${BASEHARBOR_TEST_RUNTIME:?runtime is required}"
test "$(id -u)" -ne 0
sudo apt-get update
sudo apt-get install -y uidmap slirp4netns dbus-user-session
sudo loginctl enable-linger "$(id -un)"
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
...
case "$runtime" in
  docker)
    ...
      sudo install -m 0755 -d /etc/apt/keyrings
      sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
      ...
      sudo apt-get install -y "docker-ce-rootless-extras=$extras_version"
    ...
  podman)
    sudo apt-get install -y podman
    ...
```

## Raw-Log: DOCKER Job 124543372909 (gh api .../jobs/124543372909/logs)
```
2026-10-31T12:57:08.4741560Z [command]/usr/bin/git log -1 --format=%H
2026-10-31T12:57:08.4937351Z ##[group]Run bash scripts/ci-core-rootless-runtime.sh
2026-10-31T12:57:08.4950214Z bash scripts/ci-core-rootless-runtime.sh
2026-10-31T12:57:08.4950791Z env: BASEHARBOR_TEST_RUNTIME: docker
...
2026-10-31T12:57:08.5045034Z sudo: I'm sorry github-runner. I'm afraid I can't do that
2026-10-31T12:57:08.5060841Z ##[error]Process completed with exit code 1.
```

## Raw-Log: PODMAN Job 124543373358 (gh api .../jobs/124543373358/logs)
```
2026-10-31T12:57:19.5908356Z [command]/usr/bin/git log -1 --format=%H
2026-10-31T12:57:19.6117253Z ##[group]Run bash scripts/ci-core-rootless-runtime.sh
2026-10-31T12:57:19.6131644Z env: BASEHARBOR_TEST_RUNTIME: podman
...
2026-10-31T12:57:19.6220026Z sudo: I'm sorry github-runner. I'm afraid I can't do that
2026-10-31T12:57:19.6231731Z ##[error]Process completed with exit code 1.
```

## sudoers / Privilegien
- `sudo -l` als github-runner: **"user github-runner may not run sudo on baha-runner-docker"**
- `/etc/sudoers` : `root ALL=(ALL:ALL) ALL`; `%admin ALL=(ALL) ALL`; `%sudo ALL=(ALL:ALL) ALL`
- `/etc/sudoers.d/90-cloud-init-users` (mtime 2026-09-21): `marcel ALL=(ALL) NOPASSWD:ALL`
- Kein sudoers-Eintrag für github-runner.
