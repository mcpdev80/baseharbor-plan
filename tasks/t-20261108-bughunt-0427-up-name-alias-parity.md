---
id: t-20261108-bughunt-0427-up-name-alias-parity
card_number: "0427-130"
card_short_title: "baha up NAME abgelehnt"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: ""
owner: lane-w130-upalias-r2
kanban_status: review
kanban_lane: review
kanban_summary: baha up NAME resolves the registered application NAME identically to baha app up NAME; the top-level alias exposes the full…
kanban_title: 0427-130 · baha up NAME abgelehnt
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1459]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-bughunt-0427-up-name-alias-parity · Bug Hunt v0.4.27: baha up NAME rejected although app up [NAME] documented #task #release/v0-4-27 #status/review #view/review #area/dx #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w130-upalias-r2 · **Priority:** normal  
    **PR:** [baseharbor#1459](https://github.com/mcpdev80/baseharbor/pull/1459)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w130-upalias-r2  
**Priority:** normal  
**PRs:** [baseharbor#1459](https://github.com/mcpdev80/baseharbor/pull/1459)  
**Source:** 
<!-- /generated:links -->

## Goal

`baha up NAME` resolves the registered application NAME identically to `baha app up NAME`; the top-level alias exposes the full documented argument surface.

## Scope

- In scope: align the top-level `up` argument parser (`cmd/baha/runtime.go`) with `app up` (`cmd/baha/app_lifecycle.go`) so the optional positional NAME is accepted; add parity test.
- Out of scope: consent semantics.

## Acceptance

- `baha up NAME --yes --plain` outside a repository resumes the registered deployment NAME (same result as `baha app up NAME`).
- Parser parity test: `up` and `app up` accept the identical flag/argument grammar.

## Required checks

- CLI parser unit test asserting `up <NAME>` parses; machine/CLI parity test against `app up`; documented in the existing cli-command grammar suite (no new CI framework).

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/runtime.go`, `cmd/baha/app_lifecycle.go`.
- Shared files: coordinate through the owning task.

## Handoff

- Found 2026-11-08 on develop 0fe53052d (build 0.4.11), test host 192.168.6.178.
- Report: ~/dev/Tests/Baha-Bug-09-up-name-vs-app-up-name.md
