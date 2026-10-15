---
id: core-817
areas: [platform]
type: acceptance
release: v0.4.29
version: ""
parent: v0.4.29
owner: ""
depends_on: [core-823]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#817"]
source_updated: "2026-10-15T16:50:49Z"
labels: [kind/acceptance, area/evidence, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-817 · Audit: verify host portability and architecture #task #release/v0-4-29 #status/planned #view/waiting #area/platform #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-823](core-823-tests-platform-conformance-support.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Depends on:** [core-823](core-823-tests-platform-conformance-support.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#817](https://github.com/mcpdev80/baseharbor/issues/817)
<!-- /generated:links -->

## Goal

Audit the actual v0.4.29 host-platform implementations before final contract acceptance in v0.4.31 (#174). Passing the audit alone neither implements a platform nor promotes its support level. Related: #805, #175, #603, #777.

## Scope

- [v0.4.29](../releases/v0.4.29.md) is the authoritative delivery scope.
- Boundaries: portable Application Intent, Target/Access, Runtime/Capability Provider and lifecycle/result semantics stay platform-neutral; host/runtime mechanisms stay behind their boundaries. Review at least resource/memory/VM limits, state/config/filesystem ownership, trust/certificates, secure ephemeral material, PTY/terminal, runtime/socket discovery, process/service managers, networking/localhost/browser routes, architecture compatibility and install/update artifact selection. Linux `/proc`, cgroups, systemd/systemctl, trust-store paths, socket paths and ioctls must not become portable semantics. WSL2 is Linux execution, distinct from native Windows. Darwin containers run in a Linux VM; Quadlet/systemd are Podman implementation details.
- D1–D5 review: **D1** endpoint → owned running VM provenance, privilege/isolation distinction, safe file-sharing and socket boundaries; no implicit privileged-host fallback. **D2** source/environment binding, freshness, effective limits and measured/estimated/unknown evidence; physical RAM, MemTotal/MemFree or total-minus-container-stats cannot establish SAFE; plan/preflight neither probe-start nor mutate. **D3** the Podman Machine executor keeps Linux Quadlet semantics and ownership; no remote-exec/MCP escape. **D4** four distinct lanes with exact evidence. **D5** artifact/update selection keeps portable intent; ad-hoc signing ≠ Developer ID/notarization; clean-Mac installer/browser behavior honestly documented. D1/D2 need recorded contract review in the pinned spec before dependent implementation.

## Acceptance

- Every audited platform-specific call site belongs to an explicit host/runtime/Target boundary.
- Resource/trust/path/terminal result semantics remain portable; vendor mechanisms stay internal.
- D1/D2/D3 implementation and negative tests match the reviewed contract.
- Runtime/VM available capacity, overhead and limits are distinguished from physical-host totals and partial estimates.
- WSL2/native Windows and Darwin host/Linux runtime VM remain distinct.
- amd64/arm64 differences are artifact/runtime compatibility, not application intent.
- Linux regression, genuine WSL2 and both macOS arm64 engines have the required exact-source evidence and owned cleanup.
- The #805 EN/DE matrix matches actual per-combination evidence; no upgrade from audit/build success alone.
- core-885/core-886 deferred capabilities remain explicitly unclaimed in v0.4.29.
- Any discovered frozen Linux-only public semantic is fixed or explicitly reviewed before #174 closes.

## Required checks

- Review against source and evidence receipts; no new runtime matrix for the audit itself.

## Dependencies and file ownership

- Depends on core-823 (all implementation tasks).

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
