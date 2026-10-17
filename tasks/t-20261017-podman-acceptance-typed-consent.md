---
id: t-20261017-podman-acceptance-typed-consent
type: bug
areas: [ci]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (Podman acceptance consent)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#989]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-podman-acceptance-typed-consent · Podman acceptance: honor fresh typed provider consent #task #release/v0-4-26 #status/active #view/active #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 (Podman acceptance consent) · **Priority:** high  
    **PR:** [baseharbor#989](https://github.com/mcpdev80/baseharbor/pull/989)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (Podman acceptance consent)  
**Priority:** high  
**PRs:** [baseharbor#989](https://github.com/mcpdev80/baseharbor/pull/989)  
**Source:** 
<!-- /generated:links -->

## Goal

Make the existing clean-state native Podman acceptance journey exercise the supported typed provider-consent protocol without weakening fail-closed product behavior.

## Scope

Own the lifecycle step in `.github/workflows/podman-acceptance.yml` and immediately required existing acceptance helpers/regressions. Reuse the existing plan and consent authority. No new workflow, consent bypass, generic runner framework or unrelated product changes.

## Acceptance

- Obtain a fresh operation plan and supply its required confirmation stages; stale/foreign plan IDs and missing consent must block.
- Preserve separate destructive-data authorization when required.
- On clean acceptance state, execute application-scoped SQL/cache apply and prove authenticated SQL and Valkey verification.
- Do not depend on warm state or weaken incomplete-inventory handling.
- Independently review the change, then Qwen retests the exact corrected SHA on the authorized native environment before release.

## Required checks

Focused workflow policy/actionlint and helper regressions as selected by the trusted CI; one targeted native Podman acceptance run including consent-negative cases. No full release matrix.

## Dependencies and file ownership

- No unfinished product-task dependency is established. Before assignment, verify the exact existing CI lane, native fixture and non-overlapping write ownership. A missing trusted lane is an explicit prerequisite, never a self-exemption.
- Implementation belongs to an assigned development session; Qwen performs live testing and retesting only.
- Must be fixed and independently retested before v0.4.26 release (Maintainer instruction, 2026-10-17). Release preparation must depend on this task.

## Handoff

- 2026-10-18 implementation correction ready for independent review: [Draft #989](https://github.com/mcpdev80/baseharbor/pull/989) source `78a72ebad0723eefe760090bc34130b55858d8a3` resolves [review 5558362913](https://github.com/mcpdev80/baseharbor/pull/989#pullrequestreview-5558362913). The helper now resolves through `$GITHUB_WORKSPACE` after the lifecycle step changes into the application working directory. Apply, down, up and destroy each derive separate typed consent from a fresh operation-bound plan; down consumes its emitted `baseharbor.provider-impact-scope/v1` scope, up derives a new provider plan after stop, and destroy derives the data-preserving retirement impact. Consent is unset between operations and the helper always emits `delete_data:false`; destructive impact remains fail-closed. Eight executable regressions cover invalid/destructive inputs, operation-specific plan shapes, changed working directory and the actual lifecycle shell fragment with distinct apply/down/up/destroy plan IDs. Exact-SHA [HF job 6ad3ff6d5ccb47ba0f7bec93](https://huggingface.co/jobs/ThunderHawk1080/6ad3ff6d5ccb47ba0f7bec93) PASS: eight tests, workflow policy (19 approved workflows) and diff check. [PR CI run 39077712838](https://github.com/mcpdev80/baseharbor/actions/runs/39077712838): Trusted Plan, Workflow policy, Focused Python, ci-executor-verifier-tests, pr-planner-tests, ci-actionlint and ci-policy PASS; final `PR Selected Checks` remains intentionally BLOCKED because the changed Podman workflow/helper/test coverage is unresolved and requires independent/native qualification. This session did not self-qualify that coverage. No native/live/SSH test was run; Qwen alone owns the exact-SHA native Podman retest after independent content review. No merge or self-approval.

- 2026-10-17 **independent review: changes required**, candidate `d2eda9e681c8d82b01a72601c80b5a06e18d438d`, [review 5558362913](https://github.com/mcpdev80/baseharbor/pull/989#pullrequestreview-5558362913). Four helper tests independently PASS, but an executable shell-fragment test reproduces exit 2 before apply: after `cd "$workdir"`, the relative `scripts/ci-podman-typed-consent.py` path points outside the checkout. Resolve the helper by absolute checkout root and add a real working-directory regression. Remaining down/up/destroy invocations also still lack their own fresh typed acknowledgements, as required by the audited clean-state lifecycle; down uses scope consent, up/destroy their current impact plans, never a reused apply ID or implicit deletion authorization. Cover the existing full journey's command wiring without live execution. Qwen alone performs native retest after corrected content review. No source qualification or merge. No runtime/live systems used by this reviewer.

- 2026-10-17 verification: [PR #989 CI run 39042378088](https://github.com/mcpdev80/baseharbor/actions/runs/39042378088), exact product `d2eda9e681c8d82b01a72601c80b5a06e18d438d`: Workflow policy, Trusted Plan, focused Python, `pr-planner-tests`, `ci-policy`, `ci-executor-verifier-tests`, `ci-actionlint` all **SUCCESS**; required `PR Selected Checks` **FAILURE** on unreviewed `.github/workflows/podman-acceptance.yml`, `scripts/ci-podman-typed-consent.py`, `scripts/test_ci_podman_typed_consent.py` coverage, pending independent qualification. [HF isolated helper/actionlint job](https://huggingface.co/jobs/ThunderHawk1080/6ad38ac5c662881452268b75) four tests PASS, 19-workflow policy PASS. [HF isolated Go consent test](https://huggingface.co/jobs/ThunderHawk1080/6ad38bce5ccb47ba0f7bb6b7) `TestAlternativeLessDeletionRequiresTwoPlanBoundStages` PASS (stale plan, missing acknowledgement, separate destructive deletion guard). [HF planning validation](https://huggingface.co/jobs/ThunderHawk1080/6ad38ba65ccb47ba0f7bb6ab): published Planning SHA `b5a6f36350fbdf819e3d70d02bd3c6cfed1ec3e8`, `plan.py check` 243 tasks, 0 errors, 0 warnings; 47 planning tests PASS and render reproducibly clean (`RENDER_STABLE`). No native live run; Qwen alone owns native retest after independent review. No merge/self-qualification.


- 2026-10-17 implementation handoff: [Draft #989](https://github.com/mcpdev80/baseharbor/pull/989) source `d2eda9e681c8d82b01a72601c80b5a06e18d438d`. Podman workflow takes fresh `baha app plan -o json` immediately before apply, emits bounded typed consent for its exact provider impact plan via `scripts/ci-podman-typed-consent.py`, refuses absent/stale-input shape or destructive intent rather than inferring deletion consent; product runtime still validates current plan and inventory. Regression file `scripts/test_ci_podman_typed_consent.py` covers two/one-stage, incomplete, missing, malformed, destructive plan, and workflow binding. [HF check job](https://huggingface.co/jobs/ThunderHawk1080/6ad38ac5c662881452268b75): four helper tests PASS, 19-workflow policy PASS, targeted actionlint invoked (check completion separately). No native or live testing by this session: Qwen retests after independent review. No merge, no self-approval.


- 2026-10-17: Claim acquired for isolated workflow/acceptance-helper correction. No native/live environment execution in this session; Qwen owns native retest after independent review. Scope limited to existing Podman acceptance workflow and direct regressions; no consent bypass or inventory weakening.

- 2026-10-17: Maintainer-authorized intake from Qwen's supplied pre-freeze audit; this session did not independently reproduce the native failure. Fresh-state acceptance currently invokes apply without typed consent and receives `impact-confirmation-required` (`complete:false`, `confirmations_required:2`). The audit reports that fresh consent makes apply and verification succeed. This is a test/integration mismatch. Source: `d54ac358fb6a6b256164ac2689a33e981c013baa`.
- Discussion/evidence intake: [baseharbor#987](https://github.com/mcpdev80/baseharbor/issues/987). Unassigned, not implemented or accepted. No private machine identifiers, addresses, local paths or credentials included.
