---
id: t-20261116-r28-bug-apply-consent-ux
card_number: "0428-106"
card_short_title: "Clarify apply candidate consen"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Interactive baha app apply accepted [y/N] y but then required re-execution with --confirm-candidate; baha app apply j-commer"
kanban_title: "0428-106 · Clarify apply candidate consen"
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

- [ ] t-20261116-r28-bug-apply-consent-ux · Clarify apply candidate consent #task #release/v0-4-28 #status/planned #area/cli #kind/bug

## Goal

Interactive `baha app apply` accepted `[y/N] y` but then required re-execution with `--confirm-candidate`; `baha app apply j-commerce` from repo emitted misleading `no registered deployment` though `baha app apply` resolves the manifest. Not a request to weaken the security gate.

## Reproduction (2026-11-16 J-Commerce live test)

Run `baha app apply` from repo on first candidate and accept initial prompt; inspect additional confirm hash and next-step instructions, then compare named and unnamed app arguments.

## Acceptance

- Preserve exact candidate-bound authorization and noninteractive fail-closed behavior; make separate approvals explicit before prompting, show concise actionable command and context. Clarify name-vs-repository lookup and error diagnosis with regression tests.
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
