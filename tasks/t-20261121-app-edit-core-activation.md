---
id: t-20261121-app-edit-core-activation
card_number: "0428-207"
card_short_title: "0428-207 App Edit Core"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: Codex (Marcel, active wait sweep 2026-11-21)
kanban_status: review
kanban_lane: review
kanban_summary: "App Edit activation against a real isolated Core stops failing with start real isolated Core for App Edit: existing native…"
kanban_title: 0428-207 · 0428-207 App Edit Core
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1735]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/b10dc56b785cc3ff75d054fa3d867254b6e7d286", "https://github.com/mcpdev80/baseharbor/actions/runs/44861290062"]
---

- [ ] t-20261121-app-edit-core-activation · 0428-207 App Edit Core activation fails without protected Core network #task #release/v0-4-28 #status/review #view/review #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (Marcel, active wait sweep 2026-11-21) · **Priority:** high  
    **PR:** [baseharbor#1735](https://github.com/mcpdev80/baseharbor/pull/1735)  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** Codex (Marcel, active wait sweep 2026-11-21)  
**Priority:** high  
**PRs:** [baseharbor#1735](https://github.com/mcpdev80/baseharbor/pull/1735)  
**Source:** 
<!-- /generated:links -->

## Goal

`App Edit` activation against a real isolated Core stops failing with
`start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner`.
The command either finds the protected Core / shared backend owner it needs, or reports a specific actionable reason.

## Why

w221's read-only split of the 89 other-domain `./cmd/baha/` failures placed exactly one case under rubric (b):
a real defect rather than the #1717 operator-auth fallout (rubric c) or the operator-seam class (rubric a, card
0428-204). Witness: `cmd/baha/app_edit_apply_test.go:1253`. **Site corrected by w223 (read-only round, akte
`evidence/r28-welle4-2026-11-20/app-edit-core-activation/round-1.md`):** the message is produced by
`inspectCoreDefaultNetworkBinding` in `cmd/baha/core_network_binding.go` (`:18`, raised at `:56`), **not** by
`application_provider_impact.go:63` — that file has zero operatorauth references, so the defect is independent of #1717. Evidence file
`evidence/r28-welle4-2026-11-20/other-domain-test-split/round-1.md`, group 8 detail.

## Scope

Allowed write-set:

- `cmd/baha/core_network_binding.go` (the protected-Core / shared-backend-owner verification)
- `cmd/baha/app_edit_apply_test.go`
- new test file in `cmd/baha/` with a `0428-207` identifier

Forbidden:

- `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**`,
  `internal/capability/perses_selection.go`, `internal/observability/registry.go` (Owner rails)
- `.github/**`, `scripts/**` (Owner)
- every other file in `cmd/baha/` — 0428-204 owns the operator-seam edits there, including the shared
  `operatorAuthFixtureContext` sites. Do not co-edit that file while 0428-204 is in flight: this card is
  stacked behind it.

## Acceptance criteria

1. `cmd/baha/app_edit_apply_test.go:1253` passes at the exact candidate head.
2. One regression test proves the activation path reports the missing protected Core / shared backend owner
   explicitly instead of failing during Core startup.
3. No operator-authentication behaviour changed: the rubric (c) rows are 0428-204's; a fix here that only makes
   the test authenticate is out of contract and must stop and report.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Test identifier | `0428-207` |
| Route | `auto-discovery` |

## Stop and report

- If the defect turns out to be the same operator-auth gate (rubric c), stop: it belongs to 0428-204.
- If a change outside the allowed write-set is required, stop and report file:line.

## Handoff

- Candidate branch, PR, exact head SHA and the terminal hosted run id recorded here.
- Evidence: `evidence/r28-welle4-2026-11-20/app-edit-core-activation/round-1.md`.

READ-ONLY ROUND STARTED (implementation still waits on 0428-204): w223 reproduces group 8 at develop 40cb28c758b0 and answers rubric (b) vs (c). I denied running the lifecycle test on the coordinator host (three other lanes, 96 percent disk pressure) and steered it to the named test host baha-docker with before/after container lists, plus a Go-unit probe of inspectCoreDefaultNetworkBinding whose limits must be stated as 'what this does not prove'. Evidence: evidence/r28-welle4-2026-11-20/app-edit-core-activation/round-1.md.

IMPLEMENTATION ROUND COMMISSIONED after w223s read-only round: the guard in cmd/baha/core_network_binding.go:52-58 keeps its refusal, the change is the actionable reason. Stacked onto the 204 branch if it must touch app_edit_apply_test.go (w216 owns the stamping there).

CORRECTED MY OWN MEASUREMENT: PR #1735 exists since 01:16 (head 09cf55bbaa41, base develop, develop is ancestor), files exactly cmd/baha/core_network_binding.go (+15/-1) and core_network_binding_actionability_test.go (+82/-0) - allowed write-set, guard kept. It was created as a DRAFT, which is why my required-check field looked empty; I moved it to ready with gh api -X POST pulls/1735/mark_ready so a required run exists at all. Card stays active: the akte is not on plan main and no terminal hosted run has been witnessed by the lane yet (§5.3/§4.6). Both demanded in one short note.

HANDOFF COMPLETE: PR #1735 (head 09cf55bbaa41, base develop 40cb28c758b0, draft=false after my mark-ready via graphql) and akte evidence/r28-welle4-2026-11-21/app-edit-core-activation/round-1.md on plan main (bce75e66 + merge 0dd45072). Measured by coordinator: guard refusal kept (core_network_binding.go +15/-1), new test file core_network_binding_actionability_test.go (+82/-0) asserts the message CONTENT, develop is an ancestor of the head, and the lane watched its own run 44849220708 to terminal state and labelled the four red cli shards as the inherited 0428-204 gate instead of chasing them (§5.4). This is the second clean handoff of the night and the first one that names the owner central helper correctly: the denial convention 'runWithIO directly for unauthenticated cases' is what the reviewer will check against #1615's test_operator_context_test.go.

CODEX-REVIEW REQUEST CHANGES an head 09cf55bbaa41 (plan 5fa43643, path witness 838aec5b): (2) blocking - der neue missing-inventory-test erreicht den ENOENT-ast in core_network_binding.go:69-74 nicht, weil der renderer direkt aufgerufen wird; (3) der aktivierungs-pfad inspectCoreDefaultNetworkBinding bleibt ohne regressionstest, akzeptanz-kriterium 2 offen. korrektur im Anlauf auf freien sitz.

2026-11-21 wait-sweep continuation: PR #1735 head `b10dc56b785cc3ff75d054fa3d867254b6e7d286` adds `Test0428207CoreActivationFailsBeforeComposeWhenOwnerInventoryMissing`. It drives `startControlPlaneRuntime` with a fake Docker CLI reporting an existing native network and absent protected inventories, asserts the actionable missing-inventory/shared-owner error, and asserts Compose `config`/`up` never run. `go test ./cmd/baha -run '^(Test0428207|TestAppEditApply)' -count=1` and `git diff --check` pass locally. Exact run [44861290062](https://github.com/mcpdev80/baseharbor/actions/runs/44861290062) is terminal failure: cli-0..3 fail on managed-environment operator-auth test fixtures; `packages` fails the three Loki multi-source fixture cases; Selected Checks accordingly fails. The 0428-207 test itself produced no failing output. No forbidden files changed. Resume after the 0428-204/#1726/#1615 and 0428-212/#1734 gates are resolved, hop #1735 to fresh develop, rerun exact checks, then merge.

korrektur geliefert: PR #1735 head 213331217024 (draft=false, develop IST ancestor, von mir gemessen), dateien genau core_network_binding.go + core_network_binding_actionability_test.go. gehosteter durchgang 44859099909 am exakten head: Workflow policy / Trusted Plan / Native gate plan / go-vet / go-build / cli-gofmt / Focused Python = SUCCESS, cli-0..3 = failure (geerbt, auf sauberm base 09cf55b gegentestet). akte round-2.md 11455 bytes, plan main 45f444f1. re-review eingereiht (reviewer haelt gerade #1702).

SELF-CORRECTION: booking c6e50f7c/ac06c68f was published by my card-status retry AFTER the owner's rebase completed, and it overwrote the owner's claim field on tasks/t-20261121-app-edit-core-activation.md (owner 'Codex (Marcel, active wait sweep 2026-11-21)' at 7e84a220 became 'w228-0428-207-appedit-fix'). ownership restored here; the lane's delivery stays documented: PR #1735 head 213331217024, develop ancestor, run 44859099909 (policy/Trusted Plan/vet/build/gofmt/Focused Python SUCCESS, cli-0..3 failure inherited), akte 45f444f1. card content work is the owner's from now on; my lane 47aef7ca has been ordered to stop writing on #1735 and to deliver a handoff note instead.
