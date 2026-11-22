# PR #1753 independent review

## PLAN

1. Read the refreshed handoff and resolve the live #1753 head, develop base, required hosted run, and evidence destination.
2. Compare the live head with approved head `f29bf6fa303718ee258f4edd40a62dbbecd37f77`; review the footprint operator boundary, exact hosted test receipt, native-gate state, and PR scope without local tests.
3. Publish the exact-head verdict and evidence to Planning `origin/main`, verify the remote path, update the live board, and post END to the Coordinator.

## Session mark

CODEX-REVIEW; read-only. No local tests, product changes, GitHub review/comment, merge, close, or workflow rerun.

## Candidate and verdict

**REQUEST CHANGES** for exact head `50c4bce74d2d269cd985b3e66ac51fc879e0d627` against current `develop` `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9`. The additive-only condition fails: one PR-specific implementation/test commit was added after the approved head. The feature boundary looks narrow and its hosted regression passed, but this extra product/test change is outside the current review authorization.

At verification PR #1753 was OPEN, not draft, `mergeStateStatus=BEHIND`, with blank `reviewDecision`; its live head matched the reviewed SHA. The PR file list against develop contains six product paths and no `.github/**` or `scripts/**` paths.

## Additivity since the approved head

The live comparison `f29bf6fa303718ee258f4edd40a62dbbecd37f77...50c4bce74d2d269cd985b3e66ac51fc879e0d627` reports four commits:

- `1ff16925c4e141d732459a34ddf0b7f49128a214` — `ci(0428-228): admit operator seams to native gates (#1755)`, develop content allowed by this review.
- `ce5cf8f30373e13c0d08092d84b24232e93a356a` — `fix(0428-227): restore exact operator seam test source`, a PR-specific implementation and test change, not an authorized develop hop.
- `5ca8420c1814f25bea6404e55fd054c60746eae5` — `fix(0428-183): valkey dashboards gated on real availability (#1714)`, develop content allowed by this review.
- `50c4bce74d2d269cd985b3e66ac51fc879e0d627` — mechanical hop onto develop `5ca8420c181`.

The blocking extra commit `ce5cf8f` changes `cmd/baha/ci_integration_operator_enabled.go` (16 additions) and `cmd/baha/ci_integration_operator_enabled_test.go` (69 additions). It adds a new operator admission branch and a new Go regression. This violates the explicit requirement that the delta from `f29bf6fa303` contain only develop content and no new product or test change.

Actionable correction: remove/revert `ce5cf8f30373e13c0d08092d84b24232e93a356a` from this candidate while retaining only authorized develop hops, or obtain an explicit scope change before reviewing that product/test addition. Any resulting new head needs its own exact-head CI receipt.

## Footprint operator boundary

The added branch in `cmd/baha/ci_integration_operator_enabled.go:138-147` permits the footprint probe only when `gate == "data-capabilities"` and the command matches the canonical predicate. The predicate at lines 242-249 requires exactly `app footprint show -o json`. The test at `cmd/baha/ci_integration_operator_enabled_test.go:352-419` checks the canonical command receives the scoped test operator on data-capabilities, rejects noncanonical and unrelated commands, preserves guided admission, and rejects the command on lifecycle.

Hosted behavior evidence is exact-head run `44990860430`, event `pull_request`, terminal SUCCESS. `PR · Validation · ci-integration-operator-seam-tests`, job `137111416759`, SUCCESS, ran `go test -tags=baseharbor_ci_operator_testonly ./cmd/baha -run '^TestCIIntegrationOperator' -count=1 -v`; its log contains `--- PASS: TestCIIntegrationOperatorAdmitsFootprintShowOnlyOnDataCapabilitiesGate`. This proves the operator-seam behavior on the candidate. The PR's changed file list does not include `cmd/baha/app_footprint_show.go`; the tested change is in the operator boundary and its test.

## Native gate state

Run `44990860430` is terminal SUCCESS overall. `PR Selected Checks`, job `137112373149`, SUCCESS. The run reports 15 successful and 21 skipped jobs.

`PR · Selected Runtime`, job `137111418122`, was SKIPPED. `PR · Native · ${{ matrix.id }}`, job `137111419930`, was SKIPPED. The successful `PR · Native gate plan`, job `137111382518`, emitted an empty matrix; its log used `BASE_SHA=1ff16925c4e141d732459a34ddf0b7f49128a214` and noted that the trusted native planner was absent there. The handoff explicitly says that, before #1756 adds the catalog rows, these skipped native jobs are expected and are not a rejection reason. They are not counted as passes.

## Scope and publication

The exact PR file list is:

- `cmd/baha/ci_integration_operator_enabled.go`
- `cmd/baha/ci_integration_operator_enabled_test.go`
- `internal/metrics/perses_dashboards_valkey.go`
- `internal/metrics/perses_dashboards_valkey_test.go`
- `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json`
- `internal/metrics/testdata/perses-valkey/valkey-targets.json`

No `.github/**` or `scripts/**` path is in the PR's diff against develop. The extra commit identified above is within the Go product/test paths, so the separate additive-only restriction still blocks this candidate.

Planning repository remote verified before publication:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Planning validation and cleanliness

`python3 scripts/plan.py check`: 0 errors, 10 existing dependency warnings.

`docker ps -a` before: PID 2739822; no containers listed.

`docker ps -a` after: PID 2800083; no containers listed. No review-owned containers or compose projects were started.

## END

END codex-rev-1747 DONE: REQUEST CHANGES for `50c4bce74d2d269cd985b3e66ac51fc879e0d627`; additivity verdict FAIL because of `ce5cf8f30373e13c0d08092d84b24232e93a356a`; run `44990860430` terminal SUCCESS; `PR · Selected Runtime` SKIPPED (expected per handoff). Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
