---
id: core-862
areas: [quality]
type: maintenance
release: v0.4.31
version: ""
parent: v0.4.31
owner: ""
depends_on: [t-20261017-release-0-4-31-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#862"]
source_updated: "2026-10-15T16:50:04Z"
labels: [kind/maintenance, area/security, area/evidence]
early: true
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-862 · Quality: staticcheck, govulncheck and risk-focused tests #task #release/v0-4-31 #status/planned #view/waiting #board/planned #area/quality #kind/maintenance
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-31-updates](t-20261017-release-0-4-31-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.31](../releases/v0.4.31.md)  
**Depends on:** [t-20261017-release-0-4-31-updates](t-20261017-release-0-4-31-updates.md)  
**Required by:** [t-20261017-release-0-4-31-prepare](t-20261017-release-0-4-31-prepare.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#862](https://github.com/mcpdev80/baseharbor/issues/862)
<!-- /generated:links -->

## Goal

Reproducible, low-noise static analysis, vulnerability checks and targeted coverage before the v0.5 freeze. A standalone bounded quality package, not a general refactor. Introduced as early as practical (from v0.4.25) and ratcheted in every release; **final cross-package completion and evidence belong to v0.4.31**.

## Scope

- **A — staticcheck:** version-pinned, compatible with the repo's Go toolchain; targeted/local first, then an existing CI workflow with useful diagnostics and caching. Fix actionable new findings on changed code; for legacy findings use a documented shrinking baseline or narrow justified suppressions, no sweeping or formatting-only churn. `go vet ./...` stays. `golangci-lint` only with a concrete remaining need.
- **B — govulncheck:** version-pinned against Go modules/packages with a precise reproducible local command. Gate on actionable reachable vulnerabilities; document non-reachable/inconclusive advisories separately with version/advisory/fix/evidence; exceptions have owners and review dates; never ignore silently. Respect workflow permissions and supply-chain conventions; no extra secrets or external credentials.
- **C — risk-focused tests:** measure actual package/function coverage first (a claimed 0% unit figure does not prove no runtime coverage). Prioritize uncovered real decision logic and failure paths in `health`, `providers/runtime/docker`, `provideroperation`, `providerui`, `stableid`, `database`, `exposure` as applicable on the current tree. Key cross-cutting cases: shared vs app-scoped ownership isolation, HA off by default, TLS always, configured-only destroy without deployed Core, cleanup and preservation, backup/recovery, typed CLI/MCP errors. Focused table-driven and negative tests (missing Core, partial state, wrong owner, retry/idempotency, disconnected provider). Keep runtime-dependent gates separate; never pretend opt-in integration ran. Per-package non-regressing coverage baselines for selected high-risk packages with a small documented improvement target; no global threshold; no brittle tests for generated adapters.
- **Workflow and CI:** one discoverable local entry point (script or make target only if warranted) matching CI commands; reuse existing atomic gates and fast test infrastructure; use Actions sparingly; no Docker/Podman/K3s release matrices to qualify static analysis; pinned tools, deterministic results, helpful errors; EN/DE docs.
- Out of scope: package consolidation, new providers, HA/recovery redesign, unrelated refactors, Kubernetes roadmap changes; no release, tag or merge without the separate release process.

## Acceptance

- staticcheck repeatably green with a reviewed baseline; `go vet` unchanged.
- govulncheck repeatably green for applicable reachable vulnerabilities, with documented management of non-actionable findings.
- Measured improvement and regression protection in targeted high-risk Go packages; representative negative tests.
- Local fast-check command and CI parity; EN/DE documentation.
- Evidence: workflow links with SHA, before/after coverage per selected package, actual findings and remediation/waivers, duration and noise impact, all tests green; no fake green from skipped checks; no unnecessary full-suite repetitions.

## Required checks

- The new gates themselves plus existing atomic Go checks.

## Dependencies and file ownership

- No open task dependencies. Coordinate CI workflow edits with the owner of `.github/workflows/ci.yml` (core-893 during v0.4.26). Related: core-903 (do not duplicate).

## Handoff

- Derived from a technical assessment on `release/v0.4.21`; coverage numbers and tool gaps must be re-verified on the current head. Title scope "[v0.4.x]" and the 2026-10-10 assignment note: start early, ratchet per release, finish in v0.4.31.
