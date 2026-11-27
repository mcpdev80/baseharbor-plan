---
id: t-20261116-r28-bug-provider-discovery
card_number: "0428-289"
card_short_title: "Detect mixed Compose providers"
type: bug
areas: [wizard]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w399-0428-289-providers
kanban_status: wait
kanban_lane: wait
kanban_summary: "J-Commerce has productdb (MongoDB), vectordb (pgvector Postgres), floci (local S3-compatible emulator); Wizard proposed six…"
kanban_title: 0428-289 · Detect mixed Compose providers
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1880]
sources: []
blocker: ""
wait_reason: "blocked-on develop-catalog owner freeze-lift (same gate as 0428-306 wait / 0428-307 blocked); Trusted Plan runs 46011069186/46011641329 as witnesses; local repro of base-checkout catalog read in akte"
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-provider-discovery · Detect mixed Compose providers #task #release/v0-4-28 #status/wait #view/wait #area/wizard #kind/bug
    <!-- generated:card -->
    **Owner:** w399-0428-289-providers · **Priority:** high  
    **PR:** [baseharbor#1880](https://github.com/mcpdev80/baseharbor/pull/1880)  
    **Waiting:** blocked-on develop-catalog owner freeze-lift (same gate as 0428-306 wait / 0428-307 blocked); Trusted Plan runs 46011069186/46011641329 as witnesses; local repro of base-checkout catalog read in akte  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w399-0428-289-providers  
**Priority:** high  
**PRs:** [baseharbor#1880](https://github.com/mcpdev80/baseharbor/pull/1880)  
**Source:** 
<!-- /generated:links -->

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

## Mandatory regression and existing-green-test audit

- **Investigate the green-test gap before implementing the fix:** identify all existing unit, contract, integration, native Docker, native rootless Podman and release/guided journey tests that *claim or should claim* this behavior; record exact test IDs, assertions, fixtures, mocks, skipped paths, CI selectors, job names and actual run evidence. Do not infer coverage from a green check.
- Prove whether the existing green test path actually executed the failing behavior and rejected it (including Compose detection -> generated manifest -> apply/preflight -> interrupted deployment -> app destroy -> installation destroy where relevant). Classify each gap: missing test, too-weak assertions, fixture mismatch, skipped/conditional path, wrong CI mapping, or actual product regression.
- **Red-first proof is mandatory:** add a deterministic reproduction that fails against the affected current baseline with the exact J-Commerce failure mode, then passes on the candidate. A test that remains green on the broken baseline cannot close the bug.
- Validate the changed test is discovered and executed in the *real* appropriate hosted CI check with a positive path-selection proof; show that unrelated changes do not relaunch costly native suites. Capture exact commit SHA, test ID, check name, selector/trigger, run URL and assertion result. Never count a skipped, mocked-only or non-executed assertion as native PASS.
- Where lifecycle behavior is supported for both engines, provide independent native Docker and rootless Podman verification, using existing acceptance/release qualification runs rather than adding duplicate heavyweight PR gates. Do not change gate/permission/security semantics merely to turn tests green.

## Dependencies and file ownership

- Coordinate shared CLI, wizard, lifecycle and provider files with existing v0.4.28 CLI redesign owners; no competing writes or blanket permissions.

## Handoff

- Planned only. No implementation, PR, merge or acceptance claimed. Source: 2026-11-16 J-Commerce guided-init/apply/destroy/reset transcript supplied by Owner.
