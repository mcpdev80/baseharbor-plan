---
id: t-20261125-hunt33-go-runtime-prereq
card_number: "0428-299"
card_short_title: "hunt33-go-runtime-prereq"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-299 · hunt33-go-runtime-prereq
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

- [ ] t-20261125-hunt33-go-runtime-prereq · 0428 hunt H-V33: hunt33-go-runtime-prereq #task #release/v0-4-28 #status/planned #view/ready #kind/task
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

Keep the cross-process lifecycle-lock probe fail-closed and make the Go toolchain fallback explicit on platforms where the embedded Linux/AMD64 probe is unavailable.

## Current-source recheck — 2026-11-25

Rechecked BaseHarbor `develop` at `7bdeae95ccf0ce0d2fe39ae6d4c884402268995d`. `internal/stableid/lock_probe.go` embeds a probe binary and uses it on Linux/AMD64. Other platform/architecture cases call `runToolchainProbe`, which executes `go build` without first checking whether `go` is available. The lock probe is a safety check: an unavailable probe must not be treated as a verified lock.

Evidence: [current lock probe](https://github.com/mcpdev80/baseharbor/blob/7bdeae95ccf0ce0d2fe39ae6d4c884402268995d/internal/stableid/lock_probe.go).

## Scope

- Preserve the embedded helper path on Linux/AMD64; do not add a Go dependency to that path.
- On fallback platforms, detect a missing Go executable and return a clear prerequisite error that preserves the fail-closed result.
- State the toolchain requirement only for fallback platforms that are in the supported-host contract. Do not expand support to WSL2 or macOS through this card.
- Do not replace the embedded helper or add a new runtime framework.

## Acceptance

- Linux/AMD64 uses the embedded helper and succeeds without `go` or a module cache.
- Fallback platforms with a working Go toolchain keep the current build-and-probe behavior.
- Fallback platforms without `go` produce a stable actionable error and never report that cross-process locking was verified.
- Focused tests cover helper selection, missing-Go fallback, and fail-closed behavior through normal package discovery.
- Record the exact test/package, existing CI check and trigger, and actual candidate-SHA result; no new CI gate.

## Dependencies and file ownership

- Product area: `internal/stableid` and its lifecycle-lock callers. Keep the change narrow and coordinate if shared lock-probe files are already owned.

## Handoff

Open for implementation. No product code or test was changed in this planning audit.
