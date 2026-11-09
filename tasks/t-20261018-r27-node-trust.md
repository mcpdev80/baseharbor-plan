---
id: t-20261018-r27-node-trust
card_number: "0427-042"
card_short_title: "qualify rotation revocation"
areas: [connector]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ChatGPT (externe Übernahme 2026-11-04, Owner-Direktive)
kanban_lane: closed
kanban_summary: "Reconcile existing implementation, then close actual token/mTLS/CA overlap/revocation/reconnect gaps against immutable Core…"
kanban_status: closed
kanban_title: "0427-042 · qualify rotation revocation"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-node-service, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor-node-connector#20]
sources: ["mcpdev80/baseharbor-node-connector#3"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-node-connector/commit/346e5ae77ffa929e771ecf1b1322b78fb65bc165", "https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41924876155", "https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41924886585"]
---

- [x] t-20261018-r27-node-trust · Connector: qualify rotation revocation and session recovery #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/connector #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (externe Übernahme 2026-11-04, Owner-Direktive) · **Priority:** normal  
    **PR:** [baseharbor-node-connector#20](https://github.com/mcpdev80/baseharbor-node-connector/pull/20)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-node-connector/commit/346e5ae77ffa929e771ecf1b1322b78fb65bc165), [proof 2](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41924876155), [proof 3](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41924886585)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md), [t-20261018-r27-remote-material](t-20261018-r27-remote-material.md), [t-20261105-r27-test-wire-helper](t-20261105-r27-test-wire-helper.md)  
**Owner:** ChatGPT (externe Übernahme 2026-11-04, Owner-Direktive)  
**Priority:** normal  
**PRs:** [baseharbor-node-connector#20](https://github.com/mcpdev80/baseharbor-node-connector/pull/20)  
**Source:** [baseharbor-node-connector#3](https://github.com/mcpdev80/baseharbor-node-connector/issues/3)
<!-- /generated:links -->

## Outcome and acceptance

Reconcile existing implementation, then close actual token/mTLS/CA overlap/revocation/reconnect gaps against immutable Core contract. Scope/version/capabilities checked after auth; durable admission and no ambiguous mutation replay. Core unavailable preserves target runtime; wrong peer/tenant/runtime and revoked sessions fail closed.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Connector internal/targetaccess/session*.go enrollment renewal/trust files and internal/connector/outbound*.go; no install.go writes. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused trust/session race tests and bounded real Core/Connector rotation+reconnect gate; not a full app journey. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Externe Übernahme — durch Coordinator nur markiert, nicht bearbeitet
Implementierung, Review, CI, Merge und vollständiger Planning-Abschluss liegen bei ChatGPT. Keine Claims,
keine Lanes, keine Prüfkapazität von dieser Seite; abhängige Karten (node-cli, node-streams, nc-3,
release-0-4-27-updates) bleiben auf dieser Seite gesperrt bis bestätigter Merge + Planning-Abschluss.

## ChatGPT implementation 2026-11-04

- Draft [PR #20](https://github.com/mcpdev80/baseharbor-node-connector/pull/20) on `work/r27-node-trust-chatgpt`, currently bounded reconnect backoff handling with regression tests.
- Task is actively being implemented; neither completed trust qualification nor final merge/acceptance is claimed.

## Trust implementation progress 2026-11-04

- Draft PR [#20](https://github.com/mcpdev80/baseharbor-node-connector/pull/20), candidate `c87f562e1d09f7b0f61f2e4b5d8841f9cb9d5a91`.
- Added saturating outbound reconnect delays in single-session and pooled paths.
- Added fail-closed parsing for malformed revocation serials and zero-padded revoked serial matching.
- Added regression tests for CA overlap/retirement, certificate/key reload and reconnect timing; verification of final candidate in progress.
- Existing source checks and hosted selected tests do not replace the required real current-Core rotation/reconnect qualification. Card remains active, not accepted.

## Transport verification 2026-11-04

- Candidate: `c87f562e1d09f7b0f61f2e4b5d8841f9cb9d5a91`; PR [#20](https://github.com/mcpdev80/baseharbor-node-connector/pull/20).
- Quality [41922887021](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41922887021) SUCCESS; Source Conformance [41922886851](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41922886851) SUCCESS.
- Actual encrypted transport [41922999207](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41922999207) SUCCESS for both Docker and Podman; `TestConnectorRuntimeTransport` passed in each live runtime. Transport fixture uses pinned public Core `9f28af642345a126a75cd3183969973fc93d7f39`, test CA/registry; not production enrollment.
- Native OpenBao / Core enrollment and certificate rotation: [41923296647](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41923296647); pending final runtime verdict as of this handoff. Do not mark complete until acceptance evidence is real.

## Merge and qualification handoff — 2026-11-04

- Connector [PR #20](https://github.com/mcpdev80/baseharbor-node-connector/pull/20) merged to main at [346e5ae77ffa929e771ecf1b1322b78fb65bc165](https://github.com/mcpdev80/baseharbor-node-connector/commit/346e5ae77ffa929e771ecf1b1322b78fb65bc165) from candidate `c87f562e1d09f7b0f61f2e4b5d8841f9cb9d5a91`.
- Quality [41922887021](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41922887021) and Source Conformance [41922886851](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41922886851) passed.
- Encrypted transport [41922999207](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41922999207) passed Docker and Podman; managed OpenBao/Core enrollment, local-key renewal, CA overlap/retirement and persisted revocation [41923296647](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41923296647) passed Docker and Podman, with final logs confirming native `TestNativeOpenBaoManagedCoreAndNodeCSRRotation` PASS on both.
- These native qualification workflows use the frozen Core source `9f28af642345a126a75cd3183969973fc93d7f39`. Current develop-Core compatibility / exact-current-HEAD cross-repository gate is not yet proven; keep the task active rather than misrepresenting full acceptance. No additional CI receipt or approval chain is required.

## Final current-Core qualification — 2026-11-04

- Production Connector main commit `346e5ae77ffa929e771ecf1b1322b78fb65bc165` from merged [PR #20](https://github.com/mcpdev80/baseharbor-node-connector/pull/20).
- Actual Core develop commit `ea3fb38e8f372ab2da38c10d964f3ea452fb8561` checked out and SHA-asserted in independent validation branches, without changing main workflows. The only validation-workflow change was the exact pinned Core SHA from `9f28af642345a126a75cd3183969973fc93d7f39` to this develop head.
- [Current-Core transport run 41924876155](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41924876155): source, actual encrypted transport Docker, actual encrypted transport Podman all SUCCESS.
- [Current-Core native enrollment run 41924886585](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41924886585): source, managed native enrollment/rotation Docker, managed native enrollment/rotation Podman all SUCCESS.
- Both native suites used built Connector code at its merged main content plus the exact Core develop SHA; all required selected runtime gates executed (other mutually exclusive matrix selections are legitimately skipped). No release-wide application journey claimed.
- Acceptance scoped to node-trust task; follow-on node CLI, streams and rollout remain separate tasks. This record is not a CI approval receipt or additional authority chain.
