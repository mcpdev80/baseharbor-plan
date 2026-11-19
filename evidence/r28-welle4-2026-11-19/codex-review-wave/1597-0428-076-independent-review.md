# Independent read-only review — PR #1597 / 0428-076

Reviewed 2026-11-19.

- Head `540ed13cec363a231241a17baa68c8d32ebdae63`; open draft, DIRTY, base `4094448543359a13ba312119304f1f70d3bc40a9` (stale vs current develop).
- Diff spans 23 commits/31 files and includes 0428-080 selection/parser/CLI paths outside this task.
- Draft feedback run `43810693985` passed only Draft Go/source; regular PR Selected Checks and runtime/validation gates were skipped. Exact workflow-dispatch run `43810688499` failed `validate` because `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI` requires ORAS before Core setup. No merge-ready exact-head evidence.
- No edits/comments/claim/merge by this review.

## Findings

1. Tempo query `internal/metrics/perses_dashboards.go:244` filters `service.name="baseharbor-applications"`, while `internal/telemetry/otlp_payload.go:38-42` emits application spans with `service.name="baseharbor"`; the query misses app traces.
2. Prometheus panel line 204 interpolates `$application` and `$env`, but `PersesDashboardSpec` has no variables field and its golden has no `spec.variables`.
3. Loki panel line 224 queries `job="baseharbor-applications"`; current labels in `internal/logs/render.go:182-190` are `baseharbor_application`, `baseharbor_environment`, `baseharbor_source_class`, with no `job` label.
4. `persesDashboardCatalogJSON` (`:348-359`) serializes a map without sorting despite claiming deterministic aggregate JSON.

Reconcile the stack, refresh from develop, correct/verify query semantics, and run regular exact-head gates including required runtime acceptance.
