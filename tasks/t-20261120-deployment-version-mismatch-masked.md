---
id: t-20261120-deployment-version-mismatch-masked
card_number: "0428-200"
card_short_title: "record version mismatch masked"
type: bug
areas: [cli, lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-200 · record version mismatch masked
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-deployment-version-mismatch-masked · record version mismatch masked #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-V21 (2026-11-20, develop `40cb28c758b0`)

Hunt akte: `evidence/r28-welle4-2026-11-20/bughunt-hv21-shipped-surface/round-1.md`, slice "upgrade from outside".

When the shipped binary starts on a state written by an older shipped version (`deployment.json` carrying
`"version": 1` while `DeploymentRecordVersion` is 2), failing closed is correct - nothing is migrated or promoted.
The message is the defect:

- `internal/deployment/deployment_store.go:656` `loadDeploymentRecordFile` raises
  `unsupported deployment record version 1` as a `DeploymentRecordStateError` with `Kind="corrupt"`.
- `ListDeploymentsForDisplay` (`deployment_store.go:751`) collects it as a best-effort warning.
- `resolveRegisteredApplication` (`cmd/baha/app_context.go:360`) and the final warning loops
  (`cmd/baha/app_context.go:427-455`) map only the kinds `access-denied` and `malformed` - `corrupt` falls
  through, so the user reads `application X has no registered deployment`.

Measured with the shipped binary: `baha app status olddeploy` and `baha app destroy olddeploy --yes` both print
`no registered deployment on target local` for a version-1 record. The real decision (version gate) is hidden
behind a statement that is false.

## Acceptance

1. A version-mismatched deployment record is reported with its own reason on the human surface: the message names
   the version found, the version expected, and the supported next step (upgrade path or operator action).
   `no registered deployment` must not be shown for a record that exists but is version-gated.
2. Fail-closed behavior stays: nothing is migrated, nothing is promoted, no state is rewritten.
3. A regression builds the older record on disk, runs the real command surface, and asserts the version reason
   appears for status, destroy and list - one distinct failing test per surface.
4. One hosted run at the exact head shows the owning shard executed, 0 failure. Gate failures from `0428-198` are
   recorded and reported, not fought.

## Boundaries and stops

- Allowed to write: `internal/deployment/deployment_store.go` (error kind plus message only),
  `cmd/baha/app_context.go` (the kind mapping), and their test files.
- Locked (other owners): `internal/observability/registry.go` (0428-078 plus 0428-189..194),
  `internal/machine/**` and `internal/operatorauth/**` (#1594/#1615/#1650 owner stack),
  `internal/metrics/**` (#1714), `internal/serviceaccess/**` (#1684), `cmd/baha/context_terminal*.go` (#1718).
- This card must not introduce a migration: an upgrade writer would need its own card and an owner decision.
- No subagents (AGENTS 4.8), no `git add -A`, no merge, no force-push on develop/main.
