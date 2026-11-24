---
id: t-20261120-trusted-local-operation-grant
card_number: "0428-188"
card_short_title: "Bind local operation grants to"
type: task
areas: [cli, architecture, security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex (Marcel assigned)
kanban_status: closed
kanban_lane: closed
kanban_summary: "Bind existing local runtime authorization to exactly one typed CLI operation, application/environment identity, and policy check…"
kanban_title: 0428-188 · Bind local operation grants to
priority: high
depends_on: [t-20261114-r28-cli2-uid-environment]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1717]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1717", "https://github.com/mcpdev80/baseharbor/actions/runs/44758114769", "https://github.com/mcpdev80/baseharbor/commit/3653369a4d832e16a427ebf862e959dcccb882b1"]
---

- [x] t-20261120-trusted-local-operation-grant · CLI security: Bind local operation grants to calls #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/architecture #area/cli #area/security #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Marcel assigned) · **Priority:** high  
    **PR:** [baseharbor#1717](https://github.com/mcpdev80/baseharbor/pull/1717)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1717), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44758114769), [proof 3](https://github.com/mcpdev80/baseharbor/commit/3653369a4d832e16a427ebf862e959dcccb882b1)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-uid-environment](t-20261114-r28-cli2-uid-environment.md)  
**Required by:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md), [t-20261124-r28-trusted-local-failopen-seam-dead](t-20261124-r28-trusted-local-failopen-seam-dead.md)  
**Owner:** Codex (Marcel assigned)  
**Priority:** high  
**PRs:** [baseharbor#1717](https://github.com/mcpdev80/baseharbor/pull/1717)  
**Source:** 
<!-- /generated:links -->

## Goal

Bind existing local runtime authorization to exactly one typed CLI operation, application/environment identity, and policy check through an opaque in-process grant. Preserve valid local CLI behavior while failing closed on missing, mismatched, or reused grants.

## Scope

- In scope: implement an unexported grant type whose fields cannot be directly constructed or modified by callers. Its only constructor is the existing local-runtime Check function. Bind a typed `machine.Operation`, Target identity (Environment UID + App UID), canonical Environment UID, and a monotonically increasing in-process nonce to one policy check. Do not add HMAC, TTL, socket IPC, or `SO_PEERCRED`.
- In scope: policy accepts only the opaque grant type and verifies exact operation/target/environment identity plus one-time use. Missing grant, mismatched fields, or reused nonce denies before operation execution. The grant exists only during one request's check; the nonce protects against accidental same-process reuse, not a hostile local user.
- In scope: table-driven tests for valid grant, wrong operation, wrong Target identity, wrong Environment UID, missing grant, and replay (same grant twice). Register the cases in the existing test inventory and map them to the existing CI gate(s); document exact SHA -> test ID -> mapped gate -> run URL/outcome.
- In scope: update #1594 first, then bring #1615 forward to the resulting head. Ensure the workflow `pull_request.branches` rule runs CI for #1615's actual base; if needed, move the stack onto a `lane-` base without losing its dependency chain.
- Out of scope: new infrastructure, public-key cryptography, registry changes, deriving authorization from names or environment variables, a freely settable trusted-local Boolean, unrelated CLI redesign, and changes to release scope.

## Acceptance

- Grant concrete type and fields are unexported, immutable after construction, and constructible only by the existing Check function. Operation is compared as a typed `machine.Operation`, not by parsing or matching strings.
- Policy accepts only the opaque grant type and requires exact operation, Target (Environment UID + App UID), and canonical Environment UID matches; missing, mismatched, or reused grants deny before execution.
- A monotonic in-process nonce is consumed once; repeated use of the same grant in the same process is denied.
- Tests document the trust boundary: the grant prevents accidental internal forgery/reuse, while the local OS user can intentionally construct/modify process state; the grant is not a security boundary against that user.
- All six required cases pass, including two submissions of the same grant where only the first can authorize.
- Tests are registered in the existing test inventory and mapped to the existing gate. For each case, handoff documents exact candidate SHA -> test ID -> mapped gate -> triggering event -> run URL and outcome; all required exact CI runs are green.
- PR targets `develop`; after its acceptance, #1594 is updated and verified first, then #1615 is updated and verified. The exact #1615 base is covered by `pull_request.branches` and its exact-head CI passes.
- Existing authorized local operations continue to work through the grant flow; no existing authorization or runtime protections are weakened.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: local runtime authorization grant type/issuance, policy verification/nonce consumption, focused tests, and test-inventory/gate-map entries for these tests.
- Shared files: coordinate shared authorization/policy interfaces and CI inventory/gate mapping with their owners before editing. No HMAC, socket IPC, public-key, registry, or new-infrastructure work.

## Handoff

- Owner directed an in-process opaque grant: no HMAC, TTL, Unix-socket IPC or `SO_PEERCRED`. It protects against accidental internal misuse, not a hostile local OS user. PR #1717 exact head was `4b51ce350e171e28b432b75408be4206c0896722` (base `develop`), merged at `3653369a4d832e16a427ebf862e959dcccb882b1`. Exact run https://github.com/mcpdev80/baseharbor/actions/runs/44758114769 attempt 2 succeeded on that SHA; attempt 1 failed only because the hosted Go proxy reset an HTTP/2 download, and the failed planner job alone was rerun. Test-to-gate evidence: `TestLocalRuntimeGrantIsOperationTargetEnvironmentBoundAndSingleUse` — valid case, `/operation`, `/target`, `/environment`, `/missing`, replay — and `TestCheckLocalRuntimeGrantFailsClosedAndUsesMonotonicNonce` — invalid UID, runtime-check failure, missing check, monotonic nonce — all run in `authority-package-tests`; `test_operatorauth_source_and_tests_select_real_package_runner` proves both source and test select that gate. The exact CI trigger was PR synchronize; all required exact-head jobs passed, including authority package tests, four CLI shards, CLI package runner, Docker and Podman Keycloak, planner, build, vet, source format and workflow policy. Local package/CLI regression tests, vet, build, selector test, authority package runner and diff check passed. #1615 actual base `cli2-env-policy-head` is admitted by its current `pull_request.branches: cli2-*` rule. 0428-188 accepted; #1594 is now the active next step, then update #1615 to the resulting head and run its exact CI.
