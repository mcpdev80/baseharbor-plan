# remote-material round-1 — t-20261018-r27-remote-material (w287)

## Role / scope (read-only review, no merge / no product edits)

Reviewed `mcpdev80/baseharbor` task `t-20261018-r27-remote-material` read-only. No
product source, test, CI, merge or branch change performed in this lane. Review
role only; no acceptance or merge.

## Remote witnesses

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/work/r27-remote-material` before review:

```text
dddf0d7823f6eec161ad518bbced626fa9efe52e refs/heads/develop
```

The remote `work/r27-remote-material` branch does not exist yet (no line returned).
`baseharbor-plan/main` HEAD before this review:

```text
10ecd93e... refs/heads/main
```

## Task contract (measured 2026-11-07)

`python3 scripts/plan.py show t-20261018-r27-remote-material` reports state `active`,
owner `w287`, all five prerequisites `accepted`
(`t-20261017-release-0-4-27-updates`, `t-20261018-r27-artifact-resolution`,
`t-20261018-r27-candidate-ingress`, `t-20261018-r27-node-trust`,
`t-20261022-r27-ci-runtime`). Card kanban_status was `active` (owner claimed; the
mission stated `planned` at hand-off).

Outcome: "Build remote provider/exposure/TLS projections using existing provider
owners. Secrets/keys remain protected at required execution boundary; no provider
on developer machine and no forced management service set. Preserve
receiver/consumer/rotation consequences and required native protocols; describe
supported limit explicitly. Do not enable the broad remote guard yet."

Bounded write-set (task note, Dependencies and file ownership):
`internal/application/remote_application_projection.go`,
`internal/application/remote_runtime_projection.go`, bounded exposure/material
files and their tests. Shared indexes/registrations belong only to
`t-20261018-r27-public-surfaces`. No other slice's files.

## Static source findings (exact SHA, develop HEAD dddf0d7823f6eec161ad518bbced626fa9efe52e)

- `internal/application/remote_runtime_projection.go`
  - `ProjectManagedRuntime` (lines 35-126) resolves the Core runtime definition,
    walks every service volume mount and every Compose `secrets[].file` under the
    project root, bounds the count to 128 members and the bundle to 4 MiB, and
    reads only `0600`/`0644` regular files (symlinks, wrong perms, non-regular
    members fail closed). It emits `compose.yaml` (prefixed with the authoritative
    project `name:`), `runtime.env` (owner-only enforced), and one entry per
    referenced protected member with its native mode.
  - `readRuntimeProjectionFileMode` (lines 132-167) is the fail-closed permission
    and path gate (no `/`, `..`, `\`, NUL, CRLF; no symlink; no setuid/setgid/sticky;
    readonly-binding read-only inputs promoted to `0600`/`0644`).
- `internal/application/remote_application_projection.go`
  - `NewRemoteApplicationRuntime` (33-68) compiles the managed projection, appends
    an `application-phases.json` metadata file, and injects resolved workload files.
  - `appendRemoteWorkload` (76-208) confines a workload repository to read-only
    prebuilt images, explicit non-root UIDs, bounded read-only file bindings, and
    native resource names; it rejects namespace overrides, privileged, build/extends,
    unbounded volumes and foreign ownership labels.
  - `readRemoteWorkloadBinding` (340-415) turns directory bindings into individual
    read-only file mounts with depth, symlink, count (128) and byte (4 MiB) limits.
- Test coverage already present in this tree: `remote_runtime_projection_test.go`
  (SQL TLS + cache-TLS-gateway preservation, authoritative name, definition/
  symlink/permission rejection), `remote_managed_runtime_test.go`,
  `remote_managed_snapshot_test.go`, `remote_application_lifecycle_test.go`
  (foreign workload confinement, unreferenced Core material rejection), and the
  material-disposition fixtures in `provider_change_*_test.go` plus
  `runtime_remote_probe_test.go` (retained `$POSTGRES_PASSWORD`, `sslmode=verify-ca`,
  `sslrootcert=/run/baseharbor/tls/ca.pem`).

## Contract gap (measured — NOT a fix, review role)

The mission lists required fixtures `projection / ownership / secret-leak /
TLS-material`. The static review shows the projection/ownership/TLS coverage exists
for SQL/valkey/MongoDB/RabbitMQ provider material and workload confinement. What the
task note names as "bounded exposure material" — an **HTTPS serving certificate that
is actually projected into the managed publication and consumed at the node**, rather
than only internal provider TLS — is not independently asserted by a dedicated
projection fixture in the current tree. This is a scope/coverage observation for the
product owner; it is not implemented here.

## Required checks mapping (task + RUNBOOK 5.6)

- Projection fixture: `TestManagedRuntimeProjectionPreservesSQLTLSAndAuthoritativeName`
  (`internal/application/remote_runtime_projection_test.go:22`), run under
  `go test ./internal/application/...`.
- Ownership / secret-leak: `TestManagedRuntimeProjectionPreservesSQLTLSAndAuthoritativeName`
  asserts no unrelated installation material is copied; workload-confinement negative
  in `remote_application_lifecycle_test.go:300-320`.
- TLS-material: `TestManagedRuntimeProjectionIncludesCacheTLSGateway`
  (`remote_runtime_projection_test.go:66`).
- Native protocol probe: `TestRemoteBackendProbeKeepsTLSAndContainerCredentialReference`
  (`runtime_remote_probe_test.go`); cryptographic consumption cannot be proven by
  fixtures alone — a bounded native probe is the runtime witness (RUNBOOK 5.6).

## Receipts

Test-preservation witness (RUNBOOK 0.4), read-only candidate unchanged so far:

```sh
git diff dddf0d7823f6eec161ad518bbced626fa9efe52e..dddf0d7823f6eec161ad518bbced626fa9efe52e -- internal/application/remote_runtime_projection.go internal/application/remote_application_projection.go | grep '^-func Test'
```

Output: empty (no product change introduced; candidate SHA still equals base).

## Verdict

Read-only review complete. No product change made, no branch cut, no merge. Any
implementation of this card stays inside the bounded write-set, is verified by the
projection/ownership/secret-leak/TLS fixtures under CI, and is handed off at an
exact-SHA candidate. This review neither accepts nor blocks the task; acceptance is
the Maintainer/owner decision at a verifiable exact-SHA candidate.

## Post-review remote witness

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/work/r27-remote-material` after review:

```text
dddf0d7823f6eec161ad518bbced626fa9efe52e refs/heads/develop
```
