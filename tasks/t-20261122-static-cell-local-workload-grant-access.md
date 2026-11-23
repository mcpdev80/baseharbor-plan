---
id: t-20261122-static-cell-local-workload-grant-access
card_number: "0428-243"
card_short_title: "static cell local-docker grant"
type: bug
areas: [testing, identity]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w243-0428-243-static-cell-grant-access
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-243 · static cell local-docker grant
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-static-cell-local-workload-grant-access · Static cells: --access local-docker rejected at local_workload_authority.go:62 #task #release/v0-4-28 #status/active #view/active #area/identity #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** w243-0428-243-static-cell-grant-access · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w243-0428-243-static-cell-grant-access  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by read-only hunt (0428-231 operator-auth static cells) on develop 8629450ef3c

The static-cell gates `shell-ux` (job 137187053472), `init` (137190621488) and `config-matrix` (137190621449) fail with
"Managed-environment machine operations require an authenticated BaseHarbor operator." Primary defect: the fixture registers
`--access local-docker` but `cmd/baha/local_workload_authority.go:62` compares against the short alias `local`, so the grant is
refused; the boundary then errors at `operator_auth_boundary.go:55-90` (ErrConfigurationRequired, surfaced at `cmd/baha/mcp.go:317`).
Secondary: the static cell builds `go build ./cmd/baha` without the `baseharbor_ci_operator_testonly` tag, so
`withCIIntegrationOperator` is the no-op from `ci_integration_operator_disabled.go`.

## Acceptance

1. `local_workload_authority.go:62` accepts `local-docker` (and `local-podman`) as valid local-workload grants, verified against the
   current access-mapper and probe order; the operator-auth boundary is NOT disabled or bypassed.
2. A regression via the existing `cmd/baha` shards proves the grant path now runs; no new CI job and no `.github` edit is required.
3. If the primary fix alone does not clear the static cells, the missing build tag is documented as a finding for the `.github`
   Owner scope — not changed by the lane.

## Boundaries

`cmd/baha/local_workload_authority.go` plus its existing shard tests. This is a SEPARATE mission from card 0428-231 / PR #1761
(helper fan-out, write-set `internal/operatorauth/**`), so it carries its own branch and PR; #1761 is untouched.

dispatched post-recovery 2026-11-23
