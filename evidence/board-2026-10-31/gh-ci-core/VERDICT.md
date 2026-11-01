# gh-ci-core — FINAL VERDICT (2026-11-01)

## Status: END_BLOCKED — scope-finalized, endpoint point handed to product lane

PR #1239 HEAD: `56998d04` (mergeable). Branch `work/gh-ci-core`.
Write-set (final, green): `.github/workflows/ci.yml`,
`scripts/ci-core-rootless-runtime.sh`, `scripts/test_ci_docker_runtime_doctor.py`.

## What my scope achieved (correct, on the PR)
- Dropped the rootless-docker provisioning that was provably redundant on
  GH-hosted ubuntu-latest (Owner NUDGE-2, Rule 4): no more docker-ce-rootless-
  extras .deb fetch, no sysctl userns lift, no dbus-run-session rootless daemon.
- System-daemon verify path instead: `docker version` +
  `docker run --rm --pull=always hello-world`.
  VERIFIED GREEN on GH ubuntu-latest: run 41255597778 → "Hello from Docker!"
  (the preinstalled rootful system daemon works for the unprivileged runner).
- Doctor: 12/12 pass; PR validation gates (ci-policy / actionlint /
  executor-verifier / pr-planner / receipt) all pass; Focused Python,
  Workflow policy, PR Trusted Plan pass.

## What remains red and why (NOT my scope)
`validate` (run 41254963213) fails at the native-docker integration gate with:
  `selected Docker endpoint unix:///run/user/1001/docker.sock is unavailable;
  no fallback to System Docker`  (internal/runtime/docker_engine.go:105).
Root cause: the resolver reads `DOCKER_MODE` only from a ctx
`DockerEngineSelection` that the integration tests pass empty → mode defaults
`rootless`, endpoint defaults to the (absent) rootless user socket. The fix is
a resolver env-override in `docker_engine.go` — **outside the 4-file write-set**,
and the Owner explicitly assigned it to a separate product lane. I was told not
to touch `internal/runtime`.

Empirically, neither write-set lever can green the gate alone:
- Rootless provisioning: impossible on ubuntu-latest
  (run 41255597778: `unshare --user` → `/proc/self/uid_map: Operation not
  permitted`; userns blocked by the runner apparmor profile even after the
  sudo sysctl lift).
- `DOCKER_MODE: rootful` in ci.yml: no-op, because the resolver ignores the env
  var (reads ctx mode) — so it neither avoids the reject nor creates the socket.

## END
- My write-set is finalized on PR #1239 (`56998d04`), files green, all my gates
  green. No further product changes in my scope; will not touch
  `internal/runtime`.
- The `validate` endpoint gate (docker_engine.go:105) is BLOCKED and handed to
  the product lane. PR Selected Checks stay red until that lane greens the gate;
  do not merge the merge-gate with it red.
- Next trigger: product lane ships the docker_engine.go endpoint resolution
  override, re-runs `validate` on ubuntu-latest until green, then PR #1239
  proceeds to review/merge.
