# CODEX-REVIEW — PR #1606, correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-dashboard-identity`
**Candidate:** `6e9b1224385e385484cc54dbfa69eab0502bdb20`
**Exact-head CI:** run `43803425963`, `pull_request`, COMPLETED SUCCESS, exact SHA.
**Base:** selection lane; correction evidence is `round-2.md`. Three files changed in this round; `git diff --check` clean.

## Verdict: REQUEST CHANGES

The correction replaces the fabricated `KeycloakDatasource` with Prometheus and changes the bool input to `capability.ObservabilitySupportStatus`, addressing the datasource-plugin and caller-bool concerns. Two contract gaps remain:

1. The status parameter remains caller-supplied and is not tied to a manifest, Target, or resolved signal object. The candidate has no production call site for `PersesIdentityDashboardAvailability`; tests directly pass `ObservabilitySupported` to obtain `available`. The round-2 akte calls this an authoritative resolved manifest witness, but the implementation accepts any enum value from any caller and does not establish that a real Keycloak metric was queried for the current Target. Keep positive availability unavailable until an authoritative resolver/wiring provides that proof.
2. The dashboard combines `apiVersion: perses.dev/v1alpha1` with `kind: Dashboard`. These are two different Perses resource forms: the Perses REST Dashboard is `kind: Dashboard` with `metadata` and `spec` and no `apiVersion`; the Perses Operator CRD uses `apiVersion` with `kind: PersesDashboard` and Kubernetes metadata. The current hybrid is not validated against either pinned integration contract. The golden and tests assert the same locally authored hybrid rather than decoding/validating the actual target schema. Official Perses docs describe these forms separately: [Dashboard REST API](https://perses.dev/docs/perses/latest/api/dashboard/) and [Operator PersesDashboard](https://perses.dev/docs/operator/latest/user-guide/).

## Recipe

- **File/change:** `internal/metrics/perses_identity_dashboards.go`; use the actual integration path's resource shape (REST `Dashboard` without `apiVersion`, or Operator `PersesDashboard` with its CRD envelope). Do not combine the two. Accept positive status only from the authoritative manifest/Target signal resolution path; while that resolver is out of scope/unavailable, return UNAVAILABLE.
- **Tests:** validate generated JSON against the pinned v0.55.1 REST model or the exact operator CRD, whichever is actually used. Add a test proving an arbitrary caller-provided `ObservabilitySupported` cannot establish availability without the resolved Keycloak signal and Target authority. Keep absence/unverified cases unavailable and query the actual supported metric only from an authorized source.
- **Stop:** stop before positive availability if the resolver/wiring or target Perses resource contract is unresolved; do not claim a native schema based only on a self-authored golden.

The selection dependency remains not accepted. This review does not accept it or authorize integration/merge.

Read-only review; no merge performed.
