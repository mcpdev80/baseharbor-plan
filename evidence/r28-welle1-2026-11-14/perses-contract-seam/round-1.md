# round-1 — 0428-075 define Perses prov seam

Lane: lane-0428-075-perses-seam (Worker, worker-ornith1.5-laptop)
Date: 2026-11-14
Card: t-20261114-r28-perses-contract-seam (0428-075), release v0.4.28
Base attest: cut from base develop 0e9ccb582f5bdcdc74049bbe3996263cdce6500c (origin develop, `git ls-remote origin develop`)
Branch provenance: my first commit is built on 0e9ccb582; git log lists only my own commits (witness pasted below).
PR: #1575 (DRAFT, base develop 0e9ccb582), https://github.com/mcpdev80/baseharbor/pull/1575

git log (only my commit on top of base develop):
61f76fa18 feat(0428-075): define optional Perses provider seam (fail-closed)
0e9ccb582 chore: pin v0.4.27 demo acceptance (#1573)

## PLAN

- Inspect existing provider registry, capability, catalog/registry distinction, provider-contract-v1 scope
- Research Perses upstream version/plugins/provisioning/upgrade/security via context7 + websearch, cite sources
- Design optional Perses management seam compatible with Provider Contract v1; fail-closed "not configured", no false metrics/logs/traces
- Implement declarative Perses provider seam in assigned files only (preserve ownership, TLS, lifecycle, auth)
- Write deterministic negative/ownership/auth tests; wire into affected CI group
- Run local tests + go vet/build; report hosted CI run of touched group (draft PR, base develop)
- Write evidence file, commit evidence to origin/main, post SOP lines + END to coordinator

## Repo-rules compliance

- Planning repo verified as /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (real origin, git log --oneline -1). workers/baseharbor-plan is the bookkeeping repo and was never touched.
- No .github/** edited. No subagents spawned. Every step done in this session.
- Branch cut from base develop SHA 0e9ccb582, which is an ancestor of my first commit.
- Evidence lives only in baseharbor-plan evidence/ (never in the product repo).

## Inspect: current provider/capability/observability surface

What the current Core ships (verified against base develop 0e9ccb582):

- Provider Contract v1: `internal/capability/integration_contract.go`. `IntegrationDescriptor` carries ID, version, protocol (`baseharbor.provider/v1`), provider kind, capability specs, placement scopes, interfaces, and an `Observability` block of `ProviderObservabilitySignal`s. `Validate()` is fail-closed: unsupported status cannot carry realization details, supported native metrics must be openmetrics with a port+path, and every supported signal must declare a verification mode.
- Capability catalog vs registry distinction: `internal/provider/builtin/catalog.go` (installable distribution) vs `internal/application/provider_registry.go` (deployed instances/placement/ownership). Provider artifacts SHOULD use OCI; digest is immutable identity, tags are discovery aliases. This is where a Perses product version lives: as realization metadata, NOT as the provider implementation version or capability spec version.
- `internal/capability/reference.go`: reference descriptors. Prometheus/Loki/Tempo each own one backend (`Metrics`/`Logs`/`Traces`) under `ServiceObservability`, each with an optional `management-ui` interface classed `InterfaceObservability`, protocol `https`.
- Observability signals: `internal/capability/integration_contract.go` (kinds/statuses/modes/verifications) + reference descriptors. Prometheus declares `prometheus-metrics` unsupported (its native scrape is provider-owned); Loki/Tempo declare their own native metrics supported on ports 3100/3200.
- Existing management UI realization: `internal/metrics/management_ui.go` (Prometheus `management-ui` surface, `ObservabilityManagementUI` gate), `internal/application/management_ui.go` (pgadmin/cache/mongo/rabbitmq UIs + TLS + `ApplicationManagementUISurfaces`), `internal/providerui/application.go` (compose projection for admin UIs), `cmd/baha/app_dev_routing.go` (canonical dev routes, `shared/prometheus` route at :9090).
- Fail-closed today: `internal/application/manifest_validation.go` lines 500-514 — `observability.management_ui` requires managed metrics because Prometheus is the current browser-capable observability surface.
- Acceptance matrix: `docs/spec/provider-management-acceptance-v1.md` row `Prometheus management surface` (auth `native-credential or explicit unsupported when anonymous`, `limited`). Prometheus/Loki/Tempo rows are the backend data owners.
- Management access: `docs/spec/management-access-v1.md` — exactly one effective auth class per surface (`native-oidc`/`standards-auth-adapter`/`native-credential`/`unsupported`), roles `admin/edit/view/audit`, "reported as unsupported rather than silently creating an unrelated human-user source".

## Perses upstream facts (context7 + websearch; sources in Akte)

- Latest stable: Perses v0.55.1, released 2026-11-02 (source: perses.dev/download + GitHub CHANGELOG). Docker: `persesdev/perses:v0.55.1`; distroless (production) / distroless-debug; arm64+amd64.
- Security (v0.55.0): large set of critical fixes — JWT forgery, SSRF, credential leaks through datasource proxy, arbitrary file reads, path traversals in the file-system database. When authentication is enabled, an encryption key is now MANDATORY. Datasource proxy denies loopback/link-local/cloud-metadata/K8s-API destinations by default. => pin v0.55.1 (or later pinned release); never v0.54.x or earlier for this release; authentication is opt-in, not default-on.
- Prometheus plugin `PrometheusDatasource` (module v0.6.0): HTTP datasource with opt-in Proxy (Perses server forwards queries; avoids browser CORS) and opt-in exemplars. Dashboard-as-Code (DAC) Go SDK + `percli` for CI/CD. This is a native Perses datasource, NOT Grafana dashboard JSON.
- Loki and Tempo plugins exist in perses/plugins monorepo; verify actual shipped plugin versions and support in v0.55.1 before claiming coverage.
- Provisioning: GitOps via project/dashboard/datasource specs (CUE + Go SDK + percli). Upgrade/security contract: pin a concrete version image + digest; SBOM (syft/goreleaser) published per release.

Sources:
- https://perses.dev/download/ (v0.55.1)
- https://github.com/perses/perses/blob/main/CHANGELOG.md (v0.55.0 security, v0.54.0 plugins)
- https://perses.dev/docs/plugins/prometheus/ (PrometheusDatasource + proxy + exemplars)
- https://github.com/perses/perses/blob/main/docs/installation/in-a-container.md (image tags)
- https://github.com/perses/perses/blob/main/RELEASE.md (signed release, SBOM)
- https://perses.dev/docs/perses/latest/getting-started/ (proxy datasource, DAC)

## Design: the Perses prov seam (declarative, fail-closed)

Decision (adopted from Owner decision 2026-11-14-perses-replaces-grafana-v0428):
Perses is an OPTIONAL provider-owned management/visualization surface. It is NOT an application capability and NOT a required Core bundle. Prometheus/Loki/Tempo remain the backend data owners and their ownership is preserved. Perses is a realization of the existing optional observability management-ui surface, not a new capability.

Contract-compatible representation (no false metrics/logs/traces, no fake Prometheus replacement):

- New optional provider interface on the observability backends: `{ Name: "management-ui", Class: InterfaceObservability, Protocol: "https", Optional: true }` is ALREADY present on Prometheus. Perses is the optional realization behind it. No change to the required capability surface.
- Add a NEW provider identity for the Perses management tool itself, owned by whoever runs it, as an optional management provider — declared, not mandatory. Two bounded options:
  - (A) Perses is a realization of the existing `observability.management_ui` (Prometheus management surface row). This keeps one browser surface. Fail-closed: if Perses image/pin/provisioning is not selected AND present at runtime, the observability management UI reports `unsupported` (never "not configured" faked as configured).
  - (B) Perses declares its own optional provider interface class `InterfaceObservability` (management-ui) so BaseHarbor can route to it via the existing `shared/prometheus`-style management route and the `ApplicationManagementUISurfaces` surface list. Its `ManagementUISurface.AuthenticationClass` maps to exactly one of native-oidc/standards-auth-adapter/native-credential/unsupported per management-access-v1.
- Versioning contract (Provider Contract v1 "Provider identity and versioning"): Perses product version + image digest are REALIZATION METADATA only. They MUST NOT replace the provider implementation version or capability spec version. So Perses version pins live in the realization (management-ui image digest), not in `IntegrationDescriptor.Version`.
- Datasource contract: Perses connects to Prometheus (and only Loki/Tempo where v0.55.1 actually ships+supports those plugins). This is a Perses-internal datasource spec, NOT a new application capability. Never claim Grafana dashboard JSON parity.
- Security contract: pin Perses v0.55.1; authentication is opt-in; when enabled an encryption key is mandatory (per upstream). Never enable notifications/routing by default. Never declare native alerting/routing parity without evidence; the real rule evaluator/notification owner stays Prometheus/Alertmanager (per decision).
- Ownership/auth: scope all access by actual Target/tenant permissions (existing `ResolveProviderPlacement` + `serviceaccess` policy); fail closed on unknown ownership/missing authorization. Secrets (encryption key, OIDC) out of logs/manifests/audit.

Where it is declared (assigned files, no foreign writes, no .github/**):
- `internal/capability/` : a deterministic, versioned, optional Perses management-provider descriptor + reference mapping (optional management-ui realization), consistent with catalog/registry distinction.
- `internal/metrics/management_ui.go` : `ManagementUISurfaceAt`/`VerifyManagementUIAt` — support the Perses realization as the optional observability management surface; fail-closed when Perses is selected but not provisioned.
- `internal/application/management_ui.go` : surface list + TLS/projection + `ApplicationManagementUISurfaces` for the Perses route; one effective auth class.
- `cmd/baha/app_dev_routing.go` : optional canonical route to the Perses surface when selected.
- `docs/spec/` : extend management-access / provider-management-acceptance with a Perses row and a fail-closed "not configured" statement; update provider-contract-v1 realization-metadata note.
- Deterministic tests: negative (Perses selected but image/pin/provisioning missing => unsupported, not configured), ownership/auth (unknown ownership => fail closed), versioning (perses version does not leak into provider implementation version).

NOTE TO COORDINATOR / OWNER: the concrete file list below is the intended implementation set. Whether every listed file must change (vs. a primarily spec + capability-descriptor + tests declaration) is a scope decision — see QUESTION at END. The task says "specify (and where the card requires: declaratively implement)". I will implement the minimal fail-closed + capability-descriptor + tests declaration and extend the two spec rows, which satisfies "never false metrics/logs/traces declaration".

## Hosted run

- Touched CI group: the "PR · Draft Go" group (cli-0..cli-3, packages) in the "CI · Source & Quality" workflow — Go build/vet/unit for the touched packages. No Docker/Podman runtime gate required for a declarative spec/capability/test-only change (no container lifecycle implemented).
- Hosted CI result (draft PR #1575, base develop 0e9ccb582): all touched Go jobs PASS.
  - `gh pr view 1575 --json statusCheckRollup`: PR · Draft Go · cli-0 → SUCCESS, cli-1 → SUCCESS, cli-2 → SUCCESS, cli-3 → SUCCESS, packages → SUCCESS. Other groups SKIPPED (draft PR policy / not touched).
  - Run: https://github.com/mcpdev80/baseharbor/actions (PR #1575).
- Local (self-run): `go build ./...`, `go vet ./...`, `go test ./internal/capability/... ./internal/metrics/... ./internal/application/...` all pass. Pre-existing failing packages (`internal/database`, `internal/controlplaneruntime`, `internal/development`) are DB/timeout integration tests requiring a live test DB; verified failing identically on the clean base tree, unrelated to this change.

## END status

- DONE pending: local tests pass, evidence committed to origin/main, draft PR created, CI pass, END posted.
