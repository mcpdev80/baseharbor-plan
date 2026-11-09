---
id: t-20261109-0427-179-flock-not-enforced
card_number: "0427-179"
card_short_title: "0427-179 · Lifecycle flock is"
type: bug
areas: []
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-179-impl
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0427-179 · 0427-179 · Lifecycle flock is
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1515]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-0427-179-flock-not-enforced · 0427-179 · Lifecycle flock is not cross-process enforced on runtime filesystems #task #release/v0-4-27 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-179-impl  
    **PR:** [baseharbor#1515](https://github.com/mcpdev80/baseharbor/pull/1515)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261109-0427-180-dangling-app-lock](t-20261109-0427-180-dangling-app-lock.md)  
**Owner:** lane-0427-179-impl  
**Priority:** not set  
**PRs:** [baseharbor#1515](https://github.com/mcpdev80/baseharbor/pull/1515)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- 2026-11-09 r2 correction (lane-0427-179-r2-fix): the r1 blocking gap (b) is
  fixed. The not-enforcing filesystem condition now fails closed IMMEDIATELY in
  the app CLI path (no 15s retry) with the actionable remediation text.
  Implementation: export `ErrLockFilesystemNotEnforcing` at the stableid
  boundary (internal/stableid/lock_unix.go) and add a `LockProbeFunc` test seam
  (internal/stableid/lock_probe.go); cmd/baha/application_lifecycle_lock.go now
  detects the condition via errors.Is and returns immediately; command-path
  regressions added (cmd/baha/application_lifecycle_lock_test.go) proving
  immediate fail-closed + remediation, and that genuine contention still enters
  the bounded retry. Existing cross-process/fail-closed regressions, #1507
  fairness and per-app dotfile semantics untouched. Commit 11b8bd44 integrated
  as the single new commit on PR #1515 head (branch 0427-179-flock-enforcement,
  now 11b8bd44; sibling branch 0427-179-r2-fix deleted). Local targeted checks
  green on the exact candidate. CI on the exact SHA needs PR #1515 marked ready
  (Owner; .github/** is Owner scope — never rerun by the lane).
  Evidence: evidence/bughunt-flock-enforcement-cells/round-2.md.

## Task Note
Hunt H-P5 (evidence: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp5.md, FINDING 1, confirmed in docker cell on kernel 7.0 host): regular-file flock() mutual exclusion is NOT enforced across processes inside the runtime cells (C/python/shell probes all acquired a lock an unrelated child already held), while in-process contends. Every lifecycle guarantee built on `.installation.lock` / per-app dotfiles (incl. today's #1507 fairness work) is therefore advisory-only exactly where BaseHarbor ships. Required: a validity-enforced mutual-exclusion primitive (e.g. O_EXCL lockfile + holder-liveness verification, or flock probe at acquire that fails closed when the kernel/fs does not enforce), plus a cell regression that proves cross-process contention actually blocks.
