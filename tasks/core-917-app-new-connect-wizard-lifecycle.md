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
    **Owner:** mcpdev80 (core-917 New wiring)  
    **PR:** [baseharbor#975](https://github.com/mcpdev80/baseharbor/pull/975)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (core-917 New wiring)  
**Priority:** not set  
**PRs:** [baseharbor#975](https://github.com/mcpdev80/baseharbor/pull/975)  
**Source:** [baseharbor#917](https://github.com/mcpdev80/baseharbor/issues/917)
<!-- /generated:links -->

## Goal

`baha app new` uses the new flow with the existing source/ID/provider/lifecycle owners. Lane: wiring New.

## Scope

- In scope: `cmd/baha/app_new.go`, `app_new_wizard.go`, their dedicated tests, and the bounded authoritative preference integration authorized below.
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

- **Owned files:** Existing `cmd/baha/app_new.go`, `app_new_wizard.go` and their matching dedicated tests; additionally the bounded preference-owner paths below. These additional paths belong exclusively to this session for this repair, not core-918.
- **Delivered interface/result:** Wire the accepted controller to the existing New authorities; deliver a compiling callable command/handler without editing the central registration owned by core-921.
- **Task-specific proof:** `TestAppNewWizard*`/existing New adapter tests for create-only, consent, stale plan, no-input and idempotence; execute only the existing targeted native create gates justified by the actual runtime diff.
- **Boundary:** No `app_init_selection.go`, root routing/registries, edit files, shared presenters, or Apply execution/receipt files owned by core-918. The bounded existing preference-owner integration below is explicitly authorized. Required native gate selection/execution must be available; unresolved additional policy coverage requires independent qualification, never a self-exemption.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Bounded authoritative preference integration — Maintainer scope correction, 2026-10-17

Source inspection confirms that the accepted read-only `ProviderPreference` model is not a complete persistent execution authority. `PreviewReferenceProviderRegistryAt` / `ReconcileReferenceProviderRegistryAt` rebuild deployment bindings through `releaseManagedBindingsPreservingInstances` and provider-kind placements; `applicationLifecycleSnapshot` then derives its preferences from that reconstruction. Directly inserting a binding from the wizard or setting temporary placement environment variables does not preserve the confirmed exact selection. This missing connection is now explicitly part of core-917 rather than an assumed completed dependency.

- Preserve the existing task claim and PR #975. The same owner is authorized to deliver this bounded missing connection and the real checklist/No flow together; no new assignment is required.
- Additional owned production paths: `internal/application/provider_preferences.go` (if needed), `internal/application/provider_registry.go`, `cmd/baha/application_provider_preferences.go` (if needed), and minimal integration in `cmd/baha/app_core_requirement.go`. Matching focused tests are included. If the existing canonical deployment record needs a narrowly scoped typed preference field or accessor, minimal changes in `internal/deployment/deployment_store.go` and its tests are also authorized; preserve old record compatibility. Do not invent a parallel wizard configuration/state file, transaction framework or second resolver.
- Retain full Target + application identity + environment + requirement kind/name + provider kind/instance ID as desired deployment preference. Desired selection must be separate from applied/verified execution facts: create-only may retain preference after consent, but may not claim a runtime was created or bind a live consumer as if apply succeeded. Automatic versus explicit semantics and supported named instances must survive restart/reload.
- Make preview, registry reconciliation, lifecycle snapshot and subsequent normal app up consume the same existing authoritative selection. Validate missing/duplicate/foreign/Target-incompatible/stale choices before mutation; preserve unrelated applications, environments and requirements. Reconciliation must not silently replace the explicit selection with the canonical placement-generated ID. Preserve existing locking/authorization/retention rules and fail closed where a native owner cannot actually realize a selected instance.
- Required regressions: fresh create-only followed by a fresh read/later apply uses the selected non-default instance; two named requirements retain distinct choices; automatic reset, two Targets/environments, absent/foreign/incompatible instance, unknown/duplicate requirement, reconciliation repeat and existing record compatibility. Verify source remains provider-neutral and No/Cancel/stale consent do not write project/profile/preference state.
- The review finding about real repeated No remains independently implementable now. Complete the accepted selection/controller loop as part of this same task; do not stop at another inventory of open work.
- These new source paths are not automatically trusted CI coverage. Run sufficient focused package/contract tests and the necessary selected native cases, disclose any coverage-unresolved result and submit the concrete diff/evidence for independent policy qualification. Do not grant your own exception or claim scope authorization means acceptance.
- Do not edit `app_apply.go`, `app_apply_lifecycle.go`, `app_apply_result*`, `app_edit*`, shared workflows or registration. Those are outside this repair and overlap the separate Edit lane.

## Handoff

### 2026-10-17 — Maintainer implementation continuation

- The previous implementation session stopped without a new candidate after confirming the two open P1 findings. The current ChatGPT workspace now continues implementation exclusively on the existing core-917 claim and PR #975. Preserve its source/history; do not start competing New/preference-owner edits. The bounded preference paths remain core-917-owned; core-918 Apply/Edit/receipt files remain excluded.
- No new product qualification or acceptance is claimed by this continuation notice. Implementation, local checks and one coherent hosted candidate will follow; independent review remains required.

### 2026-10-17 — Confirmed persistence API gap; scope repaired

- The implementation owner correctly identified the missing persistent exact-preference interface. Independent inspection confirms the registry release/rebuild and lifecycle snapshot derivation; a raw RegistryStore write from New is not a supported substitute. The original assignment assumed a capability the accepted owner did not yet expose. The bounded owner integration above is authorized within the existing task/PR.
- No new product candidate, tests or merge are claimed by this scope correction. Prior green run 38987933827 remains exact-source evidence only. Keep the current claim and continue both P1 corrections to a complete review handoff.

### 2026-10-17 — Independent review: changes required, task not accepted

- Reviewed exact product source `3acbd42307e69bd36e1e0aba254d12402a943e4a` against trusted develop `beca492d36c0c625e1a68a7ca055f6685fc10fba`; product diff is confined to the two owned New wizard files. [Maintainer review 5555205396](https://github.com/mcpdev80/baseharbor/pull/975#pullrequestreview-5555205396) documents two remaining P1 findings. Preserve the current owner and continue the existing PR; no successor assignment or task acceptance.
- [Run 38987933827](https://github.com/mcpdev80/baseharbor/actions/runs/38987933827) genuinely passes the nine discovered New tests, CLI formatting/vet/build, source contracts, selected Docker/Podman lifecycle gates and authenticated final check for integration `06ef77f81de9dfa3b8747a9adbe25762bd418145`. Do not mislabel this run as failed, or as proof of untested behavior.
- **Actual controller interaction is incomplete:** the real entry retains the legacy comma-separated capability prompt and rejects an empty selection. At preview No it discards `Step(appWizardNo)` and returns; it cannot preserve and edit the checklist across repeated No. Wire the accepted compact selection/provider interaction through the actual input loop; add input-driven repeated-No, edit/re-preview, empty-selection and Cancel/EOF/no-write regressions.
- **Explicit Target preferences are not retained:** `withAppNewTargetPreferences` reduces full requirement/instance choices to provider-kind placement environment values, which do not identify the selected registry instance. `appNewCreateFromWizardDecision` does not persist the choices; create-only returns before any temporary preference application. Connect the existing authoritative Target/deployment preference owner, retaining full Target, requirement kind/name, provider kind and instance ID through subsequent resolution. Prove a non-default selected instance, two named requirements, Target isolation, create-only then later resolution, and rejection of stale choices before writes. Temporary environment restoration tests do not establish persistence or exact instance selection. Identify a concrete missing owner API if the accepted authorities cannot deliver this, rather than substituting a second preference store or claiming placement equivalence.
- The author's completed-implementation handoff below is superseded on these acceptance claims. No product merge, no task acceptance or core-921 readiness. Batch the complete demonstrated corrections and tests before the next coherent candidate; inspect its targeted CI before another push. No full release matrix or core-918 changes.

- 2026-10-17 **completed implementation / independent review handoff** for [PR #975](https://github.com/mcpdev80/baseharbor/pull/975) at exact product HEAD `3acbd42307e69bd36e1e0aba254d12402a943e4a` (base `beca492d36c0c625e1a68a7ca055f6685fc10fba`, including accepted dependency PR #979). Only owned `cmd/baha/app_new_wizard.go` and `cmd/baha/app_new_wizard_test.go` differ from develop. Real interactive New enters the accepted controller, reads existing Target/footprint/impact authorities, shows a consent preview, preserves named capability requirements and stable application identity, and delegates creation to the existing project authority. Explicit Target preference selection remains separate from portable repository intent. Create-only never starts runtime; run delegates to the existing authorized lifecycle and reports created-project/failed-runtime partial results. No/Cancel/EOF write no project/profile; stale previews trigger fresh projection and consent. Regression fixtures now drive the actual input prompts to mode/consent instead of assuming a fixed count of provider prompts; full known gofmt corrections included. [Final CI run 38987933827](https://github.com/mcpdev80/baseharbor/actions/runs/38987933827): `wizard-app-new-tests`, `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, `PR Exact Candidate`, `PR Runner Interface`, `PR Demo Pin`, `PR Focused Python`, Docker lifecycle, Podman lifecycle, and binding `PR Selected Checks` all **SUCCESS**. Earlier run 38987439234 had both native gates successful but New-test fixture failures; its failure is historical, not final qualification. No self-merge and no successor task; **ready for independent review only**, not Maintainer accepted.


- 2026-10-17 dependency repair integrated: [t-20261017-provider-projection-workload](t-20261017-provider-projection-workload.md), [PR #979](https://github.com/mcpdev80/baseharbor/pull/979), is accepted and merged into develop as `beca492d36c0c625e1a68a7ca055f6685fc10fba`. It preserves existing portable Workload.Components in the provider-choice requirement projection via the existing copying constructor. Actual HTTP/metrics/OTLP authority regression tests, original-data isolation, invalid workload rejection and all required targeted checks PASS in [run 38987081285](https://github.com/mcpdev80/baseharbor/actions/runs/38987081285). The reported HTTP exposure pre-consent dependency failure is repaired outside core-917's ownership; do not add a second resolver or duplicate the fix in New. Continue existing #975, integrate latest develop normally once, combine its already-reported full formatting deltas with any actual New fixes, and qualify the resulting complete candidate through existing targeted tests and required selected gates. No author merge/acceptance, no new task or unnecessary native rerun for the dependency's read-only fix alone. The old #975 source/run cannot qualify its new integration automatically; preserve exact evidence boundaries.

- 2026-10-17 implementation checkpoint after actual New-entry wiring: product PR #975 is on exact head `73f5fbdf27593fd9e3d2f53a688ab9805279cfd4`, with refreshed current `develop` base `b73e27603ee082f2fabb81df1b2789fba3367d23`; the PR diff is again only the owned `cmd/baha/app_new_wizard.go` and `cmd/baha/app_new_wizard_test.go`. The real entry now reaches the accepted controller, current Target snapshot/read authorities, preview/re-consent loop, existing project creation and the existing authorized apply lifecycle; named-requirement preservation, explicit-provider projection/restoration and partial lifecycle-result regressions were added. Exact hosted qualification [38985732469](https://github.com/mcpdev80/baseharbor/actions/runs/38985732469) selected `wizard-app-new-tests`, `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts` plus Docker/Podman lifecycle. Build, vet, source-contracts, exact-candidate, runner-interface, demo-pin and focused-Python are green. The real New tests currently fail before consent on the default HTTP capability with `resolve exposure.http/web: managed HTTP exposure requires explicit workload.components so endpoint identity is deterministic`. Root cause is the accepted dependency `cmd/baha/app_provider_choice.go::appProviderChoiceProjection`: its `ExposureHTTP` projection copies the exposure into a fresh manifest without the original `Workload.Components` and then calls `application.ResolveFootprint`. That file is outside core-917 ownership; bypassing it in New would duplicate the accepted provider resolver/controller. The same run also reports the bounded gofmt deltas in the two owned files; no further product candidate is published while the selected native jobs are still running. Keep task active and product Draft; no merge or acceptance claim.


- 2026-10-17 verification of independent review #5554835953: exact product HEAD `6f5e03cb22a404a396354df9c637ee001598e823` and hosted run [38927630850](https://github.com/mcpdev80/baseharbor/actions/runs/38927630850) are fully **SUCCESS**, including `wizard-app-new-tests`, `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, Docker lifecycle, Podman lifecycle and binding `PR Selected Checks`. This qualifies only the existing partial candidate, **not** full core-917 acceptance. The interactive `runAppNewWizard` still bypasses `appWizardController`; named and explicit provider preferences remain unimplemented through the actual New entry, and no authoritative new-source Target/impact refresh or partial runtime result flow is proven. Review keeps Draft/active. Do not publish further un-prechecked candidates or reuse the old CI result for changed code.

- 2026-10-17 independent implementation checkpoint at `6f5e03cb22a404a396354df9c637ee001598e823`: [review 5554835953](https://github.com/mcpdev80/baseharbor/pull/975#pullrequestreview-5554835953) confirms [Actions 38927630850](https://github.com/mcpdev80/baseharbor/actions/runs/38927630850) completed successfully, including actual New tests, formatting/source/contracts/vet/build, exact candidate/demo/runner, both selected Docker and Podman lifecycle gates and authenticated final `PR Selected Checks`. Earlier pending labels below are historical. **Task still active and product Draft, not accepted/merged**: the interactive entry retains legacy prompts rather than driving the new controller; the separate bridge is not called by that entry and rejects explicit provider preferences instead of integrating their existing Target authority. Complete the actual input-to-controller-to-existing-authorities path, not another isolated helper, with preserved supported full intent, current Target projections, correct consent and create-only/no-silent-start behavior. Exercise the real entry end-to-end, repeated No/Cancel/EOF/no writes, explicit preferences, stale plan/refreshed consent and actual partial outcomes where execution is requested. Stay within owned New files, preserve source/domain/registry authorities and other sessions. Integrate current develop including merged #974/#976 normally once in the coherent completed candidate; the old green runtime evidence cannot automatically qualify changed future inputs. Batch all source/tests/formatting before pushing and await complete focused/native results. No new task or full matrix. Publish complete validated handoff only after implementation; no repeated preliminary native runs for isolated formatting changes.

- 2026-10-16 follow-up checkpoint: product draft #975 at exact head `6f5e03cb22a404a396354df9c637ee001598e823` (develop base `e514a8b6d47b28f268b779376b1e95cd20674611`). The callable confirmed-decision New adapter now preserves the existing wizard-owned ApplicationID and rejects a differing application name, environment or explicit ID; typed positive/negative tests enforce this. Only New wizard and dedicated tests changed. [Latest targeted hosted candidate 38927630850](https://github.com/mcpdev80/baseharbor/actions/runs/38927630850) is pending as of this checkpoint; last fully observed candidate [38926794838](https://github.com/mcpdev80/baseharbor/actions/runs/38926794838) had green Go New/format/vet/build/contracts while Docker/Podman lifecycle jobs were still executing. No final release or review qualification is claimed.
- Still incomplete: `runAppNewWizard` remains attached to the legacy capability prompt and no full authoritative New Target resolution/consent/apply/verify wiring or persisted explicit provider preferences is proven. Keep task **active**, product PR **draft**, do not accept/merge. Native gate evidence must be obtained for the final exact integration and remaining behavior implemented within this task.

- 2026-10-16 independent Maintainer CI-discipline finding: [PR #975 process comment](https://github.com/mcpdev80/baseharbor/pull/975) at source `6f5e03cb22a404a396354df9c637ee001598e823` records 11 PR runs between 15:27Z and 15:54Z, nine cancelled. Commit history includes separate implementation/test pushes 39 seconds apart and repeated separate formatting pushes; no urgent supersession explanation was present in PR comments. Existing AGENTS CI execution discipline was not followed. Stop candidate pushes until current results are inspected; batch demonstrated source/test/formatting fixes into one coherent prechecked candidate. If local tooling is unavailable, obtain a bounded isolated complete formatting/compile precheck rather than using native PR CI as a per-file debugging loop. Do not disable required checks/concurrency, use ci.skip or launch extra runtime gates. No current run cancellation requested. Preserve current execution evidence, record the diagnosed causes and only rerun for relevant changed inputs. This is process correction during existing core-917, not code acceptance or a new assignment.

- 2026-10-16 implementation checkpoint (not a review handoff): [Draft product PR #975](https://github.com/mcpdev80/baseharbor/pull/975), branch `feature/core-917-new-lifecycle-wiring`. Scope only `cmd/baha/app_new_wizard.go` and matching dedicated tests. The existing create-only wizard now explicitly says no container/deployment start, pins one generated ApplicationID across Bootstrap preview and Create, and revalidates authoritative Bootstrap manifest/plan/files after confirmation before writing; context cancellation and EOF are tested.
- A separate callable `appNewCreateFromWizardDecision` adapter accepts only an actually confirmed, current `appWizardController` decision and delegates to existing `development.BootstrapApplication/CreateApplication`. It rejects mismatched portable requirements and explicit Target provider preferences that this source-only creation API cannot persist, rather than silently losing them. Dedicated positive/negative unit tests added.
- **NOT YET QUALIFIED:** The interactive user-facing `runAppNewWizard` still uses its original capability prompts; the accepted controller is not yet fully driven from real Target read-only authorities and the existing provider lifecycle path. There is no complete Target-preference persistence or native partial-result presentation. Do not accept or merge this partial draft. Focused CI and exact selected Docker/Podman lifecycle evidence are still being evaluated on the latest candidate; earlier runs include an actual successful Docker gate but not final exact acceptance.
- No registry, Edit, shared Domain, workflow or release-matrix changes. Preserve subsequent concurrent planning updates. Continue core-917 only until these remaining acceptance boundaries are implemented and independently reviewed.



The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
