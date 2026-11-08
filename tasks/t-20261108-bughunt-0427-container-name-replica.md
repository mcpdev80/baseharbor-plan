---
id: t-20261108-bughunt-0427-container-name-replica
card_number: "0427-128"
card_short_title: "backup stop fails on"
type: bug
areas: [dx, lifecycle]
release: v0.4.27
version: ""
parent: ""
owner: pending-lane-0427-128-r6
kanban_status: active
kanban_lane: active
kanban_summary: "baha app backup succeeds for repository workloads that use Compose containername (linkding, JoySafety/AgenticX/Tier0 patterns);…"
kanban_title: "0427-128 · backup stop fails on"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1452]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-bughunt-0427-container-name-replica · Bug Hunt v0.4.27: backup stop fails on container_name (unplanned service replica) #task #release/v0-4-27 #status/active #view/active #area/dx #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** pending-lane-0427-128-r6 · **Priority:** normal  
    **PR:** [baseharbor#1452](https://github.com/mcpdev80/baseharbor/pull/1452)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** pending-lane-0427-128-r6  
**Priority:** normal  
**PRs:** [baseharbor#1452](https://github.com/mcpdev80/baseharbor/pull/1452)  
**Source:** 
<!-- /generated:links -->

## Goal

`baha app backup` succeeds for repository workloads that use Compose `container_name` (linkding, JoySafety/AgenticX/Tier0 patterns); the workload quiesce step no longer fails with "selected stop has an unplanned service replica". 0427-129 documents the debug-goroutine-dump regression on consent denial; this card covers the replica identity defect.

## Scope

- In scope:
  - Canonicalize expected container names in `cmd/baha/app_workload.go` (~line 651) from the effective Compose service config (container_name or `<project>-<service>-1`), so `StopOwnedProjectServices` (`internal/runtime/service_stop.go`) and `ContainerMatchesProjectResource` (`internal/runtime/container_identity.go`) match Docker `container_name` services.
  - Same identity contract applies to `internal/runtime/service_retirement.go:63` and `cmd/baha/control_plane_stop_observation.go:49` paths.
  - In scope files: `cmd/baha/app_workload.go`, `internal/runtime/service_stop.go`, `internal/runtime/container_identity.go`.
- Out of scope: registry/discovery defects, destroy --all Exit-Code semantics (0427-129).

## Acceptance

- A repository workload with explicit `container_name` reaches `baha app backup` READY→written-archive (no "unplanned service replica") on native Docker; same for the existing `project-service-1` default.
- `app down`, `up --yes` and `destroy` succeed against both identity classes.
- Unit + native integration tests for both identity classes; positive selection for a relevant change, negative for an unrelated one (see Required checks).

## Required checks

- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/app_workload.go`, `internal/runtime/service_stop.go`, `internal/runtime/container_identity.go`.
- Shared files: none.

## Handoff

- Current state: bug found on develop 0fe53052d (binary 0.4.11, Phase 0a stamped) at 2026-11-08 on the dedicated rootless test server 192.168.6.178.
- Branch: `bughunt/0427-128-container-name-replica` (PR pending; develop 0fe53052d, commit `4f7011a1...` in candidate fingerprint).
- Report: ~/dev/Tests/Baha-Bug-01-backup-container-name-replica.md
- Evidence: backups under ~/dev/Tests/backups (linkding.bhbackup = letzter Erfolg vor cnref-Test), stdout/logs under ~/tests/2026-11-08-cnrepro/
