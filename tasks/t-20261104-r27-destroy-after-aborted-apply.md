---
id: t-20261104-r27-destroy-after-aborted-apply
type: task
areas: [deployment]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w154)
kanban_status: active
kanban_lane: active
kanban_summary: app destroy --yes ends with success and leaves no running instance and no project ownership when a provider-change apply aborted…
kanban_title: "Deployment: destroy must succeed when a provider-change apply aborted before runtime materialization"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-consent-abort-leaves-undestroyable-state]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md]
---

- [ ] t-20261104-r27-destroy-after-aborted-apply · Deployment: destroy must succeed when a provider-change apply aborted before runtime materialization #task #release/v0-4-27 #status/active #view/active #area/deployment #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w154) · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-consent-abort-leaves-undestroyable-state](t-20261104-r27-consent-abort-leaves-undestroyable-state.md)  
**Owner:** coord-welle4 (Lane w154)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`app destroy --yes` ends with success and leaves no running instance and no project ownership when a
provider-change apply aborted midway — i.e. `deployment.json` exists with an applied record
(`last_applied_ref` set) but the stage runtime environment (`state/<stage>/runtime/runtime.env`) was never
materialized. Today destroy fails there with an unhelpful missing-file error, so the deployment becomes
undestroyable through the normal path.

## Scope

- In scope: the destroy path's handling of a partially-applied provider change (intent applied, runtime
  materialization missing); a regression proving red-on-develop, green-on-candidate.
- Out of scope: the impact-confirmation UX itself (two confirmations for a provider change is intended);
  the consent gate (blob-identical, fail-closed, unchanged); the never-delivered case already fixed by
  `t-20261104-r27-consent-abort-leaves-undestroyable-state` (that cell lacked deployment.json entirely).

## Measured reproduction (2026-11-04, VM lane w150, host baha-docker rebuilt from develop ea3fb38e;
full transcript: [rebuild-1.md](../evidence/r27-welle4-2026-11-04/vm-integration/rebuild-1.md))

- `baha target create` → `app init --yes` rc=0 → `app apply --no-input` rc=1 with
  "provider change: impact-confirmation-required (2 confirmations, --yes gives 1)".
- Afterwards `deployment.json` present with applied intent/runtime provider/delivery/generated state and
  `last_applied_ref` recorded; `state/r27-w150-demo/runtime/runtime.env` absent.
- `baha app destroy --yes` rc=1: "read application runtime environment: open .../runtime/runtime.env: no
  such file or directory". Phase: DESTROY, after passing all preflight checks.

## Acceptance

- Destroy in the state shape above returns success without manual cleanup between steps.
- After destroy: no running instance and no ownership of the project remain (list, not assertion).
- A never-delivered application (no last_applied_ref) and the normal apply+destroy path behave exactly as
  before (regression or untouched-path test each).
- The consent gate remains fail-closed and unmodified (blob comparison).
- Red-first is measured: the new regression fails on develop ea3fb38e (name the commit and show output)
  and passes on the candidate.

## Required checks

- Targeted: `go test ./cmd/baha ./internal/deployment -count=1` with the shared database script pairing;
  build, vet, gofmt.
- Hosted runs of the exact head to terminal state.
