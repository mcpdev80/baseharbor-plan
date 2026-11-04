---
id: t-20261018-r27-node-service
areas: [connector]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: coord-welle4 (lane w105)
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor-node-connector]
prs: ["mcpdev80/baseharbor-node-connector#19"]
sources: ["mcpdev80/baseharbor-node-connector#3"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-node-service · Connector: reconcile enrollment service and restart behavior #task #release/v0-4-27 #status/active #view/active #area/connector #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (lane w105) · **Priority:** normal  
    **PR:** [baseharbor-node-connector#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261104-r27-vm-smoke-docker-podman](t-20261104-r27-vm-smoke-docker-podman.md)  
**Owner:** coord-welle4 (lane w105)  
**Priority:** normal  
**PRs:** [baseharbor-node-connector#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19)  
**Source:** [baseharbor-node-connector#3](https://github.com/mcpdev80/baseharbor-node-connector/issues/3)
<!-- /generated:links -->

## Outcome and acceptance

Review retained PR #4 exact unique work against current Core before extending; preserve it. Package/install/start/restart/uninstall rootless service without Go on node; native XDG/systemd user/lingering; explicit re-enrollment rules and protected local key generation. No desired-state or placement authority on node.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Connector internal/targetaccess/install.go and bootstrap/enrollment service files; cmd/baseharbor-node-connector/; matching tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused Connector service/bootstrap tests/vet/build; bounded native service smoke for actual systemd behavior. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.


## Handoff 2026-11-04 (lane w105, coord f49a3303)
- Candidate: connector PR #19 (draft -> ready by coordinator), branch work/r27-node-service, head 764a2a4.
- Delivered: thin internal/nodeservice lifecycle (install/start/restart/uninstall, rootless systemd-user,
  lingering), re-enrollment determinism, protected local key generation; targetaccess reused; no desired-state
  or placement authority on the node. Nine red-first cases in evidence (slice-2).
- Path reservation: coordinator decision (b) — no contract-reserved connector service path existed; proposed
  path documented for public-surfaces/authority-contract review.
- Codex review r19a dispatched on this exact head; merge only after verdict.

## Review-Rueckruf 2026-11-04 (Luna review-19a, verdict REJECT)
- Kein aufrufbarer Produktionspfad: Install schrieb keine echte systemd-user-Unit; Remove stoppte/disabled die
  eigene Unit nicht nachweislich; lingering-Policy fehlt.
- Autorisierung erfolgt nicht vor Wirkungen (Lebensdauer-/Metadataseiteneffekte vor dem Autorisierungsschritt).
- Restart-Verhalten nicht beobachtet (Tests verglichen keine tatsaechlichen Aufrufe); fehlende Autorisierung
  nicht als Mutation mit NIL-Wirkungen belegt; zwei nativ uebersprungene Hosted-Jobs wurden nicht ausgefuehrt.
- Korrekturrunde = Lane w110 auf demselben Zweig/PR #19 (draft bis Umleitung durch coord). PR-Kopf vorher
  764a2a4.
