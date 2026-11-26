---
id: t-20261126-runner-openssl-podman-generator
card_number: "0428-358"
card_short_title: "Runtime CI cells guarantee"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: The pull-request runtime cells that exercise Keycloak database reload and Podman Quadlet paths explicitly provide their required…
kanban_title: 0428-358 · Runtime CI cells guarantee
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/02870bdc6884cbc199b36efb951f883caf6eccd1/evidence/2026-11-26/w317-0428-352-huntv33/akte.md"]
---

- [ ] t-20261126-runner-openssl-podman-generator · Runtime CI cells guarantee OpenSSL and Podman Quadlet generator #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/02870bdc6884cbc199b36efb951f883caf6eccd1/evidence/2026-11-26/w317-0428-352-huntv33/akte.md)  
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

The pull-request runtime cells that exercise Keycloak database reload and Podman Quadlet paths explicitly provide their required external binaries. Their execution no longer depends on undocumented runner-image contents or a shim installed only by unrelated cells.

## Scope

- In scope: the owned runtime provisioning path used by the affected PR cells, including `scripts/ci-core-rootless-runtime.sh` and focused provisioning checks where needed.
- In scope: OpenSSL for the Keycloak database reload acceptance path and `podman-system-generator` for Podman Quadlet runtime cells.
- Out of scope: product authentication, consent, or runtime behavior changes; unrelated `certutil`, zsh/fish, and HA-only `etcdctl` findings; changes to unrelated observability or MCP cell shims.
- Owner boundary: do not edit `.github/**`. If the correct fix requires a workflow change, stop and record the exact workflow path and line as an owner-scope dependency.

## Acceptance

- The affected cells and tests are enumerated from the current workflow and census before editing. The source references are `internal/identityprovider/keycloak_database_reload.go:123-138` and `internal/providers/runtime/podman/quadlet_runtime.go:18`; the finding evidence is PR #116's akte lines 123-132.
- Every PR runtime cell that executes the Keycloak database reload path obtains and verifies `openssl` through its owned provisioning path; the result does not rely solely on a GitHub-hosted runner image default.
- Every Podman runtime cell that executes the Quadlet path obtains and verifies `podman-system-generator` through its owned provisioning path; a shim used only by another workflow is not accepted as evidence.
- Missing required tools fail provisioning with a clear diagnostic before the acceptance test; they are not silently skipped or treated as a successful test.
- Product behavior and the OpenSSL/Quadlet code paths remain unchanged. Any required workflow change is reported as owner-scope work and blocks acceptance until separately authorized and present.
- Existing tests that exercise both paths pass in the relevant hosted Docker and Podman runtime gates. Handoff records each exact test ID, source SHA, gate, trigger, executed job, and run URL; skipped gates do not count.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding:** existing Keycloak database-reload and Podman Quadlet acceptance tests, discovered in their packages and executed by the existing hosted Docker and Podman runtime gates. No new CI job or gate is authorized by this card. The implementing lane must identify the exact test IDs before editing and prove the relevant jobs executed on the final candidate.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: the runtime provisioning helper(s) and focused checks required to provide the two named binaries.
- Shared files: `.github/**` remains owner scope; no workflow edits without explicit authorization. Coordinate shared provisioning scripts with their existing owner.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Source findings

- Hunt H-V33 evidence: [PR #116 akte](https://github.com/mcpdev80/baseharbor-plan/blob/02870bdc6884cbc199b36efb951f883caf6eccd1/evidence/2026-11-26/w317-0428-352-huntv33/akte.md), OpenSSL Finding #2 lines 123-127 and Podman generator Finding #3 lines 129-132.
- No tracking was decided for the mitigated zsh/fish Finding #1 and HA-gated `etcdctl` Finding #4; see the Codex disposition comment on PR #116.
