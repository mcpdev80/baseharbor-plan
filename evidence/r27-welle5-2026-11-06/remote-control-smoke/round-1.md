# w240 remote-control smoke — blocked before enrollment

- Role: CODEX-WORKER; coordinator: `841e7734`.
- Mission: `coordinator/missions/w240-remote-control-smoke.txt`.
- Result: **BLOCKED** before enrollment or demo operations. No connector enrollment, registration, remote demo command, or VM mutation was performed.
- Candidate Core develop SHA: `46ea6c73d17f1eb30f9346803f30b6cb6233c42c`.

## Workstation CLI

The current develop source was archived under `workers/w240-build/src` on the root filesystem and built with isolated cache/temp paths under `workers/w240-build/`. The initial archive build stopped because VCS stamping could not run without `.git`; the successful build used `-buildvcs=false` and explicit version metadata:

```text
baha dev (commit 46ea6c73d17f1eb30f9346803f30b6cb6233c42c, built unknown)
```

The binary is at `workers/w240-build/bin/baha`. The existing `/home/marcel/.local/bin/baha` remains untouched and reports `baha dev (commit none, built unknown)`. This session is only allowed to write under the ecosystem workspace and `/tmp`; it cannot install or replace the requested binary in `/home/marcel/.local/bin` or prepare `/home/marcel/.w240-build`.

Read-only CLI preflight from the develop build:

```text
baha status -o json
{"docker_engine":{"endpoint":"unix:///run/user/1000/docker.sock","context":"rootless","mode":"rootless","daemon_id":"579a6fe9-5916-4170-b629-e14dbf2ae46c","selection_origin":"active-context","verified":true},"target":"local","state":"not_deployed","ready":false,"availability_satisfied":false}

baha target list -o json
{"contract_version":"v1","targets":[{"name":"local","runtime":"docker","access":"local","access_provider":"local","scope":"default","selectors":["implicit","effective"]}]}

baha node list -o json
{"contract_version":"v1","nodes":[]}
```

The product path exists in this develop source: `cmd/baha/app_remote_binding.go:24-39` creates and validates the remote transport; `cmd/baha/app_remote_status.go:18-33` collects remote status through it. The node connector's current main README documents the mTLS enrollment flow. This is not a missing implementation finding.

## VM occupancy and Core reachability

The mission allows `baha-docker` or `baha-podman`. Before any VM mutation, read-only occupancy checks were made; after observing active work, the required 90-second pause was completed and the checks were repeated.

- `w237-devenv-smoke` remained `busy=true` on both post-pause checks.
- `baha-docker` was active: load `1.04, 2.08, 2.65`; existing `bh-w169-ci-*` and `bh-local-*` containers were running. Their published service ports were bound to `127.0.0.1`; `ss -ltn` showed no Core API listener reachable on a non-loopback interface. These stacks were not changed.
- `baha-podman` was idle at the check: load `0.33, 0.69, 0.79`, no running Podman containers or matching `w237`/`w240` process. No state was changed there.

The coordinator host's existing Core/Target preflight is `target=local, state=not_deployed`, with no enrolled nodes. Thus the develop CLI currently has neither a configured remote Core nor a reachable Core endpoint/CA for `baha node add`; that command's documented required inputs include `--tenant-id`, `--core-url`, `--core-address`, and `--ca-file`. I did not invent a transport, endpoint, or trust configuration.

## Outcome and next action

- Enrollment: **not performed**.
- Demo start/status/doctor: **not performed**.
- VM cleanup: no resources were created by this lane; existing containers and host state were left untouched.
- Existing `/home/marcel/.local/bin/baha` was not replaced. The mission's install destination is outside this session's writable roots.

QUESTION posted to coordinator `841e7734`: provide a writable install destination or scope adjustment and the reachable Core endpoint/CA once w237 publishes it. Resume the enrollment and remote demo smoke only after those prerequisites are resolved and after rechecking occupancy before every VM step.

## Changes

No product files, branches, PRs, tests, VM services, containers, or connector state were changed. The build and Go caches are isolated under `workers/w240-build/`. The earlier failed `/tmp/opencode/w240-core/src` attempt left a partial checkout because cleanup was rejected by the shell safety layer; it is outside the product repositories and is disclosed for coordinator cleanup.

## origin/main publication witness

Pending publication; record the exact `ls-tree` output after pushing this evidence.
