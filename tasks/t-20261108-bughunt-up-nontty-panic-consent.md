---
id: t-20261108-bughunt-up-nontty-panic-consent
card_number: "0427-157"
card_short_title: "Up panics and consent gate fai"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w157-nonttyup
kanban_status: active
kanban_lane: active
kanban_summary: "No panic path: missing confirm input = clean usage error that PRINTS the exact --confirm-candidate hash; consent stage honors…"
kanban_title: 0427-157 · Up panics and consent gate fai
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-up-nontty-panic-consent · Bug Hunt v0.4.27: Non-TTY up panics #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w157-nonttyup · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w157-nonttyup  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
No panic path: missing confirm input = clean usage error that PRINTS the exact --confirm-candidate hash; consent stage honors --yes/non-TTY with the same fail-closed semantics as interactive; regressions both branches in the lifecycle/cli-surface group.

## Problem (source evidence in the dossier)
(a) baha up without --confirm-candidate panics with a Go stack trace and the confirm hash is never surfaced on non-TTY (BF-01, blocker candidate); (b) the two-stage provider-impact consent demands an interactive TTY and auto-fails even with --yes (BF-02). Source: hunt H-X2.

## Acceptance
No panic path: missing confirm input = clean usage error that PRINTS the exact --confirm-candidate hash; consent stage honors --yes/non-TTY with the same fail-closed semantics as interactive; regressions both branches in the lifecycle/cli-surface group.

## Dependencies and file ownership
None. Write-set: up consent/confirm flow cmd/baha.

## CI remediation — 2026-11-08 (0427-157)

- PR #1486: corrected unsafe implicit provider double-acknowledgement by `--yes`, preserving explicit two-stage consent and fail-closed delete path; candidate error retains typed usage error, exact digest and historical errors.Is sentinel. Head `1ed7b144e0375cf78cb865c81a3e75d1e502d470`, exact-head CI https://github.com/mcpdev80/baseharbor/actions/runs/42502776430. Keep active until terminal CI.

## CI-verified merge #1486 — 2026-11-08

- Product [PR #1486](https://github.com/mcpdev80/baseharbor/pull/1486) merged on develop as `e7f830873f8f6b4c0104183d9df7278431e1c316` from exact head `1ed7b144e0375cf78cb865c81a3e75d1e502d470`.
- [CI #42502776430](https://github.com/mcpdev80/baseharbor/actions/runs/42502776430) = SUCCESS: Go build/vet/unit, deployment checks, gofmt, native Docker/Podman destroy retry, final selected gate all passed.
- The panic-free, digest-bearing candidate consent error is fixed. **Two-stage provider-change consent remains explicit**; ordinary `--yes` intentionally does *not* silently authorize both acknowledgements because existing fail-closed policy/tests forbid it. The card remains active if a non-TTY scoped consent UX is still an acceptance requirement; it requires a separate, explicitly bound typed plan approval, not an implicit bypass.
