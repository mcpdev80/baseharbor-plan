# CODEX-REVIEW — PR #1606

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-dashboard-identity`  
**Candidate:** `e38ed06d24a341db3920e79c9dc3a75215bec498`  
**Exact-head CI:** run `43794659927`, COMPLETED SUCCESS, exact SHA; `./internal/metrics` passed.  
**Scope:** based on selection head `e6f5e650d048c28004cdc59608e9205c648bb509`; 3 authored files; `git diff --check` clean.

## Verdict: REQUEST CHANGES

`internal/metrics/perses_identity_dashboards.go` declares `KeycloakDatasource`, although its panels issue PromQL and the evidence does not establish that the pinned Perses image includes a Keycloak datasource plugin. The generated dashboard also has `kind: Dashboard` without `apiVersion` and a flattened query shape, rather than the pinned native Perses schema. Finally, `identityDashboardCatalog(keycloakMetricVerified bool)` makes a caller-supplied bool the positive proof; no authoritative manifest/signal/Target authorization wiring exists in this candidate, and the evidence says that wiring is deferred.

## Recipe

- **File/change:** `internal/metrics/perses_identity_dashboards.go`; use the pinned supported Prometheus datasource for PromQL with an authorized Keycloak signal, or report UNAVAILABLE until the Keycloak plugin is confirmed and appropriate. Emit the pinned Perses API schema. Replace the free bool with authoritative resolved signal/authorization input, or keep status unavailable.
- **Tests:** pinned Perses schema validation; query parser checks; tests for selected authorized signal, absent/unverified metric, unselected provider, and other Target. Ensure the integration candidate wires the resolver and CI selects the tests.
- **Stop:** stop positive availability while plugin support or authoritative signal/Target proof is unresolved.

Read-only review; no merge performed.
