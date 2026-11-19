# Fix 2 — 0428-083 runtime provisioning (PR #1684, correction round)

Mission: mission-083-runtime-provisioning.md · Card: t-20261114-r28-perses-datasources
Branch: lane-0428-083-datasources-r2 · Prior reviewed head: `ab6932296f1f24c2024810f10b155633d931f7d4`
Verdict being fixed: `evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083.md` (REQUEST CHANGES, "runtime provisioning absent")
Date: 2026-11-19

## PLAN

1. Reality check: fetch origin, verify develop (da76c5cf9) is an ancestor of the head ab6932296f, merge-tree conflict count. DONE
2. Study builder + Perses startup/config-rendering path; decide the provisioning realization (config.yaml + provisioning folder mount). DONE
3. Implement: materialize the validated datasource into the Perses runtime provisioning path (authorization, pinned native plugin, proxy, TLS preserved, no secrets). DONE
4. Window hopf onto develop e1dc2cf61 (coordinator window directive mid-round): monotonic merge, no content loss. DONE (merge a4a9efee9, 0 conflicts)
5. Add ONE runtime-level test (datasource appears in rendered/joined Perses config) + isolated runtime query/proxy/TLS check. DONE
6. Focused checks: go test ./internal/metrics ./internal/application ./internal/observability, go build ./..., go vet (three packages), gofmt -l (empty), source-readability-audit.sh (PASS), doc-tests (ok). DONE
7. Commit + push monotonic to lane-0428-083-datasources-r2 (no force), ancestor witnesses; PR draft=false kept. DONE (head f0adef107)
8. Observe exact-head PR run 44520439061 to terminal; record run id + executed cells. RUNNING
9. Evidence complete, commit + push planning repo (pull --rebase first), verify on origin/main, cleanliness END. PENDING

## Reality check + window hopf (coordinator window directive mid-round)

- Mission start: develop = `da76c5cf9`; `git merge-base --is-ancestor origin/develop ab6932296` -> YES (monotonic at dispatch).
- Window move: #1691 (0428-121) squash-merged at 2026-11-19T11:56:52Z, develop = `e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88` (ls-remote witness). `git merge-base --is-ancestor e1dc2cf61 ab6932296` -> NO -> hopped the branch monotonically per instruction: `git merge origin/develop` -> merge commit `a4a9efee9`, CLEAN (zero conflicts, zero markers, nothing to resolve — the e1dc2cf61 content and the 083 files are disjoint; `internal/observability/environment.go`, the envfilter tests and `internal/runtime/project_names.go` changed on develop only in files this card does not write).
- `git merge-tree --write-tree origin/develop <head>` at BOTH bases (pre-hop vs ab6932296, post-hop vs f0adef107): 0 CONFLICT lines each.
- Content-loss check: `git diff ab6932296 HEAD -- internal/metrics/perses_prometheus_datasource.go internal/metrics/perses_prometheus_datasource_test.go internal/metrics/testdata/perses-prometheus-datasource/prometheus.json` -> empty (the reviewed candidate's files survive the merge byte-identical; only develop-side files joined the tree).
- After the hopf, the focused suite was re-run at the merged tree (see "Checks" below).

## Base attestation

- Planning repo verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `https://github.com/mcpdev80/baseharbor-plan.git`). NOT workers/baseharbor-plan.
- Mission-start `origin/develop` = `da76c5cf9c963207038d5599bd130b89ecb1e8a4`; `git merge-base --is-ancestor origin/develop ab6932296f1f24c2024810f10b155633d931f7d4` -> exit 0 (monotonic at dispatch); `git merge-tree --write-tree origin/develop ab6932296` -> 0 CONFLICT lines.
- Window hopf (coordinator directive mid-round): #1691 (0428-121) merged as squash, develop moved to `e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88`. `git merge-base --is-ancestor origin/develop ab6932296` -> NO -> the branch was hopped monotonically: merge commit `a4a9efee9` "Merge remote-tracking branch 'origin/develop' into lane-0428-083-datasources-r2 (window hopf onto e1dc2cf61)". Merge of develop INTO the candidate: zero conflicts, zero content loss.
- Final candidate head: `f0adef107bf9d95ac2537a1e224783d3eed962d5`. Ancestor witnesses (all exit 0): `e1dc2cf61 -> HEAD`, `ab6932296 -> HEAD`, `8c71395045 -> HEAD`. Post-hopf `git merge-tree --write-tree origin/develop HEAD` -> 0 CONFLICT lines.
- `git log --oneline origin/develop..HEAD` lists ONLY this chain's commits: f0adef107 (this round's feature commit), a4a9efee9 (window hopf merge), ab6932296 (prior hopf merge), 8c71395045 (the 083 feature commit). No foreign candidate is carried.

## Does new develop touch my write-set? (coordinator question)

