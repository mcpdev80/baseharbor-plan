---
id: t-20261121-perses-denial-actionability
card_number: "0428-211"
card_short_title: "0428-211 Perses anonymous"
type: task
areas: [application]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: closed
kanban_lane: closed
kanban_summary: "The anonymous Perses operator-access denial says which precondition is missing and which command to run next, so an operator…"
kanban_title: 0428-211 · 0428-211 Perses anonymous
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1733]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44889694969", "https://github.com/mcpdev80/baseharbor/pull/1733", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/perses-denial-actionability/round-2.md"]
---

- [x] t-20261121-perses-denial-actionability · Perses anonymous denial must name the next command #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/application #kind/task
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** normal  
    **PR:** [baseharbor#1733](https://github.com/mcpdev80/baseharbor/pull/1733)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44889694969), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1733), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/perses-denial-actionability/round-2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coordinator  
**Priority:** normal  
**PRs:** [baseharbor#1733](https://github.com/mcpdev80/baseharbor/pull/1733)  
**Source:** 
<!-- /generated:links -->

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

COMMISSIONED from hunt H-V24 (the one befund of that desk): message-only fix in internal/application/perses_management_ui.go:95-97 plus a content-bound assertion. Collision measured before dispatch: no open PR touches this file (gh pr view --json files over eleven PRs).

HANDOFF COMPLETE: candidate published as PR #1733 (head 3a8b4a8b11de, base develop 40cb28c758b0, single commit, draft=false) plus akte evidence/r28-welle4-2026-11-21/perses-denial-actionability/round-1.md on plan main. Measured by coordinator: 'Workflow policy' pass, 'PR Selected Checks' fail — the red is the develop-inherited Go-unit cli shards (card 0428-215 explains why: at develop push only Runtime Docker/Podman run, both success, runs 44769994971/44769994909). So this waits for CODEX-REVIEW and for the seam fix 0428-204; not mergeable on its own.

CODEX-REVIEW (ROLLE: REVIEW) VERDICT = APPROVE, content only, published on plan main (reviewer commit, plus owner's remote path witness 1f86706a, blob f9ecb731). Measured in the verdict and re-measured by coordinator: candidate #1733 head 3a8b4a8b11de identical before/after review (read-only respected); 'git merge-base --is-ancestor origin/develop <head>' = 0, so this candidate IS current; changed files exactly internal/application/perses_management_ui.go and its test (allowed write-set); the new Reason names the missing precondition, the next command 'baha login' and the path; ReasonCode stays operator_authentication_required; regression TestEvaluatePersesAnonymousDenialNamesNextCommand asserts wording by content. MERGE READINESS: NOT mergeable, because the required context 'PR Selected Checks' fails on the develop-inherited Go-unit cli shards (cards 0428-204 and 0428-215). This is the first approved candidate of the window, and it is blocked by the base, not by its own content.
