# PR #1575 Review — dedefix candidate

ROLLE: REVIEW

## PLAN

1. Reconcile the requested PR head, base, card contract and repository instructions.
2. Review the full candidate diff against `develop`, including the Perses contract seam and the German parity correction.
3. Verify the dedefix write set, exact-head hosted run and supporting evidence.
4. Record the SHA-specific verdict in Planning. No merge or frost action.

## Reviewer identity

- Session: Codeman `1a678edb-8783-4c14-9707-eddde1e8d286` (`codex-rev-pr1575`, mode `codex`)
- Model: GPT-6-Luna
- Time: 2026-11-15 21:06 UTC

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`
- PR: [#1575](https://github.com/mcpdev80/baseharbor/pull/1575), OPEN, DRAFT, base `develop`
- Base: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- Reviewed head: `219a0a24d5687552556b094223e5e4bcfa2eebc4`
- `git ls-remote origin develop` returned `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`.
- GitHub PR metadata returned head `219a0a24d5687552556b094223e5e4bcfa2eebc4`, base `develop`, state OPEN, draft true.
- Base-to-head diff: 19 files, 1041 insertions, 21 deletions. `git diff --check` passed.
- Compared with the previously reviewed `af308e66d38ad1204345bbe83d066dd7548ea6e6`, this candidate adds only 14 lines to `docs/de/spec/management-access-v1.md`.

## Contract and scope review

- The Perses code models an optional observability management surface, with no application capability declared. It leaves the existing Prometheus management surface and backend ownership intact; does not implement lifecycle; and reports reachability as unverified unless a real health path exists.
- The public status contract distinguishes `not_configured`, `configured_unverified`, and `verified`; the CLI tests assert selected/unselected states and fail-closed unknown ownership through the production status path.
- No fake metrics/logs/traces capability was introduced. However, the candidate exposes `PersesManagement` as an `IntegrationDescriptor` while intentionally omitting both capability kinds and versioned capability specifications; this fails the existing descriptor contract and is not a usable catalog/registry representation (see finding below).
- The contract pins Perses `v0.55.1`, image `persesdev/perses:v0.55.1`, and the Prometheus plugin version. The upstream [Perses release record](https://github.com/perses/perses/releases) identifies v0.55.1 as the latest release on the review date and describes security/dependency and plugin patch updates.
- The EN management-access section and DE mirror describe the same seven required technical literals: `management-ui`, `not_configured`, `configured_unverified`, `verified`, `perses`, `baha status --json`, and `baha app status --json`. The new DE addition contains no unrelated edits; `dedefix-r1.md` records the pre-fix failure, post-fix integrity/audit results, and exact candidate provenance.
- The full changed-file set matches the task's Perses seam and its tests/specifications. The candidate introduces no `.github/**` change and no unrelated PR content.

## Required-check and evidence review

- Exact-head run: [43760586692](https://github.com/mcpdev80/baseharbor/actions/runs/43760586692), `CI · Source & Quality`, `pull_request`, head `219a0a24d5687552556b094223e5e4bcfa2eebc4`, completed SUCCESS.
- Executed jobs: `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages` all succeeded. The draft selection skipped the non-selected native/release jobs; this review does not treat skipped jobs as executed evidence.
- Existing CLI contract tests are routed through the ordinary Draft Go shards; the earlier task evidence records the test-to-shard mapping and exact executed test names on the unchanged code candidate. This round changes only the DE documentation mirror. No new tests or CI routing changes were added in the dedefix round.
- Planning source artifacts reviewed: `tasks/t-20261114-r28-perses-contract-seam.md`, `act-1575-review-r8.md`, and `dedefix-r1.md`.

## repo-rule compliance

- Product review was read-only. No product file, PR, hosted run, branch, container, VM or merge state was changed.
- No local test suite was run; the review used the exact-head hosted run and the task's prior test evidence.
- Only this review artifact is being published to `baseharbor-plan`.

## Finding

### Blocking — the Perses provider descriptor is intentionally invalid

Files:

- `internal/capability/perses.go:47-55`
- `internal/capability/perses_test.go:43-58`
- Existing contract: `internal/capability/integration_contract.go:145-150`

`PersesManagement` is typed as an `IntegrationDescriptor`, but supplies no provider capability kinds and no versioned capability specifications. The existing `IntegrationDescriptor.Validate` therefore rejects it. The new test treats this rejection as expected. Since the built-in catalog is assembled from validated integration descriptors, this value cannot serve as the concrete provider-owned management-tool representation required by the task; it is an invalid descriptor beside the separate surface/status implementation.

**Change recipe:** replace the invalid `IntegrationDescriptor` value with a purpose-specific management-tool/surface contract tied to the existing observability owner and its optional `management-ui` interface, or define a genuinely valid versioned provider contract before representing Perses as a registry provider. Keep Perses out of application capability declarations unless a real capability is specified; do not add a fake metrics/logs/traces capability. Update the tests to verify the chosen catalog/registry boundary and ownership/interface contract instead of asserting that the exposed descriptor fails validation.

**Test requirement:** add focused `internal/capability` tests showing the chosen Perses representation is accepted at its intended boundary, is not falsely registered as an application capability provider, and preserves the existing provider catalog's validation behavior.

**Stop criterion:** the exported Perses representation has a valid and explicit catalog/registry status, the optional observability management interface and ownership are represented without fake capabilities, and the focused tests plus their existing CI route pass on the new exact head.

## Verdict

REQUEST_CHANGES for exact candidate `219a0a24d5687552556b094223e5e4bcfa2eebc4` on task `t-20261114-r28-perses-contract-seam` / PR #1575.

The dedefix correction itself passes: it mirrors the seven EN technical literals in the paired DE section, its diff is limited to that section, and the exact-head hosted run completed successfully. The contract finding above blocks acceptance. No merge or frost action is included in this verdict.
