---
id: t-20261116-r28-bug-destroy-diagnostics
card_number: "0428-107"
card_short_title: "Explain destroy owner failures"
type: bug
areas: [lifecycle]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "baha app destroy --yes --verbose printed the same generic retained provider ownership error as nonverbose; neither affected "
kanban_title: "0428-107 · Explain destroy owner failures"
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-destroy-diagnostics · Explain destroy owner failures #task #release/v0-4-28 #status/planned #area/lifecycle #kind/bug

## Goal

`baha app destroy --yes --verbose` printed the same generic `retained provider ownership` error as nonverbose; neither affected provider ID nor canonical owner/renderer path was identified.

## Reproduction (2026-11-16 J-Commerce live test)

Use failed J-Commerce registration and compare normal/verbose destroy output.

## Acceptance

- Return structured, redacted per-provider cause: instance ID, expected owner, observed canonical state, failed verification and safe next step; same useful diagnostics for standalone app destroy and installation destroy. Avoid logging secrets.
- Preserve existing BaseHarbor safety, immutable candidate consent, source ownership and shared-provider isolation. Never bypass preflight or delete foreign resources.
- Include positive/negative regressions and classify baseline-red vs candidate-green.

## Required checks and CI mapping

- Discover all affected existing tests; implement smallest causal regression and register it in existing package tests / PR-gate selection. Prove touched paths select the test and unrelated paths do not trigger unnecessary full native gates.
- Capture exact SHA, test ID, actual CI check/trigger and passing run URL. Where behavior is common to Docker and rootless Podman, produce independent native evidence in existing appropriate integration/release qualification gates. No separate CI framework.
- Reproduction is local user evidence; its observations must be verified in code before declaring a product fix.

## Dependencies and file ownership

- Coordinate shared CLI, wizard, lifecycle and provider files with existing v0.4.28 CLI redesign owners; no competing writes or blanket permissions.

## Handoff

- Planned only. No implementation, PR, merge or acceptance claimed. Source: 2026-11-16 J-Commerce guided-init/apply/destroy/reset transcript supplied by Owner.
