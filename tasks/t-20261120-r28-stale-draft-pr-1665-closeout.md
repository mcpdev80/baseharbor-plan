---
id: t-20261120-r28-stale-draft-pr-1665-closeout
card_number: "0428-176"
card_short_title: "restack with evidence or close"
type: maintenance
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w176-pr1665-1665-closeout
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-176 · restack with evidence or close
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1665]
sources: []
blocker: "write-set collision mit #1684 (management_ui.go, perses_runtime.go) + perses-runtime-smoke rot ohne 0428-177; trigger: #1684 gemergt oder 0428-177 landet"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-stale-draft-pr-1665-closeout · Stale draft PR #1665 on parked card 0428-082: restack with evidence or close #task #release/v0-4-28 #status/active #view/active #kind/maintenance
    <!-- generated:card -->
    **Owner:** w176-pr1665-1665-closeout  
    **PR:** [baseharbor#1665](https://github.com/mcpdev80/baseharbor/pull/1665)  
    **Blocker:** write-set collision mit \#1684 (management\_ui.go, perses\_runtime.go) + perses-runtime-smoke rot ohne 0428-177; trigger: \#1684 gemergt oder 0428-177 landet  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w176-pr1665-1665-closeout  
**Priority:** not set  
**PRs:** [baseharbor#1665](https://github.com/mcpdev80/baseharbor/pull/1665)  
**Source:** 
<!-- /generated:links -->








  - close: `gh pr view 1665 --json state` reports `CLOSED`, plus a per-file table proving each draft file is already present on `develop` or on an open PR with a named owner card; or
  - restack: the branch is rebased onto current `develop`, the PR base points at `develop`, it is no longer a draft, and one `pull_request` run at the exact head reaches a terminal state with run id and conclusion in the evidence file.












  dashboard-commits 3a4599539 / 47d4ff298 / 081dc926d / dda073da4 sind nicht gemergt - echter 0428-082 inhalt.
  cmd/baha/app_status_result.go und docs/spec/*. und #1684 (0428-083) traegt management_ui.go, perses_runtime.go,
  perses_datasource_lifecycle.go, app_apply_lifecycle.go - paralleles schreiben in dieselben dateien ist §4.3
  verboten, solange kein integrationsplan publiziert ist.
  die erwartbare signatur des refactor-on-top (delete perses_runtime/security, add provider_registration/migration).
  [#1665]) bleibt unveraendert, ICH fuehre dort den blockerverweis nach. WIEDERAUFNAHME: restack in eigener lane auf
  develop-spitze (aktuell 96f2ae11a25a), sobald #1684 gemergt oder 0428-177 gelandet ist.


---
