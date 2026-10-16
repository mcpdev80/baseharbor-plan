---
id: core-911
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-911)"
depends_on: [core-910, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#967"]
sources: ["mcpdev80/baseharbor#911"]
source_updated: "2026-10-15T16:46:59Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-911 · App edit: load existing selections completely #task #release/v0-4-26 #status/review #view/review #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-911) · **Priority:** not set  
    **PR:** [baseharbor#967](https://github.com/mcpdev80/baseharbor/pull/967)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md)  
**Owner:** mcpdev80 (core-911)  
**Priority:** not set  
**PRs:** [baseharbor#967](https://github.com/mcpdev80/baseharbor/pull/967)  
**Source:** [baseharbor#911](https://github.com/mcpdev80/baseharbor/issues/911)
<!-- /generated:links -->

## Goal

An existing app and its selected Target load losslessly into the shared editing state. Lane: data adapter.

## Scope

- In scope: new dedicated `app_edit_load`/guided hydration files and tests, using existing read-only owners.
- Out of scope: TUI renderers, registry, runtime mutations.

## Acceptance

- Hydrates capability selection AND explicit/automatic provider preferences; does not overwrite another Target's choice.
- Preserves rich manifests, instance names, unknown/extended fields and content not edited in the compact form; never asks for a manual UUID.
- Missing, ambiguous or incompatible sources return concrete typed results; reading mutates nothing.

## Required checks

- Fixture round trip and two Targets with different preferences; missing source and ambiguity; package tests only.

## Dependencies and file ownership

- Depends on core-910.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_edit_load.go` and `cmd/baha/app_edit_load_test.go` only.
- **Delivered interface/result:** Expose a compiling hydration adapter using the merged `GuidedReadContext` and existing authorities. Its result carries the untouched source representation plus editable selections; own any new hydration-specific types in this file.
- **Task-specific proof:** `TestAppEditLoad*`: rich intent, automatic/explicit preferences, two Targets, incomplete/ambiguous sources and no-write snapshots.
- **Boundary:** No edits to `guided_application_read_context*`, checklist/provider/presenter/controller files, lifecycle owners, shared fixtures or registration. Reading/hydration does not apply changes.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent re-review at `250c76c4020c2f2e3faddabb7a820b4e582fd7cc`: **managed-secrets hydration still requires correction; not accepted or merged**. YAML/source binding and byte-preservation corrections address earlier SQL cases, and hosted run `38903229067` is confirmed green with five tests at integration `37a6fbb1058d5aa99f7913905f958b0ff030f180`. However, the existing portable contract stores protected-secrets intent in `Secrets.Managed`, separately from `Capabilities`; the read context copies that capabilities subset, while the authoritative footprint adds `secrets/default`. The adapter currently hydrates only the subset, dropping the active Secrets checkbox and missing a managed-secrets source/context mismatch. Normalize from existing full intent/footprint facts without shared-authority changes, retain exact preferences without duplication, and add real managed-secrets hydration/mismatch/non-mutation regressions. Integrate latest develop normally after the independent core-913 merge; keep scope to the two owned files and use the existing targeted CI. Planning baseline `647b81a` independently passes render/check and all 38 tests; preserve concurrent work.

- 2026-10-16 correction after [Maintainer review #5547904550](https://github.com/mcpdev80/baseharbor/pull/967#pullrequestreview-5547904550): [PR #967](https://github.com/mcpdev80/baseharbor/pull/967), exact source `250c76c4020c2f2e3faddabb7a820b4e582fd7cc`, trusted develop `a1e58f1f3600bf95d0318662bbec447c6e8ed74a` (same tested target; no merge necessary). Only `cmd/baha/app_edit_load.go` and `cmd/baha/app_edit_load_test.go` changed. Hydration now accepts actual authored BaseHarbor YAML using `application.ParseYAML` and canonical BaseHarbor YAML using `application.ParseCanonicalYAML`, derives exact requirement identities from existing `application.PortableContractFromManifest`, checks source/context name, environment, optional system-owned ID and multiset of complete named capabilities, returns safe typed incompatible/missing/ambiguous results, preserves original YAML bytes/comments/spacing via `[]byte` without re-rendering, clones preferences per Target and performs no writes or manual ID allocation. `TestAppEditLoad*` tests cover rich YAML with primary + analytics named SQL, automatic and explicit two-Target preferences, app/environment/capability mismatches, typed errors and actual temporary-file bytes/mtime/mode immutability. [Targeted CI run 38903229067](https://github.com/mcpdev80/baseharbor/actions/runs/38903229067) demonstrates selected Trusted Plan, Workflow policy, Focused Python, source/contracts, cli-gofmt, cli-vet, cli-build and wizard-app-edit-load-tests all PASS; final `PR Selected Checks` **SUCCESS** (run attempt 1). Planning render/check and 38 tests validated by [run 38903418097](https://github.com/mcpdev80/baseharbor-plan/actions/runs/38903418097). Earlier run 38903032043 had gofmt FAILURE and must not be treated as green. No container or runtime matrix; no authority/registry/CI/domain changes. **Independent review remains required; no merge or acceptance.**

- 2026-10-16 independent Maintainer review at `b1d976d210e4d0954dbb9ab007adb21b99c0e0ac`: **changes required, not accepted or merged**. The JSON-only `json.Valid`/`json.RawMessage` source path rejects supported authored/canonical YAML before reading. Source bytes are also not tied to the returned app identity/environment or intent: unrelated JSON (even `{}`) can be combined with a different authority context, and the rich fixture contains two SQL instances while asserting only one incomplete fake context requirement. Preserve real supported original source bytes through existing read/parse owners, bind source and context consistently and fail safely on mismatches without a second parser/state authority or developer UUID prompt. Add valid authority-backed YAML rich roundtrip with all named requirements, two-Target preferences, mismatched app/environment/intent errors, and actual no-write file/state snapshots. Only the two owned hydration files remain in scope. Hosted run `38899265776` at integration `59dd56231818fe3b5c172cb6cf99cacff02fab07` is genuinely green with four tests; it does not prove these missing semantics. Current planning main `abf9d8c` independently passes render/check (0 errors/0 warnings) and all 38 unit tests; concurrent core-913 work is preserved.

- 2026-10-16 core-911 independent-review handoff: Product [PR #967](https://github.com/mcpdev80/baseharbor/pull/967) on `task/core-911-edit-hydration`, exact product HEAD `b1d976d210e4d0954dbb9ab007adb21b99c0e0ac`, trusted `develop` SHA `a1e58f1f3600bf95d0318662bbec447c6e8ed74a` (unchanged since branch creation; no develop merge necessary). Scope is exactly `cmd/baha/app_edit_load.go` and `cmd/baha/app_edit_load_test.go`. Read-only `appEditLoad` adapter uses `GuidedReadContext` authority per Target, preserves exact original supplied source bytes including named instances, extension fields and all noncompact intent, and copies capability selections plus explicit/automatic Target-local provider preferences. Typed safe errors for missing, ambiguous, incompatible, unverifiable and wrong Target; no manual ID, command registration, mutation, or persistence. `TestAppEditLoad*` tests cover rich source byte-for-byte roundtrip, target preference separation, error taxonomy and source/authority nonmutation. Existing targeted [GitHub Actions run 38899265776](https://github.com/mcpdev80/baseharbor/actions/runs/38899265776), attempt 1, **SUCCESS**: Trusted Plan, Workflow policy, Focused Python, source/contracts, `wizard-app-edit-load-tests`, cli-gofmt, cli-vet, cli-build and final `PR Selected Checks`. Unneeded runtime, release, public-contract, candidate and legacy broad validate jobs skipped. Earlier gofmt failures are historical red evidence, not accepted. No containers or runtime matrix. **Await independent review; do not merge or self-accept.**


The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
