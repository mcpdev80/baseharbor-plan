# Fix 2 — 0428-083 runtime provisioning (PR #1684, correction round)

Mission: mission-083-runtime-provisioning.md · Card: t-20261114-r28-perses-datasources
Branch: lane-0428-083-datasources-r2 · Prior reviewed head: `ab6932296f1f24c2024810f10b155633d931f7d4`
Verdict being fixed: `evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083.md` (REQUEST CHANGES, "runtime provisioning absent")
Date: 2026-11-19

## PLAN

1. Reality check: fetch origin, verify develop (da76c5cf9) is an ancestor of the head ab6932296f, merge-tree conflict count.
2. Study builder + Perses startup/config-rendering path; decide the provisioning realization (config.yaml + provisioning folder mount).
3. Implement: materialize the validated datasource into the Perses runtime provisioning path (authorization, pinned native plugin, proxy, TLS preserved, no secrets).
4. Add ONE runtime-level test (datasource appears in rendered/joined Perses config) + isolated runtime query/proxy/TLS check.
5. Focused checks: go test ./internal/metrics ./internal/application, go build ./..., go vet (two packages), gofmt -l, source-readability-audit.sh.
6. Commit + push monotonic to lane-0428-083-datasources-r2 (no force), ancestor witness; keep PR draft=false.
7. Observe exact-head PR run to terminal; record run id + executed cells.
8. Evidence complete, commit + push planning repo (pull --rebase first), verify on origin/main, cleanliness END.

## Base attestation

- Planning repo verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `https://github.com/mcpdev80/baseharbor-plan.git`). NOT workers/baseharbor-plan.
- `origin/develop` = `da76c5cf9c963207038d5599bd130b9ecb1e8a4` (git ls-remote + fetch origin --prune, 2026-11-19).
- `git merge-base --is-ancestor origin/develop ab6932296f1f24c2024810f10b155633d931f7d4` -> exit 0 (monotonic, no hopf needed).
- `git merge-tree --write-tree origin/develop ab6932296f1f24c2024810f10b155633d931f7d4` -> 0 CONFLICT lines.
- New commits in this round are cut from `ab6932296f1f24c2024810f10b155633d931f7d4` (the current branch head) and will list ONLY this lane's commits in `git log origin/develop..HEAD` beyond the prior candidate.

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

## Findings (file:line)

- `internal/application/perses_runtime.go:75-84` (branch `lane-0428-088-perses-runtime` @ `76331c7d8`, not yet on develop): the Perses compose service starts `--config=/etc/perses/config.yaml` but mounts only `server.cert`/`server.key`; without two additional bind mounts the provisioned config and datasource never reach the container. Required change at the 088 integration point (this lane must not edit #1592's file):
  - `      - ./providers/management-ui/perses/config.yaml:/etc/perses/config.yaml:ro`
  - `      - ./providers/management-ui/perses/provisioning:/etc/perses/provisioning:ro`
  - and the deployment boundary (088's `EnsurePersesManagementUI`, `internal/application/perses_runtime.go:100`) calls `metrics.MaterializePersesPrometheusDatasourceAt` — cross-package import (application -> metrics) needs an integration owner decision, matching the existing seam where `internal/metrics/management_ui.go:13` calls into `internal/application` the other way.
- `internal/application/management_ui.go:139` (develop `da76c5cf9`): the `EnsureApplicationManagementUIs` early-return gate omits `m.Services.Perses`, so a Perses-only selection never reaches the 088 Perses projection either. Finding for the integration window (088's own head already adds the condition at its line ~139).

## Realization witness (provisioning files are exactly what Perses loads)

- Perses v0.55 provisioning loader (`internal/api/provisioning/service.go` -> `internal/cli/file/file.go`, verified at tag v0.55.1): walks configured folders recursively, accepts only `.json`/`.yaml`/`.yml`, reads `kind` per object, resolves it via `modelV1.GetStruct(kind)`, then unmarshals into the API resource struct; unsupported/unmanaged files are ignored (doc: "Perses will ignore any files not managed").
- The shipped example `dev/data/4-globaldatasource.json` at v0.55.1 carries exactly the shape this adapter emits (`kind: GlobalDatasource`, `metadata.name`, `spec.default`, `spec.plugin.kind: PrometheusDatasource`, `spec.plugin.spec.proxy.{kind: HTTPProxy, spec.url, allowedEndpoints}`).
- The config schema is `pkg/model/api/config/{config,database,provisioning}.go` at v0.55.1; `ProvisioningConfig` = `folders` + `interval` + `enable_watch` (quoted by the docs page above).

## Deviation note — file split within the recipe's file set

The recipe names `internal/metrics/perses_prometheus_datasource.go` and the Perses startup/config-rendering path under `internal/application/` as the change surface. The datasource file is at 412 lines at the reviewed head and the repository rule caps non-test Go files at 800 lines (DEVELOPMENT_GUIDELINES §12); the provisioning realization (~230 lines with contracts) is therefore a sibling file `internal/metrics/perses_prometheus_datasource_runtime.go` inside the SAME package, so the exported entry point named in the recipe lives in the metrics package and the builder's fail-closed core stays untouched. Documented here deliberately, not silent.

## repo-rule compliance

(fill)

## CI

(fill)

## Cleanliness

(fill)

## END

(fill)
