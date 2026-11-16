# CODEX-REVIEW — PR #1603

**ROLLE: REVIEW**  
**Tasks:** `t-20261114-r28-perses-dashboard-messaging`; mission also names `t-20261114-r28-perses-rabbitmq-source`, which is absent from Planning `main`.  
**Candidate:** `fed843492482b26572f093049a28e8bdcd19f777`  
**Exact-head CI:** run `43794628957`, COMPLETED SUCCESS, exact SHA; `./internal/metrics` passed.  
**Scope:** based on selection head `e6f5e650d048c28004cdc59608e9205c648bb509`; 3 authored files; `git diff --check` clean.

## Verdict: REQUEST CHANGES

The RabbitMQ messaging catalog correctly reports unavailable when there is no native observability signal, and its tests reject fabricated/unrelated signals. However, this lane declares generic package-level Perses model types (`PersesDashboard`, `PersesDashboardSpec`, `PersesPanel`, `PersesPanelSpec`, datasource types) already declared by #1597 in the same `internal/metrics` package. The separate branches pass independently, but fan-in will fail compilation with redeclared identifiers. The standalone run therefore does not establish integration compatibility.

The requested RabbitMQ-source task has no task file/ID in Planning `main`; the existing card is only dashboard-messaging. The candidate also does not provide a separate source contract/evidence for that nonexistent card.

## Recipe

- **File/change:** `internal/metrics/perses_messaging_dashboards.go`; rename the model types with a `PersesMessaging` prefix or reuse a shared native model without duplicate declarations.
- **Tests:** compile and run `go test ./internal/metrics` on an integration candidate containing both #1597 and #1603; assert the unavailable result remains fail-closed. Coordinator must map/create the RabbitMQ-source task contract before that separate task can be reviewed.
- **Stop:** stop if integration still reports duplicate declarations, or if the separate source-card contract remains absent; do not infer approval for a missing card from this dashboard review.

Read-only review; no merge performed.
