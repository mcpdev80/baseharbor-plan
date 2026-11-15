# 0428-078 — Perses identity dashboard — round-1 evidence

- Owner: w078
- Card: `t-20261114-r28-perses-dashboard-identity` (plan.py show — goal/acceptance/write-set maßgeblich)
- Card state at start: `active` (claimed via `plan.py claim --owner w078`)
- Dependency `t-20261114-r28-perses-dashboard-selection`: **NOT accepted** (`wait`); my write-set stays disjoint from that lane per FÄCHERREGEL.

## PLAN

- Reality check: `git ls-remote origin` (baseharbor + baseharbor-plan), `plan.py show`/`claim`, branch provenance from `a270725bd`
- Inspect current Core source: metrics perses catalog, capability signal registry, Keycloak current metric signal, 0428-076 golden precedent
- Implement identity panels in own file `internal/metrics/perses_identity_dashboards.go` (own catalog, disjoint write-set per FÄCHERREGEL); no edits to `perses_selection.go`
- Add `identity-keycloak` backend + signal-zeugnis to selection catalog as BEFUND (file:line, exact 1–2 line proposal) for coordinator fan-in; do NOT edit
- Golden-file tests per identity panel (real Keycloak fixture + no-data/unavailable), determinism, Perses-native JSON, key-mapping
- Wire identity panels into CLI status JSON witness (own path; register wiring as BEFUND for coordinator fan-in)
- `go vet`, `go test ./internal/metrics/... ./cmd/baha/...`, build binary
- Draft PR (title 0428-078), push lane branch, evidence with ls-remote shas, cleanliness state
- Down container stacks, END with head SHA

## Reality witnesses

