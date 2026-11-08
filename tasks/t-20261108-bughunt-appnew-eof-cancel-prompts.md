---
id: t-20261108-bughunt-appnew-eof-cancel-prompts
card_number: "0427-138"
card_short_title: "Wizard cancel uneven"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "A single cancel path: EOF/Ctrl-D at every prompt = clean cancel with no side effects; regression in the cli-surface group."
kanban_title: 0427-138 · Wizard cancel uneven
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1471, mcpdev80/baseharbor#1484, mcpdev80/baseharbor#1493]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42481515062", "https://github.com/mcpdev80/baseharbor/commit/f5abba4219cb65ef16d655ac03b95eab008bc172"]
---
- [x] t-20261108-bughunt-appnew-eof-cancel-prompts · Bug Hunt v0.4.27: Wizard cancel is uneven #task #release/v0-4-27 #status/closed #view/closed #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** —
    **PR:** [baseharbor#1471](https://github.com/mcpdev80/baseharbor/pull/1471), [baseharbor#1484](https://github.com/mcpdev80/baseharbor/pull/1484), [baseharbor#1493](https://github.com/mcpdev80/baseharbor/pull/1493)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42481515062), [proof 3](https://github.com/mcpdev80/baseharbor/commit/f5abba4219cb65ef16d655ac03b95eab008bc172)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261108-bughunt-trust-uninstall-eof-error](t-20261108-bughunt-trust-uninstall-eof-error.md)  
**Owner:** —
**Priority:** normal  
**PRs:** [baseharbor#1471](https://github.com/mcpdev80/baseharbor/pull/1471), [baseharbor#1484](https://github.com/mcpdev80/baseharbor/pull/1484), [baseharbor#1493](https://github.com/mcpdev80/baseharbor/pull/1493)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
A single cancel path: EOF/Ctrl-D at every prompt = clean cancel with no side effects; regression in the cli-surface group.

## Problem (source evidence in the dossier)
EOF/empty input on app-new prompts returns a usageError instead of a clean wizard cancel; Ctrl-D is interpreted differently per prompt. Source: hunt H-D3 BF-01/BF-02.

## Acceptance
A single cancel path: EOF/Ctrl-D at every prompt = clean cancel with no side effects; regression in the cli-surface group.

## Dependencies and file ownership
None. Write-set: cmd/baha app new wizard prompts.


## Code/PR owner — 2026-11-08

- Claimed for [PR #1471](https://github.com/mcpdev80/baseharbor/pull/1471): top-level `baha new` EOF cancellation now has a single clean return, and early app-new name/location/stack EOF regressions verify no project creation. Existing pre-consent cancellation test retained.
- Exact PR CI is pending; card remains `active` until full prompt matrix and acceptance. No conflicting worker claim.


## Merge and acceptance handoff — 2026-11-08

- [PR #1471](https://github.com/mcpdev80/baseharbor/pull/1471) merged at `f5abba4219cb65ef16d655ac03b95eab008bc172`, exact head `4c809b1937dafc210a36b67585e56910390bee55`; [CI #42481515062](https://github.com/mcpdev80/baseharbor/actions/runs/42481515062) terminal SUCCESS, including Go-unit, native Docker/Podman and selected checks.
- Name/location/stack-entry EOF and existing pre-consent EOF regressions pass; top-level interactive `baha new` now interprets EOF as clean cancellation. **Full all-prompts matrix not yet proven.** Move to `review` with Owner retained; no acceptance/closed assertion before remaining modes and needs-list inputs are checked.


## Remaining partial-input EOF regression — 2026-11-08

- [PR #1484](https://github.com/mcpdev80/baseharbor/pull/1484) adds a fail-closed EOF guard for unterminated partial inputs in `readPrompt`: Ctrl-D after partial `yes` must not authorize project creation. Regression tests cover partial input and confirmation.
- This complements merged #1471. Card stays `review` with existing owner until the exact-head CI and complete acceptance are verified. No separate duplicate implementation lane.

## CI remediation — 2026-11-08 (0427-138)

- PR #1484: strict partial-line EOF cancellation retained; workspace wizard scripted fixture responses now terminate with newline (avoids false EOF) on head `24431d9f0504f712696a17883bc27ad3b68421d9`, exact-head CI run https://github.com/mcpdev80/baseharbor/actions/runs/42502959988. Keep active until terminal CI.

## Verified PR #1484 merge — 2026-11-08

- [PR #1484](https://github.com/mcpdev80/baseharbor/pull/1484) merged to develop as `fa355e8360497b03a40837b60ae6c88f166a8699` from exact head `24431d9f0504f712696a17883bc27ad3b68421d9`.
- [CI #42502959988](https://github.com/mcpdev80/baseharbor/actions/runs/42502959988) = SUCCESS, including source format, gofmt, Go unit/build/vet and native Docker/Podman destroy retry. Workspace prompt fixtures updated to terminate legitimate scripted answers with newline; unterminated partial input cancels safely.
- Keep card status under normal acceptance triage; this is not proof of unrelated Wizard or full Release E2E.

## Consolidated review PR #1493 — 2026-11-08

- [PR #1493](https://github.com/mcpdev80/baseharbor/pull/1493) exact head `7b1c01b843305a36c51600f7125f74aece5cf2cd`; [CI #42510870133](https://github.com/mcpdev80/baseharbor/actions/runs/42510870133). Added early wizard EOF/partial-input matrix asserting clean cancellation, no filesystem mutation across name/directory/stack/mode/needs/pre-consent prompts.
- Card intentionally remains `review` until the relevant contract is fully established by actual executed CI; no synthetic PASS or unrelated Remote smoke acceptance.

## Corrected PR #1493 exact-head CI — 2026-11-08

- Formatter-corrected PR head `050123164e4522792db900d852c3f6d42fb8137a` tested by [CI #42510949058](https://github.com/mcpdev80/baseharbor/actions/runs/42510949058); prior run cancelled after a gofmt-only error.
- Source format, CLI gofmt/build/vet and source-contract checks succeeded; native Docker/Podman and complete CLI package tests must still finish. No premature acceptance.

## Final review acceptance and merged PR #1493 — 2026-11-08

- [PR #1493](https://github.com/mcpdev80/baseharbor/pull/1493) merged to develop as `7af8d440e9a4dd1b633fdc44e4093109fe44ae37` from exact head `050123164e4522792db900d852c3f6d42fb8137a`.
- [Exact-head CI #42510949058](https://github.com/mcpdev80/baseharbor/actions/runs/42510949058) terminal **SUCCESS**: full CLI package tests (includes new R27 review regressions), CLI build/vet/gofmt, source contracts, native Docker + Podman destroy-retry and final `PR Selected Checks` all passed. No skipped required selected check.
- Acceptance rationale: Reviewed shared `readPrompt` EOF contract: buffered partial input is never interpreted as affirmative; `appNewAbortOnEOF` and controller return a clean cancel before consent. New `TestR27WizardEarlyPromptEOFMatrixNoMutation` exercises nine early prompt/cut cases and checks no project root or error. Existing #1471 and #1484 cover chooser, pre-consent and partial input. Exact-head full cmd/baha tests and selected native CI passed.
- Card status **closed**, resolution `accepted`, no processing owner; unrelated remote Core/workstation E2E and larger release qualification are tracked separately.
