# fix-9 — 0428-083 perses datasources, adapt to develop's Perses compose signatures (decision b)

**Card:** t-20261114-r28-perses-datasources / **PR:** #1684 / **Lane:** lane-0428-083-datasources-r2
**Worker:** x-083h5 / **Date:** 2026-11-20
**Outcome:** Content adapted + committed + pushed. **END_BLOCKED** on the native gate — the single failing CI gate (`native/docker/perses-runtime-smoke`) is a Docker rootless-overlayfs **tmpfs** regression on the CI runners, **not** a card defect. All Go gates (build/vet/unit/contracts) are green.

---

## 1. What changed (decision b, binding)

The coordinator's decision (b): strip the compose rename/extra parameter, keep the datasource mounts on develop's existing 3-arg Perses compose signatures.

- `writePersesGatewayComposeServices(b *strings.Builder, m Manifest, files RuntimeFiles)` — **stays 3-arg** (develop's signature). The datasource splice call uses `files.Dir` as the compose context dir, not a 4th parameter:
  ```go
  if err := splicePersesDatasourceMounts(&rendered, files.Dir, files.ResourceProject); err != nil {
  ```
- `RuntimeComposeYAMLForContextDir` **removed** — dead (never called, two exported paths for one semantics). Only `RuntimeComposeYAMLForProject(m, files)` remains.
- `runtimeComposeYAMLForProject(m, resourceProject string, files RuntimeFiles)` — the private helper keeps the `files RuntimeFiles` param (develop's shape); the dead `contextDir := files.Dir` local was removed.
- Call site in `runtime_postgres.go`: `writePersesGatewayComposeServices(&b, m, files)` (3-arg).

**Datasource logic is byte-identical** to the prior candidate 576c6ad8 (only compose signatures adapted):

```
$ git diff --name-only 576c6ad8fb1a 1c0e33ad \
    internal/metrics/perses_prometheus_datasource.go \
    internal/metrics/perses_datasource_lifecycle.go \
    internal/application/perses_datasource_seam.go
# (empty — my datasource files are byte-identical)
```

## 2. Commit / branch witness

```
$ git ls-remote origin refs/heads/develop
36d075fad77fa61ac8c153e979855546589b32c2  refs/heads/develop
$ git ls-remote origin refs/heads/lane-0428-083-datasources-r2
1c0e33ad864ed3e43b7dbaee57093c507ab90e40  refs/heads/lane-0428-083-datasources-r2
$ git show -s --format="%H %P" HEAD
1c0e33ad864ed3e43b7dbaee57093c507ab90e40 36d075fad77fa61ac8c153e979855546589b32c2
$ git log --oneline origin/develop..HEAD
1c0e33ad 0428-083 datasources: adapt datasource mounts to develop's Perses compose signatures (decision b)
```

Single linear commit `1c0e33ad`, parent = newest develop tip `36d075fa`. Branch history shows only my commit. Pushed with `--force-with-lease` (`6b40ad5a → 1c0e33ad`). PR #1684 state=OPEN, mergeable=MERGEABLE.

## 3. Test-first proof (decision b's core)

Test `TestPersesDatasourceMountResolvesAgainstComposeContextDir` (in `internal/application/perses_datasource_mount_test.go`) pins the contract: a Prometheus datasource mount the gateway Perses service carries resolves against the **compose context-dir** (`RuntimeFiles.Dir`), so the mount source, resolved relative to `files.Dir`, lands on the datasource projection root the apply boundary materialized.

- **RED on pure develop** (deps absent):
  ```
  $ go vet ./internal/application/
  vet: internal/application/perses_datasource_mount_test.go:20:23: undefined: datasourceMountRoots
  ```
  `datasourceMountRoots` / `persesDatasourceMounts` / `PersesDatasourceContainerConfigPath` are my seam code — absent on develop → compile error = red.

- **GREEN with my (b) change**:
  ```
  $ go test ./internal/application/ -run TestPersesDatasourceMountResolvesAgainstComposeContextDir -v
  --- PASS: TestPersesDatasourceMountResolvesAgainstComposeContextDir (0.46s)
  ok   github.com/mcpdev80/baseharbor/internal/application  0.462s
  ```

## 4. Regression isolation (why the CI failure is not my code)

The ONLY diff between the prior candidate 576c6ad8 (passed CI run #6693) and this adapted head 1c0e33ad in the Perses render path is `contextDir := files.Dir` (extracted local) vs `files.Dir` (passed directly to the splice) — **the identical value**. The rendered compose is therefore byte-identical.

- `TestRenderPersesServiceBlockIdentical` and `TestExactComposeRenderProvesNoRegression`: PASS — the datasource splice is a correct no-op when no artifacts are present (the smoke-test path).
- The failing mount (`/etc/perses/database`) is **develop's code**, not mine:
  ```
  $ git grep -n "/etc/perses/database:rw,noexec,nosuid,nodev" origin/develop -- '*.go'
  internal/serviceaccess/perses_compose_realization.go:388:  b.WriteString("      - /etc/perses/database:rw,noexec,nosuid,nodev\n")
  ```
  My commit adds zero lines of tmpfs/database.

## 5. CI failure — root cause (STATE, infra, not card)

CI run #44671189705 (head `1c0e33ad`) and #44667006086 (head `6b40ad5a`) both ran the required `native/docker/perses-runtime-smoke` gate. Both failed; every other gate (Go unit shards cli-0..3 + packages + owner, go-build, go-vet, contracts, PR Selected Checks) passed. The gate runs `TestPersesRuntimeSmokeDockerIsolated` with `BASEHARBOR_PERSES_RUNTIME_SMOKE=1`.

The failure reproduces **identically on this local host** and on the **Azure GitHub-hosted runners**:

```
error mounting "tmpfs" to rootfs at "/etc/perses/database":
  create mountpoint for /etc/perses/database
  mount: make mountpoint "/etc/perses/database":
  mkdirat /home/marcel/.local/share/docker/rootfs/overlayfs/<sha>/etc/perses/database: read-only file system
```

Both the 4-arg candidate (576c6ad8) and the 3-arg adaptation (1c0e33ad) hit this exact error. The tmpfs mount at line 388 of `perses_compose_realization.go` is develop's, present in both candidates. This is a Docker rootless-overlayfs tmpfs limitation — the container's `/etc/perses/database` path cannot have a tmpfs mounted onto a read-only overlay rootfs. It is a runner/daemon environment regression, not a card defect.

Witnesses:
- Local host: `TestPersesRuntimeSmokeDockerIsolated` FAILS on both 576c6ad8 and 1c0e33ad with the read-only tmpfs error above.
- CI #6693 (576c6ad8): success. CI #44667006086 (6b40ad5a) and #44671189705 (1c0e33ad): failure, same tmpfs error class. The runners' tmpfs-on-overlayfs behavior regressed between #6693 and the later runs.

**Go gates are green** for this card:
```
$ go build ./...                       # BUILD 0
$ go vet ./internal/application/... ./internal/metrics/...   # VET 0
$ go test ./internal/application/ ./internal/metrics/ ./contracts/...   # all ok
$ gofmt -l internal/application/perses_runtime.go internal/application/runtime_postgres.go ...  # clean
```

## 6. Why no fresh full CI re-run

Per CI execution discipline, a fresh run is only warranted for a relevant changed input or a diagnosed failure that a re-run would resolve. The failure is diagnosed as a runner tmpfs regression (identical on hosted + local hosts, byte-identical rendered compose between passing/failing candidates). A re-run on the same runner image would reproduce the same infra failure and consume runner capacity without resolving the root cause. The card's Go gates are green and the native smoke gate's failure is provably not my code.

**Blocker requires Owner action:** the `native/docker/perses-runtime-smoke` gate is required for my card (my touched `perses_runtime.go` classifies as `application-perses-runtime-smoke`). Resolving it needs the runner image / rootless-Docker daemon tmpfs behavior fixed (or an explicit Owner decision that this transient infra failure is waived for this card). Until then the gate stays red for reasons outside my write-set.

## 7. Repo-rule compliance

- Single linear commit on the current develop tip; no foreign commits; `git add` scoped to my files only.
- No `.github`/workflow/script changes; no subagents (§4.8); no VM/container/network/volume persisted.
- Datasource logic byte-identical; only compose signatures adapted per decision (b).
- Content proof (datasource files unchanged), red/green test witness, ls-remote witnesses captured above.
