---
id: core-318
areas: [kubernetes]
type: feature
release: v0.8.x
version: v0.8.5
parent: v0.8.x
owner: ""
depends_on: [core-313, core-315, core-316, core-317]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#318"]
source_updated: "2026-10-15T16:52:29Z"
labels: [kind/feature, area/kubernetes, area/mcp, area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-318 · Kubernetes: establish CLI, agent and developer parity #task #release/v0-8-x #status/planned #view/waiting #area/kubernetes #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-315](core-315-kubernetes-backup-disaster-recovery.md), [core-316](core-316-kubernetes-observability-diagnostics-evidence.md), [core-317](core-317-kubernetes-updates-migration-recovery.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.5)  
**Depends on:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-315](core-315-kubernetes-backup-disaster-recovery.md), [core-316](core-316-kubernetes-observability-diagnostics-evidence.md), [core-317](core-317-kubernetes-updates-migration-recovery.md)  
**Required by:** [core-319](core-319-kubernetes-production-hardening-conformance.md), [core-320](core-320-acceptance-complete-kubernetes-support.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#318](https://github.com/mcpdev80/baseharbor/issues/318)
<!-- /generated:links -->

## Goal

Make Kubernetes as usable through BaseHarbor by humans and generic coding agents as the Compose reference runtime.

The user or agent should not need Kubernetes expertise for normal BaseHarbor operations.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Agent-native parity

The BaseHarbor MCP/JSON control surface frozen in v0.5 must cover the complete supported Kubernetes lifecycle through the same semantic operations.

A generic coding agent must be able to:

```text
discover
inspect
plan
preflight
apply/up
status
doctor
diagnose
update
backup
restore
drift/repair
destroy
```

where those operations are supported.

No generic shell/kubectl/Helm execution tool is added to MCP.

### Safety

Machine operations preserve:

- read-only/mutating/destructive classification;
- confirmation/approval semantics;
- target identity validation;
- policy;
- ownership;
- secret safety;
- preflight;
- verification;
- evidence.

### Human DX

The normal human path remains sparse and runtime-neutral.

BaseHarbor should translate Kubernetes failures into actionable BaseHarbor concepts first, while preserving technical detail for diagnosis.

Examples:

- missing permission -> operation/resource/feature;
- admission rejection -> platform policy;
- route rejected -> exposure unavailable;
- image pull failure -> artifact/runtime verification;
- unsatisfied guarantee -> requested guarantee + missing evidence/capability.

### No Kubernetes questionnaire

Do not force users to understand or supply Kubernetes-specific fields in portable application intent.

Advanced deployment/operator configuration remains available outside the app contract.

### BaseHarbor-first tool experience

The normal human or agent workflow operates BaseHarbor, not the underlying implementation tools.

Users/agents should not need normal-path commands such as:

- `kubectl`;
- `argocd`;
- Flux-specific CLIs;
- Helm;
- provider-native infrastructure CLIs.

`baha`, JSON and MCP remain the primary lifecycle surfaces.

Native UIs/CLIs remain available to platform engineers and experts for drill-down, administration and troubleshooting. BaseHarbor hides operational complexity, not operational capability.

## Acceptance

- Generic coding agent completes the full supported Kubernetes lifecycle through MCP/JSON.
- No raw kubectl/Helm/shell fallback is required for normal BaseHarbor operations.
- Safety/confirmation semantics match human CLI behavior.
- Target mismatch and destructive actions fail closed.
- Machine output remains secret-safe.
- Human errors are actionable BaseHarbor-first diagnostics.
- Portable application configuration remains sparse and runtime-neutral.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-313, core-315, core-316, core-317.

## Handoff

- Not started (future release).
