---
id: t-20261117-hunt-signals-102
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-102"
title: "application-Klasse fehlt in der Signal-Registry"
kanban_status: blocked
kanban_lane: blocked
kanban_title: 0428-102 · App-Klasse fehlt in der
kanban_summary: ""
sources: []
source_note: "hunt hunt-signals befund-1 (akte: evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md)"
depends_on: [t-20261117-trace-probe-adapter-gap]
owner: Codex
blocker: "halde bis merge von 0428-108 (neuer develop-shead, nicht ed55d893)"
wait_reason: ""
resolution: ""
superseded_by: ""
prs: [mcpdev80/baseharbor#1677]
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md", "https://github.com/mcpdev80/baseharbor/pull/1677", "https://github.com/mcpdev80/baseharbor/actions/runs/44031866829"]
card_short_title: App-Klasse fehlt in der
---

- [ ] t-20261117-hunt-signals-102 · application-Klasse fehlt in der Signal-Registry #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** Codex  
    **PR:** [baseharbor#1677](https://github.com/mcpdev80/baseharbor/pull/1677)  
    **Blocker:** halde bis merge von 0428-108 (neuer develop-shead, nicht ed55d893)  
    **Needs:** [t-20261117-trace-probe-adapter-gap](t-20261117-trace-probe-adapter-gap.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-signals/befund-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1677), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44031866829)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261117-trace-probe-adapter-gap](t-20261117-trace-probe-adapter-gap.md)  
