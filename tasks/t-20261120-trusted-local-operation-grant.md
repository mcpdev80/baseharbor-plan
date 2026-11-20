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
kanban_status: planned
kanban_lane: ready
kanban_summary: "Bind existing local runtime authorization to exactly one CLI operation, target, and canonical environment through a short-lived,…"
kanban_title: 0428-188 · Bind local operation grants to
priority: high
depends_on: [t-20261114-r28-cli2-uid-environment]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-trusted-local-operation-grant · CLI security: Bind local operation grants to calls #task #release/v0-4-28 #status/planned #view/ready #area/architecture #area/cli #area/security #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Marcel assigned) · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-uid-environment](t-20261114-r28-cli2-uid-environment.md)  
**Required by:** [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
**Owner:** Codex (Marcel assigned)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Bind existing local runtime authorization to exactly one CLI operation, target, and canonical environment through a short-lived, single-use typed grant. Preserve valid local CLI behavior while failing closed on absent, altered, mismatched, expired, or replayed grants.

## Scope

- In scope: implement a typed grant with typed operation (no string matching), Target (Environment UID + App UID), canonical Environment UID, 16-byte nonce, expiry no more than 60 seconds, and HMAC over a canonical encoding of all fields. Issue only at the existing local runtime authorization check; use the existing Unix socket and verify the caller with `SO_PEERCRED`. Keep the HMAC key only in the authority process or in a 0600 file inaccessible to the CLI. The CLI may request and forward the grant unchanged, but may not mint or alter one.
- In scope: verify at the policy boundary that the MAC is valid, all operation/target/environment fields exactly match the concrete call, expiry is valid, and the nonce has not been used; consume the nonce once so concurrent replay is denied. Any missing field, mismatch, invalid MAC, expiry, or replay denies before operation execution. Keep verification on the existing architecture; if the policy boundary is in another process, use the existing socket to ask the authority to verify rather than exposing its key.
- In scope: table-driven tests for valid grant, wrong operation, wrong target, wrong environment, missing grant, modified MAC, expired grant, and replay (same nonce twice). Register the cases in the existing test inventory and map them to the existing CI gate(s); document exact SHA -> test ID -> mapped gate -> run URL/outcome.
- In scope: update #1594 first, then bring #1615 forward to the resulting head. Ensure the workflow `pull_request.branches` rule runs CI for #1615's actual base; if needed, move the stack onto a `lane-` base without losing its dependency chain.
- Out of scope: new infrastructure, public-key cryptography, registry changes, deriving authorization from names or environment variables, a freely settable trusted-local Boolean, unrelated CLI redesign, and changes to release scope.

## Acceptance

- Grant fields and typed operation exactly match the scope; canonical MAC encoding is unambiguous and covers every field.
- Only the existing local runtime authorization can issue grants; the Unix-socket peer is checked with `SO_PEERCRED`, and the CLI cannot mint, modify, or validate grants using the secret key.
- Policy verification matches the exact operation, Target (Environment UID + App UID), and canonical Environment UID; invalid/missing/expired/replayed grants deny before execution.
- Nonces are consumed atomically; restart behavior cannot make a prior grant replayable (for example, use a process-lifetime key and replay set so restart invalidates all outstanding grants).
- All eight required cases pass, including two submissions of the same valid nonce where only the first can authorize.
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

- Owned files or areas: local runtime authorization grant type/issuance, Unix-socket request/response and peer verification, policy verification/nonce consumption, focused tests, and test-inventory/gate-map entries for these tests.
- Shared files: coordinate shared authorization/policy interfaces and CI inventory/gate mapping with their owners before editing. No public-key, registry, or new-infrastructure work.

## Handoff

- Planned and assigned. No product implementation has started. Product PR must target `develop`; after this task's grant is merged, update and validate #1594 first, then #1615. Record exact SHA -> test ID -> mapped gate -> run URL/outcome for each required test.
