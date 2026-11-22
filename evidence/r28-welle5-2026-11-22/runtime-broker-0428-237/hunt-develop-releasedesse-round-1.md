# Hunt develop releasedesserte round 1 (0428-237)

- read-only bug-hunt, no product change, no commit, no push, no merge, no comment, no subagent
- evidence only in baseharbor-plan
- target: develop snapshot 8629450ef3c5198bb675331c12f56b2c9377aa1c (confirmed via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- releasedesserte cut = next release v0.4.28 (latest released tag; v0.4.29+ have no tag yet), epic core-818. In-dev cut mapped as `v0.4.27..develop` via GitHub compare API. base tag SHA (dereferenced): 6c40fab4de9a611bc8da2e834417427a83c01ca5
- focus: runtime-broker readiness path (cmd/baha/app_broker.go, internal/runtimebroker, internal/runtimeexecutor, internal/runtime, internal/runtime/contract)

## PLAN

1. Establish reality: git remote guard (all remotes -> github.com/mcpdev80), confirm develop snapshot 8629450ef3c via ls-remote, identify releasedesserte cut v0.4.27..develop.
2. Map the in-dev cut (250 commits, 285 changed files) and isolate the runtime-broker readiness path: `verifyRuntimeBrokerRunning` (Docker + Podman), `verifyRuntimeBrokerReady` (mTLS /readyz probe + build-identity + docs), `waitForOpenBaoManagerReady` (proper retry loop), the compose healthcheck `retries:12`.
3. Finding 1: `verifyRuntimeBrokerBuildIdentity` error message passes expectedVersion twice for the "got" placeholder (cmd/baha/app_broker.go:502).
4. Finding 2: readiness path has no FailingStreak tolerance on any non-`healthy` container state -- the Docker path in `verifyRuntimeBrokerRunning` (cmd/baha/app_broker.go:440-447) fails on first `starting`/`unhealthy` poll, unlike the intended healthcheck `retries:12` contract.
5. Finding 3: the /readyz probe reads the raw curl body as JSON without checking the HTTP status code; a 503 "provider not ready" (JSON `{"title":"provider not ready","status":503}`) yields an empty `ready.Status`, producing the unhelpful "readiness response is not ready" instead of the dependency failure (cmd/baha/app_broker.go:462-479).
6. Write akte with findings (file:line), no product change.
7. Verify cleanliness: no container/network/volume/state created, no product change.
8. Post END to coordinator 9142ab1f.

## Findings

### Finding 1 -- version-mismatch error message carries the wrong value (cmd/baha/app_broker.go:502)

`verifyRuntimeBrokerBuildIdentity(actualVersion, actualCommit string)` (line 491) compares the CLI build version against the runtime image version and rejects a mismatch. The error at line 502 is:

    fmt.Errorf("%w: CLI version %s requires runtime version %s, got %s", errRuntimeBrokerIncompatible, expectedVersion, expectedVersion, actualVersion)

The format has four `%s` args mapped as: CLI version, requires runtime version, got. But the second and third both pass `expectedVersion`. The "got" (fourth) correctly gets `actualVersion`, but the "requires runtime version" placeholder (third) also receives `expectedVersion` instead of `actualVersion`. A reader sees "CLI version 0.4.28 requires runtime version 0.4.28, got 0.5.0" -- the required runtime value is wrong and identical to the CLI value, which masks the actual mismatch.

Correct mapping: the third verb should receive `actualVersion`.

Evidence witness (read-only):

    git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop -> 8629450ef3c5198bb675331c12f56b2c9377aa1c
    gh api "repos/mcpdev80/baseharbor/compare/6c40fab4...8629450e...--jq '.files[].filename' | grep app_broker.go  -> app_broker.go (in-cut)

### Finding 2 -- readiness path has no FailingStreak tolerance (cmd/baha/app_broker.go:440-447 and :412-421)

The compose healthcheck for the runtime broker service declares `retries: 12` (internal/runtimebroker/compose_render.go:261), i.e. the container is allowed 12 consecutive failing healthchecks before Docker marks it `unhealthy`. The BaseHarbor readiness probe is supposed to ride out transient health degradation. But `verifyRuntimeBrokerRunning` returns immediately on the first poll that is not `healthy`:

- Docker path (line 440-447): `if !container.Running { ... }` then `if health != "" && health != "healthy" { return fmt.Errorf(...) }`. A container whose healthcheck is still in `starting` (Docker reports `starting` before the first pass) or momentarily reports `unhealthy` fails the entire readiness wait on that single poll, even though the loop in `waitRuntimeBrokerReady` (line 378) only retries once per second and the healthcheck `start-period`/`retries` contract expects tolerance.
- Podman path (line 412-421): same pattern -- `case "healthy": return nil`, `case "unhealthy": return ...`, `case "", "starting": return ...`.

No `FailingStreak` counter exists anywhere (grep for `FailingStreak` returns nothing in the repo). The intended tolerance (healthcheck retries:12) lives only in the compose spec; the readiness probe discards it and hard-fails on the first non-`healthy` observation. During a cold broker start, a transient `starting` state is normal and produces a spurious "readiness failed" error.

Evidence witness (read-only):

    grep -rn "FailingStreak" cmd/baha/ internal/  -> no matches
    grep -n "retries:" internal/runtimebroker/compose_render.go -> 261:      retries: 12

### Finding 3 -- /readyz probe ignores HTTP status and mislabels a 503 (cmd/baha/app_broker.go:462-479)

`verifyRuntimeBrokerReady` runs the mTLS `/readyz` probe with `curl --silent --show-error` (line 454-461) and treats the body as the readiness verdict. There is no HTTP-status check: after `curl` (no `--fail`), both a 200 and a 503 return success to curl, so `out` is parsed as JSON at line 471. The server (internal/runtimeexecutor/server.go:104-113) returns `200 {"status":"ready"}` or `503 {"type":"about:blank","title":"provider not ready","status":503}`. Because the 503 body has no top-level `status` field, `ready.Status` is "" and line 474-478 returns the generic error "application runtime broker readiness response is not ready" -- losing the actual reason (dependency not ready). The dependency is never surfaced to the user; the human-readable `ready.Dependency` is only populated by a server that returns a `dependency` field, which the 503 path does not.

Correct mapping: the probe should branch on `resp.StatusCode == 200` before parsing, and on non-200 surface the server's title/dependency (or at least the HTTP code) instead of the ambiguous "response is not ready".

Evidence witness (read-only):

    grep -n "writeProblem\|writeJSON" internal/runtimeexecutor/handler.go -> 132,140
    awk '/func writeProblem/{f=1} f{print} f&&/^}/{exit}' internal/runtimeexecutor/handler.go -> {"type":"about:blank","title":title,"status":status}

## Cleanliness

- Read-only hunt. No product change, no commit, no push, no merge, no comment, no subagent.
- No container, network, volume or state created. No docker/podman compose project started.
- Working tree on `lane-0428-214-destroystamp @7e6792939` clean except pre-existing untracked `0428-211-hopdevelop-wt/` (belongs to an earlier lane, not touched).
- docker ps -a before/after: no daemon started on this host (coordinator/codeman host; docker/podman tests run only on named SSH hosts per owner directive 2026-11-05).
- cleanliness: no change, clean.

## END

w27-pr1627-0428-061-pull DONE
