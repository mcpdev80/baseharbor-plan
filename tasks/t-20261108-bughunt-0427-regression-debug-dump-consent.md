---
id: t-20261108-bughunt-0427-regression-debug-dump-consent
card_number: "0427-129"
card_short_title: "debug goroutine dump on"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: ""
owner: lane-w129-dbgdump
kanban_status: closed
kanban_lane: closed
kanban_summary: baha up without --confirm-candidate on an already-initialized app repository exits 1 with a clean stderr (no goroutine dump) on…
kanban_title: "0427-129 · debug goroutine dump on"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1439]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-regression-dbgdump/round-1.md","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-regression-dbgdump/act-129-verify.md"]
---

- [x] t-20261108-bughunt-0427-regression-debug-dump-consent · Bug Hunt v0.4.27 (Regression 0427-120): debug goroutine dump on consent denial (develop 0fe53052d) #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/dx #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w129-dbgdump · **Priority:** normal  
    **PR:** [baseharbor#1439](https://github.com/mcpdev80/baseharbor/pull/1439)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-regression-dbgdump/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-regression-dbgdump/act-129-verify.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w129-dbgdump  
**Priority:** normal  
**PRs:** [baseharbor#1439](https://github.com/mcpdev80/baseharbor/pull/1439)  
**Source:** 
<!-- /generated:links -->

## Goal

`baha up` without `--confirm-candidate` on an already-initialized app repository exits 1 with a clean stderr (no goroutine dump) on develop; 0427-120 PR #1439 must be re-merged or back-ported so the develop build reflects the removed debug dump.

## Scope

- In scope:
  - Ensure develop build `0fe53052d...` includes the consent-stack-removal fix from PR #1439 (merge into develop or re-apply removal in `cmd/baha/deployment_record.go` ~line 522-526).
  - In scope files: `cmd/baha/deployment_record.go`.
- Out of scope: consent semantics, exit-code defects (tracked by 0427-128/other cards).

## Acceptance

- `baha up` (plain/yes) without `--confirm-candidate` on an app with an existing manifest prints only the candidate block and the consent error; stderr contains no `goroutine` line.
- The regression check passes: build SHA from develop 0fe53052d matches PR #1439 state (i.e., debug dump removed).

## Required checks

- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/deployment_record.go`.
- Shared files: none.

## Handoff

- Current state: debug stack dump still present on develop 0fe53052d; consent denial (plain/yes) still prints stack + error.
- Branch: develop (0fe53052d); PR #1439 merged 2026-11-08 but not yet merged into develop — re-merge / back-port.
- Evidence: stderr log from `~/tests/2026-11-08-linkding` repro (see Baha-Bug-03).
