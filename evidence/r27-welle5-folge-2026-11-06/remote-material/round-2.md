# remote-material round-2 — t-20261018-r27-remote-material (w287)

## Role / scope (worker, own session only — AGENTS 4.8)

Worker lane w287 implementing the owner-decided scope in its OWN session. No subagents,
no delegating writes/pushes/reviews. Evidence path fixed in akte.

## Remote witnesses (measured)

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`:

```text
3fa6f7b0d0ba01943501627e4c5d811cc7bee848 refs/heads/develop
```

Base provenance (branch cut ref, in akte): `dddf0d7823f6eec161ad518bbced626fa9efe52e`
confirmed ancestor of origin/develop via `git merge-base --is-ancestor dddf0d7823 origin/develop` (rc=0).

Branch HEAD after fetch+merge of origin/develop (fast-forward):

```text
3fa6f7b0d0ba01943501627e4c5d811cc7bee848 (HEAD -> work/r27-remote-material)
```

Worktree in persistent zone `workers/worktrees/w287-remote-material` (tmpfs not a launch window,
per §0.2). No stray `/tmp/opencode/w287-remote-material-wt` worktree exists.

## Owner decision 2026-11-07 (massgeblich)

Exactly ONE bounded cut: the SERVING certificate of an exposed Deployment is projected through
the existing provider-owner (serviceaccess PKI: `EnsureNativeTLS` / `EnsureTLSMaterial`) into
the managed publication and consumed at the node (HTTPS-serving path), including rotation (new
material consumed without re-bootstrap). Card wording is binding: a standalone unused adapter is
not complete — the consumer must actually use it.

Required: positive + negative regression + bounded protocol probe where cryptographic consumption
cannot be proven by fixtures. Do NOT enable the broad remote guard (no default-flip, no shared
registry/index — that belongs to t-20261018-r27-public-surfaces). Supported limit stated in akte:
one serving certificate per exposure, rotation without restart.

## Implementation seam (measured)

- `EnsureRuntime(ctx, issuer, store, m)` (internal/application/runtime_postgres.go:79) is the ONLY
  place with the issuer (OpenBao). It produces every backend material under `files.Dir` then writes
  the authoritative compose via `RuntimeComposeYAMLForProject`.
- `ProjectManagedRuntime(files, m)` (internal/application/remote_runtime_projection.go:35) builds the
  published bundle by walking the generated compose's `services[*].volumes` mounts + Compose
  `secrets[].file`. It has NO issuer.
- Therefore: produce one serving cert + CA per exposure during `EnsureRuntime` under
  `files.Dir/providers/exposure/<name>/runtime/{server-cert.pem, server-key.pem, ca.pem}`, and
  reference each serving material from the generated runtime compose (named volume mount) so
  `ProjectManagedRuntime` includes it in the published bundle. The compose is authoritative and
  verified by `ProjectManagedRuntime` (ErrRuntimeDefinitionChanged on drift), so the serving mount
  MUST live in `RuntimeComposeYAMLForProject`.

## Supported limit (documented per mission)

- One serving certificate per HTTP exposure (bounded by `len(m.Exposures)`).
- Rotation: new serving material is consumed without re-bootstrap (issuer reconciles existing leaf).
- No broad remote guard: no default-flip, no shared registry/index.

## Testanforderung (measured CI coverage)

- New fixtures: projection (one serving cert per exposure present in the published bundle),
  ownership (foreign exposure serving rejected), secret-leak (serving key stays owner-only on host),
  TLS-material (serving cert + CA projected, modes 0600/0644), plus a bounded protocol probe asserting
  cryptographic consumption at the node.
- Every new test lives under `internal/application/` and runs in the normal `go test ./internal/...`
  release-source CI job (ci.yml), triggered on the PR's selected checks (draft PR → ready). No
  `.github/**` change is needed for the unit fixtures.
- Erhalt-Pflicht: `git diff dddf0d7823..HEAD -- internal/application/*_exposure_serving*test.go | grep '^-func Test'`
  is empty (no removed test functions).

## Build / vet / test status

- `go build ./internal/application/...` clean after merge.
- Baseline `go test ./internal/application/...` clean before serving change.
- (post-merge)

## STOP-KRITERIEN

(1) parent conflict with another lane in same write-set, (2) prerequisite not accepted,
(3) a required check needs a .github change, (4) two identical failed correction attempts.

## Evidence / handoff

Evidence akte only in baseharbor-plan (never product repo). END at a4573079:
`END_DONE w287-pr1410-remote-material: head=<sha> base=<sha> pr=<n> akte=<pfad>` with ls-remote line.
