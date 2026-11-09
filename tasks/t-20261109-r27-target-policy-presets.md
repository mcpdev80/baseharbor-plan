---
id: t-20261109-r27-target-policy-presets
card_number: "0427-186"
card_short_title: "Editable Target policy presets"
type: feature
areas: [remote, deployment]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "mcpdev80 (PR #1514)"
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: "0427-186 · Editable Target policy presets"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-connection-client]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1514]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-r27-target-policy-presets · Target: editable best-practice deployment policy presets #task #release/v0-4-27 #status/active #view/active #area/deployment #area/remote #kind/feature
    <!-- generated:card -->
    **Owner:** mcpdev80 (PR \#1514) · **Priority:** high  
    **PR:** [baseharbor#1514](https://github.com/mcpdev80/baseharbor/pull/1514)  
    **Needs:** [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md)  
**Required by:** [t-20261109-r27-local-delta-delivery](t-20261109-r27-local-delta-delivery.md)  
**Owner:** mcpdev80 (PR #1514)  
**Priority:** high  
**PRs:** [baseharbor#1514](https://github.com/mcpdev80/baseharbor/pull/1514)  
**Source:** 
<!-- /generated:links -->

## Goal and scope

Implement the Owner-approved [target-preset decision](../decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md) for developer/test/staging/production/custom. Presets are **editable starting values**, not imposed global bans; existing Targets remain backward compatible.

## Verified 2026-11-09

- PR [#1514](https://github.com/mcpdev80/baseharbor/pull/1514) is **OPEN**, not merged, and currently **dirty** against develop; the PR describes itself explicitly as a foundation, not feature acceptance.
- Current slice adds policy defaults, CLI target-create overrides and guided Target wizard editing. These require rebasing and fresh full qualifying CI.
- Still missing: authoritative Core-side policy enforcement at ingress for CLI/API/MCP using verified provenance, operator-authorized editing of existing Target rules, and true negative forged-metadata/dirty-source cases.
- Do not mark accepted on unit tests, PR presence, or client-supplied branch/dirty assertions.

## Acceptance

- Presets editable in wizard and CLI with consistent persisted Target rules; unconfigured legacy Targets unaffected.
- Core evaluates real verified source identity/branch/dirty provenance at authorized candidate ingress and refuses forged evidence.
- Operator can edit an existing Target policy without bypassing authorization.
- Exact-head targeted CI, relevant security negatives, and end-to-end acceptance documented before merging and closing.
- Delta/OCI transfer is tracked separately on 0427-187; no release or tag authorized.
