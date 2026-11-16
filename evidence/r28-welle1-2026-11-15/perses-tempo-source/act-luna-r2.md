# CODEX-REVIEW — PR #1610

**ROLLE: REVIEW**
**Task:** t-20261114-r28-perses-tempo-source
**Candidate:** 4b222b1dd5b55ca0ff427f54663e235f25e984e1
**Base:** Perses seam 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08; candidate merges the seam into corrected head d8ffac475e28ed82220e48e5216df287adadc6df. git diff --check clean.
**Exact-head CI:** run 43794189336, pull_request, COMPLETED SUCCESS, exact SHA; Draft source/routing, CLI shards 0–3, and packages passed. Native/release jobs were skipped under draft selection.

## Verdict: REQUEST CHANGES

The r1 recipe's fail-closed selection/ownership/error-propagation work is present, and the verifier no longer reports success based on a pin alone. However, PersesTempoDatasourceKind is still "TraceDatasource"; the supported Perses plugin kind is "TempoDatasource". The candidate's tests assert the locally declared constant and golden, so they accept the unsupported kind. Perses v0.55 plugin docs specify TempoDatasource and TempoTraceQuery: https://perses.dev/docs/plugins/tempo/model/. The emitted struct also is not a Perses REST datasource resource (kind: Datasource, metadata, spec.plugin.kind/spec) and is not validated against the pinned plugin schema. The correction leaves the actual trace-query path absent and reachability unverified, despite the task requiring a supported, scoped datasource path and actual query proof.

## Recipe

- **File/change:** internal/metrics/perses_tempo_datasource.go; use the pinned plugin kind TempoDatasource and the exact Perses datasource resource envelope for the configured REST/proxy integration. Do not emit a custom TraceDatasource resource.
- **Tests:** validate JSON against the pinned Perses v0.55.1 datasource/plugin model; test a real TraceQL query through the authorized Tempo service-access path, with missing/denied/unreachable cases failing closed. Until a real query/health path exists, expose only an explicitly unverified/unavailable state and do not claim verified provisioning.
- **Stop:** stop if the Perses plugin/resource path or authorized query contract cannot be confirmed; pin validation alone is not plugin or health evidence.

The task's seam/runtime dependencies remain unaccepted. This review does not accept them or authorize merge.

Read-only review; no merge performed.
