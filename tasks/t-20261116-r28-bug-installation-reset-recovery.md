---
id: t-20261116-r28-bug-installation-reset-recovery
card_number: "0428-101"
card_short_title: "Unblock full installation rese"
type: bug
areas: [lifecycle]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "baha destroy --yes selects all owned resources, asks for two current-plan confirmations plus deletion consent, but aborts be"
kanban_title: "0428-101 · Unblock full installation rese"
priority: critical
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-installation-reset-recovery · Unblock full installation reset #task #release/v0-4-28 #status/planned #area/lifecycle #kind/bug

## Goal

`baha destroy --yes` selects all owned resources, asks for two current-plan confirmations plus deletion consent, but aborts because application destroy preflight fails on retained provider ownership. Global XDG state and Core resources remain; user had to manually delete Docker resources and BaseHarbor directories.

## Reproduction (2026-11-16 J-Commerce live test)

Start Core; create the same failed J-Commerce app registration; run `baha destroy --yes`; consent three times. Inspect cleanup report: app FAILED, target-runtime SKIPPED, xdg-data/config SKIPPED.

## Acceptance

- An explicitly authorized installation destroy handles unmaterialized/broken app records without bypassing authorization or deleting ambiguous/foreign resources. Clearly enumerate preserved items, finish verifiable owned Core/provider/registry cleanup and rerun idempotently. Native Docker and rootless Podman coverage; no broad docker prune.
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
