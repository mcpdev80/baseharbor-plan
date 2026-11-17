# CODEX-REVIEW-2 — PR #1676

Date: 2026-11-17. Separate sequential REVIEW role under `coordinator/mission-codex-review2-1676.md` and coord contract ruling. No product edit, GitHub review mutation, or merge performed.

## Candidate identity and CI

- PR #1676 exact head: `ecfccbb9bb897e3bcd1d4cad8f5559b3a6e23e6c`; base develop observed at `8db0d9bdf8d9ae77db94c9ddce9c209001c4da54`, included as second parent of merge commit `9ae08086e01739984eb197375dece37c145b8b8e`.
- Exact-head `pull_request` run [44018836577](https://github.com/mcpdev80/baseharbor/actions/runs/44018836577) is terminal `completed/success` on that SHA; `PR Selected Checks` is `SUCCESS`. No new run is needed for the unchanged product SHA.
- PR state was OPEN, non-draft, MERGEABLE, `mergeStateStatus=CLEAN`; head matches exactly.
- Reviewed the candidate diff from `develop` to this SHA. Product files remain unchanged since review-1.

## Contract applied

Per coord's explicit contract-owner ruling and the task's `## contract-ruling` decision line, workload-only apps with no declared endpoint are snapshot-only logical metadata. No scrape endpoint is invented; this source must not be projected into Prometheus file_sd or provider networks; only this non-scraped metadata skips source verification. Real endpoint-backed provider sources retain normal verification and fail-closed behavior. This ruling supersedes review-1's endpoint objection; review-1 wording is not used as the acceptance contract.

## Guardrail verdicts

1. **Snapshot identity and non-projection — PARTIAL.** `TestWorkloadOnlyRegistersSharedSnapshotOnDeploy` exercises `EnsureRuntime -> EnsureProviderFiles`, asserts the `runtime-sources.json` contains the source ID, owner, and symbolic `runtime://` target, then positively scans `ProviderFiles.TargetsDir` JSON files and fails if the workload source ID appears. This proves file_sd target-file absence. The test does not inspect generated Compose/provider network projection, and it does not explicitly assert that `VerifyProviderSourcesAt` sends no source-specific query (it only observes a nil return). Production filters exist in `providerMetricNetworks` and the `VerificationNone` branch in `VerifyProviderSourcesAt`, but this guardrail specifically requires positive absence evidence in the generated file_sd/network/query outputs. Those network/query absence assertions are missing.
2. **Existing scrapeable sources — PASS by diff inspection.** Existing `Verification != ObservabilityVerifyNone` sources keep the existing target file generation, provider network inclusion, and `up{baseharbor_provider,baseharbor_source}` verification loop. The new conditional skips only `VerificationNone`; no other verification behavior is removed or changed.
3. **Card contract trace — PASS.** The task frontmatter has `source_note` pointing to the snapshot-only contract ruling; the task body has the `## contract-ruling (coord 04:5xZ)` decision line. The task's evidence list also points to this review-2 akte.
4. **`VerificationNone` scope — PASS by production-code scope.** The only new production registration assigning `ObservabilityVerifyNone` is the metrics metadata item created in `reconcileApplicationMetricsSource`; the adjacent code comment identifies the symbolic target as non-scraped and excludes it from file_sd/network. The logs/traces entries in that function retain their own verification modes. Existing endpoint-backed provider sources are not assigned this mode by this change.

## Verdict — CHANGES REQUESTED

Guardrail (1) is not fully evidenced. Recipe: extend the real-path workload-only test to inspect generated `ProviderFiles.Compose` and assert the workload provider network is absent; add an explicit assertion that no Prometheus source-specific query is issued for this logical metadata (for example, a recording local HTTP endpoint/client seam asserting zero query requests while ordinary endpoint-backed sources still exercise the query path). Keep the existing positive snapshot assertion and file_sd directory scan. Then update the same SHA's checks/evidence as required by the changed candidate; a product SHA change needs a new exact-head PR run and another review.

Planning publish is pending: `plan.py render` succeeds, but current `plan.py check` reports 20 schema errors in the five modified hunt-intake cards `tasks/t-20261117-hunt-signals-{101..105}.md` (missing release/repo metadata, plus tag/state mismatch). Those card files have concurrent modifications outside this review; none were changed by the review. No APPROVE attempt and no merge. Head guard was not exercised because verdict is not APPROVE.

Coordinator subsequently completed the hunt-intake schema fixes in commits `224b0d3c`, `39fbc8c7`, and `93f261aa`. Recheck after those updates: `python3 scripts/plan.py render && python3 scripts/plan.py check` passes with 0 errors and 34 existing warnings. This supersedes the pending-publication note; the review remains CHANGES REQUESTED solely for the absent explicit network/query absence assertions.
