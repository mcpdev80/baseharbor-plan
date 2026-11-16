# CODEX-REVIEW — PR #1616

**ROLLE: REVIEW**
**Task:** t-20261114-r28-perses-loki-source
**Candidate:** fdb4f84b47e4c98b1982de16983a994254917ef6
**Base:** Perses seam 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08; head merges the seam into 7bf8f407afebc1cf605376cd53e79201a69b8fe3. Two authored files; git diff --check clean.
**Exact-head CI:** run 43794261907, pull_request, COMPLETED SUCCESS, exact SHA; Draft source/routing, CLI shards 0–3, and packages passed. Native/release jobs were skipped under draft selection.

## Verdict: REQUEST CHANGES

internal/logs/loki_datasource.go does not build or return a Perses datasource resource; LokiDatasourceNow returns only an internal status/target descriptor. It accepts caller-supplied selected and owner fields and does not bind them to a manifest-resolved Loki source; ValidateLokiDatasourceSource is separate and is not used by the builder. QueryLoki accepts an arbitrary HTTP client and endpoint, so the claimed service-access TLS/authorization boundary is not enforced by this API. The plugin version is a mutable local variable (LokiPluginVersion = v0.6.0) because the seam pin is missing; the lane evidence itself records the missing seam pin as an Owner finding. The tests cannot prove a supported, pinned Perses resource or authorized source selection. Perses plugin docs define a Datasource resource whose spec.plugin.kind is LokiDatasource: https://perses.dev/docs/plugins/loki/model/.

## Recipe

- **Files/change:** internal/logs/loki_datasource.go; bind selected state, ownership, source, Target, endpoint, and service-access policy into one resolved input; do not accept unrelated caller-provided bool/client/endpoint as authority. Construct the native Perses datasource (kind: Datasource with spec.plugin.kind: LokiDatasource and the pinned proxy config) or keep the feature unavailable. Move the Loki plugin pin into the seam-owned PersesRelease contract through the coordinator/Owner, then consume that pin here.
- **Tests:** validate the resource against the pinned plugin schema; cover unselected/absent/not-ready/denied/foreign-Target cases and an actual authorized Loki query through the service-access TLS client. Ensure secrets never appear in results/errors. Obtain a new exact-head CI run after the correction and seam pin.
- **Stop:** stop if the seam pin or authoritative owner/Target resolver is unresolved; do not claim a configured datasource from a local plugin string or status descriptor.

The task's seam/runtime dependencies remain unaccepted. This review does not accept them or authorize merge.

Read-only review; no merge performed.
