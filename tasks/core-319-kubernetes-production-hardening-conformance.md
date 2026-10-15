---
id: core-319
type: acceptance
release: v0.8.x
version: v0.8.6
parent: v0.8.x
owner: ""
depends_on: [core-313, core-314, core-315, core-316, core-317, core-318]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#319"]
source_updated: "2026-10-15T16:52:24Z"
labels: [kind/acceptance, area/runtime, area/security, area/kubernetes]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-319 · Kubernetes: verify production hardening and conformance #task #release/v0-8-x #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.6)  
**Depends on:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md), [core-315](core-315-kubernetes-backup-disaster-recovery.md), [core-316](core-316-kubernetes-observability-diagnostics-evidence.md), [core-317](core-317-kubernetes-updates-migration-recovery.md), [core-318](core-318-kubernetes-cli-agent-developer-parity.md)  
**Required by:** [core-320](core-320-acceptance-complete-kubernetes-support.md)  
**Owner:** unassigned  
**PRs:** none  
**Source:** [baseharbor#319](https://github.com/mcpdev80/baseharbor/issues/319)
<!-- /generated:links -->

## Goal

Harden the completed Kubernetes feature set across realistic restricted-cluster conditions before declaring Kubernetes first-class production-ready.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Conformance dimensions

Exercise the complete supported feature set against a deliberately small, evidence-based matrix covering:

##### Authorization

- namespace-only;
- platform-managed dependencies;
- optional broader admin/dev context;
- missing individual permissions.

##### Namespace ownership

- dedicated BaseHarbor-managed namespace where explicitly allowed;
- pre-provisioned platform-owned namespace;
- shared namespace containing unrelated workloads.

##### Admission/policy

- Pod Security restricted-compatible environment;
- mutating admission;
- validating admission/policy rejection;
- ResourceQuota/LimitRange.

##### Runtime/provider

- stateless workload;
- persistent workload;
- stateful path where supported;
- application/shared/external capability placement;
- private image pull reference.

##### Networking/exposure

- NetworkPolicy enforcement where available;
- platform-owned shared Gateway;
- cross-namespace trust where supported;
- external provider egress limitations.

##### Failure/recovery

- SSA field conflict;
- foreign-owned resource;
- finalizer;
- failed rollout/readiness;
- backup/restore failure;
- Target mismatch;
- partial update/recovery.

##### Kubernetes/API compatibility

Maintain the supported Kubernetes/API matrix from v0.7 and exercise the complete v0.8 surface on the declared supported range.

### Security review

Re-run the full BaseHarbor security invariants:

- least privilege;
- no privilege broadening for convenience;
- secret safety;
- workload/operator identity separation;
- ownership-safe destructive actions;
- platform-owned resource protection;
- no false isolation/availability claims.

### CI discipline

Keep validation economical.

Use local/repository/Hugging Face evidence first where practical and GitHub Actions only where necessary.

Do not create a giant version × CNI × CSI × Gateway-controller Cartesian matrix.

### Delivery conformance

Add delivery mode to the production conformance matrix:

```text
direct
delegated/GitOps
```

For delegated delivery cover at least:

- application/shared/external Delivery Provider placement where supported;
- no double reconciliation;
- foreign delivery resource ownership;
- desired revision mismatch;
- delivery provider unavailable;
- GitOps out-of-sync while runtime objects exist;
- GitOps reports synced but BaseHarbor semantic verification fails;
- safe destroy/update behavior through the declared reconciliation owner.

Do not create a Cartesian matrix across every GitOps implementation. One real reference provider plus contract-level conformance is sufficient.

## Acceptance

- Complete Kubernetes feature set passes the supported restricted-access matrix.
- Namespace-only remains a hard release gate.
- Shared namespace leaves unrelated resources untouched.
- Admission/Quota/SSA/finalizer failures are handled safely.
- Supported Kubernetes/API range is validated.
- Security review passes with no silent privilege broadening.
- Test evidence corresponds to the exact implementation head.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-313, core-314, core-315, core-316, core-317, core-318.

## Handoff

- Not started (future release).
