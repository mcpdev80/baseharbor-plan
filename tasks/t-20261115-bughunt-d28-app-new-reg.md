---
id: t-20261115-bughunt-d28-app-new-reg
card_number: "0427-191"
card_short_title: "bf02 app new registration"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: "Codex (Wait sweep; 2026-11-21)"
kanban_status: closed
kanban_lane: closed
kanban_summary: "BF-02 (UX/documentation): explain that the default baha app new create-only path writes project files but does not register a…"
kanban_title: 0427-191 · bf02 app new registration
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1744]
sources: []
blocker: ""
wait_reason: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-21/bf02-app-new-registration/round-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44879306761"]
---

- [x] t-20261115-bughunt-d28-app-new-reg · BF-02 baha app new writes no registration (only up/apply create state) #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Wait sweep; 2026-11-21)  
    **PR:** [baseharbor#1744](https://github.com/mcpdev80/baseharbor/pull/1744)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-21/bf02-app-new-registration/round-1.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44879306761)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** Codex (Wait sweep; 2026-11-21)  
**Priority:** not set  
**PRs:** [baseharbor#1744](https://github.com/mcpdev80/baseharbor/pull/1744)  
**Source:** 
<!-- /generated:links -->

## Goal

BF-02 (UX/documentation): explain that the default `baha app new` create-only path writes project files but does not register a deployment in the selected Target. Found during H-D28; reverified on current develop `40cb28c758b02960356434b630086a341ebe1738`.

## Scope

- In scope: English and German application-command documentation. Explain the create-only/no-registration result, the meaning of the registered-deployment list, and exact next steps.
- Out of scope: changing `app new`, registration, authorization, or deployment behavior; changing published v0.4.27 artifacts.

## Acceptance

- EN/DE docs explain create-only scaffolding does not register a deployment; choosing `run` is described separately.
- Show the exact follow-up (`baha app init --quick`, then `baha up`) and explain operator sign-in when the selected Target requires it.
- A current-source smoke confirms generated files and no `BASEHARBOR_STATE_DIR` after create-only. Avoid claiming `app list` can be read without operator authentication.
- Strict EN/DE MkDocs, documentation audit, locale parity, and exact required PR checks pass; merge the docs PR before accepting.

## Required checks

- Documentation audit, locale parity, and both strict MkDocs builds are the focused local checks; hosted equivalents plus `PR Selected Checks` must be recorded at the exact PR SHA.
- The behavior smoke is an explicit review witness, not a new test or CI gate.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

2026-11-21: PR #1744 merged after exact hosted run 44879306761; all selected docs/policy/source-format checks passed and no job failed or remained in progress. Merge commit `d2d4ded3dedbb6ef7efdd9dc6ba3c114c5e3a163`; exact PR head `1dcf8d29f02d3cab37653edbe0bda0bfccd6d831`, base `develop` `40cb28c758b02960356434b630086a341ebe1738`. Current-source create-only smoke, documentation audit, locale parity, both strict MkDocs builds, and diff check passed. Clarification is on current develop and is not part of the published v0.4.27 tag. Full evidence: [round-1](../evidence/r28-welle1-2026-11-21/bf02-app-new-registration/round-1.md).
