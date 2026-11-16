# CODEX-REVIEW — Luna batch17

Date: 2026-11-16. Role: CODEX-REVIEW (Luna). No merge, no candidate mutation.

## Scope and candidate witnesses

| Object | Candidate | Exact pull_request run | Remote state |
| --- | --- | --- | --- |
| 1 / #1663 / 0428-093 | `55550400c1e41769d646fb73864b66d91606bf70` | `43950312560` SUCCESS | OPEN, DRAFT, base `develop` |
| 2 / #1666 / 0428-094 | `5b0197a9c23e796b5dfad14333faa92aa3553f87` | `43952223844` SUCCESS | OPEN, DRAFT, base `develop` |
| 3 / #1665 / 0428-082 | `3a45995396ddbff9bd3cc9ccb59e77384b1145ef` | `43951946780` SUCCESS | OPEN, DRAFT, base `develop` |
| 4 / 0428-074 design | `design-1.md` (read-only artifact) | not applicable | Planning evidence only |

The three code candidates and their listed run IDs were checked at exact head. Each run completed successfully. They are draft-qualified runs: six draft jobs passed and 25 non-draft jobs were skipped. No claim is made that skipped release or qualification gates passed.

## Verdicts

### Object 1 — #1663: APPROVE CONTENT

The 15 non-test English contract/output sites are covered: 12 output strings and three canonical setters now emit `Warning`. Both affected JSON schemas change their `const` from `Achtung` to `Warning`; `contracts/README.md`, tests, and golden data follow the contract. No `docs/de/**` path is in the PR. The separate demo consumer belongs to 0428-098 and is outside this review.

CI capture is present. The specifically named Release Source Preflight job was skipped in this draft run, so it is not evidence for that job. The changed Go package is `cmd/baha`; the exact run's four Draft Go CLI shards passed. The shard runner discovers and selects named tests from `./cmd/baha` and executes them with `go test -count=1 -json`; therefore `TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker` is included by the existing CLI shard path. No workflow change is needed. Verdict covers content and test capture, not skipped non-draft gates.

### Object 2 — #1666: REQUEST CHANGES

The malformed YAML case now fails loudly with `ErrConfigMissing`, the valid-config regression is present, and the exact run's draft Go jobs passed. However, `LoadConfig` explicitly accepts an existing empty/whitespace-only `config.yaml` as an implicit default (`internal/deployment/target.go`, around the empty-file branch); the new `TestLoadConfigEmptyFileSucceeds` codifies this. An existing empty file is a malformed configuration, not an absent configuration. The historical reproduction also identifies the XDG double-append case where the intended sibling `config.yaml` is missed; the new test checks the helper predicate but does not exercise `LoadConfig` end-to-end with that XDG setup.

**Recipe:** keep the clean default only when the config file is absent and the resolved root is genuinely empty. Return an actionable error (using `ErrConfigMissing` or a dedicated parse error) for an existing empty/whitespace-only file. Add a `LoadConfig` regression that sets `XDG_CONFIG_HOME` to the reproduced root, places `config.yaml` at the sibling location, and asserts fail-loud behavior. Retain the valid-config and truly-empty-root cases. Run the targeted deployment tests and obtain a new exact-head CI run after the correction.

### Object 3 — #1665: REQUEST CHANGES

The handoff evidence supports excluding the lost dirty alert files and `.gitignore` work; neither is in this candidate. The 0428-080 selection test blob and datasource implementation match their stated predecessor heads, so the selection tests were not altered by the dashboard implementation. The candidate does not, however, establish a production-valid dashboard or verified panel signals:

1. `internal/metrics/perses_infra_dashboards.go` builds a custom JSON object (`kind: "dashboard"`, top-level `id`/`title`/`panels`) and tests its own serialization. It is not validated against the native/versioned Perses dashboard resource schema required by task 0428-082, whose repository-native resource shape uses `kind: "Dashboard"`, `metadata`, and `spec`.
2. `MissingSignal` is derived from the datasource `up{...}` reachability probe, not from the metrics consumed by the dashboard panels. Tests fake only that generic `up` result; they do not show panel data present or absent. This does not prove explicit no-data behavior for the queried signals.
3. The CPU query uses `cpu_seconds_total{job="prometheus"}`. The standard node_exporter CPU series is `node_cpu_seconds_total`; the candidate does not provide evidence that its unprefixed series exists. The other node-exporter queries also lack an in-repository scrape/provisioning witness. See [Prometheus node_exporter guide](https://github.com/prometheus/docs/blob/main/docs/guides/node-exporter.md).
4. The PR base is `develop`, while its prerequisite selection and datasource PRs remain open/draft, and the diff consequently aggregates their changes with 0428-082. The task declares those dependencies and the coordinator rules require stacked PRs to target the basis branch until it lands. The candidate is not a standalone 0428-082 diff against the approved base.

**Recipe:** retarget/stack the PR on the declared dependency branch in the prescribed order, preserving the one-card diff. Use the pinned native Perses resource model and validate the dashboard against its versioned schema. Base panels only on metrics that BaseHarbor actually provisions or verifies; correct the CPU series name and provide a scrape/source witness for all panels. Make missing-signal state reflect panel query results through schema-supported no-data behavior, and test both present and absent panel data. Re-run 0428-080 tests unchanged and obtain exact-head CI for the corrected candidate.

### Object 4 — 0428-074 design artifact: APPROVE CONTENT

`design-1.md` inventories the current alerts and secure-access contracts, distinguishes notification recipients from operator access, compares options with scope/cost/risk, and recommends the narrow fail-closed extension. It explicitly leaves the queue-124 positive-path contract, recipient shape, and evaluator choice to the owner. It does not invent a receiver, secret, runtime, or successful positive path. The design is complete for the requested decision; no hidden contract choice is taken. A small naming mismatch between the sketch's exported `AlertNotificationRoute` field type and its private `alertNotificationRoute` example can be harmonized when implementation begins, but does not change this design verdict.

## CI and review limits

All three PRs remain DRAFT. Their exact-head draft jobs are successful; skipped non-draft jobs are not treated as successful evidence. No PR was approved on GitHub, changed, marked ready, or merged. No product files were modified.

## END

END_DONE mission-luna-batch17 — object verdicts recorded: #1663 APPROVE CONTENT; #1666 REQUEST CHANGES; #1665 REQUEST CHANGES; 0428-074 APPROVE CONTENT. Review evidence only; no merge. See this file for exact-head witnesses and actionable correction recipes.
