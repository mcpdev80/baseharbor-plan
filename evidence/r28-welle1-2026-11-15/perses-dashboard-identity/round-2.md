# round-2.md — 0428-078 Perses identity dashboard (correction round, PR #1606)

- Worker: w078-correction
- Card: `t-20261114-r28-perses-dashboard-identity` (plan.py show — goal/acceptance/write-set maßgeblich)
- Card state at start: `active` (claimed via `plan.py claim --owner w078` in round-1)
- Correction trigger: Luna r1 verdict REQUEST CHANGES on candidate `e38ed06d24a` (PR #1606)
- Candidate branch: `lane-0428-078-perses-identity` (origin head `e38ed06d24a341db3920e79c9dc3a75215bec498`)
- Dependency `t-20261114-r28-perses-dashboard-selection`: **NOT accepted** (`wait`); my write-set stays disjoint from that lane per FÄCHERREGEL.

## PLAN

- Reality check: `git ls-remote origin` (baseharbor + baseharbor-plan), branch provenance from `e38ed06d24a`
- Inspect current source: `internal/metrics/perses_identity_dashboards.go` (candidate), `internal/capability/reference.go` Keycloak signal, `internal/capability/perses_selection.go` (080 lane, untouchable), Perses v0.55 schema (authoritative)
- Correct `perses_identity_dashboards.go`: replace unconfirmed `KeycloakDatasource` with the pinned supported Prometheus datasource for PromQL; add Perses `apiVersion`; replace caller-supplied `bool` proof with authoritative resolved observability-signal verdict; keep unavailable-preserving cells (valkey #1604 precedent)
- Add golden file + tests: pinned Perses schema validation (apiVersion + PrometheusDatasource), query parser, selected-authorized-signal / absent-unverified / unselected / other-Target
- `go vet`, `go test ./internal/metrics/... ./cmd/baha/...`, build binary
- Draft PR #1606 stays draft; commit only on `lane-0428-078-perses-identity` (fast-forward from `e38ed06d24a`), evidence to planning repo main
- Down container stacks, END with head SHA

## Reality witnesses

- baseharbor-plan remote heads (ls-remote origin, this session):
  - `main` = `3f9f51452dc00123d04b880c2357555348401298`
- baseharbor remote heads (ls-remote origin, this session):
  - `lane-0428-078-perses-identity` = `e38ed06d24a341db3920e79c9dc3a75215bec498`
  - `lane-0428-080-r28-perses-selection` = `e6f5e650d048c28004cdc59608e9205c648bb509`
- Base branch head (candidate): `e38ed06d24a` (confirmed via ls-remote). Branch `lane-0428-078-perses-identity` is this ref.

## Luna r1 scope decision (self-applied STOP-KLAUSEL)

Luna r1 (`act-luna-r1.md`) rejected three things in `internal/metrics/perses_identity_dashboards.go`:

- `PersesIdentityDatasourceKeycloak = "KeycloakDatasource"` is declared but the panels issue PromQL and the pinned Perses image (v0.55.1) ships the **Prometheus** PromQL datasource, not a Keycloak datasource plugin. Fix: the identity panels query the verified current Keycloak metric **through the pinned supported Prometheus datasource** (`PrometheusDatasource`), i.e. the same authorized-datasource pattern the database-dashboards precedent uses. Keycloak's openmetrics `/metrics` (Port 9000) is realized via the Prometheus datasource, never via a fabricated `KeycloakDatasource`.
- The generated dashboard has `kind: Dashboard` without `apiVersion`. Fix: emit the pinned native Perses API schema with `apiVersion: perses.dev/v1alpha1` on the dashboard resource.
- `identityDashboardCatalog(keycloakMetricVerified bool)` makes a caller-supplied bool the positive proof. Fix: replace the bool with an **authoritative resolved observability-signal verdict** — the resolved `keycloak-metrics` signal status from `internal/capability/reference.go`. When the resolved signal is `ObservabilitySupported` (native openmetrics `/metrics`, verified by backend-query) the identity dashboard is realized (available); when the signal is absent/unverified the identity dashboard is explicitly **UNAVAILABLE** with a reason naming the missing verified signal — no fabricated panel, no exporter, no silent Grafana-parity claim.

STOP-KLAUSEL applied (mission): where authoritative signal/Target-proof is not resolvable at this layer (coord-befund: only registry-backed infra exists; the enable-path resolver is a parallel owner task), positive availability is NOT asserted beyond the resolved `supported` signal. The catalog stays **unavailable-preserving** exactly like the valkey precedent `t-20261114-r28-perses-dashboard-valkey` (PR #1604, Luna APPROVED content for UNAVAILABLE scope). No new resolver is built (parallel owner decision). `perses_selection.go` (080 lane) is NOT touched (FÄCHERREGEL). No `.github/**` edits. No `ready_for_review`, no merge, no force-push, no subagent (§4.8).

## Verified signal/precedent witnesses

- `internal/capability/reference.go` `KeycloakIntegration` signal `keycloak-metrics`: Kind=Metrics, Status=**ObservabilitySupported**, Mode=**ObservabilityNative**, Protocol=openmetrics, Verification=**ObservabilityVerifyBackend**, Port=9000, Path=`/metrics`. This is the resolved, authoritative current signal.
- `internal/capability/integration_contract.go`: `ObservabilitySupported`, `ObservabilityRequiresAdapter`, `ObservabilityVerifyBackend` constants; the observability signal registry is the only authoritative signal source in this repo (coord-befund: no plugin-support resolver).
- Perses v0.55 authoritative schema (perses.dev): dashboard resource needs `apiVersion: perses.dev/v1alpha1`; the only native PromQL datasource shipped with Perses is `PrometheusDatasource`; the PromQL query type for `TimeSeriesQuery` is `PrometheusTimeSeriesQuery`; panel kinds `GaugeChart`/`TimeSeriesChart`/`StatChart`.
- Valkey precedent (PR #1604, Luna APPROVED): an absent signal is reported as `kind: DashboardUnavailable`, `unavailable: true` with a reason; no fabricated panel. This round mirrors that for the absent/unverified-signal case.

## END

- lane: w078-correction
- status: DONE (correction candidate committed + pushed; PR #1606 stays draft, awaiting owner 080 merge-window + Codex abnahme)
- base head (ls-remote origin, this session): `lane-0428-078-perses-identity` = `e38ed06d24a341db3920e79c9dc3a75215bec498`
- candidate head (local commit): `6e9b1224385e385484cc54dbfa69eab0502bdb20`
- candidate head (ls-remote origin, this session): `lane-0428-078-perses-identity` = `6e9b1224385e385484cc54dbfa69eab0502bdb20`
- PR: #1606 (draft, open), base `lane-0428-080-r28-perses-selection`
- Ancestry: `git merge-base --is-ancestor e38ed06d24a HEAD` => PASS; `git log e38ed06d24a..HEAD` lists only my own commit `6e9b1224`.
- Tests (self-run, this session): `go test ./internal/metrics/... ./internal/capability/...` => PASS; `go build ./...` => OK; `go vet ./internal/metrics/ ./internal/capability/` => clean; gofmt clean.
- CI: dispatched to coordinator for the 0428-078 gate (Owner scope; no workflow_dispatch / rerun by this lane).
- Cleanliness: only /tmp/opencode/perses-identity-r2/ touched; no docker/podman compose started this shift. No foreign state.
