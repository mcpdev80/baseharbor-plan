---
id: t-20261017-release-0-4-26-prepare
type: acceptance
areas: [release]
release: v0.4.26
version: v0.4.26
release_stage: prepare
parent: v0.4.26
owner: ""
priority: normal
depends_on: [core-752, core-893, core-893-interface, core-894, core-895, core-896, core-900, core-901, core-910, core-911, core-912, core-913, core-914, core-915, core-916, core-917, core-918, core-919, core-920, core-921, core-922, core-923, t-20261016-pr-impact-selection, t-20261016-registration-ci-readiness, t-20261016-wizard-task-ci-readiness, t-20261017-concise-code-comments, t-20261017-podman-acceptance-typed-consent, t-20261017-podman-backup-guided-runtime, t-20261017-provider-projection-workload, t-20261018-scoped-runtime-reset-xdg-ownership, t-20261018-podman-recovery-core-state-owner, t-20261018-podman-recovery-bootstrap-cleanup]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-4-26-prepare · v0.4.26 · Pre-release: complete ecosystem readiness and candidate preparation #task #release/v0-4-26 #status/planned #view/waiting #board/planned #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-922](core-922-docs-new-edit-provider-selection.md), [core-923](core-923-acceptance-new-edit-journeys-consumers.md), [t-20261017-podman-acceptance-typed-consent](t-20261017-podman-acceptance-typed-consent.md), [t-20261017-podman-backup-guided-runtime](t-20261017-podman-backup-guided-runtime.md), [t-20261018-scoped-runtime-reset-xdg-ownership](t-20261018-scoped-runtime-reset-xdg-ownership.md), [t-20261018-podman-recovery-core-state-owner](t-20261018-podman-recovery-core-state-owner.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md) (v0.4.26)  
**Depends on:** [core-752](core-752-inspect-reconcile-default-instances.md), [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-893-interface](core-893-interface-agree-planning-execution-interface.md), [core-894](core-894-actions-concise-names-clear-results.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md), [core-901](core-901-pilot-verify-parallel-task-prs-ci-costs.md), [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-911](core-911-app-edit-load-existing-selections.md), [core-912](core-912-wizard-needs-first-selection.md), [core-913](core-913-wizard-compatible-providers-same-view.md), [core-914](core-914-preview-actual-footprint.md), [core-915](core-915-preview-provider-consequences-partial-results.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md), [core-917](core-917-app-new-connect-wizard-lifecycle.md), [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-919](core-919-footprint-cli-json-one-projection.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md), [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-922](core-922-docs-new-edit-provider-selection.md), [core-923](core-923-acceptance-new-edit-journeys-consumers.md), [t-20261016-pr-impact-selection](t-20261016-pr-impact-selection.md), [t-20261016-registration-ci-readiness](t-20261016-registration-ci-readiness.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md), [t-20261017-concise-code-comments](t-20261017-concise-code-comments.md), [t-20261017-podman-acceptance-typed-consent](t-20261017-podman-acceptance-typed-consent.md), [t-20261017-podman-backup-guided-runtime](t-20261017-podman-backup-guided-runtime.md), [t-20261017-provider-projection-workload](t-20261017-provider-projection-workload.md), [t-20261018-scoped-runtime-reset-xdg-ownership](t-20261018-scoped-runtime-reset-xdg-ownership.md), [t-20261018-podman-recovery-core-state-owner](t-20261018-podman-recovery-core-state-owner.md)  
**Required by:** [t-20261017-release-0-4-26-qualify](t-20261017-release-0-4-26-qualify.md)  
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

### 2026-10-18 — #993 sandbox correction source review
- Exact correction candidate `b981f3b60bebfaebf6eb7f2f467dfd06142c90fe` addresses review 5562183275: controlled rm fixture contains actual removals to its sandbox and blocks/logs global temporary-path removals; external sentinel asserted retained. No additional source blocker found in this correction.
- Actual CI 39113140692 selected checks successful; finalcheck remains blocked. Dedicated five-test suite execution remains separate evidence, not inferred from generic CI jobs. Formal source/CI qualification and acceptance remain open; unscoped production reset still only authorized for dedicated runner context.
- No additional local/native reviewer execution or merge.


### 2026-10-18 — Native retest and cleanup review follow-up
- #989 exact-candidate native lifecycle/negative-consent/data-retention evidence supplied positive; formal CI/source qualification remains open.
- #990 only reaches Core startup; full Podman disaster recovery blocked at Compose-only Core lookup. [Bug #994](https://github.com/mcpdev80/baseharbor/issues/994) requires correction and native retest before release. Implementation session must create/claim canonical task, link #988/#990, and sync generated release dependencies/views.
- #993 review [5562183275](https://github.com/mcpdev80/baseharbor/pull/993#pullrequestreview-5562183275) found a P1 hazard in its new unscoped-reset regression: HOME/XDG isolation does not isolate the script's absolute /tmp deletions. Contain those destructive commands before any further shared-host execution; #992 is not accepted.
- No new live execution or release acceptance by this reviewer. Preserve existing claims, metadata and generated views until the implementation owner's validated render.


### 2026-10-17 — Additional pre-release cleanup bug #992
- [Product bug #992](https://github.com/mcpdev80/baseharbor/issues/992) must be corrected and independently retested before v0.4.26 release. Source inspection at `78a72ebad0723eefe760090bc34130b55858d8a3` shows `ci-runtime-reset.sh podman <scope>` still removes entire selected XDG BaseHarbor state directories; only runtime resource selection is scoped.
- Do not use this scoped helper on shared XDG state as if it were isolated. No live cleanup was executed to establish the finding. Implementation belongs to a development session; executable disposable-sandbox regressions first, then independent review and Qwen native retest as appropriate. Preserve foreign resources and do not publish private machine identifiers.
- Create/claim the canonical bug task and synchronize release dependencies/views before implementation. This Handoff intake preserves all existing claims/generated metadata; no completed validation or resolution is claimed.


Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
