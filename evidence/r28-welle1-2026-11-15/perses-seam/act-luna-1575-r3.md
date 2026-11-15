# PR #1575 Review — r3 correction candidate

ROLLE: REVIEW

## PLAN

1. Verify the PR, branch, base, exact requested head and Planning evidence.
2. Review `219a0a24d..293e0e05ac0` and re-check the unresolved r1 contract finding against the resulting descriptor model.
3. Verify the exact-head hosted run and the lane's focused test/equivalence evidence.
4. Run Planning validation and publish this SHA-specific verdict. No merge.

## Reviewer identity

- Session: Codeman `1a678edb-8783-4c14-9707-eddde1e8d286` (`codex-rev-pr1575`, mode `codex`)
- Model: GPT-6-Luna
- Time: 2026-11-15 22:26 UTC

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`
- PR: [#1575](https://github.com/mcpdev80/baseharbor/pull/1575), OPEN, DRAFT, base `develop`
- `develop`: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- Reviewed head: `293e0e05ac04716e441a72679704cbfcc38d6e0e`
- `refs/heads/lane-0428-075-perses-seam` and `refs/pull/1575/head` both resolve to the reviewed head.
- PR metadata confirms base `develop`, head `293e0e05ac04716e441a72679704cbfcc38d6e0e`, state OPEN, draft true.
- Requested correction diff `219a0a24d5687552556b094223e5e4bcfa2eebc4..293e0e05ac04716e441a72679704cbfcc38d6e0e`: 5 files, 201 insertions, 102 deletions. `git diff --check` passed.
- The mission's worker akte is present on Planning `main`: `round-3.md`, initial commit `48aa016c`, with terminal CI follow-up commit `4e2d610e`.

## Correction review

- `parseServiceField` moved from `internal/application/manifest_parse.go` into `internal/application/manifest_parse_services.go`. The moved function body is unchanged; imports are in the new file. The lane reports the source-readability audit passing and an external comparison harness returning identical parser outputs on base and candidate for its scanned YAML and Perses grammar cases.
- The descriptor test rewrite is present and retains its declared intent. Its positive validation and reference-catalog exclusion do not, however, resolve the contract issue below.
- Planning `scripts/plan.py check` before publishing this artifact: 536 tasks, 7 epics, 13 releases and 22 decisions; **0 errors, 17 warnings**. The warnings concern existing unrelated dependency-state inconsistencies.
- After a concurrent `main` commit was integrated during the push rebase, the final check failed on that new task's malformed source reference: `tasks/t-20261115-r28-podman-runtime-performance.md` has `sources: ["https://github.com/mcpdev80/baseharbor/issues/376"]`, while `plan.py` expects `repo#issue` and raises `ValueError: not enough values to unpack`. This review did not edit that unrelated task.

## Exact-head verification

- Run [43768376429](https://github.com/mcpdev80/baseharbor/actions/runs/43768376429): workflow `CI · Source & Quality`, event `pull_request`, head `293e0e05ac04716e441a72679704cbfcc38d6e0e`, completed SUCCESS.
- Succeeded jobs: `PR · Draft source and routing`, `PR · Draft Go · packages`, and `PR · Draft Go · cli-0` through `cli-3`.
- The hosted run skipped native/HA, release and other non-draft jobs. The lane akte records the focused Perses, manifest grammar, build, vet, formatting and readability checks; it also records three full application-package failures reproduced on the untouched base. I did not run local product tests.

## Blocking finding — Perses still claims the Metrics capability

Files:

- `internal/capability/perses.go:47-63`
- `internal/capability/perses_test.go:60-108`
- `internal/metrics/perses_contract_test.go:47-79`

The r1 finding was that `PersesManagement` was an invalid `IntegrationDescriptor`. This correction makes it pass validation by assigning `Provider.Kind = "perses"`, `Provider.Capabilities = [Metrics]`, and `Capabilities = [MetricsV1.ID]`. Under the existing descriptor contract, those fields say the Perses provider implements the Metrics capability. Perses is a visualization client that consumes the backend's metrics; it does not implement the Prometheus/Metrics capability. The comments call this a reused “owner,” but `IntegrationDescriptor` has no ownership/reference field that encodes that relationship. Keeping the valid descriptor out of `ReferenceIntegrations()` prevents current built-in catalog registration; it does not make the descriptor's capability claim accurate or safe for other consumers.

This conflicts with the task's explicit requirement not to falsely declare metrics/logs/traces capabilities. The rewritten tests assert that Perses carries the Metrics capability and passes validation, so they currently lock in the false provider claim rather than proving the intended management-surface boundary.

**Change recipe:** do not model Perses as an `IntegrationDescriptor` that claims `Metrics`. Represent it with a distinct management-tool/surface type and an explicit reference to the existing observability capability owner and its optional `management-ui` interface. Keep it outside provider capability registration. If the shared contract needs an owner-reference extension, specify and review that extension before downstream consumers use it; do not use the consumed `MetricsV1` capability as a surrogate implementation claim.

**Test requirement:** assert that the Perses management representation carries no provider capability claim, resolves its owner to the real observability provider descriptor, preserves the `management-ui` interface/scopes, and remains absent from capability provider registration. Keep a regression test proving the owner continues to validate and no Metrics/Logs/Traces capability is attributed to Perses.

**Stop criterion:** Perses is represented as an optional management surface with an explicit owner/interface relationship and no false capability implementation claim; focused contract tests and their existing CI routing pass on the exact new head.

## Verdict

REQUEST_CHANGES for exact candidate `293e0e05ac04716e441a72679704cbfcc38d6e0e` on PR #1575 / task `t-20261114-r28-perses-contract-seam`.

The parser extraction and exact-head checks pass. The capability-ownership finding blocks acceptance. No merge or PR mutation is included.
