---
id: t-20261017-release-0-4-27-prepare
type: acceptance
areas: [release]
release: v0.4.27
version: v0.4.27
release_stage: prepare
parent: v0.4.27
owner: ""
priority: normal
depends_on: [nc-3, t-20261017-release-0-4-27-updates, t-20261018-r27-access-profiles, t-20261018-r27-access-proof, t-20261018-r27-access-wizard, t-20261018-r27-app-binding, t-20261018-r27-artifact-resolution, t-20261018-r27-authority-contract, t-20261018-r27-candidate-contract, t-20261018-r27-candidate-ingress, t-20261018-r27-candidate-pack, t-20261018-r27-ci-lanes, t-20261018-r27-client-commands, t-20261018-r27-connection-client, t-20261018-r27-device-enrollment, t-20261018-r27-device-lifecycle, t-20261018-r27-docs, t-20261018-r27-execution-journal, t-20261018-r27-journal-wiring, t-20261018-r27-local-parity-proof, t-20261018-r27-maintenance-client, t-20261018-r27-managed-users, t-20261018-r27-management-host, t-20261018-r27-mutation-lock, t-20261018-r27-native-auth, t-20261018-r27-node-cli, t-20261018-r27-node-service, t-20261018-r27-node-streams, t-20261018-r27-node-trust, t-20261018-r27-onboarding-wizard, t-20261018-r27-profile-codec, t-20261018-r27-profile-contract, t-20261018-r27-protected-credentials, t-20261018-r27-public-surfaces, t-20261018-r27-remote-docker-web, t-20261018-r27-remote-material, t-20261018-r27-remote-podman-web, t-20261018-r27-remote-rollout, t-20261018-r27-secure-export, t-20261018-r27-state-owner, t-20261018-r27-state-recovery, t-20261018-r27-team-auth, t-20261018-r27-team-proof, t-20261018-r27-video-proof]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-4-27-prepare · v0.4.27 · Pre-release: complete ecosystem readiness and candidate preparation #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-profiles](t-20261018-r27-access-profiles.md), [t-20261018-r27-access-proof](t-20261018-r27-access-proof.md), [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-execution-journal](t-20261018-r27-execution-journal.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-maintenance-client](t-20261018-r27-maintenance-client.md), [t-20261018-r27-managed-users](t-20261018-r27-managed-users.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-profile-contract](t-20261018-r27-profile-contract.md), [t-20261018-r27-protected-credentials](t-20261018-r27-protected-credentials.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-remote-docker-web](t-20261018-r27-remote-docker-web.md), [t-20261018-r27-remote-material](t-20261018-r27-remote-material.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-profiles](t-20261018-r27-access-profiles.md), [t-20261018-r27-access-proof](t-20261018-r27-access-proof.md), [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-execution-journal](t-20261018-r27-execution-journal.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-maintenance-client](t-20261018-r27-maintenance-client.md), [t-20261018-r27-managed-users](t-20261018-r27-managed-users.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-profile-contract](t-20261018-r27-profile-contract.md), [t-20261018-r27-protected-credentials](t-20261018-r27-protected-credentials.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-remote-docker-web](t-20261018-r27-remote-docker-web.md), [t-20261018-r27-remote-material](t-20261018-r27-remote-material.md), [t-20261018-r27-remote-podman-web](t-20261018-r27-remote-podman-web.md), [t-20261018-r27-remote-rollout](t-20261018-r27-remote-rollout.md), [t-20261018-r27-secure-export](t-20261018-r27-secure-export.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Required by:** [t-20261017-release-0-4-27-qualify](t-20261017-release-0-4-27-qualify.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Finish every prerequisite for complete-ecosystem pre-release readiness.

## Scope and acceptance

- Apply canonical audit sections 1–8 and section 9 atomic-first prerequisites, plus RELEASE_WORKFLOW.md#prepare. Re-read current sources and workflows instead of copying obsolete v0.4.25 exceptions.
- Accept all assigned implementation/CI/docs/consumer tasks and verify release-note/epic criteria, even when no executable children have been cut. Accepted cards alone do not prove release readiness; inspect deferred or waived test debts explicitly.
- Complete implementation/security/ownership/standards and CLI/JSON/MCP parity; current Core/BaseHarbor, Demo, Console and Node Connector compatibility; real supported developer journeys, auth/mTLS and cleanup evidence.
- Complete concise EN/DE docs/reference/specs, navigation/links, changelog and actual human release message, compatibility/security/upgrade/deferred notes, strict Pages candidate builds/workflow without deployment. Keep process rules out of the product README.
- Freeze actual immutable ecosystem SHAs, candidate tree, gate requirements and verifier-compatible evidence origins. Verify all required targeted checks, runtime/platform gates and consumer receipts; missing/failed/skipped/unverified requirements block readiness.
- Deliver a reviewable readiness dossier and exact authorized-run plan. Preparation does not authorize full pre-release, promotion, tag, publication or public Pages deployment.

## Required checks

Existing canonical documentation audit, strict EN/DE MkDocs, source/contracts/build/security and affected native/consumer gates. Reuse only verifier-proven compatible evidence; do not rerun unaffected green gates.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#prepare). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
