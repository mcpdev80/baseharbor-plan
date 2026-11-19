---
id: t-20261114-r28-cli2-source-model
card_number: "0428-059"
card_short_title: "Extend app sources and"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: codex-open-pr-sweep-1595
kanban_status: active
kanban_lane: active
kanban_summary: "Extend app sources and components. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-059 · Extend app sources and
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-uid-app]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1595]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-source-model/round-1.md"]
---

- [ ] t-20261114-r28-cli2-source-model · CLI redesign: Extend app sources and components #task #release/v0-4-28 #status/active #view/active #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-1595 · **Priority:** high  
    **PR:** [baseharbor#1595](https://github.com/mcpdev80/baseharbor/pull/1595)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/cli2-source-model/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-contract](t-20261114-r28-cli2-contract.md), [t-20261114-r28-cli2-uid-app](t-20261114-r28-cli2-uid-app.md)  
**Required by:** [t-20261114-r28-cli2-app-interact](t-20261114-r28-cli2-app-interact.md), [t-20261114-r28-cli2-app-status](t-20261114-r28-cli2-app-status.md), [t-20261114-r28-cli2-source-pull](t-20261114-r28-cli2-source-pull.md), [t-20261119-r28-cli-machine-coverage-regeneration](t-20261119-r28-cli-machine-coverage-regeneration.md)  
**Owner:** codex-open-pr-sweep-1595  
**Priority:** high  
**PRs:** [baseharbor#1595](https://github.com/mcpdev80/baseharbor/pull/1595)  
**Source:** 
<!-- /generated:links -->

## Goal

Extend app sources and components. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Build source/component domain changes for optional unique components, multiple per source, local directory and existing Git/OCI, incremental add/path/remove with ownership-safe detach.

## Entry points and ownership

- Starting points: `internal/development/ source models; cmd/baha/app_workspace.go; app_workspace_wizard.go`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

No neighboring scans or artificial components; unique names and multi-component maps, non-Git source, no local files deleted, deterministic machine parity.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

2026-11-19 22:17 UTC — stack recovery owner `codex-open-pr-sweep-1595`. PR #1595 remains OPEN+DRAFT, exact head `818d572b982a69e2caebd5474a4ba270ed21fd41`, base `lane-0428-uid-target` at `ae0602e02882619dea151dc82d62b98b72481566`, `CLEAN` relative to that base. Current exact-head run `43814664405` is SUCCESS for the draft source/routing and Go shard/package cells, but the selected-check aggregator, source format/build/vet and native/release cells were skipped under draft policy. Prior content reviews approve; this does not satisfy a new non-draft exact-head acceptance run.

The stack is the current integration blocker: #1580 is OPEN+DRAFT and CONFLICTING against its base #1578; both are still unmerged. #1595 is based on #1580, so do not retarget it directly to `develop` or merge the stacked history until #1578 → #1580 ownership/conflicts and required checks are reconciled. Downstream #1614, #1623 and #1625 overlap the generated CLI index / machine-coverage paths in this PR; integrate those shared paths sequentially and leave their current owner files untouched. No product changes have been made in this recovery pass yet. Next: verify the parent stack owners/conflicts and choose the smallest safe sequence; then hop/promote #1595 and run exact-head checks when the base is valid.

draft PR #1595 @ eda0cd61c, base lane-0428-uid-target; local package+audit runs green on candidate SHA; CI trigger finding (no PR CI for lane bases) in akte

BOARD-KORREKTUR nach unabhaengiger GEGENLESE (akte evidence/r28-welle4-2026-11-19/codex-review-wave/board-sweep-gegenlese-1.md, haupt e86d817d): der PR dieses fachers ist draft=true. Ein draft ist KEIN kanditat (§5.2), also war der zustand 'review' zu gut — er versprach einen pruefbaren kanditaten, den es nicht gibt. FEHLENDE STUFE, klar benannt: draft auf non-draft, EIN monotoner hopf auf den aktuellen develop, EIN exact-head-lauf bis terminal; die arbeit im zweig ist vorhanden. Rueckstandiger zustand, kein inhaltlicher rueckstand

INHASBERSCHAFT FREIGEGEBEN (transfer-ersuchen, queue662): der eigentümer-text nannte 'lane-0428-059-cli2-source-model (flash)' — GEMESSEN KEINE solche sitzung (codeman agent list: nur codex-rev-cli2b als reviewer, idle; der flash-sitz traegt 0428-083). zweig refs/heads/lane-0428-059-cli2-source-model = 818d572b982a, PR #1595 draft=true base.ref=lane-0428-uid-target, 19 dateien, unveraendert seit 11-16. write-set cmd/baha/app_workspace* + human_workspace.go ist DISJUNKT zu meinen laeufernden PRs (#1690 application_provider_authorization.go, #1702 app_status_*/app_perses_*, #1684 app_apply_lifecycle.go — keine gemeinsame datei gemessen). ACHTUNG: ein base.ref der cli2-kette eroeffnet KEINEN pull_request-lauf (ci.yml :14-18 nur develop/main/lane-*)

INHASBERSCHAFT FREIGEGEBEN, karte zurueck auf planned/ready damit scripts/plan.py claim sie annehmen kann (active ohne owner war ein regelverstoss, den mein eigenes skript nicht schreiben kann: 'if a.owner:' ist fuer einen leeren string falsy — queue662, werkzeug-befund). Gemessen: keine sitzung namens lane-0428-059-cli2-source-model mehr (flash traegt 0428-083); zweig 818d572b982a; PR #1595 draft=true base.ref=lane-0428-uid-target; write-set cmd/baha/app_workspace* disjunkt zu meinen laeufernden PRs. WARNUNG an den nehmer: ein base.ref der cli2-kette eroeffnet KEINEN pull_request-lauf (ci.yml :14-18 oeffnet nur develop/main/lane-*) — basis auf develop umbiegen oder den Zweig in lane-* umbenennen, sonst gibt es nie einen exact-head-beleg

2026-11-19 22:28 UTC — refreshed 0428-059 recovery check:
- Current product develop is `4b3a3559070e9b81b1886a357f6a46bc6dfce790`. Current `.github/workflows/ci.yml` already includes `lane-*` in `pull_request.branches`; the historical claim above that lane bases receive no PR run is superseded. Exact run `43814664405` is a draft run whose selected/normal/native cells were skipped by draft policy. Making the recovery candidate ready will trigger normal PR checks on a lane base.
- PR #1578 remains OPEN+DRAFT at `6f07aef2`, based on old develop `2581000b`; PR #1580 remains OPEN+DRAFT at `ae0602e0`, based on stale #1578 and reported conflicting. PR #1595 remains OPEN+DRAFT at `818d572b` on #1580. Do not retarget the existing #1595 branch to develop: its visible develop diff includes the parent stack.
- Independent source-model audit confirms the authored #1595 commit `eda0cd61` is a single-parent commit. Replaying only that commit's owned patch on current develop avoids the #1578/#1580 merge history. A local scratch application of the 14 non-shared paths was clean and touched no `security.go`. The other five paths (`cmd/baha/machine_coverage.go` and four generated CLI index/coverage documents) overlap current develop and are reserved for integration-owner reconciliation; a blind cherry-pick conflicts on the machine registry.
- On scratch `4b3a355` plus those 14 non-shared paths, the focused command
  `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/usr/bin/false go test ./cmd/baha -run '^(TestWorkspaceInitAcceptsLocalDirectorySource|TestWorkspaceInitRejectsArtificialComponents|TestWorkspaceSourceAddAndRemoveDetachSafely|TestWorkspaceComponentAddListRemove|TestWorkspacePathSetsAndShowsSourcePaths|TestWorkspacePathRejectsForeignCheckoutOwnership|TestWorkspaceRootNamespaceMirrorsSourceModelCommands|TestWorkspaceSourceModelPreservesExistingMachineSemantics|TestWorkspaceLocalSourceMappingOverridesPortablePath|TestWorkspaceGitStatusIncludesLocalGitSources|TestWorkspaceWizardCreatesPortableModelAndLocalMapping|TestWorkspaceWizardCancelDoesNotWriteState)$' -count=1`
  passed; `go test ./internal/development` passed in the combined exploratory run. An unfiltered `cmd/baha` run was interrupted after encountering native/test-environment failures and an interactive Git credential prompt; it is not acceptance evidence. Two unrelated target-default failures were reproduced on unmodified current develop, so do not attribute them to this patch.
- Next safe step is to sequence the five shared coverage/index paths with the integration owner, then prepare a fresh candidate at current develop containing only the owned slice, regenerate the reserved documents, and obtain exact-head non-draft checks. No product branch or PR ref was changed in this recovery check; `security.go` remains untouched.

2026-11-19 22:31 UTC — Owner-authorized sweep continuation: found and fixed a managed-tenant authorization flaw. `loadWorkspaceSourceModel` is now read-only; source add/remove and component add/remove authorize with `workspace.init`, component list with `workspace.show`, repository checkout writes with `workspace.map`, and local-source path writes with `workspace.init`. Regression coverage confirms viewer reads work, all six write variants are denied without changing the model/mapping, and editor source/map/local-path writes persist. Exact commits: `1d081ca1` and `2769d2a5`; pushed candidate head `2769d2a56ec1a63396836bac15b1ea6d88872bba` to the existing PR branch after confirming no Codeman worker/claim for 0428-059. Local `go test ./cmd/baha -run 'TestWorkspaceSourceModelWritesRequireUpdatePermission|TestWorkspace(ComponentAddListRemove|SourceAddAndRemoveDetachSafely|PathSetsAndShowsSourcePaths)' -count=1` passed, as did `go test ./internal/development -count=1` and `git diff --check`; independent read-only review found no missed write path. PR `CI · PR #1595` run `44629295354` is currently running; the draft Go package/CLI shards and draft source/routing jobs are pending, other draft-excluded jobs are skipped. Test route is ordinary Go package discovery, selected by the `synchronize` PR event on this `lane-*` base (confirmed by Coordinator; prior claims here that lane bases do not open CI were incorrect). PR remains OPEN+DRAFT, based on `lane-0428-uid-target`; #1580 → #1578 stack and downstream generated-file sequencing still block promotion/merge. No base retarget or generated-file edits made. 0428-154 is published as the dependent generator-only follow-up.

2026-11-19 22:34 UTC — run `44629295354` reached terminal SUCCESS on exact head `2769d2a56ec1a63396836bac15b1ea6d88872bba`. `PR · Draft source and routing`, `PR · Draft Go · cli-0/1/2/3`, and `PR · Draft Go · packages` all passed. `PR Selected Checks`, normal Go/source-format/validate, native gates and release checks were SKIPPED by draft policy; this is not a promotion/merge pass. PR remains OPEN+DRAFT. Read-only parent-stack audit: #1578 remains owned/waiting under active env-policy sequence 0428-053 and has a path traversal validation blocker; #1580 remains OPEN+DRAFT/CONFLICTING against #1578 and its last exact run skipped qualifying checks. No changes made to either parent. Continue only after stack and five generated-file paths are sequenced; preserve the current exact-head draft run as partial evidence.

2026-11-19 22:47 UTC — owner-authorized clean-base candidate and reviewable PR:
- Rebuilt the slice on current `develop` `4b3a3559070e9b81b1886a357f6a46bc6dfce790`, retaining only the 0428-059 implementation. Incorporated the managed-tenant fix for model reads/writes and added source/component/path CLI coverage classifications. Updated the German machine-coverage reference with the 18 new command rows after `documentation-audit` exposed the manual EN/DE command-parity requirement; the other generated command-index/coverage files came from `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run 'TestMachineDocumentationTracksRegistryAndCommandTree|TestHumanCommandIndexTracksExactCommandMetadata' -count=1`.
- Candidate commits: `85e61c3b7c26013941502a4909250db49e9e98da` (feature + generated docs) and `fb3a61a7ac0980578f3c8c54769a93b617300554` (German command-reference parity). PR #1595 now targets current `develop`, is ready for review, and has no stacked history in its diff.
- Local checks at the feature candidate: generator tests passed; `go test ./cmd/baha -run 'TestWorkspaceSourceModelWritesRequireUpdatePermission|TestWorkspace(ComponentAddListRemove|SourceAddAndRemoveDetachSafely|PathSetsAndShowsSourcePaths)' -count=1` passed; `go test ./internal/development -count=1` passed; `go build ./...` passed; `git diff --check` passed. After the German reference correction, `PATH=/tmp/baseharbor-pyshim:$PATH bash scripts/documentation-audit.sh` passed including EN/DE page coverage, technical integrity, workflow boundaries, Python fixtures, navigation and governance checks. The initial exact run `44631484053` on `85e61c3b` failed `documentation-audit` on the missing German command rows; it was superseded by the corrected head. Exact PR run `44631877286` for `fb3a61a7` is pending; no merge until this exact run reaches terminal success and selected checks are verified.
- Fresh read-only Codeman observation at 22:41 UTC confirms 0428-059 remains our only active claim; no worker overlaps these files. Other active Codeman write sets remain untouched. Do not mark this task accepted yet.
