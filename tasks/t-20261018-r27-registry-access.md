---
id: t-20261018-r27-registry-access
areas: [artifacts]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: coord-welle5 (Lane w195, freigegeben)
kanban_lane: review
kanban_summary: Resolve explicitly configured app-scoped OCI registry/artifact endpoints including GitLab/GHCR/Harbor/Quay/Artifactory/Nexus…
kanban_status: review
kanban_title: "Registries: use configured enterprise endpoints and native credentials"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-contract, t-20261018-r27-native-auth, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1395]
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-registry-access · Registries: use configured enterprise endpoints and native credentials #task #release/v0-4-27 #status/review #view/review #area/artifacts #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (Lane w195, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1395](https://github.com/mcpdev80/baseharbor/pull/1395)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-image-transfer](t-20261018-r27-image-transfer.md), [t-20261018-r27-local-registry](t-20261018-r27-local-registry.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md)  
**Owner:** coord-welle5 (Lane w195, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1395](https://github.com/mcpdev80/baseharbor/pull/1395)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Resolve explicitly configured app-scoped OCI registry/artifact endpoints including GitLab/GHCR/Harbor/Quay/Artifactory/Nexus when they expose the supported native protocol. Reuse native Docker credential helpers/Podman auth files and configured CA/proxy/auth scope; fallback only through existing opted-in protected store. Discover actual protocol/capabilities, not brand names. Do not treat every artifact store as an image registry or scrape a proprietary API. Denied/private/unavailable endpoint has no public/plain-HTTP/local fallback. Select a readable tag/ref then record its exact resolved identity; tags are not immutable and lists are bounded to authorized app sources.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

cmd/baha/application_registry_source.go and matching tests; existing credential APIs are inputs, not a second credential store. Paths are reservations confirmed by accepted contract predecessor; shared registrations belong only to public-surfaces, not this slice. No overlapping writes or draft-branch consumers.

## Required checks

Native credential-helper/authfile and TLS registry API fixtures; missing CA/auth, tampered host, denied tags, endpoint mismatch and log redaction; small real registry auth/pull smoke only for uncovered native behavior. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.

## Runde 1 pruefbar 2026-11-05 (kopf c2ada69cd33)
Nachgemessen: ls-remote echt==head, develop VORFAHR, lauf 42120843177 TERMINAL SUCCESS (14 selected checks
gruen), akte round-1.md auf main. Konfig-getriebener endpunkt, native credentials, fail-closed mutante rot,
zusammenbau echt, red-first belegt.
