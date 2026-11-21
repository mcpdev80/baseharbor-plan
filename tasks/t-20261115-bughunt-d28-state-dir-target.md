---
id: t-20261115-bughunt-d28-state-dir-target
card_number: "0427-189"
card_short_title: "bf01 state-dir isolation"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: "Codex (Owner-directed wait-card closeout, 2026-11-21)"
kanban_status: review
kanban_lane: review
kanban_summary: "BF-01 (blocker): BASEHARBORSTATEDIR does not isolate target selection; target switch reads foreign registrations. Found on…"
kanban_title: 0427-189 · bf01 state-dir isolation
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1585]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-2.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-3.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-4.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-21/bf01/round-5.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44842355914"]
---

- [ ] t-20261115-bughunt-d28-state-dir-target · BF-01 target selection ignores BASEHARBOR_STATE_DIR (reads foreign registrations) #task #release/v0-4-27 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Owner-directed wait-card closeout, 2026-11-21)  
    **PR:** [baseharbor#1585](https://github.com/mcpdev80/baseharbor/pull/1585)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-1.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-2.md), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-3.md), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/bf01/round-4.md), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-21/bf01/round-5.md), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/44842355914)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** Codex (Owner-directed wait-card closeout, 2026-11-21)  
**Priority:** not set  
**PRs:** [baseharbor#1585](https://github.com/mcpdev80/baseharbor/pull/1585)  
**Source:** 
<!-- /generated:links -->

## Goal

BF-01 (blocker): BASEHARBOR_STATE_DIR does not isolate target selection; target switch reads foreign registrations. Found on develop 0e9ccb582 during H-D28.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
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

**Zwischenstand 15.11.:** BF-01-Kandidat veroeffentlicht: Draft PR mcpdev80/baseharbor#1585 (Branch lane-0428-fix-bf01-v2, head 8041a9f0119e390e03533082da05f9d62bdcc7e1, base develop 0e9ccb582; Merge-Frost: Draft, kein Merge). Gehosteter run CI PR #1585, run 43684179345, terminal success. Evidenz: evidence/r28-welle1-2026-11-15/bf01/round-1.md (round-1, END-Zeile korrigiert) und round-2.md (Konsolidierung, Rot-Zustand ehrlich zurueckgenommen: Test ist auf base gruen, Kandidat haertet die Grenze strukturell). PR #1584 war dasselbe Material mit veralteter Historie und ist geschlossen.

*__Ende*

**Codex closeout continuation — 2026-11-21:**

- Took over under the Owner instruction to close wait cards except #1615. PR #1585 remains Draft and open; exact updated head `b50bc6a8053d19438d87466079c7a1ec06abfcbc`, base `develop` at `40cb28c758b02960356434b630086a341ebe1738`, GitHub reports mergeable. Product diff remains exactly six BF-01 files.
- Local checks on that head passed: `go test ./cmd/baha -run '^TestStateDirIsolatesTargetSelection$' -count=1` and `go test ./internal/orgconfig ./internal/deployment -count=1`; `git diff --check` passed.
- Exact hosted Draft run [44842355914](https://github.com/mcpdev80/baseharbor/actions/runs/44842355914) is still in progress. Four Go shards are running; source/routing passed. Draft suppresses full PR selection. Await terminal results before changing PR readiness or declaring completion.

**Zwischenstand 15.11. Runde 4 (Review-r1 abgearbeitet):** Kandidat head 13e096fc66d90e20b8f262b7f58024790c62b0e5 auf lane-0428-fix-bf01-v2 (Draft PR mcpdev80/baseharbor#1585, base develop 0e9ccb582; Merge-Frost). Regression rot auf reinem develop (isolation_test.go:105) und gruen auf dem Kandidaten; LV-02-Welt-schreibgeschuetzter Guard in ea3a0705e integriert; Throwaway-Merge-Zeugnis mit 756b2be7e: go vet + internal/orgconfig (42 Zellen) + TestWorld/TestStateDir + BF-01-Zelle gruen. Gehosteter run 43692224878 terminal completed/success. Evidenz: evidence/r28-welle1-2026-11-15/bf01/round-4.md.


**Current exact-head gate (2026-11-21):** PR #1585 head `b50bc6a8053d19438d87466079c7a1ec06abfcbc` remains Draft on develop `40cb28c758b02960356434b630086a341ebe1738`. Run 44842355914 is terminal failure: CLI shards fail on the separate managed-operator auth fixtures; packages fails the Loki client-certificate fixtures, which are green on superseding #1734 run 44853938826. `TestStateDirIsolatesTargetSelection` is assigned to cli-2 by the existing SHA partition, but the compact hosted failure report is not an exact per-test PASS witness. Keep 0427-189 active; after shared gates clear, collect exact-head required CI and explicit test PASS evidence before merge/acceptance. #1615 untouched. Full current details: [round-5](../evidence/r28-welle1-2026-11-21/bf01/round-5.md).
**Codex independent review (2026-11-21):** REQUEST CHANGES on exact head `70d39070f4ad2618b120e7a5438fdff7ed94f665` after successful exact-head CI run `44933797592`; the diff is six BF-01 files, but base-to-head history contains foreign-authored merge `55a8c0f`, so replay task-owned commits from current develop and rerun selected checks before acceptance.
