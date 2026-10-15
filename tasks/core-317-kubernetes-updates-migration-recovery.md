---
id: core-317
type: feature
release: v0.8.x
version: v0.8.4
parent: v0.8.x
owner: ""
depends_on: [core-313, core-314, core-315]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#317"]
source_updated: "2026-10-15T16:52:35Z"
labels: [kind/feature, area/recovery, area/kubernetes, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-317 · Kubernetes: secure updates, migration and recovery #task #release/v0-8-x #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.4)  
**Depends on:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md), [core-315](core-315-kubernetes-backup-disaster-recovery.md)  
**Required by:** [core-318](core-318-kubernetes-cli-agent-developer-parity.md), [core-319](core-319-kubernetes-production-hardening-conformance.md), [core-320](core-320-acceptance-complete-kubernetes-support.md)  
**Owner:** unassigned  
**PRs:** none  
**Source:** [baseharbor#317](https://github.com/mcpdev80/baseharbor/issues/317)
<!-- /generated:links -->

## Goal

Make application/provider updates and BaseHarbor state migrations safe and predictable on Kubernetes using the compatibility rules frozen in v0.5.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Update model

```text
current observed state
 -> compatibility preflight
 -> recovery point where required
 -> plan
 -> apply/update
 -> reconcile
 -> verify
 -> READY or actionable recovery state
```

### Scope

Where supported by BaseHarbor today, cover:

- application image/config updates;
- runtime object changes;
- capability-provider updates;
- BaseHarbor deployment/runtime state migrations;
- binding migrations;
- safe replacement/recreation;
- recovery after partial failure;
- deprecation/canonical-writer behavior.

### Kubernetes-specific realization

Kubernetes rollout mechanisms may be used, but BaseHarbor success is based on the application/capability semantic result.

Do not equate:

```text
Deployment rollout complete
=
BaseHarbor update verified
```

### Immutable/recreate-sensitive fields

Preflight must recognize changes that require replacement or have data/identity consequences.

Do not delete/recreate persistent or provider-owned resources blindly.

### Recovery

- preserve last verified state/recovery information where needed;
- rollback only when technically safe;
- otherwise provide explicit recovery flow;
- foreign/platform-owned resources are never rolled back/mutated as if BaseHarbor owned them.

### Namespace-only

Updates/migrations must not introduce cluster-admin requirements unless the specific selected provider/platform operation genuinely requires them.

### Delivery-aware update semantics

Update/recovery must distinguish who owns reconciliation:

- direct delivery: BaseHarbor performs the runtime update;
- delegated delivery: BaseHarbor produces/requests the desired revision, the Delivery Provider/external reconciler performs runtime reconciliation, and BaseHarbor observes plus semantically verifies the result.

BaseHarbor must not bypass a delegated reconciler by directly mutating the same owned resource set during normal update/recovery.

## Acceptance

- Application updates use preflight -> apply -> verify semantics.
- Kubernetes rollout status alone is not treated as semantic success.
- Provider/runtime state migrations follow v0.5 compatibility rules.
- Replacement-sensitive resources are detected before destructive change.
- Recovery/rollback preserves ownership and durable data safety.
- Namespace-only remains the normal access profile.
- CLI/JSON/MCP expose the same update/recovery state.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-313, core-314, core-315.

## Handoff

- Not started (future release).
