# CODEX-REVIEW — PR #1610 correction follow-up

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-tempo-source`  
**Candidate:** `7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4`  
**Base:** `lane-0428-075-perses-seam` @ `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`  
**Exact-head CI:** run `43820902132`, event `pull_request`, created `2026-11-16T07:01:56Z`, COMPLETED SUCCESS, exact head. Full base-to-head diff is three lane commits; correction delta `4b222b1d..7a2736ba` includes the native datasource/query adapter, validation, tests, fixtures and service-issuer test support. `git diff --check` clean.

## Verdict: REQUEST CHANGES

The implementation now emits the native plugin kinds and exercises a real TraceQL HTTP query through the service-access client, but its datasource resource envelope is not tied to the pinned Perses v0.55.1 model. The candidate sets `PersesTempoAPIVersion = "perses.dev/v1"` (`internal/metrics/perses_tempo_datasource.go:69–72`) and serializes that as `apiVersion`. Its embedded `perses-pin.json` repeats the same value, so `ValidatePersesTempoResource` only checks the resource against a self-authored witness; it does not validate against the pinned upstream model. The Perses v0.55.1 Go `v1.Datasource` model contains `kind`, `metadata`, and `spec`, with no `apiVersion` field ([pinned source](https://github.com/perses/perses/blob/v0.55.1/pkg/model/api/v1/datasource.go)); Perses' documented Tempo resource example uses `apiVersion: v1`, not `perses.dev/v1` ([Tempo model](https://perses.dev/docs/plugins/tempo/model/)). This makes the new “upstream contract witness” circular and leaves the emitted envelope unverified against the supported native format. The code also defines `ValidatePersesTempoTraceQuery`, but the production builder validates the datasource resource only and does not invoke the query validator before returning the query object.

## Recipe / stop

- **Files/change:** update `PersesTempoAPIVersion`, `PersesTempoPinSource`/`perses-pin.json`, and `ValidatePersesTempoResource` in `internal/metrics/perses_tempo_datasource.go` and the fixture so they match the actual Perses v0.55.1 REST/config model. For the REST `Datasource` object, use the model's supported shape (no `apiVersion` field); if emitting a YAML resource document, use the exact documented version value and format. Pin the upstream schema/model to an immutable v0.55.1 source witness rather than repeating local constants.
- **Required tests:** validate the serialized datasource and trace-query objects against the actual pinned model/schema (including proxy shape, project metadata, selector and query wrapper); assert the emitted resource has no unsupported group/version. Invoke both datasource and trace-query validation from the production builder. Retain malformed-resource, direct-URL, absent/denied source, real query, empty-answer, and unreachable-path cases.
- **Checks:** after correction, rerun focused `internal/metrics` tests/build and obtain exact-head `pull_request` SUCCESS on the corrected SHA.
- **Stop:** if the v0.55.1 REST/config route cannot consume the datasource object in the proposed form, stop and settle the correct Perses API/config contract before claiming native provisioning.

The round-3 runtime identity note remains a dependency/boundary finding: health verification correctly errors when the authorized service-access query cannot complete; do not report it verified or healthy without an observed real answer. The task's seam, runtime, and signal-inventory dependencies remain separate gates. No dependency is accepted or merge authorized by this review.

Read-only SHA-exact review; no product files changed; no merge.
