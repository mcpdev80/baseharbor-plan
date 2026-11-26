---
id: t-20261126-trusted-catalog-baseline-identity-tests
card_number: "0428-352"
card_short_title: "Trusted catalog baseline for"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Register the two identity dashboard test source paths in the trusted source catalog on develop so the base-ref Trusted Plan can…
kanban_title: 0428-352 · Trusted catalog baseline for
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261126-trusted-catalog-baseline-identity-tests · Trusted catalog baseline for identity dashboard tests #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Register the two identity dashboard test source paths in the trusted source catalog on develop so the base-ref Trusted Plan can route them to the existing Docker and Podman data-capabilities gates. This is a catalog baseline prerequisite for card 0428-078; candidate-side catalog edits cannot authorize their own Trusted Plan selection.

## Scope

- In scope: exactly two component entries in `scripts/pr-gate-coverage.json`.
- Out of scope: product/test source changes; changes to `scripts/pr-gate-plan.py`, `scripts/pr-gate-map-v1.json`, `.github/**`, gate definitions, or any trust/gating bypass.

## Acceptance

- Add exactly these component rows, following the existing `{id, path, surfaces}` object format and source-ID convention:
  - `{"id":"source.cmd.baha.app.identity.dashboard.status.test.go","path":"cmd/baha/app_identity_dashboard_status_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}`
  - `{"id":"source.internal.metrics.identity.dashboard.witness.test.go","path":"internal/metrics/identity_dashboard_witness_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}`
- Keep all existing catalog entries and gate-selection behavior unchanged.
- The catalog baseline must land on develop before the clean canonical 0428-078 product reissue is qualified.
- Preserve earlier failed Trusted Plan run records; do not rewrite history or represent failed runs as qualifying evidence.

## Required checks

- Validate the catalog JSON and the Plan-repository-owned product catalog invariants using the existing Hosted Plan/product CI applicable to the baseline PR.
- The eventual product candidate must be a clean canonical 0428-078 reissue on updated develop and must obtain two distinct `pull_request` runs on the same final head, sequentially: trigger the second only after the first run succeeds. A rerun/attempt increment is not a distinct run.
- No product code or tests are changed in this baseline task; no product test result is claimed by this card.

## Test binding

- **Test binding:** existing catalog validation; no new test is introduced by this baseline.
- Existing surfaces, verbatim: gate IDs `atomic/docker/data-capabilities` and `atomic/podman/data-capabilities`, represented by source surfaces `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`.

## Dependencies and file ownership

- Owned files: `scripts/pr-gate-coverage.json` only (product repository baseline PR).
- Related card: 0428-078 (`tasks/t-20261114-r28-perses-dashboard-identity.md`), whose identity dashboard tests consume this trusted catalog baseline.
- The existing 0428-273 baseline card covers the distinct #1819 catalog set and is not expanded by this task.

## Handoff

- Worker: implement exactly the two catalog rows on a baseline branch/PR, with no product/test code or workflow edits. Record the exact merged develop SHA. Then the 0428-078 owner prepares/qualifies a clean canonical candidate against that updated develop and runs the required two-run sequence.
