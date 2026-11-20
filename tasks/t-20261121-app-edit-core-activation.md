---
id: t-20261121-app-edit-core-activation
card_number: "0428-207"
card_short_title: "0428-207 App Edit Core"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "App Edit activation against a real isolated Core stops failing with start real isolated Core for App Edit: existing native…"
kanban_title: 0428-207 · 0428-207 App Edit Core
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-app-edit-core-activation · 0428-207 App Edit Core activation fails without protected Core network #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`App Edit` activation against a real isolated Core stops failing with
`start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner`.
The command either finds the protected Core / shared backend owner it needs, or reports a specific actionable reason.

## Why

w221's read-only split of the 89 other-domain `./cmd/baha/` failures placed exactly one case under rubric (b):
a real defect rather than the #1717 operator-auth fallout (rubric c) or the operator-seam class (rubric a, card
0428-204). Witness: `cmd/baha/app_edit_apply_test.go:1253` fails at
`cmd/baha/application_provider_impact.go:63`. Evidence file
`evidence/r28-welle4-2026-11-20/other-domain-test-split/round-1.md`, group 8 detail.

## Scope

Allowed write-set:

- `cmd/baha/application_provider_impact.go`
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
