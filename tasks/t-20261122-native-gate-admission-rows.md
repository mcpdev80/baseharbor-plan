---
id: t-20261122-native-gate-admission-rows
card_number: "0428-230"
card_short_title: "native gate rows for"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Owner (scripts und pr-gate-coverage.json sind Owner-scope; ausfuehrende lane nur mit ausdruecklicher benutzer-beauftragung, derselbe fall wie 0428-228)
kanban_status: active
kanban_lane: active
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
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md"]
---

- [ ] t-20261122-native-gate-admission-rows · native gate rows for env-destroy #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** Owner (scripts und pr-gate-coverage.json sind Owner-scope; ausfuehrende lane nur mit ausdruecklicher benutzer-beauftragung, derselbe fall wie 0428-228)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Owner (scripts und pr-gate-coverage.json sind Owner-scope; ausfuehrende lane nur mit ausdruecklicher benutzer-beauftragung, derselbe fall wie 0428-228)  
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

Erweiterung des vertrags, gemessen an develop 1ff16925c4e: neben den acht bereits benannten komponenten fehlen auch die acht test-quellen von PR 1750 und die drei ci_integration_operator-quellen in den native_checks-zeilen - deshalb ist PR . Selected Runtime an den gehopften heads 5d47569f337 (#1750) und ce5cf8f3037 (#1753) weiterhin SKIPPED, obwohl PR 1755 gemergt ist. rezept und feldformen: evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md. Karte 0428-234 ist als superseded in diese karte folded.
