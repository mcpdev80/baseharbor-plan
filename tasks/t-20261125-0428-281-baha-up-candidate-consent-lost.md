---
id: t-20261125-0428-281-baha-up-candidate-consent-lost
card_number: "0428-281"
card_short_title: "up loses candidate consent"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: w85-0428-281-consent
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-281 · up loses candidate consent
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/actions/runs/45398943139
  - https://github.com/mcpdev80/baseharbor/pull/1647
---

- [ ] t-20261125-0428-281-baha-up-candidate-consent-lost · baha up loses candidate consent #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w85-0428-281-consent · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45398943139), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1647)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w85-0428-281-consent  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem

- Where: the root `up` command (cmd/baha/app_up.go:41, Name "up") resolves through app_input_resolver.go (resolveApplication ... "up" at :602). On develop, `git grep confirmCandidate|confirm-candidate|candidateDigest` across the up path (app_up.go / app_input_resolver.go) finds NOTHING, while `baha app apply` (cmd/baha/app_apply.go:42,71,199-201) requires --confirm-candidate and FAILS CLOSED on a repository-owned candidate without it.
- Expected: when `up` performs an internal apply on a repository-owned candidate, the operator's candidate consent (--confirm-candidate <digest>) must be preserved and threaded through, exactly as in the never-merged fix commit 5f9c67102 ("fix: preserve candidate consent in root up").
- Actual: `up` drops the consent, the apply fails closed ("candidate consent required"), and the four candidate-binding Light gates fail: atomic/docker policy, connectivity, reconciliation, full-destroy (jobs under run 45398943139). guided/lifecycle/failure pass because they do not bind a repository candidate. The operator-auth admission itself is fixed (binary 475902075 admitted) — this is a DIFFERENT, product-side defect.

## Regression

- Port commit 5f9c67102 onto current develop: thread/preserve the candidate-consent digest through the `up` resolution path (cmd/baha/app_input_resolver.go ~+11 lines) so the internal apply receives --confirm-candidate and does not fail closed when consent was granted, and keep the fail-closed behaviour when consent was NOT granted.
- Add/restore the regression from 5f9c67102 (cmd/baha/runtime_repository_up_test.go ~+13 lines): assert that `up` with a confirmed candidate succeeds AND that `up` without confirmation still fails closed (no silent allow).

## Acceptance

- The v0.4.28 atomic/docker Light gates policy + connectivity + reconciliation + full-destroy go GREEN on the exact candidate head (previously failing only for this consent-propagation cause).
- A CI-discovered Go test asserts up preserves candidate consent (success when granted, fail-closed when not) per the 5f9c67102 test.
- Write-set is cmd/baha product code ONLY (app_input_resolver.go + runtime_repository_up_test.go). No .github/** or scripts/** change. This is a hard dependency for #1812's Docker+Podman Light gates and therefore for the serial chain #1812 -> #1819 -> #1820.

Owner-authorized SEPARATE consent PR (minimal 2-file shape of ref commit 5f9c671, re-derived on develop 46d3dccc1). FIRST dependency of the chain: consent PR green -> merge -> rebase #1812 -> Docker then Podman Light gates. #1812 stays blocked until this merges. Hosted CI only.
