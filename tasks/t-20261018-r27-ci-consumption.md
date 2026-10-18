---
id: t-20261018-r27-ci-consumption
areas: [docs]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-ci-lanes, t-20261018-r27-docs, t-20261018-r27-public-surfaces]
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
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

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
