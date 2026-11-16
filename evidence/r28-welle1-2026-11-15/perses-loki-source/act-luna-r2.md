# CODEX-REVIEW — PR #1616 correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-loki-source`
**Candidate:** `787fe6ca363e9154c77284c98414cd00b5c5ac00`
**Base:** Perses seam lane; correction delta is one commit over previously reviewed `fdb4f84b47e4c98b1982de16983a994254917ef6`.
**Exact-head PR CI:** run [43813918063](https://github.com/mcpdev80/baseharbor/actions/runs/43813918063), `pull_request`, COMPLETED SUCCESS, exact candidate SHA. Draft source/routing, packages and CLI shards succeeded.
**Diff:** five files; native datasource, provider/runtime snapshot binding and tests; `git diff --check` clean. PR is open/draft.

## Verdict: APPROVE CONTENT

The correction addresses the r1 defects: it produces a native `LokiDatasource` resource, derives the endpoint from the selected/materialized Loki provider, requires a retained authorized source snapshot, binds queries to the service-access-managed TLS client, and fails closed for unselected, absent, foreign-owned, or endpoint-less sources. Reachability remains unverified until a real query succeeds; secrets are not included in the resource. The package tests in the exact-head PR run succeeded, including native-resource, source/ownership negatives, service-access-client binding, and golden coverage.

The local Loki plugin constant is explicitly assigned to the separate Owner seam-pin triage by the mission and round-2 evidence. I do not treat that outstanding `PersesRelease.LokiPluginVersion` field as a candidate defect here. The seam/runtime dependencies remain unaccepted, so this content verdict does not accept them or authorize integration.

## Recipe / stop

- **Candidate change:** no further correction required by this review.
- **Next gate:** retain the real-query/service-access tests and exact-head package CI. Resolve the Loki plugin pin in the seam through its separate Owner/coordinator state before integrating this datasource; satisfy the card dependencies before acceptance.
- **Stop:** do not treat this review as acceptance of the seam/runtime dependencies or permission to merge.

A separate same-SHA `workflow_dispatch` run 43814344423 failed in the broad runtime integration workflow. The requested exact-head PR run is successful; the dispatch result is a separate runtime gate/state for the coordinator to assess. No merge.
