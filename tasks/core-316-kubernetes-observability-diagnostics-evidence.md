---
id: core-316
type: feature
release: v0.8.x
version: v0.8.3
parent: v0.8.x
owner: ""
depends_on: [core-313, core-314]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#316"]
source_updated: "2026-10-15T16:52:42Z"
labels: [kind/feature, area/evidence, area/observability, area/kubernetes]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-316 · Kubernetes: add observability, diagnostics and evidence #task #release/v0-8-x #status/planned #view/waiting
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.3)  
**Depends on:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md)  
**Required by:** [core-318](core-318-kubernetes-cli-agent-developer-parity.md), [core-319](core-319-kubernetes-production-hardening-conformance.md), [core-320](core-320-acceptance-complete-kubernetes-support.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#316](https://github.com/mcpdev80/baseharbor/issues/316)
<!-- /generated:links -->

## Goal

Complete Kubernetes observability and diagnostic behavior so BaseHarbor can explain application/runtime health without requiring raw Kubernetes tooling for normal operation.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Semantic observability

BaseHarbor must expose the same portable categories:

- status/health;
- readiness/verification;
- logs where supported;
- metrics;
- traces/OTLP;
- provider diagnostics;
- drift/conflict;
- audit/evidence.

Kubernetes resources/events are implementation evidence, not the user-facing semantic model.

### Namespaced diagnostics

Normal diagnostics must work with namespace-only permissions.

Optional access to Events or broader cluster data may enrich diagnostics but must not be mandatory for the basic lifecycle.

When data cannot be read because of permissions:

- report diagnostic visibility as limited;
- do not turn limited diagnostics into application failure;
- do not request broader rights silently.

### Observability provider placement

Metrics/logs/traces must preserve:

```text
application
shared
external
```

where supported.

BaseHarbor must not force a Kubernetes-local Prometheus/Loki/Tempo stack when the deployment uses platform or external observability.

### Evidence

Evidence must distinguish:

- desired;
- applied;
- observed;
- verified;
- unsupported/unverifiable;
- platform/admission mutation;
- provider state.

Keep audit/evidence separate from telemetry.

### Developer/agent experience

`baha status`, `doctor` and machine/MCP diagnostics should answer the useful BaseHarbor question first and include Kubernetes detail only as drill-down evidence.

### Existing observability mechanisms

Prefer consuming/reusing existing platform or provider observability when it satisfies the BaseHarbor contract instead of deploying a duplicate BaseHarbor-owned monitoring stack.

Prometheus, Loki, Tempo, platform monitoring or future ecosystem integrations remain provider realizations, not portable application semantics.

## Acceptance

- Normal Kubernetes diagnostics work with namespace-only permissions.
- Optional Event/cluster visibility enriches but does not gate the lifecycle.
- Metrics/logs/traces preserve provider-placement semantics.
- BaseHarbor does not force its own monitoring stack.
- Desired/applied/observed/verified states remain distinct.
- Admission mutations and SSA conflicts are represented accurately.
- Audit/evidence remains separate from telemetry.
- CLI/JSON/MCP expose equivalent diagnostic truth.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-313, core-314.

## Handoff

- Not started (future release).