**Required by:** [t-20261117-hunt-signals-103](t-20261117-hunt-signals-103.md), [t-20261117-hunt-signals-104](t-20261117-hunt-signals-104.md)  
**Owner:** Codex  
**Priority:** not set  
**PRs:** [baseharbor#1677](https://github.com/mcpdev80/baseharbor/pull/1677)  
**Source:** 
<!-- /generated:links -->

Einzelschritte in der referenzierten hunt-akte (befund-1.md); Umsetzung als normale task-kette (claim -> branch -> CI -> evidence -> review).


## Test binding

- **Test binding (select exactly one):** ☑ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Tests: `internal/observability.TestListApplicationMetricsRequiresExplicitClassAndApplicationScope`; `internal/metrics.TestBindWritesAttributedTargetAndPrunesOnlySameApplication`; `internal/metrics.TestVerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata`; existing `internal/metrics.TestWorkloadOnlyRegistersSharedSnapshotOnDeploy`.
- Local route: `go test ./internal/observability ./internal/metrics -count=1` passed at PR head `58db26baf9dcd80566dcbb0042eed2818e5af822`; `go vet ./internal/observability ./internal/metrics` passed. Compile-only checks for updated List call sites in `cmd/baha` and `internal/identityprovider` passed.
- CI trigger/route: Ready PR #1677 with changed Go source paths selected `PR · Go unit · packages`, `PR · Go unit · owner`, `PR · Validation · go-build`, `PR · Validation · go-vet`, and `PR · Validation · identity-provider-package-tests`. Run [44031866829](https://github.com/mcpdev80/baseharbor/actions/runs/44031866829) is exact-head. Go unit shards, package/owner unit checks, build, vet, identity-provider package checks and Docker identity passed. Docker observability failed. Job 133865952530 terminally failed at guided-up-consented: prometheus:bh-atomic-docker-observability-demo-dev is a native OTLP trace source with no runtime probe adapter. The preceding --confirm-candidate refusal is the expected negative-consent assertion; the confirmed flow then fails on trace verification. The offending source is already present on origin/develop (internal/application/runtime_observability.go); #1677 does not change it. Develop advanced from the PR base after #1575 and #1577 merged; latest verified remote develop is ed55d893374b593a7a6032f0de496ca9920ad08d. Keep #1677 unmerged; 0428-108 now owns the same root-cause fix; keep #1677 scoped, wait for 0428-108 acceptance/merge, then rebase and rerun exact-head checks.
- The CI plan selected Docker observability for this PR; no Podman runtime job was selected. Acceptance remains open until the failure is diagnosed and applicable exact-head checks are green.


## Review fix prepared for the next push

- Exact-diff review found application metrics verification filters the registry by app name but not by environment, while IDs are keyed by app+environment and pruning is environment-specific. Fixed in separate local commit `f7b9275dddf2ab0d508df44912e4aac8d8a3fa88`: verification skips IDs outside the current app/environment prefix, with a regression fixture registering the same app in dev and prod and asserting only the current environment is queried.
- Verified on that commit: the targeted regression test, `go test ./internal/observability ./internal/metrics -count=1`, `go vet ./internal/observability ./internal/metrics`, and `git diff --check` pass. Commit remains local/unpushed until the planned 0428-108 hop so the next candidate run includes both fixes. No exact-head CI claim for this commit yet.

## CI failure triage

- Exact run [44031866829](https://github.com/mcpdev80/baseharbor/actions/runs/44031866829), Docker observability job [133865952530](https://github.com/mcpdev80/baseharbor/actions/runs/44031866829/job/133865952530), failed in TestObservabilityFullStackAcceptanceInCI on the consented guided-up path. The non-consented candidate refusal is the expected security assertion.
- Side-find (`--confirm-candidate`, no new card): bounded failure summary in job 133865952530 at log lines 3176-3181 contains both the expected negative-consent message (`:3179`) and the distinct actual failure, `native OTLP trace source ... has no runtime probe adapter` (`:3180`), followed by the consented-path exit (`:3181`). The refusal is implemented at `cmd/baha/app_candidate_consent.go:148-152` (message at `:150`) and the full-stack fixture proceeds to the consented apply at `cmd/baha/app_observability_acceptance_test.go:190`; the terminal assertion is trace queryability at `:249-250`. Thus the bounded summary does not indicate a `--confirm-candidate` gate defect: the refusal is an expected negative-consent assertion, while the separately failing trace assertion is owned by 0428-108. No extra card is warranted.
- Root cause verified from job logs and source: app workload traces are recorded with ProviderPrometheus, Mode Native, Protocol otlp, and a symbolic runtime target; runtimeComponentTraceProbe only supports RuntimeBroker and RuntimeExecutor. This code is already in develop at 4bab986dc; #1677 only touches registry/list/metrics verification paths and does not introduce the trace source.
- Base freshness also changed: latest verified remote develop is ed55d893374b593a7a6032f0de496ca9920ad08d following #1575 and #1577. Branch head remains 58db26baf9dcd80566dcbb0042eed2818e5af822. Coordinator confirmed that 0428-108 is already active on this same root cause and received the independent reproduction as a fourth regression; 0428-102 waits for 0428-108 before rebase and exact-head rerun.


## Dependency refresh - 2026-11-17

- 0428-108 now has PR [#1679](https://github.com/mcpdev80/baseharbor/pull/1679), but it is still in progress: current remote head `af2fb5f6` is incomplete and exact run [44040963470](https://github.com/mcpdev80/baseharbor/actions/runs/44040963470) failed compile/test checks. Do not rebase or rerun #1677 against this candidate.
- Latest verified `origin/develop`: `4094448543359a13ba312119304f1f70d3bc40a9`. Keep #1677 blocked on 0428-108 acceptance; preserve local environment-isolation commit `f7b9275d` for the combined post-dependency candidate.


- 0428-108 has advanced from the incomplete `af2fb5f6` candidate to complete PR head `082cefab0d5a2624031daa520e52c14f17379a69`; exact run [44042477049](https://github.com/mcpdev80/baseharbor/actions/runs/44042477049) completed successfully; independent review remains open. #1677 stays blocked pending accepted 108 and then a fresh develop rebase.


- 0428-108 review requires provider-scoped reconciliation and pruning, including the real empty-desired runtime-component caller, with a same-ID foreign-provider regression. Run #44042477049 is green only on pre-review head 082cefab; it is not acceptance evidence for the follow-up changes.


- 0428-108 has pushed provider-scoped registry correction `39810520b5b1b7859faee4d9b489a4864a150948`; clean-checkout `go build ./...`, affected-package vet, observability tests, and focused application trace/empty-desired tests pass. Exact CI [44046875648](https://github.com/mcpdev80/baseharbor/actions/runs/44046875648) is active. Keep #1677 blocked pending this exact head's gates and acceptance, then rebase against current develop.
