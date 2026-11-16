---
id: t-20261116-r28-bug-failed-apply-destroy
card_number: "0428-100"
card_short_title: "Recover failed apply destroy"
type: bug
areas: [deployment]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "A failed baha app apply may register a DEGRADED deployment without a materialized application runtime; baha app destroy --ye"
kanban_title: "0428-100 · Recover failed apply destroy"
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

- [ ] t-20261116-r28-bug-failed-apply-destroy · Recover failed apply destroy #task #release/v0-4-28 #status/planned #area/deployment #kind/bug

## Goal

A failed `baha app apply` may register a DEGRADED deployment without a materialized application runtime; `baha app destroy --yes` then fails `retained provider ownership could not be verified through its canonical deployment and native renderer`. `baha app list` reports DEGRADED while `baha app status` reports NOT APPLIED.

## Reproduction (2026-11-16 J-Commerce live test)

Run `baha app init` in J-Commerce, select SQL/cache/queue/metrics, confirm candidate, allow preflight to reject privileged `cadvisor` and docker.sock-mounted `floci`, then run `baha app destroy --yes`. A deployment record persists although no app runtime exists.

## Acceptance

- Destroy safely reconciles partial provider registration and removes verified exclusively app-owned records/resources. Shared/foreign/ambiguous resources remain protected and are reported. A second destroy is idempotent; app list no longer contains the failed app. Regression reproduces exact ownership error on baseline and passes on fix. Link historical v0.4.27 `t-20261104-r27-destroy-after-aborted-apply` but do not reopen that accepted card.
- Preserve existing BaseHarbor safety, immutable candidate consent, source ownership and shared-provider isolation. Never bypass preflight or delete foreign resources.
- Include positive/negative regressions and classify baseline-red vs candidate-green.

## Required checks and CI mapping

- Discover all affected existing tests; implement smallest causal regression and register it in existing package tests / PR-gate selection. Prove touched paths select the test and unrelated paths do not trigger unnecessary full native gates.
- Capture exact SHA, test ID, actual CI check/trigger and passing run URL. Where behavior is common to Docker and rootless Podman, produce independent native evidence in existing appropriate integration/release qualification gates. No separate CI framework.
- Reproduction is local user evidence; its observations must be verified in code before declaring a product fix.

## Dependencies and file ownership

- Coordinate shared CLI, wizard, lifecycle and provider files with existing v0.4.28 CLI redesign owners; no competing writes or blanket permissions.
- Historical related accepted card: `t-20261104-r27-destroy-after-aborted-apply` (different abort state; do not duplicate or reopen).

## Handoff

- Planned only. No implementation, PR, merge or acceptance claimed. Source: 2026-11-16 J-Commerce guided-init/apply/destroy/reset transcript supplied by Owner.
