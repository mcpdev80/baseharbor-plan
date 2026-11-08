---
id: t-20261106-r27-control-plane-single-default
card_number: "0427-115"
card_short_title: "default Deploy must be SINGLE"
type: task
areas: [platform, runtime, testing]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle5 (w277, entlassen)
kanban_status: closed
kanban_lane: closed
kanban_summary: The default BaseHarbor developer/control-plane deployment MUST use a single instance per required service. Currently the shipped…
kanban_title: "0427-115 · default Deploy must be SINGLE"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1404]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/commits/f3db942859c68e78fe2e7c0a339be7eb0e380acb.json"]
---

- [x] t-20261106-r27-control-plane-single-default · Control plane: default deployment must be SINGLE instances (per-service one postgres/one openbao, no HA ensemble); HA only as explicit opt-in #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/platform #area/runtime #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (w277, entlassen) · **Priority:** critical  
    **PR:** [baseharbor#1404](https://github.com/mcpdev80/baseharbor/pull/1404)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/receipts/commits/f3db942859c68e78fe2e7c0a339be7eb0e380acb.json)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle5 (w277, entlassen)  
**Priority:** critical  
**PRs:** [baseharbor#1404](https://github.com/mcpdev80/baseharbor/pull/1404)  
**Source:** 
<!-- /generated:links -->

## Goal

The default BaseHarbor developer/control-plane deployment MUST use a single instance per required service. Currently the shipped Compose template starts an HA ensemble without an explicit request. SINGLE becomes the default, while HA remains available only as an explicit opt-in.

## Scope

- In scope: shipped Compose assets, effective default profile selection, actual `baha up` and development-environment startup paths, PostgreSQL/etcd, OpenBao, Keycloak, HAProxy, and related initialization, endpoints, persistence, and profile validation. The default must not start extra HA members, load balancers, or require a cluster quorum.
- In scope: explicit HA opt-in with a complete, healthy cluster and visible selection. Repeated `up` or upgrades must not silently switch existing installations between SINGLE and HA.
- Out of scope: destructive automatic migration of existing installations, unrelated application workloads, or eliminating HA support.

## Verified defect (coordinator observation, 2026-11-06)

- Owner requirement: the default must be non-HA, with one instance of each service.
- Product evidence: `internal/runtime/assets/compose.yaml` declares `openbao-member-1/2/3` at lines 268/297/326, HAProxy at line 356, and `postgres-etcd-1/2/3` at lines 10/23/36, without HA-only profiles. The shipped template therefore starts an HA ensemble by default.
- Existing Go code supports both profiles: `internal/runtime/control_plane_profile.go` includes `OpenBaoMembers` and `validateSingleControlPlane`, but the shipped default asset does not follow the SINGLE path.
- Live observation on `baha-docker`: `bh-local-shared-openbao-member-1/2/3`, an admin instance and HAProxy ran in the development smoke setup; the same topology appeared in the CI context.

## Acceptance criteria (mandatory)

- Fresh, unmodified `baha up`, without HA flags/profiles/overrides, starts exactly ONE active instance per required control-plane service on BOTH Docker and Podman. In particular, one OpenBao and one PostgreSQL, no additional OpenBao members, no HAProxy HA load balancer, no three-node etcd/Keycloak control plane, and no mandatory cluster quorum.
- The shipped DEFAULT is SINGLE without any CLI options. Rendered `docker compose config` and the Podman equivalent show the correct topology; the actual startup paths are verified using the running container inventory and health checks. Unit tests of `validateSingleControlPlane` alone do not count.
- HA requires explicitly documented opt-in. With opt-in, the complete chosen ensemble starts healthy, including cluster membership and endpoints. Without opt-in, HA services must not appear in the active rendered configuration.
- SINGLE and HA continue to work after restart and repeated `up`. Configuration, PKI/initialization, ports, and persistence match the selected mode. Existing HA installations are neither silently rebuilt nor deleted; switching modes requires a deliberate, safe decision.
- Red-first regression: the test FAILS on the old incorrect default and PASSES on the fix. Additional negative test: HA is not implicitly enabled. Positive test: explicit opt-in starts the correct HA ensemble. A source mutant that enables HA without opt-in makes the regression test FAIL.
- Every evidence record includes the exact product SHA, host/runtime, commands, rendered Compose configuration, container/service inventory, health, and explicit PASS/FAIL lines. SKIP is never PASS. Green hosted CI does not replace actual Docker/Podman evidence.
- Before merge, a reviewer verifies both the code and the executed default/HA paths. Missing or skipped runtime cells mean BLOCKED.

## Required tests

- Deterministic tests for default profile, Compose-rendered topology, actual CLI/devenv entrypoint, SINGLE validation, and HA opt-in; document red-first and mutation control.
- Real isolated smoke matrix on `baha-docker` and `baha-podman`: per runtime (1) default SINGLE with exact instance counts and health, (2) explicit HA with cluster health, (3) restart/idempotency and persisted state. Never execute tests on the Codeman/coordinator host `baha-runner-docker-2`.
- Targeted Go tests, build, vet, formatting, and GitHub Selected Checks at the final SHA, plus real runtime transcripts committed to the planning repository. Skipped runtime gates do not count.

## Dependencies and file ownership

- Main product scope: `internal/runtime/assets/compose.yaml`, control-plane profile selection, and actual startup paths. Coordinate any files already owned by active tasks before editing; no overlapping concurrent writes.
- Acceptance linkage: `core-815`, `t-20261105-r27-compose-host-isolation`, and `t-20261104-r27-vm-integration-runs`. The default contract must pass before final release qualification.

## Handoff

- Ready for an implementation lane. The defect is verified; no product fix or new test execution is asserted by this card.

2026-11-06 w248 base refresh assigned by Owner. Scope: merge current develop into existing PR branch without content changes, run the resulting hosted gates to terminal, and publish round-2 base-refresh evidence.

## Owner decision — 2026-11-07

**Option A approved.** No further `podman system reset`, Podman-2 rebuild, or replay solely to reconstruct historical pre-reset evidence. The pre-reset volume state remains **unknown** and must never be reported as proven safe. If a clean environment is needed in the future, rebuild it from scratch rather than resetting shared test-host state. Preserve all existing functional evidence. Refresh the exact candidate against develop, verify required checks and code review, then merge #1404 if qualified. Do not weaken the functional acceptance criteria.

## Merge record — 2026-11-07

- PR #1404 merged into `develop`, merge SHA `f3db942859c68e78fe2e7c0a339be7eb0e380acb`.
- Exact candidate head: `ed98ed1dde79fe91cfde11b8d5dfa738f802992f`.
- Hosted CI run 42237544020: completed / success.
- Owner accepted the historical unknown pre-reset volume state without further reset or VM rebuild; this is not evidence that old resources were untouched.
- Downstream compose-isolation task #1383 can now run final integration qualification against merged develop.
