---
id: t-20261125-hunt33-unguarded-git-sudo
card_number: "0428-294"
card_short_title: "hunt33-unguarded-git-sudo"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-294 · hunt33-unguarded-git-sudo
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261125-hunt33-unguarded-git-sudo · 0428 hunt H-V33: hunt33-unguarded-git-sudo #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Fail with a clear, actionable prerequisite error when BaseHarbor reaches an unguarded host-side `git` or `sudo` invocation and that executable is unavailable.

## Current-source recheck — 2026-11-25

Rechecked BaseHarbor `develop` at `7bdeae95ccf0ce0d2fe39ae6d4c884402268995d`.

- `internal/development/pinned_git_archive.go` still invokes `git archive` directly at line 48 with no local availability check.
- `cmd/baha/dev_hosts.go` still invokes `sudo` directly at line 206 when the process is not root.
- The H-V33 evidence also named `internal/openbao/bootstrap_auth.go` for sudo, but the current file contains policy text and no Go `sudo` invocation. Drop that stale path.
- PostgreSQL commands in `runtime_credential_rotation.go` and `shared_backends_runtime.go` are sent through `Runtime.ExecProject`, which maps to Compose `exec` inside a service container. They are image prerequisites, not host-runner executables; do not add them to this host-executable task.

Evidence: [git archive path](https://github.com/mcpdev80/baseharbor/blob/7bdeae95ccf0ce0d2fe39ae6d4c884402268995d/internal/development/pinned_git_archive.go), [sudo hosts path](https://github.com/mcpdev80/baseharbor/blob/7bdeae95ccf0ce0d2fe39ae6d4c884402268995d/cmd/baha/dev_hosts.go), [Compose ExecProject implementation](https://github.com/mcpdev80/baseharbor/blob/7bdeae95ccf0ce0d2fe39ae6d4c884402268995d/internal/runtime/compose.go).

## Scope

- Add preflight availability checks for only the remaining host `git` and `sudo` call sites, matching established `exec.LookPath` error handling.
- Report which executable is required and a safe remediation; do not expose command arguments or secrets.
- Preserve authorization, host mutation consent, and existing runtime/ownership checks. Availability checks must not execute a privileged command or alter hosts on their own.
- Remove the stale OpenBao and in-container PostgreSQL claims from this card; provider-image prerequisites remain a separate H-V33 concern.

## Acceptance

- Missing `git` fails before attempting archive extraction with a clear prerequisite error; existing successful archive behavior remains unchanged.
- Missing `sudo` fails before launching the hosts writer with a clear prerequisite error; the root execution path does not require sudo.
- Focused tests cover both missing-executable branches and the normal/root path using existing package test discovery.
- Bind the tests to the existing relevant check; no new CI gate or pipeline. Record exact source SHA, test IDs, selected check/trigger, and actual result.

## Dependencies and file ownership

- Product implementation ownership: BaseHarbor development and workstation-hosts areas. Coordinate the two source paths if they share a PR.
- No change to authorization or host-mutation consent semantics.

## Handoff

Open for implementation. The current-source audit corrects the original H-V33 host-exec list; no product code was changed in this planning cleanup.
