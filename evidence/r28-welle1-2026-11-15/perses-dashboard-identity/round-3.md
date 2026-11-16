# round-3.md — 0428-078 Perses identity dashboard (Luna r2 correction, PR #1606)

- Worker: w078-correction (lane: perses-identity-r3, session)
- Card: `t-20261114-r28-perses-dashboard-identity` (plan.py show — goal/acceptance/write-set maßgeblich)
- Card state at start: `active` (claimed via `plan.py claim --owner w078` in round-1)
- Correction trigger: Luna r2 verdict REQUEST CHANGES on candidate `6e9b1224385e385484cc54dbfa69eab0502bdb20` (PR #1606)
- Candidate branch: `lane-0428-078-perses-identity`
- Dependency `t-20261114-r28-perses-dashboard-selection`: **NOT accepted** (`wait`); write-set stays disjoint from that lane per FÄCHERREGEL.

## PLAN

- Reality check: `git ls-remote origin` (baseharbor + baseharbor-plan), `plan.py show`, branch provenance from `6e9b1224385`
- Read act-luna-r2 (origin/main) + round-2; inspect `internal/metrics/perses_identity_dashboards.go`, the golden file, the host-lane 077 precedent golden + struct, and the single CLI call-site resolved-signal path
- Form decision: emit ONE Perses form, REST/DaC `kind: Dashboard` + `metadata` + `spec`, NO `apiVersion` (matches host-lane 077 accepted precedent + owner clarification); drop `apiVersion` field + `PersesIdentityDashboardAPIVersion` constant
- Witness-strength: the single prod CLI call-site threads the resolved signal status from `internal/capability/reference.go` (no enum literal in prod path); add a non-forgeability test proving a caller without the resolved Keycloak signal cannot set available
- Golden + schema test pinned to the REST/DaC form (no apiVersion); keep the unavailable-preserving / witness-fehlend case
- `go vet`, `go test ./internal/metrics/... ./cmd/baha/...`, build binary, gofmt clean
- Commit fast-forward only on `lane-0428-078-perses-identity` from `6e9b1224385` (FF only, no amend), push with explicit refspec, evidence to planning repo main
- Down container stacks, END with head SHA

## Reality witnesses

- baseharbor remote heads (ls-remote origin, this session):
  - `lane-0428-078-perses-identity` = `6e9b1224385e385484cc54dbfa69eab0502bdb20`
  - `lane-0428-077-r28-perses-dashboard-hosts` = `abe9bd52da94074240a363369424b6a2abc9f155`
  - `develop` = `26f6ce4f7d40512d041427204dbaf6a93a8a8f5c`
- baseharbor-plan remote heads (ls-remote origin, this session):
  - `main` = `7ca8322ff6c0bfb5f90747fa4685f7012e328490`
- Base branch head (candidate): `6e9b1224385e385484cc54dbfa69eab0502bdb20` (confirmed via ls-remote). Branch `lane-0428-078-perses-identity` is this ref.

## Luna r2 scope decision (worker, grounded + documented)

Luna r2 (`act-luna-r2.md`, origin/main) rejected two things in `internal/metrics/perses_identity_dashboards.go`:

1. **The JSON mixes two Perses resource forms.** The realized resource carries `apiVersion: perses.dev/v1alpha1` AND `kind: Dashboard`. Per the authoritative Perses v0.55.1 contract these are two distinct, mutually exclusive forms:
   - REST/Perses-server Dashboard (`GET/POST /api/v1/projects/<project>/dashboards`, dashboard-as-code Go SDK `sdk/dashboard`): `kind: Dashboard` + `metadata{name, project}` + `spec{display,datasources,panels,layouts,...}`, **no `apiVersion`**.
   - Perses Operator CRD (`perses.dev/v1alpha1`): `apiVersion: perses.dev/v1alpha1` + `kind: PersesDashboard` + Kubernetes `metadata{name, namespace}`.
   The hybrid is neither. BaseHarbor runs Perses as a server (no Perses Kubernetes operator in the product), so the REST/DaC form is the actual integration path.
2. **The availability status is not tied to a resolved manifest/signal witness.** `PersesIdentityDashboardAvailability` accepts a caller-supplied `ObservabilitySupportStatus` and any enum value flips the verdict; tests pass the enum directly, so no caller-provided `ObservabilitySupported` can be rejected without a real resolved Keycloak signal.

### Form witness (owner-requested grep; this line is the form evidence)

BaseHarbor's own accepted host-lane precedent `perses_dashboards_hosts.go` + its golden files emit the pure REST/DaC form — `kind: Dashboard`, `metadata{name, version}`, `spec{...}` — with NO `apiVersion`:

`git show origin/lane-0428-077-r28-perses-dashboard-hosts:internal/metrics/perses_dashboards_hosts.go` struct `PersesHostDashboard{ Kind, Metadata, Spec }` (no APIVersion field); golden `internal/metrics/testdata/perses-dashboard-hosts/prometheus-host-container.json`:

```json
{
  "kind": "Dashboard",
  "metadata": { "name": "prometheus-host-container", "version": 0 },
  "spec": { ... }
}
```

This confirms `kind: Dashboard` + `metadata` + `spec`, no `apiVersion`. The identity fix aligns the realized resource to exactly this envelope: drop `apiVersion` from `PersesIdentityDashboardResource` and remove the `PersesIdentityDashboardAPIVersion` constant (no longer part of the emitted form). The golden file is regenerated to the REST/DaC form and the schema test asserts `kind == Dashboard` and NO `apiVersion`.

### Witness-strength fix (owner-requested, two prongs)

- (a) **Prod call-site threads the resolved status, no enum literal in prod path.** The single prod caller of `PersesIdentityDashboardAvailability` must pass the resolved signal status resolved from `internal/capability/reference.go` Keycloak `keycloak-metrics` signal (`Status: ObservabilitySupported, Mode: ObservabilityNative, Protocol: openmetrics, Verification: ObservabilityVerifyBackend`), never a literal enum or caller bool. The CLI fan-in wiring (single `cmd/baha` status result) is the 080 owner merge-window task; this lane registers the exact fan-in site as a BEFUND (below) so prod is not left with a literal.
- (b) **Non-forgeability test.** `TestIdentityAvailabilityIsAuthoritativeNotCallerBool` (existing) plus a new witness that a caller which does not hold the resolved `keycloak-metrics` signal verdict (e.g. an empty/absent or non-supported resolved status) cannot flip the identity dashboard to available.

### Owner-loop note (selection/witness foundation is a separate thread)

The identity backend's binding into the selection catalog (`perses_selection.go`, 080 lane) and any new manifest/Target resolver are a separate owner thread that is **not accepted and not a prerequisite** for this lane. This candidate is not made dependent on them beyond the fail-closed enum mapping that already exists: where the resolved signal is not `ObservabilitySupported` the dashboard is explicitly UNAVAILABLE (unavailable-preserving, exactly the valkey + host precedent). No new resolver is built (parallel owner decision, FÄCHERREGEL). If Luna sees a dependency here that she did not call, she overrides.

## Verified witnesses

- Perses v0.55.1 REST Dashboard API (authoritative): `kind: Dashboard`, `metadata{name, project}`, `spec{display,datasources,panels,layouts,duration,timezone}`, **no `apiVersion`**; the only native PromQL datasource shipped with the pinned release is `PrometheusDatasource`; native PromQL query type `PrometheusTimeSeriesQuery`.
- Perses v0.55.1 Operator CRD (authoritative): `apiVersion: perses.dev/v1alpha1`, `kind: PersesDashboard`, Kubernetes `metadata{name, namespace}`.
- `internal/capability/reference.go` (origin/develop, `26f6ce4f7d4`) Keycloak `keycloak-metrics` signal: `Status: ObservabilitySupported, Mode: ObservabilityNative, Protocol: openmetrics, Verification: ObservabilityVerifyBackend, Port: 9000, Path: /metrics` — the resolved authoritative signal.
- Host-lane 077 accepted precedent: pure REST/DaC envelope, no `apiVersion` (witness line above).
- `git diff --check` clean.

## END

- lane: perses-identity-r3
- status: DONE (correction candidate committed + pushed; PR #1606 stays draft, awaiting owner 080 merge-window + Codex abnahme)
- base head (ls-remote origin, this session): `lane-0428-078-perses-identity` = `6e9b1224385e385484cc54dbfa69eab0502bdb20`
- candidate head (local commit): `4e81c16ddcf7d1cd1bec1cbec663c97df91b198f`
- candidate head (ls-remote origin, this session): `lane-0428-078-perses-identity` = `4e81c16ddcf7d1cd1bec1cbec663c97df91b198f`
- PR: #1606 (draft, open), base `lane-0428-080-r28-perses-selection`
- Ancestry: `git merge-base --is-ancestor 6e9b1224385e385484cc54dbfa69eab0502bdb20 HEAD` => PASS; `git log 6e9b1224385e385484cc54dbfa69eab0502bdb20..HEAD` lists only my own commit `4e81c16dd`.
- Tests (self-run, this session): `go test ./internal/metrics/...` => ok; `./cmd/baha/... -run "Perses|Identity|Dashboard"` => ok; `go build ./...` => OK; `go vet ./internal/metrics/` => clean; gofmt clean.
- Cleanliness: only /tmp/opencode/perses-identity-r3/ touched; no docker/podman compose started this shift. No foreign state.

## Fan-in BEFUND (single prod CLI call-site, 080 owner merge-window)

`PersesIdentityDashboardAvailability(resolvedKeycloakSignalStatus capability.ObservabilitySupportStatus)` is not yet called from any prod path on `origin/develop` (grep `PersesIdentityDashboardAvailability` on `26f6ce4f7d4` returns nothing in `cmd/baha`). The 080 fan-in must call it and thread the resolved Keycloak signal status from `internal/capability/reference.go` (never a literal enum) onto the CLI status JSON `perses.identity_dashboards` witness. Exact proposal: add to `applicationStatusResult` in `cmd/baha/app_status_result.go` a field

    IdentityDashboards map[string]metricsprovider.PersesIdentityDashboardAvailabilityEntry `json:"identity_dashboards,omitempty"`

and set it in `collectApplicationStatusResult` from `metrics.PersesIdentityDashboardAvailability(<resolved keycloak-metrics signal status from reference.go>)`, where the resolved status is the `keycloak-metrics` signal's `ObservabilitySupportStatus` for the current manifest/Target. This keeps prod free of an enum literal in the availability path (owner point a).

## origin/main ls-remote witness (second-to-last action, §5.3)

`git ls-remote origin main` (baseharbor-plan, this session):

    87e6bf8e16a3cd399f183c3f63887e70567d76ce  refs/heads/main

The round-3 evidence commit `87e6bf8e` is present on origin/main (pushed above); the END candidate is verified and the evidence path is present on origin/main.
