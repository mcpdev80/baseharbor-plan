---
id: t-20261125-hunt47-deployment-record-v1-wall
card_number: "0428-356"
card_short_title: "deployment v1 record wall"
type: bug
areas: [cli, deployment]
release: v0.4.28
version: ""
parent: ""
owner: w193-0428-224-hunt-v47-intake
kanban_status: planned
kanban_lane: ready
kanban_summary: An operator holding a pre-stable-identity (version-1) deployment record has either a working migrate-at-load path or a supported…
kanban_title: 0428-356 · deployment v1 record wall
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/blob/develop/internal/deployment/deployment_store.go
---

- [ ] t-20261125-hunt47-deployment-record-v1-wall · 0428 hunt H-V47: deployment-record v1 records dead-end — unloadable, unlistable for removal, remedy binary refused by downgrade gate #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** w193-0428-224-hunt-v47-intake · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/develop/internal/deployment/deployment_store.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261125-hunt47-destroystep-v1-warning-kind](t-20261125-hunt47-destroystep-v1-warning-kind.md)  
**Owner:** w193-0428-224-hunt-v47-intake  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Summary

An operator holding a pre-stable-identity (version-1) deployment record has either a working migrate-at-load path or a supported command to inspect/remove that deployment's state — not a manual delete of protected state.

## Scope

- In scope:
  - `internal/deployment/deployment_store.go:661-670` (load gate: any `record.Version != 2` → `deployable_version_mismatch`), the save refusal (`:418-423`) and the drift text `internal/deployment/deployment_identity_drift.go:51-52` ("do not remove a record whose storage version is unsupported").
  - CLI translation `cmd/baha/app_context.go:452-463`: the next-action "Run the same or a newer BaseHarbor that wrote this deployment's state" contradicts `cmd/baha/update_mutation.go:43-45` which refuses to obtain/downgrade to that binary.
  - `docs/spec/candidate-contract-v1.md:92-94` promises "existing deployment records written before this field existed remain loadable" — decide and align with the gate.
- Out of scope:
  - provider-registry v1 (0428-341), destroy --all skip semantics for these records (0428-343), generic version-gate message direction (0428-345).

## Acceptance

- One of: (a) migrate-at-load projects v1 records (name-only identity → UUID identity per the 0427-149 uniqueness rules) preserving the deployment directory, or (b) a supported, tested removal/inspection route for `deployable_version_mismatch` records exists (uuid-addressed destroy or an explicit recovery command) and the next-action names it.
- The chosen contract is asserted by an existing-seam test (the `w200_deployment_version_mismatch_*` family already pins fail-closed status/destroy messages; extend rather than replace) and reflected in the candidate-contract spec text.

## Required checks

- **Modified features:** `internal/deployment` listing/load suites (`w200_deployment_version_mismatch_deploy_test.go`, `deployment_owner_binding_test.go`) and the `cmd/baha` status/destroy version-mismatch tests stay green; add the chosen-path regression.
- **New tests:** named test in `internal/deployment` (e.g. `TestLoadDeploymentRecordMigratesV1Projection` or `TestDestroyRemovesVersionMismatchedRecord`); normal auto-discovered Go tests, selected by the standard unit lane.
- **CI integration and mapping:** no `.github/**` change; package selection already routes internal/deployment and cmd/baha changes into the Go unit lane via scripts/pr-gate-plan.py.
- **Mapping selection proof:** record the plan artifact selecting the unit lane for the touched paths.
- **Hard acceptance gate:** exact SHA -> test ID -> mapped check -> run URL.

## Dependencies and file ownership

- Owned files or areas: `internal/deployment/deployment_store.go`, `deployment_list.go`, `deployment_identity_drift.go`, `cmd/baha/app_context.go` (translation only), `docs/spec/candidate-contract-v1.md`.
- Shared files: 0428-343 consumes the SAME `deployable_version_mismatch` kind on the destroy-all path; coordinate the kind's shape once here.

## Handoff

- Cast from hunt H-V47 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/`, origin/main 59a288736, anchor develop 99d9ddebc). BF-47-2 LIVE at intake, confirmed at 99d9ddebc: the gate (`deployment_store.go:661-670`) still refuses every version != 2, no migrate-at-load exists, the save seam refuses foreign versions, and the CLI next-action still routes operators to a binary the self-update downgrade gate forbids. Intake unit witness: a genuine v1 record (name-only identity) listed via `listAllDeployments` yields exactly one `deployable_version_mismatch` warning and ZERO records — invisible to every name/uuid-addressed path in the current binary.
- Current state, branch, PR and evidence links. Newest first.