Measured `git show e1dc2cf61 --name-only` (#1691 squash content): it changes `internal/observability/environment.go`, `internal/observability/envfilter_route2_test.go`, `envfilter_route5_listseam_test.go`, `internal/runtime/project_names.go`, `internal/logs/*`, `internal/metrics/prometheus_files.go`, `prometheus_test.go`, `prometheus_verify.go` and `cmd/baha` logs/traces — it does NOT touch `internal/metrics/perses_prometheus_datasource*.go` or my new testdata. The shared-package compile risk was re-verified at the merged head: `go build ./...`, `go vet ./internal/metrics ./internal/application ./internal/observability` and full `go test` of those three packages all PASS (no semantic collision).

## Worktree

Product work happens in `/tmp/opencode/083-datasources-r2-wt` (branch `lane-0428-083-datasources-r2`, fast-forwarded to the remote head `ab6932296f` before editing; `git status --porcelain` empty).

## Design decision — where Perses consumes the datasource

Measured remote truth (git ls-remote + fetch, 2026-11-19): exactly ONE branch in the repository carries the Perses runtime container — `lane-0428-088-perses-runtime` (head `76331c7d8`, PR #1592, open). No branch on origin carries BOTH `internal/application/perses_runtime.go` and `internal/metrics/perses_prometheus_datasource.go`; develop (`da76c5cf9`) carries NEITHER. So the runtime consumer of this card's output exists only as the still-unmerged content of the dependency card 0428-088 (card `depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime, t-20261114-r28-perses-signal-inventory]`; AGENTS 3.8: "gewartet wird nur auf Inhalte, nie auf Merges"). `perses_runtime.go`'s `writePersesUIComposeService` starts Perses with `--config=/etc/perses/config.yaml` (command at its line ~75) while mounting only `server.cert`/`server.key` — that file never existed anywhere: Perses could not read any datasource.

Realization in this correction round (per the Perses v0.55 provisioning contract — https://perses.dev/docs/perses/latest/configuration/provisioning/ : a config with a file database plus `provisioning.folders` injects the resources in those folders into the database at startup and reconciles them at the configured interval; the provisioning file schema is the API resource schema):

- `internal/metrics/perses_prometheus_datasource.go` gains (additive, same file per the recipe):
  - `BuildPersesPrometheusDatasourceAt(m, dataDir, namespace)` — the Target-bound public entry over the existing fail-closed builder (selected-surface gate, pinned release validation, metrics-policy source authorization, materialized endpoint, retained-snapshot source tie-in; no live probe => reachability "unverified").
  - `MaterializePersesPrometheusDatasourceAt(m, dataDir, namespace)` — the provisioning call site. Builds fail-closed, then writes the two artifacts Perses reads at startup, at the application's compose context root `<dataDir>/applications/<project>/providers/management-ui/perses/` (project = `RuntimeProjectName` = `baseharbor-<name>-<env>`, the exact root 088's compose mounts against — precedent: `internal/application/runtime_retirement.go` uses `applications/<project>`):
    - `config.yaml` — the exact file `--config=` consumes (database file/folder + `provisioning.folders` + reconcile interval), and
    - `provisioning/globaldatasource-baseharbor-prometheus.json` — a Perses-native `GlobalDatasource` provisioning resource (v0.55 schema verified against the pinned image tag's `dev/data/4-globaldatasource.json` and the `internal/cli/file` loader semantics): `kind: GlobalDatasource`, `metadata.name: baseharbor-prometheus`, `spec.default: true`, `spec.plugin.kind: PrometheusDatasource` (the pinned native plugin kind), `spec.plugin.spec.proxy.kind: HTTPProxy` carrying `url` + the pinned Prometheus API `allowedEndpoints` (access stays proxy, never direct). No secret, token or credential value is ever written; the authentication class stays an owner reference.
  - `RemovePersesPrometheusDatasourceAt(m, dataDir, namespace)` — ownership-safe teardown of exactly this card's projection subtree.
  - `PersesDatasourceProviderPaths(dataDir, namespace, m)` — the two provider-relative mount sources for the compose mount lines (finding below).
- Fail-closed materialization: an unselected surface or any builder error removes the provisioning artifacts (a stale datasource can never be served by a deselected surface), and an unwritable path is an error, never a silent skip.
- `internal/application/perses_runtime.go` (owned by the still-open 0428-088 lane, head `76331c7d8`, NOT on develop) and `internal/application/management_ui.go` (owned by the still-open 0428-084 lane, PR #1598, head `3852472aa`, NOT on develop) are NOT modified — editing them here would be a write-set collision and would carry a second card's content onto this chain. The mount gap is reported as a finding with file:line below.

## Runtime witness — which file Perses gets at startup

- `internal/application/perses_runtime.go:75` (branch `lane-0428-088-perses-runtime` @ `76331c7d8`): `command: ["--config=/etc/perses/config.yaml", ...]` — that in-container path is what the compose service starts Perses with. This candidate produces exactly that file (`<dataDir>/applications/baseharbor-<name>-<env>/providers/management-ui/perses/config.yaml`, test witness: `TestPersesPrometheusDatasourceRuntimeProvisioning` logs/assert the path and content) plus the provisioning folder it names. The two container bind mounts are the 088 render's job (finding below: perses_runtime.go:77-84 currently mounts only the cert pair).
- Provisioning call site (this card): `MaterializePersesPrometheusDatasourceAt` in `internal/metrics/perses_prometheus_datasource_runtime.go` (exported entry, the deployment path invokes it at the apply boundary once 088's Perses service renders; the builder core it consumes is the existing `buildPersesPrometheusDatasourceAtWithRelease` — the Target-bound builder this file already carried).
- Persistence folder: `/persistence/database` (file database on the `<service>-data` volume mounted at `/persistence`, `internal/application/perses_runtime.go:82` on the 088 branch — witness that the config's database folder exists).

## Tests

- `TestPersesPrometheusDatasourceRuntimeProvisioning` (internal/metrics, runtime-level): materializes at a real state root, then reads the JOINED configuration: parses `config.yaml`, follows `provisioning.folders` to the folder the server loads, and decodes the `GlobalDatasource` resource from that folder — pins kind/plugin-kind/proxy kind, `spec.default`, the exact materialized endpoint URL, the 6-entry pinned Prometheus API allowlist, the absence of `directUrl` and of any secret-bearing key, and the provider-root path layout the compose mounts consume.
- `TestPersesPrometheusDatasourceRuntimeProvisioningFailClosed`: authorization revoked (policy collects only `application-provider` while the snapshot carries the platform source) and surface deselected -> materialize errors AND the previously written artifacts are removed (no stale datasource survives).
- `TestPersesPrometheusDatasourceRuntimeProxyQueryTLS` (isolated runtime query/proxy/TLS check): live HTTPS Prometheus-shaped endpoint (httptest TLS, private leaf), the materialized proxy URL equals the endpoint, the health query over a client pinned to that CA verifies up=1 and the server sees the exact authorized `max(up{...})` query, and an empty-pool client fails closed at the TLS layer.
- Goldens: `TestPersesPrometheusDatasourceGlobalDatasourceGoldenFile` (testdata/perses-prometheus-datasource/globaldatasource.json) and `TestPersesPrometheusDatasourceConfigGoldenFile` (config golden), plus `TestPersesPrometheusDatasourceProxyURLFailClosed` (endpoint contract negatives).
- Retained: the full pre-existing datasource suite (fail-closed/unselected/denied/golden cells) is untouched and green.
- CI pickup duty: every new test lives in `internal/metrics` package tests, executed by the existing `PR · Go unit · packages` shard on every PR push (targeted checks select `internal/metrics`); no `.github/**` change is needed for the unit coverage. The host-gated compose-level join (actual container mount) runs where 088's runtime gate executes (`targeted-integration.yml`; `internal/application/perses_runtime_test.go` composes the mounts). The mount lines themselves are the file:line finding below, not a silent CI gap of this card.

## Checks

- `go build ./...` -> exit 0. `go vet ./internal/metrics ./internal/application ./internal/observability` -> exit 0. `gofmt -l .` -> empty.
- `go test ./internal/metrics -count=1` -> ok; `go test ./internal/application -count=1` -> ok; `go test ./internal/observability -count=1` -> ok (post-hopf tree, merged with e1dc2cf61).
- Doc-test gate: `go test ./cmd/baha -run "TestMachineDocumentation|TestHumanDocumentation" -count=1` -> ok (no new CLI command/parameter introduced; nothing to classify).
- `bash scripts/source-readability-audit.sh` -> PASS (file size / function span / regression ratchet; baseline podman/lifecycle.go 843 lines untouched).

## Findings (file:line)

- `internal/application/perses_runtime.go:75-84` (branch `lane-0428-088-perses-runtime` @ `76331c7d8`, NOT on develop): the Perses compose service starts `--config=/etc/perses/config.yaml` but mounts only `./providers/management-ui/perses/server.cert` and `server.key` (volumes, lines 80-82); the config file and provisioning folder never reach the container. Required change at the 088 integration (this lane must not edit #1592's file):
  - volume line `- ./providers/management-ui/perses/config.yaml:/etc/perses/config.yaml:ro`
  - volume line `- ./providers/management-ui/perses/provisioning:/etc/perses/provisioning:ro`
  - call `metrics.MaterializePersesPrometheusDatasourceAt` at the deploy boundary before the Perses service starts.
- `internal/application/management_ui.go:139` (develop `e1dc2cf61`): the `EnsureApplicationManagementUIs` early-return gate omits `m.Services.Perses`/`ObservabilityManagementUI`, so the Perses projection path is only reached through the 088/084 branches' own call sites. For the integration window.

## Realization witness (provisioning files are exactly what Perses loads)

Verified directly against the pinned release `v0.55.1` (GitHub contents API at tag `v0.55.1`):

- Config schema `pkg/model/api/config/database.go`: `File{folder, extension}` accepts exactly "json"/"yaml" ("wrong file extension defined when using the filesystem as a database..." otherwise); `Database.Verify()` requires at least one of file/sql — the config keys this projection writes exist as documented and the json extension matches the loader.
- Provisioning schema `pkg/model/api/config/provisioning.go`: `ProvisioningConfig{folders []string, interval Duration, enable_watch bool}` — `provisioning.folders` is exactly the key the loader consumes.
- Loader `internal/api/provisioning/service.go` -> `internal/cli/file/file.go`: walks configured folders recursively, accepts only `.json`/`.yaml`/`.yml` by extension, reads `kind` from each object, `modelV1.GetStruct(kind)` must resolve, then unmarshals into the API resource struct (a list-shaped JSON document decodes as multiple entities). The `GlobalDatasource` kind resolves through GetStruct, so the shipped resource loads.
- Provisioned resource shape matches the pinned image's own shipped example `dev/data/4-globaldatasource.json`: `kind`, `metadata.name`, `spec.default`, `spec.plugin.kind`, `spec.plugin.spec.proxy.{kind: HTTPProxy, spec: {url, allowedEndpoints}}`.
- Docs (perses.dev v0.55 "Provisioning"): resources in the configured folders are injected into the database at startup and re-injected at the configured interval; provisioning data overrides the database; unmanaged files are ignored.

## Deviation note — file split within the recipe's file set

The recipe names `internal/metrics/perses_prometheus_datasource.go` and the Perses startup/config-rendering path under `internal/application/` as the change surface. The datasource file is at 412 lines at the reviewed head; the provisioning realization (~350 lines with contracts) is a sibling file `internal/metrics/perses_prometheus_datasource_runtime.go` inside the SAME package, keeping files well under the 800-line limit (DEVELOPMENT_GUIDELINES §12) and leaving the builder's fail-closed core untouched. Documented deliberately, not silent.

## Checks (at final head f0adef107, post-hopf tree)

- `go build ./...` -> exit 0.
- `go vet ./internal/metrics ./internal/application ./internal/observability` -> exit 0.
- `gofmt -l .` -> empty.
- `go test ./internal/metrics -count=1` -> ok; `go test ./internal/application -count=1` -> ok; `go test ./internal/observability -count=1` -> ok. (No full `go test ./...` per mission — the CI covers breadth.)
- Doc-test gate: `go test ./cmd/baha -run "TestMachineDocumentation|TestHumanDocumentation" -count=1` -> ok (no new CLI command/parameter; nothing to classify in machine_coverage.go).
- `bash scripts/source-readability-audit.sh` -> PASS x3 (file size / function span / regression ratchet; baseline `internal/providers/runtime/podman/lifecycle.go` 843 lines untouched).

## repo-rule compliance

- Fail-closed everywhere (§2): selection, pin, authorization, endpoint and snapshot errors propagate and remove stale provisioning; no empty artifact with nil error path exists.
- Secrets (§6): the provisioning artifacts carry endpoint URL and owner references only; the test scans both files for secret-bearing keys and fails on any.
- Lifecycle (§8): materialize belongs to the apply boundary; the compose render that mounts the artifacts is the 088 content (finding), so nothing in plan/preflight mutates.
- Scoped change (§11): no refactors; `internal/application/` startup/config path deliberately NOT edited — those files carry unmerged 088/084/089 lane content and editing them here would put a second card's work on this chain (write-set rule); the integration mount is a recorded finding with file:line.
- One candidate per chain (§3.8): all commits land on the named branch `lane-0428-083-datasources-r2`; no second branch.
- No `.github/**`, no `scripts/**` edits; no reruns/dispatch; no merge; no PR comments on foreign PRs; no subagent (§4.8); targeted `git add <file>` only; worktree under /tmp/opencode (workspace layout rule); quarantined checkout never cited (all remote witnesses via `git ls-remote`/`gh api`/fetch in my own worktree).
- VM smoke: this mission names no VM test; the runtime-level proof is the unit/host-runnable `internal/metrics` tests, which the existing `PR · Go unit · packages` CI job executes on every PR push (no .github change needed).

## CI

(fill)

## CI

(observe run 44520439061 to terminal here; §4.6)

## Cleanliness witnesses (before)

`docker ps -a --format '{{.Names}} {{.Status}}'` on this coordinator server host (read-only witness, 2026-11-19): ambient containers only, belonging to other cards/infrastructure:

## END

(fill)
