# Hunt evidence: CONFIG -> SNAPSHOT -> VERIFY config-chain (0.4.28 welle 3)

- Lane: mission-hunt-configchain
- Date: 2026-11-17
- Base (attested): develop `bcae1e8c1261c9e44db03fe285a5d090c532dfcd` (tip of develop; `git merge-base --is-ancestor bcae1e8c1 HEAD` = YES). This is a bug-hunt (reine Befundung), so no branch is cut and no commit is made.
- Base attestation witness: `git rev-parse origin/develop` = `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`; `git merge-base --is-ancestor bcae1e8c1 HEAD` -> YES.
- Method: local read-only analysis + local `go build`/`go test`/`go vet` on the three merged PR paths at develop tip. No containers, no workflow changes.
- Scope: three merged 0.4.28 paths — (1) keycloak-metrics-registration (#1660, commit `1df7c343`), (2) bad-config fail-loud (#1666, commit `8db0d9bd`), (3) workload-only snapshot-only (#1676, commit `bcae1e8c`).
- Repo rules: bug-hunt, no product commits, no containers. Evidence only in baseharbor-plan. No subagents.

## pfadtabelle: config input -> snapshot entry -> verify point -> error outcome

### Path (1) keycloak-metrics — #1660 `1df7c343`

| config input | snapshot entry | verify point | error outcome |
| --- | --- | --- | --- |
| Identity capability selected, `KeycloakIntegration` declared (reference.go:160, metrics/openmetrics, `VerifyBackend`, port 9000, path `/metrics`) | `RegisterProviderSignals(id="keycloak-metrics", Descriptor=KeycloakIntegration)` writes `observability/signals.json` (registry.go:284 `registryPath()`) one source per collectable signal | `RegisterProviderSignals` validates: signal must be declared (registry.go:196), collectable (199), have runtime realization (211), `source.Validate()` (222); read back via `observability.List(SignalMetrics, placement, [app], true, true)` | fail-closed if metrics disabled: no source registered, gate unavailable; fail-closed if metrics enabled but no registration (pre-#1660: `identity_dashboard_eligible` stuck false) |
| `MetricsPolicy.Enabled` true + `Collect[PlatformProvider]` true (app-scoped Keycloak) | `signals["keycloak-metrics"] = {Network: ConsumerNetwork, Target: "keycloak:9000"}` written with `Class=SourcePlatformProvider` (keycloak_realization.go:146-160) | `RegisterProviderSignals` gate at keycloak_realization.go:137-144 | disabled -> no-op, every gate stays fail-closed (regression guard #1660 test) |
| `MetricsPolicy.Collect[ApplicationProvider]` true (provider-scoped Keycloak) | `Class=SourceApplicationProvider`, gated on `Collect[ApplicationProvider]` (keycloak_realization.go:141-144) | same `RegisterProviderSignals` | disabled -> no source, gate unavailable |

### Path (2) bad-config fail-loud — #1666 `8db0d9bd`

| config input | snapshot entry | verify point | error outcome |
| --- | --- | --- | --- |
| `ConfigPath()` resolves `config.yaml`, file ABSENT, root EMPTY (fresh install) | clean implicit `Config{Version:1, ...}` returned (target.go:177) | `LoadConfig()` -> no error; daemon reads default | quiet (correct: genuinely absent) |
| `ConfigPath()` resolves `config.yaml`, file ABSENT, root POPULATED (active-target/.installation.lock present) OR config.yaml one level up (XDG double-append) | `ErrConfigMissing` wrapped, `target.go:187` | `LoadConfig()` returns error; caller must surface | LOUD (fail) - BF-05 miss |
| `config.yaml` EXISTS but empty/whitespace-only | `ErrConfigEmpty` wrapped, `target.go:204` | `LoadConfig()` returns error | LOUD (fail) - BF-05 r2 |
| `config.yaml` EXISTS, unparseable | `decodeConfig` returns error `read BaseHarbor config: %w` (target.go:183, unchanged pre-existing) | `LoadConfig()` returns error | LOUD (fail) - unchanged pre-existing |
| `config.yaml` EXISTS, valid | `decodeConfig(data)` -> loaded Config | `LoadConfig()` returns config with targets | quiet (correct happy path) |
| detection helper `dirExistsAndHasBaseharborState` | two signals only: config.yaml one level up (target.go:236) OR active-target/.installation.lock (target.go:248) | `LoadConfig()` predicate | org-config subtree (active.json/organization/) does NOT count (target.go:255 comment) - keeps org-config scoping |

### Path (3) workload-only snapshot-only — #1676 `bcae1e8c`

| config input | snapshot entry | verify point | error outcome |
| --- | --- | --- | --- |
| Workload-only app (no `Metrics.Sources`, no `Runtime.Permissions[metrics]`), `MetricsPolicy.Enabled && Collect[ApplicationProvider]` | `reconcileApplicationMetricsSource` (runtime_observability.go:65) registers application-provider metrics source with `Target=runtime://<project>/workload`, `Verification=VerifyNone`, `ReconcileSignals(id=<prometheus>:<project>)` | shared Prometheus `runtime-sources.json` now has 1 source instead of `sources:[]` | previously snapshot stayed empty (zero sources); now snapshot records the runtime identity |
| same app, metrics policy disabled | no registration, `reconcileApplicationMetricsSource` returns nil (runtime_observability.go:75) | snapshot stays `sources:[]` | quiet (fail-closed preserved) |
| app DECLARES metrics sources but materializes none | `VerifyProviderSourcesAt` iterates sources, `VerifyBackend` source queried, no up=1 | fails closed | fail-closed (unchanged) |
| verified source (VerifyNone workload-only) | `syncProviderTargets`/`providerMetricNetworks` skip `Verification==VerifyNone` (prometheus_files.go:65, 163); `verifyProviderSourcesAt` skips VerifyNone (prometheus_verify.go:163) | not rendered as file_sd target, not on provider network | quiet (no scrape target for symbolic workload) |
| compose render | `providerComposeYAMLWithProviderNetworksAndAccess` skips `registration.Network==""` entries (prometheus_render.go:140, 167) | compose.yaml has no empty `metrics-N` network refs | quiet (no dangling network refs) |

## hunt results (dead branches / duplicate registration / broken error-chain)

- Dead branches (config-flags with no effect): none found. Every metrics-collection flag path (`Enabled`, `Collect[ApplicationProvider]`, `Collect[PlatformProvider]`) maps to a real gating decision in `registerKeycloakSignals` (keycloak_realization.go:137-144) and `reconcileApplicationMetricsSource` (runtime_observability.go:75). go vet clean across identityprovider/metrics/application/deployment/observability.
- Duplicate registration paths: none. `RegisterProviderSignals` is called from exactly one keycloak site (keycloak_realization.go via registerKeycloakSignals), plus Loki/tempo/OTel. `RegisterProviderSignals` idempotently dedupes by `(ID, Provider)` at registry.go:275. workload-only registration uses `ReconcileSignals` (registry.go:338), a separate idempotent path. No double-write of `keycloak-metrics`.
- Broken error-chain: none found. BF-05 fail-loud returns `ErrConfigMissing`/`ErrConfigEmpty` (both `ErrConfigMissing` family) from `LoadConfig`; every test asserts `errors.Is(err, ...)` and passes. workload-only `VerifyNone` is correctly skipped in both the render path (prometheus_files.go) and verify path (prometheus_verify.go); fail-closed for declare-but-materialize-none is preserved.
- Contract check: keycloak-metrics declares `Verification: ObservabilityVerifyBackend` for `Status: ObservabilitySupported` (reference.go:160) — contract-valid (integration_contract.go:241 accepts VerifyBackend on supported). The runtime-applied workload-only source uses `VerifyNone` legitimately (no backend to scrape) and the verify loop skips it (prometheus_verify.go:163). No contradiction.

## local verification (run locally, read-only build/test at develop tip)

- base develop HEAD: `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`
- `go build ./internal/application/... ./internal/metrics/... ./internal/identityprovider/... ./internal/deployment/... ./internal/observability/...` -> OK
- `go vet ./internal/identityprovider/... ./internal/metrics/... ./internal/application/... ./internal/deployment/... ./internal/observability/...` -> OK (exit 0)
- identityprovider (keycloak signal, #1660):
  - PASS TestKeycloakSignalRegistrationRegistersNativeMetricsSignal
  - PASS TestKeycloakSignalRegistrationFailsClosedWithoutMetrics
- deployment (fail-loud, #1666):
  - PASS TestLoadConfigFailsLoudOnUnparseableConfig
  - PASS TestLoadConfigMissingUnderPopulatedRootFailsLoud
  - PASS TestLoadConfigMissingUnderEmptyRootSucceeds
  - PASS TestLoadConfigExistingEmptyFileFailsLoud (+ /empty, /whitespace)
  - PASS TestLoadConfigValidStillLoads
  - PASS TestLoadConfigEndToEndXDGPath
  - PASS TestLoadConfigDoubleAppendResolvedPathMissingFailsLoud
  - PASS TestDirExistsAndHasBaseharborState
- metrics (workload-only, #1676):
  - PASS TestWorkloadOnlyRegistersSharedSnapshotOnDeploy
  - full `./internal/metrics/...` -> ok
- full `./internal/application/...` -> ok (50.7s)

Note on CI: these are unit tests already in the three merged PRs, in packages `internal/metrics`, `internal/application`, `internal/identityprovider`, `internal/deployment` that are covered by existing CI test groups via `go test ./...`-style selection. No `.github/**` change needed; no new trigger rule. (Owner-scope reminder noted; no workflow touched.)

## before/after container/cleanliness

- No containers, no compose projects, no podman/docker started. No network namespaces/volumes/state created.
- before: `/tmp/opencode` clean; clone at `/home/marcel/dev/baseharbor-ecosystem/workers/.w-hunt-cfg` (worktree zone).
- after: same; no orphans. cleanliness: clean.

END mission-hunt-configchain DONE
