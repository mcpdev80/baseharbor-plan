---
id: t-20261114-r28-cli2-audit-events
card_number: "0428-058"
card_short_title: "Audit secret and Env actions"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w058-0428-058-hop
kanban_status: active
kanban_lane: active
kanban_summary: "Audit secret and environment actions. Follow the owner working brief, command mapping and code entry index; revalidate current…"
kanban_title: 0428-058 · Audit secret and Env actions
priority: high
depends_on: [t-20261114-r28-cli2-env-delete, t-20261114-r28-cli2-env-policy, t-20261114-r28-cli2-env-registry, t-20261114-r28-cli2-identity-secrets]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1809]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-audit-events · CLI redesign: Audit secret and environment actions #task #release/v0-4-28 #status/active #view/active #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** w058-0428-058-hop · **Priority:** high  
    **PR:** [baseharbor#1809](https://github.com/mcpdev80/baseharbor/pull/1809)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-env-delete](t-20261114-r28-cli2-env-delete.md), [t-20261114-r28-cli2-env-policy](t-20261114-r28-cli2-env-policy.md), [t-20261114-r28-cli2-env-registry](t-20261114-r28-cli2-env-registry.md), [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
**Required by:** [t-20261114-r28-cli2-app-data](t-20261114-r28-cli2-app-data.md), [t-20261114-r28-cli2-final-acceptance](t-20261114-r28-cli2-final-acceptance.md), [t-20261114-r28-cli2-wizard-env](t-20261114-r28-cli2-wizard-env.md)  
**Owner:** w058-0428-058-hop  
**Priority:** high  
**PRs:** [baseharbor#1809](https://github.com/mcpdev80/baseharbor/pull/1809)  
**Source:** 
<!-- /generated:links -->

## Goal

Audit secret and environment actions. Follow the [owner working brief](../evidence/cli-redesign-20261114/brief.md), [command mapping](../evidence/cli-redesign-20261114/command-map.md) and [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md); revalidate current `develop` and the owner-approved contract. This task is a bounded slice of existing umbrella `t-20261114-r28-cli-command-semantics`, not a second independent product.

## Scope

Add auditable secret read/change and env edit/delete outcomes per configured policy. Track who/what/where/result without storing values; distinguish human and runtime actor, define storage/failure behavior per accepted contract.

## Entry points and ownership

- Starting points: `internal/evidence/; cmd/baha/secret_operations.go; environment domain audit hooks`. Verify exact current lines before changing files.
- Own only this slice and its dedicated tests; coordinate shared file writes and interface changes through the coordinator. `cmd/baha/commands.go`, shared parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their respective integration/CI owners. Do not edit another worker's reserved files concurrently.
- One task/branch/PR per worker. Stop when dependency or safe behavior is undecided; do not guess or quietly weaken policy. No Console/Node Connector public repo implementation.

## Acceptance

Success/denial/failed reveal and mutations, exact resource context, no credentials, retention/integrity promised only with actual proof; trusted local is not a person.

- Preserve authorization, ownership, consent, plan/preflight/apply/verify and semantic parity across supported interfaces. Unimplemented/unverified capabilities must be explicit; no secret values in Git, logs, audit or normal machine output.
- Use English CLI UX and actionable guided/noninteractive failures. Apply owner rule: as little as possible, as much as necessary.

## Required checks and handoff

- Before coding list exact test IDs/packages and fixture/runtime requirements for this slice; execute appropriate focused tests and record actual results at exact candidate SHA. If native Docker/Podman, real TLS or cross-repo proof is required by changed risk, unit fakes are not a substitute.
- Map every added/changed test to an existing CI check or native gate and its trigger. If routing is missing, coordinate with the CI owner and block acceptance until actual execution is proven. No parallel CI framework or indiscriminate full matrix.
- Handoff exact branch/PR/commit, tests → check/gate → trigger → actual result, remaining gaps, dependencies and shared-file conflicts. Codex/Owner-delegated Maintainer reviews and merges only after actual checks; never claim an independent review that did not occur. No release/tag authorized.

## Handoff

Planned and unassigned. No product implementation or acceptance yet.

dispatched post-recovery 2026-11-23

reconcile per Owner sweep: #1809 open under w058. Trusted Plan block = 0428-242 fail-loud catalog guardian on uncataloged cmd/baha/secret_audit_test.go + secret_operations.go (owner/CI-scope, card gate-catalog-residual-unblock-prs). H-V37: Draft Go reds on #1809 = STALE runs, not content. Lane: hold product, blocked on catalog card for the gate.

reconcile Owner sweep: #1809 open under w058. Trusted Plan block = 0428-242 catalog guardian on uncataloged cmd/baha/secret_audit_test.go+secret_operations.go (owner/CI scope, card 0428-260). H-V37: Draft Go reds = STALE. Lane hold product; gate blocked on 0428-260.

reclassified from active: H-V37 proved Draft Go reds stale; only the catalog guardian blocks

#1813 merged to develop (d4fa8c589): cmd/baha/secret_audit_test.go + secret_operations.go now cataloged -> guardian missing-path abort cleared. Lane routed the additive hop (merge develop d4fa8c589 into lane branch) + own exact Headed rerun. Code complete; H-V37: prior Draft Go reds stale. Should go green after hop.

RESTART (89ed2fab) of dead c9127cee. Branch lane-0428-058: additive hop to d4fa8c589 (#1813 rows) + exact Headed rerun; code complete.

Independent exact-head REVIEW on 3eed1ae8 = correction needed (audit-correctness bug): cmd/baha/secret_operations.go recordSecretAudit — an existing AuthorizationDecision with Allowed=false falls through to the PrincipalFromContext branch and records AuthorizationResult=allow while outcome=denial (verified principal can coexist with a policy denial) -> corrupts the audit record this PR adds. authorizeMCPOperation stores denied machine decisions in this enforcement context. FIX: any present decision must take precedence (deny must NOT fall back to principal allow); same pattern in the new env audit helper -> correct both if same contract. Add regression: verified principal + explicit denied decision -> authorization_result=deny. actor attribution safe. Require exact-head Hosted CI before merge. (Hosted green already: run 45273785058.)

Audit-precedence correction LANDED: head 2dfb66b3, exact-head run 45278870978 terminal GREEN (17 required pass / 13 advisory skipped / 0 fail); WithAuthorizationDecision helper + deny regression + env fix; evidence on origin/main. Ready for Owner exact-diff independent review (Codex not used per Owner directive; no merge under frost).

RUN TERMINAL GREEN: cleanup-stall self-resolved, run 45278870978 completed/success at exact head 2dfb66b (all validation + runtime assertions + cleanup + evidence-manifest/upload done). Fully green candidate in review -> ready for Owner external exact-diff accept. No Codex contact; no merge (frost).

Correction round 2 (maintainer review on 2dfb66b): acceptance requires success/denial/failed REVEAL auditing, but head adds NONE to authorizeHumanReveal (cmd/baha/secret_operations.go) or inspectApplicationEnvironment --reveal (environment_operations.go). creds has recordConnectionRevealAudit; env reveal + denied/failed reveals are unaudited. Fix: add matching reveal audit to BOTH paths recording outcome (success/denied/failed), mirror the creds pattern, tests for all three outcomes. Keep PR open until exact-head Hosted CI covers it. No merge (frost).

Correction bundle (2 independent review findings on 2dfb66b): A) reveal audit missing on authorizeHumanReveal + inspectApplicationEnvironment --reveal (need success/denied/failed). B) recordSecretAudit on the runtime branch keeps the person-like ActorFromContext default 'cli/local-operator' and labels AuthorizationResult=deny even on SUCCEEDED local runtime ops -> must set runtime actor (trusted-local != person) and AuthorizationResult matching the real outcome. Both fixes in one new head + tests; Hosted CI rerun required; PR stays open.

Correction round 3 (head bdbaabd5): A reveal audit fixed; B secret-audit actor/result fixed; C NEW cmd/baha/env_destroy.go recordEnvDestroyAudit no-decision/no-principal branch sets deny + no trusted-local actor even on success. Routed w058: mirror secret-audit (success->allow, runtime actor), Hosted regression assertion, exact-head green. Bundle A/B/C in one head; PR open; no merge; no Codex.

Correction round 3 bundle on bdbaabd5: A) reveal audit present but recordRevealSuccess fires at AUTHORIZATION, before env-file read/parse + creds/export release -> false success on later failure; fix = keep deny at auth seam, record success/failure at actual consumer outcome (or separate authorization-outcome event) + Hosted regressions (post-auth read failure; successful release). B) secret-audit runtime actor/result. C) env_destroy recordEnvDestroyAudit success->allow+trusted-local. One new head, exact-head Hosted, PR open; no merge; no Codex.

Reconciled head 41acb5f8 (run 45289726632 jobs green, workflow in_progress): finding C env_destroy (trusted-local+allow) FIXED. STILL OPEN: finding A premature-success — recordRevealSuccess fires inside authorizeHumanReveal right after auth, before consumer read/parse/release; later failure logs false success. Routed w058: move success audit to consumer outcome (+failure path), Hosted regressions for post-auth read failure + successful release. Held until green exact-head.
