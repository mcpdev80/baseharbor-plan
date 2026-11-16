# PR #1610 Review — Perses Tempo datasource

ROLLE: REVIEW

## PLAN

1. Confirm PR #1610 base/head, exact diff, branch provenance, and lane evidence.
2. Compare implementation and tests with task `t-20261114-r28-perses-tempo-source` acceptance criteria.
3. Verify exact-head CI run `43780642360`.
4. Record a SHA-specific verdict and actionable correction recipe. No merge or frost.

## Candidate and witnesses

- Repository: `mcpdev80/baseharbor`; PR [#1610](https://github.com/mcpdev80/baseharbor/pull/1610), OPEN, DRAFT.
- PR base: `lane-0428-075-perses-seam` at `492b8e8f994b16e6f73819a08175f8178cd63292` (the approved PR #1575 head).
- Reviewed head: `c27e7a789a1b6eaf52afabcb545e1a9e351b057a`.
- Remote PR head and `refs/pull/1610/head` resolve to the reviewed head. The `origin/lane-0428-075-perses-seam..HEAD` history contains exactly one commit: `c27e7a789 perses-tempo-source (0428-091): add Perses Tempo datasource`.
- Exact diff `492b8e8f994b16e6f73819a08175f8178cd63292..c27e7a789a1b6eaf52afabcb545e1a9e351b057a`: 3 new files, 406 insertions; `git diff --check` passes.
- Lane evidence: `evidence/r28-welle2-2026-11-16/perses-tempo-source/round-1.md`, present by Planning commit `2be5da2e` (ancestor of Planning `main`). Its provenance records the initial empty-PR false delivery and the corrected single-commit branch. The evidence has stale/inconsistent candidate and CI statements in later sections; this review relies on direct remote and API witnesses above instead.

## Findings — changes required

### 1. Health verification passes without a health check

`internal/metrics/perses_tempo_datasource.go:176-189` says pin validation alone MUST NOT pass and that a missing/unreachable Tempo path returns an error, but `VerifyPersesTempoDatasourceHealth` returns `nil` once the release pin validates. There is no request, provider endpoint check, or reachability evidence. This reports success for an unverified datasource and violates the task's “scoped and verified” acceptance.

**Recipe:** make the verifier fail closed when no real Tempo health/query path is available, or implement the approved probe and return success only after it succeeds under the selected authorization context. Add tests that prove missing endpoint, denied access, and unreachable endpoint fail, and that a successful probe is required for success. Stop if the approved authorization and probe contract cannot be identified; do not treat a valid Perses release pin as health evidence.

### 2. Builder does not enforce selection, authorization, or source presence

`BuildPersesTempoDatasource` and `persesTempoDatasourceFromRelease` validate only the Perses release. They do not check that the manifest selected Perses or that Tempo is selected and authorized. At lines 136-139, provider endpoint errors are discarded; the function then returns a default datasource with an empty config and `nil` error. Thus an unselected/unauthorized or absent Tempo path can still produce a datasource, contrary to the documented fail-closed behavior. The tests construct only a selected manifest and the absent-source test treats this success as correct.

**Recipe:** use the existing manifest selection, Tempo ownership, TLS and tenant/Target authorization contracts before building. Propagate missing/denied/unknown-owner errors and do not emit a default datasource without an authorized materialized source. Add negative tests for Perses unselected, Tempo absent, denied/unknown owner, and missing provider endpoint; assert no datasource is produced in each case. Stop on unknown ownership or authorization rather than inferring it from `ProviderTempo` as a string.

### 3. Native plugin and actual trace-query behavior are not verified

The committed golden file is generated from this implementation's own struct and contains only `kind`, `name`, `default`, and an empty `config`; it is not evidence that the pinned Perses image accepts this native `TraceDatasource` configuration or that a trace query reaches the existing Tempo provider. The task requires a verified supported plugin/format and an actual trace query, plus unsupported, denied, and absent-source behavior. Current tests assert constants and a self-produced JSON file; `TestPersesTempoDatasourceNegativeWrongKind` only compares two literals and does not exercise a rejection path.

**Recipe:** validate the exact emitted resource against the pinned Perses plugin/schema and exercise a real trace query through the authorized Tempo endpoint. Add non-vacuous unsupported-plugin, denied-access and absent-source tests with observable failure results. Route the tests through the actual CI job and record the exact executed job/trigger. Stop if the pinned image/plugin or authorized query path cannot be verified; explicitly report unsupported coverage rather than claiming provisioned/verified support.

## Exact-head CI

- Run [43780642360](https://github.com/mcpdev80/baseharbor/actions/runs/43780642360): `CI · Source & Quality`, `pull_request`, head `c27e7a789a1b6eaf52afabcb545e1a9e351b057a`, completed SUCCESS.
- Successful jobs: `PR · Draft source and routing`, `PR · Draft Go · packages`, and `PR · Draft Go · cli-0` through `cli-3`.
- `PR Selected Checks`, native/runtime, and release jobs were skipped for this draft run. The successful run is recorded as requested, but skipped jobs provide no test evidence for the missing acceptance behaviors.
- I did not run local product tests or modify product files.

## Planning validation

- `python3 scripts/plan.py check`: 538 tasks, 7 epics, 13 releases, 22 decisions; 0 errors, 22 warnings (exit success).

## repo-rule compliance

- Review is read-only against the product repository. No PR state, product branch, CI run, or release state was changed.
- No merge or frost action was performed.

## Verdict

REQUEST_CHANGES for candidate `c27e7a789a1b6eaf52afabcb545e1a9e351b057a` / PR #1610 / task `t-20261114-r28-perses-tempo-source`.

The exact-head CI run is green, but the current implementation returns success without health verification, builds a default datasource without enforcing selection/authorization/source availability, and does not verify the pinned native plugin with an actual authorized trace query. Re-review the corrected exact head against these recipes and task acceptance criteria. No merge is authorized by this review akte.
