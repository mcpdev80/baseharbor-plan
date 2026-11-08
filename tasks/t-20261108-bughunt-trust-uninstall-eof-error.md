---
id: t-20261108-bughunt-trust-uninstall-eof-error
card_number: "0427-161"
card_short_title: "Uninstall prompt EOF I/O error"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w161-eoftrust
kanban_status: review
kanban_lane: review
kanban_summary: "Uninstall prompt shares the install path io.EOF guard: EOF = clean cancel with \"Host trust unchanged.\" and exit 0-style…"
kanban_title: 0427-161 · Uninstall prompt EOF I/O error
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261108-bughunt-appnew-eof-cancel-prompts]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1485]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx1.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-trust-uninstall-eof-error · Bug Hunt v0.4.27: Trust prompt EOF error #task #release/v0-4-27 #status/review #view/review #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w161-eoftrust · **Priority:** normal  
    **PR:** [baseharbor#1485](https://github.com/mcpdev80/baseharbor/pull/1485)  
    **Needs:** [t-20261108-bughunt-appnew-eof-cancel-prompts](t-20261108-bughunt-appnew-eof-cancel-prompts.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261108-bughunt-appnew-eof-cancel-prompts](t-20261108-bughunt-appnew-eof-cancel-prompts.md)  
**Owner:** lane-w161-eoftrust  
**Priority:** normal  
**PRs:** [baseharbor#1485](https://github.com/mcpdev80/baseharbor/pull/1485)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Uninstall prompt shares the install path io.EOF guard: EOF = clean cancel with "Host trust unchanged." and exit 0-style semantics consistent with card 138; regression in the existing trust-prompt field.

## Problem (source evidence in the dossier)
EOF (Ctrl-D) at the trust uninstall prompt surfaces "read host trust removal approval: read /dev/stdin: input/output error" instead of a clean unchanged-abort; the install path already guards io.EOF but uninstall does not. Source: hunt H-X1 BF-06/BF-26 (robustness, fail-closed).

## Acceptance
Uninstall prompt shares the install path io.EOF guard: EOF = clean cancel with "Host trust unchanged." and exit 0-style semantics consistent with card 138; regression in the existing trust-prompt field.

## Dependencies and file ownership
Depends on the shared cancel-path decision of 0427-138. Write-set: cmd/baha hosttrust uninstall prompt reader.
