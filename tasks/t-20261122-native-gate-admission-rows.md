---
id: t-20261122-native-gate-admission-rows
card_number: "0428-230"
card_short_title: "native gate rows for"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-230 · native gate rows for
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

- [ ] t-20261122-native-gate-admission-rows · native gate rows for env-destroy #task #release/v0-4-28 #status/planned #view/ready #kind/task
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


## Why

A bug-hunt census (evidence/r28-welle5-2026-11-22/native-gate-admission/befund-1.md, plan 8ceac4228) measured that the
PR-level native gate selector never admits the environment-destroy components, so a PR that changes only those sources
gets `matrix={"include":[]}` from `PR · Native gate plan` (job 137070848046 on head 2f0f80786d8) while the actual test
execution happens only through the coreless application shards (`scripts/pr-gate-plan.py:1171`, `:1231`). The native
check row is therefore an admission gap, not an execution gap: the planner file itself exists at develop 8b9a8f50645
(`git ls-tree` = blob 4259fbf665) and no warning annotation was ever emitted.

## Findings to carry into the edit

- Selection loop is `scripts/validate-pr-gate-coverage.py:74-88` (function starts at line 66) and only reads rows from
  `coverage["native_checks"]` with `selection_scope == "focused"`.
- Eight components have `runtime_specific` or `required_test_names` but no `native_checks` row: the env-destroy
  integration test source (docker + podman), `runtime.podman-service-stop` and its test component (podman,
  TestSelectedStopAcceptsPinnedContainerName), and the six `cmd/baha/*runtime_test.go` application components
  (docker + podman).
- The catalog at develop 8b9a8f50645 and at head 2f0f80786d8 is byte-identical, so this is not caused by any open PR.

## Acceptance

- `scripts/pr-gate-coverage.json` gains `native_checks` rows that list the components above in `source_components`, so
  `PR · Native gate plan` selects at least one native check for a PR that only touches those paths.
- `scripts/test_pr_gate_coverage.py` (or the existing validator test group) asserts the new rows in hosted CI; no test
  may pass by being skipped.
- One follow-up PR CI run shows `Native gates selected: true` with the executed job ids recorded in this card's
  evidence.

## Owner scope

`scripts/**` is Owner-scope for lanes (AGENTS write bans): the edit is made by the Owner or by a lane explicitly
commissioned for it; lanes only re-run and witness.
