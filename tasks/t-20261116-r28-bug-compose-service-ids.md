---
id: t-20261116-r28-bug-compose-service-ids
card_number: "0428-288"
card_short_title: "Preserve Compose service IDs"
type: bug
areas: [wizard]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w147-0428-288-pr1833-fix
kanban_status: wait
kanban_lane: wait
kanban_summary: "docker compose config --services yields vectordb, but baha app init persisted vector-db in workload.components and Runtime API…"
kanban_title: 0428-288 · Preserve Compose service IDs
priority: high
depends_on: [t-20261125-0428-284-1812-postretry-gate-failure]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1870", mcpdev80/baseharbor#1833]
sources: []
blocker: ""
wait_reason: "W15 required next proof: hop PR #1833 onto current develop, then obtain two distinct fresh pull_request runs on the exact same head (attempt 1 each); run 45513816046 on a7b0a48048c11d20234160eede941532ddc33156 is attempt 2 and void as pair evidence. Wait for successor card 0428-284 / PR #1856, not closed #1842."
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-compose-service-ids · Preserve Compose service IDs #task #release/v0-4-28 #status/wait #view/wait #area/wizard #kind/bug
    <!-- generated:card -->
    **Owner:** w147-0428-288-pr1833-fix · **Priority:** high  
    **PR:** [baseharbor#1870](https://github.com/mcpdev80/baseharbor/pull/1870), [baseharbor#1833](https://github.com/mcpdev80/baseharbor/pull/1833)  
    **Waiting:** W15 required next proof: hop PR \#1833 onto current develop, then obtain two distinct fresh pull\_request runs on the exact same head (attempt 1 each); run 45513816046 on a7b0a48048c11d20234160eede941532ddc33156 is attempt 2 and void as pair…  
    **Needs:** [t-20261125-0428-284-1812-postretry-gate-failure](t-20261125-0428-284-1812-postretry-gate-failure.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261125-0428-284-1812-postretry-gate-failure](t-20261125-0428-284-1812-postretry-gate-failure.md)  
**Owner:** w147-0428-288-pr1833-fix  
**Priority:** high  
**PRs:** [baseharbor#1870](https://github.com/mcpdev80/baseharbor/pull/1870), [baseharbor#1833](https://github.com/mcpdev80/baseharbor/pull/1833)  
**Source:** 
<!-- /generated:links -->

## Goal

`docker compose config --services` yields `vector_db`, but `baha app init` persisted `vector-db` in `workload.components` and Runtime API consumers. Preflight then fails `workload service "vector-db" is not present in the application Compose file`.

## Reproduction (2026-11-16 J-Commerce live test)

Use J-Commerce docker-compose.yaml including `vector_db`, and run `baha app init`, followed by `baha app apply`. Inspect `baseharbor.yaml` components and runtime permission service names.

## Acceptance

- Use literal Compose service identifiers at all runtime lookup and manifest references, separating presentation/logical IDs from Compose keys. Positive tests for underscores, dashes and mixed service graphs; no silent unsafe aliasing.
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

- QUALIFIED (owner 2026-11-26): exact head a7b0a480 base f7540e59, hosted run 45513816046 TERMINAL SUCCESS (35/35 jobs terminal, 0 fail), mergeable/clean; old 45510613765 superseded-void. Independent Codex review dispatched (w136); merge on APPROVE.


- BASE REFRESH 2026-11-26: run 45510613765 terminal green AT b9d312b but base 9d7e229 behind develop f7540e591 -> not merge-ready; w128 re-dispatched for merge-develop + requal (two IDs on new exact head).


- Planned only. No implementation, PR, merge or acceptance claimed. Source: 2026-11-16 J-Commerce guided-init/apply/destroy/reset transcript supplied by Owner.
- DECISION: YES — PR #1833 may add exactly the three source-classification rows under `scripts/pr-gate-coverage.json` `components`, using only the existing row keys `{id, path, surfaces}`. This is an existing-mechanism data correction: the component array begins at `scripts/pr-gate-coverage.json:138`, source paths resolve through component surfaces in `scripts/validate-pr-gate-coverage.py:21-55`, and the validator checks component `id`/`path`/`surfaces` at `scripts/validate-pr-gate-coverage.py:145-170`. The three rows may classify only `internal/application/manifest_validation.go`, `internal/application/workload.go`, and `internal/application/workload_test.go` to the existing `source.gate.atomic.{docker,podman}.data.capabilities` surfaces. No scripts code, gate-behavior, or `.github` change is authorized by this decision. Expires when PR #1833 is merged or closed; it grants no reusable authorization.

## W15 qualification requirement

Before 0428-288 can qualify, hop PR #1833 onto current develop and obtain two distinct fresh `pull_request` runs on that exact same head, both attempt 1. Run 45513816046 is attempt 2 and is void as pair evidence. The sequencing dependency now points to successor card 0428-284 / PR #1856 rather than closed #1842.
