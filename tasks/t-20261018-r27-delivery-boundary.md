---
id: t-20261018-r27-delivery-boundary
card_number: "0427-025"
card_short_title: "map native standards and one"
areas: [architecture]
type: architecture
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: w2-delivery (lane)
kanban_lane: closed
kanban_summary: "Start from existing direct/delegated Selection, OwnerBaseHarbor/OwnerExternal, revision and provenance. Map OCI…"
kanban_status: closed
kanban_title: "0427-025 · map native standards and one"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1333"]
sources: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1333q.md","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1333r.md","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/merge-1333.md"]
---

- [x] t-20261018-r27-delivery-boundary · Delivery: map native standards and one reconciliation owner #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** w2-delivery (lane) · **Priority:** critical  
    **PR:** [baseharbor#1333](https://github.com/mcpdev80/baseharbor/pull/1333)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1333q.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1333r.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/merge-1333.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md)  
**Required by:** [core-325](core-325-delivery-delegated-deployment-gitops.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-promote](t-20261018-r27-promote.md)  
**Owner:** w2-delivery (lane)  
**Priority:** critical  
**PRs:** [baseharbor#1333](https://github.com/mcpdev80/baseharbor/pull/1333)  
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

### Coordinator ownership decision (2026-11-03, night wave)

For the one-writer production guard (acceptance clause 1) the lane may make the minimal
integration edit in internal/deployment/deployment_store.go at SaveDeploymentRecord (read-only check
hook + one regression test file); all other files in internal/deployment stay read-only. Shared decision
indexes remain owned by public-surfaces per card; decision/index.md entries for ADR 0022 are allowed as
navigation-only additions. Recorded here per card rule update dependencies/ownership before work.

### Coordinator scope decision on one-writer depth (2026-11-03, night wave)

In-scope for THIS card now: (a) fix the serialization bypass — persist the guarded/canonical
owner (guardRecord), never the raw caller record, carry prior Conflict into the guard, and assert
unchanged stored bytes on every rejection; (b) honest EN/DE scope text. The authoritative ACTIVE-
reconciler observation (cross-process read/check/write lock around the real apply/observe path)
DEPENDS on t-20261018-r27-state-owner + t-20261018-r27-authority-contract, not yet accepted; it is
an EXPLICIT deferred dependency named in the spec, not a silent claim. Full enforcement is
re-qualified when those predecessors accept.

### Coordinator note on regression file scope (2026-11-03, r1333f)

The authorized 'one regression file' for the store hook covers focused regression files for the
guard behaviour, including preferences_retention_test.go alongside one_writer_guard_test.go, as long
as each file tests only the authorized SaveDeploymentRecord seam. Recorded; not a licence for broader
internal/deployment edits.

### Coordinator acceptance note (2026-11-03, r1333q)

CODEX-REVIEW verdict on head 337ed4ee: **ACCEPT-WITH-DEFERRAL** (evidence/r27-night-2026-11-02/review-1333q.md).
Deferral: live reconciler detection and cross-process runtime lock -> authority-contract + state-owner
cards (recorded there as of 2026-11-02/03). Merge via CODEX-MERGE in flight; card closes on merge proof.
