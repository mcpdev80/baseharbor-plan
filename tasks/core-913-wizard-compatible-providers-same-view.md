---
id: core-913
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-913 implementation)"
depends_on: [core-910, core-912]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#966]
sources: ["mcpdev80/baseharbor#913"]
source_updated: "2026-10-15T16:46:46Z"
labels: [area/dx]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/966", "https://github.com/mcpdev80/baseharbor/commit/b3428843bc8f04156339a7b7f6d1e0ed6fa955d6", "https://github.com/mcpdev80/baseharbor/actions/runs/38903170816"]
---

- [x] core-913 · Wizard: offer compatible providers in the same view #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-913 implementation)  
    **PR:** [baseharbor#966](https://github.com/mcpdev80/baseharbor/pull/966)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/966), [proof 2](https://github.com/mcpdev80/baseharbor/commit/b3428843bc8f04156339a7b7f6d1e0ed6fa955d6), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/38903170816)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-912](core-912-wizard-needs-first-selection.md)  
**Required by:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (core-913 implementation)  
**Priority:** not set  
**PRs:** [baseharbor#966](https://github.com/mcpdev80/baseharbor/pull/966)  
**Source:** [baseharbor#913](https://github.com/mcpdev80/baseharbor/issues/913)
<!-- /generated:links -->

## Goal

For a need, a compatible provider preference can be set in place; Automatic stays the default. Lane: provider view.

## Scope

- In scope: separate `app_provider_choice` files and tests, using only the agreed selection-component interface.
- Out of scope: checklist core files, central registry, resolver; persistence (not in this task).

## Acceptance

- Shows the current compatible providers/instances from the Target/registry/resolver result instead of a fixed product catalog.
- No additional mandatory screen; shows the proposed actual provider and reason; errors are concrete with no silent substitute.
- The preference stays Target/deployment intent, never a portable manifest field.

## Required checks

- Automatic/explicit, available/incompatible/ambiguous, no provider, Target switch; component/contract tests only.

## Dependencies and file ownership

- Depends on core-910 and core-912.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_provider_choice.go` and `cmd/baha/app_provider_choice_test.go` only.
- **Delivered interface/result:** Consume the accepted core-912 component API and existing Target/provider facts. Return Target-scoped preference selections without writing them. All APIs must be present on develop before assignment.
- **Task-specific proof:** `TestAppProviderChoice*`: automatic/explicit, compatibility/ambiguity, missing candidate and Target switch.
- **Boundary:** No changes to selection-component source, resolver/registry, persistence or portable manifest schema. If the predecessor API is insufficient, correct and integrate it before assigning this task.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent Maintainer acceptance: **accepted and merged** via [PR #966](https://github.com/mcpdev80/baseharbor/pull/966), squash commit `b3428843bc8f04156339a7b7f6d1e0ed6fa955d6` on product `develop`. Reviewed source `6a27ac0c5b1d5fb80a55a755093999dccba4463e` resolves current selected requirements through ephemeral existing manifest constructors and `application.ResolveFootprint` per requirement; newly added SQL, deselected ambiguous source needs and mixed SQL/cache ambiguity now behave correctly without replacing the resolver. Earlier full-identity preference, registry, environment/binding and explicit display fixes retained. [Hosted run 38903170816](https://github.com/mcpdev80/baseharbor/actions/runs/38903170816), attempt 1, SUCCESS at integration `4e3de34e3e355f503551870ed2086bbdcbdb882b` over trusted base `a1e58f1f3600bf95d0318662bbec447c6e8ed74a`; logs confirm ten provider-choice tests, all mandatory source/format/vet/build/Python/policy/final checks green, no runtime matrix. Unsupported or declaration-dependent intent remains explicitly rejected rather than invented. Only the two owned files changed. Planning and concurrent core-911 handoff preserved; render/check passes with 0 errors/0 warnings and all 38 unit tests before publication. Component acceptance does not accept later controller/wiring or release work.

- 2026-10-16 follow-up to independent review #5547880685: [PR #966](https://github.com/mcpdev80/baseharbor/pull/966) updated at exact source HEAD `6a27ac0c5b1d5fb80a55a755093999dccba4463e`, trusted develop base `a1e58f1f3600bf95d0318662bbec447c6e8ed74a`, GitHub PR integration `4e3de34e3e355f503551870ed2086bbdcbdb882b` (0 behind develop, no force-push).
- Automatic is now resolved **per currently selected Requirement** by an ephemeral single-requirement `application.Manifest` projection built with existing manifest helpers, then the authoritative `application.ResolveFootprint`. Unselected original intent cannot block current selections, and ambiguous SQL cannot hide an independently resolved cache regardless of iteration order. Exact Requirement names, environment, registry ownership and authoritative existing bindings are retained; no additional resolver, runtime writes, persistent preferences or portable provider fields.
- New `TestAppProviderChoice*` regressions cover: selecting SQL over SQL-free manifest with one proposed PostgreSQL instance; deselecting an old ambiguous SQL need while cache resolves; ambiguous SQL and unique cache in both requirement orders; and `reflect.DeepEqual` preservation of original manifest, Target snapshot and selection. All previously reviewed identity, Registry.Validate, duplicate-instance, environment, binding and explicit/automatic display tests remain.
- [Targeted hosted GitHub Actions run 38903170816](https://github.com/mcpdev80/baseharbor/actions/runs/38903170816) **SUCCESS**: Trusted Plan, Workflow policy, Focused Python, actual `wizard-provider-choice-tests`, cli-gofmt, cli-build, cli-vet, source-contracts and authenticated binding `PR Selected Checks`. No container/runtime/full release matrix.
- **Review only**: no author merge or task acceptance. Await independent Maintainer review; no other task started.


- 2026-10-16 independent re-review at `5737acc9177f9b0055e063b8d4af9221346a8d25`: **changes still required, not accepted or merged**. Prior identity/registry/environment/binding/explicit-view corrections are present, but Automatic resolves the original manifest rather than the current checklist intent. A newly selected SQL need over a minimal SQL-free manifest has a compatible candidate but no automatic proposal; deselected original needs can still fail resolution. Additionally, a global ambiguous result discards the footprint and suppresses unrelated uniquely resolvable needs. Resolve an ephemeral projection of the current exact selected requirements through existing authorities, preserve original input and binding/environment semantics, and isolate per-need unresolved state without guessing providers. Add regressions for adding a need, removing an unresolved old need, ambiguous SQL plus unique cache in both orderings, and original input non-mutation. Only the two owned files remain in scope. Hosted run `38899184547` is genuinely green with seven tests at integration `17467614cab845666ed83929f5f9f39cad8696b8`; these missing interactive cases require further proof. Planning main `a317631` independently passes render/check with 0 errors/0 warnings and all 38 tests; concurrent core-911 work is preserved.

- 2026-10-16 corrected review handoff for [PR #966](https://github.com/mcpdev80/baseharbor/pull/966), addressing independent review #5547489596. Exact source HEAD `5737acc9177f9b0055e063b8d4af9221346a8d25`, trusted develop base `a1e58f1f3600bf95d0318662bbec447c6e8ed74a`, PR integration `17467614cab845666ed83929f5f9f39cad8696b8`. Normal develop integration via [PR #968](https://github.com/mcpdev80/baseharbor/pull/968); 0 behind develop, no force-push.
- Exactly two owned files `cmd/baha/app_provider_choice.go` and `cmd/baha/app_provider_choice_test.go`. Full `capability.Requirement` identity now travels with existing `application.ProviderPreference`, Target-scoped and unpersisted: independent named SQL preferences retain each name. Current Target registry is validated with `Registry.Validate`; `application.ResolveFootprint` supplies authoritative Automatic/binding decisions. Environment and application-owned instance boundaries respected, existing bindings retained, conflicts fail closed, invalid/duplicate registry entries rejected. View displays actual Automatic/Explicit mode, selected instance, provider and reason; reset to Automatic restores authoritative proposal.
- [Hosted run 38899184547](https://github.com/mcpdev80/baseharbor/actions/runs/38899184547) **SUCCESS**: Workflow policy, Trusted Plan, Focused Python, `wizard-provider-choice-tests` (actual `TestAppProviderChoice*` execution), `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, and authenticated **PR Selected Checks** on exact integration. No runtime/container/full release matrix.
- Status remains **review**, not accepted. Independent re-review and Maintainer merge required. No other task started.


- 2026-10-16 independent Maintainer review at `e99bbd79ef81f1eaf2bce992d20f426054fe6f58`: **changes required, not accepted or merged**. (1) Emitted preferences lose `Requirement.Name`, so two named SQL requirements cannot retain independently addressable provider preferences; preserve the full existing requirement/preference authority. (2) Candidate/Automatic logic omits environment ownership and existing deployment/resource bindings, plus registry validation. A prod-owned instance can be offered in dev, and Automatic wrongly becomes ambiguous when a matching authoritative binding already exists. Consume accepted registry/resolution facts, use valid fixtures and prove environment isolation, binding preservation and invalid/duplicate registry rejection without introducing another resolver. (3) `Select` updates the effective explicit choice but `View` retains the stale Automatic proposal/reason; test accurate explicit presentation and return to Automatic. Successful hosted run `38896384549` at integration `8cff2c5bb1d88c1cdbda5c171713b1a495250b00` is confirmed, including four actual provider-choice tests; it does not cover these missing semantic cases. Planning main `ee69ac2` independently passes render/check with 0 errors/0 warnings and all 38 unit tests; concurrent core-919 review preserved. Continue only the two owned files, obtain corrected focused CI and update this handoff before re-review.

- 2026-10-16 independent review handoff: [baseharbor PR #966](https://github.com/mcpdev80/baseharbor/pull/966); branch `feature/core-913-provider-choice`. Source HEAD `e99bbd79ef81f1eaf2bce992d20f426054fe6f58`, trusted develop base `1d6f1a7982f69622fb1faee6f4b99040c6b6d945`, integration SHA `8cff2c5bb1d88c1cdbda5c171713b1a495250b00`. Current with develop (0 behind); no force push or author merge.
- Exactly two owned Go files. Portable selections from core-912 are projected onto compatible Target registry instances through each instance's actual `Provider.Supports` contract and application ownership boundary. Automatic defaults to an unambiguous instance, reports why; multiple compatible candidates fail closed until an instance ID is explicitly selected, missing/incompatible instances are rejected, and preferences remain Target-scoped in memory, outside portable manifest and storage. No resolver, registry, wizard wiring or workflow changes.
- [GitHub Actions run 38896384549](https://github.com/mcpdev80/baseharbor/actions/runs/38896384549): **SUCCESS** for Trusted Plan, Workflow policy, Focused Python, `wizard-provider-choice-tests` (executed `TestAppProviderChoice*`), `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, and binding `PR Selected Checks`. No runtime/container/release matrix.
- Task remains **review**, not accepted. Independent maintainer acceptance/merge required; stop here.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
