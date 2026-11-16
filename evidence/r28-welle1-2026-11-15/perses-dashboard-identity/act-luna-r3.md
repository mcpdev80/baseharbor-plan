# CODEX-REVIEW — PR #1606 correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-dashboard-identity`
**Candidate:** `4e81c16ddcf7d1cd1bec1cbec663c97df91b198f`
**Base:** Perses selection lane; correction delta is one commit over previously reviewed `6e9b1224385e385484cc54dbfa69eab0502bdb20`.
**Exact-head PR CI:** run [43811486904](https://github.com/mcpdev80/baseharbor/actions/runs/43811486904), `pull_request`, COMPLETED SUCCESS, exact candidate SHA. Draft source/routing, packages and CLI shards succeeded.
**Diff:** three files (identity dashboard resource, tests and golden); `git diff --check` clean. PR is open/draft.

## Verdict: REQUEST CHANGES

The new resource envelope correctly removes `apiVersion` from the REST/DaC `kind: Dashboard` form, addressing the r2 schema finding. The status-witness finding remains: `PersesIdentityDashboardAvailability` still accepts a caller-provided `ObservabilitySupportStatus` and returns available for `ObservabilitySupported`; the new negative test exercises only absent/unsupported statuses. The exact candidate has no production call site for this availability function and does not thread a resolved `keycloak-metrics` signal from `internal/capability/reference.go` into a Target-scoped status result. A caller can still pass the `supported` enum directly, so the test does not establish non-forgeability or current Target authorization. The round-3 evidence itself records the CLI fan-in as a separate owner task, meaning the required production witness is not present in this candidate.

## Recipe / stop

- **Files/change:** bind the availability path to the actual resolved Keycloak signal for the current manifest/Target and its authorization/ownership context. Until that production wiring exists, return unavailable; do not treat an enum parameter as proof.
- **Tests:** retain REST/DaC schema validation. Add a production-path test proving an arbitrary caller-supplied `ObservabilitySupported` cannot make the dashboard available; prove availability only with the resolved `keycloak-metrics` signal and authorized Target, and keep unknown/denied/absent cases unavailable. Route through the exact-head CI check.
- **Stop:** if the owner fan-in/resolver is not yet available, leave positive availability disabled and resolve that dependency before acceptance.

A separate same-SHA `workflow_dispatch` run 43812046815 failed broad runtime integration setup (including missing ORAS and a root-container policy failure). The requested exact-head PR run is green; the dispatch result does not fix or cause the status-witness finding. No merge.
