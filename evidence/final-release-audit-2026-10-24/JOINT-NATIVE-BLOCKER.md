# Joint native qualification blocker

Core R `3e27497b4ef7b567858ba646bc3071bee37d19bd` and Demo D `03396c805369e61d2e0745d00f78c8add809e2e0` retain their independent native acceptance. The previously frozen Console U `645dda54c0382b897e1cb709413f88b5827c38ce` and Connector K `543e155dacf6adcd98655333b0d2612fef6814ad` have **not** passed the joint native gate.

Connector run `40130842592`, attempt 1, executed the real Docker and Podman jobs against actual K. Both failed the browser application journey. No integration-manifest producer receipt exists for acceptance. Selected 63 and complete 65 remain held.

## Independently authenticated failure

Docker job `120982056297` logs fetched through GitHub show first local application `apply` accepted and terminal failed at stage `apply`, code `approval_required`, cause `impact-confirmation-required`. The test at Console `scripts/browser/application-journey.mjs:183` expected `capability_missing` / `core_required`. Core setup observation remained empty. Earlier native Connector enrollment and engine tests passed, but those explicitly disclaim the complete operator HTTP/Console journey.

## Exact source diagnosis

Core R file blobs authenticated through GitHub and compared with the locally inspected source:

- `cmd/baha/app_core_requirement.go`: `570d4e11b5fce7d7f675d21e894da9a3a4074174`.
- `cmd/baha/application_provider_authorization.go`: `18c4d68193038627dd0e7fc36068366b59c4d071`.
- `cmd/baha/provider_change_confirmation.go`: `54650b3f2c6215e8a18a2465cf3d35e79396c3c9`.

`requireResolvedApplicationCore` now resolves actual application footprint and selected provider plan; it does not call the historical mandatory `requireApplicationCore` path. `runApplicationApplyLifecycle` then authorizes provider changes before materialization. `acknowledgeProviderImpact` explicitly refuses to infer either impact acknowledgement from ordinary apply approval or --yes. Missing required stages classify as `approval_required` / `impact-confirmation-required`, with the concrete impact plan in error details; stale consent classifies as conflict.

Current Console ApplicationActions submits an empty input for apply; only destroy submits generic approval. Thus replacing the old expected error or injecting approval=true would not qualify a real usable consent path. A correction must present the actual Core-owned plan and collect its required acknowledgement stages, preserve current plan identity and exact application/environment/target, and retain no-effect and stale-consent boundaries. Browser interception must not fabricate consent or an execution result.

Existing Core regression `TestApplicationImpactAuthorizationRequiresConcreteConsentWithoutWrites` asserts ordinary --yes rejection, concrete two-stage error details, acceptance of explicit matching plan_id/first/second, rejection of stale plan_id, and no provider/deployment-state writes from authorization.

No source was modified by this audit lane. Any corrected U/K must be reviewed, merged to actual commits, resolved into a fresh canonical DAG, and genuinely requalified before selected 63 / complete 65. Earlier final-freeze files describe the attempted baseline, not a successful release-ready graph.
