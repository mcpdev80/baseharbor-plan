---
id: t-20261122-target-create-operator-auth-decision
card_number: "0428-247"
card_short_title: "target create opauth decision"
type: task
areas: [cli, security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: "Owner / Core"
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-247 · target create opauth decision
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "Owner decision recorded 2026-11-25: target.create requires the existing authenticated operator authority path; implementation and #1746 verification remain pending."
resolution: ""
evidence: []
---

- [ ] t-20261122-target-create-operator-auth-decision · target create reaches the managed-operator auth boundary with no local-workload hook; owner decides the consent/auth path #task #release/v0-4-28 #status/wait #view/wait #area/cli #area/security #kind/task
    <!-- generated:card -->
    **Owner:** Owner / Core · **Priority:** high  
    **Waiting:** Owner decision recorded; implementation and #1746 verification remain pending  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Owner / Core  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by H-V27 (f0f6c8b4) + owner Pre-Release evidence, develop 676909a7

#1746 Pre-Release job 137212735131 runs `baha target create mcp-static --provider docker --access local-docker --reference local --scope default --default` and fails with managed-operator auth denial (`operator_authentication_required`). This is NOT a mapping carve-out #1771 can close and NOT a #1746 content defect; it is product auth semantics, the same class as consent 0428-236.

Exact chain (file:line, read-only verified):
- `cmd/baha/main.go:158-175` `cliLocalWorkloadOperation` maps only the `app` subcommands (plan/up); `target create` returns empty, so `main.go:153` sets no `localWorkloadScope`. App commands have a hook (`app_context.go:106,124`); target create has no analog.
- Denial at `cmd/baha/mcp.go:300` + `314-323`; `ManagedEnvironment` for dev is true (`internal/operatorauth/config.go:89-93`); `verifiedLocalWorkloadAuthorityWithRuntime` needs `LocalWorkloadOperation=true` (`local_workload_authority.go:57`) which target create never sets.
- `--access local-docker` resolves to `accessProvider=local` (`target.go:118-119`) only — satisfying the access condition, not the managed-operator boundary.
- Path: `createTarget` target.go:286 → `createTargetDefinition` target_mutation.go:583 → `authorizeTargetCreation`:64 → `authorizeMCPOperation` mcp.go:419 → managed boundary.

## Owner decision — 2026-11-25

Select the product path: `target.create` is a mutating operation and requires an authenticated, authorized operator through the existing managed-operator/local-workload authority seam. Add the target-create route and authorization hook; do not weaken the shared authorization guard or carve out a managed-boundary exception. Reads remain unchanged. #1746 must verify that an authorized operator can create the target and an unauthorized caller is denied.

## Boundaries

Owner/Core decision record only. No lane edits to mcp.go / local_workload_authority.go / main.go guard logic. Blocks #1746 static/mcp acceptance until ruled.

Scope durch H-V27+H-V28 belegt: target.create only. app footprint show/list/mcp-reads OK.
