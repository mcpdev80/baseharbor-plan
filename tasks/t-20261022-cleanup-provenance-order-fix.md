---
id: t-20261022-cleanup-provenance-order-fix
type: task
areas: []
release: v0.4.26
version: ""
parent: ""
owner: Codeman (o23 demo cleanup fix)
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-cleanup-provenance-order-fix · Demo: cleanup-provenance ordering fixes owned-container snapshot before teardown #task #release/v0-4-26 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** Codeman (o23 demo cleanup fix)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Owner:** Codeman (o23 demo cleanup fix)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

On the frozen demo input D = `896dc3cb`, harden the cleanup provenance ordering so the
owned-container preview/verification in `failure-runtime-diagnostics.sh` `owned_containers()`
(lines 95-131) runs against a snapshot captured before `acceptance.sh:89`
`baha destroy --all --yes` consumes them, eliminating the Podman
`preparation=1 destroy=0` race documented in `o22-cleanup-prov.md`.

## Scope

- In scope: `baseharbor-demo/scripts/failure-runtime-diagnostics.sh` ordering hardening;
  one regression assertion proving the destroy count is measured pre-teardown.
- Out of scope: core product, runner/executor state, other demo fixtures, releases/tags.

## Acceptance

- The Core non-mutating `--json` preview is captured once, early, and reused for the
  native ownership verification so the Quadlet daemon cannot tear the snapshot between
  preview and verify.
- Auto-collection (owned container `exited`/`dead`) during verification is
  accounted-with-reason, not a `preparation=1` failure; truly foreign/ambiguous
  identities still fail.
- A regression test measures the owned destroy count pre-teardown and asserts the
  teardown consumes exactly that count.
- Current ownership semantics are unchanged (no weakened proof, no new mutable preview).

## Required checks

- `bash -n` on edited shell scripts; `python3 -c "import ast"` on the diagnostics script.
- Targeted mock dry-run of the diagnostics script reproducing the early-collection race,
  asserting `preparation==0` (accounted) and the pre-teardown count assertion.

## Dependencies and file ownership

- Owned files: `baseharbor-demo/scripts/failure-runtime-diagnostics.sh`, demo cleanup fixtures.
- Shared: `acceptance.sh` cleanup ordering (read-only; hardening lives in the diagnostics script).

## Handoff

- Owner dispatch 2026-10-22 (T3-FIX). Branch `fix/v0426-cleanup-provenance-order` @ `d9c78b5`,
  PR #118 to `main` (OPEN). Fix implemented and locally verified (diagnostics compile, fixture
  all-pass, regression fails on un-fixed D). CI dispatch blocked by a GitHub Actions runner-side
  `git fetch` exit-13 outage affecting the whole core targeted/Pre-Release fleet (runs
  39854022100 / 39854057519 / 39854990885 / 39856259550 all abort at checkout, before any gate).
  Re-dispatch `targeted-demo-acceptance.yml` (workflow 364538116, inputs
  ref=2adae47a, demo_ref=d9c78b5, runtime=podman, gate=backup-restore) once infra recovers,
  poll to terminal, record receipt. Full evidence in
  `evidence/board-2026-10-22/o23-demo-cleanup-fix.md`.
