---
id: t-20261018-r27-delivery-boundary
areas: [architecture]
type: architecture
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-delivery-boundary · Delivery: map native standards and one reconciliation owner #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md)  
**Required by:** [core-325](core-325-delivery-delegated-deployment-gitops.md), [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-promote](t-20261018-r27-promote.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Start from existing direct/delegated Selection, OwnerBaseHarbor/OwnerExternal, revision and provenance. Map OCI Image/Distribution and image-layout, Docker Compose, Podman Quadlet/systemd, Kubernetes/OpenShift native APIs, Git/Helm/Kustomize and existing CI/GitOps as applicable. No universal bundle, deployment package, stage DSL, builder, registry server, scheduler, approval or pipeline engine. Identify adopted standards, narrow unavoidable Baha extensions and required tool feature/version checks. One writer per resource: delegated desired state stays in Git/external delivery; Baha retains only its own bindings/operation receipts and observations. Direct mode remains available without GitOps. Deliver minimal typed owner/selection checks and contract fixtures, not Kubernetes implementation.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

internal/delivery/contract.go and focused tests; docs/spec/delivery-provider-v1.md and DE counterpart (reuse existing document if present); one product ADR. Reserved paths for this slice only; proposed filenames are fixed in the accepted contract predecessor before assignment. Shared command/HTTP/MCP/help/golden registrations belong to public-surfaces. If another write owner is needed, coordinate and serialize before implementation; no branch-to-branch dependencies or duplicate state.

## Required checks

Focused delivery contract and delegated-owner denial fixtures; docs/link/EN-DE; no native runtime. Use existing trusted contract/docs/package checks for this prerequisite; acceptance must not wait on downstream ci-lanes. Any genuinely missing contract-check route is resolved explicitly before assignment, without self-exemption. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.
