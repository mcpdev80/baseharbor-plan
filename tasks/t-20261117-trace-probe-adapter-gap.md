---
id: t-20261117-trace-probe-adapter-gap
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-108"
title: "runtimeComponentTraceProbe lacks trace-consumer adapter for prometheus sources"
kanban_status: closed
kanban_lane: closed
kanban_title: 0428-108 · runtimeComponentTraceProbe
kanban_summary: ""
sources: []
source_note: "0428-093 lane diagnose-pflicht END_BLOCKED (akte: evidence/r28-welle3-2026-11-16/i18n-abachtung/rebase-window-1.md); PR zu frueh geoeffnet, candidate unvollstaendig bis restauration; run auf af2fb5f6 zaehlt nicht"
depends_on: []
owner: coord
blocker: ""
resolution: accepted
superseded_by: ""
prs: [mcpdev80/baseharbor#1679]
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/i18n-abachtung/rebase-window-1.md", "https://github.com/mcpdev80/baseharbor/pull/1679", "https://github.com/mcpdev80/baseharbor/actions/runs/44040963470", "https://github.com/mcpdev80/baseharbor/actions/runs/44042477049", "https://github.com/mcpdev80/baseharbor/actions/runs/44046875648", "https://github.com/mcpdev80/baseharbor/commit/0ec4706b12c8fa869a2c23db18b6cab4f91f2178"]
card_short_title: runtimeComponentTraceProbe
---

- [x] t-20261117-trace-probe-adapter-gap · runtimeComponentTraceProbe lacks trace-consumer adapter #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** coord  
    **PR:** [baseharbor#1679](https://github.com/mcpdev80/baseharbor/pull/1679)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/i18n-abachtung/rebase-window-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1679), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44040963470), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44042477049), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44046875648), [proof 6](https://github.com/mcpdev80/baseharbor/commit/0ec4706b12c8fa869a2c23db18b6cab4f91f2178)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261117-hunt-signals-102](t-20261117-hunt-signals-102.md)  
**Owner:** coord  
**Priority:** not set  
**PRs:** [baseharbor#1679](https://github.com/mcpdev80/baseharbor/pull/1679)  
**Source:** 
<!-- /generated:links -->


## 2026-11-17 candidate status

- PR #1679 is open at exact head `af2fb5f6fac1c8a56079a2fe18faecbb06fc2315`, based on `develop`; exact run [44040963470](https://github.com/mcpdev80/baseharbor/actions/runs/44040963470) failed Go unit shards, build, vet, and selected checks. This head is incomplete: the lane worktree has additive commit `1b5a0df37` with the production trace receiver adapter/pruning files, while the work was still restoring omitted intent-removal and project-scope regression changes. The run is not acceptance evidence.
- Latest verified BaseHarbor `origin/develop` is `4094448543359a13ba312119304f1f70d3bc40a9`. Keep 0428-108 active; require a clean complete candidate and a new exact-head CI run.


## 2026-11-17 complete candidate refresh

- Lane pushed complete clean candidate `082cefab0d5a2624031daa520e52c14f17379a69`, including the trace receiver adapter, receiver/project-scoped pruning, and regressions for unbinding, receiver transitions, legacy cleanup, and removed OTLP intent. Clean-worktree build was reported as `BUILD_OK`.
- Exact-head run [44042477049](https://github.com/mcpdev80/baseharbor/actions/runs/44042477049) completed successfully on this head. Independent review remains acceptance-blocking: same-ID cross-provider preservation requires provider-scoped registration and pruning. The provider-explicit reconcile must also handle an empty desired set; the runtime-component caller must pass its provider so disabled collection removes stale owned signals while preserving a same-ID foreign provider. Regression must exercise the real caller path. This run predates these uncommitted fixes and is not their acceptance evidence.


## Review follow-up - 2026-11-17

- The registry can hold same-ID records across providers. Reconcile and prune must both scope mutations by provider; the empty-desired case must pass explicit ownership so disabled runtime-component collection removes stale owned records while preserving a same-ID foreign source.
- Verify this through the runtime-component caller, not only registry unit tests. The current API exists but the caller was still being wired at last review.
- Run [44042477049](https://github.com/mcpdev80/baseharbor/actions/runs/44042477049) succeeded on old candidate 082cefab and does not cover review fixes. Require a clean complete checkout and a new terminal exact-head run before acceptance.


## Provider-scoped registry fix - 2026-11-17

- Additive commit 39810520b is pushed to PR #1679. It scopes reconcile and prune by provider, adds explicit ownership for empty desired sets, wires runtime-component reconciliation to that API, and adds same-ID cross-provider and disabled-policy regressions.
- Clean remote-head witness at 39810520b: clean detached checkout; `go build ./...` passed; `go vet ./cmd/baha ./internal/observability ./internal/telemetry ./internal/application` passed; `go test ./internal/observability -count=1` and `go test ./internal/application -run '^Test(WorkloadTrace|WorkloadReceiver|LegacyPrometheus|ReceiverTracePrune|RuntimeComponentReconcile)'` passed. The focused same-ID and empty-desired runtime-component cases passed; an isolated fail-first with the old caller confirmed stale metrics remain without explicit ownership.
- Exact-head run [44046875648](https://github.com/mcpdev80/baseharbor/actions/runs/44046875648) is in progress on this commit. Run #44042477049 is green only for the previous head and is not evidence for this change. Keep acceptance pending the new run and final diff review.


## Maintainer acceptance - 2026-11-17

- Owner-delegated Maintainer acceptance by Codex. Exact PR head 39810520b5b1b7859faee4d9b489a4864a150948 passed required selected CI run [44046875648](https://github.com/mcpdev80/baseharbor/actions/runs/44046875648); clean detached build, affected-package vet, observability tests and focused trace/runtime-component regressions are recorded above.
- Independent diff review resolved the receiver identity, same-ID provider ownership, and empty-desired runtime-component findings with regressions. PR [#1679](https://github.com/mcpdev80/baseharbor/pull/1679) merged to develop at merge commit [0ec4706b12c8fa869a2c23db18b6cab4f91f2178](https://github.com/mcpdev80/baseharbor/commit/0ec4706b12c8fa869a2c23db18b6cab4f91f2178); verified remote develop points to that commit.
