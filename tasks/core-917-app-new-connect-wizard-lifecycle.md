---
id: core-917
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-917 New wiring)"
depends_on: [core-916]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#975]
sources: ["mcpdev80/baseharbor#917"]
source_updated: "2026-10-15T16:46:23Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-917 · App new: connect the compact wizard to the existing lifecycle #task #release/v0-4-26 #status/active #view/active #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-917 New wiring) · **Priority:** not set  
    **PR:** [baseharbor#975](https://github.com/mcpdev80/baseharbor/pull/975)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** mcpdev80 (core-917 New wiring)  
**Priority:** not set  
**PRs:** [baseharbor#975](https://github.com/mcpdev80/baseharbor/pull/975)  
**Source:** [baseharbor#917](https://github.com/mcpdev80/baseharbor/issues/917)
<!-- /generated:links -->

## Goal

`baha app new` uses the new flow with the existing source/ID/provider/lifecycle owners. Lane: wiring New.

## Scope

- In scope: `cmd/baha/app_new.go`, `app_new_wizard.go` and their dedicated tests.
- Out of scope: command registry/help/goldens (core-921); no side refactor of `app_init_selection.go`.

## Acceptance

- Writes sparse capability intent and Target preference into the correct existing owners only after valid consent; no new configuration file or manual ID.
- Consumes the existing authorized plan/preflight/confirm/apply/verify path; the user can clearly tell create-only from run intent; no silent start on create.
- When prerequisites change, the plan/consent is refreshed instead of executing an old plan blindly; partial failures use the shared presenter; repeated runs respect the existing identity.

## Required checks

- Targeted New/lifecycle adapter tests; then one small necessary native create path on the actually affected runtimes, not the whole provider matrix.

## Dependencies and file ownership

- Depends on core-916. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** Existing `cmd/baha/app_new.go`, `app_new_wizard.go` and their matching dedicated tests only.
- **Delivered interface/result:** Wire the accepted controller to the existing New authorities; deliver a compiling callable command/handler without editing the central registration owned by core-921.
- **Task-specific proof:** `TestAppNewWizard*`/existing New adapter tests for create-only, consent, stale plan, no-input and idempotence; execute only the existing targeted native create gates justified by the actual runtime diff.
- **Boundary:** No `app_init_selection.go`, root routing/registries, edit files, shared presenters or lifecycle implementation. Required native gate selection/execution must be available before assignment; this session owns running and diagnosing it.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent Maintainer CI-discipline finding: [PR #975 process comment](https://github.com/mcpdev80/baseharbor/pull/975) at source `6f5e03cb22a404a396354df9c637ee001598e823` records 11 PR runs between 15:27Z and 15:54Z, nine cancelled. Commit history includes separate implementation/test pushes 39 seconds apart and repeated separate formatting pushes; no urgent supersession explanation was present in PR comments. Existing AGENTS CI execution discipline was not followed. Stop candidate pushes until current results are inspected; batch demonstrated source/test/formatting fixes into one coherent prechecked candidate. If local tooling is unavailable, obtain a bounded isolated complete formatting/compile precheck rather than using native PR CI as a per-file debugging loop. Do not disable required checks/concurrency, use ci.skip or launch extra runtime gates. No current run cancellation requested. Preserve current execution evidence, record the diagnosed causes and only rerun for relevant changed inputs. This is process correction during existing core-917, not code acceptance or a new assignment.

- 2026-10-16 implementation checkpoint (not a review handoff): [Draft product PR #975](https://github.com/mcpdev80/baseharbor/pull/975), branch `feature/core-917-new-lifecycle-wiring`. Scope only `cmd/baha/app_new_wizard.go` and matching dedicated tests. The existing create-only wizard now explicitly says no container/deployment start, pins one generated ApplicationID across Bootstrap preview and Create, and revalidates authoritative Bootstrap manifest/plan/files after confirmation before writing; context cancellation and EOF are tested.
- A separate callable `appNewCreateFromWizardDecision` adapter accepts only an actually confirmed, current `appWizardController` decision and delegates to existing `development.BootstrapApplication/CreateApplication`. It rejects mismatched portable requirements and explicit Target provider preferences that this source-only creation API cannot persist, rather than silently losing them. Dedicated positive/negative unit tests added.
- **NOT YET QUALIFIED:** The interactive user-facing `runAppNewWizard` still uses its original capability prompts; the accepted controller is not yet fully driven from real Target read-only authorities and the existing provider lifecycle path. There is no complete Target-preference persistence or native partial-result presentation. Do not accept or merge this partial draft. Focused CI and exact selected Docker/Podman lifecycle evidence are still being evaluated on the latest candidate; earlier runs include an actual successful Docker gate but not final exact acceptance.
- No registry, Edit, shared Domain, workflow or release-matrix changes. Preserve subsequent concurrent planning updates. Continue core-917 only until these remaining acceptance boundaries are implemented and independently reviewed.



The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
