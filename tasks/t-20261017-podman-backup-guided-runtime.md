---
id: t-20261017-podman-backup-guided-runtime
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "ChatGPT (bug-988 implementation session)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#990]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-podman-backup-guided-runtime · Podman backup/restore: resolve isolated guided runtime and prove recovery #task #release/v0-4-26 #status/review #view/review #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** ChatGPT (bug-988 implementation session) · **Priority:** high  
    **PR:** [baseharbor#990](https://github.com/mcpdev80/baseharbor/pull/990)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** ChatGPT (bug-988 implementation session)  
**Priority:** high  
**PRs:** [baseharbor#990](https://github.com/mcpdev80/baseharbor/pull/990)  
**Source:** 
<!-- /generated:links -->

## Goal

Run the existing native Podman disaster-recovery test successfully from isolated state and prove actual backup/restored data and consumer access.

## Scope

Own `TestAppBackupRestoreCLIRealDisasterRecovery` and its existing guided-up/runtime-selection fixture; locate the actual owner before editing. Change production runtime resolution only if reproduction demonstrates a production defect. No new backup/recovery engine, mocked native success or weakened safety checks.

## Acceptance

- Reproduce under the supported native runner configuration and compare runtime/environment/state setup.
- Establish whether the root cause is fixture/integration setup or product runtime selection, and correct that owner.
- Execute the actual disaster-recovery test through backup and restoration; verify restored data and consumer access.
- Missing runtime, skipped tests, mocks or failed recovery are not success evidence.
- Preserve isolation, ownership, consent and cleanup; independently review and have Qwen retest the corrected SHA before release.

## Required checks

Focused Go fixture/runtime-selection tests and existing trusted CI; targeted native `TestAppBackupRestoreCLIRealDisasterRecovery` with explicit Podman selection. No full release matrix.

## Dependencies and file ownership

- No unfinished product-task dependency is established. Before assignment, verify the exact existing CI lane, native fixture and non-overlapping write ownership. A missing trusted lane is an explicit prerequisite, never a self-exemption.
- Implementation belongs to an assigned development session; Qwen performs live testing and retesting only.
- Must be fixed and independently retested before v0.4.26 release (Maintainer instruction, 2026-10-17). Release preparation must depend on this task.

## Handoff

- 2026-10-18: Candidate handed off for independent review: product PR [#990](https://github.com/mcpdev80/baseharbor/pull/990), branch `fix/t-20261017-podman-backup-guided-runtime`, exact product source `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f` against `develop` `d54ac358fb6a6b256164ac2689a33e981c013baa`. Root cause is a test fixture error: isolated state had no configured Podman Target, so the product correctly resolved its implicit Docker default. The fixture now creates a local Target with the explicitly selected native runtime before `runtimeUpGuided`, rejects unsupported runtime names, and verifies effective selection. No production runtime resolver, ownership or consent checks were modified. Real backup, restore, restored SQL data/secret and identity assertions are retained unchanged.
- Focused isolated Go 1.26.9 `TestAppBackupGuidedRuntimeFixture*` Docker/Podman/invalid cases, vet, build, formatting and diff checks PASSED: https://huggingface.co/jobs/ThunderHawk1080/6ad40008c66288145226d095. Trusted exact-SHA PR CI: https://github.com/mcpdev80/baseharbor/actions/runs/39078042399 (results to be evaluated separately). Native `TestAppBackupRestoreCLIRealDisasterRecovery` still requires Qwen's independently reviewed Podman retest; this author's isolated unit tests do NOT establish restored data or consumer access. No SSH/live author test, source qualification, self-acceptance, merge or #978 changes.


- 2026-10-18: Claim published by ChatGPT (bug-988 implementation session) before product changes. Owner scope: the existing backup/restore integration fixture and its guided runtime selection. Production runtime implementation changes require confirmed production defect. No native/SSH retest or #978 changes.

- 2026-10-17: Maintainer-authorized intake from Qwen's supplied pre-freeze audit; this session did not independently reproduce the native failure. The audit reports immediate failure in `runtimeUpGuided`: `runtime up: container runtime orchestration not found` / `ErrRuntimeNotFound`, under isolated state and Podman test selection. Other in-process native Core tests passed. Root cause remains unconfirmed; no successful disaster-recovery evidence exists. Source: `d54ac358fb6a6b256164ac2689a33e981c013baa`.
- Discussion/evidence intake: [baseharbor#988](https://github.com/mcpdev80/baseharbor/issues/988). Unassigned, not implemented or accepted. No private machine identifiers, addresses, local paths or credentials included.