- baseharbor remote heads (ls-remote origin, this session):
  - `develop` = `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
  - `main` = `aff1532c2f6c6782a8c13afad83245d1351815e7`
  - `lane-0428-080-r28-perses-selection` = `a270725bdd795a5c944caf96fd1161ec44688a55`
- baseharbor-plan remote heads (ls-remote origin, this session):
  - `main` = `338a262a1d9d57bd8f947671c929ec4087e2945d`
- Base branch head: `a270725bd` (confirmed via ls-remote). Branch `lane-0428-078-perses-identity` cut from it. Ancestry: `git merge-base --is-ancestor a270725bd HEAD` → true.
- Attestation of base SHA before branch cut: `a270725bdd795a5c944caf96fd1161ec44688a55` (from `develop`/`origin/lane-0428-080-r28-perses-selection`).

## Scope decision (coordinator, 2026-11-16)

FAÄCHERREGEL forbids edits to `perses_selection.go` (owned by the unaccepted 080 lane, active merge-window). Identity panels go in an OWN file with an OWN catalog; the enable-path binding to the selection catalog is left for coordinator fan-in. If a functionally unavoidable change to `perses_selection.go` (not just a catalog line, e.g. a `DashboardBackend` type addition) is required for tests, do NOT edit — file as BEFUND with file:line and an exact 1–2 line proposal. Positive tests remain mandatory: identity panels only on verified Keycloak metrics (signal-zeugnis), else explicit UNAVAILABLE.

## Verified starting points

- `internal/metrics/prometheus_files.go`: Go-struct-first realization marshalled to deterministic JSON (golden pattern).
- `internal/capability/perses_selection.go`: selection catalog, 3 backend templates (`prometheus-targets`, `loki-logs`, `tempo-traces`), NO identity backend. `DashboardBackend` type + `DefaultDashboardCatalog()` + `EligibleFor`/`FilterEligibleDashboards`.
- `internal/capability/perses.go`: seam pin `PersesDefaultRelease` = v0.55.1, `ValidatePersesRelease` fail-closed.
- `internal/capability/integration_contract.go`: `ObservabilitySupportStatus` values; `Collectable() == Status==ObservabilitySupported`; `ObservabilityVerifyBackend` = backend-query.
- `internal/capability/reference.go`:160 — `KeycloakIntegration.Observability.Signals` carries `keycloak-metrics` (Kind=Metrics, Status=Supported, Mode=Native, Protocol=openmetrics, Verification=VerifyBackend, Port=9000, Path=/metrics). This is the **verified current** Keycloak metric signal (NOT the obsolete SPI).
- Precedent `2e5f87037 feat(0428-076)` (other lane): `perses_dashboards.go` + `perses_dashboards_helpers.go` + `testdata/perses-dashboards/*.json` golden files + golden tests + CLI `database_dashboards` witness. Mirrored structurally for identity.

## END

- lane: w078
- status: DONE
- base head (ls-remote origin, this session): `lane-0428-080-r28-perses-selection` = `a270725bdd795a5c944caf96fd1161ec44688a55`
- candidate head (local commit): `1c124c47dc06073f1cee38944a697829caee4369`
- candidate head (ls-remote origin, this session): `lane-0428-078-perses-identity` = `1c124c47dc06073f1cee38944a697829caee4369`
- PR: #1606 (draft, open), base `lane-0428-080-r28-perses-selection`
- Ancestry: `git merge-base --is-ancestor a270725bd HEAD` → true; `git log a270725bd..HEAD` lists only my own commit.
- CI: dispatched to coordinator for the 0428-078 gate (Owner scope; no workflow_dispatch / rerun by this lane).
- Cleanliness: only /tmp/opencode/w078/ touched; no docker/podman compose started this shift. No foreign state.

## Fan-in BEFUND 1: selection catalog identity backend (perses_selection.go — 080 lane)

My identity panels are realized but the selection catalog
(`internal/capability/perses_selection.go`) has no `identity-keycloak`
`DashboardTemplate`, so `DefaultDashboardCatalog().HasTemplate("identity-keycloak")`
is false and `EligibleFor("identity-keycloak", ...)` returns an error ("no
Perses-native dashboard template"). The enable-path binding to the selection
catalog is the coordinator fan-in (080 merge window). Exact 1–2 line proposal:

file `internal/capability/perses_selection.go`, inside `DefaultDashboardCatalog()`
`templates` map (after the `tempo-traces` entry, ~line 121), add:

    "identity-keycloak": {
        Key:               "identity-keycloak",
        Backend:           DashboardBackendKeycloak,
        Datasource:        "keycloak",
        SupportedVersions: []string{AcceptedPersesVersion},
    },

and add the `DashboardBackendKeycloak DashboardBackend = "keycloak"` constant to
the `DashboardBackend` type in the same file. The metrics package
(`internal/metrics/perses_identity_dashboards.go`) already owns the realized
identity panels and the `identity-keycloak` catalog key; the selection catalog
only needs the template + backend constant to make it discoverable. The signal
zeugnis is `internal/capability/reference.go`: Keycloak integration descriptor
signal `keycloak-metrics` (Kind=metrics, Status=supported, Mode=native,
Verification=backend-query, Port=9000, Path=/metrics) — the current signal, not
the obsolete SPI.

## Fan-in BEFUND 2: CLI status JSON identity witness (cmd/baha/app_status_result.go)

`applicationStatusResult` (`cmd/baha/app_status_result.go:26`) exposes
`Perses *capability.PersesStatus` at line 38. Add an identity-dashboard
availability witness alongside it:

    IdentityDashboards map[string]metricsprovider.PersesIdentityDashboardAvailabilityEntry `json:"identity_dashboards,omitempty"`

and set it in `collectApplicationStatusResult` (~line 249) from
`metrics.PersesIdentityDashboardAvailability(keycloakMetricVerified)`, where
`keycloakMetricVerified` is the manifest's verified-current Keycloak signal
witness (true when the Keycloak integration descriptor's `keycloak-metrics`
signal is present and collectable). `metrics` is already imported in that
package (used for the database-dashboards witness of the sibling lane). This
keeps the identity witness on the same public JSON axis as `perses`.

Both BEFUNDs are Owner/scope edits under `.github/**`? No — neither touches
`.github/**`. Both are product/contract edits that the Owner coordinates at the
080 merge window; this lane delivered the disjoint implementation + golden
evidence only.
