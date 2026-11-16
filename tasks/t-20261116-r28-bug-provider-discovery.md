---
id: t-20261116-r28-bug-provider-discovery
card_number: "0428-103"
card_short_title: "Detect mixed Compose providers"
type: bug
areas: [wizard]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "J-Commerce has product_db (MongoDB), vector_db (pgvector Postgres), floci (local S3-compatible emulator); Wizard proposed si"
kanban_title: "0428-103 · Detect mixed Compose providers"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-provider-discovery · Detect mixed Compose providers #task #release/v0-4-28 #status/planned #area/wizard #kind/bug

## Goal

J-Commerce has `product_db` (MongoDB), `vector_db` (pgvector Postgres), `floci` (local S3-compatible emulator); Wizard proposed six Postgres logical instances including `identity-db-scraper` but omitted `vector_db`, MongoDB and S3. Capture evidence vs optional capability detection; don't blindly assume each emulator can be replaced.

## Reproduction (2026-11-16 J-Commerce live test)

Run `baha app init` in original J-Commerce repository and compare Compose images and application environment (`MONGO_HOST=product_db`, `PG_URL=...vector_db`, `AWS_ENDPOINT=http://floci:4566`) against the discovered provider inventory.

## Acceptance

- Correctly distinguish SQL Postgres/pgvector from MongoDB, scrutinize scraper-like services, and identify verifiable S3 use without implying `floci` equivalence. Preserve valid app binding names and offer explicit user choice where confidence is insufficient; regression fixtures.
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
