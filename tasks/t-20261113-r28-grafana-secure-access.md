---
id: t-20261113-r28-grafana-secure-access
card_number: "0428-013"
card_short_title: "Secure Grafana operator access"
type: task
areas: [security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Integrate optional Grafana operator access with existing installation origin, authenticated Core/OIDC boundary and least priv"
kanban_title: "0428-013 · Secure Grafana operator access"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-runtime, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-secure-access · Secure Grafana operator access #task #release/v0-4-28 #status/planned #area/security #kind/task

## Outcome and scope

Integrate optional Grafana operator access with existing installation origin, authenticated Core/OIDC boundary and least privilege. Do not enable anonymous admin, public default exposure, cross-tenant leakage or unrestricted iframe. Validate exact supported native Grafana auth path before implementation.

## Acceptance

Positive and negative proof for authorized/denied users, session expiry, URL origin and no public admin by default. No second authorization source or permanent broad token.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-runtime, t-20261113-r28-console-api-contracts.
- Existing gateway/management UI auth registration belongs exclusively to this slice after prerequisites; Grafana runtime worker must not edit these shared files.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Focused HTTPS/OIDC/tenant/redirect/secret tests and relevant native auth journey; exact check/trigger documented.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
