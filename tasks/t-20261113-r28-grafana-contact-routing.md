---
id: t-20261113-r28-grafana-contact-routing
card_number: "0428-031"
card_short_title: "Grafana alert contact routing"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Implement opt-in Grafana OSS notification policy/contact point lifecycle with secret-safe owner configuration. No default…
kanban_title: "0428-031 · Grafana alert contact routing"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-alerts, t-20261113-r28-grafana-secure-access]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-contact-routing · Grafana alert contact routing #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-alerts](t-20261113-r28-grafana-alerts.md), [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-alerts](t-20261113-r28-grafana-alerts.md), [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md)  
**Required by:** [t-20261113-r28-grafana-native-proof](t-20261113-r28-grafana-native-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Implement opt-in Grafana OSS notification policy/contact point lifecycle with secret-safe owner configuration. No default external notifications or permanent broad credentials.

## Acceptance

Configured test contact route accepted, invalid/foreign URL and secrets denied, removal/rotation safe, no unsolicited notifications.

## Dependencies and exclusive file ownership

- Only start implementation once dependencies in frontmatter are accepted and an actual interface is available. Do not wait on independent cards.
- **Owned files:** New Grafana alerting contacts/routing assets and tests only; no rule expressions or gateway edits.
- No other worker may change these files concurrently. File overlap requires explicit Coordinator serialization before coding.

## Worker instructions (local 256k LLM)

1. Fetch the current exact product head and this task's accepted predecessors. Read only named source paths and their direct tests, not the entire repository or all backlog.
2. Check current behavior before editing. If already delivered, present exact code/test SHA and ask Coordinator to mark the card superseded; do not duplicate.
3. Implement ONLY the Goal in owned files, using the existing Core authority/transport and native provider patterns; do not add a new API, database, custom monitoring engine or provider capability.
4. Add one executable positive and one negative test for the Acceptance, identify exact test -> existing CI check -> path/trigger -> real result. If missing CI routing, hand off to assigned shared CI owner rather than silently skipping.
5. Run the smallest relevant checks and selected native proof where required. Open one limited PR to the product's normal integration branch; hand off head SHA, files, observed test output, exact gate run and unresolved issues.
6. **Worker never reviews/merges. Codex is reviewer and merger** after required green exact-HEAD checks and real negative tests. Coordinator updates task state and schedules up to 5 ready non-overlapping workers; no release/tag authorization.

## Handoff

Unassigned. No code or acceptance evidence yet.
