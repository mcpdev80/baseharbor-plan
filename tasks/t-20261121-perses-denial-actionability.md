---
id: t-20261121-perses-denial-actionability
card_number: "0428-211"
card_short_title: "0428-211 Perses anonymous"
type: task
areas: [application]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: ""
kanban_title: "0428-211 Perses anonymous denial must name the next command"
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

## Goal

The anonymous Perses operator-access denial says **which precondition is missing and which command to run next**, so an
operator reading `baha` output can act without opening the source.

## Why

H-V24 inventoried all seven operator-auth refusal sites at develop `40cb28c758b0` (akte
`evidence/bug-hunt-2026-11-21/actionability-desk/round-1.md`). Six sites are actionability-complete; `cmd/baha/mcp.go:301`
is the model because it names `baha login`. The seventh, `internal/application/perses_management_ui.go:96`, names the
missing condition but gives no next command and no path, so an operator on the Perses management surface cannot continue.

## Scope

Allowed write-set:

- `internal/application/perses_management_ui.go` (lines 95-97: message and error text)
- the test in `internal/application/` that asserts this denial text

Forbidden: `internal/operatorauth/**`, `internal/capability/perses_selection.go`, `internal/serviceaccess/**`,
`.github/**` (Owner rails), and every `cmd/baha/` file while 0428-204 runs.

## Acceptance criteria

1. The denial names the missing precondition **and** the next step, in the same shape as `cmd/baha/mcp.go:301`.
2. A test asserts the new wording by content, so a later regression cannot silently drop it.
3. The machine-readable error code stays unchanged unless the handoff proves otherwise.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./internal/application/` (PR Selected Checks) |
| Test identifier | `0428-211` |
| Route | `auto-discovery` |

## Stop and report

If actionable wording requires changing enforcement rather than text, stop and report file:line: that is an Owner rail.

## Handoff

Branch, PR, exact head SHA, terminal hosted run id, evidence
`evidence/r28-welle4-2026-11-21/perses-denial-actionability/round-1.md`.
