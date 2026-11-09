---
id: t-20261023-appid-repo-workflow-proof
card_number: "0427-071"
card_short_title: "execute native"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: coord-welle3 (lane w33)
kanban_lane: closed
kanban_summary: Execute TestRepositoryWorkflowRealLifecycle as an actual native Docker lifecycle on a fixed current develop candidate. Preserve…
kanban_status: closed
kanban_title: "0427-071 · execute native"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor/actions/runs/41622395038]
---

- [x] t-20261023-appid-repo-workflow-proof · execute native TestRepositoryWorkflowRealLifecycle on a fixed develop candidate #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle3 (lane w33)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/41622395038)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle3 (lane w33)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Execute `TestRepositoryWorkflowRealLifecycle` as an actual native Docker lifecycle on a fixed current develop candidate. Preserve the real owned-path and foreign-owner/unsafe-permission assertions; a skipped test or unrelated green job does not qualify this behavior.

## Current Owner decision — 2026-11-03

Marcel explicitly directs Codex to remove this blocker and carry out the required existing CI execution. Codex and the assigned coordination may trigger the existing Docker Core workflow for this card and retry diagnosed failed/affected work without another Owner permission round. GitHub-hosted runners, runtime isolation and cleanup remain mandatory. No release, tag, ruleset activation or unrelated workflow changes are authorized.

The supported push trigger `runtime-validation/docker/**` already exists in `.github/workflows/docker-runtime-acceptance.yml`. A temporary branch pinned to the candidate starts the ordinary workflow without changing product source or merging draft #1055. The old "Owner decision pending" and "workflow has 0 runs" notes are superseded.

## Scope

- Execute the existing normal Docker Core workflow on fixed candidate `1706272c3e8d53d37cf4da8f9f1411e5fe419a94`, the develop head at execution selection.
- Preserve the existing task owner and all concurrent product claims. This operational unblock does not take over product implementation.
- No CI evidence collector, completed-run verifier, manifest, extra receipt or receipt approval chain is required. A new develop merge is not needed for this already-integrated test.
- Preserve the separate app.id parser fixture and provider-registry environment-dependency tasks.

## Acceptance

- The existing Docker integration step sets `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` and actually runs `TestRepositoryWorkflowRealLifecycle` on the selected source; the named test and package pass without a skip.
- The workflow checks its exact checkout/build identity and verified isolated runtime, runs its existing assertions, and completes its required cleanup and normal final execution check successfully.
- Record the ordinary execution outcome and fixed candidate in this task's handoff. Do not substitute an unrelated green workflow or close the card while its required execution is pending or failed.
- Use the current minimal two-field merge receipt only when an actual product merge occurs; this validation alone writes no additional CI receipt.

## Required checks

The existing `Runtime · Docker Core` workflow executes its normal serial runtime integration checks, recovery, logs/traces and cleanup. Its normal job result determines success. Draft #1055 and the former SHA/run/attempt/hash receipt-verification machinery are not prerequisites.

## Dependencies and file ownership

- Depends on release-start cleanup/updates (t-20261017-release-0-4-27-updates); no product file ownership yet — no implementation, only evidence retrieval or a CI workflow selection.
- Shared: the develop candidate SHA is owned by the integration lane; do not rewrite it to force a receipt.

## Handoff

- 2026-11-03: Owner-authorized acceptance based on existing normal workflow [Runtime · Docker Core run #41622395038](https://github.com/mcpdev80/baseharbor/actions/runs/41622395038), job `docker-runtime` SUCCESS. Exact checked-out develop candidate and built commit: `1706272c3e8d53d37cf4da8f9f1411e5fe419a94`; rootless Docker engine verified; `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`. Go JSON test output explicitly records `TestRepositoryWorkflowRealLifecycle` `run` then `pass` (96.74s; no skip). The test reported owned runtime absent after retirement, canonical identity/data/material retained, and unrelated shared installation unchanged. Final job output: `All eight required Docker runtime tests executed and passed.` Existing required runtime cleanup completed. No product merge, additional receipt, or new workflow trigger needed.
- Current state and ordinary execution results, newest first.
- 2026-11-03: Owner-authorized execution started via the existing push trigger. Temporary branch `runtime-validation/docker/appid-repo-1706272c` points exactly to `1706272c3e8d53d37cf4da8f9f1411e5fe419a94`; no source commit or product merge was created. Ordinary execution: https://github.com/mcpdev80/baseharbor/actions/runs/41622395038. Administrative blocker removed; native test execution remains pending. The historical handoffs below describe the earlier CI design and do not reinstate it.
- 2026-10-24 (o113): state remains waiting; v0.4.27 release-start updates unaccepted. CI-explicit-candidate-trigger #1055 is an unqualified draft PR (head work/ci-explicit-candidate-trigger-20261024) in the develop merge window; no acceptance is recorded. Resolution documented here only because the schema forbids a free-text resolution field on a non-checked card.
- Defect handoff from APPID-R2 recipe point 3 (`evidence/board-2026-10-23/codex-verdict-reviewwave.md`): `TestRepositoryWorkflowRealLifecycle` (fixture `cmd/baha/app_repository_integration_test.go:16`) SKIPS without `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` or a resolvable runtime; the mandatory-native scope check (`cmd/baha/repository_runtime_fixture_test.go:411`) is static YAML/test-name counting, not execution. Historic run IDs 39619782116 / 39627285799 / 39831982468 return HTTP 404 or run only static MCP with runtime skipped, so the required receipt is unverifiable from outside. F27 review on 2026-10-23 (live checks 17:07–17:15 UTC, authenticated `mcpdev80`) confirms develop `1861ed07888a1ec22c218ca491d23ee54f48e261`, Planning `c41cd2cf5d9d2ed7ba18bc346c0cd1ee4f2148e8`; PRs #1008 (`8a40e60a…`) and #1029 (`30e112431b04a7e24e7e7e9ea76a3600e439a988`) are merged and ancestors of develop, but no open APPID native-lifecycle PR exists. Positive owned-path case and negative foreign-owner/unsafe-permission cases are required; do not add skip-if-unverifiable or weaken the production ownership guard. This is a separate task, not a prerequisite for accepting the app.id parser fixture.
- Recipe point 4: after the retrievable receipt and exact-source reviews are attached and all acceptance criteria are mapped, run Planning render/check and publish through the existing owner protocol; no product merge is needed for the already-integrated fixture.
