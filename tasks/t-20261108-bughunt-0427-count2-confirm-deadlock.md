---
id: t-20261108-bughunt-0427-count2-confirm-deadlock
card_number: "0427-135"
card_short_title: "repeat test hangs (count=2)"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w135-count2
kanban_status: closed
kanban_lane: closed
kanban_summary: A clean go test -count=2 (without ambient Core) ends terminating rather than blocking; the confirm path leaks no pipe-holding…
kanban_title: "0427-135 · repeat test hangs (count=2)"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/compose-host-isolation/round-9.md"]
---
- [x] t-20261108-bughunt-0427-count2-confirm-deadlock · Bug Hunt v0.4.27: Wiederholtest-Hänger im Bestätigungspfad #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w135-count2 · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/compose-host-isolation/round-9.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w135-count2  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
A clean `go test -count=2` (without ambient Core) ends terminating rather than blocking; the confirm path leaks no pipe-holding goroutine. Regression in a CI-covered path.

## Problem (fund from compose acceptance, round 9, F1)
`recordDeploymentBeforeMutation` (cmd/baha deployment_record :551, consent==nil branch) leaves a goroutine holding a pipe on a truly clean host — `go test` never terminates, `-count=2` blocks. A contaminated image (ambient core triggers confirm) is green; `-count=1` on fresh runners is green => CI never caught it. Transcripts: /tmp/c2-matrix.out (lane 0427-110).

## Acceptance
- Deterministic repro (count=2, clean host) as a test or documented CI path; fix in the confirm-retry lifecycle; no leaking goroutine after a failed/aborted confirm.

## Dependencies and file ownership
None. Write-set: cmd/baha (deployment_record/confirm lifecycle) + tests.

## Resolution (dropped 2026-11-08)
Not a product defect. Triple-negative reproduction: develop 07ae6c3e9 and the compose WIP head e291fba9a both terminate under clean `-count=2`; SIGQUIT dumps show no pipe-waiting goroutine. The original hang witness came from invalidated FIFO cells plus ambient load on the compose host (round-1.md details). No product change, no PR.
