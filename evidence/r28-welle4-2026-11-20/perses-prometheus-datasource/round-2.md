# x-m083 / 0428-083 connect-perses-prometheus-datasource — round-2

## PLAN

1. Remote guard: `git remote -v` first; authoritative remote is `origin` -> `https://github.com/mcpdev80/baseharbor.git` (no `lane-origin` here).
2. Base attestations via `git ls-remote`: develop `dbe7fbc3905b`, PR #1684 head was `1c0e33ad864e` (old base `36d075fad77f`, itself based on my branch `643c49834`).
3. Reset the worktree branch to the PR head, rebase onto develop `dbe7fbc3905b`: clean (no overlap in `internal/application` or `internal/metrics`; develop only touched `internal/observability/**`, `internal/identityprovider/**`, one test). New head `43d3a8dc0`. develop is an ancestor; my card commit is the single commit on top; 18 files changed, all mine.
4. Local checks: `go build ./...` OK; `go vet ./internal/metrics/ ./cmd/baha/` OK; `go test ./internal/metrics/` ok. Pre-existing `internal/application` provider-registry failures confirmed at base `643c49834` (unrelated to card).
5. Force-push `--force-with-lease` to the unprotected lane branch `lane-0428-083-datasources-r2`; PR #1684 head moved to `43d3a8dc0` (both columns match; rebased onto develop). PR not reopened, not closed, no second branch.
6. Observe the smoke run `PR · Native · native/docker/perses-runtime-smoke` (`TestPersesRuntimeSmokeDockerIsolated`) at the new head to a terminal state (self-run duty 4.6). Both CI runs fail with the SAME tmpfs runner defect (below). My card does not touch the tmpfs realization (card 0428-177 owns it), and my diff is byte-identical to the old head there. This is the known hosted-runner tmpfs-mountpoint defect, now tracked as card 0428-177 (`t-20261120-perses-tmpfs-mountpoint.md`). Strategy change per 3.6: two identical failed runs = do not repeat the same check.
7. Post STATE to the coordinator with the failing log line, no third identical correction.

## remote witnesses

```
git ls-remote origin refs/heads/develop
dbe7fbc3905b4330acdcfbf3bfb5f4f3af34d0d2	refs/heads/develop

git ls-remote origin refs/pull/1684/head
43d3a8dc0c6c50f044d533fd15b83a086edce6b9	refs/pull/1684/head

git ls-remote origin refs/heads/lane-0428-083-datasources-r2
43d3a8dc0c6c50f044d533fd15b83a086edce6b9	refs/heads/lane-0428-083-datasources-r2
```

Both PR #1684 head and the lane branch report the identical SHA `43d3a8dc0c6c50f044d533fd15b83a086edce6b9`.

Ancestry: `git merge-base --is-ancestor dbe7fbc3905b 43d3a8dc0c6c50f044d533fd15b83a086edce6b9` -> exit 0 (develop is an ancestor of the rebased head).

`git diff origin/develop...HEAD --name-only` -> 18 files, all mine:
`cmd/baha/app_apply_lifecycle.go`, `internal/application/management_ui.go`, `internal/application/perses_datasource_mount_test.go`, `internal/application/perses_datasource_seam.go`, `internal/application/perses_runtime.go`, `internal/application/runtime_contract.go`, `internal/application/runtime_postgres.go`, `internal/metrics/perses_datasource_lifecycle.go`, `internal/metrics/perses_datasource_lifecycle_test.go`, `internal/metrics/perses_prometheus_datasource.go`, `internal/metrics/perses_prometheus_datasource_container_test.go`, `internal/metrics/perses_prometheus_datasource_runtime.go`, `internal/metrics/perses_prometheus_datasource_runtime_test.go`, `internal/metrics/perses_prometheus_datasource_test.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/testdata/perses-prometheus-datasource/{config.yaml,globaldatasource.json,prometheus.json}`.

`git diff 1c0e33ad864e 43d3a8dc0 -- internal/serviceaccess/perses_compose_realization.go internal/application/perses_runtime.go` -> 0 lines (byte-identical; my card does not change the tmpfs realization that card 0428-177 owns).

## repo-rule compliance

- One PR per card (0428-083 = PR #1684); no reopen, no close, no second branch.
- Rebase-forward via `--force-with-lease` only; never force-push to develop/main. Base is develop `dbe7fbc3905b`, an ancestor of the head.
- `git log --oneline develop..HEAD` top commit is only my card commit `43d3a8dc0 0428-083 datasources: adapt datasource mounts to develop's Perses compose signatures (decision b)`.
- No write to `cmd/baha/app_status_result.go` (card 078), no write to `internal/observability/**` (card 168, merged), no write to `.github/**` (owner scope).
- No subagents (4.8); every step executed in this session.
- The tmpfs mountpoint fix belongs to card 0428-177; this card leaves the realization untouched.

## smoke failure evidence (run 44717007640, PR #1684, head 43d3a8dc0c6c, 2026-11-20T10:12:15Z)

Job `PR · Native · native/docker/perses-runtime-smoke`, run-id 136222941263, conclusion `failure`. Same defect repeated in run 44717303429, run-id 136227165612 (`PR Selected Checks` = failure). Failing log line (trimmed):

```
error mounting "tmpfs" to rootfs at "/etc/perses/database": create mountpoint for /etc/perses/database mount: make mountpoint "/etc/perses/database": mkdirat /home/runner/.local/share/docker/.../overlayfs/3d7015008b25524673b2f8f31e8056e8f11998d8917cc9f4763db52eb85926c3/etc/perses/database: read-only file system
```

The test `TestPersesRuntimeSmokeDockerIsolated` (`internal/application/perses_runtime_test.go`, 11.51 s) fails at `runtime.UpProject` because the OCI runtime cannot create the tmpfs mountpoint at `/etc/perses/database` inside the container overlayfs. This is the documented hosted-runner tmpfs defect (upstream runc #2404, resolved upstream in runc #4417), not a defect in this card's diff. Card 0428-177 (`t-20261120-perses-tmpfs-mountpoint.md`) owns the product-side tmpfs fix.

## cleanliness: clean

## END

STATE x-m083: PR #1684 rebased onto develop head 43d3a8dc0; smoke red is the known card-177 tmpfs runner defect, not this card's diff; awaiting owner decision on whether to hold PR #1684 or proceed once 177 lands.
