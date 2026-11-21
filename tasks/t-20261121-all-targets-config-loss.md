---
id: t-20261121-all-targets-config-loss
card_number: "0428-210"
card_short_title: "0428-210 all-targets config"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: active
kanban_lane: active
kanban_summary: "TestAppListAllTargetsWorksAfterInstallationDestroy passes: after an installed-to-destroyed transition the all-targets inventory…"
kanban_title: 0428-210 · 0428-210 all-targets config
priority: normal
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-all-targets-config-loss · 0428-210 all-targets inventory depends on a deleted Target config #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** normal  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`TestAppListAllTargetsWorksAfterInstallationDestroy` passes: after an installed-to-destroyed transition the all-targets
inventory still reports the targets it is supposed to report, instead of failing with
`all-targets inventory depended on deleted Target config: BaseHarbor config root is configured but the config.yaml ...`.

## Why

w216 reported this while working 0428-204 and correctly refused to fold it into that PR: the failure is **not**
operator-auth. w221 had grouped it as `cmd/baha/app_commands.go:106` (akte
`evidence/r28-welle4-2026-11-20/other-domain-test-split/round-1.md`, group 9, one test) but labelled it covered by the
0428-204 card. The measured error line disproves that: it is a lifecycle/config-lookup defect, so it needs its own card
and its own PR (one card, one PR).

## Scope

Allowed write-set:

- `cmd/baha/app_commands.go`
- `cmd/baha/app_list_all_targets_test.go`
- the Target-config lookup they call from there (report the file before editing if it leaves `cmd/baha/`)

Forbidden: `internal/**`, `.github/**`, `scripts/**`, and every other `cmd/baha/` file while 0428-204 runs.

## Acceptance criteria

1. The named test passes at the exact candidate head, for the right reason: the inventory no longer reads a deleted
   Target config, or the destruction path keeps the record the inventory needs (state which in the handoff).
2. A regression proves the chosen behaviour across the installed-then-destroyed sequence.
3. The first failing line before and after is quoted verbatim in the evidence.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Test identifier | `0428-210` |
| Route | `auto-discovery` |

## Stop and report

If the fix requires touching the destroy/retirement consent path (`cmd/baha/application_destroy_authorization.go`) or any
Owner rail, stop and report file:line.

## Handoff

Branch, PR, exact head SHA, terminal hosted run id, evidence
`evidence/r28-welle4-2026-11-21/all-targets-config-loss/round-1.md`.

kommissioniert auf dem zweiten laptop-sitz als folge-lane der kette 0428-204: branch vom head 7db142852d22, base-ref des PRs auf den lane-branch der basis-lane. write-set cmd/baha/app_commands.go und cmd/baha/app_list_all_targets_test.go, konfliktfrei gegen 213/214/207. vorgeschaltete meldepflicht:  overlap mit #1615 (head 5466a87bffe1) in denselben dateien wird vor dem ersten schreiben geklaert, weil #1615s versuch 44854729670 44854729670 die cli-shards bereits gruen macht.

stacking-entscheid von mir, nach messung: PR-BASIS = develop 40cb28c758b0 (drei wege gemessen: ls-remote https, ls-remote lane-origin, gh api commits/develop = der #1594-merge vom 20.11. 16:06:23Z). NICHT hinter #1615 (owner-schiene, OPEN, head 231ebd269735, 'mergeable' ist deren PR nicht develop) und NICHT auf #1726 (geerbte gate-wand, andere dateien). grund: ihre lane hat den fall AM develop-head reproduziert, und 210 ist der PRODUKTIONS-fall der trennung GATE/BEWEIS/PRODUKTION. ueberschneidung mit #1615 in beiden dateien wird orthoogonal gehalten + 'OVERLAP'-zeile im PR-body fuer meine merge-reihenfolge.
