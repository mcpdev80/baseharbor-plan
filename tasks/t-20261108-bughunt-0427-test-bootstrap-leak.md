---
id: t-20261108-bughunt-0427-test-bootstrap-leak
card_number: "0427-127"
card_short_title: "Test-Bootstrap leak't Cores"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w127-bootleak-r3
kanban_status: review
kanban_lane: review
kanban_summary: "Runtime integration tests leave no residual bootstrap Core: after the test binary finishes, docker ps -a (and volumes/networks)…"
kanban_title: "0427-127 · Test-Bootstrap leak't Cores"
priority: normal
depends_on: [t-20261108-bughunt-0427-target-env-ignored, t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1454]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-bughunt-0427-test-bootstrap-leak · Bug Hunt v0.4.27: Test-Bootstrap leak't Cores #task #release/v0-4-27 #status/review #view/review #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w127-bootleak-r3 · **Priority:** normal  
    **PR:** [baseharbor#1454](https://github.com/mcpdev80/baseharbor/pull/1454)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261108-bughunt-0427-target-env-ignored](t-20261108-bughunt-0427-target-env-ignored.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w127-bootleak-r3  
**Priority:** normal  
**PRs:** [baseharbor#1454](https://github.com/mcpdev80/baseharbor/pull/1454)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Runtime integration tests leave no residual bootstrap Core: after the test binary finishes, `docker ps -a` (and volumes/networks) show zero `bh-w169-ci-bootstrap-*` objects created by that run, on both docker and podman cells.

## Problem (bug-hunt intake 2026-11-08, verified before carding)

Witnessed live on baha-docker 2026-11-08: three full Core stacks `bh-w169-ci-bootstrap-{2e0a4b61,d1dfaab2,afe2d8fa}-...` (keycloak/openbao/postgres sets) left `Up` by successive test runs of lane 0427-110-compose-native-acceptance. The prefix is hardcoded in `cmd/baha/runtime_integration_test_support_test.go:60` (`bootstrapTarget := "w169-ci-bootstrap-" + ...`); teardown does not destroy the bootstrap target (or fails silently), so every rerun leaks another isolated Core. "w169" is a stale wave label but the leak is current code.

## Acceptance

- Test teardown deterministically destroys the bootstrap Core (or t.Cleanup-registered full teardown on success AND failure paths).
- A CI-visible guard: a follow-up check step (same job) asserts zero leftover `bh-w169-ci-bootstrap-*` after the package finishes (CI-Aufnahmepflicht: runs in the existing go-integration job, no new engine).
- No behavior change for production destroy paths.

## Dependencies and file ownership

Depends on 0427-124 only if that fix changes target naming used by the helper; write-set: the test support file(s) under cmd/baha + one check step in the existing workflow that already runs the package.
