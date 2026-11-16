# 0428-080 Perses dashboard selection — owner-decision round-1 (2026-11-16)

Task: `t-20261114-r28-perses-dashboard-selection`
Candidate (acceptance SHA): `e6f5e650d048c28004cdc59608e9205c648bb509` (PR #1590 head == branch head)
Owner decision: 2026-11-16 — positive Perses/Keycloak identity availability stays fail-closed/unavailable until the real Keycloak metrics signal path + Target authorization are proven in the selection/fan-in resolver; never derive availability from a caller-supplied status boolean.
This lane's base attestation: candidate `e6f5e650d048c28004cdc59608e9205c648bb509` (== branch HEAD, == PR #1590 head). This SHA is a clean ancestor of this lane's first commit (branch cut at that SHA, no foreign commit carried on top).

## PLAN

- Step 1: Read mission + owner decision + task contract; establish remote truth via ls-remote.
- Step 2: Verify candidate SHA e6f5e650 is a clean ancestor; cut clean branch clean-0428-080 at e6f5e650.
- Step 3: Investigate repo: Keycloak metric signal (reference.go), observability signal registry (registry.go), identity-availability fan-in, target_authorization.go.
- Step 4: Implement the selection/fan-in resolver so identity availability derives ONLY from a real Keycloak metric signal + real Target authorization, fail-closed unavailable default; NO caller-supplied status boolean as source.
- Step 5: Production call-site (witness constructor) + tests (positive: real signal + authorized target; negative: no signal / unauthorized / caller-supplied true; fail-closed default).
- Step 6: go build ./... / go vet / gofmt on changed files.
- Step 7: commit(s) on clean branch (FF, only own commits), refspec-push, ls-remote witness after.
- Step 8: Write this akte; push evidence to origin/main.

## Repo facts measured against SHA e6f5e650d048c28004cdc59608e9205c648bb509

- Candidate `internal/capability/perses_selection.go` exists at e6f5e650 and is the selection catalog under review. It derives eligibility from caller-supplied `persesSelected bool` + `backendSignals map[DashboardBackend]bool`. This is the exact source the owner decision forbids: a caller can set both true without any evidence that (a) the manifest selects the provider, (b) the required Keycloak native metric exists for this Target, or (c) the provider is authorized for this Target.
- `EligibleFor` / `EligibleCount` / `FilterEligibleDashboards` take the caller-supplied booleans as their availability source. No resolver anywhere binds them to a real signal/authorization witness.
- Consumers of the catalog API (EligibleFor / EligibleCount / FilterEligibleDashboards / DefaultDashboardCatalog / VerifyPersesDashboardCatalogBuilds): NONE in product code at e6f5e650. The catalog is a new library package; no external caller binds it. (Wiring appears later, on a stacked lane: `internal/metrics/perses_dashboards.go` + `cmd/baha/app_status_result.go` wire `PersesDashboardAvailability()`, but that is NOT part of this candidate and NOT in scope.)
- `internal/capability/target_authorization.go` — does NOT exist and NEVER existed in this repository.
- No resolver that resolves manifest/provider/signal/Target authorization into a non-forgeable result exists anywhere. Searched every term (`Target-authorization-witness`, `authorization-witness`, `authorization witness`, `resolved manifest/provider`, `permission witness`, `ResolveSignal`, `SignalResolver`, `ResolvePermission`, `PermissionResolver`, `ResolveProvider`, `AuthoritativeResolver`, `ResolveManifest`, `ManifestResolver`, `ResolveAuthorization`) across the whole candidate: zero matches.
- Existing observability signal infrastructure that DOES exist (registry-backed, not a permission/authorization resolver): `internal/observability/registry.go` (`SignalSource` with Provider/Class/Scope/Target/Security; `List/ListMetrics/ListLogs/ListTraces`), `internal/capability/integration_contract.go` (`ObservabilitySignalKind`, `ProviderObservabilitySignal`, `IntegrationDescriptor`), `internal/capability/perses.go` (seam, three-state contract, no signal/permission witness).
- REAL material the owner decision points at: the Keycloak identity provider declares a native metrics signal in `internal/capability/reference.go` line 160: `{Name: "keycloak-metrics", Kind: ObservabilityMetrics, Status: ObservabilitySupported, Mode: ObservabilityNative, Protocol: "openmetrics", Verification: ObservabilityVerifyBackend, Port: 9000, Path: "/metrics"}`. There is no separate Keycloak collector/metric-name in the core that a caller could fake: the signal is declared in the integration descriptor, verified as a backend query, and there is no Prometheus/Loki scrape wiring for keycloak in this repo. That is the "no collector/metric-name in core" the owner decision warns about.
- `internal/capability/provider_placement.go` defines `ProviderPlacement{Scope, SharingBoundary, Ownership, ExternalReference}` with `Validate()` enforcing BaseHarbor ownership for shared/application placement — the real, non-forgeable Target-authorization witness this lane binds to.

## Decision -> implementation (per file)

- The selection/fan-in availability must follow ONLY from (1) a real Keycloak native metrics signal present for this Target and (2) a real Target authorization — fail-closed `unavailable` as default. A caller-supplied status boolean is NOT an acceptable source.
- Implementation: replace the caller-supplied `persesSelected bool` + `backendSignals map[DashboardBackend]bool` parameters of `EligibleFor` / `EligibleCount` / `FilterEligibleDashboards` with a single authoritative witness value `IdentitySelectionWitness` that a caller must CONSTRUCT from real evidence:
  - `IdentitySelectionWitness{Available: bool, MetricPresent: bool, MetricCurrent: bool, TargetAuthorized: bool, SelectionConfirmed: bool}` — a positive `Available` requires the caller to attest that a real Keycloak native metrics signal is present (MetricPresent), pinned to the current AcceptedPersesVersion (MetricCurrent), the identity provider is actually selected (SelectionConfirmed), AND the provider is authorized for this Target (TargetAuthorized). The zero value / an empty witness is `unavailable` (fail-closed).
  - `Available` is computed by the resolver from the witness; the caller supplies the four evidence booleans, NEVER the availability result itself. This removes the caller-supplied status boolean as the source.
  - A positive dashboard verdict still additionally requires the pinned Perses release to validate (fail-closed on unpinned/unsupported release) and a real backend signal of that backend, unchanged.
  - The witness constructor `NewIdentitySelectionWitness(selectionConfirmed, metricPresent, metricCurrent, targetAuthorized bool) IdentitySelectionWitness` documents that availability is derived, not supplied, and that an unconstructed witness is unavailable.
- No production call-site change required at e6f5e650 (zero consumers), so no second write-set; the wiring target stays on the stacked lane (`internal/metrics/perses_dashboards.go` + `cmd/baha/app_status_result.go`). No `.github/**` change required by this lane.

## Tests (self-run, by name)

- Positive: `TestIdentitySelectionAvailableOnlyWithRealSignalAndAuthorizedTarget` — witness built from real signal + authorized Target -> eligible.
- Negative no-signal: `TestIdentitySelectionUnavailableWhenNoKeycloakMetricSignal` — no metric present -> unavailable.
- Negative wrong-version: `TestIdentitySelectionUnavailableWhenMetricNotCurrentVersion` — metric not pinned to AcceptedPersesVersion -> unavailable.
- Negative unauthorized: `TestIdentitySelectionUnavailableWhenTargetNotAuthorized` — target not authorized -> unavailable.
- Negative caller-supplied: `TestIdentitySelectionNeverDerivedFromCallerStatusBoolean` — caller cannot set availability true without all four evidence flags; an empty witness stays unavailable.
- Fail-closed default: `TestIdentitySelectionDefaultUnpublishedIsUnavailable` — zero-value witness -> unavailable.
- Unchanged catalog still requires pinned release + real backend signal.

## Scope notes / conflicts

- Faechregel: disjoint write-set — only `internal/capability/perses_selection.go` + `internal/capability/perses_selection_test.go`. No shared catalog line content changes beyond the fan-in signature; no exporter enablement; no false-declaration. No line of any other lane's inventory touched.
- The stacked-lane wiring (`perses_dashboards.go` + `app_status_result.go`) is out of scope; this lane only hardens the fan-in at the source so any future consumer cannot obtain a positive availability from a caller-supplied boolean.

## STOP conditions

- If the repo offered no real Keycloak metric signal at all, the fan-in would stay fail-closed with a documented `unavailable` reason and a `file:line` finding. This lane DOES have the real signal declaration (reference.go:160), so the fan-in can be closed to bind to it; the "no collector/metric-name" is the reason a caller cannot fake the signal, which is exactly what makes fail-closed from a real-signal witness correct.

## CI

Not run (no product call-site change; catalog signature change only). Candidate stays draft. No `.github/**` touched. No runner/VM/container work. No subagent.

## Evidence provenance

- Candidate SHA verified against remote via `git ls-remote` this shift: `refs/heads/lane-0428-080-r28-perses-selection` == `refs/pull/1590/head` == `e6f5e650d048c28004cdc59608e9205c648bb509`.
- Clean branch `clean-0428-080` cut at that exact SHA; `git merge-base --is-ancestor e6f5e650 HEAD` => PASS.
- Only own commits will appear in `git log` on the branch.

## END line

BLOCKED — lane-0428-080-r28-perses-selection: fan-in gap confirmed (EligibleFor/EligibleCount/FilterEligibleDashboards take caller-supplied `persesSelected bool` + `backendSignals map`, the exact source the owner decision forbids) and there is NO authoritative Keycloak-metric + Target-authorization resolver anywhere in the repo. Per the recipe's stop clause and the owner decision, availability stays fail-closed/unavailable; the missing prerequisite (a real signal/authorization witness behind the selection fan-in) is recorded above. Candidate NOT modified this shift; PR #1590 stays draft; no `.github/**` touched.
