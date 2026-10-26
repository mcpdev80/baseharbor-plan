---
id: t-20261018-r27-ci-consumption
areas: [docs]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-docs, t-20261018-r27-public-surfaces, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-ci-consumption · Automation: consume releases from GitHub Actions and GitLab CI #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Binding three-worker execution — Owner instruction, 2026-10-26

Routing: **W1/W2/W3 after accepted product inputs**. Use the [coordinator handoff](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md); it supersedes earlier five-worker or serialized implementation scheduling.

W1: paired EN/DE automation documentation and accepted CLI contract. W2: GitHub Actions example and its fixture. W3: GitLab CI example and its fixture/negative exit behavior. Reserve separate example/test files before dispatch; do not deploy or build a CI platform.

Exactly three concurrent worker slots for all v0.4.27 CI work, plus the coordinator; never three additional workers on top of active claims. Existing owners/claims and completed commits are preserved. Coordinator hands over reservations explicitly and balances remaining effort, moving a bounded unfinished subtask or cross-review to a free worker rather than inventing work. No worker edits another worker's scripts, test file or workflow; common-branch pushes, Planning metadata and final integration have one coordinator writer.

Dependencies in frontmatter remain acceptance/readiness requirements, not blanket locks on the explicitly authorized isolated receipt preparation against frozen #1090 interfaces. Parallel preparation does not accept an unmerged dependency, change a shared interface unilaterally, or qualify a new domain. The first one-gate receipt skeleton must be accepted before live domain-gate expansion. Later domain implementation still requires its accepted product contracts, fixtures and release-start inputs; choose another actually ready task or report the concrete blocker if three safe work slices do not exist.

Do not alter active producer behavior or required-check enforcement before the accepted cutover. Preserve the legacy qualification route, use the smallest sufficient checks and batch candidates; no full matrix or duplicate green runs. Cross-review must be by another worker/coordinator and applies to the final integrated SHA.


## Outcome and acceptance

Existing CI builds/tests/publishes and decides approvals. Provide runnable minimal headless Baha consumption of those produced image/release refs, explicit target/environment, bounded short-lived/native machine auth, safe secret channels, stable JSON/exit statuses, async operation ID/result polling and provenance capture. Demonstrate same-artifact stage deployment without rebuild. No Baha CI server/runner/secret database, pipeline generator, provider webhooks or automatic service installation; ordinary workflows need not be replaced. Examples are product docs, not new BaseHarbor release workflows; no secrets or live deployment triggers in example validation.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

EN/DE automation how-to and version-pinned minimal example files for GitHub Actions/GitLab CI; examples validator fixtures only. Reserved paths for this slice only; proposed filenames are fixed in the accepted contract predecessor before assignment. Shared command/HTTP/MCP/help/golden registrations belong to public-surfaces. If another write owner is needed, coordinate and serialize before implementation; no branch-to-branch dependencies or duplicate state.

## Required checks

Parse/lint examples and run their invocation/JSON/exit/timeout behavior against the accepted CLI and controlled API fixture. No actual customer CI deployment or full runtime matrix. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.
