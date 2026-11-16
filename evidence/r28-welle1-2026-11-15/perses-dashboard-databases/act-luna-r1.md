# CODEX-REVIEW — PR #1597

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-dashboard-databases`  
**Candidate:** `22d72f3e43491975b1ef941d39c40b5944f86c16`  
**Exact-head CI:** run `43794601260`, COMPLETED SUCCESS, exact SHA; `./internal/metrics` passed.  
**Scope:** based on selection head `e6f5e650d048c28004cdc59608e9205c648bb509`; 10 authored files; `git diff --check` clean.

## Verdict: REQUEST CHANGES

`internal/metrics/perses_dashboards.go` emits `kind: Dashboard` without `apiVersion` and flattens query plugin fields instead of using the pinned Perses native `PersesDashboard` schema and `spec.plugin` wrapper. Its round-trip tests decode into the same locally defined shape, so they do not establish compatibility with the pinned Perses server. Also, the database PromQL selector contains a bare trailing `up` inside the label selector (`up{...,up}`), which is invalid PromQL.

## Recipe

- **File/change:** `internal/metrics/perses_dashboards.go`; emit the exact pinned native API version/kind and plugin/query structure. Remove the stray `up` selector token and keep only valid label matchers.
- **Tests:** validate generated JSON against the pinned v0.55.1 schema or server fixture; parse PromQL with a Prometheus parser and assert expected labels; preserve golden assertions. Run affected package tests and exact-head CI.
- **Stop:** stop if the pinned Perses schema/Prometheus parser is unavailable for validation; do not substitute another locally invented schema.

Read-only review; no merge performed.
