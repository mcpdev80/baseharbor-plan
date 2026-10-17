---
id: t-20261017-podman-acceptance-typed-consent
type: bug
areas: [ci]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (Podman acceptance consent)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-podman-acceptance-typed-consent · Podman acceptance: honor fresh typed provider consent #task #release/v0-4-26 #status/active #view/active #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 (Podman acceptance consent) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (Podman acceptance consent)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make the existing clean-state native Podman acceptance journey exercise the supported typed provider-consent protocol without weakening fail-closed product behavior.

## Scope

Own the lifecycle step in `.github/workflows/podman-acceptance.yml` and immediately required existing acceptance helpers/regressions. Reuse the existing plan and consent authority. No new workflow, consent bypass, generic runner framework or unrelated product changes.

## Acceptance

- Obtain a fresh operation plan and supply its required confirmation stages; stale/foreign plan IDs and missing consent must block.
- Preserve separate destructive-data authorization when required.
- On clean acceptance state, execute application-scoped SQL/cache apply and prove authenticated SQL and Valkey verification.
- Do not depend on warm state or weaken incomplete-inventory handling.
- Independently review the change, then Qwen retests the exact corrected SHA on the authorized native environment before release.

## Required checks

Focused workflow policy/actionlint and helper regressions as selected by the trusted CI; one targeted native Podman acceptance run including consent-negative cases. No full release matrix.

## Dependencies and file ownership

- No unfinished product-task dependency is established. Before assignment, verify the exact existing CI lane, native fixture and non-overlapping write ownership. A missing trusted lane is an explicit prerequisite, never a self-exemption.
- Implementation belongs to an assigned development session; Qwen performs live testing and retesting only.
- Must be fixed and independently retested before v0.4.26 release (Maintainer instruction, 2026-10-17). Release preparation must depend on this task.

## Handoff

- 2026-10-17: Claim acquired for isolated workflow/acceptance-helper correction. No native/live environment execution in this session; Qwen owns native retest after independent review. Scope limited to existing Podman acceptance workflow and direct regressions; no consent bypass or inventory weakening.

- 2026-10-17: Maintainer-authorized intake from Qwen's supplied pre-freeze audit; this session did not independently reproduce the native failure. Fresh-state acceptance currently invokes apply without typed consent and receives `impact-confirmation-required` (`complete:false`, `confirmations_required:2`). The audit reports that fresh consent makes apply and verification succeed. This is a test/integration mismatch. Source: `d54ac358fb6a6b256164ac2689a33e981c013baa`.
- Discussion/evidence intake: [baseharbor#987](https://github.com/mcpdev80/baseharbor/issues/987). Unassigned, not implemented or accepted. No private machine identifiers, addresses, local paths or credentials included.
