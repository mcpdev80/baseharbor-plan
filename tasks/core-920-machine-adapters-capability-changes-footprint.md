---
id: core-920
areas: [cli]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-920)"
depends_on: [core-910, core-911, core-919]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#970"]
sources: ["mcpdev80/baseharbor#920"]
source_updated: "2026-10-15T16:46:05Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-920 · Machine adapters: reuse capability changes and footprint #task #release/v0-4-26 #status/review #view/review #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-920) · **Priority:** not set  
    **PR:** [baseharbor#970](https://github.com/mcpdev80/baseharbor/pull/970)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-911](core-911-app-edit-load-existing-selections.md), [core-919](core-919-footprint-cli-json-one-projection.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** mcpdev80 (core-920)  
**Priority:** not set  
**PRs:** [baseharbor#970](https://github.com/mcpdev80/baseharbor/pull/970)  
**Source:** [baseharbor#920](https://github.com/mcpdev80/baseharbor/issues/920)
<!-- /generated:links -->

## Goal

Agents can use the same useful needs/provider operations without the TUI or a CLI subprocess. Lane: JSON/MCP.

## Scope

- In scope: dedicated machine/MCP adapters and tests over existing domain operations.
- Out of scope: registration, discovery/coverage goldens and generated references (core-921 only).

## Acceptance

- Reuses existing domain/provider-change/footprint APIs; classifies useful operations instead of mirroring every UI step as a tool.
- Explicit provider preference can be discovered and expressed; Target binding, authorization, valid plan/consent and required double destructive confirmation are represented equivalently.
- Typed denied/unsupported/conflict/cancel/partial results, secret-free; no false machine capability advertised, no TTY requirement or shell escape.

## Required checks

- In-process adapter/parity/negative contract tests with the same domain fixtures, including footprint, consent/revision change and partial failure. No real provider needed for the transport contract.

## Dependencies and file ownership

- Depends on core-910, core-911 and core-919. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_machine_adapters.go` and `cmd/baha/app_machine_adapters_test.go` only; dedicated adapter fixture files if needed, listed before editing.
- **Delivered interface/result:** Deliver compiling callable JSON/MCP adapters over existing authoritative operations and accepted read/hydration/footprint APIs; describe registration inputs for core-921.
- **Task-specific proof:** `TestAppMachineAdapters*`: in-process capability/provider/footprint parity, typed denial/conflict/cancel/partial results, stale plan/consent and destructive confirmation; no TTY, shell or runtime dependency.
- **Boundary:** No registry/discovery/machine-coverage golden edits and no dependency on unfinished New/Edit CLI wiring. Runtime mutations remain inside existing authorized domain operations.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent re-review at `4374141af05780f1d1eac66969c87b5582fd6e1d`: **proposal-to-execution integration still requires correction; not accepted or merged**. Desired requirements/provider inputs and pre-execution cancellation guards address prior findings. However, Propose returns the new desired-plan ID while Change compares it against the current unchanged-state `view.PlanRevision` and accepts no desired intent for recomputation. In the new fixtures current `impact-1` versus returned `fresh` necessarily rejects the desired proposal before execution. Connect proposal/consent/apply by preserving desired full-identity intent and authoritatively re-planning against a fresh source snapshot; compare consent with the recomputed desired plan, without weakening stale checks, fabricating reader revisions, premature persistence or a second plan store. Add an integrated successful propose -> consent -> execute regression with differing current/desired IDs plus stale snapshot/changed desired plan/consent, named preferences, cancellation and partial effects. Current run `38915442608` is genuinely green but tests proposal/apply separately. Planning main `433f900` independently passes unchanged render/check with 0 errors/0 warnings and all 38 unit tests; core-916 updates preserved. Scope remains the two owned adapter files and existing targeted CI.

- 2026-10-16 correction after [review #5549008868](https://github.com/mcpdev80/baseharbor/pull/970#pullrequestreview-5549008868): existing [PR #970](https://github.com/mcpdev80/baseharbor/pull/970), exact head `4374141af05780f1d1eac66969c87b5582fd6e1d`, current normally merged develop/core-915 `701d9ac4f6e5b78658a4f429ad406f31087d44d9`. Only the two owned `cmd/baha/app_machine_adapters*` files changed. Added typed `appMachineDesiredRequest`/`appMachineDesiredChoice` with full named capability requirements and Target-scoped explicit/automatic choice, `appMachinePropose` accepting the existing core-913 `appProviderChoice` authority via a caller-supplied choice-reader and a separate existing authoritative impact planner; returns exact plan/PlanID/revision, preserved distinct SQL/primary and SQL/analytics preferences, with no premature persistence. Existing `appProviderChoice.Select` enforces compatibility and Target-bound candidates, with typed conflict/unsupported for incompatible, duplicate or foreign selections. Explicit cancellation before and after read, planning and authorization, and immediately before apply maps real canceled/deadline contexts to typed `cancel`; outcomes after an already-started failed/canceled executor remain recorded as partial. `TestAppMachineAdaptersDesiredNamedSQL`, `TestAppMachineAdaptersContextCancellation` and `TestAppMachineAdaptersPartialOnCancelledExecution` verify two named SQL choices, invalid/foreign choices, read/authorization/plan cancellation with zero apply calls and truthful partial outcomes. Existing target/revision/consent/domain authority safeguards remain. Focused [Actions 38915442608](https://github.com/mcpdev80/baseharbor/actions/runs/38915442608) is the sole final integration candidate, **SUCCESS** in all required selected gates, including `wizard-machine-adapter-tests`, `cli-gofmt`, `cli-vet`, `cli-build`, source/contracts, Focused Python, Trusted Plan, Workflow policy and final `PR Selected Checks` (attempt 1). No runtime/release matrix, CLI subprocess, registry or common files modified. Independent re-review required, no merge or task acceptance.

- 2026-10-16 independent Maintainer review at `571f5a4dcf60b7a96cfeaa377ded6b002ff492a7`: **changes required, not accepted or merged**. The adapter reuses read/hydration/footprint, revision/authorization and existing consent owners, but its change request/plan-reader cannot accept desired requirements or Target-scoped provider preferences and it offers no compatible-provider discovery operation. Existing preference output is not an expressible provider-change API. Add bounded typed desired-intent/provider inputs routed through existing authorities (including accepted core-913 where appropriate), return the authoritative plan/revisions, and prove distinct same-kind named preferences, invalid/cross-Target rejection and no premature persistence. Actual context cancellation also maps to denied and is not explicitly checked before apply; add typed cancel behavior and cancellation-at-read/plan/authorization tests with zero execution, preserving real partial outcomes if execution already occurred. Hosted run `38912949020` genuinely executed eight current tests at integration `7bb9edfbc57b39692fd18f070ce41f49b275c92d`; the missing transport cases require further proof despite green required checks. Planning baseline `163458e` independently passes render/check unchanged, 0 errors/0 warnings and all 38 tests. Continue only the two owned files, integrate latest develop after core-915 merge, obtain focused CI and publish validated handoff.

- 2026-10-16 independent review handoff: Product [PR #970](https://github.com/mcpdev80/baseharbor/pull/970), branch `task/core-920-machine-adapters`, exact source HEAD `571f5a4dcf60b7a96cfeaa377ded6b002ff492a7`, trusted develop `1c78c509ffc2846e76ed1b27bc39f478948b1cb0` (identical to current tested PR target; no merge required). Product diff limited to `cmd/baha/app_machine_adapters.go` and `cmd/baha/app_machine_adapters_test.go`. Callable in-process interfaces `appMachineInspect`, `appMachineHydrate`, `appMachineFootprintJSON`, `appMachineChange` reuse accepted `GuidedReadContext`, `appEditLoad`, `appFootprintShowContext`, authoritative `application.ProviderImpactPlan`, `ValidateProviderChangeConsent`, and `RecordProviderChangeResult`. Machine change requires injected existing authorized read, authorization, fresh authoritative impact plan and authorized executor; nil authority is unsupported. Bind Target, application identity, snapshot and plan revisions, immutable consent PlanID, two destructive confirmation stages plus distinct DeleteData consent; never execute stale/denied/cancelled requests. Source requirements including footprint-only `secrets/default`, full kind/name identity and Target preferences preserved. Actual provider outcomes and incomplete/failed receipts are represented without guessing effects; errors are typed denied/unsupported/conflict/cancel/partial and safe. Tests `TestAppMachineAdapters*` verify parity, managed secrets, denied/unsupported, stale plan/consent, double confirmation, partial/failure and immutable inputs. Existing targeted [Actions 38912949020](https://github.com/mcpdev80/baseharbor/actions/runs/38912949020), attempt 1, **SUCCESS**: Trusted Plan, Workflow policy, Focused Python, `wizard-machine-adapter-tests`, source/contracts, cli-gofmt, cli-vet, cli-build and actual final `PR Selected Checks`; native/runtime/release/candidate paths skipped. Earlier gofmt failures are not passing evidence. No registration, discovery/goldens, generated docs, shared CI or runtime changes. Registration inputs for core-921: authorized `appMachineRead`, `appEditLoadReader`, `appMachinePlanReader`, `appMachineAuthorize` and `appMachineApply` implementations supplied from existing owners; do not grant capability where any owner absent. **Await independent review. Do not merge or accept.**

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
