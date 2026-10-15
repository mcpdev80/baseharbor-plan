---
id: core-308
type: feature
release: v0.7.x
version: v0.7.5
parent: v0.7.x
owner: ""
depends_on: [core-102, core-304, core-306, core-307]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#308"]
source_updated: "2026-10-15T16:53:20Z"
labels: [kind/feature, area/kubernetes, area/availability]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-308 · Kubernetes: implement availability guarantees #task #release/v0-7-x #status/planned #view/waiting
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-307](core-307-kubernetes-stateful-workloads.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.5)  
**Depends on:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-307](core-307-kubernetes-stateful-workloads.md)  
**Required by:** [core-309](core-309-tests-kubernetes-restricted-permissions.md), [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#308](https://github.com/mcpdev80/baseharbor/issues/308)
<!-- /generated:links -->

## Goal

Realize v0.6 availability guarantees on Kubernetes without requiring cluster-wide privileges that a namespace-only user normally does not have.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Principle

```text
requested portable guarantee
        ↓
available deployment/platform facts
        ↓
runtime realization
        ↓
verification confidence
```

BaseHarbor must distinguish:

- satisfied;
- unsupported;
- unverifiable with current permissions/platform facts.

Do not silently convert `unverifiable` to success.

### Realization

Use Kubernetes primitives only as runtime implementation details, for example where required:

- replicas;
- topology spread;
- anti-affinity;
- PDB;
- rollout strategy.

These remain outside portable application intent.

### Namespace-only challenge

A namespace-only user may not be allowed to list Nodes or inspect cluster topology.

Therefore BaseHarbor must not make cluster-wide topology discovery mandatory for normal deployment.

For guarantees requiring cluster facts:

1. use platform-provided deployment facts/policy if available;
2. use namespaced observable evidence where sufficient;
3. otherwise report the specific guarantee as unverifiable/unsupported.

Example:

```text
requested: host failure tolerance
node visibility: unavailable
platform topology assertion: none

result:
  guarantee not verifiable
  deployment blocked if guarantee is required
```

### No fake HA

Multiple replicas do not prove node/failure-domain redundancy.

BaseHarbor must not claim host/failure-domain tolerance without sufficient evidence.

### Runtime vs capability providers

Capability-provider HA remains independent from workload runtime HA.

An external managed PostgreSQL provider may satisfy its own guarantee even when workload topology cannot be fully verified.

### Kubernetes primitive limitations

Kubernetes primitives are evidence/mechanisms, not guarantees by themselves.

In particular:

- a PodDisruptionBudget governs voluntary disruptions; it does not prove workload availability against node or zone failure;
- replica count does not prove failure-domain separation;
- topology constraints only contribute to a guarantee when the required topology information and resulting placement can be verified;
- rollout strategy does not by itself prove service continuity.

BaseHarbor verification must evaluate the requested portable guarantee, not merely the presence of these objects.

## Acceptance

- v0.6 guarantees map to Kubernetes without changing portable intent.
- Namespace-only operation remains supported.
- Node/cluster-wide read is not required unless needed to verify a requested guarantee.
- Missing topology visibility becomes explicit unverifiable/unsupported state.
- Required unverifiable guarantees fail closed before mutation.
- Multiple replicas alone never prove host/failure-domain tolerance.
- Runtime and capability-provider guarantees remain independent.
- CLI/JSON/MCP expose the same guarantee state.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-102, core-304, core-306, core-307. Satisfied (closed in v0.4.21): #103, #301, #302, #303.

## Handoff

- Not started (future release).
