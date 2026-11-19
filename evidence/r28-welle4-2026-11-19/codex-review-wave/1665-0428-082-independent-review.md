# Independent read-only review — PR #1665 / 0428-082

Reviewed 2026-11-19.

- Head `e580d32414565442376f23ace9a4a2dd7ed03838`; open draft, mergeable=false, base `w083-perses-datasources` at `ed55d893374b593a7a6032f0de496ca9920ad08d`.
- No exact-head workflow runs or commit statuses found. Diff spans 33 commits, 39 files, +19,087/-104 and includes `internal/metrics/perses_prometheus_datasource.go`, shared with current #1684. Reconcile stack after #1684 before review/merge.
- No edits/comments/claim/merge by this review.

## Findings

1. `internal/metrics/perses_infra_dashboards.go:457-491` labels panels CPU/memory/disk/network but uses `up`, `scrape_samples_post_metric_relabeling`, `scrape_samples_scraped`, and `scrape_duration_seconds`. These are target/scrape statistics, not host CPU/memory/disk/network; the file acknowledges no node_exporter signals. Rename/re-scope panels to scrape telemetry or add verified signal prerequisites. Current tests check families/labels but not semantic axis mapping.
2. `buildInfraWithProbe` drops the request context and uses `context.Background()` for four serial queries (`:645`), so probes can outlive caller cancellation/timeouts. Propagate context and add cancellation coverage.
