---
id: core-299
areas: [lifecycle]
type: feature
release: v0.5.x
version: v0.5.3
parent: v0.5.x
owner: ""
depends_on: [core-297, core-298]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#299"]
source_updated: "2026-10-15T16:53:58Z"
labels: [kind/feature, area/recovery, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-299 · Lifecycle: secure upgrades, recovery and deprecation #task #release/v0-5-x #status/planned #view/waiting #area/lifecycle #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-297](core-297-state-versioning-migration-compatibility.md), [core-298](core-298-contracts-cross-component-compatibility.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.5.x](../releases/v0.5.x.md) (v0.5.3)  
**Depends on:** [core-297](core-297-state-versioning-migration-compatibility.md), [core-298](core-298-contracts-cross-component-compatibility.md)  
**Required by:** [core-300](core-300-acceptance-portability-compatibility.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#299](https://github.com/mcpdev80/baseharbor/issues/299)
<!-- /generated:links -->

## Goal

Make upgrades predictable and recoverable while keeping the normal workflow simple — a safe upgrade should feel boring. Model: resolve version/state → preflight compatibility → recovery point where required → migrate/upgrade → verify → READY or actionable recovery state. Never report success before post-upgrade verification.

## Scope

- Scope: upgrade compatibility preflight; deterministic migration ordering; recovery point/backup where durable state is at risk; post-upgrade verification; rollback when technically safe; explicit recovery instructions otherwise; deprecation warnings; supported legacy reading; writers emit the canonical current form; removal tied to explicit contract-version changes.
- Deprecation model: compatible legacy input → keep reading → warn when actionable → write canonical form → remove only through the documented breaking-version policy; no warning noise for users who cannot or need not act.
- DX: patch/minor upgrades need no runbook; preflight catches incompatibility before mutation; errors name the blocker and the safest next action; no distributed/enterprise upgrade machinery before a real runtime needs it; recovery proportional to risk.
- Runtime-target upgrades must not move target/access settings into portable intent, require copying credentials into app config, silently claim platform-managed resources, or collapse unsupported/unverifiable/authorization outcomes into generic failure.
- Provider Catalog upgrades distinguish descriptor version, implementation version, Provider Protocol, service/capability contract, OCI digest and product/engine version (never implicitly coupled); digest changes are explicit artifact changes even with an unchanged tag; additive descriptor evolution preferred; deprecated catalog fields stay readable for the documented window; replacement preserves family semantics and ownership; rollback only to a previously verified identity where safe; diagnostics name the incompatible boundary.
- Comment (2026-09-23): communicate CLI version change, runtime image/API change, capability contract change, provider product/version change, state migration, workload rebuild requirement, persistent-data impact, rollback/recovery classification and whether application action is required. Concise normal output that still shows application-relevant changes; verbose/JSON/MCP expose image references, digests, migration IDs. Example: "Application capability: SQL unchanged · Provider realization: PostgreSQL 18.x → 18.y · Application impact: SQL contract unchanged".
- Out of scope: Kubernetes rolling upgrades, Operator upgrades, multi-node leader upgrades, cloud control-plane upgrades, OpenShift orchestration.

## Acceptance

- Deployment/runtime target migrations preserve access secrecy and platform ownership boundaries.
- Supported upgrade paths have non-mutating preflight.
- Risky durable-state changes establish an appropriate recovery path first.
- Post-upgrade verification gates success.
- Rollback/recovery behavior is documented per migration class.
- Deprecated compatible input remains usable according to the published policy.
- New writers emit the canonical current representation.
- Upgrade/deprecation output is concise and actionable.
- Failure tests cover incompatible state, migration failure and verification failure.
- No later-runtime upgrade machinery is introduced speculatively.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md`.
- Provider artifact/digest changes are visible in upgrade preflight.
- Provider descriptor deprecations follow the published compatibility policy.
- A compatible provider patch/minor upgrade does not require portable application changes.
- An incompatible provider/protocol/contract combination fails before mutation with an actionable recovery path.

## Required checks

- Economical local/repository validation per `docs/DEVELOPMENT_GUIDELINES.md`; no unnecessary GitHub Actions. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on the v0.5.0 freeze (#175), core-297 and core-298.

## Handoff

- Not started (future release).
