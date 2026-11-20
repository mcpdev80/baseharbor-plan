---
id: t-20261120-r28-develop-runtime-integration-red
card_number: "0428-174"
card_short_title: "runtime Integr tests fail"
type: bug
areas: [ci, runtime]
release: v0.4.28
version: ""
parent: ""
owner: w083-pr0428-083-datasources-hopf5
kanban_status: active
kanban_lane: active
kanban_summary: "Make the native runtime integration path green on develop again. The job docker-runtime, step \"Run runtime integration tests…"
kanban_title: 0428-174 · runtime Integr tests fail
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-develop-runtime-integration-red · Develop: runtime integration tests fail serially in docker-runtime (base defect) #task #release/v0-4-28 #status/active #view/active #area/ci #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** w083-pr0428-083-datasources-hopf5  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w083-pr0428-083-datasources-hopf5  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make the native runtime integration path green on `develop` again. The job `docker-runtime`, step "Run runtime integration tests serially", fails when run against plain `develop` with no lane content involved, so every PR whose candidate selects that gate is red for a reason that is not its own.

## Scope

- In scope: reproduce the failing runtime integration step on a neutral `develop` checkout, identify the first failing test and its cause, and fix it on `develop` (or prove the gate needs an environment precondition that the runner does not provide, and record that requirement).
- In scope: the gate family selected by `PR · Native · native/docker/perses-runtime-smoke`.
- Out of scope: datasource and dashboard feature work of other cards. Out of scope: `.github/**` trigger changes - report a needed change as a finding with file:line to the Coordinator (owner scope).

## Acceptance

- A hosted witness on a `develop` commit shows the runtime integration step passing, or names the environment precondition the gate needs and then shows it green.
- The failing test name, file and first error line are recorded verbatim in the evidence file.
- PR mcpdev80/baseharbor#1684 can be re-verified against the fixed base without changing its content.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable.

- **Test binding (select exactly one):** normal (auto-discovered) - the failing step runs the existing package-discovered integration tests; no new catalog entry is expected.

## Dependencies and file ownership

- Owned files or areas: the native runtime integration harness selected by `native/docker/perses-runtime-smoke` (internal/application and the contracts helpers it drives).
- Shared files: coordinate through the owning task. `.github/**` stays with the owner.

## Base defect witnesses (measured by the Coordinator, 2026-11-20)

- https://github.com/mcpdev80/baseharbor/actions/runs/44661597243 - workflow "Runtime · Docker Core", event `workflow_dispatch`, head `ec02d5faad24` (a plain `develop` commit, 2026-11-20T02:33:03Z), job `docker-runtime` conclusion `failure`, failing step "Run runtime integration tests serially".
- The same workflow's ordinary `push` runs on newer tips `f61ef0f4991c` and `36d075fad77f` conclude `success`, so the red path is reached only through the manual/dispatch selection route - which is what the PR gate selects for affected paths.
- Lane witness with a local reproduction on pure `develop`: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/perses-datasources/fix-1.md

## Handoff

- Opened by the Coordinator from the w083 finding on PR #1684 (card t-20261114-r28-perses-datasources): that candidate cannot reach a green required gate while this base defect stands. Newest first.

base-defekt, gemessen an zwei gehosteten zeugen: run 44661597243 (workflow 'Runtime · Docker Core', workflow_dispatch, head ec02d5faad24 = nacktes develop) job 'docker-runtime' step 'Run runtime integration tests serially' = failure; dieselbe workflow auf develop-push (f61ef0f4991c, 36d075fad77f) = success. mission liegt bei der lane, die den fallback lokal schon reproduziert hat (§5.3: neutraler produktionspfad, nicht reviewer-sandbox)

wurzelgrund UNABHAENGIG belegt durch die read-only PR-sweep-Lane der anderen welt (evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md): 'required native Perses smoke failed BEFORE ASSERTIONS because Docker could not create /etc/perses/database on the image's read-only root' —environment-voraussetzung, keine produktbehauptung; erklaert success auf develop-push vs. failure im selectierten dispatch-pfad. korrekturmaßstab: kleinste aenderung am tmpfs-mount des tests; waere nur .github/** behebbar, STOP mit datei:zeile an den coordinator (owner-scope)
