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

- [ ] t-20261018-r27-ci-consumption · Deferred CI consumption examples for accepted product APIs #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
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

# Deferred CI consumption examples for accepted product APIs

## Product outcome, not CI infrastructure
Document minimal headless consumption of already produced image/release refs with explicit target/environment, supported short-lived/native auth, stable JSON/exit behavior and operation polling. Same artifact across stages; no rebuild, Baha CI server, runner/secret database, pipeline generator or automatic service installation. No actual customer deployment in example tests.

## Inputs and three-slot ownership
Wait for the accepted docs/public-surface/delivery interfaces in frontmatter and accepted trusted test support. From the shared worker pool: W1 paired EN/DE automation how-to, W2 GitHub Actions example/fixture, W3 GitLab CI example/fixture. Coordinator fixes separate concrete filenames and callable interfaces before future assignment; this is not an invitation to guess unimplemented API paths or occupy additional workers.

## Acceptance
Parse/lint examples and exercise invocation/JSON/exit/timeout behavior on controlled accepted API fixtures. Keep secrets out of examples, no live triggers/customer deployment or full runtime matrix. Retain the native delivery/stage standards boundary and actual supported providers. This feature card does not modify current receipt helpers or release workflows.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman is resumed by the Owner; the coordinator preserves claims and unpublished work and assigns small non-overlapping iterations under the current order. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261018-r27-ci-consumption.md) remain immutable history, not competing operational instructions.
