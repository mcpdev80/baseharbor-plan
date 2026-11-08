---
id: t-20261108-bughunt-0427-target-env-ignored
card_number: "0427-124"
card_short_title: "Target-ENV ohne Wirkung"
type: bug
areas: [lifecycle,compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-124-target-env
kanban_status: active
kanban_lane: active
kanban_summary: Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.
kanban_title: 0427-124 · Target-ENV ohne Wirkung
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
---

## Outcome and acceptance

Fixed as far as the acceptance criterion holds on native docker AND podman runs; no silent states.

- [ ] t-20261108-bughunt-0427-target-env-ignored · 0427-124 · BASEHARBOR_TARGET wird ignoriert #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-124-target-env · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-124-target-env  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-3 docker2 hunt: grep on develop 0fe53052 shows t.Setenv(BASEHARBOR_TARGET) only in *_test.go (app_backup_runtime_fixture_test.go:26 u.a.), no production os.Getenv read; core self-install for isolated targets missing.

## Acceptance

production command paths honour BASEHARBOR_TARGET (or an explicit equivalent) for target selection; an isolated greenfield run on docker-2 completes without touching shared-plane objects; regression proves the env read on the production path.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.
